# Vercel Environment Variables Sync

> Modern, automated environment variable management for Vercel deployments

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](./SKILL.md)
[![Vercel CLI](https://img.shields.io/badge/Vercel_CLI-33%2B-black.svg)](https://vercel.com/docs/cli)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-green.svg)](https://agentskills.io/)

## Quick Start

```bash
# Navigate to skill
cd .github/skills/vercel-env-sync

# Make executable
chmod +x scripts/*.sh lib/*.sh

# Health check
source lib/env-functions.sh && vercel::env::health_check

# Audit
./scripts/env-audit.sh

# Sync (dry-run first)
./scripts/env-push.sh --all-envs --dry-run
./scripts/env-push.sh --all-envs
```

## What This Skill Does

- **Sync local→Vercel**: Push `.env.local` values to Vercel automatically
- **Pull Vercel→local**: Download Vercel vars to local files
- **Audit & verify**: Compare local vs Vercel across all environments
- **Auto-secure**: Detect and mark sensitive variables with `--sensitive`
- **Validate**: Check value formats (URLs, secret length, PostgreSQL connections)
- **Backup**: Auto-create backups before modifications

## Features

### ✅ Modern Vercel CLI

Uses `vercel env update` instead of deprecated `rm + add` pattern (Vercel CLI 33+).

### 🔒 Security First

Automatically detects sensitive variables:

- `DATABASE_URL`, `*_SECRET`, `*_KEY`, `*_TOKEN`, `*_PASSWORD`
- Adds `--sensitive` flag for encryption

### ✨ Validation

Prevents invalid configurations:

```bash
❌ BETTER_AUTH_SECRET debe tener al menos 32 caracteres
❌ DATABASE_URL debe ser una conexión PostgreSQL válida
⚠️  API_URL debería ser una URL válida
```

### 🎯 Multi-Environment

Sync across production, preview, and development with one command:

```bash
./scripts/env-push.sh --all-envs
```

### 🔍 Dry-Run Mode

Preview changes before applying:

```bash
./scripts/env-push.sh --all-envs --dry-run
```

## Documentation

- **[SKILL.md](./SKILL.md)** - Complete documentation with 10+ patterns
- **[MIGRATION.md](./MIGRATION.md)** - Migration guide from v1 to v2
- **[lib/env-functions.sh](./lib/env-functions.sh)** - Reusable function library (20+ functions)

## Scripts

| Script                                   | Purpose                        | Example                                  |
| ---------------------------------------- | ------------------------------ | ---------------------------------------- |
| [`env-push.sh`](./scripts/env-push.sh)   | Push local vars to Vercel      | `./scripts/env-push.sh --all-envs`       |
| [`env-pull.sh`](./scripts/env-pull.sh)   | Pull Vercel vars to local file | `./scripts/env-pull.sh --env production` |
| [`env-audit.sh`](./scripts/env-audit.sh) | Generate sync status report    | `./scripts/env-audit.sh --json`          |

## Common Tasks

### First-Time Setup

```bash
# Install Vercel CLI
pnpm add -g vercel

# Authenticate
vercel login

# Link project
vercel link
```

### Daily Development

```bash
# Pull latest vars
./scripts/env-pull.sh --env development

# Or run dev without local .env
vercel env run -- pnpm dev
```

### Pre-Deployment

```bash
# Audit before deploy
./scripts/env-audit.sh || exit 1

# Deploy
vercel --prod
```

### CI/CD Integration

```yaml
- name: Validate Environment Variables
  env:
    VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  run: |
    cd .github/skills/vercel-env-sync
    chmod +x scripts/*.sh
    ./scripts/env-audit.sh --json
```

## Requirements

- **Vercel CLI**: 33+ (`vercel --version`)
- **Bash**: 4+ (Git Bash compatible on Windows)
- **Files**: `.env.example` with variable names

## Project Integration

This skill is part of **The Simpsons API** project and manages:

- `DATABASE_URL` (Neon PostgreSQL)
- `NEXT_PUBLIC_APP_URL` (https://thesimpson.webcode.es)
- `BETTER_AUTH_URL`
- `BETTER_AUTH_SECRET`

See [project docs](../../../docs/VERCEL_ENV_SYNC.md) for project-specific usage.

## Related Skills

- [vercel-cli-management](../vercel-cli-management/SKILL.md) - General Vercel CLI usage
- [neon-database-management](../neon-database-management/SKILL.md) - Database env var management

## Support

- **Issues**: [GitHub Issues](https://github.com/JordiNodeJS/thesimpsonsapi/issues)
- **Docs**: [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- **Vercel**: [Environment Variables Docs](https://vercel.com/docs/projects/environment-variables)

---

**Version**: 2.0  
**Last Updated**: January 14, 2026  
**License**: MIT  
**Author**: GitHub Copilot (Claude Sonnet 4.5)
