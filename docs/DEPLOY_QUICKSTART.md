# 🚀 Quick Start Deployment Guide

**TL;DR**: Follow these steps to deploy your ATS Resume Analyzer in ~30 minutes.

## Prerequisites Checklist

- [ ] Code pushed to GitHub
- [ ] Render account (sign up at render.com)
- [ ] Vercel account (sign up at vercel.com)

---

## Step 1: Deploy Backend (Render) - ~15 min

1. **Create PostgreSQL Database**
   - Go to Render → New → PostgreSQL
   - Name: `ats-db`
   - Copy the **Internal Database URL**

2. **Run Migrations Locally** (one-time)
   ```bash
   cd backend
   # Update .env with Render database URL
   alembic upgrade head
   ```

3. **Deploy Web Service**
   - Go to Render → New → Web Service
   - Connect GitHub repo
   - Settings:
     - Root Directory: `backend`
     - Build: `pip install -r requirements.txt`
     - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     DATABASE_URL=<your-internal-db-url>
     DEBUG=false
     EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
     ```
   - Deploy!

4. **Get Backend URL**
   - Example: `https://ats-api.onrender.com`
   - Test: `https://your-api.onrender.com/api/v1/health`

---

## Step 2: Deploy Frontend (Vercel) - ~10 min

1. **Import Project**
   - Go to Vercel → Add New Project
   - Select your GitHub repo
   - Root Directory: `frontend`
   - Framework: Next.js (auto-detected)

2. **Set Environment Variable**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```
   (Replace with your actual Render backend URL)

3. **Deploy**
   - Click Deploy
   - Wait ~2-3 minutes
   - Get your frontend URL: `https://your-app.vercel.app`

---

## Step 3: Connect Frontend to Backend - ~5 min

1. **Update Backend CORS**
   - In `backend/app/main.py`, add your Vercel URL to CORS
   - Or set environment variable: `CORS_ORIGINS=https://your-app.vercel.app`
   - Commit and push (Render auto-deploys)

2. **Test Everything**
   - Open your Vercel URL
   - Upload a resume
   - Enter job description
   - Submit and verify it works!

---

## ✅ Done!

Your app is now live! 🎉

**Next Steps:**
- Share your app URL
- Monitor usage in Render/Vercel dashboards
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for post-deployment tasks

**Need Help?**
- See full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Troubleshooting: [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

---

**Estimated Total Time**: 30-45 minutes  
**Cost**: Free tier available on both platforms


