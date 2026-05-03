from sqlalchemy import Column, Integer, String
from database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(3), unique=True, nullable=False)
    flag_url = Column(String(255))
    group = Column(String(1))
