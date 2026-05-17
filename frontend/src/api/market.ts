import { apiClient } from './client'
import type { HeatmapItem, MarketIndex, MarketSentiment } from '../types/market'

export async function getMarketSentiment(): Promise<MarketSentiment> {
  const response = await apiClient.get<MarketSentiment>('/market/sentiment')
  return response.data
}

export async function getMarketIndices(): Promise<MarketIndex[]> {
  const response = await apiClient.get<MarketIndex[]>('/market/indices')
  return response.data
}

export async function getMarketHeatmap(): Promise<HeatmapItem[]> {
  const response = await apiClient.get<HeatmapItem[]>('/market/heatmap')
  return response.data
}
