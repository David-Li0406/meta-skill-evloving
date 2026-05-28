<overview>
Deploy Next.js 16 with Docker for full control over infrastructure. Works with any cloud provider or Kubernetes.
</overview>

<dockerfile>
**Optimized multi-stage Dockerfile:**

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED=1

# Build application
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```
</dockerfile>

<config>
**Enable standalone output:**

```typescript
// next.config.ts
const nextConfig = {
  output: 'standalone',
}

export default nextConfig
```

**Install sharp for image optimization:**
```dockerfile
# Add to builder stage
RUN npm install sharp
```
</config>

<build_run>
**Build image:**
```bash
docker build -t my-nextjs-app .
```

**Run container:**
```bash
docker run -p 3000:3000 \
  -e DATABASE_URL="postgresql://..." \
  -e AUTH_SECRET="..." \
  my-nextjs-app
```

**With environment file:**
```bash
docker run -p 3000:3000 --env-file .env.production my-nextjs-app
```
</build_run>

<docker_compose>
**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - AUTH_SECRET=${AUTH_SECRET}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

**Run:**
```bash
docker-compose up -d
```
</docker_compose>

<ci_cd>
**GitHub Actions example:**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```
</ci_cd>

<kubernetes>
**Kubernetes deployment:**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nextjs-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nextjs-app
  template:
    metadata:
      labels:
        app: nextjs-app
    spec:
      containers:
        - name: nextjs-app
          image: ghcr.io/myorg/my-nextjs-app:latest
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20

---
apiVersion: v1
kind: Service
metadata:
  name: nextjs-app
spec:
  selector:
    app: nextjs-app
  ports:
    - port: 80
      targetPort: 3000
  type: LoadBalancer
```
</kubernetes>

<health_check>
**Add health check endpoint:**

```typescript
// app/api/health/route.ts
export async function GET() {
  try {
    // Optional: check database connection
    // await db.$queryRaw`SELECT 1`

    return Response.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    return Response.json(
      { status: 'error', message: 'Health check failed' },
      { status: 500 }
    )
  }
}
```
</health_check>

<optimization>
**Reduce image size:**

1. Use Alpine base image (done in example)
2. Multi-stage builds (done in example)
3. Use standalone output (done in example)
4. Exclude dev dependencies

**Cache layers effectively:**
```dockerfile
# Copy package files first (changes less often)
COPY package.json package-lock.json* ./
RUN npm ci

# Then copy source (changes more often)
COPY . .
RUN npm run build
```

**Security hardening:**
```dockerfile
# Use non-root user (done in example)
# Remove build tools in production
# Use read-only filesystem where possible
```
</optimization>

<troubleshooting>
**Image too large?**
- Check you're using multi-stage builds
- Ensure `output: 'standalone'` is set
- Don't copy node_modules to final stage

**Build fails?**
- Run build locally first: `npm run build`
- Check Docker has enough memory
- Verify environment variables are available

**Runtime errors?**
- Check environment variables are passed to container
- Verify database connectivity
- Check logs: `docker logs <container-id>`
</troubleshooting>
