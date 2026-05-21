<script setup lang="ts">
import {
  Bot,
  BriefcaseBusiness,
  ChartCandlestick,
  LayoutDashboard,
  Newspaper,
  Radar,
} from '@lucide/vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const navSections = [
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
</script>

<template>
  <div class="flex h-screen w-screen overflow-hidden bg-background text-foreground">
    <nav class="flex w-[248px] shrink-0 flex-col border-r border-border bg-slate-950/45 px-3 py-4">
      <div class="mb-5 flex h-12 items-center gap-3 px-2">
        <div class="flex h-9 w-9 items-center justify-center rounded-lg border border-sky-300/25 bg-sky-300/10 text-xs font-black text-sky-200">
          SI
        </div>
        <div class="min-w-0">
          <h1 class="m-0 text-sm font-bold text-foreground">匠制科技</h1>
          <span class="block text-xs font-medium text-muted-foreground">量化工作台</span>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <section v-for="section in navSections" :key="section.label">
          <div class="px-2 pb-2 text-[11px] font-bold uppercase text-slate-500">{{ section.label }}</div>
          <div class="flex flex-col gap-1">
            <router-link
              v-for="item in section.items"
              :key="item.to"
              :to="item.to"
              class="flex h-9 items-center gap-2.5 rounded-md px-2 text-sm font-semibold text-muted-foreground transition-colors hover:bg-secondary/60 hover:text-foreground"
              :class="item.active(route.path) && 'border border-sky-300/20 bg-sky-300/10 text-sky-100'"
            >
              <component :is="item.icon" class="h-4 w-4" />
              <span>{{ item.label }}</span>
            </router-link>
          </div>
        </section>
      </div>

      <div class="mt-auto border-t border-border pt-4">
        <div class="flex items-center gap-3 rounded-lg bg-secondary/45 p-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-md bg-slate-700 text-xs font-bold">SI</div>
          <div>
            <div class="text-xs font-semibold text-foreground">本地工作区</div>
            <div class="text-xs text-emerald-300">就绪</div>
          </div>
        </div>
      </div>
    </nav>

    <main class="min-w-0 flex-1 overflow-y-auto bg-gradient-to-b from-slate-900/60 to-background p-5">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(5px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
