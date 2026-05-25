<template>
  <ShadcnButton :variant="variant" :size="size" :type="type">
    <slot></slot>
  </ShadcnButton>
</template>

<script setup lang="ts">
import { Button as ShadcnButton } from '@/components/ui/button'

withDefaults(
  defineProps<{
    variant?: 'default' | 'secondary' | 'ghost' | 'destructive' | 'outline' | 'link'
    size?: 'default' | 'sm' | 'lg' | 'icon' | 'icon-sm' | 'icon-lg'
    type?: 'button' | 'submit' | 'reset'
  }>(),
  {
    variant: 'default',
    size: 'default',
    type: 'button',
  },
)
</script>
