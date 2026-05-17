import { apiClient } from './client'
import type { PortfolioOverview } from '../types/portfolio'

export async function getPortfolioOverview(): Promise<PortfolioOverview> {
  const response = await apiClient.get<PortfolioOverview>('/portfolio/overview')
  return response.data
}
