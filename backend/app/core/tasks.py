from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.feed_service import FeedService
from app.services.ml_service import ml_service
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

async def periodic_feed_updates():
    """Periodically update all active feeds"""
    while True:
        try:
            db = SessionLocal()
            feed_service = FeedService(db)
            feed_service.fetch_all_feeds()
            logger.info("Completed periodic feed update")
        except Exception as e:
            logger.error(f"Error in periodic feed update: {e}")
        finally:
            db.close()
        
        # Wait for 1 hour before next update
        await asyncio.sleep(3600)

async def periodic_model_training():
    """Periodically retrain the ML model based on recent interactions"""
    while True:
        try:
            db = SessionLocal()
            # Update model based on interactions
            ml_service.update_from_interactions(db)
            # Retrain model with all data
            ml_service.train_model(db)
            logger.info("Completed periodic model training")
        except Exception as e:
            logger.error(f"Error in periodic model training: {e}")
        finally:
            db.close()
        
        # Wait for 24 hours before next training
        await asyncio.sleep(86400)

def start_background_tasks(background_tasks: BackgroundTasks):
    """Start all background tasks"""
    background_tasks.add_task(periodic_feed_updates)
    background_tasks.add_task(periodic_model_training) 