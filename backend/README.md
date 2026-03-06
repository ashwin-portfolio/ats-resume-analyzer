# 🚀 ATS Resume Analyzer - Backend API

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**Production-Ready REST API | ML-Powered Analysis | Enterprise-Grade Security**

[Quick Start](#-quick-start) • [API Documentation](#-api-endpoints) • [Architecture](#-architecture) • [Deployment](#-deployment)

</div>

---

## 📋 Overview

High-performance **FastAPI** backend providing RESTful API endpoints for AI-powered resume analysis. Features include ML-based semantic similarity matching, comprehensive security measures, database persistence, and production-ready error handling.

**Key Features:**
- ✅ **FastAPI** - High-performance async web framework
- ✅ **ML Pipeline** - SentenceTransformers for semantic analysis (local, no API costs)
- ✅ **PostgreSQL** - Reliable database with SQLModel ORM
- ✅ **Security** - Rate limiting, input validation, security headers
- ✅ **Production-Ready** - Structured logging, health checks, error handling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  API Layer (routes.py)                            │  │
│  │  • Request Validation (Pydantic)                  │  │
│  │  • Rate Limiting                                  │  │
│  │  • Error Handling                                 │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Business Logic Layer                              │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │ ML Pipeline (ml/)                            │ │  │
│  │  │ • Embeddings (SentenceTransformers)          │ │  │
│  │  │ • Analyzer (Hybrid scoring algorithm)        │ │  │
│  │  │ • Keyword Extractor (TF-IDF)                 │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │ File Parser (utils/)                        │ │  │
│  │  │ • PDF/DOCX extraction                        │ │  │
│  │  │ • Magic bytes validation                    │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Data Layer (models/)                             │  │
│  │  • SQLModel ORM                                   │  │
│  │  • Database connection pooling                    │  │
│  │  • Alembic migrations                             │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼───────────────────────────────────────┘
                   │
                   ▼
            ┌──────────────┐
            │  PostgreSQL  │
            │   Database   │
            └──────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.104+ | High-performance async web framework |
| **Database** | PostgreSQL | 15+ | Relational database |
| **ORM** | SQLModel | 0.0.14 | Type-safe ORM (SQLAlchemy + Pydantic) |
| **ML Library** | SentenceTransformers | 2.3+ | Semantic embeddings (local) |
| **Migrations** | Alembic | 1.12+ | Database schema versioning |
| **Server** | Uvicorn | 0.24+ | ASGI server |
| **Validation** | Pydantic | 2.5+ | Data validation and serialization |
| **Rate Limiting** | slowapi | 0.1.9 | API rate limiting |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10 or higher
- **PostgreSQL** 12+ (or use Docker)
- **pip** package manager

### Installation

```bash
# Clone repository
git clone https://github.com/ashwin-portfolio/ats-resume-analyzer.git
cd ats-resume-analyzer/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required variables:
# DATABASE_URL=postgresql://user:password@localhost:5432/ats_db
# DEBUG=false (for production)
```

### Database Setup

```bash
# Run migrations
alembic upgrade head

# Verify database connection
python -c "from app.models.database import check_db_connection; check_db_connection()"
```

### Run Development Server

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python module
python -m app.main

# Option 3: Using start script
./start.sh  # Linux/Mac
start.bat   # Windows
```

**API will be available at:** `http://localhost:8000`  
**Interactive API Docs:** `http://localhost:8000/docs`  
**ReDoc Documentation:** `http://localhost:8000/redoc`

---

## 📚 API Endpoints

### Health Check

```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "ATS Resume Analyzer",
  "ml_model_loaded": true,
  "database_connected": true
}
```

### Analyze Resume

```http
POST /api/v1/analyze
Content-Type: multipart/form-data
```

**Request:**
- `resume_file` (file, required): PDF or DOCX file (max 10MB)
- `job_description` (string, required): Job description text (min 10 chars, max 50KB)

**Response:**
```json
{
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "ats_score": 75.5,
  "skill_match_percentage": 68.3,
  "matched_keywords": [...],
  "missing_keywords": [...],
  "summary": "...",
  "recommendations": [...],
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Get Report

```http
GET /api/v1/report/{report_id}
```

### List Reports

```http
GET /api/v1/reports?page=1&limit=20
```

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 10, max: 100)

---

## 🔒 Security Features

### Rate Limiting
- **Analysis endpoint**: 10 requests/minute per IP
- **Default endpoints**: 100 requests/minute per IP
- **Health endpoint**: Not rate limited (monitoring)

### Input Validation
- ✅ File type validation (extension + magic bytes)
- ✅ File size limits (10MB maximum)
- ✅ Job description length limits (50KB maximum)
- ✅ Filename sanitization (path traversal prevention)
- ✅ Report ID validation (regex pattern)

### Security Headers
- `Content-Security-Policy` - XSS protection
- `X-Frame-Options: DENY` - Clickjacking protection
- `X-Content-Type-Options: nosniff` - MIME sniffing protection
- `Strict-Transport-Security` - HTTPS enforcement
- `Referrer-Policy` - Referrer information control

### Database Security
- ✅ Parameterized queries (SQL injection prevention)
- ✅ Connection timeouts (10 seconds)
- ✅ Query timeouts (30 seconds)
- ✅ Connection pooling (optimized for production)

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API route handlers
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── schemas.py          # Pydantic request/response models
│   │   ├── middleware.py       # Security headers middleware
│   │   └── rate_limit.py       # Rate limiting configuration
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # SentenceTransformer model loading
│   │   ├── analyzer.py        # Main analysis logic
│   │   └── keyword_extractor.py # TF-IDF keyword extraction
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py         # Database connection & session
│   │   ├── ats_report.py       # ATS Report model
│   │   └── keyword.py          # Keyword model
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_parser.py     # PDF/DOCX text extraction
│       └── text_cleaner.py    # Text preprocessing utilities
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   └── env.py                  # Alembic configuration
│
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic settings
├── .env.example                # Environment template
├── start.sh                    # Quick start script (Unix)
├── start.bat                   # Quick start script (Windows)
└── README.md                   # This file
```

---

## 🧪 Testing

Tests are in **`tests/`** inside the backend. Run from the backend directory with venv activated.

```bash
cd backend
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Start backend server in another terminal, then:
python tests/test_all_phases.py    # Phases 1–4: skeleton, DB, ML, frontend integration
python tests/test_edge_cases.py    # Edge cases: file upload, job description, network

# Database CRUD tests (uses .env DB; no server needed)
python tests/test_database.py

# Health check
curl http://localhost:8000/api/v1/health
```

See **[tests/README.md](tests/README.md)** for full instructions.

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t ats-backend .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e DEBUG=false \
  ats-backend
```

### Docker Compose (Example)

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ats_db
      - DEBUG=false
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=ats_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```

---

## 🚢 Production Deployment

### Environment Variables

```env
# Required
DATABASE_URL=postgresql://user:password@host:5432/database
DEBUG=false

# Optional
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
MODEL_CACHE_DIR=./model_cache
MAX_UPLOAD_SIZE=10485760
CORS_ORIGINS=https://your-frontend.vercel.app
RATE_LIMIT_ENABLED=true
RATE_LIMIT_ANALYZE=10/minute
RATE_LIMIT_DEFAULT=100/minute
```

### Render Deployment

1. Connect GitHub repository
2. Select "Web Service"
3. **Root Directory**: `backend`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`
6. Set environment variables in dashboard

### Performance Optimization

```bash
# Production server with multiple workers
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --no-access-log
```

---

## 📊 Performance Metrics

| Metric | Target | Status |
|--------|--------|--------|
| **API Response Time** | < 2s | ✅ Achieved |
| **Database Query Time** | < 100ms | ✅ Achieved |
| **File Upload Processing** | < 5s | ✅ Achieved |
| **ML Model Loading** | < 30s (first time) | ✅ Achieved |
| **Concurrent Requests** | 100+ | ✅ Supported |

---

## 🔧 Development

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/ --ignore-missing-imports
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Logging

Structured logging with request ID tracking:
- **DEBUG**: Detailed information (development only)
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error messages with stack traces

---

## 📖 Documentation

- **API Documentation**: Available at `/docs` (Swagger UI) and `/redoc`
- **Main Project README**: [../README.md](../README.md)
- **Deployment Guide**: [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)
- **Production Improvements**: [../docs/PRODUCTION_IMPROVEMENTS.md](../docs/PRODUCTION_IMPROVEMENTS.md)

---

## 🎓 Technical Highlights

- ✅ **Async/Await** - Non-blocking I/O for better performance
- ✅ **Type Safety** - Full type hints with Pydantic and SQLModel
- ✅ **Dependency Injection** - FastAPI's dependency system
- ✅ **Request Validation** - Automatic validation with Pydantic
- ✅ **Error Handling** - Comprehensive exception handling
- ✅ **Structured Logging** - Request ID tracking for debugging
- ✅ **Health Checks** - Database and ML model status monitoring

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

<div align="center">

**Part of the [ATS Resume Analyzer](../README.md) project**

*Built with ❤️ using FastAPI and modern Python best practices*</div>
