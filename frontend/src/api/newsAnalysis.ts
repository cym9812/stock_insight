import { apiClient } from './client'
import type { NewsAnalysisResultsResponse } from '../types/newsAnalysis'

export async function getNewsAnalysisResults(limit = 50): Promise<NewsAnalysisResultsResponse> {
  const response = await apiClient.get<NewsAnalysisResultsResponse>('/news-analysis/results', {
    params: { limit },
  })
  return response.data
}
