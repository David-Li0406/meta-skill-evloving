---
name: env-variable-management
description: Guide for adding environment variables. Use when adding new env vars to ensure all 4 locations are updated (code, SST, workflow, GitHub secrets).
---

# Environment Variable Management Skill

## Purpose

Ensure environment variables are properly configured across ALL required locations. Missing a location causes **production runtime crashes**.

## ⚠️ CRITICAL: 4 Locations Must Stay in Sync

When adding ANY new environment variable, you MUST update **ALL 4 locations**:

| #   | Location            | Purpose                | File                               |
| --- | ------------------- | ---------------------- | ---------------------------------- |
| 1   | **Code**            | Read the variable      | `process.env.VAR_NAME`             |
| 2   | **SST Config**      | Lambda runtime env     | `sst.config.ts`                    |
| 3   | **Deploy Workflow** | CI/CD secrets → `.env` | `.github/workflows/deploy-sst.yml` |
| 4   | **GitHub Secrets**  | Actual secret values   | GitHub repo settings               |

## Required vs Optional Pattern

### Required Variables (Fail Fast)

For variables that MUST exist in production:

**In `sst.config.ts`:**

```typescript
environment: {
  MY_REQUIRED_VAR: (() => {
    const value = process.env.MY_REQUIRED_VAR;
    if (!value) {
      throw new Error(
        "MY_REQUIRED_VAR environment variable must be set for SST deployment"
      );
    }
    return value;
  })(),
}
```

**In `deploy-sst.yml`:**

```yaml
- name: Create .env.production file
  env:
    MY_REQUIRED_VAR: ${{ secrets.MY_REQUIRED_VAR }}
  run: |
    # Validate required secret
    if [ -z "$MY_REQUIRED_VAR" ]; then
      echo "::error::MY_REQUIRED_VAR secret is required but not set"
      exit 1
    fi
    echo "MY_REQUIRED_VAR=$MY_REQUIRED_VAR" >> .env.production
```

### Optional Variables (Graceful Fallback)

For variables with defaults or optional features:

**In `sst.config.ts`:**

```typescript
environment: {
  // Optional: only include if set
  ...(process.env.MY_OPTIONAL_VAR && {
    MY_OPTIONAL_VAR: process.env.MY_OPTIONAL_VAR,
  }),
}
```

**In `deploy-sst.yml`:**

```yaml
if [ -n "$MY_OPTIONAL_VAR" ]; then
echo "MY_OPTIONAL_VAR=$MY_OPTIONAL_VAR" >> .env.production
echo "✅ MY_OPTIONAL_VAR configured"
else
echo "::warning::MY_OPTIONAL_VAR not set. Feature X will be disabled."
fi
```

## Current Required Secrets

These MUST be set in GitHub Secrets for deployment:

| Secret                  | Purpose                    |
| ----------------------- | -------------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS deployment credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS deployment credentials |
| `NEXT_PUBLIC_API_URL`   | Backend API URL            |
| `HMAC_SECRET`           | API request signing        |
| `SENTRY_DSN`            | Error tracking             |
| `DEEPL_API_KEY`         | Translation service        |
| `STRIPE_SECRET_KEY`     | Payment processing         |
| `STRIPE_WEBHOOK_SECRET` | Webhook verification       |
| `REVALIDATE_SECRET`     | Cache revalidation         |

## Current Optional Secrets

| Secret                         | Purpose     | Fallback     |
| ------------------------------ | ----------- | ------------ |
| `NEXT_PUBLIC_GOOGLE_ANALYTICS` | Analytics   | Disabled     |
| `NEXT_PUBLIC_GOOGLE_ADS`       | Ads         | Disabled     |
| `NEXT_PUBLIC_GOOGLE_MAPS`      | Maps        | Disabled     |
| `SENTRY_AUTH_TOKEN`            | Source maps | Warning only |
| `CLOUDFLARE_ZONE_ID`           | CDN purge   | Skipped      |
| `CLOUDFLARE_API_TOKEN`         | CDN purge   | Skipped      |
| `GOOGLE_PLACES_API_KEY`        | Places API  | Disabled     |

## Step-by-Step: Adding a New Environment Variable

### Step 1: Add to Code

```typescript
// In your code file
const myVar = process.env.MY_NEW_VAR;
if (!myVar) {
  // Handle missing - throw for required, fallback for optional
}
```

### Step 2: Add to `sst.config.ts`

Find the `environment` block in `sst.config.ts` (~line 165):

```typescript
const site = new sst.aws.Nextjs("site", {
  // ...
  environment: {
    // Add here - use required or optional pattern above
    MY_NEW_VAR: (() => {
      const value = process.env.MY_NEW_VAR;
      if (!value) {
        throw new Error("MY_NEW_VAR must be set for SST deployment");
      }
      return value;
    })(),
  },
});
```

### Step 3: Add to `deploy-sst.yml`

Find "Create .env.production file" step (~line 89):

```yaml
- name: Create .env.production file
  env:
    # Add to env block
    MY_NEW_VAR: ${{ secrets.MY_NEW_VAR }}
  run: |
    # Add validation (for required) or conditional (for optional)
    if [ -z "$MY_NEW_VAR" ]; then
      echo "::error::MY_NEW_VAR is required"
      exit 1
    fi
    echo "MY_NEW_VAR=$MY_NEW_VAR" >> .env.production
```

### Step 4: Add to GitHub Secrets

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `MY_NEW_VAR` with the actual value

### Step 5: Update Documentation (Optional but Recommended)

Add to the tables in this skill file.

## `NEXT_PUBLIC_` Prefix Rules

| Prefix            | Visibility      | Use Case                   |
| ----------------- | --------------- | -------------------------- |
| `NEXT_PUBLIC_*`   | Client + Server | Analytics IDs, public URLs |
| No prefix         | Server only     | API keys, secrets, tokens  |

**Security**: Never expose secrets to the client. API keys like `STRIPE_SECRET_KEY` must NOT have `NEXT_PUBLIC_` prefix.

## Local Development

Create `.env.local` (gitignored) with your dev values:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8080/api
HMAC_SECRET=dev-secret-for-testing
# ... other vars
```

## Common Mistakes

1. **Adding to code but not SST** → Runtime crash in Lambda
2. **Adding to SST but not workflow** → Build fails, secret not available
3. **Adding to workflow but not GitHub Secrets** → Empty value, validation fails
4. **Using `NEXT_PUBLIC_` for secrets** → Exposed to browser
5. **Forgetting local `.env.local`** → Dev environment broken

## Checklist for New Env Variable

- [ ] Added `process.env.VAR_NAME` in code?
- [ ] Added to `sst.config.ts` environment block?
- [ ] Added to `deploy-sst.yml` env and run sections?
- [ ] Added secret value in GitHub repo settings?
- [ ] Decided: required (throw) or optional (fallback)?
- [ ] Correct prefix: `NEXT_PUBLIC_` only for public values?
- [ ] Updated `.env.local` for local dev?
- [ ] Documented in this skill file (if persistent)?

## Files to Reference

- [sst.config.ts](../../../sst.config.ts) - Lambda environment (~line 165)
- [.github/workflows/deploy-sst.yml](../../workflows/deploy-sst.yml) - CI/CD (~line 89)
- GitHub repo → Settings → Secrets → Actions

## Testing Your Changes

After adding a new env var:

1. **Local**: Add to `.env.local`, run `yarn dev`
2. **CI dry-run**: Push to branch, check workflow logs
3. **Production**: Merge to main, verify in CloudWatch logs
