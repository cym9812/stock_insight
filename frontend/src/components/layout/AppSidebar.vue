<script setup lang="ts">
import { ChevronsLeft, ChevronsRight } from '@lucide/vue'
import { useRoute } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import { navigationSections } from '@/config/navigation'

defineProps<{
  collapsed?: boolean
  fullWidth?: boolean
  showCollapseButton?: boolean
}>()

defineEmits<{
  toggleCollapse: []
  navigate: []
}>()

const route = useRoute()
</script>

<template>
  <nav
    class="flex h-full flex-col border-r border-border bg-slate-950/45 px-3 py-4 transition-[width] duration-200 ease-out"
    :class="collapsed ? 'w-[72px]' : fullWidth ? 'w-full' : 'w-[248px]'"
    aria-label="主导航"
  >
    <div
      class="mb-5 flex h-12 items-center"
      :class="collapsed ? 'justify-center px-0' : 'gap-3 px-2'"
    >
      <div
        v-if="!collapsed"
        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-sky-300/25 bg-sky-300/10 text-xs font-black text-sky-200"
      >
        SI
      </div>
      <div v-if="!collapsed" class="min-w-0">
        <h1 class="m-0 text-sm font-bold text-foreground">匠制科技</h1>
        <span class="block text-xs font-medium text-muted-foreground">量化工作台</span>
      </div>
        <Button
          v-if="showCollapseButton"
          variant="ghost"
          size="icon-sm"
          class="shrink-0 text-muted-foreground hover:bg-secondary/70 hover:text-foreground"
          :class="!collapsed && 'ml-auto'"
          :aria-label="collapsed ? '展开导航栏' : '收起导航栏'"
          :title="collapsed ? '展开导航栏' : '收起导航栏'"
          @click="$emit('toggleCollapse')"
        >
          <ChevronsRight v-if="collapsed" class="h-4 w-4" />
          <ChevronsLeft v-else class="h-4 w-4" />
        </Button>
    </div>

    <div class="flex flex-col gap-4">
      <section v-for="section in navigationSections" :key="section.label">
        <div v-if="!collapsed" class="px-2 pb-2 text-[11px] font-bold uppercase text-slate-500">{{ section.label }}</div>
        <div class="flex flex-col gap-1">
          <router-link
            v-for="item in section.items"
            :key="item.to"
            :to="item.to"
            class="flex h-9 items-center rounded-md text-sm font-semibold text-muted-foreground transition-colors hover:bg-secondary/60 hover:text-foreground"
            :aria-label="collapsed ? item.label : undefined"
            :title="collapsed ? item.label : undefined"
            :class="[
              collapsed ? 'justify-center px-0' : 'gap-2.5 px-2',
              item.active(route.path) && 'border border-sky-300/20 bg-sky-300/10 text-sky-100',
            ]"
            @click="$emit('navigate')"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" />
            <span v-if="!collapsed">{{ item.label }}</span>
          </router-link>
        </div>
      </section>
    </div>

    <div class="mt-auto border-t border-border pt-4">
      <div
        class="flex items-center rounded-lg bg-secondary/45 p-2"
        :class="collapsed ? 'justify-center' : 'gap-3'"
      >
        <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-700 text-xs font-bold">SI</div>
        <div v-if="!collapsed">
          <div class="text-xs font-semibold text-foreground">本地工作区</div>
          <div class="text-xs text-emerald-300">就绪</div>
        </div>
      </div>
    </div>
  </nav>
</template>
