from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.article import Article, ArticleCreate, ArticleUpdate, ArticleWithInteractions
from app.models.article import Article as ArticleModel
from app.db.session import get_db
from sqlalchemy import func
from app.models.interaction import Interaction

router = APIRouter()

@router.post("/", response_model=Article)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(ArticleModel).filter(ArticleModel.url == str(article.url)).first()
    if db_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with this URL already exists"
        )
    
    db_article = ArticleModel(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/", response_model=List[ArticleWithInteractions])
def read_articles(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        ArticleModel,
        func.count(Interaction.id).label('interaction_count'),
        func.sum(func.case([(Interaction.interaction_type == 'save', 1)], else_=0)).label('save_count'),
        func.sum(func.case([(Interaction.interaction_type == 'click', 1)], else_=0)).label('click_count')
    ).outerjoin(Interaction)
    
    if category:
        query = query.filter(ArticleModel.category == category)
    if priority:
        query = query.filter(ArticleModel.priority == priority)
    
    articles = query.group_by(ArticleModel.id).order_by(ArticleModel.date_found.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            **article[0].__dict__,
            'interaction_count': article[1] or 0,
            'save_count': article[2] or 0,
            'click_count': article[3] or 0
        }
        for article in articles
    ]

@router.get("/{article_id}", response_model=ArticleWithInteractions)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(
        ArticleModel,
        func.count(Interaction.id).label('interaction_count'),
        func.sum(func.case([(Interaction.interaction_type == 'save', 1)], else_=0)).label('save_count'),
        func.sum(func.case([(Interaction.interaction_type == 'click', 1)], else_=0)).label('click_count')
    ).outerjoin(Interaction).filter(ArticleModel.id == article_id).group_by(ArticleModel.id).first()
    
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return {
        **article[0].__dict__,
        'interaction_count': article[1] or 0,
        'save_count': article[2] or 0,
        'click_count': article[3] or 0
    }

@router.put("/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if db_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    update_data = article.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}", response_model=Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if db_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    db.delete(db_article)
    db.commit()
    return db_article 