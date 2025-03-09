from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.schemas.feed import Feed, FeedCreate, FeedUpdate, FeedWithStats
from app.models.feed import Feed as FeedModel
from app.models.article import Article
from app.db.session import get_db
from sqlalchemy import func
from datetime import datetime
import feedparser

router = APIRouter()

def fetch_feed_articles(feed_id: int, db: Session):
    """Background task to fetch articles from a feed"""
    feed = db.query(FeedModel).filter(FeedModel.id == feed_id).first()
    if not feed or not feed.is_active:
        return
    
    parsed = feedparser.parse(str(feed.url))
    for entry in parsed.entries:
        # Check if article already exists
        existing = db.query(Article).filter(Article.url == entry.link).first()
        if existing:
            continue
        
        article = Article(
            title=entry.title,
            url=entry.link,
            source=feed.name,
            summary=entry.summary if hasattr(entry, 'summary') else '',
            date_published=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
            if hasattr(entry, 'published') else datetime.utcnow(),
            date_found=datetime.utcnow()
        )
        db.add(article)
    
    feed.last_fetched = datetime.utcnow()
    db.commit()

@router.post("/", response_model=Feed)
def create_feed(feed: FeedCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_feed = db.query(FeedModel).filter(FeedModel.url == str(feed.url)).first()
    if db_feed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feed with this URL already exists"
        )
    
    db_feed = FeedModel(**feed.dict())
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    
    # Schedule initial feed fetch
    background_tasks.add_task(fetch_feed_articles, db_feed.id, db)
    
    return db_feed

@router.get("/", response_model=List[FeedWithStats])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = db.query(
        FeedModel,
        func.count(Article.id).label('article_count'),
        func.max(Article.date_published).label('last_article_date')
    ).outerjoin(Article, Article.source == FeedModel.name
    ).group_by(FeedModel.id
    ).offset(skip).limit(limit).all()
    
    return [
        {
            **feed[0].__dict__,
            'article_count': feed[1],
            'last_article_date': feed[2]
        }
        for feed in feeds
    ]

@router.get("/{feed_id}", response_model=FeedWithStats)
def read_feed(feed_id: int, db: Session = Depends(get_db)):
    feed = db.query(
        FeedModel,
        func.count(Article.id).label('article_count'),
        func.max(Article.date_published).label('last_article_date')
    ).outerjoin(Article, Article.source == FeedModel.name
    ).filter(FeedModel.id == feed_id
    ).group_by(FeedModel.id).first()
    
    if feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )
    
    return {
        **feed[0].__dict__,
        'article_count': feed[1],
        'last_article_date': feed[2]
    }

@router.put("/{feed_id}", response_model=Feed)
def update_feed(feed_id: int, feed: FeedUpdate, db: Session = Depends(get_db)):
    db_feed = db.query(FeedModel).filter(FeedModel.id == feed_id).first()
    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )
    
    update_data = feed.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_feed, field, value)
    
    db.commit()
    db.refresh(db_feed)
    return db_feed

@router.delete("/{feed_id}", response_model=Feed)
def delete_feed(feed_id: int, db: Session = Depends(get_db)):
    db_feed = db.query(FeedModel).filter(FeedModel.id == feed_id).first()
    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )
    
    db.delete(db_feed)
    db.commit()
    return db_feed

@router.post("/{feed_id}/fetch", response_model=Feed)
def fetch_feed(feed_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_feed = db.query(FeedModel).filter(FeedModel.id == feed_id).first()
    if db_feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )
    
    background_tasks.add_task(fetch_feed_articles, feed_id, db)
    return db_feed 