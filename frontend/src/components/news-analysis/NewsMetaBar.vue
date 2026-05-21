<template>
  <div class="flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
    <span class="inline-flex h-6 items-center rounded-md border border-border bg-secondary/45 px-2 font-semibold">
      {{ formatUnixSeconds(item.publish_time) }}
    </span>
    <span v-if="item.event_type" class="inline-flex h-6 items-center rounded-md border border-border bg-secondary/45 px-2 font-semibold">
      {{ item.event_type }}
    </span>
    <span v-if="item.confidence !== null" class="inline-flex h-6 items-center rounded-md border border-border bg-secondary/45 px-2 font-semibold">
      {{ Math.round(item.confidence * 100) }}% 置信度
    </span>
    <a
      v-if="item.source_url"
      class="inline-flex h-6 items-center rounded-md border border-sky-300/20 bg-sky-300/10 px-2 font-bold text-sky-200 transition-colors hover:bg-sky-300/15"
      :href="item.source_url"
      target="_blank"
      rel="noreferrer"
    >
      来源
    </a>
  </div>
</template>

<script setup lang="ts">
import type { NewsAnalysisResultItem } from '../../types/newsAnalysis'
import { formatUnixSeconds } from './newsAnalysisUi'

defineProps<{
  item: NewsAnalysisResultItem
}>()
</script>
