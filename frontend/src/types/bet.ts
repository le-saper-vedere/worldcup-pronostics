export interface BetCreate {
  match_id: number
  type: 'exact' | 'winner'
  predicted_home?: number
  predicted_away?: number
  predicted_winner?: '1' | 'N' | '2'
}
