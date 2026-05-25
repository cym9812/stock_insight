<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader title="策略与选股" subtitle="信号、推荐与因子筛选">
      <template #actions>
        <div class="flex flex-wrap items-center gap-2 rounded-lg border border-border bg-card p-2">
          <SelectField v-model="filter.market" label="市场" :options="marketOptions" />
          <SelectField v-model="filter.winRate" label="胜率" :options="winRateOptions" />
          <Button>应用筛选</Button>
        </div>
      </template>
    </PageHeader>

    <section class="mb-4 grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-4">
      <PanelCard v-for="rec in filteredRecommendations" :key="rec.ticker">
        <div class="mb-3 flex items-center justify-between gap-3">
          <span class="text-xl font-black text-foreground">{{ rec.ticker }}</span>
          <span :class="['text-xs font-bold', getConfidenceColor(rec.confidence)]">{{ rec.confidence }}% 置信度</span>
        </div>
        <div :class="['mb-3 text-base font-black uppercase', rec.prediction === 'up' ? 'text-emerald-300' : 'text-rose-300']">
          {{ rec.prediction === 'up' ? '看多' : '看空' }}
        </div>
        <p class="mb-4 text-sm leading-6 text-muted-foreground">{{ rec.reason }}</p>
        <router-link :to="`/stock/${rec.ticker}`" class="text-sm font-bold text-sky-200 hover:text-sky-100">
          深度分析
        </router-link>
      </PanelCard>
    </section>

    <PanelCard class="mb-4">
      <template #header>
        <h3 class="m-0 text-sm font-semibold text-foreground">AI 策略表现（回测）</h3>
        <span class="text-xs text-muted-foreground">对比 S&P 500 指数</span>
      </template>
      <div ref="backtestChart" class="h-[340px] w-full"></div>
    </PanelCard>

    <PanelCard class="overflow-x-auto">
      <template #header><h3 class="m-0 text-sm font-semibold text-foreground">多因子选股</h3></template>
      <table class="w-full min-w-[760px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border text-left text-xs text-muted-foreground">
            <th class="px-3 py-2 font-semibold">代码</th>
            <th class="px-3 py-2 font-semibold">信号</th>
            <th class="px-3 py-2 font-semibold">市盈率（PE）</th>
            <th class="px-3 py-2 font-semibold">MACD 状态</th>
            <th class="px-3 py-2 font-semibold">RSI</th>
            <th class="px-3 py-2 font-semibold">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in screenerData" :key="stock.ticker" class="border-b border-border/70 hover:bg-secondary/25">
            <td class="px-3 py-3 font-bold">{{ stock.ticker }}</td>
            <td class="px-3 py-3"><MetricChip :tone="signalTone(stock.signalClass)" class="font-bold uppercase">{{ stock.signal }}</MetricChip></td>
            <td class="px-3 py-3">{{ stock.pe }}</td>
            <td class="px-3 py-3">{{ stock.macd }}</td>
            <td class="px-3 py-3">{{ stock.rsi }}</td>
            <td class="px-3 py-3"><Button variant="secondary" size="sm">跟踪</Button></td>
          </tr>
        </tbody>
      </table>
    </PanelCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { getRecommendations, getStrategyBacktest } from '@/api/strategies'
import Button from '@/components/ui/Button.vue'
import MetricChip from '@/components/ui/MetricChip.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import SelectField from '@/components/ui/SelectField.vue'
import { chartCategoryAxis, chartColors, chartGrid, chartTooltip, chartValueAxis } from '@/config/chartTheme'
import type { BacktestResponse, Recommendation } from '@/types/strategy'

const backtestChart = ref<HTMLElement | null>(null)
const recommendations = ref<Recommendation[]>([])
const backtestData = ref<BacktestResponse | null>(null)
const filter = ref({ market: 'all', winRate: '0' })

const marketOptions = [
  { label: '全部市场', value: 'all' },
  { label: '美股', value: 'us' },
  { label: 'A 股', value: 'cn' },
]

const winRateOptions = [
  { label: '最低胜率', value: '0' },
  { label: '> 70%', value: '70' },
  { label: '> 80%', value: '80' },
]

const screenerData = ref<Array<{ ticker: string; signal: string; signalClass: string; pe: string; macd: string; rsi: string }>>([])

const filteredRecommendations = computed(() => {
  return recommendations.value.filter(r => r.confidence >= parseInt(filter.value.winRate))
})

const getConfidenceColor = (conf: number) => {
  if (conf > 80) return 'text-emerald-300'
  if (conf > 60) return 'text-amber-200'
  return 'text-rose-300'
}

const signalTone = (value: string) => {
  if (value === 'buy' || value === 'strong-buy') return 'up'
  if (value === 'sell') return 'down'
  return 'warning'
}

const initBacktestChart = (data: BacktestResponse) => {
  if (!backtestChart.value) return
  const chart = echarts.init(backtestChart.value)
  chart.setOption({
    tooltip: chartTooltip,
    legend: { data: ['AI 策略', '基准'], textStyle: { color: chartColors.text } },
    grid: chartGrid,
    xAxis: {
      type: 'category',
      data: data.dates,
      ...chartCategoryAxis,
    },
    yAxis: {
      type: 'value',
      ...chartValueAxis,
    },
    series: [
      {
        name: 'AI 策略',
        type: 'line',
        data: data.returns,
        smooth: true,
        lineStyle: { width: 3, color: chartColors.accent },
        itemStyle: { color: chartColors.accent },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(125, 211, 252, 0.18)' },
            { offset: 1, color: 'transparent' },
          ]),
        },
      },
      {
        name: '基准',
        type: 'line',
        data: data.benchmark,
        smooth: true,
        lineStyle: { width: 2, color: chartColors.muted, type: 'dashed' },
        itemStyle: { color: chartColors.muted },
      },
    ],
  })
}

onMounted(async () => {
  try {
    const [recRes, backtestRes] = await Promise.all([
      getRecommendations(),
      getStrategyBacktest(),
    ])
    recommendations.value = recRes.recommendations
    backtestData.value = backtestRes
    initBacktestChart(backtestData.value)
  } catch (e) {
    console.error('加载策略数据失败', e)
  }
})
</script>
