---
name: env-secrets-manager
description: Secure management of environment variables and secrets across ACT projects. Use for secret audits, rotation, setup, sync, and security scans.
---

# Environment & Secrets Manager

## When Triggered
- Setting up new projects/repos
- Rotating tokens and API keys
- Auditing secret usage
- Troubleshooting auth issues
- Syncing secrets across environments

## Commands

| Command | Purpose |
|---------|---------|
| `audit` | Check secret health across all projects |
| `rotate <name>` | Rotate a secret across all projects |
| `setup <path>` | Setup .env for new project |
| `sync` | Sync secrets across environments |
| `scan` | Scan for security issues |

## Quick Reference

### Three-Tier Storage
1. **Local**: `.env.local` files (dev)
2. **GitHub**: Repository secrets (CI/CD)
3. **Vercel**: Environment variables (production)

### Projects Managed
- ACT Farm Studio, Empathy Ledger, JusticeHub
- The Harvest, Goods, ACT Farm, Global Infrastructure

### Shared Secrets
- `GITHUB_TOKEN`, `GH_PROJECT_TOKEN`
- `NOTION_TOKEN`
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

## Security Rules

**DO:**
- Use env vars for all secrets
- Add .env to .gitignore
- Rotate tokens regularly (90 days GitHub, 6mo Notion)
- Validate tokens on startup

**DON'T:**
- Hardcode secrets
- Commit .env files
- Log secrets
- Use prod secrets in dev

## File References

| Need | Reference |
|------|-----------|
| .env template | `references/env-template.md` |
| Commands | `references/commands.md` |
| Troubleshooting | `references/troubleshooting.md` |
| Emergency procedures | `references/emergency.md` |
