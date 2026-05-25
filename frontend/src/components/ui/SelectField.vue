<template>
  <label class="inline-flex shrink-0 items-center gap-2 text-xs font-medium leading-5 text-muted-foreground">
    <span class="whitespace-nowrap">{{ label }}</span>
    <Select
      :model-value="modelValue"
      @update:model-value="value => $emit('update:modelValue', String(value))"
    >
      <SelectTrigger
        size="sm"
        class="h-8 min-w-20 border-input bg-slate-950/45 px-2.5 text-xs font-semibold text-foreground shadow-none hover:bg-secondary/60 focus:ring-ring"
      >
        <SelectValue :placeholder="selectedOption?.label" />
      </SelectTrigger>
      <SelectContent class="border-border bg-popover text-popover-foreground shadow-xl shadow-slate-950/35">
        <SelectItem
          v-for="option in options"
          :key="option.value"
          :value="option.value"
          class="text-xs font-semibold"
        >
          {{ option.label }}
        </SelectItem>
      </SelectContent>
    </Select>
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const props = defineProps<{
  label: string
  modelValue: string
  options: { label: string, value: string }[]
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

const selectedOption = computed(() => props.options.find(option => option.value === props.modelValue) ?? props.options[0])
</script>
