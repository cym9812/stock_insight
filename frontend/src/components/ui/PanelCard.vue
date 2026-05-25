<template>
  <Card :class="cn('gap-0 rounded-lg border-border py-0 shadow-sm', padded && 'p-4')">
    <div v-if="$slots.header || title" class="mb-3 flex items-center justify-between gap-3">
      <slot name="header">
        <h3 class="m-0 text-sm font-semibold text-foreground">{{ title }}</h3>
      </slot>
    </div>
    <slot></slot>
  </Card>
</template>

<script setup lang="ts">
import { Card } from '@/components/ui/card'
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
