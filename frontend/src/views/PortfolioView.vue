<template>
  <div class="portfolio-view animate-fade-in">
    <header class="view-header">
      <h1 class="text-gradient">Portfolio & Watchlist</h1>
      <div class="stats glass-card">
        <div class="stat-item">
          <span class="label">Total P/L</span>
          <span class="value up">+$1,240.50 (+5.2%)</span>
        </div>
        <div class="stat-item">
          <span class="label">Daily P/L</span>
          <span class="value down">-$120.30 (-0.8%)</span>
        </div>
      </div>
    </header>

    <div class="portfolio-grid">
      <!-- Watchlist -->
      <section class="glass-card watchlist-section">
        <div class="section-header">
          <h3>Watchlist</h3>
          <button class="btn-small">+ Add Ticker</button>
        </div>
        <table class="portfolio-table">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Price</th>
              <th>Change</th>
              <th>AI Advice</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in watchlist" :key="item.ticker">
              <td><strong>{{ item.ticker }}</strong></td>
              <td>${{ item.price }}</td>
              <td :class="item.change.startsWith('+') ? 'up' : 'down'">{{ item.change }}</td>
              <td>
                <span class="advice-tag" :class="item.suggestion.toLowerCase()">
                  {{ item.suggestion }}
                </span>
              </td>
              <td><router-link :to="`/stock/${item.ticker}`" class="btn-link">View</router-link></td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Simulated Holdings -->
      <section class="glass-card holdings-section">
        <div class="section-header">
          <h3>Paper Trading Holdings</h3>
        </div>
        <table class="portfolio-table">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Avg Price</th>
              <th>Current</th>
              <th>P/L %</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hold in holdings" :key="hold.ticker">
              <td><strong>{{ hold.ticker }}</strong></td>
              <td>${{ hold.avg_price }}</td>
              <td>${{ hold.current_price }}</td>
              <td :class="hold.profit_pct >= 0 ? 'up' : 'down'">
                {{ hold.profit_pct >= 0 ? '+' : '' }}{{ hold.profit_pct }}%
              </td>
              <td><button class="btn-small outline">Sell</button></td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { API_DATA } from '../config/api';
const watchlist = ref<any[]>([]);
const holdings = ref<any[]>([]);

onMounted(async () => {
  try {
    const res = await axios.get(`${API_DATA}/portfolio/overview`);
    watchlist.value = res.data.watchlist;
    holdings.value = res.data.holdings;
  } catch (e) {
    console.error('Failed to fetch portfolio data', e);
  }
});
</script>

<style scoped>
.portfolio-view {
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

.stats {
  display: flex;
  gap: 32px;
  padding: 16px 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.stat-item .value {
  font-size: 1.25rem;
  font-weight: 700;
}

.portfolio-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.watchlist-section, .holdings-section {
  padding: 24px;
}

.portfolio-table {
  width: 100%;
  border-collapse: collapse;
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

.advice-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.advice-tag.hold { background: rgba(56, 189, 248, 0.1); color: #38bdf8; }
.advice-tag.buy { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.advice-tag.sell { background: rgba(244, 63, 94, 0.1); color: #f43f5e; }

.btn-small {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-small:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

.btn-link:hover {
  opacity: 0.8;
}

.btn-small.outline {
  background: transparent;
  border-color: var(--text-muted);
  color: var(--text-muted);
}

.btn-small.outline:hover {
  border-color: var(--down-color);
  color: var(--down-color);
}

@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
}
</style>
