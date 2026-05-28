---
name: candidate-generator
description: Generate coherent stack candidates based on requirements. Use when user needs stack options, technology recommendations, or architecture patterns for their project.
---

# Stack Candidate Generator

Generate 2-5 coherent stack candidates based on project requirements.

## Standalone Usage

Can be invoked directly:
- "Suggest stack options for a SaaS application"
- "What are good tech stacks for a real-time chat app?"
- "Generate architecture options for an e-commerce platform"

## Common Stack Patterns

### Serverless / Low-Ops

| Pattern | Best For |
|---------|----------|
| Next.js + Vercel + Supabase | Frontend-heavy, rapid development |
| React + AWS Amplify + Aurora Serverless | AWS-native, full-stack |
| React + Firebase | Real-time features, Google ecosystem |
| React + Supabase | PostgreSQL-centric, open-source |

### Container-Based / Balanced

| Pattern | Best For |
|---------|----------|
| React + AWS App Runner + RDS | AWS containers, moderate control |
| React + Cloud Run + Cloud SQL | GCP containers, simple scaling |
| Next.js + AWS ECS + Aurora | Full control, AWS ecosystem |
| React + Azure Container Apps + Azure SQL | Microsoft ecosystem |

### Kubernetes / Full Control

| Pattern | Best For |
|---------|----------|
| React + EKS + Aurora | AWS K8s, enterprise scale |
| React + GKE + Cloud SQL | GCP K8s, cost-effective |
| React + AKS + Azure SQL | Azure K8s, enterprise |

### Enterprise / .NET

| Pattern | Best For |
|---------|----------|
| Blazor + Azure App Service + Azure SQL | Microsoft full-stack |
| React + .NET API + SQL Server | Enterprise, existing .NET |
| .NET + Aspire + Azure | Distributed, orchestrated |

## Required Components

Each candidate must specify:

1. **Frontend** - Framework and hosting
2. **Backend/API** - Runtime and hosting
3. **Database** - Technology and managed/self-hosted
4. **Authentication** - Provider/solution
5. **Hosting Model** - Platform and strategy
6. **Local Dev Story** - How to run locally

## Selection Criteria

When generating candidates, consider:

| Requirement | Low Budget | Growth | Scale |
|-------------|------------|--------|-------|
| Compute | Serverless | Containers | K8s |
| Database | Managed serverless | Managed provisioned | Managed/dedicated |
| Ops maturity needed | Low | Medium | High |
| Local dev complexity | Low | Medium | Medium-High |

### By Ops Maturity

- **Low**: Firebase, Supabase, Vercel, Amplify
- **Medium**: App Runner, Cloud Run, Container Apps
- **High**: ECS, GKE, EKS, self-managed

### By Team Size

- **Solo/Small (1-5)**: Serverless, BaaS platforms
- **Medium (6-15)**: Containers, managed K8s
- **Large (16+)**: K8s, multi-service architectures

### By Offline Requirement

| Requirement | Recommended Approach |
|-------------|---------------------|
| **None** | Standard server-centric architecture |
| **Transient** | Retry logic, in-memory queue, graceful degradation |
| **Session-Durable** | IndexedDB + service worker, background sync |
| **Strong Offline-First** | CRDT-based (Y.js, Automerge), local-first (SQLite WASM) |

## Output Contract

```yaml
candidates:
  - id: "<unique_id>"
    name: "<descriptive name>"
    summary: "<one-line summary>"

    pattern_type: "<serverless|container|kubernetes|baas>"

    components:
      frontend:
        technology: "<framework>"
        hosting: "<platform>"
      backend:
        technology: "<runtime/framework>"
        hosting: "<platform>"
      database:
        technology: "<database>"
        hosting: "<managed|serverless|self-hosted>"
      auth:
        provider: "<solution>"
      async:
        technology: "<if needed>"
      storage:
        technology: "<if needed>"

    fits:
      budget: "<minimal|startup|growth|scale|enterprise>"
      ops_maturity: "<low|medium|high>"
      team_size: "<solo|small|medium|large>"

    local_dev_story: |
      <How a developer runs this end-to-end on a laptop>

    offline_story:
      level: "<none|transient|session_durable|strong_offline_first>"
      technologies: ["<offline tech stack>"]
      notes: "<implementation considerations>"

    strengths:
      - "<strength 1>"
      - "<strength 2>"

    tradeoffs:
      - "<tradeoff 1>"
      - "<tradeoff 2>"
```

## Example Output

```yaml
candidates:
  - id: "next-vercel-supabase"
    name: "Next.js + Vercel + Supabase"
    summary: "Modern full-stack with minimal ops"

    pattern_type: "serverless"

    components:
      frontend:
        technology: "Next.js 14 (App Router)"
        hosting: "Vercel Edge"
      backend:
        technology: "Next.js API Routes + Supabase Edge Functions"
        hosting: "Vercel + Supabase"
      database:
        technology: "PostgreSQL"
        hosting: "Supabase (managed)"
      auth:
        provider: "Supabase Auth"
      storage:
        technology: "Supabase Storage"

    fits:
      budget: "startup"
      ops_maturity: "low"
      team_size: "small"

    local_dev_story: |
      1. Clone repo
      2. cp .env.example .env.local
      3. supabase start (local Supabase)
      4. npm run dev
      Full stack running in < 5 minutes

    strengths:
      - "Zero DevOps needed"
      - "Excellent DX"
      - "Built-in auth, storage, realtime"

    tradeoffs:
      - "Vendor lock-in to Vercel/Supabase"
      - "Limited compute customization"
```
