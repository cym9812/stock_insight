export interface WatchlistItem {
  ticker: string
  price: number
  change: string
  suggestion: string
}

export interface HoldingItem {
  ticker: string
  avg_price: number
  current_price: number
  profit_pct: number
}

export interface PortfolioOverview {
  watchlist: WatchlistItem[]
  holdings: HoldingItem[]
}
