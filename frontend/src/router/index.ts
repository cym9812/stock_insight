import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import StrategyView from '../views/StrategyView.vue'
import StockDetailView from '../views/StockDetailView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import NewsTaskStatusView from '../views/NewsTaskStatusView.vue'
import NewsAnalysisResultsView from '../views/NewsAnalysisResultsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/strategy',
      name: 'strategy',
      component: StrategyView
    },
    {
      path: '/stock/:ticker?',
      name: 'stock-detail',
      component: StockDetailView
    },
    {
      path: '/portfolio',
      name: 'portfolio',
      component: PortfolioView
    },
    {
      path: '/tasks/news-analysis',
      name: 'news-task-status',
      component: NewsTaskStatusView
    },
    {
      path: '/news-analysis/results',
      name: 'news-analysis-results',
      component: NewsAnalysisResultsView
    }
  ]
})

export default router
