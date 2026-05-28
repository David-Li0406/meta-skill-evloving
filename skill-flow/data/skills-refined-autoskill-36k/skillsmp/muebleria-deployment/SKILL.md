---
name: muebleria-deployment
description: >
  Deployment patterns (Docker, environment variables, CI/CD) for MuebleriaIris.
  Trigger: When deploying to production, configuring Docker, or setting up CI/CD.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Deploying to production"
    - "Setting up Docker"
    - "Configuring CI/CD"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Deploying to production
- Setting up Docker containers
- Configuring environment variables
- Creating CI/CD pipelines
- Setting up reverse proxy (Nginx)

---

## Critical Patterns

### Pattern 1: Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "4321:4321"
    environment:
      - VITE_API_URL=http://localhost:5000
    volumes:
      - ./src:/app/src
      - ./public:/app/public
    command: npm run dev
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/muebleria
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - FLASK_ENV=development
    volumes:
      - ./backend:/app
    depends_on:
      - db
    command: flask run --host=0.0.0.0

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=muebleria
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Pattern 2: Dockerfile (Backend)

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Pattern 3: Dockerfile (Frontend)

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production image
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## Environment Variables

### Pattern 4: Environment Variables (.env)

```bash
# .env.example - Template (commit to repo)
# Copy to .env and fill with real values (DO NOT COMMIT .env)

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/muebleria

# Flask
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=production

# Frontend
VITE_API_URL=http://localhost:5000

# MercadoPago
MERCADOPAGO_ACCESS_TOKEN=your-token-here
MERCADOPAGO_PUBLIC_KEY=your-public-key-here

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# URLs
FRONTEND_URL=https://muebleriairis.com
BACKEND_URL=https://api.muebleriairis.com
```

### Pattern 5: Loading Environment Variables

```python
# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MercadoPago
    MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN')
    MERCADOPAGO_PUBLIC_KEY = os.environ.get('MERCADOPAGO_PUBLIC_KEY')
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# backend/app/__init__.py
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
```

---

## CI/CD Pipeline

### Pattern 6: GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          cd backend
          pytest
  
  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Run tests
        run: npm test
  
  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Add deployment script here
          echo "Deploying to production..."
```

---

## Nginx Configuration

### Pattern 7: Nginx Reverse Proxy

```nginx
# nginx.conf
server {
    listen 80;
    server_name muebleriairis.com;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Production Checklist

### Pattern 8: Pre-deployment Checklist

```markdown
## Security
- [ ] .env file not committed
- [ ] SECRET_KEY and JWT_SECRET_KEY are strong random strings
- [ ] Database credentials are secure
- [ ] CORS is configured properly
- [ ] HTTPS is enabled (SSL certificate)
- [ ] Security headers configured

## Database
- [ ] Migrations are up to date
- [ ] Database backup strategy in place
- [ ] Connection pooling configured

## Performance
- [ ] Static files are compressed
- [ ] CDN configured for images
- [ ] Database indexes created
- [ ] Caching strategy implemented

## Monitoring
- [ ] Error logging configured
- [ ] Application monitoring set up
- [ ] Uptime monitoring configured
- [ ] Backup alerts configured

## Environment Variables
- [ ] All environment variables set on server
- [ ] FLASK_ENV=production
- [ ] Debug mode disabled
```

---

## Docker Commands

```bash
# Development
docker-compose up -d              # Start all services
docker-compose logs -f backend    # View backend logs
docker-compose exec backend bash  # Enter backend container
docker-compose down               # Stop all services

# Production Build
docker build -f Dockerfile.backend -t muebleria-backend:latest .
docker build -f Dockerfile.frontend -t muebleria-frontend:latest .

# Run containers
docker run -d -p 5000:5000 --env-file .env muebleria-backend:latest
docker run -d -p 80:80 muebleria-frontend:latest

# Database backup
docker exec postgres pg_dump -U postgres muebleria > backup.sql

# Database restore
docker exec -i postgres psql -U postgres muebleria < backup.sql
```

---

## Best Practices

### DO:
- Use environment variables for all secrets
- Use `.env.example` as template (commit)
- Never commit `.env` file
- Use multi-stage Docker builds
- Set up health checks
- Use volume mounts for development
- Configure logging properly
- Set up automated backups

### DON'T:
- Hardcode secrets in code
- Use default passwords in production
- Run as root in containers
- Expose unnecessary ports
- Skip SSL/HTTPS in production
- Forget to rotate secrets periodically

---

## QA Checklist

- [ ] Docker images build successfully
- [ ] docker-compose.yml works locally
- [ ] All environment variables documented
- [ ] CI/CD pipeline passes
- [ ] Database migrations applied
- [ ] HTTPS configured
- [ ] Monitoring set up
- [ ] Backup strategy in place

---

## Resources

- **Docker**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **GitHub Actions**: https://docs.github.com/actions
- **Nginx**: https://nginx.org/en/docs/
