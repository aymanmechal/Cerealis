<template>
  <div class="rounded-2xl bg-secondary/70 p-4">
    <p class="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">{{ label }}</p>
    <p :class="['mt-1.5 text-xl font-bold tracking-tight', accent ? 'text-primary' : 'text-foreground']">
      {{ value }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ label: string; value: string; accent?: boolean }>()
</script>
