<template>
  <div class="rounded-3xl bg-secondary/60 p-5">
    <!-- Header -->
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-base font-semibold">Évolution du prix</h3>
      <div class="flex items-center gap-2">
        <!-- Mois / Année toggle — only when year data is available -->
        <div v-if="yearData?.length" class="flex rounded-full bg-secondary p-0.5 text-[11px]">
          <button
            :class="['rounded-full px-2.5 py-1 font-semibold transition-all',
              view === 'month' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground']"
            @click="view = 'month'"
          >Mois</button>
          <button
            :class="['rounded-full px-2.5 py-1 font-semibold transition-all',
              view === 'year' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground']"
            @click="view = 'year'"
          >Année</button>
        </div>
        <span class="text-xs text-muted-foreground">€/t</span>
      </div>
    </div>

    <!-- Bar area: 165 px container; each column = price label (≤12 px) + gap + bar (max 128 px) = ≤142 px — never clips -->
    <div class="flex items-end gap-0.5 overflow-hidden" style="height:165px">
      <div
        v-for="d in current"
        :key="d.month + '-bar'"
        class="flex min-w-0 flex-1 flex-col items-center gap-0.5 overflow-hidden px-0.5"
      >
        <span
          class="text-[9px] font-semibold leading-none"
          :style="{ color: d.predicted ? 'hsl(158 55% 52%)' : 'hsl(var(--primary))' }"
        >{{ d.value }}</span>
        <div class="w-full rounded-t-sm transition-all" :style="barStyle(d)" />
      </div>
    </div>

    <!-- Label row: separate container so it's never obscured by overflow:hidden above -->
    <div class="mt-1 flex gap-0.5">
      <div
        v-for="d in current"
        :key="d.month + '-lbl'"
        class="flex min-w-0 flex-1 justify-center overflow-hidden"
        style="height:28px"
      >
        <span
          class="text-[9px] font-medium text-muted-foreground"
          style="writing-mode:vertical-rl; transform:rotate(180deg); white-space:nowrap"
        >{{ d.month }}</span>
      </div>
    </div>

    <!-- Legend (month view only) -->
    <div v-if="view === 'month'" class="mt-3 flex items-center justify-center gap-5 text-xs">
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
import { ref, computed } from 'vue'

interface Bar {
  month: string
  value: number
  predicted?: boolean
}

const props = defineProps<{ data: Bar[]; yearData?: Bar[] }>()

const view = ref<'month' | 'year'>('month')

const current = computed(() =>
  view.value === 'year' && props.yearData?.length ? props.yearData : props.data
)

const min   = computed(() => Math.min(...current.value.map(d => d.value)))
const range = computed(() => Math.max(...current.value.map(d => d.value)) - min.value || 1)

function barHeight(value: number): number {
  // 20 px floor, 108 px range → max 128 px; label (~12 px) + gap (2 px) + bar (128 px) = 142 px < 165 px container
  return 20 + ((value - min.value) / range.value) * 108
}

function barStyle(d: Bar): Record<string, string> {
  const h = barHeight(d.value) + 'px'
  if (d.predicted) {
    return {
      height: h,
      backgroundColor: 'hsl(var(--primary-light))',
      borderTop: '2px dashed hsl(var(--primary))',
    }
  }
  return { height: h, backgroundColor: 'hsl(var(--primary))' }
}
</script>
