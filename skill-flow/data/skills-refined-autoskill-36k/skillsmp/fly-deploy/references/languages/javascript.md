# JavaScript/Node.js on fly.io

## Next.js

### Recommended Configuration

**next.config.js** - Enable standalone output for minimal Docker image:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Optional: For better performance
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}

module.exports = nextConfig
```

### Dockerfile for Next.js

See `assets/dockerfiles/nextjs.Dockerfile` for the complete template.

**Key points:**
- Multi-stage build for minimal image size
- Standalone output reduces image from ~1GB to ~200MB
- Handles `.next/standalone` output correctly
- Copies public and static assets
- Runs as non-root user

### fly.toml for Next.js

```toml
app = "my-nextjs-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/"

[[vm]]
  memory = "512mb"  # Next.js needs more than 256mb
  cpus = 1
```

### Environment Variables

**NEXT_PUBLIC_* variables:**

For variables used in browser-side code, they must be set at **build time**:

```dockerfile
# In Dockerfile
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

Then set during build:
```bash
fly deploy --build-arg NEXT_PUBLIC_API_URL=https://api.example.com
```

**Server-side variables:**

Set via fly secrets (available at runtime):
```bash
fly secrets set DATABASE_URL=postgres://...
fly secrets set API_KEY=secret123
```

### Common Issues

**Static assets 404:**
- Ensure `public/` folder is copied to standalone output
- Check Dockerfile copies `.next/static` correctly

**Module not found errors:**
- Verify `package.json` dependencies are complete
- Check `node_modules` aren't in `.dockerignore`

**Out of memory:**
- Increase to 512MB minimum: `fly scale memory 512`
- For large apps: 1GB recommended

---

## Express

### Dockerfile for Express

See `assets/dockerfiles/express.Dockerfile` for the complete template.

**Key points:**
- Install production dependencies only
- Use `.dockerignore` to exclude `node_modules`, `.git`
- Run as non-root user
- Support both npm and yarn

### fly.toml for Express

```toml
app = "my-express-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "5s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  memory = "256mb"
  cpus = 1
```

### Health Check Endpoint

Always implement a health check:

```js
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() })
})
```

### Database Connections

For apps with databases, handle graceful shutdown:

```js
const gracefulShutdown = async () => {
  console.log('Received shutdown signal, closing connections...')

  // Close database connections
  await db.close()

  // Close server
  server.close(() => {
    console.log('Server closed')
    process.exit(0)
  })

  // Force exit after 10s
  setTimeout(() => {
    console.error('Forced shutdown after timeout')
    process.exit(1)
  }, 10000)
}

process.on('SIGTERM', gracefulShutdown)
process.on('SIGINT', gracefulShutdown)
```

### Common Patterns

**Static file serving:**
```js
const express = require('express')
const path = require('path')

app.use(express.static(path.join(__dirname, 'public')))
```

**CORS configuration:**
```js
const cors = require('cors')

app.use(cors({
  origin: process.env.FRONTEND_URL || '*',
  credentials: true
}))
```

---

## RedwoodJS

### Prerequisites

RedwoodJS requires both API and Web sides to be deployed.

### Dockerfile for RedwoodJS

RedwoodJS provides official Dockerfile generation:

```bash
yarn rw setup deploy fly
```

This creates:
- `Dockerfile` - Multi-stage build for API and Web
- `fly.toml` - Basic configuration
- `.dockerignore` - Optimized for Redwood

See `assets/dockerfiles/redwood.Dockerfile` for reference template.

### fly.toml for RedwoodJS

```toml
app = "my-redwood-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "8910"

[http_service]
  internal_port = 8910
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/"

[[vm]]
  memory = "512mb"  # RedwoodJS needs more memory
  cpus = 1

[deploy]
  release_command = "yarn rw prisma migrate deploy"
```

### Database Setup

RedwoodJS uses Prisma. After attaching Postgres:

```bash
# Attach database
fly postgres attach <postgres-app-name>

# Deploy migrations
fly deploy
```

The `release_command` automatically runs migrations before deployment.

### Environment Variables

**redwood.toml:**
```toml
[web]
  title = "My Redwood App"
  port = 8910
  apiUrl = "/.redwood/functions"

[api]
  port = 8911
```

**fly secrets:**
```bash
fly secrets set DATABASE_URL=postgres://...
fly secrets set SESSION_SECRET=$(openssl rand -hex 32)
```

### Common Issues

**Prisma generate fails:**
- Ensure `prisma generate` runs in Dockerfile
- Check DATABASE_URL is set

**GraphQL endpoint 404:**
- Verify API is built and served
- Check apiUrl in redwood.toml

---

## General Node.js Best Practices

### .dockerignore

Always include:
```
node_modules
npm-debug.log
.git
.env
.DS_Store
dist
build
coverage
.next
```

### Package Management

**Using npm:**
```dockerfile
COPY package*.json ./
RUN npm ci --only=production
```

**Using yarn:**
```dockerfile
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --production
```

**Using pnpm:**
```dockerfile
RUN npm install -g pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod
```

### Performance Tips

1. **Multi-stage builds** - Separate build and runtime stages
2. **Layer caching** - Copy package files before source code
3. **Minimal base image** - Use `node:20-alpine` for smaller images
4. **Production mode** - Always set `NODE_ENV=production`
5. **Memory limits** - Monitor and adjust based on actual usage

### Monitoring

Check memory usage:
```bash
fly ssh console -C "free -m"
```

Check Node.js process:
```bash
fly ssh console -C "ps aux | grep node"
```
