# 🚀 Deployment Guide

Complete guide for deploying the ATS Resume Analyzer to production.

## 📋 Prerequisites

- GitHub account with repository pushed
- Render account (for backend)
- Vercel account (for frontend)
- PostgreSQL database (provided by Render)

---

## 🔧 Part 1: Backend Deployment (Render)

### Step 1: Prepare GitHub Repository

1. Ensure all code is committed and pushed to GitHub:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended for easy repo connection)
3. Verify your email

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `ats-db`
   - **Database**: `ats_db`
   - **User**: `ats_user`
   - **Region**: Choose closest to your users
   - **Plan**: Starter (free tier available)
3. Click **"Create Database"**
4. **Important**: Copy the **Internal Database URL** (you'll need this)

### Step 4: Run Database Migrations

1. Get the database connection string from Render dashboard
2. Locally, update your `.env` with the Render database URL
3. Run migrations:
   ```bash
   cd backend
   source venv/bin/activate
   alembic upgrade head
   ```

### Step 5: Deploy Backend Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `ats-resume-analyzer-api`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 6: Configure Environment Variables

In Render dashboard, go to **Environment** tab and add:

```env
DATABASE_URL=<Internal Database URL from Step 3>
DEBUG=false
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
MODEL_CACHE_DIR=./model_cache
MAX_UPLOAD_SIZE=10485760
PYTHON_VERSION=3.10
PYTHONUNBUFFERED=1
```

**Important Notes:**
- Use the **Internal Database URL** (not external) for better performance
- The `$PORT` variable is automatically provided by Render
- First deployment may take 5-10 minutes (model download)

### Step 7: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (first time: ~5-10 minutes)
3. Once deployed, you'll get a URL like: `https://ats-resume-analyzer-api.onrender.com`
4. Test the health endpoint: `https://your-app.onrender.com/api/v1/health`

### Step 8: Update CORS Settings

1. In `backend/app/main.py`, update CORS origins:
   ```python
   allow_origins=[
       "http://localhost:3000",  # Keep for local dev
       "https://your-frontend.vercel.app",  # Add your Vercel URL
   ],
   ```

2. Commit and push changes:
   ```bash
   git add backend/app/main.py
   git commit -m "Update CORS for production"
   git push
   ```

3. Render will auto-deploy the changes

---

## 🎨 Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Ensure `frontend/.env.local` is in `.gitignore` (should be already)
2. Create `frontend/.env.production` (optional, or use Vercel env vars)

### Step 2: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub (recommended)
3. Import your GitHub repository

### Step 3: Configure Project

1. In Vercel dashboard, click **"Add New Project"**
2. Select your repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

### Step 4: Set Environment Variables

In Vercel dashboard, go to **Settings** → **Environment Variables**:

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

**Important:**
- Replace `your-backend.onrender.com` with your actual Render backend URL
- The `NEXT_PUBLIC_` prefix is required for Next.js client-side access

### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build (~2-3 minutes)
3. Once deployed, you'll get a URL like: `https://ats-resume-analyzer.vercel.app`
4. Test the application

### Step 6: Update Backend CORS (if not done)

1. Update backend CORS with your Vercel URL
2. Redeploy backend

---

## ✅ Post-Deployment Checklist

### Backend Verification

- [ ] Health endpoint works: `https://your-api.onrender.com/api/v1/health`
- [ ] ML model loaded (check health response: `ml_model_loaded: true`)
- [ ] Database connection working
- [ ] API docs accessible: `https://your-api.onrender.com/docs`
- [ ] CORS configured correctly

### Frontend Verification

- [ ] Frontend loads without errors
- [ ] Can upload resume file
- [ ] Can submit job description
- [ ] Analysis completes successfully
- [ ] Report page displays correctly
- [ ] All API calls work

### Integration Testing

- [ ] End-to-end flow works (upload → analyze → view report)
- [ ] Error handling works (test with invalid file)
- [ ] Loading states display correctly
- [ ] Mobile responsive design works

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Deployment fails
- **Solution**: Check build logs in Render dashboard
- Check Python version compatibility
- Ensure all dependencies are in `requirements.txt`

**Problem**: Database connection fails
- **Solution**: Verify `DATABASE_URL` is correct
- Use Internal Database URL (not external)
- Check database is running in Render dashboard

**Problem**: ML model not loading
- **Solution**: First deployment takes longer (model download)
- Check `MODEL_CACHE_DIR` is writable
- Increase deployment timeout if needed

**Problem**: CORS errors
- **Solution**: Update CORS origins in `app/main.py`
- Include both localhost (dev) and Vercel URL (prod)
- Redeploy after changes

### Frontend Issues

**Problem**: API calls fail
- **Solution**: Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running
- Check CORS configuration

**Problem**: Build fails
- **Solution**: Check build logs in Vercel
- Ensure all dependencies are in `package.json`
- Check Node.js version compatibility

**Problem**: Environment variables not working
- **Solution**: Ensure `NEXT_PUBLIC_` prefix for client-side vars
- Redeploy after adding env vars
- Check Vercel environment variable settings

---

## 📊 Monitoring

### Render Monitoring

- View logs: Render dashboard → Your service → Logs
- Monitor metrics: CPU, Memory, Response times
- Set up alerts for downtime

### Vercel Monitoring

- View logs: Vercel dashboard → Your project → Logs
- Monitor analytics: Vercel Analytics (if enabled)
- Check build status

---

## 🔄 Updating Deployment

### Backend Updates

1. Make changes locally
2. Test locally
3. Commit and push to GitHub
4. Render auto-deploys (or manually trigger)
5. Monitor deployment logs

### Frontend Updates

1. Make changes locally
2. Test locally
3. Commit and push to GitHub
4. Vercel auto-deploys
5. Monitor build logs

---

## 💰 Cost Estimation

### Render (Backend + Database)

- **Free Tier**: 
  - Web service: Free (spins down after 15 min inactivity)
  - PostgreSQL: Free (limited to 90 days)
- **Starter Plan**: $7/month (always-on web service)
- **Standard Plan**: $25/month (better performance)

### Vercel (Frontend)

- **Free Tier**: Unlimited (with limitations)
- **Pro Plan**: $20/month (for production use)

**Total Estimated Cost:**
- **Free Tier**: $0/month (with limitations)
- **Production**: ~$27-45/month

---

## 🎯 Next Steps After Deployment

1. **Set up custom domains** (optional)
2. **Enable analytics** (Vercel Analytics, Google Analytics)
3. **Set up monitoring** (Sentry for error tracking)
4. **Configure backups** (database backups on Render)
5. **Add SSL certificates** (automatic on both platforms)
6. **Set up CI/CD** (already configured via GitHub)

---

## 📝 Notes

- Render free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- Consider upgrading to paid plans for production use
- Database backups are important - configure in Render
- Monitor usage to avoid unexpected costs

---

**Last Updated**: 2025-12-06  
**Status**: Ready for deployment


