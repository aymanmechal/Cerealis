<template>
  <div class="rounded-3xl bg-secondary/60 p-5">
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-base font-semibold">Évolution du prix</h3>
      <div class="flex items-center gap-2">
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

    <div
      ref="scrollEl"
      class="no-scrollbar"
      :class="view === 'year' ? 'overflow-x-auto' : 'overflow-x-hidden'"
    >
      <div
        class="flex flex-col"
        :style="view === 'year' ? { minWidth: current.length * 36 + 'px' } : {}"
      >
        <div class="flex items-end gap-0.5" style="height:165px">
          <div
            v-for="d in current"
            :key="d.month + '-bar'"
            :class="[
              'flex flex-col items-center gap-0.5',
              view === 'year' ? 'w-7 flex-none' : 'flex-1 min-w-0 px-0.5'
            ]"
          >
            <span
              class="text-[9px] font-semibold leading-none"
              :style="{ color: d.predicted ? 'hsl(158 55% 52%)' : 'hsl(var(--primary))' }"
            >{{ d.value }}</span>
            <div class="w-full rounded-t-sm transition-all" :style="barStyle(d)" />
          </div>
        </div>

        <div class="mt-1 flex gap-0.5">
          <div
            v-for="d in current"
            :key="d.month + '-lbl'"
            :class="[
              'flex justify-center',
              view === 'year' ? 'w-7 flex-none' : 'flex-1 min-w-0 overflow-hidden'
            ]"
            style="height:16px"
          >
            <span class="text-[9px] font-medium text-muted-foreground truncate">{{ d.month }}</span>
          </div>
        </div>
      </div>
    </div>

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
import { ref, computed, watch, nextTick } from 'vue'

interface Bar {
  month: string
  value: number
  predicted?: boolean
}

const props = defineProps<{ data: Bar[]; yearData?: Bar[] }>()

const view     = ref<'month' | 'year'>('month')
const scrollEl = ref<HTMLDivElement | null>(null)

const current = computed(() => {
  if (view.value === 'year' && props.yearData?.length) return props.yearData
  return props.data
})

watch(view, async (v) => {
  if (v === 'year') {
    await nextTick()
    if (scrollEl.value) scrollEl.value.scrollLeft = scrollEl.value.scrollWidth
  }
})

const min   = computed(() => Math.min(...current.value.map(d => d.value)))
const range = computed(() => Math.max(...current.value.map(d => d.value)) - min.value || 1)

function barHeight(value: number): number {
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
