---
name: cloudflare-management
description: Use this skill when deploying and managing Cloudflare Workers, Pages, KV, R2, D1, and secrets with the Wrangler CLI.
---

# Cloudflare Management Skill

## When to Activate

Activate this skill when:
- Setting up Cloudflare Workers or Pages
- Working with KV, R2, or D1 storage
- Deploying applications to Cloudflare
- Configuring `wrangler.toml`
- Managing Cloudflare resources and secrets

## Installation

```bash
# Install Wrangler globally
npm install -g wrangler
# or
pnpm add -g wrangler

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

## Project Initialization

```bash
# Create a new Worker project
wrangler init <name>

# Create from a template
wrangler init <name> --template cloudflare/worker-template
```

## Quick Commands

### Workers

```bash
# Initialize new worker
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
# Add/update secret
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

# Put key
wrangler kv key put <key> <value> --namespace-id <id>

# Get key
wrangler kv key get <key> --namespace-id <id>
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

## Configuration Files

### `wrangler.toml` Example

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"

# KV binding
[[kv_namespaces]]
binding = "MY_KV"
id = "xxx"

# D1 binding
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

# R2 binding
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
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
# Deploy to workers.dev
wrangler deploy

# Deploy to specific environment
wrangler deploy --env production
```

## Best Practices

- Use `wrangler dev` for local testing first.
- Monitor logs with `wrangler tail`.
- Never commit secrets; use `wrangler secret put`.
- Use environment-specific configurations for staging and production.

## Common Patterns

### KV + R2 Caching

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cacheKey = url.pathname;

    // Check KV cache
    let content = await env.MY_KV.get(cacheKey);
    if (content) return new Response(content);

    // Fetch from R2
    const object = await env.MY_BUCKET.get(cacheKey.slice(1));
    if (!object) return new Response("Not found", { status: 404 });

    content = await object.text();

    // Cache in KV
    await env.MY_KV.put(cacheKey, content, { expirationTtl: 3600 });

    return new Response(content);
  }
}
```

## Resources

- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)