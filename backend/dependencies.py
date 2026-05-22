from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    # Mocked data
    user = db.query(User).filter(User.id == 1).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
