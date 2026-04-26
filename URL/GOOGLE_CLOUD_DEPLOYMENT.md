# Deploying URL Shortener to Google Cloud

This guide covers deploying to **Google Cloud Run** (recommended - serverless, cheapest).

## Prerequisites

1. **Google Cloud Account** - [Create free account](https://cloud.google.com/free)
   - Free tier includes $300 credit + free services
   - Cloud Run: 2M requests/month free

2. **Install Google Cloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

3. **Authenticate**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

## Step 1: Create a Google Cloud Project

```bash
# Set your project ID (e.g., "url-shortener-123")
export PROJECT_ID="url-shortener-123"

# Create project
gcloud projects create $PROJECT_ID

# Set as current project
gcloud config set project $PROJECT_ID
```

## Step 2: Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## Step 3: Deploy to Cloud Run

### Option A: Deploy from Local Machine (Easiest)

```bash
cd backend

# Deploy directly
gcloud run deploy url-shortener \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 3600 \
  --set-env-vars DATABASE_URL="sqlite:///./url_shortener.db"
```

**Output example:**
```
Service [url-shortener] revision [url-shortener-00001-abc] has been deployed.
Service URL: https://url-shortener-xxxxx.run.app
```

✅ **Your backend is live!** Copy the service URL.

### Option B: Deploy via GitHub (CI/CD)

1. Push your code to GitHub
2. Go to [Google Cloud Console](https://console.cloud.google.com/)
3. Cloud Run → Create Service
4. Select "GitHub" as source
5. Connect your repo and select `backend` folder
6. Set environment variables in the deployment form

## Step 4: Update Frontend URL

Edit `url_with_backend.html` and change:

```javascript
// OLD
const BACKEND_URL = 'http://localhost:5000';

// NEW
const BACKEND_URL = 'https://url-shortener-xxxxx.run.app';  // Use your Cloud Run URL
```

## Step 5: Deploy Frontend

### Option A: Google Cloud Storage + Cloud CDN

```bash
# Create storage bucket
gsutil mb gs://url-shortener-frontend-$(date +%s)

# Upload HTML file
gsutil -m cp url_with_backend.html gs://your-bucket-name/

# Make it public
gsutil acl ch -u AllUsers:R gs://your-bucket-name/url_with_backend.html

# Access at: https://storage.googleapis.com/your-bucket-name/url_with_backend.html
```

### Option B: Static Site with Netlify (Easiest for Frontend)

1. Go to [Netlify.com](https://netlify.com)
2. Click "New site from Git" or drag & drop `url_with_backend.html`
3. Your frontend is live and gets a free domain

### Option C: GitHub Pages

1. Push to GitHub repo
2. Enable GitHub Pages in Settings
3. Site is live at `https://yourusername.github.io/repo-name/url_with_backend.html`

## Step 6: Test Everything

```bash
# Test backend
curl https://url-shortener-xxxxx.run.app/

# Should return:
# {"status":"URL Shortener Backend Running"}
```

Then open your frontend URL in a browser and test:
- ✅ Enter a URL
- ✅ Click "Shorten URL"
- ✅ See shortened URL
- ✅ Click to copy
- ✅ Click to redirect

## Monitoring & Logs

```bash
# View logs
gcloud run logs read url-shortener --region us-central1 --limit 100

# View metrics
gcloud run describe url-shortener --region us-central1

# Stream logs in real-time
gcloud run logs read url-shortener --region us-central1 --follow
```

## Database Persistence Issue

⚠️ **Important**: SQLite database is ephemeral on Cloud Run (deleted when service scales down).

### Solution 1: Use Cloud SQL (PostgreSQL)

```bash
# Create Cloud SQL instance
gcloud sql instances create url-shortener-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1

# Create database
gcloud sql databases create url_shortener \
  --instance url-shortener-db

# Get connection string and update in deployment
```

Then update `app.py`:
```python
DATABASE_URL = "postgresql://user:password@cloudsql-connection-name/url_shortener"
```

### Solution 2: Use Firestore (NoSQL)

Replace SQLite with Firestore for better cloud compatibility.

### Solution 3: Use Cloud Storage (Quick Fix)

Store mappings as JSON in Cloud Storage (simplest for MVP).

## Environment Variables

Set environment variables in Cloud Run:

```bash
gcloud run services update url-shortener \
  --region us-central1 \
  --set-env-vars DATABASE_URL="postgresql://...",FLASK_ENV="production"
```

## Cost Estimate

**Monthly cost for typical usage:**
- Cloud Run: ~$0.40 (free tier mostly covers)
- Cloud SQL: ~$7-15/month (if used)
- Storage: ~$0.02-0.10/month
- **Total: ~$0.50-15/month** (depending on database choice)

## Troubleshooting

### "Permission denied" error
```bash
gcloud auth application-default login
```

### "Cannot find Dockerfile"
```bash
# Make sure you're in the `backend` folder
cd backend
gcloud run deploy ...
```

### Service returns 500 error
```bash
# Check logs
gcloud run logs read url-shortener --limit 50

# Verify DATABASE_URL is set correctly
gcloud run describe url-shortener
```

### Domain/CORS issues
Make sure `Flask-CORS` is enabled in `app.py` ✅

## Quick Reference

| Task | Command |
|------|---------|
| Deploy | `gcloud run deploy url-shortener --source . --platform managed` |
| View logs | `gcloud run logs read url-shortener --limit 100` |
| Update env vars | `gcloud run services update url-shortener --set-env-vars KEY=VALUE` |
| Delete service | `gcloud run services delete url-shortener` |
| List services | `gcloud run services list` |

## Next Steps

✅ Backend deployed on Cloud Run  
⬜ Frontend deployed (use Netlify or GitHub Pages)  
⬜ Update frontend URL to point to Cloud Run  
⬜ Setup database persistence (Cloud SQL recommended)  
⬜ Add custom domain (optional)  
⬜ Setup monitoring alerts (optional)  

---

**Need help?** Check Google Cloud documentation: https://cloud.google.com/run/docs/quickstarts/build-and-deploy
