# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ ./templates/

# Expose port
EXPOSE 5000

# Create a simple healthcheck script
RUN echo '#!/bin/sh\nexec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 --access-logfile - --error-logfile - app:app' > /start.sh && chmod +x /start.sh

# Run the application with gunicorn
CMD ["/start.sh"]
