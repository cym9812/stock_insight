export interface MarketSentiment {
  score: number
  label: string
  description: string
}

export interface MarketIndex {
  name: string
  value: string
  change: string
  data: number[]
}

export interface HeatmapItem {
  name: string
  value: number
  change: number
}
