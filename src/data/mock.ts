export type Crop = "Blé" | "Maïs" | "Orge" | "Sarrasin" | "Seigle" | "Tournesol" | "Moutarde"

export const CROPS: { name: Crop; emoji: string }[] = [
  { name: "Blé",      emoji: "🌾" },
  { name: "Maïs",     emoji: "🌽" },
  { name: "Orge",     emoji: "🌿" },
  { name: "Sarrasin", emoji: "🫘" },
  { name: "Seigle",   emoji: "🌱" },
  { name: "Tournesol",emoji: "🌻" },
  { name: "Moutarde", emoji: "🌼" },
]

export const VISIBLE_CROPS: { name: Crop; emoji: string }[] = [
  { name: "Blé",       emoji: "🌾" },
  { name: "Maïs",      emoji: "🌽" },
  { name: "Orge",      emoji: "🌿" },
  { name: "Tournesol", emoji: "🌻" },
]

export const cropData: Record<Crop, {
  price: number
  weekChange: number
  monthChange: number
  updatedMin: number
  history: { month: string; value: number; predicted?: boolean }[]
  recommendation: { confidence: number; text: string; window: string }
  yearChange?: number
  yearLabel?: string
  rawPassees?: [string, number][]
}> = {
  "Blé": {
    price: 218, weekChange: 3.2, monthChange: 5.1, updatedMin: 15,
    history: [
      { month: "Nov", value: 198 }, { month: "Déc", value: 204 },
      { month: "Jan", value: 201 }, { month: "Fév", value: 210 },
      { month: "Mar", value: 215 }, { month: "Avr", value: 218 },
      { month: "Mai", value: 226, predicted: true },
      { month: "Juin", value: 232, predicted: true },
      { month: "Juil", value: 228, predicted: true },
    ],
    recommendation: { confidence: 78, text: "Une hausse modérée est attendue d'ici mi-mai grâce à la baisse des stocks mondiaux.", window: "mi-mai 2026" },
  },
  "Maïs": {
    price: 192, weekChange: -1.4, monthChange: 2.3, updatedMin: 22,
    history: [
      { month: "Nov", value: 178 }, { month: "Déc", value: 182 },
      { month: "Jan", value: 188 }, { month: "Fév", value: 190 },
      { month: "Mar", value: 195 }, { month: "Avr", value: 192 },
      { month: "Mai", value: 198, predicted: true },
      { month: "Juin", value: 205, predicted: true },
      { month: "Juil", value: 210, predicted: true },
    ],
    recommendation: { confidence: 65, text: "Marché stable à court terme. Une fenêtre favorable s'ouvre fin juin.", window: "fin juin 2026" },
  },
  "Orge": {
    price: 198, weekChange: 1.8, monthChange: 3.4, updatedMin: 18,
    history: [
      { month: "Nov", value: 182 }, { month: "Déc", value: 186 },
      { month: "Jan", value: 188 }, { month: "Fév", value: 192 },
      { month: "Mar", value: 195 }, { month: "Avr", value: 198 },
      { month: "Mai", value: 202, predicted: true },
      { month: "Juin", value: 208, predicted: true },
      { month: "Juil", value: 212, predicted: true },
    ],
    recommendation: { confidence: 72, text: "Demande brassicole soutenue. Conserver pour profiter du pic estival anticipé.", window: "début juillet 2026" },
  },
  "Sarrasin": {
    price: 398, weekChange: 2.1, monthChange: 3.8, updatedMin: 30,
    history: [
      { month: "Nov", value: 368 }, { month: "Déc", value: 375 },
      { month: "Jan", value: 380 }, { month: "Fév", value: 385 },
      { month: "Mar", value: 392 }, { month: "Avr", value: 398 },
      { month: "Mai", value: 410, predicted: true },
      { month: "Juin", value: 418, predicted: true },
      { month: "Juil", value: 412, predicted: true },
    ],
    recommendation: { confidence: 70, text: "Forte demande en alimentation bio. Pic de prix anticipé mi-juin.", window: "mi-juin 2026" },
  },
  "Seigle": {
    price: 182, weekChange: -0.8, monthChange: 1.5, updatedMin: 45,
    history: [
      { month: "Nov", value: 170 }, { month: "Déc", value: 174 },
      { month: "Jan", value: 176 }, { month: "Fév", value: 178 },
      { month: "Mar", value: 180 }, { month: "Avr", value: 182 },
      { month: "Mai", value: 186, predicted: true },
      { month: "Juin", value: 190, predicted: true },
      { month: "Juil", value: 188, predicted: true },
    ],
    recommendation: { confidence: 63, text: "Marché du seigle stable. Légère hausse prévue sur l'été.", window: "fin juin 2026" },
  },
  "Tournesol": {
    price: 456, weekChange: 3.5, monthChange: 4.2, updatedMin: 12,
    history: [
      { month: "Nov", value: 420 }, { month: "Déc", value: 430 },
      { month: "Jan", value: 438 }, { month: "Fév", value: 444 },
      { month: "Mar", value: 450 }, { month: "Avr", value: 456 },
      { month: "Mai", value: 468, predicted: true },
      { month: "Juin", value: 480, predicted: true },
      { month: "Juil", value: 472, predicted: true },
    ],
    recommendation: { confidence: 80, text: "Tension sur les huiles végétales mondiales. Opportunité de vente en juin.", window: "mi-juin 2026" },
  },
  "Moutarde": {
    price: 648, weekChange: 1.9, monthChange: 2.6, updatedMin: 60,
    history: [
      { month: "Nov", value: 610 }, { month: "Déc", value: 620 },
      { month: "Jan", value: 628 }, { month: "Fév", value: 634 },
      { month: "Mar", value: 641 }, { month: "Avr", value: 648 },
      { month: "Mai", value: 660, predicted: true },
      { month: "Juin", value: 672, predicted: true },
      { month: "Juil", value: 665, predicted: true },
    ],
    recommendation: { confidence: 75, text: "Marché de la moutarde sous tension. Conserver jusqu'au pic de juin.", window: "mi-juin 2026" },
  },
}

export const marketStats = {
  prixPetrole: 82.5,
  eurUsd: 1.08,
  inflation: 2.3,
  temperature: 14.5,
}

export const history = {
  recommendations: [
    { date: "12 avr 2026", crop: "Blé",      text: "Conserver - hausse anticipée +4% à 30 jours.",    tag: "Hausse" as const },
    { date: "05 avr 2026", crop: "Tournesol", text: "Vendre 50% du stock — pic local probable.",        tag: "Vendre" as const },
    { date: "28 mar 2026", crop: "Maïs",      text: "Marché stable, attendre la mi-juin.",             tag: "Stable" as const },
    { date: "20 mar 2026", crop: "Orge",      text: "Demande brassicole forte, conserver.",            tag: "Hausse" as const },
    { date: "11 mar 2026", crop: "Blé",       text: "Vendre une partie avant correction.",             tag: "Vendre" as const },
  ],
  alerts: [
    { state: "triggered" as const, date: "18 avr 2026", text: "Prix cible atteint — Blé à 225€/t" },
    { state: "pending"   as const, date: "—",           text: "En attente — Maïs > 200€/t" },
  ],
}
