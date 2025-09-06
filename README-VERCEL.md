# Vercel Deployment Guide

This FastAPI restaurant finder app is configured for deployment on Vercel.

## Files Created/Modified for Vercel:

1. **`vercel.json`** - Vercel configuration file
2. **`api/index.py`** - Serverless function entry point with Mangum ASGI adapter
3. **`requirements.txt`** - Updated dependencies (added mangum, removed uvicorn, gunicorn)
4. **`templates/index.html`** - Updated to use relative URLs
5. **`.vercelignore`** - Excludes unnecessary files from deployment
6. **`main.py`** - Removed (replaced by api/index.py)

## Deployment Steps:

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from project directory
```bash
cd restaurant-Project
vercel
```

### 4. Set Environment Variables
In your Vercel dashboard:
- Go to your project settings
- Navigate to Environment Variables
- Add: `GOOGLE_API_KEY` with your Google Places API key

### 5. Redeploy
After setting environment variables:
```bash
vercel --prod
```

## Project Structure:
```
restaurant-Project/
├── api/
│   └── index.py          # Vercel serverless function
├── templates/
│   └── index.html        # Frontend template
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── .vercelignore        # Files to ignore
└── README-VERCEL.md     # This file
```

## Environment Variables Required:
- `GOOGLE_API_KEY`: Your Google Places API key

## Notes:
- The app will be available at your Vercel domain
- All routes are handled by the FastAPI app in `api/index.py`
- Static files (templates) are served by Vercel
- CORS is configured to allow all origins for development
