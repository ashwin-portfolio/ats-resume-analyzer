# 🚀 Quick Start Guide

## Run in 3 Steps (Windows)

### 1️⃣ Navigate to backend folder
```bash
cd backend
```

### 2️⃣ Run the start script
```bash
start.bat
```

### 3️⃣ Open your browser
```
http://localhost:8000/docs
```

That's it! The API is running! 🎉

---

## Test the API

### Option 1: Browser (Interactive)
Visit: http://localhost:8000/docs

Try the `/health` endpoint:
1. Click on "GET /api/v1/health"
2. Click "Try it out"
3. Click "Execute"

### Option 2: cURL (Command Line)
```bash
curl http://localhost:8000/api/v1/health
```

### Option 3: Test Script (Automated)
```bash
pip install requests
python test_api.py
```

---

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/analyze` | Analyze resume (mock) |
| GET | `/api/v1/report/{id}` | Get report |
| GET | `/api/v1/reports` | List reports |

---

## Test Resume Upload

### Using the Interactive Docs (http://localhost:8000/docs):

1. Navigate to `POST /api/v1/analyze`
2. Click "Try it out"
3. Upload any PDF/DOCX file
4. Paste a job description
5. Click "Execute"
6. See the ATS analysis results!

### Using cURL:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "resume_file=@your_resume.pdf" \
  -F "job_description=Looking for Python developer with FastAPI experience"
```

---

## What's Working Now?

✅ FastAPI server running  
✅ All endpoints respond  
✅ File upload handling  
✅ Mock ATS analysis  
✅ API documentation  
✅ CORS enabled  

## What's Next?

The backend returns **mock data** right now. To make it real:

1. **ML Pipeline** - Add real resume analysis
2. **Database** - Save reports to PostgreSQL
3. **Frontend** - Build the UI with Next.js

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
Edit `app/main.py` and change:
```python
port=8000  # Change to 8001 or any free port
```

### "Cannot import app.api.routes"
Make sure you're running from the correct directory:
```bash
cd backend/app
python main.py
```

---

## 📚 More Info

- **Full Setup Guide:** `SETUP.md`
- **Structure Overview:** `../docs/BACKEND_STRUCTURE.md`
- **Progress Tracker:** `../docs/PROGRESS.md`

---

**Questions?** Check the docs or run:
```bash
python main.py --help
```

