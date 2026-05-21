<template>
  <details class="group">
    <summary class="inline-flex h-6 cursor-pointer list-none items-center rounded text-xs font-bold text-muted-foreground transition-colors hover:text-foreground">
      展开分析
    </summary>

    <div class="mt-3 grid grid-cols-[1fr_1.15fr] gap-4 rounded-md border border-border/70 bg-slate-950/20 p-3 max-lg:grid-cols-1">
      <div>
        <div class="mb-2 text-[11px] font-black uppercase text-muted-foreground">行业</div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="sector in item.sectors"
            :key="`${item.news_id}-sector-${sector.name}`"
            :class="['inline-flex min-h-7 items-center rounded-full border px-2.5 text-xs font-semibold', getImpactUi(sector.impact).chipClass]"
          >
            {{ sector.name }}
          </span>
          <span v-if="!item.sectors.length" class="inline-flex min-h-7 items-center rounded-full border border-border bg-secondary/40 px-2.5 text-xs text-muted-foreground">
            无
          </span>
        </div>
      </div>
      <div>
        <div class="mb-2 text-[11px] font-black uppercase text-muted-foreground">公司</div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="company in item.companies"
            :key="`${item.news_id}-company-${company.name}`"
            :class="['inline-flex min-h-7 max-w-56 items-center gap-1.5 rounded-md border px-2.5 text-xs font-semibold', getImpactUi(company.impact).chipClass]"
          >
            {{ company.name }}
            <small v-if="company.stock_code" class="text-muted-foreground">{{ company.stock_code }}</small>
          </span>
          <span v-if="!item.companies.length" class="inline-flex min-h-7 items-center rounded-md border border-border bg-secondary/40 px-2.5 text-xs text-muted-foreground">
            无
          </span>
        </div>
      </div>
    </div>

    <section class="mt-3">
      <div class="mb-2 text-[11px] font-black uppercase text-muted-foreground">推理依据</div>
      <p class="m-0 rounded-md border border-border/70 bg-slate-950/20 p-3 text-sm leading-7 text-slate-300">{{ item.reasoning }}</p>
    </section>
  </details>
</template>

<script setup lang="ts">
import type { NewsAnalysisResultItem } from '../../types/newsAnalysis'
import { getImpactUi } from './newsAnalysisUi'

defineProps<{
  item: NewsAnalysisResultItem
}>()
</script>
