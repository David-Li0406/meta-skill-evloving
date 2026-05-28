---
name: local-dev-evaluator
description: Evaluate local development experience for any stack. Use when user asks about local dev setup, docker-compose vs kubernetes, or developer experience for a technology stack.
---

# Local Dev Experience Evaluator

Evaluate and recommend the best local development approach for any stack.

## Standalone Usage

Can be invoked directly:
- "How do I run this stack locally?"
- "Should I use docker-compose or local k8s?"
- "Evaluate local dev experience for Next.js + Supabase"

## Assumptions

- Docker Desktop is available
- Local Kubernetes is available (Docker Desktop K8s, minikube, kind, or k3s)

## Available Approaches

| Approach | When to Use | Complexity |
|----------|-------------|------------|
| **docker-compose** | Simple apps, all deps containerized | Low |
| **local-k8s** | K8s-native apps, need K8s features | Medium |
| **hybrid** | Complex apps: deps in compose, services in k8s | Medium-High |
| **aspire** | .NET distributed apps | Medium |
| **native** | Simple apps, few deps | Very Low |

### When to Use Each

**docker-compose**:
- Web app + database + cache
- Microservices with < 5 services
- No K8s-specific features needed
- Team familiar with Docker

**local-k8s**:
- Using K8s-specific features (ConfigMaps, Services, Ingress)
- Deploying to K8s in production
- Need to test K8s manifests locally
- Using Helm charts

**hybrid**:
- Complex microservices architecture
- Heavy stateful deps (databases) in compose
- Stateless services in K8s
- Need both simplicity and K8s testing

**aspire**:
- .NET distributed applications
- Need unified observability dashboard
- Code-first infrastructure definition
- Multiple .NET services

**native**:
- Single service with minimal deps
- Using local SQLite or in-memory
- Frontend-only development
- Rapid iteration priority

## Evaluation Criteria

### Time to First Run

| Rating | Time | Description |
|--------|------|-------------|
| Excellent | < 5 min | `git clone && docker-compose up` |
| Good | 5-15 min | Multiple steps, some build time |
| Fair | 15-30 min | Complex setup, many deps |
| Poor | > 30 min | Manual steps, external deps |

### Dependency Complexity

| Level | Containers | Description |
|-------|------------|-------------|
| Low | 1-3 | Standard images (postgres, redis) |
| Medium | 4-6 | Some custom config |
| High | 7+ | Complex networking, custom builds |

### Production Parity

| Area | Full | Partial | None |
|------|------|---------|------|
| **Auth** | Same provider | Mock/simplified | Disabled |
| **Data** | Same DB + migrations | Same DB + seed | Different DB |
| **Async** | Same queue/events | Local queue | Sync only |
| **Config** | Same config system | .env files | Hardcoded |

## Output Contract

```yaml
local_dev_evaluation:
  stack: "<stack description>"

  recommended_approach: "<docker-compose|local-k8s|hybrid|aspire|native>"

  time_to_first_run: "<excellent|good|fair|poor>"
  estimated_minutes: <N>

  dependency_complexity: "<low|medium|high>"
  container_count: <N>

  prod_parity:
    auth: "<full|partial|none>"
    data: "<full|partial|none>"
    async: "<full|partial|none>"
    config: "<full|partial|none>"
    overall: "<high|medium|low>"

  debugging_support: "<excellent|good|fair|poor>"
  dev_observability: "<excellent|good|fair|poor>"

  dx_score: <1-5>

  setup_steps:
    - step: "<step name>"
      command: "<command>"

  files_needed:
    - "<file 1>"
    - "<file 2>"

  notes:
    - "<important consideration>"

  recommendations:
    - "<recommendation>"
```

## Example: Next.js + Supabase

```yaml
local_dev_evaluation:
  stack: "Next.js + Supabase"

  recommended_approach: "native"

  time_to_first_run: "excellent"
  estimated_minutes: 3

  dependency_complexity: "low"
  container_count: 1  # Supabase CLI runs all-in-one

  prod_parity:
    auth: "full"
    data: "full"
    async: "full"
    config: "partial"
    overall: "high"

  debugging_support: "excellent"
  dev_observability: "good"

  dx_score: 5

  setup_steps:
    - step: "Install Supabase CLI"
      command: "brew install supabase/tap/supabase"
    - step: "Start local Supabase"
      command: "supabase start"
    - step: "Start Next.js"
      command: "npm run dev"

  notes:
    - "Supabase CLI includes: PostgreSQL, Auth, Storage, Edge Functions"
    - "Studio UI available at localhost:54323"
```

## Example: EKS + Aurora

```yaml
local_dev_evaluation:
  stack: "React + Node.js API + Aurora PostgreSQL"

  recommended_approach: "docker-compose"

  time_to_first_run: "good"
  estimated_minutes: 10

  dependency_complexity: "medium"
  container_count: 4  # frontend, api, postgres, redis

  prod_parity:
    auth: "partial"  # Local JWT vs Cognito
    data: "full"     # Same PostgreSQL
    async: "partial" # Local Redis vs ElastiCache
    config: "partial"
    overall: "medium"

  dx_score: 4

  setup_steps:
    - step: "Copy environment"
      command: "cp .env.example .env.local"
    - step: "Start services"
      command: "docker-compose up -d"
    - step: "Run migrations"
      command: "npm run db:migrate"
    - step: "Start dev server"
      command: "npm run dev"

  files_needed:
    - "docker-compose.yml"
    - ".env.example"
    - "docker-compose.override.yml (optional)"
```

## Scoring Guide

| DX Score | Criteria |
|----------|----------|
| 5 | < 5 min, low complexity, high parity, excellent debugging |
| 4 | 5-15 min, low-medium complexity, good parity |
| 3 | 15-30 min, medium complexity, partial parity |
| 2 | > 30 min, high complexity, limited parity |
| 1 | Complex manual setup, poor parity, difficult debugging |
