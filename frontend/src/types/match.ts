export interface Team {
  id: number
  name: string
  code: string
  group: string
}

export interface Match {
  id: number
  date: string
  stage: string
  status: string | null
  score_home: number | null
  score_away: number | null
  team_home: Team
  team_away: Team
}
