---
name: multi-env-setup
description: Use this skill when configuring applications across development, staging, and production environments, including setting up environment-specific secrets and configurations.
---

# Multi-Environment Setup

## Prerequisites
- Separate accounts or API keys per environment
- Secret management solution (e.g., Vault, AWS Secrets Manager)
- CI/CD pipeline with environment variables
- Environment detection in the application

## Instructions

### Step 1: Create Configuration Structure
Set up the base and per-environment configuration files. For example:
```
config/
├── app/
│   ├── base.json           # Shared config
│   ├── development.json    # Dev overrides
│   ├── staging.json        # Staging overrides
│   └── production.json     # Prod overrides
```

### Step 2: Implement Environment Detection
Add logic to detect and load environment-specific config. Example in TypeScript:
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

export function getAppConfig() {
  const env = detectEnvironment();
  // Load the appropriate config based on the detected environment
}
```

### Step 3: Configure Secrets
Store API keys securely using your secret management solution. Ensure that each environment has its own set of secrets.

### Step 4: Add Environment Guards
Implement safeguards for production-only operations to prevent accidental changes or data loss.

## Output
- Multi-environment configuration structure
- Environment detection logic
- Secure secret management
- Production safeguards enabled

## Error Handling
Refer to your project's error handling documentation for comprehensive error management strategies.

## Examples
Refer to your project's examples documentation for detailed use cases and configurations.

## Resources
- [Application Environments Guide](https://example.com/environments)
- [12-Factor App Config](https://12factor.net/config)