from datetime import datetime
from pydantic import BaseModel
from schemas.team import TeamRead


class MatchRead(BaseModel):
    id: int
    date: datetime
    stage: str
    status: str | None = None
    score_home: int | None = None
    score_away: int | None = None
    team_home: TeamRead
    team_away: TeamRead

    class Config:
        from_attributes = True
