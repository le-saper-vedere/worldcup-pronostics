from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    username: str
    avatar_url: str | None = None
    total_points: int

class Config:
    from_attributes = True