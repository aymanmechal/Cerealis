<template>
  <div class="flex flex-col gap-5 px-5 pb-6 pt-12 animate-fade-in">
    <header>
      <p class="text-xs font-medium uppercase tracking-wider text-muted-foreground">Céréalis</p>
      <h1 class="mt-0.5 text-2xl font-bold tracking-tight">Ma carte</h1>
    </header>

    <div class="overflow-hidden rounded-3xl shadow-sm">
      <svg
        viewBox="0 0 360 280"
        xmlns="http://www.w3.org/2000/svg"
        style="display:block;width:100%"
        aria-label="Vue aérienne de l'exploitation"
      >
        <defs>
          <pattern id="h-colza" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45 0 0)">
            <line x1="0" y1="0" x2="0" y2="8" stroke="rgba(0,0,0,0.08)" stroke-width="1.5"/>
          </pattern>
          <pattern id="h-ble" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(28 0 0)">
            <line x1="0" y1="0" x2="0" y2="10" stroke="rgba(0,0,0,0.065)" stroke-width="1.5"/>
          </pattern>
          <pattern id="h-orge" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(115 0 0)">
            <line x1="0" y1="0" x2="0" y2="8" stroke="rgba(0,0,0,0.08)" stroke-width="1.5"/>
          </pattern>
          <pattern id="h-mais" patternUnits="userSpaceOnUse" width="9" height="9" patternTransform="rotate(155 0 0)">
            <line x1="0" y1="0" x2="0" y2="9" stroke="rgba(0,0,0,0.07)" stroke-width="1.5"/>
          </pattern>
          <pattern id="road-tracks" patternUnits="userSpaceOnUse" width="28" height="18">
            <line x1="7"  y1="0" x2="7"  y2="18" stroke="rgba(0,0,0,0.07)" stroke-width="2"/>
            <line x1="21" y1="0" x2="21" y2="18" stroke="rgba(0,0,0,0.07)" stroke-width="2"/>
          </pattern>
        </defs>

        <rect width="360" height="280" fill="#d8e4cc"/>

        <polygon
          points="2,2 118,2 115,62 110,152 2,146"
          :fill="P.colza.fill"
          :stroke="sel === 'colza' ? '#fff' : P.colza.stroke"
          :stroke-width="sel === 'colza' ? 2.5 : 0.8"
          :opacity="sel && sel !== 'colza' ? 0.74 : 1"
          style="cursor:pointer"
          @click="toggle('colza')"
        />
        <polygon
          points="136,2 358,2 358,94 346,138 318,150 215,152 132,148"
          :fill="P.ble.fill"
          :stroke="sel === 'ble' ? '#fff' : P.ble.stroke"
          :stroke-width="sel === 'ble' ? 2.5 : 0.8"
          :opacity="sel && sel !== 'ble' ? 0.74 : 1"
          style="cursor:pointer"
          @click="toggle('ble')"
        />
        <polygon
          points="2,170 110,165 112,220 102,278 2,278"
          :fill="P.orge.fill"
          :stroke="sel === 'orge' ? '#fff' : P.orge.stroke"
          :stroke-width="sel === 'orge' ? 2.5 : 0.8"
          :opacity="sel && sel !== 'orge' ? 0.74 : 1"
          style="cursor:pointer"
          @click="toggle('orge')"
        />
        <polygon
          points="132,165 358,160 358,278 195,280 132,278"
          :fill="P.mais.fill"
          :stroke="sel === 'mais' ? '#fff' : P.mais.stroke"
          :stroke-width="sel === 'mais' ? 2.5 : 0.8"
          :opacity="sel && sel !== 'mais' ? 0.74 : 1"
          style="cursor:pointer"
          @click="toggle('mais')"
        />

        <polygon points="2,2 118,2 115,62 110,152 2,146"           fill="url(#h-colza)" style="pointer-events:none"/>
        <polygon points="136,2 358,2 358,94 346,138 318,150 215,152 132,148" fill="url(#h-ble)"   style="pointer-events:none"/>
        <polygon points="2,170 110,165 112,220 102,278 2,278"       fill="url(#h-orge)"  style="pointer-events:none"/>
        <polygon points="132,165 358,160 358,278 195,280 132,278"   fill="url(#h-mais)"  style="pointer-events:none"/>

        <polygon points="118,0 136,0 132,153 110,156"   fill="#A07850" style="pointer-events:none"/>
        <polygon points="0,150 360,144 360,166 0,172"    fill="#A07850" style="pointer-events:none"/>
        <polygon points="118,0 136,0 132,153 110,156"   fill="url(#road-tracks)" style="pointer-events:none"/>
        <polygon points="0,150 360,144 360,166 0,172"    fill="url(#road-tracks)" style="pointer-events:none"/>
        <line x1="118" y1="0" x2="112" y2="153" stroke="rgba(0,0,0,0.10)" stroke-width="1" style="pointer-events:none"/>
        <line x1="136" y1="0" x2="131" y2="152" stroke="rgba(0,0,0,0.10)" stroke-width="1" style="pointer-events:none"/>
        <line x1="0"   y1="151" x2="360" y2="145" stroke="rgba(0,0,0,0.10)" stroke-width="1" style="pointer-events:none"/>
        <line x1="0"   y1="171" x2="360" y2="165" stroke="rgba(0,0,0,0.10)" stroke-width="1" style="pointer-events:none"/>

        <rect x="82" y="128" width="26" height="17" rx="1.5" fill="#7A5C3A" style="pointer-events:none"/>
        <rect x="82" y="128" width="26" height="5"  rx="1.5" fill="#5C4228" style="pointer-events:none"/>
        <rect x="86" y="135" width="5"  height="5"  rx="0.5" fill="#3E2A18" style="pointer-events:none"/>
        <rect x="95" y="135" width="5"  height="5"  rx="0.5" fill="#3E2A18" style="pointer-events:none"/>
        <rect x="104" y="137" width="4" height="8"  rx="0.5" fill="#3E2A18" style="pointer-events:none"/>

        <g @click="toggle('colza')" style="cursor:pointer">
          <text x="53" y="50"   text-anchor="middle" dominant-baseline="middle" font-size="14">🌻</text>
          <text x="53" y="64"   text-anchor="middle" dominant-baseline="middle" font-size="9.5" font-weight="700" fill="#3a3937"  font-family="Inter,system-ui,sans-serif">Colza 2ha</text>
          <rect x="7"  y="71"   width="92" height="15" rx="7.5" fill="rgba(255,255,255,0.88)"/>
          <text x="53" y="78.5" text-anchor="middle" dominant-baseline="middle" font-size="7"   font-weight="600" fill="#3a3937"  font-family="Inter,system-ui,sans-serif">En croissance</text>
        </g>

        <g @click="toggle('ble')" style="cursor:pointer">
          <text x="238" y="50"  text-anchor="middle" dominant-baseline="middle" font-size="15">🌾</text>
          <text x="238" y="65"  text-anchor="middle" dominant-baseline="middle" font-size="10.5" font-weight="700" fill="#ffffff"  font-family="Inter,system-ui,sans-serif">Blé 8ha</text>
          <rect x="174" y="72"  width="128" height="16" rx="8"   fill="rgba(255,255,255,0.92)"/>
          <text x="238" y="80"  text-anchor="middle" dominant-baseline="middle" font-size="7.5" font-weight="600" fill="#1D9E75" font-family="Inter,system-ui,sans-serif">Vendre maintenant</text>
        </g>

        <g @click="toggle('orge')" style="cursor:pointer">
          <text x="52" y="194"  text-anchor="middle" dominant-baseline="middle" font-size="13">🌿</text>
          <text x="52" y="207"  text-anchor="middle" dominant-baseline="middle" font-size="9"   font-weight="700" fill="#1a5c47" font-family="Inter,system-ui,sans-serif">Orge 3ha</text>
          <rect x="5"  y="213"  width="94"  height="15" rx="7.5" fill="rgba(255,255,255,0.88)"/>
          <text x="52" y="220.5" text-anchor="middle" dominant-baseline="middle" font-size="6.8" font-weight="600" fill="#1a5c47" font-family="Inter,system-ui,sans-serif">Vendre dans 3 sem</text>
        </g>

        <g @click="toggle('mais')" style="cursor:pointer">
          <text x="245" y="190" text-anchor="middle" dominant-baseline="middle" font-size="15">🌽</text>
          <text x="245" y="205" text-anchor="middle" dominant-baseline="middle" font-size="10.5" font-weight="700" fill="#ffffff"  font-family="Inter,system-ui,sans-serif">Maïs 4ha</text>
          <rect x="181" y="212" width="128" height="16" rx="8"   fill="rgba(255,255,255,0.92)"/>
          <text x="245" y="220" text-anchor="middle" dominant-baseline="middle" font-size="7.5" font-weight="600" fill="#b07000" font-family="Inter,system-ui,sans-serif">Récolter dans 12j</text>
        </g>

        <g transform="translate(335,18)">
          <circle cx="0" cy="0" r="13" fill="white" fill-opacity="0.88"/>
          <text x="0" y="1" text-anchor="middle" dominant-baseline="middle" font-size="10" font-weight="700" fill="#1D9E75" font-family="Inter,system-ui,sans-serif">N</text>
        </g>
      </svg>
    </div>

    <Transition name="pop" mode="out-in">
      <div
        v-if="selected"
        :key="sel!"
        class="rounded-3xl bg-secondary/70 p-5"
      >
        <div class="mb-4 flex items-start justify-between gap-3">
          <div>
            <p class="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
              Parcelle sélectionnée
            </p>
            <h3 class="mt-1 text-lg font-bold">{{ selected.emoji }} {{ selected.name }}</h3>
          </div>
          <span
            class="flex-shrink-0 rounded-full px-3 py-1 text-xs font-semibold"
            :style="{
              backgroundColor: selected.fill + '28',
              color: selected.badgeColor,
              border: `1px solid ${selected.fill}50`,
            }"
          >{{ selected.status }}</span>
        </div>
        <div>
          <DetailRow label="Culture"          :value="`${selected.emoji} ${selected.name}`" />
          <DetailRow label="Surface"          :value="`${selected.surface} ha`" />
          <DetailRow label="Statut"           :value="selected.status" accent />
          <DetailRow label="Récolte estimée"  :value="selected.harvestDate" />
          <DetailRow label="Vente optimale"   :value="selected.saleDate" />
        </div>
      </div>

      <div
        v-else
        key="empty"
        class="flex items-center justify-center gap-2.5 rounded-3xl border-2 border-dashed border-border px-5 py-6"
      >
        <span class="text-base">👆</span>
        <p class="text-sm text-muted-foreground">Appuyez sur une parcelle pour voir ses détails</p>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import DetailRow from '@/components/DetailRow.vue'

type ParcelKey = 'ble' | 'mais' | 'orge' | 'colza'

interface Parcel {
  name: string
  emoji: string
  fill: string
  stroke: string
  badgeColor: string
  status: string
  surface: number
  harvestDate: string
  saleDate: string
}

const P: Record<ParcelKey, Parcel> = {
  ble: {
    name: 'Blé',   emoji: '🌾',
    fill: '#1D9E75', stroke: '#167a5b', badgeColor: '#1D9E75',
    status: 'Vendre maintenant', surface: 8,
    harvestDate: '15 juin 2026', saleDate: '30 juil 2026',
  },
  mais: {
    name: 'Maïs',  emoji: '🌽',
    fill: '#EF9F27', stroke: '#c07d0a', badgeColor: '#b07000',
    status: 'Récolter dans 12j', surface: 4,
    harvestDate: '6 mai 2026',  saleDate: '20 juin 2026',
  },
  orge: {
    name: 'Orge',  emoji: '🌿',
    fill: '#9FE1CB', stroke: '#78c4a8', badgeColor: '#1a5c47',
    status: 'Vendre dans 3 sem', surface: 3,
    harvestDate: '20 mai 2026', saleDate: '4 juil 2026',
  },
  colza: {
    name: 'Colza', emoji: '🌻',
    fill: '#B4B2A9', stroke: '#8a8880', badgeColor: '#3a3937',
    status: 'En croissance', surface: 2,
    harvestDate: '10 juil 2026', saleDate: '24 août 2026',
  },
}

const sel      = ref<ParcelKey | null>(null)
const selected = computed(() => sel.value ? P[sel.value] : null)

function toggle(id: ParcelKey) {
  sel.value = sel.value === id ? null : id
}
</script>

<style scoped>
.pop-enter-active {
  transition: opacity 0.2s ease, transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-leave-active {
  transition: opacity 0.14s ease-in, transform 0.14s ease-in;
}
.pop-enter-from {
  opacity: 0;
  transform: scale(0.96) translateY(8px);
}
.pop-leave-to {
  opacity: 0;
  transform: scale(0.98) translateY(4px);
}
</style>
