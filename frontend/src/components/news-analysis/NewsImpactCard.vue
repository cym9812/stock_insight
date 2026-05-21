<template>
  <article
    :class="[
      'grid grid-cols-[88px_minmax(0,1fr)] gap-3 rounded-lg border border-l-4 bg-card/95 p-3 shadow-sm transition-colors hover:bg-slate-800/70 max-lg:grid-cols-1',
      ui.cardClass,
    ]"
  >
    <ImpactRail :impact="displayImpact" :score="score" />

    <section class="grid min-w-0 gap-2">
      <div class="flex min-w-0 items-center justify-between gap-3">
        <NewsMetaBar :item="item" />
      </div>

      <details v-if="isExpandableNews(item.content)" class="group">
        <summary class="block cursor-pointer list-none">
          <span class="line-clamp-1 text-[15px] font-bold leading-6 text-foreground group-open:line-clamp-none">
            {{ item.content }}
            <span class="ml-1 text-xs font-semibold text-sky-200/80 group-open:hidden">展开全文</span>
          </span>
        </summary>
      </details>
      <p v-else class="m-0 line-clamp-1 text-[15px] font-bold leading-6 text-foreground">{{ item.content }}</p>

      <p class="m-0 line-clamp-1 text-sm leading-6 text-slate-300">
        <span
          class="mr-2 inline-flex h-5 min-w-7 translate-y-[-1px] items-center justify-center rounded border border-sky-300/15 bg-sky-300/10 px-1.5 align-middle text-[10px] font-black text-sky-200"
        >
          AI
        </span>
        <span class="align-middle">{{ aiLine }}</span>
      </p>

      <AnalysisDrawer v-if="isAnalyzed(item)" :item="item" />
    </section>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { NewsAnalysisResultItem } from '@/types/newsAnalysis'
import AnalysisDrawer from './AnalysisDrawer.vue'
import ImpactRail from './ImpactRail.vue'
import NewsMetaBar from './NewsMetaBar.vue'
import { getDisplayImpact, getImpactUi, getPriorityScore, isAnalyzed, isExpandableNews } from './newsAnalysisUi'

const props = defineProps<{
  item: NewsAnalysisResultItem
}>()

const score = computed(() => getPriorityScore(props.item))
const displayImpact = computed(() => getDisplayImpact(props.item))
const ui = computed(() => getImpactUi(displayImpact.value))
const aiLine = computed(() => {
  if (props.item.analysis_status === 'failed') return 'AI 分析多次重试后仍失败'
  if (props.item.analysis_status === 'pending' || props.item.analysis_status === 'analyzing') {
    return 'AI 分析进行中'
  }
  return props.item.summary || '暂无摘要'
})
</script>
