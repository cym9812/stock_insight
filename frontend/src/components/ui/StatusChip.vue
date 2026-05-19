<template>
  <span :class="cn('inline-flex h-6 items-center rounded-md border px-2 text-xs font-bold', toneClass)">
    <slot></slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = withDefaults(
  defineProps<{
    tone?: 'up' | 'down' | 'warning' | 'neutral' | 'accent'
  }>(),
  {
    tone: 'neutral',
  },
)

const toneClass = computed(() => {
  if (props.tone === 'up') return 'border-emerald-400/25 bg-emerald-400/10 text-emerald-300'
  if (props.tone === 'down') return 'border-rose-400/25 bg-rose-400/10 text-rose-300'
  if (props.tone === 'warning') return 'border-amber-300/25 bg-amber-300/10 text-amber-200'
  if (props.tone === 'accent') return 'border-sky-300/25 bg-sky-300/10 text-sky-200'
  return 'border-border bg-secondary/60 text-muted-foreground'
})
</script>
