---
name: cost-vercel
description: Estimate Vercel costs for any project using live pricing data. Use when user asks about Vercel pricing, Next.js hosting costs, or edge deployment costs.
---

# Vercel Cost Evaluator

Estimate costs for Vercel-based projects using current pricing data.

## Before Answering Vercel Cost Questions

**IMPORTANT**: Always verify tool availability before providing cost estimates.

### Step 1: Check Available Tools

Check if the following tools are available:

**Vercel CLI** (preferred):
- `vercel` CLI for project information
- `vercel ls` - List deployments
- `vercel project ls` - List projects

**Vercel API**:
- REST API for project and usage info

### Step 2: If Tools Are Unavailable

If Vercel CLI is not accessible, help the user set them up:

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# List projects
vercel project ls

# Get project info
vercel inspect <deployment-url>
```

**Option B: Vercel API**
```bash
# Get access token from dashboard
# https://vercel.com/account/tokens

# List projects
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v9/projects"

# Get project usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage"

# Get team usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/teams/TEAM_ID/usage"
```

Ask the user which option fits their environment before proceeding.

### Step 3: Fallback to Web Search

If no tools are available and user cannot install them, use web search to fetch current pricing from:
- https://vercel.com/pricing
- https://vercel.com/docs/limits/overview

## How to Get Live Pricing

### Using Vercel CLI

```bash
# List all projects
vercel project ls

# Get deployment details
vercel ls
vercel inspect DEPLOYMENT_URL

# Check current usage (requires dashboard)
vercel open  # Opens dashboard
```

### Using Vercel API

```bash
# Get account/team usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage"

# Response includes:
# - bandwidth (bytes)
# - serverlessFunctionExecution (gb-hours)
# - edgeFunctionInvocations
# - imageOptimization
# - builds

# Get specific project usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v9/projects/PROJECT_ID"

# List team members (for seat count)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v2/teams/TEAM_ID/members"
```

### Using Vercel Dashboard API

```bash
# Get billing information
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/billing"

# Get invoices
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/billing/invoices"
```

## Standalone Usage

Can be invoked directly for cost estimation:
- "How much does Vercel Pro cost for 5 developers?"
- "Estimate Vercel costs for a Next.js app"
- "What's included in Vercel free tier?"

## Cost Estimation Process

1. **Identify tier** needed (Hobby/Pro/Enterprise)
2. **Count team members** for seat pricing
3. **Query current pricing** using available tools
4. **Estimate usage** (bandwidth, functions, etc.)
5. **Calculate overages** above included limits
6. **Factor in add-ons** (Postgres, KV, Blob)

## Pricing Structure (Query for Current Values)

### Tier Information

| Tier | Query Method |
|------|-------------|
| Hobby | `vercel.com/pricing` |
| Pro | API: `/v1/billing` or web |
| Enterprise | Contact sales |

### Usage Metrics (Query via API)

| Metric | API Endpoint |
|--------|-------------|
| Bandwidth | `GET /v1/usage` → bandwidth |
| Function Execution | `GET /v1/usage` → serverlessFunctionExecution |
| Edge Invocations | `GET /v1/usage` → edgeFunctionInvocations |
| Image Optimization | `GET /v1/usage` → imageOptimization |
| Build Minutes | `GET /v1/usage` → builds |

### Get Current Usage

```bash
# Get overall usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage"

# Get usage by project
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage?projectId=PROJECT_ID"

# Get usage for time period
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage?from=2024-01-01&to=2024-01-31"
```

## Output Contract

```yaml
vercel_cost_estimate:
  description: "<what's being estimated>"
  pricing_source: "<cli|api|web>"
  pricing_date: "<when pricing was fetched>"

  recommended_tier: "<hobby|pro|enterprise>"
  team_size: <N>

  tier_details:
    name: "<tier name>"
    seat_price: "<$X/user/mo>"
    included:
      bandwidth_gb: <N>
      function_gb_hours: <N>
      edge_invocations: <N>
      image_optimizations: <N>

  usage_estimate:
    bandwidth_gb: <N>
    function_gb_hours: <N>
    edge_invocations: <N>

  baseline_monthly:
    seats: "<$X>"
    bandwidth_overage: "<$X>"
    functions_overage: "<$X>"
    edge_functions: "<$X>"
    storage_services: "<$X>"
    total: "<$X>"

  at_10x_scale:
    seats: "<$X>"
    overages: "<$X>"
    total: "<$X>"

  included_features:
    - "Global edge network (CDN)"
    - "Automatic HTTPS"
    - "Preview deployments"
    - "Serverless functions"
    - "Edge functions"
    - "Git integration"
    - "Instant rollbacks"

  warnings:
    - "<warning if applicable>"

  optimization_tips:
    - "<tip 1>"
    - "<tip 2>"
```

## Cost Optimization Strategies

### Monitor Usage via API

```bash
# Set up usage monitoring
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage"

# Check usage trends
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/usage?from=$(date -d '30 days ago' +%Y-%m-%d)"

# Get per-project breakdown
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v9/projects" | jq '.projects[].name'
```

### Optimize Bandwidth

```bash
# Check bandwidth by deployment
vercel ls --all

# Review large deployments
vercel inspect DEPLOYMENT_URL
```

```javascript
// In next.config.js - optimize images
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
}
```

### Optimize Functions

```javascript
// Use Edge Runtime for simple functions (cheaper)
export const config = {
  runtime: 'edge',
}

// Use ISR to reduce function calls
export async function getStaticProps() {
  return {
    props: { data },
    revalidate: 60, // Regenerate every 60 seconds
  }
}
```

### Use Static Generation

```javascript
// Prefer static pages (no function cost)
export async function generateStaticParams() {
  // Pre-render pages at build time
  return posts.map((post) => ({
    slug: post.slug,
  }))
}
```

## Vercel Add-on Services

Query pricing for add-ons:

```bash
# Vercel Postgres
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/storage/postgres"

# Vercel KV
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/storage/kv"

# Vercel Blob
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.vercel.com/v1/storage/blob"
```

## Vercel Considerations

**Strengths**:
- Zero-config deployment for Next.js
- Global edge network
- Preview deployments for every PR
- Excellent DX

**Watch out for**:
- Per-seat pricing adds up for larger teams
- Bandwidth overages can be expensive
- Function execution time affects cost
- Hobby tier is non-commercial only

## Vercel vs Alternatives

When comparing costs:
- **vs AWS (CloudFront + Lambda)**: Use `cost-aws` - often cheaper at scale but more complex
- **vs GCP (Cloud Run)**: Use `cost-gcp` - good middle ground
- **vs Netlify**: Similar model, compare specific features
- Consider total cost including team seats for large teams
