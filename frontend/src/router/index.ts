import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import StrategyView from '../views/StrategyView.vue'
import StockDetailView from '../views/StockDetailView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import KLineView from '../views/KLineView.vue'

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
      path: '/old-kline',
      name: 'kline',
      component: KLineView
    }
  ]
})

export default router
