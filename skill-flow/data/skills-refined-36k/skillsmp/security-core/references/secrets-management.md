# Secrets Management

Best practices for handling sensitive configuration and credentials.

## Core Principles

1. **Never commit secrets to version control**
2. **Use environment variables or dedicated secret managers**
3. **Rotate secrets regularly**
4. **Encrypt secrets at rest**
5. **Audit secret access**
6. **Use least privilege access**

## Environment Variables

### TypeScript

```typescript
// ✅ Good: Use environment variables
import { z } from 'zod';

const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  API_KEY: z.string(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

const env = EnvSchema.parse(process.env);

export default env;
```

### Python

```python
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    database_url: SecretStr
    jwt_secret: SecretStr
    api_key: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()

# Use .get_secret_value() to access
db_url = settings.database_url.get_secret_value()
```

## Secret Managers

### AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName: string): Promise<string> {
  const client = new SecretsManagerClient({ region: 'us-east-1' });

  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);

  if (response.SecretString) {
    return response.SecretString;
  }

  throw new Error('Secret not found');
}

// Usage
const dbPassword = await getSecret('prod/database/password');
```

### HashiCorp Vault

```typescript
import vault from 'node-vault';

const client = vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

async function getSecret(path: string): Promise<any> {
  const result = await client.read(path);
  return result.data;
}

// Usage
const secrets = await getSecret('secret/data/myapp/config');
```

## Local Development

### .env Files

```bash
# .env (never commit this file)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-development-secret-at-least-32-chars
API_KEY=dev-api-key-12345

# .env.example (commit this as template)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=change-me
API_KEY=change-me
```

### .gitignore

```
# Environment files
.env
.env.local
.env.*.local

# Secret keys
*.key
*.pem
secrets/
```

## Secret Rotation

```typescript
import { Effect } from 'effect';

interface SecretRotator {
  getCurrentSecret(): Promise<string>;
  rotateSecret(): Promise<string>;
  validateSecret(secret: string): Promise<boolean>;
}

class JWTSecretRotator implements SecretRotator {
  async getCurrentSecret(): Promise<string> {
    return await secretsManager.getSecret('jwt_secret_current');
  }

  async rotateSecret(): Promise<string> {
    // Generate new secret
    const newSecret = crypto.randomBytes(64).toString('hex');

    // Store as "next" secret
    await secretsManager.setSecret('jwt_secret_next', newSecret);

    // Wait for propagation
    await this.waitForPropagation();

    // Promote "next" to "current"
    await secretsManager.setSecret('jwt_secret_current', newSecret);

    // Archive old secret
    const oldSecret = await secretsManager.getSecret('jwt_secret_current');
    await secretsManager.setSecret('jwt_secret_previous', oldSecret);

    return newSecret;
  }

  async validateSecret(token: string): Promise<boolean> {
    const secrets = [
      await secretsManager.getSecret('jwt_secret_current'),
      await secretsManager.getSecret('jwt_secret_previous'), // Grace period
    ];

    for (const secret of secrets) {
      try {
        jwt.verify(token, secret);
        return true;
      } catch {
        continue;
      }
    }

    return false;
  }

  private async waitForPropagation(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 5000));
  }
}
```

## Secure Key Generation

```bash
# Generate secure random secrets

# 32-byte secret (256 bits)
openssl rand -base64 32

# 64-byte secret (512 bits)
openssl rand -base64 64

# Hex encoded
openssl rand -hex 32

# For JWT RS256 keys
openssl genrsa -out private.key 4096
openssl rsa -in private.key -pubout -out public.key
```

## CI/CD Secrets

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
      - uses: actions/checkout@v3

      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          npm run deploy
```

### Environment-Specific Secrets

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
        run: npm run deploy
```

## Best Practices

1. **Use strong random generation** - openssl, crypto.randomBytes
2. **Minimum key length** - 256 bits (32 bytes) for symmetric keys
3. **Regular rotation** - Every 90 days or on compromise
4. **Audit access** - Log all secret reads
5. **Encrypt in transit** - Always use TLS
6. **Encrypt at rest** - Use KMS or equivalent
7. **Separate by environment** - Don't reuse secrets across dev/prod
8. **Grace period for rotation** - Accept both old and new during transition
9. **Least privilege** - Only grant access to needed secrets
10. **Never log secrets** - Redact in logs

## Secret Scanning

```bash
# Install secret scanning tools
npm install -g @trufflesecurity/trufflehog

# Scan repository
trufflehog git https://github.com/user/repo

# Pre-commit hook
# .git/hooks/pre-commit
#!/bin/bash
trufflehog git file://. --since-commit HEAD --only-verified --fail
```

## Checklist

- [ ] .env files in .gitignore
- [ ] No secrets in code
- [ ] Using secret manager in production
- [ ] Secrets rotated regularly
- [ ] Audit logging enabled
- [ ] Least privilege access configured
- [ ] Strong key generation
- [ ] Grace period for rotation
- [ ] Secret scanning in CI/CD
- [ ] Documented rotation procedures
