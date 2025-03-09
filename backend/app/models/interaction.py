from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    interaction_type = Column(String)  # click, save, dismiss, share
    timestamp = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    article = relationship("Article", back_populates="interactions") 