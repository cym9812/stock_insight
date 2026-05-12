<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { CandlestickChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent, DataZoomComponent, GraphicComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { API_DATA } from '../config/api'

echarts.use([CandlestickChart, BarChart, GridComponent, TooltipComponent, TitleComponent, DataZoomComponent, GraphicComponent, CanvasRenderer])
const stocks = ref<string[]>([])
const selectedStock = ref<string>('')
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: any = null

const fetchStocks = async () => {
  try {
    const res = await axios.get(`${API_DATA}/stocks`)
    stocks.value = res.data.stocks
    if (stocks.value.length > 0) {
      selectedStock.value = stocks.value[0]
    }
  } catch (error) {
    console.error('Failed to fetch stocks:', error)
  }
}

const renderChart = (data: any[]) => {
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value, 'dark')
  }

  const categoryData = []
  const values = []
  const volumes = []

  for (let i = 0; i < data.length; i++) {
    const item = data[i]
    categoryData.push(item.trade_time.split('T')[0])
    // ECharts expects: [open, close, lowest, highest]
    values.push([item.open, item.close, item.low, item.high])
    volumes.push([i, item.volume, item.close > item.open ? 1 : -1])
  }

  const upColor = '#10b981'
  const downColor = '#ef4444'

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    grid: [
      { left: '5%', right: '3%', top: '5%', height: '60%' },
      { left: '5%', right: '3%', top: '70%', height: '20%' }
    ],
    xAxis: [
      {
        type: 'category',
        data: categoryData,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      },
      {
        type: 'category',
        gridIndex: 1,
        data: categoryData,
        axisLabel: { show: false }
      }
    ],
    yAxis: [
      { scale: true, splitArea: { show: false }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } } },
      { scale: true, gridIndex: 1, splitNumber: 2, axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false }, splitLine: { show: false } }
    ],
    dataZoom: [
      { type: 'inside', xAxisIndex: [0, 1], start: 50, end: 100 },
      { show: true, xAxisIndex: [0, 1], type: 'slider', top: '92%', start: 50, end: 100, backgroundColor: 'rgba(0,0,0,0)', dataBackground: { lineStyle: { opacity: 0 }, areaStyle: { opacity: 0 } }, selectedDataBackground: { lineStyle: { opacity: 0 }, areaStyle: { opacity: 0 } } }
    ],
    series: [
      {
        name: 'KLine',
        type: 'candlestick',
        data: values,
        itemStyle: {
          color: upColor,
          color0: downColor,
          borderColor: upColor,
          borderColor0: downColor
        }
      },
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: {
          color: (params: any) => params.data[2] === 1 ? upColor : downColor
        }
      }
    ]
  }
  chartInstance.setOption(option)
}

const fetchKLine = async () => {
  if (!selectedStock.value) return
  try {
    const res = await axios.get(`${API_DATA}/${selectedStock.value}`)
    renderChart(res.data.data)
  } catch (error) {
    console.error('Failed to fetch kline:', error)
  }
}

watch(selectedStock, fetchKLine)

onMounted(async () => {
  await fetchStocks()
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<template>
  <div class="kline-container glass-card">
    <header class="header">
      <h2>行情看板</h2>
      <div class="selector">
        <label>选择股票：</label>
        <select v-model="selectedStock" class="glass-select">
          <option v-for="s in stocks" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
    </header>
    <div ref="chartRef" class="chart-wrapper"></div>
  </div>
</template>

<style scoped>
.kline-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h2 {
  margin: 0;
  font-weight: 600;
}

.glass-select {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 8px;
  outline: none;
  font-family: inherit;
  font-size: 1rem;
  cursor: pointer;
  backdrop-filter: blur(4px);
}

.glass-select option {
  background: var(--bg-dark);
  color: var(--text-main);
}

.chart-wrapper {
  flex: 1;
  width: 100%;
  min-height: 400px;
}
</style>
