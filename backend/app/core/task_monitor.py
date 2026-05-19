from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from threading import Lock
from uuid import uuid4

from apscheduler.events import (
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_SUBMITTED,
    JobEvent,
    JobExecutionEvent,
    JobSubmissionEvent,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler


@dataclass
class TaskRunRecord:
    run_id: str
    job_id: str
    job_name: str
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    duration_seconds: float | None
    message: str | None = None


class TaskExecutionMonitor:
    def __init__(self, max_records: int = 200):
        self._max_records = max_records
        self._records: list[TaskRunRecord] = []
        self._lock = Lock()

    def mark_submitted(self, job_id: str, job_name: str, scheduled_at: datetime | None) -> None:
        with self._lock:
            self._records.append(
                TaskRunRecord(
                    run_id=uuid4().hex,
                    job_id=job_id,
                    job_name=job_name,
                    status="running",
                    scheduled_at=scheduled_at,
                    started_at=datetime.now(UTC),
                    finished_at=None,
                    duration_seconds=None,
                )
            )
            self._trim()

    def mark_finished(
        self,
        job_id: str,
        job_name: str,
        status: str,
        scheduled_at: datetime | None,
        message: str | None = None,
    ) -> None:
        finished_at = datetime.now(UTC)
        with self._lock:
            record = self._find_open_record(job_id, scheduled_at)
            if record is None:
                self._records.append(
                    TaskRunRecord(
                        run_id=uuid4().hex,
                        job_id=job_id,
                        job_name=job_name,
                        status=status,
                        scheduled_at=scheduled_at,
                        started_at=None,
                        finished_at=finished_at,
                        duration_seconds=None,
                        message=message,
                    )
                )
            else:
                record.status = status
                record.finished_at = finished_at
                record.message = message
                if record.started_at is not None:
                    record.duration_seconds = round((finished_at - record.started_at).total_seconds(), 3)
            self._trim()

    def get_records(self, job_id: str, limit: int = 20) -> list[TaskRunRecord]:
        with self._lock:
            records = [record for record in self._records if record.job_id == job_id]
            return list(reversed(records[-limit:]))

    def get_last_record(self, job_id: str) -> TaskRunRecord | None:
        with self._lock:
            for record in reversed(self._records):
                if record.job_id == job_id:
                    return record
        return None

    def _find_open_record(self, job_id: str, scheduled_at: datetime | None) -> TaskRunRecord | None:
        for record in reversed(self._records):
            if record.job_id != job_id or record.status != "running":
                continue
            if scheduled_at is None or record.scheduled_at == scheduled_at:
                return record
        return None

    def _trim(self) -> None:
        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records :]


task_execution_monitor = TaskExecutionMonitor()
_monitor_installed = False


def install_scheduler_monitor(scheduler: AsyncIOScheduler) -> None:
    global _monitor_installed
    if _monitor_installed:
        return

    def listener(event: JobEvent) -> None:
        job_name = _get_job_name(scheduler, event.job_id)
        if event.code == EVENT_JOB_SUBMITTED:
            if isinstance(event, JobSubmissionEvent) and event.scheduled_run_times:
                for scheduled_at in event.scheduled_run_times:
                    task_execution_monitor.mark_submitted(event.job_id, job_name, scheduled_at)
            else:
                task_execution_monitor.mark_submitted(event.job_id, job_name, None)
            return

        if event.code == EVENT_JOB_EXECUTED:
            scheduled_at = event.scheduled_run_time if isinstance(event, JobExecutionEvent) else None
            task_execution_monitor.mark_finished(event.job_id, job_name, "success", scheduled_at)
            return

        if event.code == EVENT_JOB_ERROR:
            execution = event if isinstance(event, JobExecutionEvent) else None
            scheduled_at = execution.scheduled_run_time if execution is not None else None
            message = repr(execution.exception) if execution is not None else "Job failed"
            task_execution_monitor.mark_finished(event.job_id, job_name, "error", scheduled_at, message)
            return

        if event.code == EVENT_JOB_MISSED:
            scheduled_at = event.scheduled_run_time if isinstance(event, JobExecutionEvent) else None
            task_execution_monitor.mark_finished(event.job_id, job_name, "missed", scheduled_at, "Run missed")

    scheduler.add_listener(
        listener,
        EVENT_JOB_SUBMITTED | EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED,
    )
    _monitor_installed = True


def _get_job_name(scheduler: AsyncIOScheduler, job_id: str) -> str:
    job = scheduler.get_job(job_id)
    if job is None:
        return job_id
    return job.name or job.id
