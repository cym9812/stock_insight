<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader :title="selectedStock || '个股分析'">
      <template #actions>
        <span :class="['text-lg font-black', priceChange >= 0 ? 'text-emerald-300' : 'text-rose-300']">
          ${{ currentPrice }} ({{ priceChange }}%)
        </span>
        <SelectField v-model="selectedStock" label="代码" :options="stockOptions" />
      </template>
    </PageHeader>

    <div class="grid grid-cols-[minmax(0,1fr)_350px] gap-4 max-lg:grid-cols-1">
      <PanelCard>
        <template #header><h3 class="m-0 text-sm font-semibold text-foreground">超级 K 线</h3></template>
        <div ref="klineRef" class="h-[440px] w-full"></div>
      </PanelCard>

      <aside class="grid gap-4">
        <PanelCard>
          <template #header><h3 class="m-0 text-sm font-semibold text-foreground">多维分析</h3></template>
          <div ref="radarRef" class="h-[250px] w-full"></div>
        </PanelCard>

        <PanelCard class="min-h-64">
          <template #header>
            <div class="flex items-center gap-2">
              <Sparkles class="h-4 w-4 text-sky-200" />
              <h3 class="m-0 text-sm font-semibold text-foreground">AI 洞察</h3>
            </div>
          </template>
          <div v-if="loadingAnalysis" class="py-5 text-sm italic text-muted-foreground">正在生成洞察...</div>
          <div v-else>
            <p class="mb-4 text-sm leading-6 text-slate-300">{{ analysis.summary }}</p>
            <div>
              <h4 class="mb-2 text-sm font-bold text-rose-300">风险提示</h4>
              <ul class="m-0 space-y-2 pl-5 text-sm text-muted-foreground">
                <li v-for="risk in analysis.risks" :key="risk">{{ risk }}</li>
              </ul>
            </div>
          </div>
        </PanelCard>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { Sparkles } from '@lucide/vue'
import * as echarts from 'echarts'
import { useRoute } from 'vue-router'
import { getStockAnalysis, getStockBars, getStocks } from '@/api/stocks'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import SelectField from '@/components/ui/SelectField.vue'
import { chartCategoryAxis, chartColors, chartGrid, chartTooltip, chartValueAxis } from '@/config/chartTheme'
import type { StockAnalysis, StockBar } from '@/types/stock'

const route = useRoute()

const klineRef = ref<HTMLElement | null>(null)
const radarRef = ref<HTMLElement | null>(null)

const stocks = ref<string[]>([])
const stockOptions = computed(() => stocks.value.map(stock => ({ label: stock, value: stock })))
const selectedStock = ref<string>((route.params.ticker as string) || '')
const klineData = ref<StockBar[]>([])
const analysis = ref<StockAnalysis>({
  ticker: '',
  radar: { indicators: [], values: [] },
  summary: '',
  risks: [],
})
const loadingAnalysis = ref(false)

const currentPrice = ref(0)
const priceChange = ref(0)

const initKLine = (data: StockBar[]) => {
  if (!klineRef.value) return
  const chart = echarts.init(klineRef.value)

  const categoryData = data.map(d => d.trade_time?.split('T')[0] ?? '')
  const values = data.map(d => [d.open, d.close, d.low, d.high])

  chart.setOption({
    tooltip: { ...chartTooltip, axisPointer: { type: 'cross' } },
    grid: { ...chartGrid, bottom: 58 },
    xAxis: { type: 'category', data: categoryData, ...chartCategoryAxis },
    yAxis: { scale: true, ...chartValueAxis },
    dataZoom: [{ type: 'inside', start: 50, end: 100 }, { type: 'slider', start: 50, end: 100 }],
    series: [
      {
        type: 'candlestick',
        data: values,
        itemStyle: { color: chartColors.up, color0: chartColors.down, borderColor: chartColors.up, borderColor0: chartColors.down },
      },
    ],
  })
}

const initRadar = (data: StockAnalysis['radar']) => {
  if (!radarRef.value) return
  const chart = echarts.init(radarRef.value)
  chart.setOption({
    radar: {
      indicator: data.indicators.map((n: string) => ({ name: n, max: 100 })),
      splitArea: { show: false },
      axisName: { color: chartColors.muted },
      axisLine: { lineStyle: { color: chartColors.axis } },
      splitLine: { lineStyle: { color: chartColors.splitLine } },
    },
    series: [{
      type: 'radar',
      data: [{
        value: data.values,
        name: 'Analysis',
        areaStyle: { color: 'rgba(125, 211, 252, 0.18)' },
        lineStyle: { color: chartColors.accent },
        itemStyle: { color: chartColors.accent },
      }],
    }],
  })
}

const fetchData = async () => {
  if (!selectedStock.value) {
    loadingAnalysis.value = false
    return
  }
  loadingAnalysis.value = true
  try {
    const [klRes, anRes] = await Promise.all([
      getStockBars(selectedStock.value),
      getStockAnalysis(selectedStock.value),
    ])

    klineData.value = klRes.data
    analysis.value = anRes

    if (klineData.value.length > 1) {
      const last = klineData.value[klineData.value.length - 1]
      const prev = klineData.value[klineData.value.length - 2]
      if (last.close !== null && prev.close !== null && prev.close !== 0) {
        currentPrice.value = last.close
        priceChange.value = parseFloat((((last.close - prev.close) / prev.close) * 100).toFixed(2))
      }
    }

    await nextTick()
    initKLine(klineData.value)
    initRadar(analysis.value.radar)
  } catch (e) {
    console.error('Failed to fetch stock detail', e)
  } finally {
    loadingAnalysis.value = false
  }
}

onMounted(async () => {
  stocks.value = await getStocks()
  if (!selectedStock.value && stocks.value.length > 0) {
    selectedStock.value = stocks.value[0]
  }
  fetchData()
})

watch(selectedStock, fetchData)
</script>
