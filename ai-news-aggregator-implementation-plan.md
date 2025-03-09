# AI News Aggregator Implementation Plan

## Project Overview
This plan details the implementation of an ML-powered AI news aggregator that learns from user interactions. It's designed to work with Cursor for code completion and includes all necessary file structures, dependencies, and integration points.

## Tech Stack

### Core Technologies
- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy
- **ML Pipeline**: scikit-learn + PyTorch
- **Containerization**: Docker
- **Deployment**: AWS (or alternative cloud provider)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

### Development Tools
- **Cursor**: For AI-assisted code completion
- **Git**: Version control
- **Poetry**: Python dependency management
- **npm**: JavaScript dependency management
- **DBeaver**: Database management
- **Postman**: API testing

## Project Structure

```
ai-news-aggregator/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── articles.py
│   │   │   │   ├── feeds.py
│   │   │   │   └── ml.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── article.py
│   │   │   ├── feed.py
│   │   │   ├── interaction.py
│   │   │   └── preference.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── article.py
│   │   │   ├── feed.py
│   │   │   └── ml.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── feed_service.py
│   │   │   ├── article_service.py
│   │   │   ├── user_service.py
│   │   │   └── ml_service.py
│   │   └── ml/
│   │       ├── __init__.py
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   ├── relevance_model.py
│   │       │   ├── priority_model.py
│   │       │   └── recommendation_model.py
│   │       ├── features/
│   │       │   ├── __init__.py
│   │       │   ├── text_features.py
│   │       │   ├── user_features.py
│   │       │   └── interaction_features.py
│   │       ├── training/
│   │       │   ├── __init__.py
│   │       │   ├── train_relevance.py
│   │       │   ├── train_priority.py
│   │       │   └── train_recommendation.py
│   │       └── inference/
│   │           ├── __init__.py
│   │           ├── relevance_inference.py
│   │           ├── priority_inference.py
│   │           └── recommendation_inference.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_ml/
│   ├── scripts/
│   │   ├── seed_db.py
│   │   └── train_initial_models.py
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── auth/
│   │   │   ├── articles/
│   │   │   │   ├── ArticleCard.tsx
│   │   │   │   ├── ArticleDetail.tsx
│   │   │   │   ├── ArticleList.tsx
│   │   │   │   └── ArticleFilter.tsx
│   │   │   ├── dashboard/
│   │   │   └── common/
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ArticleDetailPage.tsx
│   │   │   ├── SettingsPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useArticles.ts
│   │   │   ├── useFeeds.ts
│   │   │   └── useAnalytics.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── authService.ts
│   │   │   ├── articleService.ts
│   │   │   └── userService.ts
│   │   ├── store/
│   │   │   ├── index.ts
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.ts
│   │   │   │   ├── articleSlice.ts
│   │   │   │   └── uiSlice.ts
│   │   │   └── hooks.ts
│   │   ├── utils/
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── constants.ts
│   │   └── types/
│   │       ├── article.ts
│   │       ├── user.ts
│   │       └── feed.ts
│   ├── public/
│   ├── .eslintrc.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
├── ml-pipeline/
│   ├── __init__.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── data_extraction.py
│   │   ├── feature_engineering.py
│   │   ├── model_training.py
│   │   └── model_evaluation.py
│   ├── notebooks/
│   │   ├── exploratory_analysis.ipynb
│   │   ├── feature_importance.ipynb
│   │   └── model_comparison.ipynb
│   ├── scripts/
│   │   ├── run_daily_training.py
│   │   └── export_models.py
│   └── Dockerfile
├── infra/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── scripts/
│   ├── setup.sh
│   ├── run-dev.sh
│   └── deploy.sh
├── .env.example
├── README.md
└── LICENSE
```

## Core Components Implementation

### 1. Feed Collection Service (`backend/app/services/feed_service.py`)

```python
# This service handles RSS feed collection and processing
import feedparser
from datetime import datetime
from app.models.feed import Feed
from app.models.article import Article
from app.db.session import get_db
from app.services.ml_service import classify_article

class FeedService:
    def __init__(self, db=None):
        self.db = db or next(get_db())
    
    def fetch_all_feeds(self):
        """Fetch all active feeds and process new articles"""
        feeds = self.db.query(Feed).filter(Feed.is_active == True).all()
        for feed in feeds:
            self._process_feed(feed)
    
    def _process_feed(self, feed):
        """Process a single feed and extract articles"""
        parsed = feedparser.parse(feed.url)
        for entry in parsed.entries:
            # Check if article already exists
            existing = self.db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue
                
            # Create new article
            article = Article(
                title=entry.title,
                url=entry.link,
                source=feed.name,
                summary=entry.summary if hasattr(entry, 'summary') else '',
                date_published=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z') 
                if hasattr(entry, 'published') else datetime.now(),
                date_found=datetime.now()
            )
            
            # Initial ML classification
            classification = classify_article(article.title, article.summary)
            article.category = classification['category']
            article.priority = classification['priority']
            article.key_points = classification['key_points']
            
            self.db.add(article)
            self.db.commit()
```

### 2. ML Service (`backend/app/services/ml_service.py`)

```python
# This service coordinates ML model inference and training
import pickle
from pathlib import Path
import numpy as np
from app.ml.features.text_features import extract_text_features
from app.ml.models.relevance_model import RelevanceModel
from app.ml.models.priority_model import PriorityModel
from app.ml.models.recommendation_model import RecommendationModel

MODEL_DIR = Path(__file__).parent.parent / "ml" / "saved_models"

class MLService:
    def __init__(self):
        self.relevance_model = self._load_model("relevance_model.pkl")
        self.priority_model = self._load_model("priority_model.pkl")
        self.recommendation_model = self._load_model("recommendation_model.pkl")
    
    def _load_model(self, filename):
        """Load a pickled model file"""
        model_path = MODEL_DIR / filename
        if model_path.exists():
            with open(model_path, "rb") as f:
                return pickle.load(f)
        return None
    
    def classify_article(self, title, content):
        """Classify an article using the ML models"""
        features = extract_text_features(title, content)
        
        # Default classification if models aren't trained yet
        if self.relevance_model is None:
            return {
                "category": "Research",
                "priority": "Low",
                "key_points": ["Initial classification", "Model not trained", "Default values"]
            }
        
        relevance_score = self.relevance_model.predict_proba([features])[0][1]
        
        if relevance_score < 0.5:
            return {
                "category": "Not Relevant",
                "priority": "Low",
                "key_points": ["Low relevance score", "Automatic classification", f"Score: {relevance_score:.2f}"]
            }
        
        # For relevant articles, determine category and priority
        category_probs = self.category_model.predict_proba([features])[0]
        categories = ["Models/Agents", "Tools", "Research", "Industry"]
        category = categories[np.argmax(category_probs)]
        
        priority_score = self.priority_model.predict_proba([features])[0][1]
        priority = "High" if priority_score > 0.7 else "Low"
        
        return {
            "category": category,
            "priority": priority,
            "key_points": ["Automated extraction", f"Relevance: {relevance_score:.2f}", f"Priority: {priority_score:.2f}"]
        }
    
    def update_from_feedback(self, article_id, user_id, feedback_data):
        """Update models based on user feedback"""
        # Implementation for handling feedback and retraining
        pass

ml_service = MLService()
classify_article = ml_service.classify_article
```

### 3. React Frontend Article Component (`frontend/src/components/articles/ArticleCard.tsx`)

```typescript
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { Card, Badge, Button, Stack, Text } from '@your-ui-library/react';
import { Article } from '../../types/article';
import { trackInteraction } from '../../store/slices/articleSlice';
import { formatDate } from '../../utils/formatters';

interface ArticleCardProps {
  article: Article;
  compact?: boolean;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, compact = false }) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const handleClick = () => {
    // Track user interaction
    dispatch(trackInteraction({
      articleId: article.id,
      interactionType: 'click',
      timestamp: new Date().toISOString()
    }));
    
    navigate(`/articles/${article.id}`);
  };
  
  const handleSave = (e: React.MouseEvent) => {
    e.stopPropagation();
    dispatch(trackInteraction({
      articleId: article.id,
      interactionType: 'save',
      timestamp: new Date().toISOString()
    }));
  };
  
  return (
    <Card 
      onClick={handleClick}
      elevation={article.priority === 'High' ? 3 : 1}
      className={`article-card ${article.priority.toLowerCase()}-priority`}
    >
      <Stack spacing={2}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Badge color={article.category === 'Models/Agents' ? 'blue' : 
                        article.category === 'Tools' ? 'green' :
                        article.category === 'Research' ? 'purple' : 'orange'}>
            {article.category}
          </Badge>
          <Badge color={article.priority === 'High' ? 'red' : 'gray'}>
            {article.priority}
          </Badge>
        </Stack>
        
        <Text variant="h3">{article.title}</Text>
        
        {!compact && (
          <Text variant="body2" color="textSecondary">
            {article.summary.substring(0, 120)}...
          </Text>
        )}
        
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Text variant="caption">{article.source} • {formatDate(article.date_found)}</Text>
          <Button 
            variant="outlined" 
            size="small" 
            onClick={handleSave}
            startIcon={<BookmarkIcon />}
          >
            Save
          </Button>
        </Stack>
      </Stack>
    </Card>
  );
};

export default ArticleCard;
```

### 4. User Interaction Tracking (`backend/app/api/routes/ml.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.interaction import Interaction
from app.schemas.ml import InteractionCreate
from app.services.ml_service import ml_service
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/interactions")
def track_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Track a user interaction with an article"""
    db_interaction = Interaction(
        user_id=current_user.id,
        article_id=interaction.article_id,
        interaction_type=interaction.interaction_type,
        timestamp=interaction.timestamp,
        additional_data=interaction.additional_data
    )
    db.add(db_interaction)
    db.commit()
    
    # Trigger ML update if enough new interactions
    interaction_count = db.query(Interaction).count()
    if interaction_count % 50 == 0:  # Update models every 50 interactions
        # This would be better as a background task
        ml_service.update_models(db)
    
    return {"status": "success"}

@router.post("/feedback/{article_id}")
def provide_feedback(
    article_id: int,
    feedback_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Provide explicit feedback on article classification"""
    ml_service.update_from_feedback(article_id, current_user.id, feedback_data)
    return {"status": "feedback recorded"}
```

## ML Pipeline Implementation

### 1. Relevance Model (`backend/app/ml/models/relevance_model.py`)

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class RelevanceModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
    
    def train(self, X, y):
        """Train the relevance model"""
        self.model.fit(X, y)
        self.is_trained = True
        return self
    
    def predict(self, X):
        """Predict relevance (binary)"""
        if not self.is_trained:
            return np.ones(len(X))  # Default to relevant if not trained
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Predict relevance probability"""
        if not self.is_trained:
            return np.ones((len(X), 2))  # Default probabilities if not trained
        return self.model.predict_proba(X)
```

## Integration with External APIs

### 1. DeepSeek API Integration (`backend/app/services/article_service.py`)

```python
import requests
import os
import json
from app.models.article import Article

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def enrich_article_with_ai(article):
    """Enrich article with AI analysis using DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analyze this AI technology news:
    Title: {article.title}
    Content: {article.summary}
    
    Provide:
    1. Category (choose one: Models/Agents, Tools, Research, Industry)
    2. Priority (High or Low based on impact to AI professionals)
    3. Three key points as bullet points
    4. Suggested action items for AI professionals
    
    Format as JSON.
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an AI news analyst focusing on analyzing and categorizing AI-related content."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        ai_analysis = json.loads(result["choices"][0]["message"]["content"])
        
        return {
            "category": ai_analysis.get("category", "Uncategorized"),
            "priority": ai_analysis.get("priority", "Low"),
            "key_points": ai_analysis.get("key_points", []),
            "action_items": ai_analysis.get("action_items", [])
        }
    except Exception as e:
        print(f"Error enriching article with AI: {e}")
        return {
            "category": "Uncategorized",
            "priority": "Low",
            "key_points": ["Error in AI analysis"],
            "action_items": ["Review manually"]
        }
```

## Database Models

### 1. Article Model (`backend/app/models/article.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

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
    date_found = Column(DateTime, default=datetime.now)
    is_archived = Column(Boolean, default=False)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="article")
```

### 2. User Interaction Model (`backend/app/models/interaction.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    interaction_type = Column(String)  # click, save, dismiss, share
    timestamp = Column(DateTime, default=datetime.now)
    additional_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    article = relationship("Article", back_populates="interactions")
```

## Setup and Deployment

### Environment Setup (`scripts/setup.sh`)

```bash
#!/bin/bash
# Setup script for AI News Aggregator

# Check requirements
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }
command -v poetry >/dev/null 2>&1 || { echo "Poetry is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "NPM is required but not installed. Aborting." >&2; exit 1; }

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from example. Please edit with your configurations."
fi

# Install backend dependencies
cd backend
poetry install
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..

# Build Docker containers
docker-compose build

echo "Setup complete! To start the development environment, run: ./scripts/run-dev.sh"
```

### Development Environment (`scripts/run-dev.sh`)

```bash
#!/bin/bash
# Start development environment

# Start Docker services
docker-compose up -d

# Start backend
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Handle shutdown
function cleanup {
    echo "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID
    docker-compose down
}

trap cleanup EXIT

# Wait for user to exit
echo "Development environment running. Press Ctrl+C to stop."
wait
```

## Integrating with Cursor

To best leverage Cursor with this project:

1. **Repository Setup**:
   - Initialize Git: `git init`
   - Make initial commit with structure: `git add . && git commit -m "Initial project structure"`

2. **Cursor Configuration**:
   - Create a `.cursor` folder in the project root
   - Add a `settings.json` file with AI completion settings

3. **Using Cursor Effectively**:
   - Start with skeleton files and let Cursor fill in implementations
   - Use `/explain` for understanding complex code sections
   - Use `/generate` for creating new components based on project patterns

## Connecting Components

### Database Connection
In `backend/app/db/session.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/ai_news")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### API Connection
In `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
```

## Implementation Timeline

### Phase 1: Core Structure (Week 1-2)
- Project setup
- Database models
- Basic API endpoints
- Frontend scaffolding

### Phase 2: RSS Feed Integration (Week 3)
- Feed service
- Content fetching
- Initial processing

### Phase 3: ML Pipeline (Week 4-5)
- Feature engineering
- Initial models
- Training pipeline

### Phase 4: User Interface (Week 6-7)
- Dashboard
- Article views
- User preferences

### Phase 5: Feedback Loop (Week 8)
- Interaction tracking
- Model retraining
- Personalization

### Phase 6: Testing & Deployment (Week 9-10)
- Testing
- CI/CD
- Production deployment
