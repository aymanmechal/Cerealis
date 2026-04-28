<template>
  <div class="flex flex-col gap-5 px-5 pb-6 pt-12 animate-fade-in">
    <header class="flex items-center justify-between">
      <h1 class="text-2xl font-bold uppercase tracking-tight">Tableau de bord</h1>
      <button
        class="flex items-center justify-center rounded-full bg-secondary p-2.5 text-foreground transition-opacity active:opacity-60 disabled:opacity-40"
        :disabled="loading"
        @click="onRefresh"
      >
        <RefreshCw :class="['h-4 w-4', loading && 'animate-spin']" />
      </button>
    </header>

    <CropChips :active="crop" @change="crop = $event" />

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
        <p class="mt-1 text-xs opacity-80">{{ updatedLabel }}</p>
        <div class="mt-4 inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold backdrop-blur">
          <component :is="heroBadgeIcon" class="h-3 w-3" />
          {{ heroBadge }}
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <StatCard
        label="Variation 1 mois"
        :value="`${data.monthChange >= 0 ? '+' : ''}${data.monthChange}%`"
        :color="data.monthChange >= 0 ? 'positive' : 'negative'"
      />
      <StatCard
        label="Prix Pétrole"
        :value="`${stats.prixPetrole.toFixed(1)} $/b`"
      />
      <StatCard
        label="Inflation"
        :value="`${stats.inflation.toFixed(1)}%`"
        :color="inflationColor"
        sub="vs objectif BCE 2%"
      />
      <StatCard
        label="EUR / USD"
        :value="stats.eurUsd.toFixed(2)"
      />
    </div>

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
        {{ sellLabel }}
      </div>
    </div>

    <PriceChart :data="data.history" :year-data="yearData" />

    <Teleport to="body">
      <div
        v-if="loading"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/25 backdrop-blur-sm"
      >
        <div class="flex flex-col items-center gap-3 rounded-2xl bg-card px-8 py-6 shadow-xl">
          <RefreshCw class="h-6 w-6 animate-spin text-primary" />
          <p class="text-xs font-medium text-muted-foreground">Chargement…</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RefreshCw, Sparkles, TrendingUp, TrendingDown } from 'lucide-vue-next'
import { CROPS, cropData, marketStats as mockStats, type Crop } from '@/data/mock'
import { fetchData } from '@/services/api'
import CropChips from '@/components/CropChips.vue'
import PriceChart from '@/components/PriceChart.vue'
import StatCard from '@/components/StatCard.vue'

const crop     = ref<Crop>('Blé')
const loading  = ref(false)
const liveData  = ref<typeof cropData | null>(null)
const liveStats = ref<typeof mockStats | null>(null)

const data     = computed(() => (liveData.value ?? cropData)[crop.value])
const cropMeta = computed(() => CROPS.find(c => c.name === crop.value)!)
const stats    = computed(() => liveStats.value ?? mockStats)

const heroBadge = computed(() => {
  const yc = data.value.yearChange
  const yl = data.value.yearLabel
  if (yc !== undefined && yl) return `vs ${yl} : ${yc >= 0 ? '+' : ''}${yc}%`
  const w = data.value.weekChange
  return `${w >= 0 ? '+' : ''}${w}% tendance récente`
})

const heroBadgeIcon = computed(() => {
  const val = data.value.yearChange ?? data.value.weekChange
  return val >= 0 ? TrendingUp : TrendingDown
})

const sellLabel = computed(() => {
  const w = data.value.recommendation.window
  if (!w || w === '—' || w === 'maintenant') return 'Vendre maintenant'
  return `Vendre en ${w}`
})

const inflationColor = computed((): 'positive' | 'negative' | 'warning' => {
  const inf = stats.value.inflation
  if (inf < 2)  return 'positive'
  if (inf <= 4) return 'warning'
  return 'negative'
})

const updatedLabel = computed(() => {
  const mins = data.value.updatedMin
  const lastDate = new Date(Date.now() - mins * 60_000)
  const now = new Date()
  if (lastDate.toDateString() === now.toDateString()) return 'Mis à jour aujourd\'hui'
  return 'Dernière mise à jour : ' +
    lastDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
})

const CONFIDENCE: Partial<Record<Crop, number>> = {
  'Blé':       82,
  'Maïs':      78,
  'Orge':      80,
  'Tournesol': 74,
}

const API_KEYS: Record<Crop, string> = {
  'Blé':       'Prix_Ble',
  'Maïs':      'Prix_Mais',
  'Orge':      'Prix_Orge',
  'Sarrasin':  'Prix_Sarrasin',
  'Seigle':    'Prix_Seigle',
  'Tournesol': 'Prix_Tournesol',
  'Moutarde':  'Prix_Moutarde',
}

type ApiPoint = [string, number]

function parseDate(s: string): Date {
  const norm = /^\d{4}-\d{2}$/.test(s) ? s + '-01' : s
  return new Date(norm.includes('T') ? norm : norm + 'T00:00:00')
}

function fmtMonth(dateStr: string): string {
  return parseDate(dateStr)
    .toLocaleDateString('fr-FR', { month: 'short' })
    .replace('.', '')
}

function pctChange(current: number, past: number | null | undefined): number {
  if (!past) return 0
  return +((current - past) / past * 100).toFixed(1)
}

function priceAgo(points: ApiPoint[], days: number): number | null {
  if (points.length < 2) return null
  const target = parseDate(points[points.length - 1][0]).getTime() - days * 86_400_000
  let best: ApiPoint | null = null
  let bestDiff = Infinity
  for (const p of points.slice(0, -1)) {
    const diff = Math.abs(parseDate(p[0]).getTime() - target)
    if (diff < bestDiff) { bestDiff = diff; best = p }
  }
  return best?.[1] ?? null
}

function buildText(price: number, predites: ApiPoint[]): string {
  if (!predites.length) return 'Données de prévision non disponibles.'
  const peak = predites.reduce((b, p) => p[1] > b[1] ? p : b, predites[0])
  if (peak[1] <= price) return 'Les prix sont actuellement à leur pic. Nous recommandons de vendre maintenant.'
  const peakMonth = parseDate(peak[0]).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
  const pct = (peak[1] - price) / price * 100
  if (pct > 5) return `Une hausse significative est prévue (+${pct.toFixed(1)}%). Attendez ${peakMonth} pour maximiser vos revenus.`
  return `Une légère hausse est attendue. La fenêtre optimale de vente est prévue en ${peakMonth}.`
}

function parseCrop(c: { donnees_passees: ApiPoint[]; donnees_predites: ApiPoint[] }, cropName?: Crop): typeof cropData['Blé'] {
  const passees  = c.donnees_passees ?? []
  const predites = c.donnees_predites ?? []

  const price      = passees.length ? passees[passees.length - 1][1] : 0
  const lastDate   = passees.length ? parseDate(passees[passees.length - 1][0]) : new Date()
  const updatedMin = Math.max(0, Math.floor((Date.now() - lastDate.getTime()) / 60_000))

  const weekChange  = passees.length >= 2 ? pctChange(price, passees[passees.length - 2][1]) : 0
  const monthChange = pctChange(price, priceAgo(passees, 30))

  const yearAgo    = priceAgo(passees, 365)
  const yearChange = yearAgo !== null ? pctChange(price, yearAgo) : undefined
  const yearLabel  = yearAgo !== null
    ? String(parseDate(passees[passees.length - 1][0]).getFullYear() - 1)
    : undefined

  const history = [
    ...passees.slice(-6).map(([d, v]) => ({ month: fmtMonth(d), value: Math.round(v) })),
    ...predites.slice(0, 6).map(([d, v]) => ({ month: fmtMonth(d), value: Math.round(v), predicted: true as const })),
  ]

  let window     = '—'
  let confidence = 65
  if (predites.length) {
    const peak = predites.reduce((b, p) => p[1] > b[1] ? p : b, predites[0])
    const base = cropName !== undefined ? (CONFIDENCE[cropName] ?? 68) : 68
    if (peak[1] <= price) {
      window     = 'maintenant'
      confidence = base
    } else {
      window = parseDate(peak[0]).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
      const avg    = predites.reduce((s, p) => s + p[1], 0) / predites.length
      const spread = avg > 0 ? (peak[1] - avg) / avg : 0
      confidence   = Math.min(95, base + Math.round(spread * 200))
    }
  }

  return {
    price: Math.round(price),
    weekChange,
    monthChange,
    updatedMin,
    history,
    recommendation: { confidence, text: buildText(price, predites), window },
    yearChange,
    yearLabel,
    rawPassees: passees,
  }
}

const yearData = computed(() => {
  const raw = data.value.rawPassees
  if (!raw?.length) return []

  const byYear: Record<string, number[]> = {}
  for (const [dateStr, p] of raw) {
    const yr = String(parseDate(dateStr).getFullYear())
    ;(byYear[yr] ??= []).push(p)
  }

  return Object.entries(byYear)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([yr, prices]) => ({
      month: yr,
      value: Math.round(prices.reduce((s, p) => s + p, 0) / prices.length),
    }))
})

function mapResponse(raw: any): void {
  console.log('API response:', JSON.stringify(raw, null, 2))

  const mapped = { ...cropData } as typeof cropData
  for (const c of CROPS) {
    const apiCrop = raw[API_KEYS[c.name as Crop]]
    if (apiCrop) {
      try { mapped[c.name as Crop] = parseCrop(apiCrop, c.name as Crop) }
      catch (e) { console.warn(`Mapping failed for ${c.name}, keeping mock:`, e) }
    }
  }
  liveData.value = mapped

  const s = raw.market_stats
  if (s) {
    liveStats.value = {
      prixPetrole: s.Prix_Petrole ?? mockStats.prixPetrole,
      eurUsd:      s.Valeur_Euro  ?? mockStats.eurUsd,
      inflation:   s.Inflation    ?? mockStats.inflation,
      temperature: s.Temperature  ?? mockStats.temperature,
    }
  }
}

async function loadData(months = 12) {
  loading.value = true
  try {
    const raw = await fetchData(months)
    mapResponse(raw)
  } catch (e) {
    console.warn('API unavailable, using mock data:', e)
  } finally {
    loading.value = false
  }
}

function onRefresh() { loadData(12) }

onMounted(() => loadData(12))
</script>
