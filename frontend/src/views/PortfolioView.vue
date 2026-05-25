<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader title="投资组合与自选" subtitle="模拟持仓、自选列表与 AI 建议">
      <template #actions>
        <div class="flex gap-5 rounded-lg border border-border bg-card px-4 py-3">
          <div class="flex flex-col">
            <span class="text-xs text-muted-foreground">总盈亏</span>
            <span class="text-lg font-black text-foreground">$0.00 (0.0%)</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs text-muted-foreground">当日盈亏</span>
            <span class="text-lg font-black text-foreground">$0.00 (0.0%)</span>
          </div>
        </div>
      </template>
    </PageHeader>

    <div class="grid gap-4">
      <PanelCard class="overflow-x-auto">
        <template #header>
          <h3 class="m-0 text-sm font-semibold text-foreground">自选列表</h3>
          <Button variant="secondary" size="sm">添加代码</Button>
        </template>
        <table class="w-full min-w-[760px] border-collapse text-sm">
          <thead>
            <tr class="border-b border-border text-left text-xs text-muted-foreground">
              <th class="px-3 py-2 font-semibold">代码</th>
              <th class="px-3 py-2 font-semibold">价格</th>
              <th class="px-3 py-2 font-semibold">涨跌</th>
              <th class="px-3 py-2 font-semibold">AI 建议</th>
              <th class="px-3 py-2 font-semibold">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in watchlist" :key="item.ticker" class="border-b border-border/70 hover:bg-secondary/25">
              <td class="px-3 py-3 font-bold">{{ item.ticker }}</td>
              <td class="px-3 py-3">${{ item.price }}</td>
              <td :class="['px-3 py-3 font-bold', item.change.startsWith('+') ? 'text-emerald-300' : 'text-rose-300']">{{ item.change }}</td>
              <td class="px-3 py-3"><MetricChip :tone="adviceTone(item.suggestion)" class="font-bold uppercase">{{ item.suggestion }}</MetricChip></td>
              <td class="px-3 py-3">
                <router-link :to="`/stock/${item.ticker}`" class="text-sm font-bold text-sky-200 hover:text-sky-100">查看</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </PanelCard>

      <PanelCard class="overflow-x-auto">
        <template #header><h3 class="m-0 text-sm font-semibold text-foreground">模拟交易持仓</h3></template>
        <table class="w-full min-w-[720px] border-collapse text-sm">
          <thead>
            <tr class="border-b border-border text-left text-xs text-muted-foreground">
              <th class="px-3 py-2 font-semibold">代码</th>
              <th class="px-3 py-2 font-semibold">持仓均价</th>
              <th class="px-3 py-2 font-semibold">现价</th>
              <th class="px-3 py-2 font-semibold">盈亏 %</th>
              <th class="px-3 py-2 font-semibold">操作</th>
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
              <td class="px-3 py-3"><Button variant="outline" size="sm">卖出</Button></td>
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
import MetricChip from '@/components/ui/MetricChip.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import type { HoldingItem, WatchlistItem } from '@/types/portfolio'

const watchlist = ref<WatchlistItem[]>([])
const holdings = ref<HoldingItem[]>([])

const adviceTone = (value: string) => {
  const normalized = value.toLowerCase()
  if (normalized === 'buy') return 'up'
  if (normalized === 'sell') return 'down'
  return 'accent'
}

onMounted(async () => {
  try {
    const overview = await getPortfolioOverview()
    watchlist.value = overview.watchlist
    holdings.value = overview.holdings
  } catch (e) {
    console.error('加载投资组合数据失败', e)
  }
})
</script>
