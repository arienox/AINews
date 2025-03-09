from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User
from app.models.article import Article
from app.models.feed import Feed
from app.models.interaction import Interaction

def init_db(db: Session) -> None:
    # Create a default admin user
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_superuser=True
        )
        db.add(admin)
    
    # Add some default AI news feeds
    default_feeds = [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog/rss.xml",
            "description": "Latest updates from OpenAI"
        },
        {
            "name": "Google AI Blog",
            "url": "http://ai.googleblog.com/feeds/posts/default",
            "description": "Research and perspectives from Google AI"
        },
        {
            "name": "DeepMind Blog",
            "url": "https://deepmind.com/blog/feed/basic/",
            "description": "Latest research from DeepMind"
        }
    ]
    
    for feed_data in default_feeds:
        feed = db.query(Feed).filter(Feed.url == feed_data["url"]).first()
        if not feed:
            feed = Feed(**feed_data)
            db.add(feed)
    
    db.commit() 