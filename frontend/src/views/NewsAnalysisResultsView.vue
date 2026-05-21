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
      <div class="mb-3 flex items-center justify-between gap-3 rounded-md border border-border/70 bg-slate-950/20 p-2 max-md:flex-col max-md:items-start">
        <div class="inline-flex rounded-md bg-slate-950/35 p-1">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="h-7 rounded px-3 text-xs font-bold text-muted-foreground transition-colors hover:text-foreground"
            :class="currentFilter === tab.value && 'bg-primary text-primary-foreground'"
            @click="currentFilter = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>
        <span class="text-xs font-medium text-muted-foreground">按重要性、紧急度和置信度排序</span>
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
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import StatusChip from '@/components/ui/StatusChip.vue'
import type { NewsAnalysisResultItem } from '@/types/newsAnalysis'

const items = ref<NewsAnalysisResultItem[]>([])
const loading = ref(false)
const error = ref('')
const currentFilter = ref('all')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '利好', value: 'positive' },
  { label: '利空', value: 'negative' },
  { label: '高优先级', value: 'high' },
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
    .sort((a, b) => (getPriorityScore(b) ?? -1) - (getPriorityScore(a) ?? -1))
})

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
