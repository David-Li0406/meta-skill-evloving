# Node.js Dockerfile Template

Use this template to create a production-ready Dockerfile for Node.js applications that follows Docker best practices for layer caching, security, and build efficiency.

## Template Variables

- `{{APP_NAME}}` - Application name (e.g., "fanhub-backend")
- `{{NODE_VERSION}}` - Node.js version (e.g., "18")
- `{{PORT}}` - Exposed port (e.g., "3000")
- `{{BUILD_COMMAND}}` - Build command if needed (e.g., "npm run build")
- `{{START_COMMAND}}` - Command to start app (e.g., "node src/index.js")

## Basic Node.js API Template

```dockerfile
# Use official Node.js LTS Alpine image (smaller, more secure)
FROM node:{{NODE_VERSION}}-alpine

# Set working directory for all subsequent commands
WORKDIR /app

# Copy dependency files FIRST (for layer caching)
# This layer only rebuilds when package files change
COPY package*.json ./

# Install dependencies
# Use 'npm ci' for reproducible installs (respects package-lock.json exactly)
RUN npm ci --only=production

# Copy application source code LAST
# This layer rebuilds on every code change (but deps are cached)
COPY . .

# Expose the application port
EXPOSE {{PORT}}

# Set NODE_ENV to production
ENV NODE_ENV=production

# Start the application
CMD ["{{START_COMMAND}}"]
```

## React/Frontend Build Template (Multi-Stage)

```dockerfile
# Stage 1: Build the application
FROM node:{{NODE_VERSION}}-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN {{BUILD_COMMAND}}

# Stage 2: Production image with nginx
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## Development Dockerfile Template

```dockerfile
FROM node:{{NODE_VERSION}}-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies)
RUN npm ci

# Copy source code
COPY . .

# Expose port and enable hot-reload
EXPOSE {{PORT}}

# Start with nodemon for auto-restart
CMD ["npm", "run", "dev"]
```

## .dockerignore Template

```
# Node
node_modules
npm-debug.log
yarn-debug.log
yarn-error.log

# Git
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile

# IDE
.vscode
.idea
*.swp
*.swo
*~

# Testing
coverage
.nyc_output
__tests__
*.test.js
*.spec.js

# Documentation
README.md
CHANGELOG.md
LICENSE
*.md

# Environment
.env
.env.local
.env.*.local

# Build artifacts
dist
build
.next
.nuxt

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log
```

## Usage Example

**For FanHub Backend API:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY src/ ./src/
COPY database/ ./database/

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "src/index.js"]
```

**For FanHub Frontend:**

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## Best Practices Checklist

When using this template, ensure:

- [ ] `WORKDIR` is set before any `COPY` or `RUN` commands
- [ ] `package*.json` is copied BEFORE `npm install/ci`
- [ ] Source code is copied AFTER dependencies (for caching)
- [ ] Using `npm ci` instead of `npm install` (reproducible builds)
- [ ] `.dockerignore` excludes `node_modules` and dev files
- [ ] Multi-stage build for frontend apps (smaller final image)
- [ ] Alpine images used (smaller, more secure)
- [ ] `ENV NODE_ENV=production` set for production builds
- [ ] Only production dependencies in final image (`--only=production`)

## Common Customizations

### Add Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js
```

### Add Non-Root User (Security)

```dockerfile
# Create app user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs
```

### Add Build Arguments

```dockerfile
ARG NODE_ENV=production
ARG API_URL
ENV NODE_ENV=$NODE_ENV
ENV REACT_APP_API_URL=$API_URL
```

## Template Selection Guide

| Use Case | Template | Why |
|----------|----------|-----|
| **Node.js API** | Basic API Template | Simple, single-stage, production-ready |
| **React/Vue App** | Frontend Multi-Stage | Smaller final image (only static files) |
| **Development** | Development Template | Includes dev dependencies, hot-reload |
| **Microservice** | Basic + Health Check | Production API with monitoring |
| **Security-Critical** | Basic + Non-Root User | Runs as non-root for security |

## When to Use This Template

Ask Copilot to use this template when:
- Creating a new Dockerfile for a Node.js project
- Refactoring an existing Dockerfile to follow best practices
- Setting up Docker for a new service in FanHub
- Teaching someone Docker best practices

**Example prompts:**
- *"Use the Dockerfile template to create a Dockerfile for our new admin-api service"*
- *"Generate a production Dockerfile for a Node.js API on port 4000"*
- *"Create a multi-stage Dockerfile for a React app"*
