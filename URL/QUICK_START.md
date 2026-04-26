# Quick Start Guide

## Setup & Run Backend in 3 Steps

### Step 1: Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Frontend
- Use `url_with_backend.html` (updated version that connects to backend)
- Original `url.html` uses localStorage and doesn't need a server

## API Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shorten` | Create shortened URL |
| GET | `/api/urls` | Get all URLs |
| GET | `/api/url/<code>` | Get URL details |
| GET | `/r/<code>` | Redirect & count click |
| DELETE | `/api/url/<code>` | Delete URL |

## Features

✅ **Persistent Storage** - Uses SQLite database  
✅ **Click Tracking** - Count how many times each link is visited  
✅ **Duplicate Detection** - Won't create duplicate entries for same URL  
✅ **Easy Sharing** - Click the short URL to copy to clipboard  
✅ **REST API** - Integrate with other applications  
✅ **CORS Enabled** - Works from different domains  

## File Structure

```
URL/
├── url.html                 # Original (localStorage version)
├── url_with_backend.html    # Updated (uses backend)
└── backend/
    ├── app.py              # Main Flask application
    ├── requirements.txt    # Python dependencies
    ├── .env.example        # Environment variables template
    ├── README.md           # Full documentation
    └── url_shortener.db    # SQLite database (auto-created)
```

## Troubleshooting

**Error: "Connection refused"**
- Make sure backend is running on port 5000
- Check if another app is using port 5000

**Error: "Module not found"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Database issues**
- Delete `url_shortener.db` to reset
- It will be recreated automatically on next run

## Next Steps

1. ✅ Backend is ready to use
2. Run frontend with `python -m http.server 8000` in the project root
3. Open `http://localhost:8000/url_with_backend.html` in browser
4. Start shortening URLs!
