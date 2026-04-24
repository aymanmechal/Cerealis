<template>
  <div class="rounded-3xl bg-secondary/60 p-5">
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-base font-semibold">Évolution du prix</h3>
      <span class="text-xs text-muted-foreground">€/t</span>
    </div>
    <div class="flex h-40 items-end justify-between gap-1.5">
      <div
        v-for="d in data"
        :key="d.month"
        class="flex flex-1 flex-col items-center gap-1.5"
      >
        <span class="text-[9px] font-medium text-muted-foreground">{{ d.value }}</span>
        <div
          class="w-full rounded-t-md transition-all"
          :style="{
            height: barHeight(d.value) + 'px',
            backgroundColor: d.predicted ? 'hsl(var(--primary-light))' : 'hsl(var(--primary))',
          }"
        />
        <span class="text-[10px] font-medium text-muted-foreground">{{ d.month }}</span>
      </div>
    </div>
    <div class="mt-4 flex items-center justify-center gap-5 text-xs">
      <div class="flex items-center gap-1.5">
        <span class="h-2.5 w-2.5 rounded-sm bg-primary" />
        <span class="text-muted-foreground">Réalisé</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="h-2.5 w-2.5 rounded-sm bg-primary-light" />
        <span class="text-muted-foreground">Prévision IA</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Bar {
  month: string
  value: number
  predicted?: boolean
}

const props = defineProps<{ data: Bar[] }>()

const min = computed(() => Math.min(...props.data.map(d => d.value)))
const range = computed(() => Math.max(...props.data.map(d => d.value)) - min.value || 1)

function barHeight(value: number): number {
  return 30 + ((value - min.value) / range.value) * 100
}
</script>
