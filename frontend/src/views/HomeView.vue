<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query'
import { api } from '@/services/api'
import type { Match } from '@/types/match'

const {
  data: matches,
  isLoading,
  error,
} = useQuery({
  queryKey: ['matches'],
  queryFn: () => api<Match[]>('/matches'),
})
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Matches</h2>

    <p v-if="isLoading" class="text-gray-500">Loading...</p>
    <p v-else-if="error" class="text-red-600">Error: {{ error.message }}</p>

    <ul v-else-if="matches" class="space-y-3">
      <li
        v-for="match in matches"
        :key="match.id"
        class="bg-white rounded-lg shadow p-4 flex items-center justify-between"
      >
        <span class="font-medium">{{ match.team_home.name }}</span>
        <span class="text-gray-400 mx-4">vs</span>
        <span class="font-medium">{{ match.team_away.name }}</span>
      </li>
    </ul>
  </div>
</template>
