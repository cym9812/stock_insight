<template>
  <div class="mx-auto w-full max-w-[1400px]">
    <PageHeader title="News Analysis Task" subtitle="Scheduler registration, next run time, and recent execution records">
      <template #actions>
        <Button :disabled="loading" @click="loadStatus">{{ loading ? 'Refreshing' : 'Refresh' }}</Button>
      </template>
    </PageHeader>

    <div v-if="error" class="mb-4 rounded-lg border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">
      {{ error }}
    </div>

    <section class="mb-4 grid grid-cols-4 gap-3 max-xl:grid-cols-2 max-sm:grid-cols-1">
      <PanelCard v-for="metric in metrics" :key="metric.label" class="min-h-24">
        <span class="text-xs font-bold uppercase text-muted-foreground">{{ metric.label }}</span>
        <strong :class="['mt-2 block text-xl font-black', metric.className]">{{ metric.value }}</strong>
      </PanelCard>
    </section>

    <PanelCard class="mb-4">
      <template #header>
        <h3 class="m-0 text-sm font-semibold text-foreground">Task Plan</h3>
        <span class="text-xs font-bold text-sky-200">{{ status?.job_id ?? 'market_news_monitor' }}</span>
      </template>
      <dl class="grid grid-cols-2 gap-4 max-md:grid-cols-1">
        <div v-for="detail in taskDetails" :key="detail.label" class="min-w-0 rounded-md bg-slate-950/20 p-3">
          <dt class="mb-1 text-xs font-semibold text-muted-foreground">{{ detail.label }}</dt>
          <dd class="m-0 break-words text-sm text-foreground">{{ detail.value }}</dd>
        </div>
      </dl>
    </PanelCard>

    <PanelCard class="overflow-x-auto">
      <template #header>
        <h3 class="m-0 text-sm font-semibold text-foreground">Recent Runs</h3>
        <span class="text-xs text-muted-foreground">{{ status?.recent_runs.length ?? 0 }} records</span>
      </template>
      <table class="w-full min-w-[880px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border text-left text-xs text-muted-foreground">
            <th class="px-3 py-2 font-semibold">Status</th>
            <th class="px-3 py-2 font-semibold">Scheduled</th>
            <th class="px-3 py-2 font-semibold">Started</th>
            <th class="px-3 py-2 font-semibold">Finished</th>
            <th class="px-3 py-2 font-semibold">Duration</th>
            <th class="px-3 py-2 font-semibold">Message</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!status?.recent_runs.length">
            <td colspan="6" class="px-3 py-10 text-center text-muted-foreground">No execution records yet</td>
          </tr>
          <tr v-for="run in status?.recent_runs" :key="run.run_id" class="border-b border-border/70 hover:bg-secondary/25">
            <td class="px-3 py-3"><StatusChip :tone="statusTone(run.status)">{{ run.status }}</StatusChip></td>
            <td class="px-3 py-3">{{ formatDateTime(run.scheduled_at) }}</td>
            <td class="px-3 py-3">{{ formatDateTime(run.started_at) }}</td>
            <td class="px-3 py-3">{{ formatDateTime(run.finished_at) }}</td>
            <td class="px-3 py-3">{{ formatDuration(run.duration_seconds) }}</td>
            <td class="max-w-72 break-words px-3 py-3 text-muted-foreground">{{ run.message ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </PanelCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { getNewsAnalysisTaskStatus } from '@/api/tasks'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import StatusChip from '@/components/ui/StatusChip.vue'
import type { ScheduledTaskStatus, TaskRunStatus } from '@/types/task'

const status = ref<ScheduledTaskStatus | null>(null)
const loading = ref(false)
const error = ref('')
let refreshTimer: number | undefined

const loadStatus = async () => {
  loading.value = true
  error.value = ''
  try {
    status.value = await getNewsAnalysisTaskStatus()
  } catch (err) {
    console.error('Failed to load news analysis task status', err)
    error.value = 'Failed to load task status'
  } finally {
    loading.value = false
  }
}

const formatDateTime = (value?: string | null) => {
  if (!value) return '-'
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(new Date(value))
}

const formatDuration = (value?: number | null) => {
  if (value === null || value === undefined) return '-'
  return `${value.toFixed(2)}s`
}

const statusTone = (value?: TaskRunStatus | string) => {
  if (value === 'success') return 'up'
  if (value === 'error') return 'down'
  if (value === 'missed') return 'warning'
  if (value === 'running') return 'accent'
  return 'neutral'
}

const statusColor = (value?: TaskRunStatus | string) => {
  if (value === 'success') return 'text-emerald-300'
  if (value === 'error') return 'text-rose-300'
  if (value === 'missed') return 'text-amber-200'
  if (value === 'running') return 'text-sky-200'
  return 'text-foreground'
}

const metrics = computed(() => [
  {
    label: 'Scheduler',
    value: status.value?.scheduler_running ? 'Running' : 'Stopped',
    className: status.value?.scheduler_running ? 'text-emerald-300' : 'text-rose-300',
  },
  {
    label: 'Job',
    value: status.value?.exists ? 'Registered' : 'Missing',
    className: status.value?.exists ? 'text-emerald-300' : 'text-rose-300',
  },
  { label: 'Next Run', value: formatDateTime(status.value?.next_run_time), className: 'text-foreground' },
  {
    label: 'Last Result',
    value: status.value?.last_run?.status ?? 'No runs',
    className: statusColor(status.value?.last_run?.status),
  },
])

const taskDetails = computed(() => [
  { label: 'Name', value: status.value?.name ?? '-' },
  { label: 'Trigger', value: status.value?.trigger ?? '-' },
  { label: 'Last Scheduled', value: formatDateTime(status.value?.last_run?.scheduled_at) },
  { label: 'Last Duration', value: formatDuration(status.value?.last_run?.duration_seconds) },
])

onMounted(() => {
  loadStatus()
  refreshTimer = window.setInterval(loadStatus, 30000)
})

onUnmounted(() => {
  if (refreshTimer) window.clearInterval(refreshTimer)
})
</script>
