export interface StockBar {
  code: string | null
  trade_time: string | null
  open: number | null
  high: number | null
  low: number | null
  close: number | null
  volume: number | null
}

export interface StockBarsResponse {
  ticker: string
  count: number
  data: StockBar[]
}

export interface StockListResponse {
  stocks: string[]
}

export interface RadarAnalysis {
  indicators: string[]
  values: number[]
}

export interface StockAnalysis {
  ticker: string
  radar: RadarAnalysis
  summary: string
  risks: string[]
}
