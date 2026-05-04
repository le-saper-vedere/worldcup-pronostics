<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-bold text-gray-900">World Cup Pronostics</h1>
        <nav class="flex gap-4">
          <RouterLink to="/" class="text-gray-700 hover:text-blue-600">Matches</RouterLink>
        </nav>
      </div>
    </header>
    <main class="max-w-5xl mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
