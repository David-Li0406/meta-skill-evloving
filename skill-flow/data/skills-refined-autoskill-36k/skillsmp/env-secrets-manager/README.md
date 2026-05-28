# Environment & Secrets Manager - Quick Start

**Secure, reliable secret management for all ACT projects**

---

## Quick Commands

```bash
# Check health of all secrets
/env-secrets-manager audit

# Rotate a token
/env-secrets-manager rotate NOTION_TOKEN

# Setup new project
/env-secrets-manager setup /path/to/project

# Sync secrets across environments
/env-secrets-manager sync

# Security scan
/env-secrets-manager scan
```

---

## What This Skill Does

✅ **Audits** secrets across all 7 ACT projects
✅ **Rotates** tokens safely across all environments
✅ **Syncs** secrets to local .env, GitHub, and Vercel
✅ **Scans** for hardcoded secrets and security issues
✅ **Sets up** new projects with correct secret configuration

---

## When to Use

- 🔐 **Setting up new project** → `/env-secrets-manager setup`
- 🔄 **Rotating expired token** → `/env-secrets-manager rotate`
- 🩺 **Checking secret health** → `/env-secrets-manager audit`
- 🔍 **Finding security issues** → `/env-secrets-manager scan`
- 🔁 **Syncing environments** → `/env-secrets-manager sync`
- ❌ **"Token invalid" errors** → `/env-secrets-manager audit NOTION_TOKEN`

---

## Example Workflows

### Setting Up a New Project

```bash
# 1. Create new Next.js project
npx create-next-app@latest my-new-project

# 2. Setup secrets from template
/env-secrets-manager setup ./my-new-project

# 3. Test connections
cd my-new-project && npm run dev
```

### Rotating a Compromised Token

```bash
# 1. Generate new token at source (GitHub, Notion, etc.)
# 2. Rotate across all projects
/env-secrets-manager rotate GITHUB_TOKEN --new-value ghp_newtoken123

# 3. Verify all projects still work
/env-secrets-manager audit GITHUB_TOKEN
```

### Monthly Security Check

```bash
# 1. Run full audit
/env-secrets-manager audit --output audit-report.md

# 2. Scan for security issues
/env-secrets-manager scan

# 3. Rotate expiring tokens
/env-secrets-manager rotate --expiring
```

---

## Architecture

### Projects Managed

1. ACT Farm Studio
2. Empathy Ledger
3. JusticeHub
4. The Harvest
5. Goods
6. ACT Farm
7. Global Infrastructure

### Environments Synced

- **Local**: `.env.local` files
- **GitHub**: Repository secrets
- **Vercel**: Project environment variables

### Secrets Tracked

**Shared across all projects:**
- GITHUB_TOKEN / GH_PROJECT_TOKEN
- NOTION_TOKEN
- SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY
- OPENAI_API_KEY

**Project-specific:**
- NOTION_DATABASE_ID
- VERCEL_PROJECT_ID
- GHL_LOCATION_ID

---

## Files Reference

- `SKILL.md` - Complete documentation
- `scripts/audit.mjs` - Audit implementation
- `scripts/rotate.mjs` - Rotation implementation
- `scripts/setup.mjs` - Project setup
- `scripts/sync.mjs` - Environment sync
- `scripts/scan.mjs` - Security scanner
- `templates/env.template` - Standard .env template

---

## Security Features

✅ Never commits secrets to git
✅ Encrypts secrets at rest (optional)
✅ Scans git history for leaked secrets
✅ Validates tokens before deployment
✅ Tracks rotation history
✅ Minimal permission scopes

---

## Support

**Common Issues**: See SKILL.md "Common Issues & Fixes"
**Full Documentation**: See SKILL.md
**Emergency**: See SKILL.md "Emergency Procedures"

---

**Status**: ✅ Production Ready
**Last Updated**: 2025-12-27
