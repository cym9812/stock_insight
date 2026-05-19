<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader title="Market Overview" subtitle="Real-time market sentiment and index performance" />

    <div class="grid grid-cols-2 gap-4 max-lg:grid-cols-1">
      <PanelCard>
        <template #header><h3 class="m-0 text-sm font-semibold text-foreground">Market Sentiment</h3></template>
        <div ref="sentimentGauge" class="h-[230px] w-full"></div>
        <div class="-mt-5 text-center">
          <span :class="['text-xl font-black uppercase', sentiment.label.toLowerCase() === 'fear' ? 'text-rose-300' : 'text-emerald-300']">
            {{ sentiment.label }}
          </span>
          <p class="mt-2 text-sm text-muted-foreground">{{ sentiment.description }}</p>
        </div>
      </PanelCard>

      <div class="grid gap-2.5">
        <PanelCard v-for="idx in indices" :key="idx.name" class="flex items-center justify-between">
          <div class="flex flex-col">
            <span class="text-sm font-medium text-muted-foreground">{{ idx.name }}</span>
            <span class="text-2xl font-black text-foreground">{{ idx.value }}</span>
            <span :class="['text-sm font-bold', idx.change.startsWith('+') ? 'text-emerald-300' : 'text-rose-300']">
              {{ idx.change }}
            </span>
          </div>
          <div :ref="el => setIndexChartRef(el, idx.name)" class="h-[50px] w-[120px]"></div>
        </PanelCard>
      </div>

      <PanelCard class="col-span-2 max-lg:col-span-1">
        <template #header><h3 class="m-0 text-sm font-semibold text-foreground">Market Heatmap (Sectors)</h3></template>
        <div ref="heatmapChart" class="h-[360px] w-full"></div>
      </PanelCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { getMarketHeatmap, getMarketIndices, getMarketSentiment } from '@/api/market'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import { chartColors } from '@/config/chartTheme'
import type { HeatmapItem, MarketIndex, MarketSentiment } from '@/types/market'

const sentimentGauge = ref<HTMLElement | null>(null)
const heatmapChart = ref<HTMLElement | null>(null)
const indexChartRefs = ref<Record<string, HTMLElement>>({})

const sentiment = ref<MarketSentiment>({ score: 0, label: 'Neutral', description: '' })
const indices = ref<MarketIndex[]>([])
const sectors = ref<HeatmapItem[]>([])

const setIndexChartRef = (el: unknown, name: string) => {
  if (el instanceof HTMLElement) indexChartRefs.value[name] = el
}

const initSentimentGauge = (score: number) => {
  if (!sentimentGauge.value) return
  const chart = echarts.init(sentimentGauge.value)
  chart.setOption({
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 5,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: chartColors.down },
          { offset: 0.5, color: chartColors.warning },
          { offset: 1, color: chartColors.up },
        ]),
      },
      progress: { show: true, width: 12 },
      pointer: { show: true, length: '60%', width: 5 },
      axisLine: { lineStyle: { width: 12 } },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: {
        valueAnimation: true,
        formatter: '{value}',
        color: chartColors.text,
        fontSize: 32,
        offsetCenter: [0, '20%'],
      },
      data: [{ value: score }],
    }],
  })
}

const initMiniChart = (el: HTMLElement, data: number[], color: string) => {
  const chart = echarts.init(el)
  chart.setOption({
    grid: { left: 0, right: 0, top: 0, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 'dataMin', max: 'dataMax' },
    series: [{
      data,
      type: 'line',
      smooth: true,
      showSymbol: false,
      lineStyle: { color, width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: `${color}44` },
          { offset: 1, color: 'transparent' },
        ]),
      },
    }],
  })
}

const initHeatmap = (data: HeatmapItem[]) => {
  if (!heatmapChart.value) return
  const chart = echarts.init(heatmapChart.value)
  chart.setOption({
    tooltip: { formatter: '{b}: {c}%' },
    series: [{
      type: 'treemap',
      data: data.map(d => ({
        name: d.name,
        value: d.value,
        itemStyle: {
          color: d.change > 0
            ? `rgba(52, 211, 153, ${Math.min(d.change / 5 + 0.3, 1)})`
            : `rgba(251, 113, 133, ${Math.min(Math.abs(d.change) / 5 + 0.3, 1)})`,
        },
      })),
      breadcrumb: { show: false },
      label: { show: true, formatter: '{b}\n{c}%' },
    }],
  })
}

onMounted(async () => {
  try {
    const [sentimentData, indexData, heatmapData] = await Promise.all([
      getMarketSentiment(),
      getMarketIndices(),
      getMarketHeatmap(),
    ])

    sentiment.value = sentimentData
    indices.value = indexData
    sectors.value = heatmapData

    await nextTick()
    initSentimentGauge(sentiment.value.score)
    initHeatmap(sectors.value)

    indices.value.forEach(idx => {
      const el = indexChartRefs.value[idx.name]
      if (el) {
        const color = idx.change.startsWith('+') ? chartColors.up : chartColors.down
        initMiniChart(el, idx.data, color)
      }
    })
  } catch (e) {
    console.error('Failed to fetch dashboard data', e)
  }
})
</script>
