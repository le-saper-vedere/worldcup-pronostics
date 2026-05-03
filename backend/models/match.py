from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    team_home_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team_away_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    stage = Column(String(20), nullable=False)
    score_home = Column(Integer)
    score_away = Column(Integer)
    status = Column(String(20), default="upcoming")

    team_home = relationship("Team", foreign_keys=[team_home_id])
    team_away = relationship("Team", foreign_keys=[team_away_id])
