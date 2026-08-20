# Dockerfile for Intent-Deterministic Development Platform
# Developer: ADITYA KAMBLE

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create artifact directory
RUN mkdir -p /app/artifacts

# Set environment variables
ENV PLATFORM_ENV=production
ENV LOG_LEVEL=info
ENV RT_MAX_WORKERS=4
ENV PYTHONUNBUFFERED=1

# Expose metrics port
EXPOSE 9090

# Default command
CMD ["python3", "main.py", "--demo"]