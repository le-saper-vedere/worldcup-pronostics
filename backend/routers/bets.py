from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, model_validator
from database import get_db
from models.bet import Bet
from models.match import Match
from schemas.bet import BetRead
from dependencies import get_current_user
from models.user import User
from datetime import datetime, timedelta, timezone
from typing import Literal


router = APIRouter(prefix="/bets", tags=["bets"])

class BetCreate(BaseModel):
    match_id: int
    type: Literal["exact", "winner"]
    predicted_home: int | None = None
    predicted_away: int | None = None
    predicted_winner: Literal["1", "N", "2"] | None = None

    @model_validator(mode="after")
    def check_consistency(self):
        if self.type == "exact":
            if self.predicted_home is None or self.predicted_away is None:
                raise ValueError("type='exact' requires predicted_home and predicted_away")
        elif self.type == "winner":
            if self.predicted_winner is None:
                raise ValueError("type='winner' requires predicted_winner")
        return self

@router.get("/", response_model=list[BetRead])
def get_bets(db: Session = Depends(get_db)):
    return db.query(Bet).options(
        joinedload(Bet.user),
        joinedload(Bet.match).joinedload(Match.team_home),
        joinedload(Bet.match).joinedload(Match.team_away),
    ).all()

@router.get("/me", response_model=list[BetRead])
def get_my_bets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Bet).options(
        joinedload(Bet.user),
        joinedload(Bet.match).joinedload(Match.team_home),
        joinedload(Bet.match).joinedload(Match.team_away),
    ).filter(Bet.user_id == current_user.id).all()



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
def create_bet(bet: BetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    match = db.query(Match).filter(Match.id == bet.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    deadline = match.date - timedelta(hours=1)
    if datetime.now(timezone.utc) > deadline:
        raise HTTPException(status_code=400, detail="Betting deadline has passed")
    existing_bet = db.query(Bet).filter(
        Bet.user_id == current_user.id,
        Bet.match_id == bet.match_id,
        Bet.type == bet.type,
    ).first()
    if existing_bet:
        existing_bet.predicted_home = bet.predicted_home
        existing_bet.predicted_away = bet.predicted_away
        existing_bet.predicted_winner = bet.predicted_winner
        db.commit()
        db.refresh(existing_bet)
        return existing_bet
    new_bet = Bet(
        user_id=current_user.id,
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
def update_bet(id: int, bet: BetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_bet = db.query(Bet).filter(Bet.id == id).first()
    if db_bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    if db_bet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your bet")
    db_bet.type = bet.type
    db_bet.predicted_home = bet.predicted_home
    db_bet.predicted_away = bet.predicted_away
    db_bet.predicted_winner = bet.predicted_winner
    db.commit()
    db.refresh(db_bet)
    return db_bet


@router.delete("/{id}")
def delete_bet(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_bet = db.query(Bet).filter(Bet.id == id).first()
    if db_bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    if db_bet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your bet")
    db.delete(db_bet)
    db.commit()
    return {"message": "Bet deleted"}

