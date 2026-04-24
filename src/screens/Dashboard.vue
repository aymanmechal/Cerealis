<template>
  <div class="flex flex-col gap-5 px-5 pb-6 pt-12 animate-fade-in">
    <header class="flex items-end justify-between">
      <div>
        <p class="text-xs font-medium uppercase tracking-wider text-muted-foreground">Céréalis</p>
        <h1 class="mt-0.5 text-2xl font-bold tracking-tight">Mon tableau de bord</h1>
      </div>
      <button
        class="flex items-center gap-1.5 rounded-full bg-secondary px-3.5 py-2 text-xs font-semibold text-foreground transition-opacity active:opacity-60"
        @click="handleRefresh"
      >
        <RefreshCw :class="['h-3.5 w-3.5', refreshing && 'animate-spin']" />
        Actualiser les données
      </button>
    </header>

    <CropChips :active="crop" @change="crop = $event" />

    <!-- Hero -->
    <div class="relative overflow-hidden rounded-3xl bg-primary p-6 text-primary-foreground shadow-[0_20px_40px_-20px_hsl(var(--primary)/0.6)]">
      <div class="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/10" />
      <div class="absolute -bottom-16 -left-8 h-44 w-44 rounded-full bg-white/5" />
      <div class="relative">
        <div class="flex items-center gap-2 text-sm font-medium opacity-90">
          <span class="text-lg">{{ cropMeta.emoji }}</span>
          <span>{{ crop }}</span>
        </div>
        <div class="mt-3 flex items-baseline gap-1">
          <span class="text-6xl font-bold tracking-tight">{{ data.price }}</span>
          <span class="text-xl font-medium opacity-90">€/t</span>
        </div>
        <p class="mt-1 text-xs opacity-80">Mis à jour il y a {{ data.updatedMin }} min</p>
        <div class="mt-4 inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold backdrop-blur">
          <TrendingUp class="h-3 w-3" />
          {{ positive ? '+' : '' }}{{ data.weekChange }}% cette semaine
        </div>
      </div>
    </div>

    <!-- Stats grid -->
    <div class="grid grid-cols-2 gap-3">
      <StatCard label="Variation 1 mois" :value="`+${data.monthChange}%`" accent />
      <StatCard label="Brent" :value="`${marketStats.brent} $/b`" />
      <StatCard label="Stock mondial" :value="`${marketStats.worldStock} Mt`" />
      <StatCard label="EUR / USD" :value="marketStats.eurUsd.toFixed(2)" />
    </div>

    <!-- AI Recommendation -->
    <div class="rounded-3xl bg-accent p-5">
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary/15">
            <Sparkles class="h-4 w-4 text-primary" />
          </div>
          <h3 class="text-base font-semibold text-accent-foreground">Recommandation IA</h3>
        </div>
        <span class="rounded-full bg-white/70 px-2.5 py-1 text-[10px] font-semibold text-accent-foreground">
          Confiance IA : {{ data.recommendation.confidence }}%
        </span>
      </div>
      <p class="mt-3 text-sm leading-relaxed text-accent-foreground/90">{{ data.recommendation.text }}</p>
      <div class="mt-4 inline-flex items-center gap-1.5 rounded-full bg-primary px-3.5 py-1.5 text-xs font-semibold text-primary-foreground">
        Vendre vers {{ data.recommendation.window }}
      </div>
    </div>

    <PriceChart :data="data.history" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RefreshCw, Sparkles, TrendingUp } from 'lucide-vue-next'
import { CROPS, cropData, marketStats, type Crop } from '@/data/mock'
import CropChips from '@/components/CropChips.vue'
import PriceChart from '@/components/PriceChart.vue'
import StatCard from '@/components/StatCard.vue'

const crop = ref<Crop>('Blé')
const refreshing = ref(false)

const data = computed(() => cropData[crop.value])
const cropMeta = computed(() => CROPS.find(c => c.name === crop.value)!)
const positive = computed(() => data.value.weekChange >= 0)

function handleRefresh() {
  refreshing.value = true
  setTimeout(() => { refreshing.value = false }, 1000)
}
</script>
