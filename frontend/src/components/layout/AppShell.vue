<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import MobileTopBar from '@/components/layout/MobileTopBar.vue'
import { getCurrentNavigationLabel } from '@/config/navigation'

const route = useRoute()
const isDesktopNavCollapsed = ref(false)
const isMobileNavOpen = ref(false)

const currentTitle = computed(() => getCurrentNavigationLabel(route.path))

const closeMobileNav = () => {
  isMobileNavOpen.value = false
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') closeMobileNav()
}

watch(() => route.fullPath, closeMobileNav)

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="flex h-screen w-screen overflow-hidden bg-background text-foreground">
    <aside class="hidden shrink-0 lg:block">
      <AppSidebar
        :collapsed="isDesktopNavCollapsed"
        show-collapse-button
        @toggle-collapse="isDesktopNavCollapsed = !isDesktopNavCollapsed"
      />
    </aside>

    <div class="flex min-w-0 flex-1 flex-col">
      <MobileTopBar :title="currentTitle" @open-nav="isMobileNavOpen = true" />

      <main class="min-w-0 flex-1 overflow-y-auto bg-gradient-to-b from-slate-900/60 to-background p-3 sm:p-4 lg:p-5">
        <slot />
      </main>
    </div>

    <teleport to="body">
      <transition name="mobile-nav-fade">
        <div
          v-if="isMobileNavOpen"
          class="fixed inset-0 z-40 bg-slate-950/70 backdrop-blur-sm lg:hidden"
          aria-hidden="true"
          @click="closeMobileNav"
        />
      </transition>

      <transition name="mobile-nav-slide">
        <aside
          v-if="isMobileNavOpen"
          class="fixed inset-y-0 left-0 z-50 h-dvh w-[min(82vw,320px)] lg:hidden"
          role="dialog"
          aria-modal="true"
          aria-label="移动端导航"
        >
          <AppSidebar full-width @navigate="closeMobileNav" />
        </aside>
      </transition>
    </teleport>
  </div>
</template>

<style scoped>
.mobile-nav-fade-enter-active,
.mobile-nav-fade-leave-active {
  transition: opacity 180ms ease;
}

.mobile-nav-fade-enter-from,
.mobile-nav-fade-leave-to {
  opacity: 0;
}

.mobile-nav-slide-enter-active,
.mobile-nav-slide-leave-active {
  transition: transform 200ms ease;
}

.mobile-nav-slide-enter-from,
.mobile-nav-slide-leave-to {
  transform: translateX(-100%);
}
</style>
