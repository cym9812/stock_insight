export type NewsImpactDirection = 'positive' | 'negative' | 'neutral' | 'uncertain'
export type NewsScoreLevel = 'low' | 'medium' | 'high'

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
  summary: string
  event_type: string
  market_impact: NewsImpactDirection | string
  importance: NewsScoreLevel | string
  urgency: NewsScoreLevel | string
  sectors: NewsImpactItem[]
  companies: NewsImpactItem[]
  reasoning: string
  confidence: number
}

export interface NewsAnalysisResultsResponse {
  items: NewsAnalysisResultItem[]
}
