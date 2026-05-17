<template>
  <div class="stock-detail animate-fade-in">
    <header class="detail-header">
      <div class="stock-title">
        <h1 class="text-gradient">{{ selectedStock }}</h1>
        <span class="stock-price" :class="priceChange >= 0 ? 'up' : 'down'">
          ${{ currentPrice }} ({{ priceChange }}%)
        </span>
      </div>
      <div class="selector glass-card">
        <select v-model="selectedStock">
          <option v-for="s in stocks" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
    </header>

    <div class="detail-grid">
      <!-- Main Chart Section -->
      <section class="glass-card chart-section">
        <div class="chart-header">
          <h3>Super K-Line</h3>
        </div>
        <div ref="klineRef" class="main-chart"></div>
      </section>

      <!-- Sidebar Analysis -->
      <aside class="sidebar-grid">
        <!-- Hexagon/Radar Chart -->
        <section class="glass-card radar-section">
          <h3>Multi-dimension Analysis</h3>
          <div ref="radarRef" class="radar-chart"></div>
        </section>

        <!-- AI Summary Panel -->
        <section class="glass-card ai-summary-section">
          <div class="ai-header">
            <span class="ai-icon">✨</span>
            <h3>AI Insight</h3>
          </div>
          <div v-if="loadingAnalysis" class="loading">Generating insights...</div>
          <div v-else class="ai-content">
            <p class="summary">{{ analysis.summary }}</p>
            <div class="risk-alerts">
              <h4>Risk Alerts</h4>
              <ul>
                <li v-for="risk in analysis.risks" :key="risk">{{ risk }}</li>
              </ul>
            </div>
          </div>
        </section>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import * as echarts from 'echarts';
import { useRoute } from 'vue-router';
import { getStockAnalysis, getStockBars, getStocks } from '../api/stocks';
import type { StockAnalysis, StockBar } from '../types/stock';

const route = useRoute();

const klineRef = ref<HTMLElement | null>(null);
const radarRef = ref<HTMLElement | null>(null);

const stocks = ref<string[]>([]);
const selectedStock = ref<string>((route.params.ticker as string) || '');
const klineData = ref<StockBar[]>([]);
const analysis = ref<StockAnalysis>({
  ticker: '',
  radar: { indicators: [], values: [] },
  summary: '',
  risks: []
});
const loadingAnalysis = ref(false);

const currentPrice = ref(0);
const priceChange = ref(0);

const initKLine = (data: StockBar[]) => {
  if (!klineRef.value) return;
  const chart = echarts.init(klineRef.value);
  
  const categoryData = data.map(d => d.trade_time?.split('T')[0] ?? '');
  const values = data.map(d => [d.open, d.close, d.low, d.high]);
  
  chart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    grid: { left: '5%', right: '5%', bottom: '15%' },
    xAxis: { type: 'category', data: categoryData, axisLine: { lineStyle: { color: '#475569' } } },
    yAxis: { scale: true, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
    dataZoom: [{ type: 'inside', start: 50, end: 100 }, { type: 'slider', start: 50, end: 100 }],
    series: [
      {
        type: 'candlestick',
        data: values,
        itemStyle: { color: '#10b981', color0: '#f43f5e', borderColor: '#10b981', borderColor0: '#f43f5e' }
      }
    ]
  });
};

const initRadar = (data: StockAnalysis['radar']) => {
  if (!radarRef.value) return;
  const chart = echarts.init(radarRef.value);
  chart.setOption({
    radar: {
      indicator: data.indicators.map((n: string) => ({ name: n, max: 100 })),
      splitArea: { show: false },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: data.values,
        name: 'Analysis',
        areaStyle: { color: 'rgba(56, 189, 248, 0.3)' },
        lineStyle: { color: '#38bdf8' },
        itemStyle: { color: '#38bdf8' }
      }]
    }]
  });
};

const fetchData = async () => {
  if (!selectedStock.value) {
    loadingAnalysis.value = false;
    return;
  }
  loadingAnalysis.value = true;
  try {
    const [klRes, anRes] = await Promise.all([
      getStockBars(selectedStock.value),
      getStockAnalysis(selectedStock.value)
    ]);
    
    klineData.value = klRes.data;
    analysis.value = anRes;
    
    if (klineData.value.length > 1) {
      const last = klineData.value[klineData.value.length - 1];
      const prev = klineData.value[klineData.value.length - 2];
      if (last.close !== null && prev.close !== null && prev.close !== 0) {
        currentPrice.value = last.close;
        priceChange.value = parseFloat(((last.close - prev.close) / prev.close * 100).toFixed(2));
      }
    }

    await nextTick();
    initKLine(klineData.value);
    initRadar(analysis.value.radar);
  } catch (e) {
    console.error('Failed to fetch stock detail', e);
  } finally {
    loadingAnalysis.value = false;
  }
};

onMounted(async () => {
  stocks.value = await getStocks();
  if (!selectedStock.value && stocks.value.length > 0) {
    selectedStock.value = stocks.value[0];
  }
  fetchData();
});

watch(selectedStock, fetchData);
</script>

<style scoped>
.stock-detail {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.stock-title h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 800;
}

.stock-price {
  font-size: 1.25rem;
  font-weight: 600;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 24px;
}

.chart-section {
  padding: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.main-chart {
  width: 100%;
  height: 500px;
}

.sidebar-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.radar-section {
  padding: 20px;
}

.radar-chart {
  width: 100%;
  height: 250px;
}

.ai-summary-section {
  padding: 24px;
  flex: 1;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.ai-icon { font-size: 1.5rem; }

.ai-content .summary {
  line-height: 1.6;
  color: var(--text-main);
  margin-bottom: 20px;
}

.risk-alerts h4 {
  color: var(--down-color);
  margin-bottom: 12px;
}

.risk-alerts ul {
  padding-left: 20px;
  color: var(--text-muted);
}

.risk-alerts li {
  margin-bottom: 8px;
}

.selector {
  padding: 8px 16px;
}

.selector select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-main);
  padding: 8px 16px;
  border-radius: 8px;
  outline: none;
  font-family: inherit;
  font-size: 1rem;
  cursor: pointer;
}

.selector select option {
  background: var(--bg-dark);
  color: var(--text-main);
}

.loading {
  color: var(--text-muted);
  font-style: italic;
  padding: 20px 0;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
