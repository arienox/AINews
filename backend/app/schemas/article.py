from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    url: HttpUrl
    source: str
    summary: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = "Low"
    key_points: Optional[List[str]] = []
    action_items: Optional[List[str]] = []

class ArticleCreate(ArticleBase):
    date_published: Optional[datetime] = None

class ArticleUpdate(ArticleBase):
    is_archived: Optional[bool] = None

class ArticleInDBBase(ArticleBase):
    id: int
    date_published: Optional[datetime]
    date_found: datetime
    is_archived: bool

    class Config:
        from_attributes = True

class Article(ArticleInDBBase):
    pass

class ArticleWithInteractions(Article):
    interaction_count: int
    save_count: int
    click_count: int 