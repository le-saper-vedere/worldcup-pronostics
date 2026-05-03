from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    slack_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    total_points = Column(Integer, nullable=False, server_default="0")
    avatar_url = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())