<template>
  <div class="flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
    <MetricChip>
      {{ formatUnixSeconds(item.publish_time) }}
    </MetricChip>
    <MetricChip v-if="item.event_type">
      {{ item.event_type }}
    </MetricChip>
    <MetricChip v-if="item.confidence !== null">
      {{ Math.round(item.confidence * 100) }}% 置信度
    </MetricChip>
    <a
      v-if="item.source_url"
      class="transition-opacity hover:opacity-85"
      :href="item.source_url"
      target="_blank"
      rel="noreferrer"
    >
      <MetricChip tone="accent" class="font-bold">来源</MetricChip>
    </a>
  </div>
</template>

<script setup lang="ts">
import type { NewsAnalysisResultItem } from '../../types/newsAnalysis'
import MetricChip from '@/components/ui/MetricChip.vue'
import { formatUnixSeconds } from './newsAnalysisUi'

defineProps<{
  item: NewsAnalysisResultItem
}>()
</script>
