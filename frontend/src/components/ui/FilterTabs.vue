<template>
  <div class="max-w-full overflow-x-auto">
    <ToggleGroup
      :model-value="modelValue"
      type="single"
      size="sm"
      class="inline-flex min-w-max rounded-md bg-slate-950/35 p-1"
      @update:model-value="value => value && $emit('update:modelValue', String(value))"
    >
      <ToggleGroupItem
        v-for="option in options"
        :key="option.value"
        :value="option.value"
        class="h-7 min-w-0 rounded px-3 text-xs font-bold text-muted-foreground data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
      >
        {{ option.label }}
      </ToggleGroupItem>
    </ToggleGroup>
  </div>
</template>

<script setup lang="ts">
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'

defineProps<{
  modelValue: string
  options: { label: string, value: string }[]
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
