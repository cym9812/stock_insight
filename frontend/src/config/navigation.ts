import {
  Bot,
  BriefcaseBusiness,
  ChartCandlestick,
  LayoutDashboard,
  Newspaper,
  Radar,
} from '@lucide/vue'
import type { Component } from 'vue'

export interface NavigationItem {
  to: string
  label: string
  icon: Component
  active: (path: string) => boolean
}

export interface NavigationSection {
  label: string
  items: NavigationItem[]
}

export const navigationSections: NavigationSection[] = [
  {
    label: '市场',
    items: [
      { to: '/dashboard', label: '市场总览', icon: LayoutDashboard, active: (path: string) => path === '/dashboard' },
      { to: '/strategy', label: '策略中心', icon: Radar, active: (path: string) => path === '/strategy' },
      { to: '/stock', label: '个股分析', icon: ChartCandlestick, active: (path: string) => path.startsWith('/stock') },
      { to: '/portfolio', label: '投资组合', icon: BriefcaseBusiness, active: (path: string) => path === '/portfolio' },
    ],
  },
  {
    label: '自动化',
    items: [
      { to: '/tasks/news-analysis', label: '新闻任务', icon: Bot, active: (path: string) => path.startsWith('/tasks') },
      { to: '/news-analysis/results', label: '新闻雷达', icon: Newspaper, active: (path: string) => path.startsWith('/news-analysis') },
    ],
  },
]

export const getCurrentNavigationLabel = (path: string) => {
  for (const section of navigationSections) {
    const item = section.items.find(navItem => navItem.active(path))
    if (item) return item.label
  }

  return '量化工作台'
}
