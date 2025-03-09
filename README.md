# AI News Aggregator

An ML-powered news aggregator that learns from user interactions to provide personalized AI-related news content.

## Features

- RSS feed aggregation and processing
- ML-based article categorization and prioritization
- User interaction tracking and personalization
- RESTful API with FastAPI
- React + TypeScript frontend
- PostgreSQL database with SQLAlchemy ORM

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=ai_news
   ```

4. Initialize the database:
   ```bash
   alembic upgrade head
   ```

5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Create a `.env` file:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. Run the frontend:
   ```bash
   npm run dev
   ```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 