# Deployment Checklist

Complete this checklist to deploy your URL Shortener to Google Cloud:

## ✅ Pre-Deployment Setup

- [ ] Create Google Cloud account (https://cloud.google.com/free)
- [ ] Verify $300 free credit is added
- [ ] Install Google Cloud CLI: `brew install google-cloud-sdk`
- [ ] Run: `gcloud auth login`
- [ ] Run: `gcloud auth application-default login`
- [ ] Create a Google Cloud project or select existing one

## ✅ Backend Deployment to Cloud Run

- [ ] Update `backend/requirements.txt` with gunicorn ✅ (Already done)
- [ ] Update `backend/app.yaml` for App Engine ✅ (Already done)
- [ ] Update `backend/Dockerfile` for Cloud Run ✅ (Already done)
- [ ] Update `backend/.gcloudignore` ✅ (Already done)
- [ ] Update `backend/app.py` to handle PORT env var ✅ (Already done)

### Deploy Command:
```bash
cd backend
gcloud run deploy url-shortener \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --platform managed
```

- [ ] Copy the **Service URL** from deployment output
- [ ] Save it somewhere (you'll need it next)

**Example URL:** `https://url-shortener-xxxxx.run.app`

## ✅ Test Backend

- [ ] Open browser: `https://[YOUR-SERVICE-URL]/`
- [ ] Should see: `{"status":"URL Shortener Backend Running"}`
- [ ] Backend is working! ✅

## ✅ Update Frontend

Edit `url_with_backend.html`:

- [ ] Find line with: `const BACKEND_URL = 'http://localhost:5000';`
- [ ] Replace with your Cloud Run URL
- [ ] Save file

**Example:**
```javascript
const BACKEND_URL = 'https://url-shortener-xxxxx.run.app';
```

## ✅ Deploy Frontend (Choose ONE)

### Option 1: Netlify (Easiest - Recommended)
- [ ] Go to https://netlify.com
- [ ] Drag & drop `url_with_backend.html` to Netlify
- [ ] Copy your site URL
- [ ] Frontend is live! ✅

### Option 2: GitHub Pages
- [ ] Commit files to GitHub
- [ ] Go to repo Settings → Pages
- [ ] Enable GitHub Pages from main branch
- [ ] Copy your GitHub Pages URL
- [ ] Frontend is live! ✅

### Option 3: Google Cloud Storage
- [ ] Run: `gsutil mb gs://url-shortener-[random]-bucket`
- [ ] Run: `gsutil cp url_with_backend.html gs://your-bucket/`
- [ ] Run: `gsutil acl ch -u AllUsers:R gs://your-bucket/url_with_backend.html`
- [ ] Access at: `https://storage.googleapis.com/your-bucket/url_with_backend.html`
- [ ] Frontend is live! ✅

## ✅ End-to-End Testing

- [ ] Open your frontend URL in browser
- [ ] Input a long URL (e.g., `https://www.github.com/some/very/long/url`)
- [ ] Click "Shorten URL"
- [ ] See shortened URL appear
- [ ] Click shortened URL (should copy to clipboard)
- [ ] Try redirecting by changing backend URL in console:
  ```javascript
  fetch('[BACKEND_URL]/api/urls').then(r => r.json()).then(console.log)
  ```
- [ ] Should see your URLs listed
- [ ] Everything works! ✅

## ✅ Monitoring & Logs

- [ ] View backend logs: `gcloud run logs read url-shortener --limit 50`
- [ ] Check for any errors
- [ ] Verify database is working (entries saved)

## ✅ Documentation

Create a `DEPLOYMENT_INFO.md` file with:

- [ ] Backend URL (Cloud Run): `https://url-shortener-xxxxx.run.app`
- [ ] Frontend URL (Netlify/GitHub): `https://your-domain.netlify.app`
- [ ] How to update: "Edit `url_with_backend.html` backend URL and redeploy"
- [ ] Support links: Documentation files

## ✅ Optional: Custom Domain

- [ ] Register custom domain (GoDaddy, Namecheap, etc.)
- [ ] Point DNS to:
  - **For Netlify:** Add custom domain in Netlify settings
  - **For Cloud Run:** Use Cloud Load Balancer (advanced)
  - **For GitHub Pages:** Update CNAME file

## ✅ Optional: Database Persistence

- [ ] Current setup uses SQLite (data lost on Cloud Run scale-down)
- [ ] Upgrade path: Use Cloud SQL (PostgreSQL)
  - [ ] Create Cloud SQL instance
  - [ ] Update `DATABASE_URL` env var
  - [ ] Test persistence

## ✅ Sharing with Others

- [ ] Frontend URL ready to share
- [ ] Test with friends/colleagues
- [ ] Collect feedback
- [ ] Document any issues

## ✅ Post-Deployment

- [ ] Bookmark all URLs (backend, frontend, docs)
- [ ] Save all passwords/keys in secure location
- [ ] Enable Google Cloud billing alerts (optional)
- [ ] Setup monitoring dashboard (optional)

---

## Troubleshooting

### Backend won't deploy
- [ ] Check `gcloud config get-value project`
- [ ] Verify APIs enabled: `gcloud services list --enabled`
- [ ] Check files exist: `app.py`, `requirements.txt`, `Dockerfile`

### Frontend can't connect to backend
- [ ] Verify backend URL in JavaScript
- [ ] Check CORS is enabled in `app.py` (should be)
- [ ] Open browser console (F12) for error messages
- [ ] Verify backend is running: `curl https://[URL]/`

### Data not persisting
- [ ] SQLite doesn't persist on Cloud Run (expected)
- [ ] Solution: Use Cloud SQL for production
- [ ] Or accept data loss on service restart (ok for demo)

### Getting 500 errors
- [ ] View logs: `gcloud run logs read url-shortener --limit 20`
- [ ] Look for Python error messages
- [ ] Check environment variables are set

---

## Success Checklist

After deployment, you should have:

- ✅ Backend API running on Google Cloud Run
- ✅ Frontend hosted and accessible
- ✅ Can shorten URLs
- ✅ URLs display with click counts
- ✅ Delete button works
- ✅ Shared URL works (redirects properly)
- ✅ Logs show successful requests

---

**Need Help?**
- Google Cloud Docs: https://cloud.google.com/run/docs
- Backend Errors: Check `gcloud run logs read url-shortener`
- Frontend Issues: Open browser DevTools (F12)

**Congratulations on going live! 🎉**
