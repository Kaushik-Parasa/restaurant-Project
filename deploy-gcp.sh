#!/bin/bash

# GCP Cloud Run Deployment Script for Restaurant Finder

# Set your project ID (replace with your actual project ID)
PROJECT_ID="your-project-id"
SERVICE_NAME="restaurant-finder"
REGION="us-central1"

echo "🚀 Deploying Restaurant Finder to Google Cloud Run..."

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "📋 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build and deploy to Cloud Run
echo "🔨 Building and deploying..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the URL shown above"
echo "💡 Don't forget to set your GOOGLE_API_KEY environment variable!"
