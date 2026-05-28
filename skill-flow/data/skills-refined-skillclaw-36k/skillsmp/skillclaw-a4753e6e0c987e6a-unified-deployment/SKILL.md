---
name: unified-deployment
description: Use this skill when deploying applications to Cloudflare Workers and/or Supabase Edge Functions, whether for production, publishing APIs/functions, or testing deployments on feature branches.
---

# Unified Deployment Skill

This skill handles deployment to multiple platforms:

- **Cloudflare Workers**: API application (Hono) deployment via Wrangler
- **Supabase Edge Functions**: Serverless functions (Deno) deployment via Supabase CLI
- **Both**: Deploy to both platforms simultaneously

## When to Use

- Deploying to production
- Publishing APIs or functions
- Setting up CI/CD deployments
- Testing deployments on feature branches

## Pre-deployment Checklist

### For Cloudflare Workers

Before deploying to Cloudflare, verify:

1. Environment variables in `.env`:
   - `CLOUDFLARE_API` (API token)
   - `CLOUDFLARE_ACCOUNT_ID` (Account ID)
2. `wrangler.jsonc` configuration is valid
3. Dependencies installed in `apps/api` (`bun install`)
4. Bun is installed

### For Supabase Edge Functions

Before deploying to Supabase, verify:

1. Environment variables in `.env`:
   - `SUPABASE_URL` (Project URL)
   - `SUPABASE_PROJECT_REF` (Project reference ID)
2. Supabase CLI is installed (`npm install -g supabase` or `brew install supabase/tap/supabase`)
3. Logged into Supabase CLI (`supabase login`)
4. Project is linked (script will attempt to link automatically)
5. Functions exist in `supabase/functions/` directory

## Branch-Based Deployments

The deployment skill automatically detects your git branch and deploys accordingly:

### Branch Detection

| Branch            | Environment | Description                       |
| ----------------- | ----------- | --------------------------------- |
| `main` / `master` | Production  | Deploys to production resources   |
| Any other branch  | Preview     | Creates branch-specific resources |

### Cloudflare Workers Branch Naming

Feature branches deploy to separate workers with sanitized names:

| Git Branch          | Worker Name             | URL                                           |
| ------------------- | ----------------------- | --------------------------------------------- |
| `main`              | `api`                   | `https://api.*.workers.dev`                   |
| `feature/user-auth` | `api-feature-user-auth` | `https://api-feature-user-auth.*.workers.dev` |
| `fix/login-bug`     | `api-fix-login-bug`     | `https://api-fix-login-bug.*.workers.dev`     |

**Naming Rules:**

- Max 63 characters (DNS limit)
- Only lowercase alphanumeric and hyphens