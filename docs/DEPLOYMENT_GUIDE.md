# Deployment Guide

**Developer: ADITYA KAMBLE**  
**Complete Guide to Deploying the Intent-Deterministic Development Platform**

## 📚 Table of Contents

1. [Overview](#overview)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Setup](#production-setup)
6. [CI/CD Integration](#cicd-integration)
7. [Monitoring & Logging](#monitoring--logging)
8. [Scaling & Performance](#scaling--performance)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Intent-Deterministic Development Platform can be deployed in multiple ways depending on your needs:

- **Local Development**: For development and testing
- **Docker**: For containerized deployments
- **Cloud**: For production on AWS, GCP, Azure
- **Kubernetes**: For orchestrated deployments
- **Edge/IoT**: For on-device deployment

---

## Local Deployment

### Prerequisites

```bash
# Python 3.8+
python3 --version

# pip
pip3 --version

# Git
git --version
```

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/ION.git
cd ION

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 main.py --help
```

### Running Locally

```bash
# Run example
python3 main.py --example 1

# Run real-time demo
python3 main.py --realtime

# Compile ION source
python3 main.py --compile service.ion

# Run full demo
python3 main.py --demo
```

### Environment Configuration

Create `.env` file:

```bash
# Platform Configuration
PLATFORM_ENV=development
LOG_LEVEL=debug
MAX_WORKERS=4

# Real-Time Configuration
RT_RESOLUTION_MS=1
RT_MAX_WORKERS=4
RT_MONITORING=true

# Artifact Storage
ARTIFACT_DIR=./artifacts
ARTIFACT_RETENTION_DAYS=30

# Security
SECURITY_LEVEL=standard
ENABLE_AUDIT_LOG=true
```

Load environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

PLATFORM_ENV = os.getenv('PLATFORM_ENV', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
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

# Expose port (if needed)
EXPOSE 8080

# Run application
CMD ["python3", "main.py", "--demo"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ion-platform:
    build: .
    container_name: ion-platform
    volumes:
      - ./artifacts:/app/artifacts
      - ./projects:/app/projects
    environment:
      - PLATFORM_ENV=production
      - LOG_LEVEL=info
      - RT_MAX_WORKERS=4
    ports:
      - "8080:8080"
    restart: unless-stopped

  ion-monitoring:
    image: prom/prometheus
    container_name: ion-monitoring
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
```

### Build and Run

```bash
# Build Docker image
docker build -t ion-platform:latest .

# Run container
docker run -d \
  --name ion-platform \
  -v $(pwd)/artifacts:/app/artifacts \
  -p 8080:8080 \
  ion-platform:latest

# Or use Docker Compose
docker-compose up -d

# View logs
docker logs -f ion-platform

# Stop container
docker-compose down
```

### Multi-Stage Dockerfile

For optimized production builds:

```dockerfile
# Build stage
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python3", "main.py", "--demo"]
```

---

## Cloud Deployment

### AWS Deployment

#### EC2 Deployment

```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name my-key-pair \
  --security-group-ids sg-12345678

# SSH into instance
ssh -i my-key-pair.pem ec2-user@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Install dependencies
sudo yum update -y
sudo yum install python3 git -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run platform
python3 main.py --demo
```

#### AWS Lambda Deployment

Create `lambda_handler.py`:

```python
import json
from ion_language import parse_ion
from ion_compiler import IONCompiler
from artifact_generator import ArtifactGenerator

def lambda_handler(event, context):
    # Parse ION source from event
    source = event.get('source', '')
    
    # Compile
    compiler = IONCompiler()
    result = compiler.compile_source(source)
    
    # Generate artifacts
    artifact_gen = ArtifactGenerator()
    artifacts = artifact_gen.generate_all_artifacts(intent, proof)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': result.success,
            'artifacts': len(artifacts)
        })
    }
```

Deploy with AWS CLI:

```bash
# Create deployment package
zip lambda.zip lambda_handler.py

# Deploy Lambda
aws lambda create-function \
  --function-name ion-compiler \
  --runtime python3.9 \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda.zip \
  --role arn:aws:iam::123456789012:role/lambda-role
```

#### AWS ECS Deployment

Create `ecs-task-definition.json`:

```json
{
  "family": "ion-platform",
  "containerDefinitions": [
    {
      "name": "ion-platform",
      "image": "ion-platform:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "PLATFORM_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

Deploy:

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Run task
aws ecs run-task \
  --cluster ion-cluster \
  --task-definition ion-platform
```

### Google Cloud Platform Deployment

#### Cloud Run Deployment

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/ion-platform

# Deploy to Cloud Run
gcloud run deploy ion-platform \
  --image gcr.io/PROJECT_ID/ion-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Google Cloud Functions

Create `main.py`:

```python
def ion_compiler(request):
    source = request.get_json().get('source', '')
    
    from ion_compiler import IONCompiler
    compiler = IONCompiler()
    result = compiler.compile_source(source)
    
    return {'success': result.success}
```

Deploy:

```bash
gcloud functions deploy ion-compiler \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated
```

### Azure Deployment

#### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry myregistry --image ion-platform:latest .

# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name ion-platform \
  --image myregistry.azurecr.io/ion-platform:latest \
  --cpu 1 \
  --memory 2
```

---

## Production Setup

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB

**Recommended:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+

### Configuration

Create `config/production.py`:

```python
import os

class ProductionConfig:
    PLATFORM_ENV = 'production'
    LOG_LEVEL = 'info'
    
    # Real-time configuration
    RT_RESOLUTION_MS = 1
    RT_MAX_WORKERS = 8
    RT_MONITORING = True
    
    # Artifact storage
    ARTIFACT_DIR = '/var/lib/ion/artifacts'
    ARTIFACT_RETENTION_DAYS = 90
    
    # Security
    SECURITY_LEVEL = 'critical'
    ENABLE_AUDIT_LOG = True
    AUDIT_LOG_RETENTION_DAYS = 365
    
    # Performance
    MAX_CONCURRENT_COMPILATIONS = 10
    VERIFICATION_TIMEOUT = 300  # seconds
    
    # Monitoring
    ENABLE_METRICS = True
    METRICS_PORT = 9090
```

### Systemd Service

Create `/etc/systemd/system/ion-platform.service`:

```ini
[Unit]
Description=Intent-Deterministic Development Platform
After=network.target

[Service]
Type=simple
User=ion
Group=ion
WorkingDirectory=/opt/ion
Environment="PLATFORM_ENV=production"
ExecStart=/opt/ion/venv/bin/python3 /opt/ion/main.py --demo
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
# Enable service
sudo systemctl enable ion-platform

# Start service
sudo systemctl start ion-platform

# Check status
sudo systemctl status ion-platform

# View logs
sudo journalctl -u ion-platform -f
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/ion-platform`:

```nginx
upstream ion_backend {
    server 127.0.0.1:8080;
}

server {
    listen 80;
    server_name ion.example.com;

    location / {
        proxy_pass http://ion_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /artifacts {
        alias /var/lib/ion/artifacts;
        autoindex off;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/ion-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy ION Platform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: python3 quick_test.py
      
      - name: Run examples
        run: python3 main.py --example 1

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t ion-platform:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push ion-platform:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Add deployment commands
          echo "Deploying to production..."
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - python3 -m pip install -r requirements.txt
    - python3 quick_test.py

build:
  stage: build
  script:
    - docker build -t ion-platform:$CI_COMMIT_SHA .
    - docker push ion-platform:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/ion-platform ion-platform=ion-platform:$CI_COMMIT_SHA
  only:
    - main
```

---

## Monitoring & Logging

### Prometheus Metrics

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ion-platform'
    static_configs:
      - targets: ['localhost:9090']
```

### Application Metrics

Add to your application:

```python
from prometheus_client import start_http_server, Counter, Histogram

# Define metrics
compilation_counter = Counter('ion_compilations_total', 'Total compilations')
compilation_duration = Histogram('ion_compilation_duration_seconds', 'Compilation duration')

# Use metrics
@compilation_duration.time()
def compile_with_metrics(source):
    compilation_counter.inc()
    return compiler.compile_source(source)

# Start metrics server
start_http_server(9090)
```

### Logging Configuration

Create `logging_config.py`:

```python
import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        '/var/log/ion/platform.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
```

---

## Scaling & Performance

### Horizontal Scaling

#### Kubernetes Deployment

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ion-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ion-platform
  template:
    metadata:
      labels:
        app: ion-platform
    spec:
      containers:
      - name: ion-platform
        image: ion-platform:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        env:
        - name: PLATFORM_ENV
          value: "production"
```

Create `k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ion-platform
spec:
  selector:
    app: ion-platform
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Performance Tuning

#### Memory Optimization

```python
# Configure memory limits
from memory_model import MemoryManager

memory_manager = MemoryManager(
    max_heap_size=1024 * 1024 * 1024,  # 1GB
    enable_gc=True,
    gc_threshold=0.8
)
```

#### Thread Pool Configuration

```python
from realtime_system import RealTimeScheduler

# Configure for high throughput
scheduler = RealTimeScheduler(
    max_workers=16,  # Increase workers
    enable_monitoring=True
)
```

---

## Security Considerations

### HTTPS/SSL

Configure SSL with Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name ion.example.com;

    ssl_certificate /etc/ssl/certs/ion.crt;
    ssl_certificate_key /etc/ssl/private/ion.key;

    location / {
        proxy_pass http://ion_backend;
    }
}
```

### Capability-Based Security

```python
from capability_security import CapabilityEnforcer, SecurityContext

# Configure production security
enforcer = CapabilityEnforcer()
enforcer.set_audit_logging(True)
enforcer.set_security_level('critical')

# Create restricted context
context = enforcer.create_context(
    principal="production_user",
    capabilities=[file_capability, network_capability]
)
```

### Network Security

Configure firewall rules:

```bash
# Allow only necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 9090/tcp  # Metrics port - internal only
sudo ufw enable
```

---

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### Permission Denied

```bash
# Solution: Check file permissions
chmod +x main.py
sudo chown -R ion:ion /opt/ion
```

#### Port Already in Use

```bash
# Solution: Find and kill process
lsof -i :8080
kill -9 <PID>
```

#### Memory Issues

```bash
# Solution: Increase memory limits
export PYTHONMALLOC=debug
python3 -X限 memory_limit=2GB main.py --demo
```

### Health Checks

Create health check endpoint:

```python
def health_check():
    try:
        # Check core components
        from ion_compiler import IONCompiler
        from realtime_system import RealTimeScheduler
        
        compiler = IONCompiler()
        scheduler = RealTimeScheduler()
        
        return {
            'status': 'healthy',
            'components': {
                'compiler': 'ok',
                'scheduler': 'ok'
            }
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
```

---

## Quick Deployment Checklist

- [ ] Install dependencies
- [ ] Configure environment variables
- [ ] Set up artifact storage
- [ ] Configure logging
- [ ] Enable monitoring
- [ ] Set up SSL/HTTPS
- [ ] Configure firewall
- [ ] Set up backups
- [ ] Test health checks
- [ ] Configure alerts

---

## Summary

The Intent-Deterministic Development Platform can be deployed in various environments:

- ✅ **Local**: For development and testing
- ✅ **Docker**: For containerized deployments
- ✅ **Cloud**: AWS, GCP, Azure with managed services
- ✅ **Kubernetes**: For orchestrated, scalable deployments
- ✅ **Edge/IoT**: For on-device real-time execution

Choose the deployment method that best fits your infrastructure and requirements.

**Developer: ADITYA KAMBLE**