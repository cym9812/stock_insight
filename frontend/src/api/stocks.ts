import { apiClient } from './client'
import type { StockAnalysis, StockBarsResponse, StockListResponse } from '../types/stock'

export async function getStocks(): Promise<string[]> {
  const response = await apiClient.get<StockListResponse>('/stocks')
  return response.data.stocks
}

export async function getStockBars(ticker: string): Promise<StockBarsResponse> {
  const response = await apiClient.get<StockBarsResponse>(`/stocks/${ticker}/bars`)
  return response.data
}

export async function getStockAnalysis(ticker: string): Promise<StockAnalysis> {
  const response = await apiClient.get<StockAnalysis>(`/stocks/${ticker}/analysis`)
  return response.data
}
