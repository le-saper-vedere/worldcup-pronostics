from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.team import Team

router = APIRouter(prefix="/teams", tags=["teams"])

class TeamCreate(BaseModel):
      name: str
      code: str      

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.get("/{id}")
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/")
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    new_team = Team(name=team.name, code=team.code)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.put("/{id}")
def update_team(id: int, team: TeamCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team.name = team.name
    db_team.code = team.code
    db.commit()
    db.refresh(db_team)
    return db_team


@router.delete("/{id}")
def delete_team(id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted"}
