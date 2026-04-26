import os
import string
import random
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./url_shortener.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class URLMapping(Base):
    __tablename__ = "url_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    long_url = Column(String)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(length=6):
    """Generate a random short code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_url(url):
    """Validate if the URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

# API Endpoints

@app.post("/api/shorten")
def shorten_url():
    """Create a shortened URL"""
    data = request.get_json()
    long_url = data.get("long_url", "").strip()
    
    if not long_url:
        return jsonify({"error": "long_url is required"}), 400
    
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400
    
    db = SessionLocal()
    try:
        # Check if URL already exists
        existing = db.query(URLMapping).filter(
            URLMapping.long_url.ilike(long_url)
        ).first()
        
        if existing:
            return jsonify({
                "short_code": existing.short_code,
                "short_url": f"{request.host_url}r/{existing.short_code}",
                "long_url": existing.long_url,
                "clicks": existing.clicks,
                "message": "URL already shortened"
            }), 200
        
        # Generate unique short code
        short_code = generate_short_code()
        while db.query(URLMapping).filter(URLMapping.short_code == short_code).first():
            short_code = generate_short_code()
        
        # Save to database
        url_mapping = URLMapping(short_code=short_code, long_url=long_url)
        db.add(url_mapping)
        db.commit()
        db.refresh(url_mapping)
        
        return jsonify({
            "short_code": url_mapping.short_code,
            "short_url": f"{request.host_url}r/{url_mapping.short_code}",
            "long_url": url_mapping.long_url,
            "clicks": url_mapping.clicks
        }), 201
    finally:
        db.close()

@app.get("/api/urls")
def get_all_urls():
    """Get all shortened URLs"""
    db = SessionLocal()
    try:
        urls = db.query(URLMapping).all()
        return jsonify([{
            "short_code": url.short_code,
            "short_url": f"{request.host_url}r/{url.short_code}",
            "long_url": url.long_url,
            "clicks": url.clicks,
            "created_at": url.created_at.isoformat()
        } for url in urls]), 200
    finally:
        db.close()

@app.get("/api/url/<short_code>")
def get_url_info(short_code):
    """Get info about a shortened URL"""
    db = SessionLocal()
    try:
        url_mapping = db.query(URLMapping).filter(URLMapping.short_code == short_code).first()
        if not url_mapping:
            return jsonify({"error": "Short URL not found"}), 404
        
        return jsonify({
            "short_code": url_mapping.short_code,
            "short_url": f"{request.host_url}r/{url_mapping.short_code}",
            "long_url": url_mapping.long_url,
            "clicks": url_mapping.clicks,
            "created_at": url_mapping.created_at.isoformat()
        }), 200
    finally:
        db.close()

@app.get("/r/<short_code>")
def redirect_url(short_code):
    """Redirect to the original URL and increment clicks"""
    db = SessionLocal()
    try:
        url_mapping = db.query(URLMapping).filter(URLMapping.short_code == short_code).first()
        if not url_mapping:
            return jsonify({"error": "Short URL not found"}), 404
        
        url_mapping.clicks += 1
        db.commit()
        
        return redirect(url_mapping.long_url, code=302)
    finally:
        db.close()

@app.delete("/api/url/<short_code>")
def delete_url(short_code):
    """Delete a shortened URL"""
    db = SessionLocal()
    try:
        url_mapping = db.query(URLMapping).filter(URLMapping.short_code == short_code).first()
        if not url_mapping:
            return jsonify({"error": "Short URL not found"}), 404
        
        db.delete(url_mapping)
        db.commit()
        
        return jsonify({"message": "URL deleted successfully"}), 200
    finally:
        db.close()

@app.get("/")
def root():
    """Health check"""
    return jsonify({"status": "URL Shortener Backend Running"}), 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
