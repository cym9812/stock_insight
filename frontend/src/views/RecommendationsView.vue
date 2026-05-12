<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_DATA } from '../config/api'

const recommendations = ref<any[]>([])

const fetchRecommendations = async () => {
  try {
    const res = await axios.get(`${API_DATA}/recommendations`)
    recommendations.value = res.data.recommendations
  } catch (error) {
    console.error('Failed to fetch recommendations:', error)
  }
}

onMounted(fetchRecommendations)
</script>

<template>
  <div class="rec-container">
    <h2 class="page-title">AI 每日选股策略</h2>
    <div class="grid">
      <div class="rec-card glass-card" v-for="rec in recommendations" :key="rec.ticker">
        <div class="card-header">
          <h3>{{ rec.ticker }}</h3>
          <span :class="['badge', rec.prediction === 'up' ? 'badge-up' : 'badge-down']">
            {{ rec.prediction === 'up' ? '📈 看涨' : '📉 看跌' }}
          </span>
        </div>
        
        <div class="confidence">
          <div class="confidence-header">
            <span>AI 信心指数</span>
            <span>{{ rec.confidence }}%</span>
          </div>
          <div class="progress-bg">
            <div 
              class="progress-fill" 
              :style="{ 
                width: rec.confidence + '%',
                background: rec.prediction === 'up' ? 'var(--up-color)' : 'var(--down-color)' 
              }">
            </div>
          </div>
        </div>

        <div class="reason">
          <h4>推荐理由：</h4>
          <p>{{ rec.reason }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rec-container {
  padding: 8px;
}

.page-title {
  margin: 0 0 24px 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.rec-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.rec-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  letter-spacing: 1px;
}

.badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.badge-up {
  background: rgba(16, 185, 129, 0.15);
  color: var(--up-color);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-down {
  background: rgba(239, 68, 68, 0.15);
  color: var(--down-color);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.confidence-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.progress-bg {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.reason h4 {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.reason p {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--text-main);
}
</style>
