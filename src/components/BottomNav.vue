<template>
  <nav class="flex-shrink-0 border-t border-border bg-background/95 backdrop-blur-xl">
    <div class="flex items-center justify-around px-2 pb-5 pt-2">
      <button
        v-for="item in items"
        :key="item.id"
        class="flex flex-1 flex-col items-center gap-1 py-1"
        @click="$emit('change', item.id)"
      >
        <component
          :is="item.icon"
          :class="cn('h-6 w-6 transition-colors', active === item.id ? 'text-primary' : 'text-muted-foreground')"
          :stroke-width="active === item.id ? 2.4 : 2"
        />
        <span :class="cn('text-[10px] font-medium transition-colors', active === item.id ? 'text-primary' : 'text-muted-foreground')">
          {{ item.label }}
        </span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Home, Map } from 'lucide-vue-next'
import { cn } from '@/lib/utils'

type Screen = 'dashboard' | 'map'

defineProps<{ active: Screen }>()
defineEmits<{ change: [screen: Screen] }>()

const items: { id: Screen; label: string; icon: unknown }[] = [
  { id: 'dashboard', label: 'Accueil', icon: Home },
  { id: 'map', label: 'Carte', icon: Map },
]
</script>
