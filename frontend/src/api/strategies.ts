import { apiClient } from './client'
import type { BacktestResponse, RecommendationsResponse } from '../types/strategy'

export async function getRecommendations(): Promise<RecommendationsResponse> {
  const response = await apiClient.get<RecommendationsResponse>('/strategies/recommendations')
  return response.data
}

export async function getStrategyBacktest(strategyId = 'ai_daily'): Promise<BacktestResponse> {
  const response = await apiClient.get<BacktestResponse>('/strategies/backtest', {
    params: { strategy_id: strategyId },
  })
  return response.data
}
