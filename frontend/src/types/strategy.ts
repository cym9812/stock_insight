export interface Recommendation {
  ticker: string
  prediction: 'up' | 'down'
  confidence: number
  reason: string
}

export interface RecommendationsResponse {
  date: string
  recommendations: Recommendation[]
}

export interface BacktestResponse {
  strategy_id: string
  returns: number[]
  benchmark: number[]
  dates: string[]
}
