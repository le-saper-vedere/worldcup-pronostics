const STAGE_LABELS: Record<string, string> = {
  group: 'Poule',
  round32: '1/16',
  round16: '1/8',
  quarter: '1/4',
  semi: '1/2',
  third: '3e place',
  final: 'Finale',
}

export const stageLabel = (stage: string): string => {
  return STAGE_LABELS[stage] ?? stage
}
