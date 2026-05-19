export const chartColors = {
  accent: '#7dd3fc',
  accentStrong: '#38bdf8',
  up: '#34d399',
  down: '#fb7185',
  warning: '#fbbf24',
  text: '#e6edf6',
  muted: '#8996a8',
  faint: '#5f6d80',
  axis: 'rgba(148, 163, 184, 0.28)',
  splitLine: 'rgba(148, 163, 184, 0.12)',
}

export const chartGrid = {
  left: '3%',
  right: '3%',
  top: 28,
  bottom: 28,
  containLabel: true,
}

export const chartTooltip = {
  trigger: 'axis',
  backgroundColor: '#111620',
  borderColor: 'rgba(148, 163, 184, 0.18)',
  textStyle: { color: chartColors.text },
}

export const chartCategoryAxis = {
  axisLine: { lineStyle: { color: chartColors.axis } },
  axisLabel: { color: chartColors.muted },
  axisTick: { show: false },
}

export const chartValueAxis = {
  axisLine: { show: false },
  axisLabel: { color: chartColors.muted },
  splitLine: { lineStyle: { color: chartColors.splitLine } },
}
