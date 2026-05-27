<template>
  <div class="mx-auto w-full max-w-[1420px]">
    <PageHeader
      eyebrow="AI 市场情报"
      title="新闻影响雷达"
      subtitle="快速扫描可能影响市场的新闻与 AI 影响信号"
    >
      <template #actions>
        <div class="flex flex-wrap items-center gap-2">
          <StatusChip tone="up">利好 {{ impactCounts.positive }}</StatusChip>
          <StatusChip tone="down">利空 {{ impactCounts.negative }}</StatusChip>
          <StatusChip tone="neutral">中性 {{ impactCounts.neutral }}</StatusChip>
          <StatusChip tone="accent">待分析 {{ impactCounts.pending }}</StatusChip>
          <StatusChip tone="warning">失败 {{ impactCounts.failed }}</StatusChip>
        </div>
        <Button :disabled="loading" @click="loadResults">{{ loading ? '刷新中' : '刷新' }}</Button>
      </template>
    </PageHeader>

    <div v-if="error" class="mb-4 rounded-lg border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">
      {{ error }}
    </div>

    <PanelCard class="border-border/60 bg-card/75 p-3 shadow-none">
      <!-- Unified Filter Toolbar -->
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border/60 bg-black/30 p-2 text-xs">
        
        <!-- Left Section: Category Filter Tabs & Time Presets -->
        <div class="flex flex-wrap items-center gap-3">
          <!-- Filter Tabs -->
          <FilterTabs v-model="currentFilter" :options="tabs" />
          
          <!-- Vertical Separator (hidden on mobile) -->
          <div class="h-5 w-px bg-border/40 max-sm:hidden"></div>
          
          <!-- Time Presets -->
          <div class="flex gap-1.5 max-sm:flex-wrap max-sm:justify-start">
            <button
              @click="setQuickDate('today')"
              class="rounded bg-muted/40 border border-border/50 px-2.5 py-1 hover:bg-secondary/60 hover:text-foreground transition-colors"
              :class="{ 'bg-primary/10 text-primary border-primary/30 font-medium': isQuickActive('today') }"
            >
              今天
            </button>
            <button
              @click="setQuickDate('past3')"
              class="rounded bg-muted/40 border border-border/50 px-2.5 py-1 hover:bg-secondary/60 hover:text-foreground transition-colors"
              :class="{ 'bg-primary/10 text-primary border-primary/30 font-medium': isQuickActive('past3') }"
            >
              近 3 天
            </button>
            <button
              @click="setQuickDate('past7')"
              class="rounded bg-muted/40 border border-border/50 px-2.5 py-1 hover:bg-secondary/60 hover:text-foreground transition-colors"
              :class="{ 'bg-primary/10 text-primary border-primary/30 font-medium': isQuickActive('past7') }"
            >
              近 1 周
            </button>
            <button
              @click="setQuickDate('all')"
              class="rounded bg-muted/40 border border-border/50 px-2.5 py-1 hover:bg-secondary/60 hover:text-foreground transition-colors"
              :class="{ 'bg-primary/10 text-primary border-primary/30 font-medium': isQuickActive('all') }"
            >
              全部
            </button>
          </div>
        </div>

        <!-- Right Section: Date Pickers & Sorting -->
        <div class="flex flex-wrap items-center gap-3 max-md:w-full max-md:justify-between max-sm:flex-col max-sm:items-stretch">
          <!-- Date Range Pickers -->
          <div class="flex items-center gap-1.5 rounded-md border border-border bg-muted/45 px-2 py-1 max-sm:justify-center">
            <span class="text-muted-foreground font-medium">时间:</span>
            <input
              type="date"
              v-model="startDate"
              class="border-0 bg-transparent text-foreground focus:outline-none w-[115px] cursor-pointer"
            />
            <span class="text-muted-foreground/60">-</span>
            <input
              type="date"
              v-model="endDate"
              class="border-0 bg-transparent text-foreground focus:outline-none w-[115px] cursor-pointer"
            />
          </div>

          <!-- Vertical Separator (hidden on mobile/tablet) -->
          <div class="h-5 w-px bg-border/40 max-md:hidden"></div>

          <!-- Sort Selectors -->
          <div class="flex items-center gap-2 max-sm:justify-between">
            <SelectField v-model="sortBy" label="排序" :options="sortByOptions" />
            <SelectField v-model="sortDirection" label="方向" :options="sortDirectionOptions" />
          </div>
        </div>
      </div>


      <!-- News Items Grid -->

      <div class="grid gap-2">
        <article v-if="!filteredItems.length" class="rounded-lg border border-dashed border-border p-10 text-center text-sm text-muted-foreground">
          暂无新闻分析结果
        </article>
        <NewsImpactCard v-for="item in filteredItems" :key="item.news_id" :item="item" />
      </div>

      <!-- Pagination Row -->
      <div v-if="totalPages > 1" class="mt-4 flex items-center justify-between border-t border-border/40 pt-4 max-sm:flex-col max-sm:gap-3">
        <span class="text-xs text-muted-foreground">
          显示第 {{ (page - 1) * pageSize + 1 }} 到 {{ Math.min(page * pageSize, total) }} 条，共 {{ total }} 条记录
        </span>
        <div class="flex items-center gap-1.5">
          <Button
            size="sm"
            variant="outline"
            :disabled="page <= 1"
            @click="page = 1"
            class="h-8 px-2.5"
          >
            首页
          </Button>
          <Button
            size="sm"
            variant="outline"
            :disabled="page <= 1"
            @click="page--"
            class="h-8 px-2.5"
          >
            上一页
          </Button>
          <span class="mx-2.5 text-xs font-medium text-foreground">
            第 {{ page }} / {{ totalPages }} 页
          </span>
          <Button
            size="sm"
            variant="outline"
            :disabled="page >= totalPages"
            @click="page++"
            class="h-8 px-2.5"
          >
            下一页
          </Button>
          <Button
            size="sm"
            variant="outline"
            :disabled="page >= totalPages"
            @click="page = totalPages"
            class="h-8 px-2.5"
          >
            尾页
          </Button>
        </div>
      </div>
    </PanelCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { getNewsAnalysisResults } from '@/api/newsAnalysis'
import NewsImpactCard from '@/components/news-analysis/NewsImpactCard.vue'
import Button from '@/components/ui/Button.vue'

import FilterTabs from '@/components/ui/FilterTabs.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import SelectField from '@/components/ui/SelectField.vue'
import StatusChip from '@/components/ui/StatusChip.vue'
import type { NewsAnalysisResultItem, NewsAnalysisStats } from '@/types/newsAnalysis'

function getLocalDateString(date: Date = new Date()): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const items = ref<NewsAnalysisResultItem[]>([])
const loading = ref(false)
const error = ref('')
const currentFilter = ref('all')
const sortBy = ref<SortBy>('priority')
const sortDirection = ref<SortDirection>('desc')

// Pagination States
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const totalPages = ref(0)

// Category statistics matching selected date range
const stats = ref<NewsAnalysisStats>({
  positive: 0,
  negative: 0,
  neutral: 0,
  pending: 0,
  failed: 0,
})

// Date Filter States (default to today)
const startDate = ref(getLocalDateString())
const endDate = ref(getLocalDateString())

type SortBy = 'priority' | 'publish_time'
type SortDirection = 'desc' | 'asc'

const tabs = [
  { label: '全部', value: 'all' },
  { label: '利好', value: 'positive' },
  { label: '利空', value: 'negative' },
  { label: '高优先级', value: 'high' },
]

const sortByOptions: { label: string, value: SortBy }[] = [
  { label: '优先级', value: 'priority' },
  { label: '发布时间', value: 'publish_time' },
]

const sortDirectionOptions: { label: string, value: SortDirection }[] = [
  { label: '降序', value: 'desc' },
  { label: '升序', value: 'asc' },
]

const impactCounts = computed(() => stats.value || {
  positive: 0,
  negative: 0,
  neutral: 0,
  pending: 0,
  failed: 0,
})

// Direct render items from backend paginated response
const filteredItems = computed(() => items.value)

function setQuickDate(type: 'today' | 'past3' | 'past7' | 'all') {
  const today = new Date()
  if (type === 'today') {
    startDate.value = getLocalDateString(today)
    endDate.value = getLocalDateString(today)
  } else if (type === 'past3') {
    const past3 = new Date()
    past3.setDate(today.getDate() - 2)
    startDate.value = getLocalDateString(past3)
    endDate.value = getLocalDateString(today)
  } else if (type === 'past7') {
    const past7 = new Date()
    past7.setDate(today.getDate() - 6)
    startDate.value = getLocalDateString(past7)
    endDate.value = getLocalDateString(today)
  } else if (type === 'all') {
    startDate.value = ''
    endDate.value = ''
  }
}

function isQuickActive(type: 'today' | 'past3' | 'past7' | 'all'): boolean {
  const today = getLocalDateString()
  if (type === 'today') {
    return startDate.value === today && endDate.value === today
  }
  if (type === 'past3') {
    const past3 = new Date()
    past3.setDate(new Date().getDate() - 2)
    return startDate.value === getLocalDateString(past3) && endDate.value === today
  }
  if (type === 'past7') {
    const past7 = new Date()
    past7.setDate(new Date().getDate() - 6)
    return startDate.value === getLocalDateString(past7) && endDate.value === today
  }
  if (type === 'all') {
    return !startDate.value && !endDate.value
  }
  return false
}

let currentRequestId = 0

const loadResults = async () => {
  currentRequestId++
  const requestId = currentRequestId
  loading.value = true
  error.value = ''
  try {
    const response = await getNewsAnalysisResults({
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value,
      sort_dir: sortDirection.value,
      filter_type: currentFilter.value,
      start_date: startDate.value || null,
      end_date: endDate.value || null,
    })
    
    // Only apply results if this is still the latest request
    if (requestId !== currentRequestId) {
      return
    }

    items.value = response.items || []
    total.value = response.total_count || 0
    totalPages.value = response.total_pages || 0
    if (response && response.stats) {
      stats.value = response.stats
    }
  } catch (err) {
    if (requestId === currentRequestId) {
      console.error('加载新闻分析结果失败', err)
      error.value = '加载新闻分析结果失败'
    }
  } finally {
    if (requestId === currentRequestId) {
      loading.value = false
    }
  }
}


// Watch filters/sorts/dates and reset page to 1
watch([currentFilter, sortBy, sortDirection, startDate, endDate, pageSize], () => {
  if (page.value !== 1) {
    page.value = 1
  } else {
    loadResults()
  }
})

// Watch page change
watch(page, () => {
  loadResults()
})

onMounted(loadResults)
</script>

