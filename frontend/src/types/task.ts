export type TaskRunStatus = 'running' | 'success' | 'error' | 'missed'

export interface TaskRunRecord {
  run_id: string
  job_id: string
  job_name: string
  status: TaskRunStatus
  scheduled_at: string | null
  started_at: string | null
  finished_at: string | null
  duration_seconds: number | null
  message: string | null
}

export interface ScheduledTaskStatus {
  job_id: string
  name: string
  exists: boolean
  scheduler_running: boolean
  trigger: string | null
  next_run_time: string | null
  last_run: TaskRunRecord | null
  recent_runs: TaskRunRecord[]
}
