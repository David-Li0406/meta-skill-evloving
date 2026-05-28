---
name: local-dev-plan
description: Generate a local development environment plan for any stack. Use when user asks for local dev setup instructions, docker-compose configuration, or how to run a stack locally.
---

# Local Development Environment Plan Generator

Generate a complete local development environment plan including orchestration, dependencies, and quick start guide.

## Standalone Usage

Can be invoked directly:
- "Create a local dev setup for my React + PostgreSQL app"
- "How should I configure docker-compose for this stack?"
- "Generate local development instructions for Next.js + Supabase"

## Assumptions

- Docker Desktop is available
- Local Kubernetes is available (optional)

## Plan Structure

### 1. Orchestration Mode Selection

Choose based on stack complexity:

| Mode | When to Use |
|------|-------------|
| docker-compose | Most apps, < 6 services |
| local-k8s | K8s-native, need K8s features |
| hybrid | Complex: deps in compose, services in k8s |
| aspire | .NET distributed apps |
| native | Simple apps, minimal deps |

### 2. Dependencies Setup

For each dependency (database, cache, queue, storage):
- Container image
- Port mappings
- Volume configuration
- Health checks
- Environment variables

### 3. Quick Start Guide

Step-by-step commands to go from clone to running.

## Output Contract

```yaml
local_dev_plan:
  stack: "<stack description>"
  orchestration_mode: "<docker-compose|local-k8s|hybrid|aspire|native>"

  prerequisites:
    - "<prerequisite 1>"
    - "<prerequisite 2>"

  dependencies:
    database:
      service_name: "<name>"
      image: "<docker image>"
      ports:
        - "<host:container>"
      volumes:
        - "<volume mapping>"
      environment:
        - "<VAR=value>"
      healthcheck:
        test: "<command>"
        interval: "10s"
        retries: 5

    cache:
      service_name: "<name>"
      image: "<image>"
      ports: []

    queue:
      service_name: "<name>"
      image: "<image>"
      ports: []

    storage:
      solution: "<minio|localstack|none>"
      configuration: "<details>"

  config_files:
    - filename: "docker-compose.yml"
      content: |
        <full docker-compose content>

    - filename: ".env.example"
      content: |
        <environment template>

    - filename: "docker-compose.override.yml"
      description: "Local overrides (optional)"
      content: |
        <override content>

  migrations:
    tool: "<prisma|knex|flyway|ef-core|other>"
    commands:
      run: "<migration command>"
      seed: "<seed command>"
      reset: "<reset command>"

  secrets_strategy:
    approach: "<.env files|local vault|config files>"
    files:
      - ".env.example (committed)"
      - ".env.local (gitignored)"
    notes: "<how to manage secrets>"

  observability:
    logging: "<approach>"
    tracing: "<optional local jaeger>"
    dashboard: "<aspire dashboard if applicable>"

  prod_parity:
    - area: "Auth"
      local: "<local approach>"
      prod: "<prod approach>"
      gap: "<what differs>"
    - area: "Data"
      local: "<local approach>"
      prod: "<prod approach>"
      gap: "<what differs>"

  quick_start:
    estimated_time: "<X minutes>"
    steps:
      - name: "Clone repository"
        command: "git clone <repo> && cd <repo>"
      - name: "Copy environment"
        command: "cp .env.example .env.local"
      - name: "Start dependencies"
        command: "<docker-compose up -d>"
      - name: "Run migrations"
        command: "<migration command>"
      - name: "Seed data (optional)"
        command: "<seed command>"
      - name: "Start application"
        command: "<npm run dev | dotnet run>"
      - name: "Verify"
        command: "curl http://localhost:<port>/health"

  troubleshooting:
    - issue: "Port already in use"
      solution: "Change port in docker-compose.override.yml"
    - issue: "Database connection refused"
      solution: "Wait for healthcheck, check docker-compose logs"
```

## Docker Compose Template

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-dev}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-dev}
      POSTGRES_DB: ${DB_NAME:-app}
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${DB_USER:-dev}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "${REDIS_PORT:-6379}:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      retries: 3

  # Optional: Local S3-compatible storage
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD:-minioadmin}
    ports:
      - "${MINIO_PORT:-9000}:9000"
      - "${MINIO_CONSOLE:-9001}:9001"
    volumes:
      - minio-data:/data

volumes:
  db-data:
  minio-data:
```

## Environment Template

```bash
# .env.example
# Copy to .env.local and fill in values

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=dev
DB_PASSWORD=dev
DB_NAME=app
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}

# Storage (Minio)
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=app-uploads

# App
NODE_ENV=development
PORT=3000
```

## Aspire AppHost Example

```csharp
var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddPostgres("postgres")
    .WithPgAdmin()
    .AddDatabase("appdb");

var redis = builder.AddRedis("cache")
    .WithRedisCommander();

builder.AddProject<Projects.Api>("api")
    .WithReference(postgres)
    .WithReference(redis)
    .WithExternalHttpEndpoints();

builder.AddNpmApp("frontend", "../frontend")
    .WithReference(builder.GetProject("api"))
    .WithHttpEndpoint(3000);

builder.Build().Run();
```

## Common Patterns

### Next.js + Supabase
```yaml
orchestration_mode: native
dependencies:
  database:
    solution: "Supabase CLI"
    command: "supabase start"
quick_start:
  - "supabase start"
  - "npm run dev"
```

### React + Node + PostgreSQL
```yaml
orchestration_mode: docker-compose
dependencies:
  database: postgres:16-alpine
  cache: redis:7-alpine
quick_start:
  - "docker-compose up -d"
  - "npm run migrate"
  - "npm run dev"
```

### .NET Microservices
```yaml
orchestration_mode: aspire
quick_start:
  - "dotnet run --project AppHost"
```
