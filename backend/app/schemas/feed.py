from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class FeedBase(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = None
    update_frequency: Optional[int] = 3600  # in seconds

class FeedCreate(FeedBase):
    pass

class FeedUpdate(FeedBase):
    is_active: Optional[bool] = None

class FeedInDBBase(FeedBase):
    id: int
    is_active: bool
    last_fetched: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class Feed(FeedInDBBase):
    pass

class FeedWithStats(Feed):
    article_count: int
    last_article_date: Optional[datetime] 