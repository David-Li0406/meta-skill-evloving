---
name: cloudflare-wrangler
description: Use this skill when deploying, developing, and managing Cloudflare Workers, KV, R2, D1, and other associated resources using the Wrangler CLI.
---

# Cloudflare Wrangler Skill

## When to Activate

Activate this skill when:
- Setting up and deploying Cloudflare Workers or Pages
- Managing KV namespaces, R2 object storage, and D1 SQL databases
- Configuring and managing secrets and environment variables
- Tailing logs and monitoring deployments

## Prerequisites

- Node.js v20+ required
- Install Wrangler CLI: 
  ```bash
  npm install -g wrangler
  ```

## Quick Commands

### Workers

```bash
# Initialize a new Worker
wrangler init <name>

# Start local development
wrangler dev

# Deploy to Cloudflare
wrangler deploy

# View live logs
wrangler tail <worker>
```

### Secrets Management

```bash
# Add/update a secret
wrangler secret put <key>

# List secrets
wrangler secret list

# Delete a secret
wrangler secret delete <key>
```

### KV (Key-Value Store)

```bash
# Create a KV namespace
wrangler kv namespace create <name>

# Put a key-value pair
wrangler kv key put <key> <value> --namespace-id <id>

# Get a key's value
wrangler kv key get <key> --namespace-id <id>
```

### D1 (SQL Database)

```bash
# Create a D1 database
wrangler d1 create <name>

# Execute SQL commands
wrangler d1 execute <database> --command "SELECT * FROM users"
```

## Configuration (wrangler.toml)

### Basic Configuration

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"
account_id = "your-account-id"
```

### Advanced Configuration with Environments

```toml
[env.staging]
name = "my-worker-staging"
routes = [{ pattern = "staging-api.example.com/*", zone_name = "example.com" }]
vars = { ENVIRONMENT = "staging" }

[env.production]
name = "my-worker-production"
routes = [{ pattern = "api.example.com/*", zone_name = "example.com" }]
vars = { ENVIRONMENT = "production" }
```

## Best Practices

- Use `wrangler.jsonc` for configuration to leverage newer features.
- Set a recent `compatibility_date` for your Workers.
- Validate your configuration with `wrangler check` before deployment.
- Use environments for staging and production to manage different configurations.

This skill consolidates the best practices and commands for effectively using the Wrangler CLI with Cloudflare services.