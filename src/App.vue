<template>
  <div class="min-h-screen bg-secondary/40">
    <div class="app-shell">
      <main class="min-h-0 flex-1 overflow-y-auto">
        <Dashboard v-if="screen === 'dashboard'" />
        <MapScreen v-else-if="screen === 'map'" />
      </main>
      <BottomNav :active="screen" @change="screen = $event" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Dashboard from './screens/Dashboard.vue'
import MapScreen from './screens/MapScreen.vue'
import BottomNav from './components/BottomNav.vue'

type Screen = 'dashboard' | 'map'
const screen = ref<Screen>('dashboard')
</script>
