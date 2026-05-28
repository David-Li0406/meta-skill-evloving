---
name: cloudflare-wrangler-management
description: Use this skill when deploying, developing, and managing Cloudflare Workers, KV, R2, D1, and other associated resources using the Wrangler CLI.
---

# Cloudflare Wrangler Management Skill

## When to Activate

Activate this skill when:
- Deploying Cloudflare Workers or Pages
- Managing KV, R2, or D1 storage
- Configuring and managing Cloudflare resources
- Handling secrets and environment variables
- Developing and testing applications locally

## Installation

```bash
# Install Wrangler globally
npm install -g wrangler
# Verify installation
wrangler --version
```

## Authentication

```bash
# Login to Cloudflare
wrangler login
# Check authentication status
wrangler whoami
```

## Quick Commands

### Workers

```bash
# Initialize new Worker
wrangler init <name>
# Local development
wrangler dev
# Deploy to Cloudflare
wrangler deploy
# View logs
wrangler tail <worker>
```

### Secrets Management

```bash
# Add secret
wrangler secret put <key>
# List secrets
wrangler secret list
# Delete secret
wrangler secret delete <key>
```

### KV (Key-Value Store)

```bash
# Create namespace
wrangler kv namespace create <name>
# List namespaces
wrangler kv namespace list
# Put key
wrangler kv key put --namespace-id <id> <key> <value>
# Get key
wrangler kv key get --namespace-id <id> <key>
```

### D1 (SQL Database)

```bash
# Create database
wrangler d1 create <name>
# Execute SQL command
wrangler d1 execute <database> --command "SELECT * FROM users"
```

### R2 (Object Storage)

```bash
# Create bucket
wrangler r2 bucket create <name>
# Upload object
wrangler r2 object put <bucket>/<key> --file <path>
```

## Configuration (wrangler.jsonc)

### Minimal Config

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01"
}
```

### Full Config with Bindings

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "<KV_NAMESPACE_ID>" }
  ],
  "r2_buckets": [
    { "binding": "MY_BUCKET", "bucket_name": "my-bucket" }
  ],
  "d1_databases": [
    { "binding": "DB", "database_name": "my-db", "database_id": "<DB_ID>" }
  ]
}
```

## Development Workflow

### Local Development

```bash
# Start local dev server
wrangler dev
# With specific environment
wrangler dev --env staging
```

### Deployment

```bash
# Deploy to production
wrangler deploy
# Dry run (validate without deploying)
wrangler deploy --dry-run
```

## Best Practices

- **Version control `wrangler.jsonc`**: Treat as the source of truth for Worker config.
- **Use automatic provisioning**: Omit resource IDs for auto-creation on deploy.
- **Test locally first**: Use `wrangler dev` with local bindings before deploying.
- **Use `.dev.vars` for local secrets**: Never commit secrets to config.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: wrangler` | Install: `npm install -g wrangler` |
| Auth errors | Run `wrangler login` |
| Config validation errors | Run `wrangler check` |

## Related Resources

- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)