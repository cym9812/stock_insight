export type NewsImpactDirection = 'positive' | 'negative' | 'neutral' | 'uncertain'
export type NewsScoreLevel = 'low' | 'medium' | 'high'
export type NewsAnalysisStatus = 'pending' | 'analyzing' | 'analyzed' | 'failed'

export interface NewsImpactItem {
  name: string
  impact: NewsImpactDirection | string
  reason: string | null
  stock_code: string | null
}

export interface NewsAnalysisResultItem {
  news_id: number
  content: string
  source_url: string
  publish_time: number
  created_at: string
  analysis_status: NewsAnalysisStatus | string
  analysis_retry_count: number
  last_analysis_error: string | null
  summary: string | null
  event_type: string | null
  market_impact: NewsImpactDirection | string | null
  importance: NewsScoreLevel | string | null
  urgency: NewsScoreLevel | string | null
  sectors: NewsImpactItem[]
  companies: NewsImpactItem[]
  reasoning: string | null
  confidence: number | null
}

export interface NewsAnalysisResultsResponse {
  items: NewsAnalysisResultItem[]
}
