<template>
  <div class="flex flex-col gap-5 px-5 pb-6 pt-12 animate-fade-in">
    <header class="flex items-center justify-between">
      <h1 class="text-2xl font-bold uppercase tracking-tight">Tableau de bord</h1>
      <button
        class="flex items-center justify-center rounded-full bg-secondary p-2.5 text-foreground transition-opacity active:opacity-60 disabled:opacity-40"
        :disabled="loading"
        @click="handleRefresh"
      >
        <RefreshCw :class="['h-4 w-4', loading && 'animate-spin']" />
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
        <p class="mt-1 text-xs opacity-80">{{ updatedLabel }}</p>
        <!-- Year-on-year badge -->
        <div class="mt-4 inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold backdrop-blur">
          <component :is="heroBadgeIcon" class="h-3 w-3" />
          {{ heroBadge }}
        </div>
      </div>
    </div>

    <!-- Stats grid -->
    <div class="grid grid-cols-2 gap-3">
      <StatCard
        label="Variation 1 mois"
        :value="`${data.monthChange >= 0 ? '+' : ''}${data.monthChange}%`"
        :color="data.monthChange >= 0 ? 'positive' : 'negative'"
      />
      <StatCard
        label="Prix Pétrole"
        :value="`${activeMarketStats.prixPetrole.toFixed(1)} $/b`"
      />
      <StatCard
        label="Inflation"
        :value="`${activeMarketStats.inflation.toFixed(1)}%`"
        :color="inflationColor"
        sub="vs objectif BCE 2%"
      />
      <StatCard
        label="EUR / USD"
        :value="activeMarketStats.eurUsd.toFixed(2)"
      />
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
        {{ sellLabel }}
      </div>
    </div>

    <PriceChart :data="data.history" :year-data="yearChartData" />

    <!-- Loading overlay -->
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
import { CROPS, cropData, marketStats as mockMarketStats, type Crop } from '@/data/mock'
import { fetchData } from '@/services/api'
import CropChips from '@/components/CropChips.vue'
import PriceChart from '@/components/PriceChart.vue'
import StatCard from '@/components/StatCard.vue'

// ── State ─────────────────────────────────────────────────────────────────────

const crop = ref<Crop>('Blé')
const loading = ref(false)
const liveCropData = ref<typeof cropData | null>(null)
const liveMarketStats = ref<typeof mockMarketStats | null>(null)

const data              = computed(() => (liveCropData.value ?? cropData)[crop.value])
const cropMeta          = computed(() => CROPS.find(c => c.name === crop.value)!)
const activeMarketStats = computed(() => liveMarketStats.value ?? mockMarketStats)

// ── Hero badge (year-on-year or fallback to recent trend) ─────────────────────

const heroBadge = computed(() => {
  const yc = data.value.yearChange
  const yl = data.value.yearLabel
  if (yc !== undefined && yl) {
    return `vs ${yl} : ${yc >= 0 ? '+' : ''}${yc}%`
  }
  const w = data.value.weekChange
  return `${w >= 0 ? '+' : ''}${w}% tendance récente`
})

const heroBadgeIcon = computed(() => {
  const val = data.value.yearChange ?? data.value.weekChange
  return val >= 0 ? TrendingUp : TrendingDown
})

// ── Sell button label ─────────────────────────────────────────────────────────

const sellLabel = computed(() => {
  const w = data.value.recommendation.window
  if (!w || w === '—' || w === 'maintenant') return 'Vendre maintenant'
  return `Vendre en ${w}`
})

// ── Stat card helpers ─────────────────────────────────────────────────────────

const inflationColor = computed((): 'positive' | 'negative' | 'warning' => {
  const inf = activeMarketStats.value.inflation
  if (inf < 2)  return 'positive'
  if (inf <= 4) return 'warning'
  return 'negative'
})

// ── Last-update label ─────────────────────────────────────────────────────────

const updatedLabel = computed(() => {
  const mins = data.value.updatedMin
  const lastDate = new Date(Date.now() - mins * 60_000)
  const now = new Date()
  if (lastDate.toDateString() === now.toDateString()) return 'Mis à jour aujourd\'hui'
  return 'Dernière mise à jour : ' +
    lastDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
})

// ── Per-crop base confidence values ──────────────────────────────────────────

const CROP_CONFIDENCE: Partial<Record<Crop, number>> = {
  'Blé':       82,
  'Maïs':      78,
  'Tournesol': 74,
}

// ── API key mapping ───────────────────────────────────────────────────────────

const CROP_API_KEYS: Record<Crop, string> = {
  'Blé':       'Prix_Ble',
  'Maïs':      'Prix_Mais',
  'Orge':      'Prix_Orge',
  'Sarrasin':  'Prix_Sarrasin',
  'Seigle':    'Prix_Seigle',
  'Tournesol': 'Prix_Tournesol',
  'Moutarde':  'Prix_Moutarde',
}

// ── Date / format helpers ─────────────────────────────────────────────────────

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

// ── Price helpers ─────────────────────────────────────────────────────────────

function pctChange(current: number, past: number | null | undefined): number {
  if (!past) return 0
  return +((current - past) / past * 100).toFixed(1)
}

function priceNDaysAgo(points: ApiPoint[], days: number): number | null {
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

// ── AI recommendation text ────────────────────────────────────────────────────

function buildRecommText(currentPrice: number, predites: ApiPoint[]): string {
  if (!predites.length) return 'Données de prévision non disponibles.'
  const peak = predites.reduce((b, p) => p[1] > b[1] ? p : b, predites[0])
  if (peak[1] <= currentPrice) {
    return 'Les prix sont actuellement à leur pic. Nous recommandons de vendre maintenant.'
  }
  const peakMonth = parseDate(peak[0]).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
  const pctAbove  = (peak[1] - currentPrice) / currentPrice * 100
  if (pctAbove > 5)
    return `Une hausse significative est prévue (+${pctAbove.toFixed(1)}%). Attendez ${peakMonth} pour maximiser vos revenus.`
  return `Une légère hausse est attendue. La fenêtre optimale de vente est prévue en ${peakMonth}.`
}

// ── Core mapping: one API crop → dashboard entry ──────────────────────────────

function mapApiCrop(c: { donnees_passees: ApiPoint[]; donnees_predites: ApiPoint[] }, cropName?: Crop): typeof cropData['Blé'] {
  const passees = c.donnees_passees ?? []
  const predites = c.donnees_predites ?? []

  const currentPrice = passees.length ? passees[passees.length - 1][1] : 0
  const lastDate     = passees.length ? parseDate(passees[passees.length - 1][0]) : new Date()
  const updatedMin   = Math.max(0, Math.floor((Date.now() - lastDate.getTime()) / 60_000))

  const weekChange  = passees.length >= 2 ? pctChange(currentPrice, passees[passees.length - 2][1]) : 0
  const monthChange = pctChange(currentPrice, priceNDaysAgo(passees, 30))

  // Year-on-year: compare current price to price ~365 days ago
  const yearAgoPrice = priceNDaysAgo(passees, 365)
  const yearChange   = yearAgoPrice !== null ? pctChange(currentPrice, yearAgoPrice) : undefined
  const yearLabel    = yearAgoPrice !== null
    ? String(parseDate(passees[passees.length - 1][0]).getFullYear() - 1)
    : undefined

  // Chart: last 6 historical (solid) + up to 6 predicted (light + dashed)
  const history = [
    ...passees.slice(-6).map(([d, v]) => ({ month: fmtMonth(d), value: Math.round(v) })),
    ...predites.slice(0, 6).map(([d, v]) => ({ month: fmtMonth(d), value: Math.round(v), predicted: true as const })),
  ]

  let window     = '—'
  let confidence = 65
  if (predites.length) {
    const peak = predites.reduce((b, p) => p[1] > b[1] ? p : b, predites[0])
    // Use per-crop base confidence when available, otherwise derive from spread
    const baseConfidence = cropName !== undefined ? (CROP_CONFIDENCE[cropName] ?? 68) : 68
    if (peak[1] <= currentPrice) {
      window     = 'maintenant'
      confidence = baseConfidence
    } else {
      window = parseDate(peak[0]).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
      const avg    = predites.reduce((s, p) => s + p[1], 0) / predites.length
      const spread = avg > 0 ? (peak[1] - avg) / avg : 0
      confidence   = Math.min(95, baseConfidence + Math.round(spread * 200))
    }
  }

  return {
    price: Math.round(currentPrice),
    weekChange,
    monthChange,
    updatedMin,
    history,
    recommendation: { confidence, text: buildRecommText(currentPrice, predites), window },
    yearChange,
    yearLabel,
    rawPassees: passees,
  }
}

// ── Year chart data (grouped by year, averages) ───────────────────────────────

const yearChartData = computed(() => {
  const raw = data.value.rawPassees
  if (!raw?.length) return []

  const byYear: Record<string, number[]> = {}
  for (const [dateStr, price] of raw) {
    const yr = String(parseDate(dateStr).getFullYear())
    ;(byYear[yr] ??= []).push(price)
  }

  return Object.entries(byYear)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([yr, prices]) => ({
      month: yr,
      value: Math.round(prices.reduce((s, p) => s + p, 0) / prices.length),
    }))
})

// ── Response mapper ───────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapResponse(raw: any): void {
  console.log('API response:', JSON.stringify(raw, null, 2))

  const mapped = { ...cropData } as typeof cropData
  for (const c of CROPS) {
    const apiCrop = raw[CROP_API_KEYS[c.name as Crop]]
    if (apiCrop) {
      try { mapped[c.name as Crop] = mapApiCrop(apiCrop, c.name as Crop) }
      catch (e) { console.warn(`Mapping failed for ${c.name}, keeping mock:`, e) }
    }
  }
  liveCropData.value = mapped

  const stats = raw.market_stats
  if (stats) {
    liveMarketStats.value = {
      prixPetrole: stats.Prix_Petrole ?? mockMarketStats.prixPetrole,
      eurUsd:      stats.Valeur_Euro  ?? mockMarketStats.eurUsd,
      inflation:   stats.Inflation    ?? mockMarketStats.inflation,
      temperature: stats.Temperature  ?? mockMarketStats.temperature,
    }
  }
}

// ── Data loading ──────────────────────────────────────────────────────────────

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

function handleRefresh() { loadData(12) }

onMounted(() => loadData(12))
</script>
