<template>
  <div class="strategy-view animate-fade-in">
    <header class="view-header">
      <h1 class="text-gradient">Strategy & Screener</h1>
      <div class="filters glass-card">
        <select v-model="filter.market">
          <option value="all">All Markets</option>
          <option value="us">US Stocks</option>
          <option value="cn">A-Share</option>
        </select>
        <select v-model="filter.winRate">
          <option value="0">Min Win Rate</option>
          <option value="70"> > 70%</option>
          <option value="80"> > 80%</option>
        </select>
        <button class="btn-primary">Apply Filters</button>
      </div>
    </header>

    <!-- Strategy List -->
    <section class="strategy-list grid-layout">
      <div v-for="rec in filteredRecommendations" :key="rec.ticker" class="glass-card recommendation-card">
        <div class="card-header">
          <span class="ticker">{{ rec.ticker }}</span>
          <span class="confidence" :style="{ color: getConfidenceColor(rec.confidence) }">
            {{ rec.confidence }}% Confidence
          </span>
        </div>
        <div class="prediction" :class="rec.prediction">
          {{ rec.prediction === 'up' ? '▲ BULLISH' : '▼ BEARISH' }}
        </div>
        <p class="reason">{{ rec.reason }}</p>
        <div class="card-footer">
          <router-link :to="`/stock/${rec.ticker}`" class="btn-link">Deep Dive →</router-link>
        </div>
      </div>
    </section>

    <!-- Performance Backtest -->
    <section class="glass-card backtest-section">
      <div class="section-header">
        <h3>AI Strategy Performance (Backtest)</h3>
        <span class="text-muted">vs. S&P 500 Index</span>
      </div>
      <div ref="backtestChart" class="chart-container"></div>
    </section>

    <!-- Screener Table -->
    <section class="glass-card screener-section">
      <h3>Multi-factor Screener</h3>
      <table class="screener-table">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Signal</th>
            <th>PE Ratio</th>
            <th>MACD Status</th>
            <th>RSI</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in screenerData" :key="stock.ticker">
            <td><strong>{{ stock.ticker }}</strong></td>
            <td><span class="tag" :class="stock.signalClass">{{ stock.signal }}</span></td>
            <td>{{ stock.pe }}</td>
            <td>{{ stock.macd }}</td>
            <td>{{ stock.rsi }}</td>
            <td><button class="btn-small">Track</button></td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';
import { API_DATA } from '../config/api';

const backtestChart = ref<HTMLElement | null>(null);
const recommendations = ref<any[]>([]);
const backtestData = ref<any>(null);
const filter = ref({ market: 'all', winRate: '0' });

const screenerData = ref([
  { ticker: 'NVDA', signal: 'Strong Buy', signalClass: 'strong-buy', pe: '75.2', macd: 'Golden Cross', rsi: '62' },
  { ticker: 'AMD', signal: 'Buy', signalClass: 'buy', pe: '42.1', macd: 'Neutral', rsi: '55' },
  { ticker: 'INTC', signal: 'Sell', signalClass: 'sell', pe: '18.5', macd: 'Death Cross', rsi: '38' },
  { ticker: 'MSFT', signal: 'Hold', signalClass: 'hold', pe: '35.4', macd: 'Neutral', rsi: '50' },
]);

const filteredRecommendations = computed(() => {
  return recommendations.value.filter(r => r.confidence >= parseInt(filter.value.winRate));
});

const getConfidenceColor = (conf: number) => {
  if (conf > 80) return '#10b981';
  if (conf > 60) return '#f59e0b';
  return '#f43f5e';
};

const initBacktestChart = (data: any) => {
  if (!backtestChart.value) return;
  const chart = echarts.init(backtestChart.value);
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['AI Strategy', 'Benchmark'], textStyle: { color: '#f8fafc' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.dates,
      axisLine: { lineStyle: { color: '#475569' } },
      axisLabel: { color: '#94a3b8' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
      axisLabel: { color: '#94a3b8' }
    },
    series: [
      {
        name: 'AI Strategy',
        type: 'line',
        data: data.returns,
        smooth: true,
        lineStyle: { width: 3, color: '#38bdf8' },
        itemStyle: { color: '#38bdf8' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(56, 189, 248, 0.2)' },
            { offset: 1, color: 'transparent' }
          ])
        }
      },
      {
        name: 'Benchmark',
        type: 'line',
        data: data.benchmark,
        smooth: true,
        lineStyle: { width: 2, color: '#94a3b8', type: 'dashed' },
        itemStyle: { color: '#94a3b8' }
      }
    ]
  });
};

onMounted(async () => {
  try {
    const [recRes, backtestRes] = await Promise.all([
      axios.get(`${API_DATA}/recommendations`),
      axios.get(`${API_DATA}/strategy/backtest`)
    ]);
    recommendations.value = recRes.data.recommendations;
    backtestData.value = backtestRes.data;
    initBacktestChart(backtestData.value);
  } catch (e) {
    console.error('Failed to load strategy data', e);
  }
});
</script>

<style scoped>
.strategy-view {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.filters {
  display: flex;
  gap: 12px;
  padding: 12px 20px;
}

select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  outline: none;
}

.strategy-list {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  margin-bottom: 40px;
}

.recommendation-card {
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.ticker {
  font-size: 1.25rem;
  font-weight: 800;
}

.confidence {
  font-size: 0.85rem;
  font-weight: 600;
}

.prediction {
  font-size: 1.5rem;
  font-weight: 900;
  margin-bottom: 16px;
}

.prediction.up { color: var(--up-color); }
.prediction.down { color: var(--down-color); }

.reason {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 20px;
}

.btn-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

.backtest-section {
  padding: 24px;
  margin-bottom: 40px;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.screener-section {
  padding: 24px;
  overflow-x: auto;
}

.screener-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

th {
  text-align: left;
  color: var(--text-muted);
  font-weight: 500;
  padding: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

td {
  padding: 16px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.tag {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.tag.buy { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.tag.strong-buy { background: #10b981; color: white; }
.tag.sell { background: rgba(244, 63, 94, 0.1); color: #f43f5e; }
.tag.hold { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }

.btn-small {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
}
</style>
