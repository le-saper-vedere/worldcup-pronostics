from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    type = Column(String(10), nullable=False)
    predicted_home = Column(Integer)
    predicted_away = Column(Integer)
    predicted_winner = Column(String(1))
    points_earned = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
    match = relationship("Match")

    __table_args__ = (
        UniqueConstraint("user_id", "match_id", "type", name="uq_user_match_type"),
    )
