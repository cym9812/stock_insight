<template>
  <button :type="type" :class="buttonVariants({ variant, size })">
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { cva } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-md text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-slate-200',
        secondary: 'border border-border bg-secondary text-secondary-foreground hover:bg-slate-600/40',
        ghost: 'text-muted-foreground hover:bg-secondary hover:text-foreground',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-rose-400',
        outline: 'border border-border bg-transparent text-foreground hover:bg-secondary',
      },
      size: {
        default: 'h-9 px-4',
        sm: 'h-8 px-3 text-xs',
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
)

withDefaults(
  defineProps<{
    variant?: 'default' | 'secondary' | 'ghost' | 'destructive' | 'outline'
    size?: 'default' | 'sm' | 'icon'
    type?: 'button' | 'submit' | 'reset'
  }>(),
  {
    variant: 'default',
    size: 'default',
    type: 'button',
  },
)
</script>
