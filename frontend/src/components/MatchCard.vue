<script setup lang="ts">
import type { Match } from '@/types/match'
import { flagUrl } from '@/utils/flags'
import { formatTime } from '@/utils/dates'
import { stageLabel } from '@/utils/matches'
import { computed, ref } from 'vue'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from '@nuxt/ui/composables/useToast'
import { api } from '@/services/api'
import type { BetCreate } from '@/types/bet'

const props = defineProps<{
  match: Match
}>()

const queryClient = useQueryClient()
const toast = useToast()

const isOpen = ref(false)

const homeScore = ref<number | null>(null)
const awayScore = ref<number | null>(null)
const winner = ref<'1' | 'N' | '2' | null>(null)

const winnerOptions = computed(() => [
  { value: '1', label: `${props.match.team_home.name} gagne` },
  { value: 'N', label: 'Match nul' },
  { value: '2', label: `${props.match.team_away.name} gagne` },
])

const { mutate, isPending } = useMutation({
  mutationFn: (data: BetCreate) => api('/bets/', { method: 'POST', body: data }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['bets'] })
    homeScore.value = null
    awayScore.value = null
    winner.value = null
    isOpen.value = false
    toast.add({
      title: 'Pronostic enregistré',
      description: `${props.match.team_home.name} vs ${props.match.team_away.name}`,
      icon: 'i-lucide-check-circle',
      color: 'success',
    })
  },
  onError: (error: Error) => {
    toast.add({
      title: 'Erreur',
      description: error.message,
      icon: 'i-lucide-alert-circle',
      color: 'error',
    })
  },
})

function handleSubmit() {
  if (homeScore.value !== null && awayScore.value !== null) {
    mutate({
      match_id: props.match.id,
      type: 'exact',
      predicted_home: homeScore.value,
      predicted_away: awayScore.value,
    })
  }
  if (winner.value !== null) {
    mutate({
      match_id: props.match.id,
      type: 'winner',
      predicted_winner: winner.value,
    })
  }
}
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
      <UButton
        size="sm"
        variant="soft"
        :icon="isOpen ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
        @click="isOpen = !isOpen"
      >
        {{ isOpen ? 'Fermer' : 'Pronostiquer' }}
      </UButton>
    </div>

    <div v-if="isOpen" class="mt-4 pt-4 border-t border-gray-200 space-y-6">
      <div>
        <div class="flex items-baseline justify-between mb-3">
          <h4 class="text-sm font-semibold text-gray-800">Score exact</h4>
          <span class="text-xs text-gray-500">5 points si tu trouves</span>
        </div>
        <div class="flex items-center justify-center gap-4">
          <div class="flex flex-col items-center gap-1">
            <span class="text-xs text-gray-600">{{ match.team_home.name }}</span>
            <UInput
              v-model.number="homeScore"
              type="number"
              min="0"
              placeholder="0"
              class="w-20"
              :ui="{ base: 'text-center text-lg font-semibold' }"
            />
          </div>
          <span class="text-gray-400 text-xl mt-5">–</span>
          <div class="flex flex-col items-center gap-1">
            <span class="text-xs text-gray-600">{{ match.team_away.name }}</span>
            <UInput
              v-model.number="awayScore"
              type="number"
              min="0"
              placeholder="0"
              class="w-20"
              :ui="{ base: 'text-center text-lg font-semibold' }"
            />
          </div>
        </div>
      </div>

      <div>
        <div class="flex items-baseline justify-between mb-3">
          <h4 class="text-sm font-semibold text-gray-800">Sinon, juste le vainqueur</h4>
          <span class="text-xs text-gray-500">1 point si tu trouves</span>
        </div>
        <URadioGroup v-model="winner" :items="winnerOptions" />
      </div>

      <div class="flex justify-end pt-2 border-t border-gray-100">
        <UButton
          size="md"
          variant="solid"
          icon="i-lucide-check"
          :loading="isPending"
          :disabled="isPending"
          @click="handleSubmit"
        >
          Valider mon pronostic
        </UButton>
      </div>
    </div>
  </UCard>
</template>
