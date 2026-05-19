<template>
  <div class="mx-auto w-full max-w-[1420px]">
    <PageHeader
      eyebrow="AI Market Intelligence"
      title="News Impact Radar"
      subtitle="Fast scan of market-moving news and AI impact signals"
    >
      <template #actions>
        <div class="flex flex-wrap items-center gap-2">
          <StatusChip tone="up">Positive {{ impactCounts.positive }}</StatusChip>
          <StatusChip tone="down">Negative {{ impactCounts.negative }}</StatusChip>
          <StatusChip tone="neutral">Neutral {{ impactCounts.neutral }}</StatusChip>
        </div>
        <Button :disabled="loading" @click="loadResults">{{ loading ? 'Refreshing' : 'Refresh' }}</Button>
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
        <span class="text-xs font-medium text-muted-foreground">Sorted by importance, urgency, and confidence</span>
      </div>

      <div class="grid gap-2">
        <article v-if="!filteredItems.length" class="rounded-lg border border-dashed border-border p-10 text-center text-sm text-muted-foreground">
          No news analysis results
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
import { getPriorityScore } from '@/components/news-analysis/newsAnalysisUi'
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
  { label: 'All', value: 'all' },
  { label: 'Positive', value: 'positive' },
  { label: 'Negative', value: 'negative' },
  { label: 'High Priority', value: 'high' },
]

const impactCounts = computed(() => ({
  positive: items.value.filter(item => item.market_impact === 'positive').length,
  negative: items.value.filter(item => item.market_impact === 'negative').length,
  neutral: items.value.filter(item => !['positive', 'negative'].includes(item.market_impact)).length,
}))

const filteredItems = computed(() => {
  return [...items.value]
    .filter(item => {
      if (currentFilter.value === 'all') return true
      if (currentFilter.value === 'high') return item.importance === 'high' || item.urgency === 'high'
      return item.market_impact === currentFilter.value
    })
    .sort((a, b) => getPriorityScore(b) - getPriorityScore(a))
})

const loadResults = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getNewsAnalysisResults(100)
    items.value = response.items
  } catch (err) {
    console.error('Failed to load news analysis results', err)
    error.value = 'Failed to load news analysis results'
  } finally {
    loading.value = false
  }
}

onMounted(loadResults)
</script>
