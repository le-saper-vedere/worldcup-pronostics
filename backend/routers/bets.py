from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from database import get_db
from models.bet import Bet
from models.match import Match
from schemas.bet import BetRead

router = APIRouter(prefix="/bets", tags=["bets"])


class BetCreate(BaseModel):
    user_id: int
    match_id: int
    type: str
    predicted_home: int | None = None
    predicted_away: int | None = None
    predicted_winner: str | None = None


@router.get("/", response_model=list[BetRead])
def get_bets(db: Session = Depends(get_db)):
    return db.query(Bet).options(
        joinedload(Bet.user),
        joinedload(Bet.match).joinedload(Match.team_home),
        joinedload(Bet.match).joinedload(Match.team_away),
    ).all()


@router.get("/{id}", response_model=BetRead)
def get_bet(id: int, db: Session = Depends(get_db)):
    bet = db.query(Bet).options(
        joinedload(Bet.user),
        joinedload(Bet.match).joinedload(Match.team_home),
        joinedload(Bet.match).joinedload(Match.team_away),
    ).filter(Bet.id == id).first()
    if bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet


@router.post("/")
def create_bet(bet: BetCreate, db: Session = Depends(get_db)):
    new_bet = Bet(
        user_id=bet.user_id,
        match_id=bet.match_id,
        type=bet.type,
        predicted_home=bet.predicted_home,
        predicted_away=bet.predicted_away,
        predicted_winner=bet.predicted_winner,
    )
    db.add(new_bet)
    db.commit()
    db.refresh(new_bet)
    return new_bet


@router.put("/{id}")
def update_bet(id: int, bet: BetCreate, db: Session = Depends(get_db)):
    db_bet = db.query(Bet).filter(Bet.id == id).first()
    if db_bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    db_bet.user_id = bet.user_id
    db_bet.match_id = bet.match_id
    db_bet.type = bet.type
    db_bet.predicted_home = bet.predicted_home
    db_bet.predicted_away = bet.predicted_away
    db_bet.predicted_winner = bet.predicted_winner
    db.commit()
    db.refresh(db_bet)
    return db_bet


@router.delete("/{id}")
def delete_bet(id: int, db: Session = Depends(get_db)):
    db_bet = db.query(Bet).filter(Bet.id == id).first()
    if db_bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    db.delete(db_bet)
    db.commit()
    return {"message": "Bet deleted"}
