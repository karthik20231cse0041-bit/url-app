FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY .env.example .env

# Expose port (Cloud Run requires port from PORT env var)
EXPOSE 8080

# Run application with gunicorn
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --timeout 0 app:app
