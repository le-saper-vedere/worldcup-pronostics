<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query'
import { api } from '@/services/api'
import type { Match } from '@/types/match'
import MatchCard from '@/components/MatchCard.vue'
import { computed } from 'vue'
import { formatDate } from '@/utils/dates'

const {
  data: matches,
  isLoading,
  error,
} = useQuery({
  queryKey: ['matches'],
  queryFn: () => api<Match[]>('/matches'),
})

const matchesByDate = computed(() => {
  if (!matches.value) return {}

  return matches.value.reduce(
    (acc, match) => {
      const dateKey = match.date.slice(0, 10)
      return {
        ...acc,
        [dateKey]: [...(acc[dateKey] || []), match],
      }
    },
    {} as Record<string, Match[]>,
  )
})
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Matches</h2>

    <p v-if="isLoading" class="text-gray-500">Loading...</p>
    <p v-else-if="error" class="text-red-600">Error: {{ error.message }}</p>

    <ul v-else-if="matches" class="space-y-3">
      <li v-for="(dayMatches, date) in matchesByDate" :key="date">
        <h3 class="text-lg font-semibold">{{ formatDate(date) }}</h3>
        <ul class="space-y-2">
          <li v-for="match in dayMatches" :key="match.id">
            <MatchCard :match="match" />
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
