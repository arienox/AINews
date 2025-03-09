from app.ml.models.article_classifier import ArticleClassifier
from app.models.article import Article
from app.models.interaction import Interaction
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta

class MLService:
    def __init__(self):
        self.classifier = ArticleClassifier()
        try:
            self.classifier.load()
        except ValueError:
            # Model not trained yet
            pass
    
    def classify_article(self, title: str, summary: str) -> Dict[str, Any]:
        """Classify a new article"""
        # Combine title and summary for classification
        text = f"{title}\n{summary}"
        
        try:
            return self.classifier.predict(text)
        except ValueError:
            # Return default classification if model is not trained
            return {
                "category": "Uncategorized",
                "category_confidence": 0.0,
                "priority": "Low",
                "priority_confidence": 0.0,
                "key_terms": []
            }
    
    def train_model(self, db: Session) -> None:
        """Train the model using historical data"""
        # Get articles with interactions
        articles = db.query(Article).filter(
            Article.category.isnot(None),
            Article.priority.isnot(None)
        ).all()
        
        if not articles:
            raise ValueError("No labeled articles available for training")
        
        texts = [f"{article.title}\n{article.summary}" for article in articles]
        categories = [article.category for article in articles]
        priorities = [article.priority for article in articles]
        
        # Train the model
        self.classifier.fit(texts, categories, priorities)
        
        # Save the model
        self.classifier.save()
    
    def update_from_interactions(self, db: Session) -> None:
        """Update article classifications based on user interactions"""
        # Get recent interactions
        recent_interactions = db.query(Interaction).filter(
            Interaction.timestamp >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        if not recent_interactions:
            return
        
        # Group interactions by article
        article_interactions: Dict[int, List[Interaction]] = {}
        for interaction in recent_interactions:
            if interaction.article_id not in article_interactions:
                article_interactions[interaction.article_id] = []
            article_interactions[interaction.article_id].append(interaction)
        
        # Update article priorities based on interaction patterns
        for article_id, interactions in article_interactions.items():
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                continue
            
            # Calculate engagement score
            engagement_score = sum(
                2 if i.interaction_type == "save" else
                1 if i.interaction_type == "click" else
                0 for i in interactions
            )
            
            # Update priority if engagement is high
            if engagement_score >= 5 and article.priority != "High":
                article.priority = "High"
                db.add(article)
        
        db.commit()

ml_service = MLService() 