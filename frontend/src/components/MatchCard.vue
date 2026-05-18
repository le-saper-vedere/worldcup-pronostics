<script setup lang="ts">
import type { Match } from '@/types/match'
import { flagUrl } from '@/utils/flags'
import { formatTime } from '@/utils/dates'
import { stageLabel } from '@/utils/matches'

defineProps<{
  match: Match
}>()
</script>

<template>
  <UCard>
    <div class="flex items-center gap-4">
      <span class="text-sm font-semibold text-gray-600 w-14 shrink-0">
        {{ formatTime(match.date) }}
      </span>
      <img
        v-if="flagUrl(match.team_home.code)"
        :src="flagUrl(match.team_home.code)!"
        :alt="match.team_home.name"
        class="w-6 h-4 object-cover rounded-sm"
      />
      <span>{{ match.team_home.name }}</span>
      <span class="text-gray-400">vs</span>
      <img
        v-if="flagUrl(match.team_away.code)"
        :src="flagUrl(match.team_away.code)!"
        :alt="match.team_away.name"
        class="w-6 h-4 object-cover rounded-sm"
      />
      <span>{{ match.team_away.name }}</span>
      <UBadge color="neutral" variant="subtle" size="sm" class="ml-auto shrink-0">
        {{ stageLabel(match.stage) }}
      </UBadge>
    </div>
  </UCard>
</template>
