from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from database import get_db
from models.match import Match
from schemas.match import MatchRead

router = APIRouter(prefix="/matches", tags=["matches"])

class MatchCreate(BaseModel):
    team_home_id: int
    team_away_id: int
    date: datetime
    stage: str

@router.get("/", response_model=list[MatchRead])
def get_matches(
        stage: str | None = None,
    upcoming: bool = False, 
    db: Session = Depends(get_db)): 
    query = db.query(Match).options(
    joinedload(Match.team_home),
    joinedload(Match.team_away)
)
    if stage:
        query = query.filter(Match.stage == stage)
    if upcoming:
        query = query.filter(Match.date > datetime.now())
    return query.order_by(Match.date).all()

@router.get("/{id}", response_model=MatchRead)
def get_match(id: int, db: Session = Depends(get_db)):
    match = db.query(Match).options(
        joinedload(Match.team_home),
        joinedload(Match.team_away)
    ).filter(Match.id == id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.post("/")
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    new_match = Match(
        team_home_id=match.team_home_id,
        team_away_id=match.team_away_id,
        date=match.date,
        stage=match.stage,
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match

@router.put("/{id}")
def update_match(id: int, match: MatchCreate, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.id == id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    db_match.team_home_id = match.team_home_id
    db_match.team_away_id = match.team_away_id
    db_match.date = match.date
    db_match.stage = match.stage
    db.commit()
    db.refresh(db_match)
    return db_match

@router.delete("/{id}")
def delete_match(id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.id == id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return {"message": "Match deleted"}