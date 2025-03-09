from datetime import datetime
from sqlalchemy.orm import Session
from app.models.feed import Feed
from app.models.article import Article
from app.services.ml_service import ml_service
import feedparser

class FeedService:
    def __init__(self, db: Session):
        self.db = db
    
    def fetch_all_feeds(self) -> None:
        """Fetch all active feeds and process new articles"""
        feeds = self.db.query(Feed).filter(Feed.is_active == True).all()
        for feed in feeds:
            self._process_feed(feed)
    
    def _process_feed(self, feed: Feed) -> None:
        """Process a single feed and extract articles"""
        parsed = feedparser.parse(str(feed.url))
        for entry in parsed.entries:
            # Check if article already exists
            existing = self.db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue
            
            # Extract article content
            title = entry.title
            summary = entry.summary if hasattr(entry, 'summary') else ''
            
            # Classify article using ML service
            classification = ml_service.classify_article(title, summary)
            
            # Create new article
            article = Article(
                title=title,
                url=entry.link,
                source=feed.name,
                summary=summary,
                category=classification["category"],
                priority=classification["priority"],
                key_points=[term["term"] for term in classification["key_terms"]],
                date_published=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                if hasattr(entry, 'published') else datetime.utcnow(),
                date_found=datetime.utcnow()
            )
            
            self.db.add(article)
        
        # Update feed metadata
        feed.last_fetched = datetime.utcnow()
        self.db.add(feed)
        self.db.commit()
    
    def get_feed_stats(self, feed_id: int) -> dict:
        """Get statistics for a feed"""
        feed = self.db.query(Feed).filter(Feed.id == feed_id).first()
        if not feed:
            return None
        
        articles = self.db.query(Article).filter(Article.source == feed.name).all()
        
        stats = {
            "total_articles": len(articles),
            "categories": {},
            "priorities": {"High": 0, "Low": 0}
        }
        
        for article in articles:
            # Count categories
            if article.category not in stats["categories"]:
                stats["categories"][article.category] = 0
            stats["categories"][article.category] += 1
            
            # Count priorities
            stats["priorities"][article.priority] += 1
        
        return stats 