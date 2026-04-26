# ⚡ Quick Deploy to Google Cloud in 5 Minutes

## Prerequisites (2 min)

1. **Install Google Cloud CLI**
   ```bash
   brew install google-cloud-sdk
   ```

2. **Login**
   ```bash
   gcloud auth login
   ```

## Deploy Backend to Cloud Run (3 min)

```bash
# Go to backend folder
cd backend

# Deploy (replace with your project ID)
gcloud run deploy url-shortener \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --platform managed

# When prompted:
# - Set Project ID: [your-project-id]
# - Region: us-central1
```

✅ **Copy the Service URL** from output (looks like: `https://url-shortener-xxxxx.run.app`)

## Update Frontend

Edit `url_with_backend.html` - change line ~265:

```javascript
// OLD:
const BACKEND_URL = 'http://localhost:5000';

// NEW (paste your Cloud Run URL):
const BACKEND_URL = 'https://url-shortener-xxxxx.run.app';
```

## Deploy Frontend (Pick One)

### 🚀 Netlify (Easiest - 1 min)
1. Drag & drop `url_with_backend.html` → [netlify.com](https://netlify.com)
2. Get your live URL instantly
3. Done! ✅

### 🐙 GitHub Pages (Free - 2 min)
1. Push to GitHub
2. Settings → Pages → Enable
3. Live at `https://yourusername.github.io/repo/url_with_backend.html`

### ☁️ Google Cloud Storage
```bash
# Create bucket
gsutil mb gs://url-shortener-$(date +%s)

# Upload
gsutil cp url_with_backend.html gs://your-bucket/

# Make public
gsutil acl ch -u AllUsers:R gs://your-bucket/url_with_backend.html
```

## Test It

Open your frontend URL → Try shortening a URL

## View Logs

```bash
gcloud run logs read url-shortener --limit 20
```

## Costs

✅ **Free tier:** 2 million requests/month  
💰 **Typical usage:** $0.50-5/month  

---

**🎉 Done!** Your URL Shortener is live on Google Cloud!

For advanced setup (custom database, domain, etc), see: [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)
