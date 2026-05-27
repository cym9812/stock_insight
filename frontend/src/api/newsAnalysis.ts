import { apiClient } from './client'
import type { NewsAnalysisResultsResponse } from '../types/newsAnalysis'

export interface GetNewsAnalysisResultsParams {
  page?: number
  page_size?: number
  sort_by?: string
  sort_dir?: string
  filter_type?: string
  start_date?: string | null
  end_date?: string | null
}


export async function getNewsAnalysisResults(
  params: GetNewsAnalysisResultsParams = {},
): Promise<NewsAnalysisResultsResponse> {
  const response = await apiClient.get<NewsAnalysisResultsResponse>('/news-analysis/results', {
    params,
  })
  return response.data
}

