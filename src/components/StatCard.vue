<template>
  <div class="rounded-2xl bg-secondary/70 p-4">
    <p class="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">{{ label }}</p>
    <div class="mt-1.5 flex items-center gap-1.5">
      <span v-if="color || accent" :class="['h-2 w-2 flex-shrink-0 rounded-full', dotClass]" />
      <p :class="['text-xl font-bold leading-none tracking-tight', valueClass]">{{ value }}</p>
    </div>
    <p v-if="sub" class="mt-1 text-[10px] leading-none text-muted-foreground">{{ sub }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  label: string
  value: string
  accent?: boolean
  color?: 'positive' | 'negative' | 'warning'
  sub?: string
}>()

const dotClass = computed(() => {
  if (props.color === 'positive' || props.accent) return 'bg-primary'
  if (props.color === 'negative') return 'bg-red-500'
  if (props.color === 'warning') return 'bg-orange-400'
  return ''
})

const valueClass = computed(() => {
  if (props.color === 'positive' || props.accent) return 'text-primary'
  if (props.color === 'negative') return 'text-red-500'
  if (props.color === 'warning') return 'text-orange-400'
  return 'text-foreground'
})
</script>
