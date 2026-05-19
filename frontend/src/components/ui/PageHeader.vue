<template>
  <header class="mb-5 flex items-center justify-between gap-4 max-md:flex-col max-md:items-start">
    <div class="min-w-0">
      <span
        v-if="eyebrow"
        class="mb-2 inline-flex h-6 items-center rounded-full border border-border bg-secondary/70 px-2.5 text-[11px] font-bold text-muted-foreground"
      >
        {{ eyebrow }}
      </span>
      <h1 class="m-0 text-2xl font-bold leading-tight text-foreground md:text-[1.7rem]">{{ title }}</h1>
      <p v-if="subtitle" class="mt-1.5 max-w-3xl text-sm leading-6 text-muted-foreground">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.actions" class="flex items-center gap-2.5 max-md:w-full max-md:flex-wrap">
      <slot name="actions"></slot>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  eyebrow?: string
}>()
</script>
