from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, articles, feeds, auth
from app.core.tasks import start_background_tasks
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="AI News Aggregator",
    description="""
    An ML-powered news aggregator that learns from user interactions to provide personalized AI-related news content.
    
    Features:
    * Automated RSS feed aggregation
    * ML-based article categorization
    * User interaction tracking
    * Personalized content prioritization
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(feeds.router, prefix="/feeds", tags=["Feeds"])

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    background_tasks = BackgroundTasks()
    start_background_tasks(background_tasks)

@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to AI News Aggregator",
        "docs": "/docs",
        "redoc": "/redoc"
    } 