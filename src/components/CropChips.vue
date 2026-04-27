<template>
  <div class="no-scrollbar -mx-5 overflow-x-auto px-5">
    <div class="flex gap-2 pb-1">
      <button
        v-for="c in VISIBLE_CROPS"
        :key="c.name"
        :class="cn(
          'shrink-0 rounded-full px-4 py-2 text-sm font-semibold transition-all',
          active === c.name
            ? 'bg-primary text-primary-foreground shadow-[0_4px_12px_-4px_hsl(var(--primary)/0.5)]'
            : 'bg-secondary text-foreground/70'
        )"
        @click="$emit('change', c.name)"
      >
        <span class="mr-1">{{ c.emoji }}</span>{{ c.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { VISIBLE_CROPS, type Crop } from '@/data/mock'
import { cn } from '@/lib/utils'

defineProps<{ active: Crop }>()
defineEmits<{ change: [crop: Crop] }>()
</script>
