from app.core.scheduler import scheduler
from app.core.task_monitor import TaskRunRecord, task_execution_monitor
from app.schemas.task import ScheduledTaskStatusResponse, TaskRunRecordResponse

NEWS_ANALYSIS_JOB_ID = "market_news_monitor"


class TaskService:
    def get_news_analysis_status(self) -> ScheduledTaskStatusResponse:
        job = scheduler.get_job(NEWS_ANALYSIS_JOB_ID)
        last_run = task_execution_monitor.get_last_record(NEWS_ANALYSIS_JOB_ID)
        recent_runs = task_execution_monitor.get_records(NEWS_ANALYSIS_JOB_ID, limit=10)

        return ScheduledTaskStatusResponse(
            job_id=NEWS_ANALYSIS_JOB_ID,
            name=job.name if job is not None else "Market News Scraper & AI Analysis",
            exists=job is not None,
            scheduler_running=scheduler.running,
            trigger=str(job.trigger) if job is not None else None,
            next_run_time=getattr(job, "next_run_time", None) if job is not None else None,
            last_run=self._to_run_response(last_run) if last_run is not None else None,
            recent_runs=[self._to_run_response(record) for record in recent_runs],
        )

    def _to_run_response(self, record: TaskRunRecord) -> TaskRunRecordResponse:
        return TaskRunRecordResponse(
            run_id=record.run_id,
            job_id=record.job_id,
            job_name=record.job_name,
            status=record.status,
            scheduled_at=record.scheduled_at,
            started_at=record.started_at,
            finished_at=record.finished_at,
            duration_seconds=record.duration_seconds,
            message=record.message,
        )
