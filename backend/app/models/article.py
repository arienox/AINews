from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    source = Column(String)
    summary = Column(Text)
    category = Column(String)
    priority = Column(String)
    key_points = Column(ARRAY(String))
    action_items = Column(ARRAY(String))
    date_published = Column(DateTime)
    date_found = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)
    
    # Relationships
    users = relationship("User", secondary="user_articles", back_populates="articles")
    interactions = relationship("Interaction", back_populates="article") 