# Secrets and Environment Variables

## Understanding the Difference

**Environment Variables (`[env]` in fly.toml):**
- Non-sensitive configuration
- Committed to version control
- Visible in fly.toml
- Examples: `NODE_ENV=production`, `PORT=8080`

**Secrets (via `fly secrets`):**
- Sensitive data (API keys, passwords, tokens)
- Encrypted at rest
- Never shown in plaintext after setting
- Examples: `DATABASE_URL`, `SECRET_KEY`, `API_TOKEN`

---

## Setting Environment Variables

### In fly.toml

```toml
[env]
  NODE_ENV = "production"
  PORT = "8080"
  LOG_LEVEL = "info"
  API_VERSION = "v1"
```

These are baked into your app's configuration and visible to anyone with access to the repository.

### Reading Environment Variables

**Node.js:**
```js
const nodeEnv = process.env.NODE_ENV
const port = process.env.PORT || 8080
```

**Python:**
```python
import os
node_env = os.getenv('NODE_ENV', 'development')
port = int(os.getenv('PORT', 8080))
```

**Rust:**
```rust
let node_env = std::env::var("NODE_ENV").unwrap_or_else(|_| "development".to_string());
let port = std::env::var("PORT").unwrap_or_else(|_| "8080".to_string());
```

---

## Managing Secrets

### Setting Secrets

```bash
# Set single secret
fly secrets set API_KEY=abc123

# Set multiple secrets
fly secrets set API_KEY=abc123 SECRET_KEY=xyz789

# Set from file
fly secrets set API_KEY=$(cat api_key.txt)

# Generate random secret
fly secrets set SECRET_KEY=$(openssl rand -hex 32)
```

**Important:** Setting secrets triggers an immediate deployment to inject them into your app.

### Staging Secrets (No Immediate Deployment)

Use `--stage` to prepare secrets without deploying:

```bash
# Stage secrets
fly secrets set API_KEY=abc123 --stage
fly secrets set SECRET_KEY=xyz789 --stage

# Deploy when ready
fly secrets deploy
```

### Listing Secrets

```bash
# List all secrets (names only, not values)
fly secrets list
```

Output:
```
NAME            DIGEST          CREATED AT
API_KEY         abc123ef        2024-01-10T10:30:00Z
DATABASE_URL    def456gh        2024-01-10T09:15:00Z
SECRET_KEY      ghi789jk        2024-01-10T10:30:00Z
```

**Note:** You cannot view secret values after setting them. If you lose a secret, you must set it again.

### Removing Secrets

```bash
# Remove single secret
fly secrets unset API_KEY

# Remove multiple secrets
fly secrets unset API_KEY SECRET_KEY
```

---

## Common Secret Patterns

### Database Connection

```bash
# Postgres (automatically set by fly postgres attach)
fly secrets set DATABASE_URL=postgresql://user:pass@host:5432/dbname

# MongoDB
fly secrets set MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db

# Redis
fly secrets set REDIS_URL=redis://user:pass@host:6379
```

### Application Secrets

```bash
# Django secret key
fly secrets set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Rails secret key
fly secrets set SECRET_KEY_BASE=$(rails secret)

# Generic random secret
fly secrets set SECRET_KEY=$(openssl rand -hex 32)

# JWT secret
fly secrets set JWT_SECRET=$(openssl rand -base64 32)
```

### API Keys and Tokens

```bash
# External API keys
fly secrets set STRIPE_API_KEY=sk_live_...
fly secrets set SENDGRID_API_KEY=SG....
fly secrets set OPENAI_API_KEY=sk-...

# OAuth credentials
fly secrets set GITHUB_CLIENT_ID=abc123
fly secrets set GITHUB_CLIENT_SECRET=xyz789

# Auth tokens
fly secrets set AUTH_TOKEN=$(uuidgen)
```

---

## File-Based Secrets

For applications that expect secrets in files (certificates, SSH keys):

### Method 1: Base64 in fly.toml

```toml
[[files]]
  guest_path = "/app/cert.pem"
  secret_name = "CERT_PEM_BASE64"
```

Set the secret:
```bash
fly secrets set CERT_PEM_BASE64=$(base64 < cert.pem)
```

### Method 2: Dockerfile Secret Mounts

Build-time secrets (won't be in final image):

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-slim

RUN --mount=type=secret,id=npmrc,dst=/root/.npmrc \
    npm install
```

Build with:
```bash
fly deploy --build-secret npmrc=@$HOME/.npmrc
```

---

## Security Best Practices

### 1. Never Commit Secrets to Git

**Bad:**
```toml
[env]
  DATABASE_URL = "postgresql://user:password@host/db"  # ❌ NEVER DO THIS
```

**Good:**
```bash
fly secrets set DATABASE_URL=postgresql://user:password@host/db  # ✅
```

### 2. Use .env Files Locally

**.env (never commit):**
```
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=local-dev-key
API_KEY=test-key
```

**.env.example (commit this):**
```
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=generate-with-openssl-rand-hex-32
API_KEY=get-from-api-provider
```

**.gitignore:**
```
.env
.env.local
```

### 3. Rotate Secrets Regularly

```bash
# Generate new secret
NEW_SECRET=$(openssl rand -hex 32)

# Update secret
fly secrets set SECRET_KEY=$NEW_SECRET

# App automatically redeploys with new secret
```

### 4. Separate Secrets by Environment

**For staging:**
```bash
fly secrets set API_KEY=test_key -a my-app-staging
```

**For production:**
```bash
fly secrets set API_KEY=prod_key -a my-app-production
```

### 5. Limit Secret Access

**Security architecture:**
- API servers can only encrypt secrets, not decrypt them
- Secrets are decrypted only on the machines running your app
- People with deploy access can read secrets by deploying code that prints them

**Recommendation:**
- Limit deploy access to trusted team members
- Use GitHub Actions with stored secrets (see `github-integration.md`)
- Audit deployments regularly

---

## Environment-Specific Configuration

### Using fly.toml for Different Environments

**fly.staging.toml:**
```toml
app = "my-app-staging"
primary_region = "ord"

[env]
  NODE_ENV = "staging"
  LOG_LEVEL = "debug"
```

**fly.production.toml:**
```toml
app = "my-app-production"
primary_region = "ord"

[env]
  NODE_ENV = "production"
  LOG_LEVEL = "info"

[[vm]]
  memory = "512mb"
```

Deploy:
```bash
# Staging
fly deploy --config fly.staging.toml

# Production
fly deploy --config fly.production.toml
```

---

## Reading Secrets in Your App

Secrets are injected as environment variables, accessible the same way as regular env vars.

### Node.js with dotenv (Local Development)

```js
// Load .env file in development
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config()
}

const dbUrl = process.env.DATABASE_URL
const apiKey = process.env.API_KEY

if (!dbUrl || !apiKey) {
  throw new Error('Required environment variables are missing')
}
```

### Python with python-dotenv

```python
import os
from dotenv import load_dotenv

# Load .env in development
if os.getenv('NODE_ENV') != 'production':
    load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')

if not DATABASE_URL or not API_KEY:
    raise ValueError('Required environment variables are missing')
```

### Rust with dotenvy

```rust
use dotenvy::dotenv;

fn main() {
    // Load .env in development
    if std::env::var("NODE_ENV").unwrap_or_default() != "production" {
        dotenv().ok();
    }

    let db_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let api_key = std::env::var("API_KEY")
        .expect("API_KEY must be set");
}
```

---

## Troubleshooting

### Secret Not Found in App

**Check secret is set:**
```bash
fly secrets list
```

**Redeploy if needed:**
```bash
fly deploy
```

Secrets are injected during deployment. If you set a secret but didn't deploy, your running app won't have it yet.

### Secret Contains Special Characters

Use quotes or escape sequences:

```bash
# With quotes
fly secrets set PASSWORD='p@$$w0rd!'

# With escape
fly secrets set PASSWORD=p@\$\$w0rd\!

# From file (safest)
echo 'p@$$w0rd!' > pass.txt
fly secrets set PASSWORD=$(cat pass.txt)
rm pass.txt
```

### Accidentally Exposed Secret

1. **Immediately rotate the secret:**
```bash
fly secrets set API_KEY=new-key
```

2. **Revoke the old secret** at the provider (Stripe, GitHub, etc.)

3. **Review logs** for any unauthorized access

4. **Update documentation** about the incident

### Secret Deployment Failed

If setting a secret causes deployment failure:

```bash
# Unset the problematic secret
fly secrets unset PROBLEMATIC_SECRET

# Fix your app to handle the secret properly

# Set secret again
fly secrets set PROBLEMATIC_SECRET=value
```

---

## Advanced Patterns

### Using Secrets in Build Arguments

For NEXT_PUBLIC_* variables in Next.js:

```bash
fly deploy --build-arg NEXT_PUBLIC_API_URL=https://api.example.com
```

In Dockerfile:
```dockerfile
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

### Secrets in GitHub Actions

Store secrets in GitHub repository settings, then:

```yaml
# .github/workflows/deploy.yml
- name: Deploy to fly.io
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
  run: |
    fly deploy --remote-only
```

See `github-integration.md` for complete GitHub Actions setup.

### Vault Integration (Advanced)

For enterprise secret management, integrate with HashiCorp Vault or similar:

```js
// Fetch secrets from Vault at startup
const vault = require('node-vault')({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN
});

async function loadSecrets() {
  const result = await vault.read('secret/data/myapp');
  process.env.API_KEY = result.data.data.api_key;
  process.env.DB_PASSWORD = result.data.data.db_password;
}
```

Store only `VAULT_ADDR` and `VAULT_TOKEN` as fly secrets.
