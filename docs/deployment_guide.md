# Deployment Guide

This guide covers deploying the Exoplanet Intelligence System to production.

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL database (Supabase)
- Git

## Environment Setup

### 1. Clone the Repository

```
bash
git clone https://github.com/your-repo/exoplanet-intelligence-system.git
cd exoplanet-intelligence-system
```

### 2. Backend Setup

#### Create Virtual Environment

```
bash
cd backend
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

#### Install Dependencies

```
bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```
bash
cp .env.example .env
```

Edit `.env`:
```
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Model Paths
CLASSIFICATION_MODEL_PATH=models/classification_pipeline.pkl
REGRESSION_MODEL_PATH=models/regression_pipeline.pkl

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# CORS
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
```

### 3. Frontend Setup

```
bash
cd frontend
npm install
```

Configure environment variables:

```bash
# Create .env file
VITE_API_URL=https://your-backend-url.onrender.com/api
```

## Database Setup (Supabase)

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Run Schema

1. Open Supabase SQL Editor
2. Copy and execute contents of `database/schema.sql`
3. (Optional) Run `database/seed_data.sql` for test data

## Local Development

### Run Backend

```
bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Run Frontend

```
bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Production Deployment

### Backend (Render/Railway)

#### Option 1: Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in Render dashboard
7. Deploy

#### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

### Frontend (Vercel)

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Configure:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add environment variable: `VITE_API_URL`
6. Deploy

## Verifying Deployment

### 1. Check Backend Health

```
bash
curl https://your-backend-url.onrender.com/api/health
```

### 2. Test Classification Endpoint

```
bash
curl -X POST https://your-backend-url.onrender.com/api/predict/classification \
  -H "Content-Type: application/json" \
  -d '{"features": {"koi_prad": 2.5, "koi_depth": 150, "koi_period": 45.3}}'
```

### 3. Test Regression Endpoint

```
bash
curl -X POST https://your-backend-url.onrender.com/api/predict/regression \
  -H "Content-Type: application/json" \
  -d '{"features": {"koi_prad": 2.5, "koi_depth": 150, "koi_period": 45.3}}'
```

## Troubleshooting

### Backend Issues

- **Model not loading**: Check that `.pkl` files are in the correct location
- **CORS errors**: Verify CORS_ORIGINS includes your frontend URL
- **Database connection**: Check SUPABASE_URL and SUPABASE_KEY

### Frontend Issues

- **API not connecting**: Verify VITE_API_URL is correct
- **Build errors**: Ensure all dependencies are installed

### Performance Issues

- Consider adding caching with Redis
- Enable Gzip compression on the backend
- Use CDN for static assets

## Security Checklist

- [ ] Environment variables are set in production
- [ ] CORS is configured properly
- [ ] Database has RLS enabled
- [ ] No sensitive data in code
- [ ] HTTPS is enabled (Render/Vercel)

## Monitoring

### Backend Logs

Check Render/Railway dashboard for logs

### Frontend Errors

Configure error tracking with Sentry or similar

## Updates

To update the deployed application:

```
bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
# Backend: Push to GitHub (auto-deploy)
# Frontend: Push to GitHub (auto-deploy)
```

## Support

For deployment issues, please open an issue on GitHub.
