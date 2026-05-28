---
name: docker-containerization
description: Comprehensive Docker containerization guidance using multi-stage builds, Docker Hardened Images, and Docker AI Agent (Gordon) for Node.js/Next.js applications. Use when containerizing applications with best practices for security, efficiency, and AI-assisted operations.
---

# Docker Containerization Skill

## Overview
This skill provides comprehensive guidance for Docker containerization using multi-stage builds, Docker Hardened Images (DHI), and Docker AI Agent (Gordon) for Node.js/Next.js applications. It includes best practices for security, efficiency, and AI-assisted operations.

## When to Use This Skill
- Containerizing Node.js/Next.js applications with Docker
- Implementing multi-stage builds for optimized images
- Using Docker Hardened Images for security
- Leveraging Docker AI Agent (Gordon) for Dockerfile creation and optimization
- Creating production-ready containerized applications

## Core Dockerfile Patterns

### Multi-Stage Dockerfile for Node.js Applications
Use this pattern for optimized, secure, and production-ready Node.js applications:

```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Node.js TypeScript Application
# ========================================

ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Build Dependencies Stage
# ========================================
FROM base AS build-deps

# Copy package files
COPY package*.json ./

# Install all dependencies with build optimizations
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# Create necessary directories and set permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# Build Stage
# ========================================
FROM build-deps AS build

# Copy only necessary files for building (respects .dockerignore)
COPY --chown=nodejs:nodejs . .

# Build the application
RUN npm run build

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Development Stage
# ========================================
FROM build-deps AS development

# Set environment
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# Copy source files
COPY . .

# Ensure all directories have proper permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# Switch to non-root user
USER nodejs

# Expose ports
EXPOSE 3000 5173 9229

# Start development server
CMD ["npm", "run", "dev:docker"]

# ========================================
# Production Stage
# ========================================
ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS production

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# Set optimized environment variables
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# Copy production dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# Copy built application from build stage
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# Switch to non-root user for security
USER nodejs

# Expose port
EXPOSE 3000

# Start production server
CMD ["node", "dist/server.js"]

# ========================================
# Test Stage
# ========================================
FROM build-deps AS test

# Set environment
ENV NODE_ENV=test \
    CI=true

# Copy source files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs
```

### Simple Dockerfile for Next.js Applications
For simpler Next.js applications, use this optimized pattern:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=base /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/package*.json ./
EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm", "start"]
```

## Docker AI Agent (Gordon) Usage

### Enable Docker AI Agent (Gordon)
1. Install latest Docker Desktop 4.53+
2. Go to Settings > Beta features
3. Toggle Docker AI Agent (Gordon) on

### Gordon Commands

#### Start Gordon AI Conversation
```bash
docker ai
```

#### Rate Dockerfile with Gordon
Have Gordon analyze a Dockerfile and provide improvement suggestions:
```bash
docker ai rate my Dockerfile
```

#### Migrate Dockerfile to Docker Hardened Images
After starting Gordon conversation, request migration:
```
Migrate my dockerfile to DHI
```

## Docker Best Practices

### Security
- Always use non-root users in containers
- Use minimal base images (e.g., Alpine)
- Implement multi-stage builds to reduce attack surface
- Scan images for vulnerabilities

### Performance
- Use build cache optimization with `--mount=type=cache`
- Leverage multi-stage builds to reduce final image size
- Copy only necessary files in each stage
- Use `.dockerignore` to exclude unnecessary files

### Development Workflow
1. Create a `.dockerignore` file to exclude unnecessary files
2. Use multi-stage builds for development and production
3. Implement proper environment variables for different stages
4. Test images locally before deployment

## Common Docker Commands

### Building Images
```bash
docker build -t my-app:latest .
docker build -t my-app:latest --target production .
```

### Running Containers
```bash
docker run -p 3000:3000 my-app:latest
docker run -d -p 3000:3000 --name my-container my-app:latest
```

### Development Mode
```bash
docker build -t my-app:dev --target development .
docker run -p 3000:3000 -v $(pwd):/app my-app:dev
```

## Docker Compose for Multi-Service Applications

```yaml
version: '3.8'
services:
  frontend:
    build:
      context: ./frontend
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      target: production
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Troubleshooting

### Common Issues
- Large image sizes: Use multi-stage builds and Alpine base images
- Slow builds: Implement proper caching with build cache mounts
- Security vulnerabilities: Use non-root users and scan images regularly
- Port conflicts: Ensure proper port mapping in Docker Compose

### Debugging Commands
```bash
# Check running containers
docker ps

# View container logs
docker logs <container-id>

# Execute commands in running container
docker exec -it <container-id> sh

# Build with no cache if needed
docker build --no-cache -t my-app:latest .
```
