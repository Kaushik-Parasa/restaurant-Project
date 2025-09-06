# GCP Cloud Run Deployment Guide

This FastAPI restaurant finder app is configured for deployment on Google Cloud Platform using Cloud Run.

## Files Created for GCP:

1. **`Dockerfile`** - Container configuration for Cloud Run
2. **`main.py`** - Restored original FastAPI app (removed Vercel-specific code)
3. **`requirements.txt`** - Updated for GCP deployment
4. **`.gcloudignore`** - Excludes unnecessary files from deployment
5. **`deploy-gcp.sh`** - Automated deployment script

## Prerequisites:

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK** installed locally
3. **Google Places API Key**

## Quick Deployment:

### 1. Install Google Cloud SDK
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Or use package manager:
# Windows: choco install gcloudsdk
# macOS: brew install google-cloud-sdk
# Linux: curl https://sdk.cloud.google.com | bash
```

### 2. Authenticate and Set Project
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Set Environment Variable
```bash
export GOOGLE_API_KEY="your_google_places_api_key_here"
```

### 4. Deploy (Option A - Automated)
```bash
# Make script executable
chmod +x deploy-gcp.sh

# Edit deploy-gcp.sh and set your PROJECT_ID
# Then run:
./deploy-gcp.sh
```

### 4. Deploy (Option B - Manual)
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Deploy to Cloud Run
gcloud run deploy restaurant-finder \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

## Project Structure:
```
restaurant-Project/
├── main.py              # FastAPI application
├── templates/
│   └── index.html       # Frontend template
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── .gcloudignore       # Files to ignore
├── deploy-gcp.sh       # Deployment script
└── README-GCP.md       # This file
```

## Environment Variables:
- `GOOGLE_API_KEY`: Your Google Places API key

## Benefits of GCP Cloud Run:
- ✅ **Simple deployment** - Just run one command
- ✅ **Automatic scaling** - Scales to zero when not used
- ✅ **Pay per use** - Only pay when requests are made
- ✅ **No server management** - Fully managed service
- ✅ **Custom domains** - Easy to add your own domain
- ✅ **Built-in monitoring** - Cloud Logging and Monitoring

## Troubleshooting:

### Common Issues:
1. **Authentication Error**: Run `gcloud auth login`
2. **Project Not Set**: Run `gcloud config set project YOUR_PROJECT_ID`
3. **API Not Enabled**: The script enables required APIs automatically
4. **Memory Issues**: Increase memory in deployment command

### Check Logs:
```bash
gcloud run services logs read restaurant-finder --region us-central1
```

### Update Service:
```bash
gcloud run deploy restaurant-finder --source . --region us-central1
```

## Cost Estimation:
- **Free tier**: 2 million requests/month
- **After free tier**: ~$0.40 per million requests
- **Memory**: ~$0.00002400 per GB-second
- **CPU**: ~$0.00002400 per vCPU-second

Your app will likely stay within the free tier for personal use!
