from pydantic import BaseModel

class TeamRead(BaseModel):
    id: int
    name: str
    code: str
    group: str

    class Config:
        from_attributes = True