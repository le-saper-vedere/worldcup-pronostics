from datetime import datetime
from pydantic import BaseModel
from schemas.user import UserRead
from schemas.match import MatchRead


class BetRead(BaseModel):
    id: int
    type: str
    predicted_home: int | None = None
    predicted_away: int | None = None
    predicted_winner: str | None = None
    points_earned: int | None = None
    created_at: datetime
    user: UserRead
    match: MatchRead

    class Config:
        from_attributes = True
