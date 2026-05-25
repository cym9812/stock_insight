<script setup lang="ts">
import { Menu } from '@lucide/vue'
import Button from '@/components/ui/Button.vue'

defineProps<{
  title: string
}>()

defineEmits<{
  openNav: []
}>()
</script>

<template>
  <header class="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-slate-950/55 px-3 lg:hidden">
    <Button
      variant="ghost"
      size="icon"
      class="shrink-0 text-muted-foreground hover:bg-secondary/70 hover:text-foreground"
      aria-label="打开导航菜单"
      title="打开导航菜单"
      @click="$emit('openNav')"
    >
      <Menu class="h-5 w-5" />
    </Button>
    <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-sky-300/25 bg-sky-300/10 text-[11px] font-black text-sky-200">
      SI
    </div>
    <div class="min-w-0">
      <div class="truncate text-sm font-bold text-foreground">{{ title }}</div>
      <div class="text-xs font-medium text-muted-foreground">量化工作台</div>
    </div>
  </header>
</template>
