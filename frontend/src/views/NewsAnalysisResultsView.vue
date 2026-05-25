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
        </div>
        <Button :disabled="loading" @click="loadResults">{{ loading ? '刷新中' : '刷新' }}</Button>
      </template>
    </PageHeader>

    <div v-if="error" class="mb-4 rounded-lg border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">
      {{ error }}
    </div>

    <PanelCard class="border-border/70 bg-card/60 p-3 shadow-none">
      <div class="mb-3 flex items-center justify-between gap-3 rounded-md border border-border/70 bg-slate-950/20 p-2 max-md:flex-col max-md:items-stretch">
        <FilterTabs v-model="currentFilter" :options="tabs" />
        <div class="flex shrink-0 items-center justify-end gap-3 max-sm:flex-wrap max-sm:justify-start">
          <SelectField v-model="sortBy" label="排序字段" :options="sortByOptions" />
          <SelectField v-model="sortDirection" label="方向" :options="sortDirectionOptions" />
        </div>
      </div>

      <div class="grid gap-2">
        <article v-if="!filteredItems.length" class="rounded-lg border border-dashed border-border p-10 text-center text-sm text-muted-foreground">
          暂无新闻分析结果
        </article>
        <NewsImpactCard v-for="item in filteredItems" :key="item.news_id" :item="item" />
      </div>
    </PanelCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { getNewsAnalysisResults } from '@/api/newsAnalysis'
import NewsImpactCard from '@/components/news-analysis/NewsImpactCard.vue'
import { getPriorityScore, isAnalyzed } from '@/components/news-analysis/newsAnalysisUi'
import Button from '@/components/ui/Button.vue'
import FilterTabs from '@/components/ui/FilterTabs.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import SelectField from '@/components/ui/SelectField.vue'
import StatusChip from '@/components/ui/StatusChip.vue'
import type { NewsAnalysisResultItem } from '@/types/newsAnalysis'

const items = ref<NewsAnalysisResultItem[]>([])
const loading = ref(false)
const error = ref('')
const currentFilter = ref('all')
const sortBy = ref<SortBy>('priority')
const sortDirection = ref<SortDirection>('desc')

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

const impactCounts = computed(() => ({
  positive: items.value.filter(item => isAnalyzed(item) && item.market_impact === 'positive').length,
  negative: items.value.filter(item => isAnalyzed(item) && item.market_impact === 'negative').length,
  neutral: items.value.filter(item => isAnalyzed(item) && !['positive', 'negative'].includes(item.market_impact ?? '')).length,
  pending: items.value.filter(item => item.analysis_status === 'pending' || item.analysis_status === 'analyzing').length,
}))

const filteredItems = computed(() => {
  return [...items.value]
    .filter(item => {
      if (currentFilter.value === 'all') return true
      if (currentFilter.value === 'high') return isAnalyzed(item) && (item.importance === 'high' || item.urgency === 'high')
      if (!isAnalyzed(item)) return false
      return item.market_impact === currentFilter.value
    })
    .sort((a, b) => sortNewsItems(a, b, sortBy.value, sortDirection.value))
})

const sortNewsItems = (
  a: NewsAnalysisResultItem,
  b: NewsAnalysisResultItem,
  by: SortBy,
  direction: SortDirection,
) => {
  const directionMultiplier = direction === 'desc' ? -1 : 1

  if (by === 'publish_time') {
    return (a.publish_time - b.publish_time) * directionMultiplier
  }

  const priorityDiff = ((getPriorityScore(a) ?? -1) - (getPriorityScore(b) ?? -1)) * directionMultiplier
  if (priorityDiff !== 0) return priorityDiff
  return b.publish_time - a.publish_time
}

const loadResults = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getNewsAnalysisResults(100)
    items.value = response.items
  } catch (err) {
    console.error('加载新闻分析结果失败', err)
    error.value = '加载新闻分析结果失败'
  } finally {
    loading.value = false
  }
}

onMounted(loadResults)
</script>
