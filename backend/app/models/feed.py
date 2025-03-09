from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.base import Base

class Feed(Base):
    __tablename__ = "feeds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_fetched = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_frequency = Column(Integer, default=3600)  # in seconds 