---
name: multi-env-setup
description: Use this skill when configuring applications across development, staging, and production environments, ensuring proper management of environment-specific settings and secrets.
---

# Multi-Environment Setup

## Overview
Configure applications across development, staging, and production environments with proper isolation and secrets management.

## Prerequisites
- Separate API keys or accounts per environment
- Secret management solution (e.g., Vault, AWS Secrets Manager)
- CI/CD pipeline with environment variables
- Environment detection in the application

## Environment Strategy

| Environment | Purpose            | API Keys               | Data      |
|-------------|--------------------|------------------------|-----------|
| Development | Local development   | Test keys              | Sandbox   |
| Staging     | Pre-production      | Staging keys           | Test data |
| Production   | Live traffic       | Production keys        | Real data |

## Configuration Structure

```
config/
├── app/
│   ├── base.json           # Shared config
│   ├── development.json    # Dev overrides
│   ├── staging.json        # Staging overrides
│   └── production.json     # Prod overrides
```

### base.json
```json
{
  "timeout": 30000,
  "retries": 3,
  "cache": {
    "enabled": true,
    "ttlSeconds": 60
  }
}
```

### development.json
```json
{
  "apiKey": "${API_KEY_DEV}",
  "baseUrl": "https://api-sandbox.example.com",
  "debug": true,
  "cache": {
    "enabled": false
  }
}
```

### staging.json
```json
{
  "apiKey": "${API_KEY_STAGING}",
  "baseUrl": "https://api-staging.example.com",
  "debug": false
}
```

### production.json
```json
{
  "apiKey": "${API_KEY_PROD}",
  "baseUrl": "https://api.example.com",
  "debug": false,
  "retries": 5
}
```

## Environment Detection

```typescript
// src/app/config.ts
import baseConfig from '../../config/app/base.json';

type Environment = 'development' | 'staging' | 'production';

function detectEnvironment(): Environment {
  const env = process.env.NODE_ENV || 'development';
  const validEnvs: Environment[] = ['development', 'staging', 'production'];
  return validEnvs.includes(env as Environment)
    ? (env as Environment)
    : 'development';
}

export function getConfig() {
  const env = detectEnvironment();
  const envConfig = require(`../../config/app/${env}.json`);
  
  return {
    ...baseConfig,
    ...envConfig,
  };
}
```

## Environment-Specific API Keys
```bash
# .env.development
API_KEY_DEV=dev_key_xxx...
NODE_ENV=development

# .env.staging
API_KEY_STAGING=staging_key_xxx...
NODE_ENV=staging

# .env.production
API_KEY_PROD=prod_key_xxx...
NODE_ENV=production
```

## Secret Management Integration
```typescript
// lib/secrets.ts
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

const secretsManager = new SecretsManager({ region: 'us-east-1' });

async function getSecret(secretName: string) {
  const data = await secretsManager.getSecretValue({ SecretId: secretName });
  return data.SecretString;
}
```