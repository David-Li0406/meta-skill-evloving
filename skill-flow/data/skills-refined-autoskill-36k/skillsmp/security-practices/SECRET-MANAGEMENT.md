# Secret Management Guide

Comprehensive guide for handling secrets, API keys, and credentials securely.

## Core Principle

**Never commit secrets to version control. Ever.**

Even if you delete them later, they remain in git history forever.

## Environment Variables

### Setup

```bash
# 1. Create .env.example (commit this - documents required vars)
touch .env.example

# 2. Create .env (never commit this)
touch .env

# 3. Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.*.local" >> .gitignore
```

### Structure

```bash
# .env.example - Commit this with placeholder values
DATABASE_URL=postgresql://user:password@localhost:5432/database
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-here-minimum-32-chars
API_KEY=your-api-key
STRIPE_SECRET_KEY=sk_test_xxx
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# .env - Never commit - contains real values
DATABASE_URL=postgresql://prod_user:actual_password@prod-host:5432/prod_db
REDIS_URL=redis://:authpassword@redis-host:6379
JWT_SECRET=actual-32-char-minimum-secret-key-here
API_KEY=actual_api_key_12345
STRIPE_SECRET_KEY=sk_live_actual_key
AWS_ACCESS_KEY_ID=AKIAACTUALKEY
AWS_SECRET_ACCESS_KEY=actualSecretAccessKey
```

### Loading Environment Variables

```typescript
// Bun - Built-in .env support
// Variables are automatically available in Bun.env and process.env

// Validate required variables at startup
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'API_KEY',
];

for (const varName of requiredEnvVars) {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
}

// Type-safe config
interface Config {
  databaseUrl: string;
  jwtSecret: string;
  apiKey: string;
  nodeEnv: 'development' | 'production' | 'test';
}

export const config: Config = {
  databaseUrl: process.env.DATABASE_URL!,
  jwtSecret: process.env.JWT_SECRET!,
  apiKey: process.env.API_KEY!,
  nodeEnv: (process.env.NODE_ENV || 'development') as Config['nodeEnv'],
};
```

### Environment-Specific Files

```
.env                # Default, loaded in all environments
.env.local          # Local overrides (always gitignored)
.env.development    # Development environment
.env.production     # Production environment
.env.test           # Test environment
```

## Git Protection

### Complete .gitignore for Secrets

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.development.local
.env.production.local

# Secret and credential files
*.pem
*.key
*.p12
*.pfx
*.crt
credentials.json
service-account.json
secrets/
.secrets/

# Cloud provider credentials
.aws/
.azure/
.gcloud/
gcloud-service-account.json

# SSH keys
id_rsa
id_ed25519
*.pub

# API keys and tokens
api-keys.json
tokens.json
auth.json

# Database dumps (may contain sensitive data)
*.sql
*.dump
*.sqlite

# IDE and editor secrets
.idea/workspace.xml
.vscode/settings.json

# Terraform state (contains secrets)
*.tfstate
*.tfstate.*
.terraform/

# Kubernetes secrets
*-secret.yaml
*.kubeconfig
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .husky/pre-commit

# Patterns that indicate secrets
SECRET_PATTERNS=(
  'password\s*[:=]'
  'secret\s*[:=]'
  'api[_-]?key\s*[:=]'
  'private[_-]?key'
  'access[_-]?token'
  'auth[_-]?token'
  'credentials'
  'BEGIN RSA PRIVATE KEY'
  'BEGIN OPENSSH PRIVATE KEY'
  'BEGIN EC PRIVATE KEY'
  'AKIA[0-9A-Z]{16}'  # AWS Access Key ID
  'sk_live_[0-9a-zA-Z]{24}'  # Stripe Live Key
  'sk-[a-zA-Z0-9]{48}'  # OpenAI API Key
)

# Check staged files
for pattern in "${SECRET_PATTERNS[@]}"; do
  if git diff --cached --name-only -z | xargs -0 grep -l -E "$pattern" 2>/dev/null; then
    echo "ERROR: Potential secret detected matching pattern: $pattern"
    echo "Please remove secrets before committing."
    exit 1
  fi
done

# Check for .env files being committed
if git diff --cached --name-only | grep -E '^\.env($|\.local)'; then
  echo "ERROR: Attempting to commit .env file"
  exit 1
fi

exit 0
```

### Setup Pre-Commit Hook

```bash
# Install husky
bun add -d husky

# Initialize husky
bunx husky install

# Add pre-commit hook
bunx husky add .husky/pre-commit "bash .husky/pre-commit-secrets.sh"
```

## Secret Scanning Tools

### GitHub Secret Scanning

GitHub automatically scans for known secret patterns. Enable it in repository settings.

### Gitleaks

```bash
# Install
brew install gitleaks

# Scan current directory
gitleaks detect

# Scan git history
gitleaks detect --source . --verbose

# Pre-commit hook
gitleaks protect --staged
```

### TruffleHog

```bash
# Install
pip install trufflehog

# Scan git history
trufflehog git file://.

# Scan directory
trufflehog filesystem .
```

### Custom Scanning Script

```typescript
// scripts/scan-secrets.ts
import { $ } from 'bun';

const SECRET_PATTERNS = [
  /password\s*[:=]\s*['"][^'"]+['"]/gi,
  /api[_-]?key\s*[:=]\s*['"][^'"]+['"]/gi,
  /secret\s*[:=]\s*['"][^'"]+['"]/gi,
  /token\s*[:=]\s*['"][^'"]+['"]/gi,
  /AKIA[0-9A-Z]{16}/g,  // AWS Access Key
  /sk_live_[0-9a-zA-Z]{24}/g,  // Stripe Live Key
  /sk-[a-zA-Z0-9]{48}/g,  // OpenAI Key
  /ghp_[a-zA-Z0-9]{36}/g,  // GitHub Personal Access Token
  /-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/g,
];

async function scanFile(filePath: string): Promise<string[]> {
  const content = await Bun.file(filePath).text();
  const findings: string[] = [];

  for (const pattern of SECRET_PATTERNS) {
    const matches = content.match(pattern);
    if (matches) {
      for (const match of matches) {
        findings.push(`${filePath}: ${match.substring(0, 50)}...`);
      }
    }
  }

  return findings;
}

// Main
const files = await $`git ls-files`.text();
const fileList = files.trim().split('\n');

let allFindings: string[] = [];
for (const file of fileList) {
  if (file.endsWith('.md') || file.includes('node_modules')) continue;
  const findings = await scanFile(file);
  allFindings = allFindings.concat(findings);
}

if (allFindings.length > 0) {
  console.error('Potential secrets found:');
  for (const finding of allFindings) {
    console.error(`  - ${finding}`);
  }
  process.exit(1);
} else {
  console.log('No secrets detected.');
}
```

## Secret Managers

### Infisical (Open Source)

```typescript
import InfisicalClient from '@infisical/sdk';

const client = new InfisicalClient({
  siteUrl: 'https://app.infisical.com',
  auth: {
    universalAuth: {
      clientId: process.env.INFISICAL_CLIENT_ID!,
      clientSecret: process.env.INFISICAL_CLIENT_SECRET!,
    },
  },
});

// Fetch secrets
const secrets = await client.listSecrets({
  environment: 'production',
  projectId: 'your-project-id',
});

// Access specific secret
const dbUrl = await client.getSecret({
  secretName: 'DATABASE_URL',
  environment: 'production',
  projectId: 'your-project-id',
});
```

### HashiCorp Vault

```typescript
import Vault from 'node-vault';

const vault = Vault({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

// Read secret
const { data } = await vault.read('secret/data/myapp');
const dbPassword = data.data.database_password;

// Write secret
await vault.write('secret/data/myapp', {
  data: {
    database_password: 'new-password',
  },
});
```

### AWS Secrets Manager

```typescript
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretName: string): Promise<string> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  return response.SecretString!;
}

// Usage
const dbCredentials = JSON.parse(await getSecret('prod/database'));
```

### 1Password CLI

```bash
# Load secrets into environment
eval $(op signin)
export DATABASE_URL=$(op read "op://Vault/Database/url")
export API_KEY=$(op read "op://Vault/API/key")

# Or use op run
op run --env-file=.env.1password -- bun run start
```

## Handling Exposed Secrets

If you accidentally commit a secret:

### 1. Rotate the Secret Immediately

```bash
# Generate new secret
openssl rand -base64 32

# Update in your secret manager or environment
# Revoke the old credentials in the service provider
```

### 2. Remove from Git History

```bash
# Using git-filter-repo (recommended)
pip install git-filter-repo
git filter-repo --path-glob '*.env' --invert-paths

# Or using BFG
bun x bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
git push origin --force --tags
```

### 3. Check for Exposure

- Check service logs for unauthorized access
- Review GitHub security alerts
- Search for your key on GitHub: `"your-api-key"`
- Check Have I Been Pwned for data breaches

## Secure Secret Generation

```typescript
import { randomBytes } from 'crypto';

// Generate secure random string
function generateSecret(length: number = 32): string {
  return randomBytes(length).toString('base64url');
}

// Generate API key
function generateApiKey(): string {
  const prefix = 'sk_live_';
  return prefix + randomBytes(24).toString('base64url');
}

// Generate JWT secret (minimum 256 bits for HS256)
function generateJwtSecret(): string {
  return randomBytes(32).toString('base64');
}

// Generate encryption key (256 bits for AES-256)
function generateEncryptionKey(): string {
  return randomBytes(32).toString('base64');
}
```

## CI/CD Secret Management

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        run: bun install

      - name: Run tests
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          JWT_SECRET: ${{ secrets.JWT_SECRET }}
        run: bun test

      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: bun run deploy
```

### Environment Variables in Actions

```yaml
jobs:
  build:
    environment: production  # Use GitHub environment
    env:
      NODE_ENV: production
    steps:
      - name: Access secret
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Secret is masked in logs
          echo "Using API key: ${API_KEY:0:4}..."
```

## Development vs Production Secrets

```typescript
// config/index.ts
interface Secrets {
  database: {
    url: string;
    ssl: boolean;
  };
  jwt: {
    secret: string;
    expiresIn: string;
  };
  api: {
    key: string;
    rateLimit: number;
  };
}

function loadSecrets(): Secrets {
  const env = process.env.NODE_ENV || 'development';

  if (env === 'development') {
    // Development: use .env file
    return {
      database: {
        url: process.env.DATABASE_URL || 'postgresql://localhost:5432/dev',
        ssl: false,
      },
      jwt: {
        secret: process.env.JWT_SECRET || 'dev-secret-not-for-production',
        expiresIn: '7d',
      },
      api: {
        key: process.env.API_KEY || 'dev-api-key',
        rateLimit: 1000,
      },
    };
  }

  // Production: require all secrets
  const required = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];
  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`Missing required secret: ${key}`);
    }
  }

  return {
    database: {
      url: process.env.DATABASE_URL!,
      ssl: true,
    },
    jwt: {
      secret: process.env.JWT_SECRET!,
      expiresIn: '1h',
    },
    api: {
      key: process.env.API_KEY!,
      rateLimit: 100,
    },
  };
}

export const secrets = loadSecrets();
```

## Secret Rotation

### Automated Rotation Script

```typescript
// scripts/rotate-secrets.ts
import { SecretsManagerClient, RotateSecretCommand } from '@aws-sdk/client-secrets-manager';

async function rotateSecret(secretId: string): Promise<void> {
  const client = new SecretsManagerClient({ region: 'us-east-1' });

  console.log(`Rotating secret: ${secretId}`);

  await client.send(new RotateSecretCommand({
    SecretId: secretId,
    RotateImmediately: true,
  }));

  console.log(`Secret rotated successfully: ${secretId}`);
}

// Rotate all secrets
const secretsToRotate = [
  'prod/database-password',
  'prod/api-key',
  'prod/jwt-secret',
];

for (const secret of secretsToRotate) {
  await rotateSecret(secret);
}
```

### Rotation Schedule

```yaml
# Recommended rotation schedule
database_passwords: 90 days
api_keys: 90 days
jwt_secrets: 30 days
encryption_keys: 365 days (with key versioning)
service_account_keys: 90 days
ssh_keys: 365 days
```

## Testing with Secrets

```typescript
// tests/setup.ts
import { beforeAll } from 'bun:test';

beforeAll(() => {
  // Use test-specific secrets
  process.env.DATABASE_URL = 'postgresql://localhost:5432/test_db';
  process.env.JWT_SECRET = 'test-secret-for-testing-only';
  process.env.API_KEY = 'test-api-key';
});

// Alternative: use .env.test
// Bun automatically loads .env.test when NODE_ENV=test
```

## Claude Code Security Prompts

```
"Review this code for hardcoded secrets or credentials"

"Check if this .gitignore properly excludes all secret files"

"Audit this config module for secure secret loading"

"Generate a secure secret rotation script for AWS Secrets Manager"

"Create a pre-commit hook that scans for exposed secrets"
```
