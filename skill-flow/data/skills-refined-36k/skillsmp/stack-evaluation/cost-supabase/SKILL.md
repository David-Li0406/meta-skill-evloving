---
name: cost-supabase
description: Estimate Supabase costs for any project using live pricing data. Use when user asks about Supabase pricing, BaaS costs, or PostgreSQL-based backend costs.
---

# Supabase Cost Evaluator

Estimate costs for Supabase-based projects using current pricing data.

## Before Answering Supabase Cost Questions

**IMPORTANT**: Always verify tool availability before providing cost estimates.

### Step 1: Check Available Tools

Check if the following tools are available:

**Supabase CLI** (preferred):
- `supabase` CLI for project information
- `supabase projects list` - List projects
- `supabase orgs list` - List organizations

**Supabase Management API**:
- REST API for project and billing info

### Step 2: If Tools Are Unavailable

If Supabase CLI is not accessible, help the user set it up:

**Option A: Supabase CLI**
```bash
# Install Supabase CLI
# macOS
brew install supabase/tap/supabase

# npm
npm install -g supabase

# Login
supabase login
```

**Option B: Supabase Management API**
```bash
# Get access token from dashboard
# https://supabase.com/dashboard/account/tokens

# List projects
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects"

# Get project details (includes usage)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF"
```

Ask the user which option fits their environment before proceeding.

### Step 3: Fallback to Web Search

If no tools are available and user cannot install them, use web search to fetch current pricing from:
- https://supabase.com/pricing
- https://supabase.com/docs/guides/platform/billing

## How to Get Live Pricing

### Using Supabase CLI

```bash
# List all projects
supabase projects list

# Get project status (includes some usage info)
supabase status

# Link to project for detailed info
supabase link --project-ref YOUR_PROJECT_REF
```

### Using Supabase Management API

```bash
# Get organization billing
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/organizations/ORG_ID/billing"

# Get project usage
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF/usage"

# Get subscription details
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF/subscription"
```

### Using Web Scrape (Fallback)

Fetch current pricing from Supabase pricing page:
- https://supabase.com/pricing

## Standalone Usage

Can be invoked directly for cost estimation:
- "How much does Supabase Pro cost?"
- "Estimate Supabase costs for 50k users"
- "What's included in Supabase free tier?"

## Cost Estimation Process

1. **Identify tier** needed based on requirements
2. **Query current pricing** using available tools
3. **Calculate add-ons** based on expected usage
4. **Estimate at scale** (10x baseline)
5. **Compare** to alternatives if needed

## Pricing Structure (Query for Current Values)

### Tier Information

| Tier | Query Method |
|------|-------------|
| Free | `supabase.com/pricing` or API |
| Pro | `supabase.com/pricing` or API |
| Team | `supabase.com/pricing` or API |
| Enterprise | Contact sales |

### Usage-Based Add-ons

| Resource | Query Method |
|----------|-------------|
| Compute | API: `/projects/{ref}/usage` |
| Database Storage | API: `/projects/{ref}/usage` |
| File Storage | API: `/projects/{ref}/usage` |
| Bandwidth | API: `/projects/{ref}/usage` |
| Edge Functions | API: `/projects/{ref}/usage` |

### Get Current Usage

```bash
# Via API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF/usage"

# Response includes:
# - database_size_bytes
# - storage_size_bytes
# - bandwidth_bytes
# - function_invocations
# - mau (monthly active users)
```

## Output Contract

```yaml
supabase_cost_estimate:
  description: "<what's being estimated>"
  pricing_source: "<cli|api|web>"
  pricing_date: "<when pricing was fetched>"

  recommended_tier: "<free|pro|team|enterprise>"

  tier_details:
    name: "<tier name>"
    base_price: "<$X/mo>"
    included:
      database_gb: <N>
      storage_gb: <N>
      bandwidth_gb: <N>
      mau: <N>
      edge_function_invocations: <N>

  usage_estimate:
    database_gb: <N>
    storage_gb: <N>
    bandwidth_gb: <N>
    mau: <N>

  baseline_monthly:
    tier_base: "<$X>"
    compute_addon: "<$X>"
    database_addon: "<$X>"
    storage_addon: "<$X>"
    bandwidth_addon: "<$X>"
    other_addons: "<$X>"
    total: "<$X>"

  at_10x_scale:
    tier: "<$X>"
    addons: "<$X>"
    total: "<$X>"

  included_features:
    - "PostgreSQL database"
    - "Auth (email, OAuth, magic link, phone)"
    - "Realtime subscriptions"
    - "Edge Functions (Deno)"
    - "Storage (S3-compatible)"
    - "Vector embeddings (pgvector)"
    - "Auto-generated APIs"

  optimization_tips:
    - "<tip 1>"
    - "<tip 2>"
```

## Cost Optimization Strategies

### Monitor Usage via API

```bash
# Set up usage monitoring
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF/usage"

# Check daily stats
# Dashboard: https://supabase.com/dashboard/project/_/reports
```

### Optimize Database

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size(current_database()));

-- Find large tables
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Enable connection pooling (PgBouncer)
-- Use transaction mode for serverless
```

### Optimize Storage

```bash
# List storage buckets and sizes via API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.supabase.com/v1/projects/PROJECT_REF/storage/buckets"
```

## Supabase vs Alternatives

When comparing costs:
- **vs Firebase**: Supabase often cheaper for SQL-heavy workloads
- **vs AWS (RDS + Cognito + S3)**: Supabase simpler, often cheaper at small scale
- **vs PlanetScale + Clerk**: Compare feature sets, Supabase is all-in-one

## Self-Hosting Option

For very large scale, consider self-hosting:
```bash
# Self-hosted Supabase
git clone https://github.com/supabase/supabase
cd supabase/docker
docker compose up
```

Costs shift to infrastructure (compute, storage) instead of Supabase fees.
