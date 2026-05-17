<template>
  <div class="dashboard animate-fade-in">
    <header class="dashboard-header">
      <h1 class="text-gradient">Market Overview</h1>
      <p class="text-muted">Real-time market sentiment and index performance</p>
    </header>

    <div class="grid-layout main-grid">
      <!-- Market Sentiment -->
      <section class="glass-card sentiment-card">
        <h3>Market Sentiment</h3>
        <div ref="sentimentGauge" class="chart-container"></div>
        <div class="sentiment-info">
          <span class="sentiment-label" :class="sentiment.label.toLowerCase()">{{ sentiment.label }}</span>
          <p>{{ sentiment.description }}</p>
        </div>
      </section>

      <!-- Index Cards -->
      <div class="indices-grid">
        <div v-for="idx in indices" :key="idx.name" class="glass-card index-card">
          <div class="index-info">
            <span class="index-name">{{ idx.name }}</span>
            <span class="index-value">{{ idx.value }}</span>
            <span class="index-change" :class="idx.change.startsWith('+') ? 'up' : 'down'">
              {{ idx.change }}
            </span>
          </div>
          <div :ref="el => setIndexChartRef(el, idx.name)" class="mini-chart"></div>
        </div>
      </div>

      <!-- Heatmap -->
      <section class="glass-card heatmap-card">
        <h3>Market Heatmap (Sectors)</h3>
        <div ref="heatmapChart" class="chart-container"></div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { getMarketHeatmap, getMarketIndices, getMarketSentiment } from '../api/market';
import type { HeatmapItem, MarketIndex, MarketSentiment } from '../types/market';

const sentimentGauge = ref<HTMLElement | null>(null);
const heatmapChart = ref<HTMLElement | null>(null);
const indexChartRefs = ref<Record<string, HTMLElement>>({});

const sentiment = ref<MarketSentiment>({ score: 0, label: 'Neutral', description: '' });
const indices = ref<MarketIndex[]>([]);
const sectors = ref<HeatmapItem[]>([]);

const setIndexChartRef = (el: any, name: string) => {
  if (el) indexChartRefs.value[name] = el;
};

const initSentimentGauge = (score: number) => {
  if (!sentimentGauge.value) return;
  const chart = echarts.init(sentimentGauge.value);
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
          { offset: 0, color: '#ef4444' },
          { offset: 0.5, color: '#f59e0b' },
          { offset: 1, color: '#10b981' }
        ])
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
        color: '#f8fafc',
        fontSize: 32,
        offsetCenter: [0, '20%']
      },
      data: [{ value: score }]
    }]
  });
};

const initMiniChart = (el: HTMLElement, data: number[], color: string) => {
  const chart = echarts.init(el);
  chart.setOption({
    grid: { left: 0, right: 0, top: 0, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 'dataMin', max: 'dataMax' },
    series: [{
      data: data,
      type: 'line',
      smooth: true,
      showSymbol: false,
      lineStyle: { color: color, width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: color + '44' },
          { offset: 1, color: 'transparent' }
        ])
      }
    }]
  });
};

const initHeatmap = (data: HeatmapItem[]) => {
  if (!heatmapChart.value) return;
  const chart = echarts.init(heatmapChart.value);
  chart.setOption({
    tooltip: { formatter: '{b}: {c}%' },
    series: [{
      type: 'treemap',
      data: data.map(d => ({
        name: d.name,
        value: d.value,
        itemStyle: {
          color: d.change > 0 ? `rgba(16, 185, 129, ${Math.min(d.change / 5 + 0.3, 1)})` : `rgba(244, 63, 94, ${Math.min(Math.abs(d.change) / 5 + 0.3, 1)})`
        }
      })),
      breadcrumb: { show: false },
      label: { show: true, formatter: '{b}\n{c}%' }
    }]
  });
};

onMounted(async () => {
  try {
    const [sentimentData, indexData, heatmapData] = await Promise.all([
      getMarketSentiment(),
      getMarketIndices(),
      getMarketHeatmap()
    ]);

    sentiment.value = sentimentData;
    indices.value = indexData;
    sectors.value = heatmapData;

    await nextTick();
    initSentimentGauge(sentiment.value.score);
    initHeatmap(sectors.value);

    indices.value.forEach(idx => {
      const el = indexChartRefs.value[idx.name];
      if (el) {
        const color = idx.change.startsWith('+') ? '#10b981' : '#f43f5e';
        initMiniChart(el, idx.data, color);
      }
    });
  } catch (e) {
    console.error('Failed to fetch dashboard data', e);
  }
});
</script>

<style scoped>
.dashboard {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin: 0;
  font-weight: 800;
}

.main-grid {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
}

.sentiment-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-container {
  width: 100%;
  height: 250px;
}

.sentiment-info {
  text-align: center;
  margin-top: -20px;
}

.sentiment-label {
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
}

.sentiment-label.greed { color: var(--up-color); }
.sentiment-label.fear { color: var(--down-color); }

.indices-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.index-card {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.index-info {
  display: flex;
  flex-direction: column;
}

.index-name {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.index-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.index-change {
  font-weight: 600;
}

.mini-chart {
  width: 120px;
  height: 50px;
}

.heatmap-card {
  grid-column: span 2;
  padding: 24px;
}

.heatmap-card .chart-container {
  height: 400px;
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
  .heatmap-card {
    grid-column: span 1;
  }
}
</style>
