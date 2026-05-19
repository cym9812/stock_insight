<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader title="Portfolio & Watchlist" subtitle="Paper holdings, watchlist, and AI advice">
      <template #actions>
        <div class="flex gap-5 rounded-lg border border-border bg-card px-4 py-3">
          <div class="flex flex-col">
            <span class="text-xs text-muted-foreground">Total P/L</span>
            <span class="text-lg font-black text-foreground">$0.00 (0.0%)</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs text-muted-foreground">Daily P/L</span>
            <span class="text-lg font-black text-foreground">$0.00 (0.0%)</span>
          </div>
        </div>
      </template>
    </PageHeader>

    <div class="grid gap-4">
      <PanelCard class="overflow-x-auto">
        <template #header>
          <h3 class="m-0 text-sm font-semibold text-foreground">Watchlist</h3>
          <Button variant="secondary" size="sm">Add Ticker</Button>
        </template>
        <table class="w-full min-w-[760px] border-collapse text-sm">
          <thead>
            <tr class="border-b border-border text-left text-xs text-muted-foreground">
              <th class="px-3 py-2 font-semibold">Ticker</th>
              <th class="px-3 py-2 font-semibold">Price</th>
              <th class="px-3 py-2 font-semibold">Change</th>
              <th class="px-3 py-2 font-semibold">AI Advice</th>
              <th class="px-3 py-2 font-semibold">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in watchlist" :key="item.ticker" class="border-b border-border/70 hover:bg-secondary/25">
              <td class="px-3 py-3 font-bold">{{ item.ticker }}</td>
              <td class="px-3 py-3">${{ item.price }}</td>
              <td :class="['px-3 py-3 font-bold', item.change.startsWith('+') ? 'text-emerald-300' : 'text-rose-300']">{{ item.change }}</td>
              <td class="px-3 py-3"><span :class="adviceClass(item.suggestion)">{{ item.suggestion }}</span></td>
              <td class="px-3 py-3">
                <router-link :to="`/stock/${item.ticker}`" class="text-sm font-bold text-sky-200 hover:text-sky-100">View</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </PanelCard>

      <PanelCard class="overflow-x-auto">
        <template #header><h3 class="m-0 text-sm font-semibold text-foreground">Paper Trading Holdings</h3></template>
        <table class="w-full min-w-[720px] border-collapse text-sm">
          <thead>
            <tr class="border-b border-border text-left text-xs text-muted-foreground">
              <th class="px-3 py-2 font-semibold">Ticker</th>
              <th class="px-3 py-2 font-semibold">Avg Price</th>
              <th class="px-3 py-2 font-semibold">Current</th>
              <th class="px-3 py-2 font-semibold">P/L %</th>
              <th class="px-3 py-2 font-semibold">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hold in holdings" :key="hold.ticker" class="border-b border-border/70 hover:bg-secondary/25">
              <td class="px-3 py-3 font-bold">{{ hold.ticker }}</td>
              <td class="px-3 py-3">${{ hold.avg_price }}</td>
              <td class="px-3 py-3">${{ hold.current_price }}</td>
              <td :class="['px-3 py-3 font-bold', hold.profit_pct >= 0 ? 'text-emerald-300' : 'text-rose-300']">
                {{ hold.profit_pct >= 0 ? '+' : '' }}{{ hold.profit_pct }}%
              </td>
              <td class="px-3 py-3"><Button variant="outline" size="sm">Sell</Button></td>
            </tr>
          </tbody>
        </table>
      </PanelCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getPortfolioOverview } from '@/api/portfolio'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import type { HoldingItem, WatchlistItem } from '@/types/portfolio'

const watchlist = ref<WatchlistItem[]>([])
const holdings = ref<HoldingItem[]>([])

const adviceClass = (value: string) => {
  const base = 'inline-flex h-6 items-center rounded-md border px-2 text-xs font-bold uppercase'
  const normalized = value.toLowerCase()
  if (normalized === 'buy') return `${base} border-emerald-400/25 bg-emerald-400/10 text-emerald-200`
  if (normalized === 'sell') return `${base} border-rose-400/25 bg-rose-400/10 text-rose-200`
  return `${base} border-sky-300/25 bg-sky-300/10 text-sky-200`
}

onMounted(async () => {
  try {
    const overview = await getPortfolioOverview()
    watchlist.value = overview.watchlist
    holdings.value = overview.holdings
  } catch (e) {
    console.error('Failed to fetch portfolio data', e)
  }
})
</script>
