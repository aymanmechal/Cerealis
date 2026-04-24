export type Crop = "Blé" | "Maïs" | "Orge" | "Colza";

export const CROPS: { name: Crop; emoji: string }[] = [
  { name: "Blé", emoji: "🌾" },
  { name: "Maïs", emoji: "🌽" },
  { name: "Orge", emoji: "🌿" },
  { name: "Colza", emoji: "🌻" },
];

export const cropData: Record<Crop, {
  price: number;
  weekChange: number;
  monthChange: number;
  updatedMin: number;
  history: { month: string; value: number; predicted?: boolean }[];
  recommendation: { confidence: number; text: string; window: string };
}> = {
  "Blé": {
    price: 218,
    weekChange: 3.2,
    monthChange: 5.1,
    updatedMin: 15,
    history: [
      { month: "Nov", value: 198 },
      { month: "Déc", value: 204 },
      { month: "Jan", value: 201 },
      { month: "Fév", value: 210 },
      { month: "Mar", value: 215 },
      { month: "Avr", value: 218 },
      { month: "Mai", value: 226, predicted: true },
      { month: "Juin", value: 232, predicted: true },
      { month: "Juil", value: 228, predicted: true },
    ],
    recommendation: {
      confidence: 78,
      text: "Une hausse modérée est attendue d'ici mi-mai grâce à la baisse des stocks mondiaux et à la tension sur la mer Noire.",
      window: "mi-mai 2026",
    },
  },
  "Maïs": {
    price: 192,
    weekChange: -1.4,
    monthChange: 2.3,
    updatedMin: 22,
    history: [
      { month: "Nov", value: 178 },
      { month: "Déc", value: 182 },
      { month: "Jan", value: 188 },
      { month: "Fév", value: 190 },
      { month: "Mar", value: 195 },
      { month: "Avr", value: 192 },
      { month: "Mai", value: 198, predicted: true },
      { month: "Juin", value: 205, predicted: true },
      { month: "Juil", value: 210, predicted: true },
    ],
    recommendation: {
      confidence: 65,
      text: "Marché stable à court terme. Une fenêtre favorable s'ouvre fin juin avec la baisse de l'offre sud-américaine.",
      window: "fin juin 2026",
    },
  },
  "Orge": {
    price: 198,
    weekChange: 1.8,
    monthChange: 3.4,
    updatedMin: 18,
    history: [
      { month: "Nov", value: 182 },
      { month: "Déc", value: 186 },
      { month: "Jan", value: 188 },
      { month: "Fév", value: 192 },
      { month: "Mar", value: 195 },
      { month: "Avr", value: 198 },
      { month: "Mai", value: 202, predicted: true },
      { month: "Juin", value: 208, predicted: true },
      { month: "Juil", value: 212, predicted: true },
    ],
    recommendation: {
      confidence: 72,
      text: "Demande brassicole soutenue. Conserver pour profiter du pic estival anticipé.",
      window: "début juillet 2026",
    },
  },
  "Colza": {
    price: 472,
    weekChange: 4.6,
    monthChange: 6.8,
    updatedMin: 9,
    history: [
      { month: "Nov", value: 432 },
      { month: "Déc", value: 445 },
      { month: "Jan", value: 451 },
      { month: "Fév", value: 460 },
      { month: "Mar", value: 465 },
      { month: "Avr", value: 472 },
      { month: "Mai", value: 488, predicted: true },
      { month: "Juin", value: 495, predicted: true },
      { month: "Juil", value: 482, predicted: true },
    ],
    recommendation: {
      confidence: 81,
      text: "Tension forte sur les huiles végétales. Vendre dès la mi-juin pour sécuriser la marge.",
      window: "mi-juin 2026",
    },
  },
};

export const marketStats = {
  brent: 82,
  worldStock: 782,
  eurUsd: 1.08,
};

export const history = {
  recommendations: [
    { date: "12 avr 2026", crop: "Blé", text: "Conserver - hausse anticipée +4% à 30 jours.", tag: "Hausse" as const },
    { date: "05 avr 2026", crop: "Colza", text: "Vendre 50% du stock — pic local probable.", tag: "Vendre" as const },
    { date: "28 mar 2026", crop: "Maïs", text: "Marché stable, attendre la mi-juin.", tag: "Stable" as const },
    { date: "20 mar 2026", crop: "Orge", text: "Demande brassicole forte, conserver.", tag: "Hausse" as const },
    { date: "11 mar 2026", crop: "Blé", text: "Vendre une partie avant correction.", tag: "Vendre" as const },
  ],
  alerts: [
    { state: "triggered" as const, date: "18 avr 2026", text: "Prix cible atteint — Blé à 225€/t" },
    { state: "pending" as const, date: "—", text: "En attente — Maïs > 200€/t" },
  ],
};
