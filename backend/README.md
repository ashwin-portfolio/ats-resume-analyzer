# ATS Resume Analyzer - Backend

FastAPI-based backend for AI-powered Resume ATS analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- pip

### Installation

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run the server:**
```bash
cd app
python main.py
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📚 API Endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `POST /api/v1/analyze` - Analyze resume
- `GET /api/v1/report/{report_id}` - Get report by ID
- `GET /api/v1/reports` - List all reports

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── routes.py        # API routes
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── schemas.py       # Pydantic schemas
│   ├── ml/
│   │   ├── embeddings.py    # ML model loading
│   │   └── analyzer.py      # Analysis logic
│   ├── models/
│   │   └── database.py      # SQLAlchemy models
│   └── utils/
│       └── file_parser.py   # File parsing utilities
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Development

The backend uses:
- **FastAPI** for REST API
- **SentenceTransformers** for embeddings (local, no API calls)
- **PostgreSQL** for data persistence
- **SQLModel** for ORM

## 🐳 Docker Deployment

```bash
docker build -t ats-backend .
docker run -p 8000:8000 ats-backend
```

## 🚢 Deploy to Render

1. Connect GitHub repository
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

