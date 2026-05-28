# Deployment Patterns

Containerization, hosting, and production deployment for framework agents.

## Docker Configuration

### Basic Dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Build TypeScript
RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Run
CMD ["node", "dist/index.js"]
```

### Multi-Stage Build (Smaller Image)

```dockerfile
# Build stage
FROM node:22-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:22-alpine AS production

WORKDIR /app

# Copy only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built files
COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Docker Compose

```yaml
version: "3.8"

services:
  research-agent:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./data:/app/data  # For SQLite if used
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=mastra
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=research_agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Environment Configuration

### .env File

```bash
# Server
NODE_ENV=production
PORT=3000

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/research_agent

# Storage
LIBSQL_URL=file:./data/mastra.db

# Authentication
API_TOKEN=your-api-token
JWT_SECRET=your-jwt-secret

# Optional: Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

### Environment Validation

```typescript
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.string().transform(Number).default("3000"),
  OPENAI_API_KEY: z.string().min(1),
  DATABASE_URL: z.string().optional(),
  API_TOKEN: z.string().min(20),
});

// Validate at startup
const env = EnvSchema.parse(process.env);
```

## Cloud Deployment

### Railway

```toml
# railway.toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

### Fly.io

```toml
# fly.toml
app = "research-agent"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services.http_checks]]
  interval = "15s"
  timeout = "2s"
  path = "/health"
```

```bash
# Deploy
fly deploy
fly secrets set OPENAI_API_KEY=sk-...
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: research-agent
    env: docker
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
    envVars:
      - key: NODE_ENV
        value: production
      - key: OPENAI_API_KEY
        sync: false  # Set in dashboard
```

## Database Setup

### PostgreSQL with pgvector

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
  id TEXT PRIMARY KEY,
  vector vector(1536),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX ON embeddings USING ivfflat (vector vector_cosine_ops)
WITH (lists = 100);
```

### SQLite (LibSQL) for Simple Deployments

```typescript
import { LibSQLStore } from "@mastra/libsql";

const storage = new LibSQLStore({
  url: process.env.LIBSQL_URL || "file:./data/mastra.db",
});
```

## Scaling Patterns

### Horizontal Scaling

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: research-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: research-agent
  template:
    metadata:
      labels:
        app: research-agent
    spec:
      containers:
      - name: research-agent
        image: research-agent:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Connection Pooling

```typescript
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,  // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

## Monitoring

### Health Endpoints

```typescript
registerApiRoute("/health", {
  method: "GET",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const checks: Record<string, string> = {};

    // Check storage
    try {
      await mastra.storage?.getThreads({ limit: 1 });
      checks.storage = "healthy";
    } catch {
      checks.storage = "unhealthy";
    }

    // Check vector store
    try {
      await mastra.vectors?.default.query({
        indexName: "test",
        queryVector: new Array(1536).fill(0),
        topK: 1,
      });
      checks.vectors = "healthy";
    } catch {
      checks.vectors = "unhealthy";
    }

    const allHealthy = Object.values(checks).every(v => v === "healthy");

    return c.json({
      status: allHealthy ? "healthy" : "degraded",
      checks,
      timestamp: new Date().toISOString(),
    }, allHealthy ? 200 : 503);
  },
});

registerApiRoute("/ready", {
  method: "GET",
  handler: async (c) => {
    return c.json({ ready: true });
  },
});
```

### Logging

```typescript
import { logger } from "hono/logger";

// Request logging
app.use("*", logger());

// Custom structured logging
const log = (level: string, message: string, data?: Record<string, unknown>) => {
  console.log(JSON.stringify({
    level,
    message,
    timestamp: new Date().toISOString(),
    ...data,
  }));
};
```

### Metrics

```typescript
// Simple request metrics
const metrics = {
  requests: 0,
  errors: 0,
  latencies: [] as number[],
};

app.use("*", async (c, next) => {
  const start = Date.now();
  metrics.requests++;

  try {
    await next();
  } catch (err) {
    metrics.errors++;
    throw err;
  } finally {
    metrics.latencies.push(Date.now() - start);
    if (metrics.latencies.length > 1000) {
      metrics.latencies = metrics.latencies.slice(-100);
    }
  }
});

registerApiRoute("/metrics", {
  method: "GET",
  handler: (c) => {
    const avgLatency = metrics.latencies.length
      ? metrics.latencies.reduce((a, b) => a + b, 0) / metrics.latencies.length
      : 0;

    return c.json({
      totalRequests: metrics.requests,
      totalErrors: metrics.errors,
      errorRate: metrics.requests ? metrics.errors / metrics.requests : 0,
      avgLatencyMs: avgLatency,
      p99LatencyMs: metrics.latencies.sort((a, b) => b - a)[0] || 0,
    });
  },
});
```

## Security

### Rate Limiting

```typescript
const rateLimits = new Map<string, { count: number; resetAt: number }>();

app.use("/api/*", async (c, next) => {
  const ip = c.req.header("x-forwarded-for") || "unknown";
  const now = Date.now();
  const limit = rateLimits.get(ip);

  if (limit && now < limit.resetAt) {
    if (limit.count >= 100) {  // 100 requests per minute
      return c.json({
        error: "Rate limit exceeded",
        retryAfter: Math.ceil((limit.resetAt - now) / 1000),
      }, 429);
    }
    limit.count++;
  } else {
    rateLimits.set(ip, { count: 1, resetAt: now + 60000 });
  }

  await next();
});
```

### CORS

```typescript
import { cors } from "hono/cors";

app.use("*", cors({
  origin: process.env.ALLOWED_ORIGINS?.split(",") || ["http://localhost:3000"],
  allowMethods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization", "X-User-Id"],
  maxAge: 86400,
}));
```

### Input Sanitization

```typescript
// Always validate with Zod
const sanitizedInput = InputSchema.parse(body);

// Limit input sizes
app.use("*", async (c, next) => {
  const contentLength = c.req.header("content-length");
  if (contentLength && parseInt(contentLength) > 1_000_000) {
    return c.json({ error: "Request too large" }, 413);
  }
  await next();
});
```

## Graceful Shutdown

```typescript
import { serve } from "@hono/node-server";

const server = serve({
  fetch: app.fetch,
  port: parseInt(process.env.PORT || "3000"),
});

// Handle shutdown signals
const shutdown = async () => {
  console.log("Shutting down gracefully...");

  // Stop accepting new requests
  server.close();

  // Close database connections
  await pool?.end();

  // Allow in-flight requests to complete
  await new Promise(r => setTimeout(r, 5000));

  process.exit(0);
};

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
```
