# URL Shortener Backend

A Python Flask backend for the URL Shortener application. This backend provides persistent storage using SQLite and RESTful API endpoints for URL shortening.

## Features

- ✅ Create shortened URLs
- ✅ Redirect to original URLs
- ✅ Track click counts
- ✅ View all shortened URLs
- ✅ Delete URLs
- ✅ Duplicate URL detection
- ✅ URL validation

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Shorten a URL
**POST** `/api/shorten`
```json
{
  "long_url": "https://example.com/some/very/long/url"
}
```
Response:
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/r/abc123",
  "long_url": "https://example.com/some/very/long/url",
  "clicks": 0
}
```

### 2. Get All URLs
**GET** `/api/urls`

Returns a list of all shortened URLs with their statistics.

### 3. Get URL Info
**GET** `/api/url/<short_code>`

Returns information about a specific shortened URL.

### 4. Redirect (Access Short URL)
**GET** `/r/<short_code>`

Redirects to the original URL and increments the click count.

### 5. Delete URL
**DELETE** `/api/url/<short_code>`

Deletes a shortened URL.

## Database

- **Type**: SQLite
- **File**: `url_shortener.db` (auto-created)
- **Table**: `url_mappings` with columns:
  - `id`: Primary key
  - `short_code`: Unique short code
  - `long_url`: Original URL
  - `clicks`: Click counter
  - `created_at`: Creation timestamp

## Frontend Integration

Update your HTML file to use these API endpoints instead of localStorage:

```javascript
// Example: Shorten URL
async function shortenUrl(longUrl) {
  const response = await fetch('http://localhost:5000/api/shorten', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ long_url: longUrl })
  });
  return await response.json();
}

// Example: Get all URLs
async function getAllUrls() {
  const response = await fetch('http://localhost:5000/api/urls');
  return await response.json();
}
```

## Environment Variables

Create a `.env` file if you want to customize:

```
DATABASE_URL=sqlite:///./url_shortener.db
FLASK_ENV=development
```

## Running in Production

For production, use a production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

- **CORS errors**: Make sure Flask-CORS is installed and enabled
- **Database locked**: Close other connections to the database
- **Port already in use**: Change port in `app.py` or kill the process using port 5000
