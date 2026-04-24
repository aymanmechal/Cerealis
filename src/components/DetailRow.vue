<template>
  <div class="flex items-center justify-between border-b border-border/60 py-2 last:border-none">
    <span class="text-sm text-muted-foreground">{{ label }}</span>
    <span :class="['text-sm font-semibold', accent ? 'text-primary' : 'text-foreground']">{{ value }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{ label: string; value: string; accent?: boolean }>()
</script>
