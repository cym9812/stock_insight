import { apiClient } from './client'
import type { ScheduledTaskStatus } from '../types/task'

export async function getNewsAnalysisTaskStatus(): Promise<ScheduledTaskStatus> {
  const response = await apiClient.get<ScheduledTaskStatus>('/tasks/news-analysis/status')
  return response.data
}
