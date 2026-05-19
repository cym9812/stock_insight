<template>
  <section
    :class="
      cn(
        'rounded-lg border border-border bg-card text-card-foreground shadow-sm',
        padded && 'p-4',
      )
    "
  >
    <div v-if="$slots.header || title" class="mb-3 flex items-center justify-between gap-3">
      <slot name="header">
        <h3 class="m-0 text-sm font-semibold text-foreground">{{ title }}</h3>
      </slot>
    </div>
    <slot></slot>
  </section>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'

withDefaults(
  defineProps<{
    title?: string
    padded?: boolean
  }>(),
  {
    padded: true,
  },
)
</script>
