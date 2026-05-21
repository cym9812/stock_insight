<template>
  <aside
    :class="[
      'grid h-full min-h-[108px] w-[88px] shrink-0 grid-rows-[56px_1fr] overflow-hidden rounded-md border bg-slate-950/25 max-lg:min-h-0 max-lg:w-full max-lg:grid-cols-[1fr_auto] max-lg:grid-rows-1',
      ui.railClass,
    ]"
  >
    <div :class="['flex items-center justify-center gap-1.5 border-b border-white/10 px-2 max-lg:border-b-0 max-lg:border-r', ui.signalClass]">
      <span :class="['h-2 w-2 rounded-full', ui.dotClass]"></span>
      <strong class="text-[11px] font-black uppercase tracking-wide">{{ ui.label }}</strong>
    </div>
    <div class="flex flex-col items-center justify-center gap-1 px-2 py-2 text-center">
      <span class="block text-[9px] font-bold uppercase tracking-wide text-muted-foreground">Priority</span>
      <strong class="text-xl font-black leading-none text-foreground">{{ score ?? '--' }}</strong>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getImpactUi } from './newsAnalysisUi'

const props = defineProps<{
  impact: string | null
  score: number | null
}>()

const ui = computed(() => getImpactUi(props.impact))
</script>
