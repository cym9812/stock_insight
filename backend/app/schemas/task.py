from datetime import datetime

from pydantic import BaseModel


class TaskRunRecordResponse(BaseModel):
    run_id: str
    job_id: str
    job_name: str
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    duration_seconds: float | None
    message: str | None = None


class ScheduledTaskStatusResponse(BaseModel):
    job_id: str
    name: str
    exists: bool
    scheduler_running: bool
    trigger: str | None
    next_run_time: datetime | None
    last_run: TaskRunRecordResponse | None
    recent_runs: list[TaskRunRecordResponse]
