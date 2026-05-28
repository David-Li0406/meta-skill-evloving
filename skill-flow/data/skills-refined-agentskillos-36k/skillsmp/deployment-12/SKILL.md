---
name: deployment
description: Deploy applications to Cloudflare Workers and/or Supabase Edge Functions. Supports unified multi-platform deployment. Use when deploying to production, publishing APIs/functions, or when user requests deployment.
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

1. Environment variables in .env:
   - `CLOUDFLARE_API` (API token)
   - `CLOUDFLARE_ACCOUNT_ID` (Account ID)
2. `wrangler.jsonc` configuration is valid
3. Dependencies installed in `apps/api` (`bun install`)
4. Bun is installed

### For Supabase Edge Functions

Before deploying to Supabase, verify:

1. Environment variables in .env:
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
- Slashes and underscores converted to hyphens
- Leading/trailing hyphens removed

### Supabase Preview Branches

For feature branches, the script:

1. Checks if a Supabase preview branch exists
2. Prompts to create one if it doesn't
3. Deploys functions to the branch environment

**Important:** Supabase preview branches have their own:

- Project reference (different URL)
- `anon` API key
- `service_role` API key
- Isolated database

After deploying to a Supabase branch, run the following to get credentials:

```bash
supabase branches get <branch-name> --project-ref $SUPABASE_PROJECT_REF
```

### Cleanup Commands

**Delete Cloudflare Preview Worker:**

```bash
wrangler delete --name api-feature-user-auth
```

**Delete Supabase Preview Branch:**

```bash
supabase branches delete feature-user-auth --project-ref $SUPABASE_PROJECT_REF
```

### Connecting Cloudflare to Supabase Branches

When your Cloudflare Worker connects to Supabase, and you deploy to a feature branch:

1. The Cloudflare Worker deploys as `api-<branch-name>`
2. You need to update the worker's environment variables with the branch-specific Supabase credentials

**Option 1: Use Wrangler Secrets (Recommended)**

```bash
# Get branch credentials
supabase branches get feature-user-auth --project-ref $SUPABASE_PROJECT_REF

# Set secrets on branch worker
wrangler secret put SUPABASE_URL --name api-feature-user-auth
wrangler secret put SUPABASE_ANON_KEY --name api-feature-user-auth
```

**Option 2: Use separate .dev.vars files**
Create branch-specific local configuration for testing.

## Deployment Process

### Step 1: Environment Verification

- Read the .env file from project root to verify credentials exist
- Check platform-specific environment variables based on deployment target

### Step 2: Execute Deployment Script

The unified deployment script supports interactive platform selection.

Choose the appropriate script based on the user's platform:

**For Unix/Mac/Linux:**

```bash
.claude/skills/deployment/scripts/deploy.sh
```

**For Windows PowerShell:**

```powershell
.claude/skills/deployment/scripts/deploy.ps1
```

**Automated Deployment (Non-interactive):**
Set `DEPLOY_TARGET` environment variable to skip interactive prompt:

```bash
# Deploy to Cloudflare only
DEPLOY_TARGET=cloudflare .claude/skills/deployment/scripts/deploy.sh

# Deploy to Supabase only
DEPLOY_TARGET=supabase .claude/skills/deployment/scripts/deploy.sh

# Deploy to both platforms
DEPLOY_TARGET=both .claude/skills/deployment/scripts/deploy.sh
```

### Step 3: Platform Selection

If running interactively, the script will prompt:

```
Select deployment platform:
  1) Cloudflare Workers
  2) Supabase Edge Functions
  3) Both platforms

Enter choice [1-3]:
```

### Step 4: Deployment Execution

**Cloudflare Workers:**

- Navigate to `apps/api` directory
- Execute `bun run deploy`
- Deploy with Wrangler and minification
- Return deployment URL (format: `https://api.*.workers.dev`)

**Supabase Edge Functions:**

- Navigate to project root
- Link project if not already linked
- Execute `supabase functions deploy`
- Deploy all functions in `supabase/functions/`
- Return functions URL (format: `https://<ref>.supabase.co/functions/v1/`)

### Step 5: Verify Deployment Success

- Check the output for success messages
- Display deployment URLs for each platform
- Show deployment summary
- Report any errors encountered

## Error Handling

### Cloudflare Workers Errors

- **Missing .env file**: Prompt user to create `.env` with required Cloudflare variables
- **Invalid API token**: Direct user to https://dash.cloudflare.com/profile/api-tokens
  - Token needs "Workers Scripts > Edit" permission
- **Wrangler errors**: Display full error and check:
  - API token permissions
  - Account ID is correct
  - Network connectivity
- **Bun not found**: Install from https://bun.sh
- **node_modules missing**: Run `bun install` in `apps/api`

### Supabase Edge Functions Errors

- **Supabase CLI not installed**: Install via:
  - `npm install -g supabase`
  - `brew install supabase/tap/supabase` (Mac)
  - `scoop install supabase` (Windows with Scoop)
- **Not logged in**: Run `supabase login` to authenticate
- **Project not linked**: Script will attempt auto-linking with `SUPABASE_PROJECT_REF`
  - If fails, run manually: `supabase link --project-ref <ref>`
- **Missing SUPABASE_PROJECT_REF**: Add to .env file
- **Functions directory not found**: Ensure `supabase/functions/` exists with function subdirectories

## Environment Variables Reference

### Cloudflare Workers

```bash
CLOUDFLARE_API="your-api-token"
CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

### Supabase Edge Functions

```bash
SUPABASE_URL="https://your-ref.supabase.co"
SUPABASE_PROJECT_REF="your-ref"
SUPABASE_ANON_KEY="your-anon-key"  # Optional, for API integration
SUPABASE_SERVICE_ROLE_KEY="your-service-key"  # Optional, for admin operations
```

## Safety Guidelines

- Always verify environment variables before deploying
- Show user what platform(s) will be deployed to
- Report deployment URLs after successful deploy
- Keep .env file secure and never commit it
- Supabase service role keys should NEVER be exposed publicly
- Test locally before deploying to production

## Available Endpoints After Deployment

### Cloudflare Workers API

- **Base URL**: `https://api.*.workers.dev`
- **Health Check**: `GET /`
- **Database Test**: `GET /db-test` (tests Supabase connection)

### Supabase Edge Functions

- **Base URL**: `https://<ref>.supabase.co/functions/v1`
- **Hello World**: `GET /hello-world` or `POST /hello-world`
