import type { NewsAnalysisResultItem } from '../../types/newsAnalysis'

export function isAnalyzed(item: NewsAnalysisResultItem) {
  return item.analysis_status === 'analyzed'
}

export function getDisplayImpact(item: NewsAnalysisResultItem) {
  if (item.analysis_status === 'failed') return 'failed'
  if (item.analysis_status === 'pending' || item.analysis_status === 'analyzing') return 'pending'
  return item.market_impact ?? 'neutral'
}

export function getImpactUi(impact: string | null) {
  if (impact === 'positive') {
    return {
      tone: 'up',
      label: '利好',
      railClass: 'border-emerald-400/35 bg-emerald-400/10',
      signalClass: 'bg-emerald-400/12 text-emerald-200',
      dotClass: 'bg-emerald-300',
      textClass: 'text-emerald-200',
      chipClass: 'border-emerald-400/25 bg-emerald-400/10 text-emerald-200',
      cardClass: 'border-l-emerald-300',
    }
  }
  if (impact === 'negative') {
    return {
      tone: 'down',
      label: '利空',
      railClass: 'border-rose-400/35 bg-rose-400/10',
      signalClass: 'bg-rose-400/12 text-rose-200',
      dotClass: 'bg-rose-300',
      textClass: 'text-rose-200',
      chipClass: 'border-rose-400/25 bg-rose-400/10 text-rose-200',
      cardClass: 'border-l-rose-300',
    }
  }
  if (impact === 'pending') {
    return {
      tone: 'neutral',
      label: '待分析',
      railClass: 'border-sky-300/25 bg-sky-300/8',
      signalClass: 'bg-sky-300/10 text-sky-100',
      dotClass: 'bg-sky-300',
      textClass: 'text-sky-100',
      chipClass: 'border-sky-300/25 bg-sky-300/10 text-sky-100',
      cardClass: 'border-l-sky-400/70',
    }
  }
  if (impact === 'failed') {
    return {
      tone: 'down',
      label: 'AI 失败',
      railClass: 'border-amber-300/25 bg-amber-300/8',
      signalClass: 'bg-amber-300/10 text-amber-100',
      dotClass: 'bg-amber-300',
      textClass: 'text-amber-100',
      chipClass: 'border-amber-300/25 bg-amber-300/10 text-amber-100',
      cardClass: 'border-l-amber-300/70',
    }
  }
  return {
    tone: 'neutral',
    label: '中性',
    railClass: 'border-slate-500/30 bg-slate-500/10',
    signalClass: 'bg-slate-500/12 text-slate-200',
    dotClass: 'bg-slate-300',
    textClass: 'text-slate-200',
    chipClass: 'border-slate-500/25 bg-slate-500/10 text-slate-200',
    cardClass: 'border-l-slate-500',
  }
}

export function getPriorityScore(item: NewsAnalysisResultItem) {
  if (!isAnalyzed(item) || item.importance === null || item.urgency === null || item.confidence === null) {
    return null
  }
  const weight: Record<string, number> = { high: 3, medium: 2, low: 1 }
  const importance = weight[item.importance] ?? 1
  const urgency = weight[item.urgency] ?? 1
  return Math.min(100, Math.round(importance * 26 + urgency * 16 + item.confidence * 18))
}

export function isExpandableNews(content: string) {
  return content.trim().length > 72
}

export function formatUnixSeconds(value: number) {
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date(value * 1000))
}
