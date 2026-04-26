# Alternative Cloud Deployment Options

If you want to deploy to a different cloud platform, here are the alternatives:

## 1. ⚡ Render (Recommended Alternative)

**Pros:** Free tier, very simple, no credit card needed  
**Cons:** May be slower than Cloud Run  
**Cost:** Free for starter tier

### Deploy Steps:

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to render.com
# 3. Click "New +" → "Web Service"
# 4. Connect GitHub
# 5. Select your repository
# 6. Settings:
#    - Build Command: pip install -r requirements.txt
#    - Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
#    - Environment: Add DATABASE_URL variable

# 7. Deploy!
```

**Get Your URL:** Copy from Render dashboard  

---

## 2. 🚂 Railway (Very Simple)

**Pros:** Generous free tier ($5/month), super easy  
**Cons:** Limited free credits  
**Cost:** Free tier + pay as you go

### Deploy Steps:

```bash
# 1. Go to railway.app
# 2. Click "New Project"
# 3. Select "GitHub Repo"
# 4. Connect and select repo
# 5. Add environment variables:
#    - DATABASE_URL=sqlite:///./url_shortener.db
# 6. Deploy!
```

**Get Your URL:** Auto-generated at deployment

---

## 3. 🪰 Fly.io (Fast & Modern)

**Pros:** Global deployment, fast, modern infrastructure  
**Cons:** Requires learning fly CLI  
**Cost:** Free tier available

### Deploy Steps:

```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Go to backend folder
cd backend

# 4. Initialize
fly launch

# 5. Deploy
fly deploy

# 6. Get your URL
fly open
```

---

## 4. 🟦 AWS (Most Powerful)

**Pros:** Massive free tier, highly scalable  
**Cons:** Complex setup, confusing pricing  
**Cost:** Free tier for 12 months

### Deploy to Elastic Beanstalk:

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Go to backend
cd backend

# 3. Initialize
eb init -p python-3.11 url-shortener-app

# 4. Create environment
eb create production

# 5. Deploy
eb deploy

# 6. Get URL
eb open
```

---

## 5. 🔷 Azure (Enterprise)

**Pros:** Best enterprise support, free tier available  
**Cons:** Steep learning curve  
**Cost:** Free tier + pay as you go

### Deploy to App Service:

```bash
# 1. Install Azure CLI
brew install azure-cli

# 2. Login
az login

# 3. Create resource group
az group create --name url-shortener --location eastus

# 4. Create App Service Plan
az appservice plan create --name url-shortener-plan \
  --resource-group url-shortener --sku B1

# 5. Deploy
az webapp deployment source config-zip --resource-group url-shortener \
  --name url-shortener-app --src backend.zip
```

---

## 6. 🐋 Docker (Any Platform)

**General template for any Docker-compatible platform:**

```bash
# 1. Build Docker image
docker build -t url-shortener:latest .

# 2. Tag for registry
docker tag url-shortener:latest [your-registry]/url-shortener:latest

# 3. Push to registry
docker push [your-registry]/url-shortener:latest

# 4. Deploy using registry URL
# (Each platform has different deployment method)
```

---

## Quick Comparison

| Platform | Free Tier | Setup Time | Performance | Recommendation |
|----------|-----------|-----------|-------------|-----------------|
| **Google Cloud Run** | 2M req/mo | 2 min | Excellent | ✅ Best choice |
| Render | ✅ Generous | 2 min | Good | Good alternative |
| Railway | ✅ $5/mo | 3 min | Very good | Simple & reliable |
| Fly.io | ✅ Generous | 5 min | Excellent | Fast deployment |
| AWS | ✅ Limited | 10 min | Excellent | Most features |
| Azure | ✅ Limited | 15 min | Excellent | Enterprise |
| Heroku | ❌ Paid | 3 min | Good | Deprecated free tier |

---

## Frontend Deployment Options

For the `url_with_backend.html` frontend, best options are:

### 🚀 Netlify (Recommended)
- Drop & deploy
- Free SSL, CDN, analytics
- Best for simple HTML apps

### 🐙 GitHub Pages
- Free with GitHub
- Perfect for portfolios
- Deploy from git push

### ☁️ Vercel
- Next.js optimized
- Great for modern apps
- Free tier available

### ☁️ Google Cloud Storage
- Works with Cloud Run
- Cheap storage
- Need to manage CORS

---

## My Recommendation

**For easiest experience:**
1. **Backend:** Google Cloud Run (or Render as backup)
2. **Frontend:** Netlify (drag & drop)
3. **Database:** Start with SQLite, upgrade to Cloud SQL if needed

**For best value:**
1. **Backend:** Railway ($5/mo free tier)
2. **Frontend:** GitHub Pages (free)
3. **Database:** SQLite

---

Still want Google Cloud? See: [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)  
Quick deploy? See: [DEPLOY_NOW.md](./DEPLOY_NOW.md)
