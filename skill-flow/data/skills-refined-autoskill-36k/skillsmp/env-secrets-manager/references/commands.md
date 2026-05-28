# Command Reference

## Audit Commands

```bash
# Check all secrets across all projects
/env-secrets-manager audit

# Check specific project
/env-secrets-manager audit --project empathy-ledger

# Check specific secret
/env-secrets-manager audit --secret NOTION_TOKEN

# Output to file
/env-secrets-manager audit --output secrets-report.md
```

## Rotation Commands

```bash
# Rotate Notion token
/env-secrets-manager rotate NOTION_TOKEN

# Rotate with prompt to create new token
/env-secrets-manager rotate GITHUB_TOKEN --interactive

# Rotate all expiring tokens
/env-secrets-manager rotate --expiring

# Dry run (show what would change)
/env-secrets-manager rotate NOTION_TOKEN --dry-run
```

## Setup Commands

```bash
# Setup new project
/env-secrets-manager setup /path/to/new-project

# Setup with custom template
/env-secrets-manager setup /path/to/project --template custom.env

# Copy secrets from another project
/env-secrets-manager setup /path/to/new --copy-from empathy-ledger
```

## Sync Commands

```bash
# Sync all environments (local + GitHub + Vercel)
/env-secrets-manager sync

# Sync only GitHub secrets
/env-secrets-manager sync --github-only

# Sync specific project
/env-secrets-manager sync --project justicehub

# Force sync (overwrite all)
/env-secrets-manager sync --force
```

## Scan Commands

```bash
# Scan for security issues
/env-secrets-manager scan

# Scan specific directory
/env-secrets-manager scan --path ./src

# Scan git history
/env-secrets-manager scan --history

# Auto-fix issues
/env-secrets-manager scan --fix
```

## Supported Secrets for Rotation

- `NOTION_TOKEN` - Notion integration token
- `GITHUB_TOKEN` / `GH_PROJECT_TOKEN` - GitHub PAT
- `SUPABASE_SERVICE_ROLE_KEY` - Supabase service key
- `OPENAI_API_KEY` - OpenAI API key
- Custom tokens
