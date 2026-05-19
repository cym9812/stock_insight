import type { NewsAnalysisResultItem } from '../../types/newsAnalysis'

export function getImpactUi(impact: string) {
  if (impact === 'positive') {
    return {
      tone: 'up',
      label: 'Positive',
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
      label: 'Negative',
      railClass: 'border-rose-400/35 bg-rose-400/10',
      signalClass: 'bg-rose-400/12 text-rose-200',
      dotClass: 'bg-rose-300',
      textClass: 'text-rose-200',
      chipClass: 'border-rose-400/25 bg-rose-400/10 text-rose-200',
      cardClass: 'border-l-rose-300',
    }
  }
  return {
    tone: 'neutral',
    label: 'Neutral',
    railClass: 'border-slate-500/30 bg-slate-500/10',
    signalClass: 'bg-slate-500/12 text-slate-200',
    dotClass: 'bg-slate-300',
    textClass: 'text-slate-200',
    chipClass: 'border-slate-500/25 bg-slate-500/10 text-slate-200',
    cardClass: 'border-l-slate-500',
  }
}

export function getPriorityScore(item: NewsAnalysisResultItem) {
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
