# Pattern: Config Loading

> Standard patterns for loading, validating, and managing configuration.

---

## When to Use This Pattern

- Loading environment variables at application startup
- Managing different configurations for dev/staging/prod
- Validating required configuration exists
- Handling secrets and sensitive values

**Do NOT use when:**
- Simple scripts with 1-2 config values
- Runtime configuration changes (use feature flags instead)

---

## The Pattern

### TypeScript/JavaScript

```typescript
// config/schema.ts - Define configuration schema with validation
import { z } from 'zod';

// Environment enum
const Environment = z.enum(['development', 'staging', 'production', 'test']);

// Database config schema
const DatabaseConfigSchema = z.object({
  host: z.string().min(1),
  port: z.coerce.number().int().positive().default(5432),
  database: z.string().min(1),
  username: z.string().min(1),
  password: z.string().min(1),
  ssl: z.coerce.boolean().default(false),
  poolSize: z.coerce.number().int().min(1).max(100).default(10),
});

// API config schema
const ApiConfigSchema = z.object({
  port: z.coerce.number().int().positive().default(3000),
  host: z.string().default('0.0.0.0'),
  corsOrigins: z.string().transform(s => s.split(',')).default('*'),
  rateLimitRpm: z.coerce.number().int().positive().default(100),
});

// External services config
const ExternalServicesSchema = z.object({
  stripe: z.object({
    apiKey: z.string().startsWith('sk_'),
    webhookSecret: z.string().startsWith('whsec_'),
  }),
  sendgrid: z.object({
    apiKey: z.string().startsWith('SG.'),
    fromEmail: z.string().email(),
  }).optional(),
});

// Full config schema
const ConfigSchema = z.object({
  env: Environment,
  database: DatabaseConfigSchema,
  api: ApiConfigSchema,
  services: ExternalServicesSchema,
  logLevel: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

export type Config = z.infer<typeof ConfigSchema>;
export { ConfigSchema, Environment };

// config/loader.ts - Load and validate configuration
import { ConfigSchema, Config } from './schema';

class ConfigurationError extends Error {
  constructor(message: string, public errors: z.ZodError['errors']) {
    super(message);
    this.name = 'ConfigurationError';
  }
}

function loadFromEnv(): Record<string, unknown> {
  return {
    env: process.env.NODE_ENV || 'development',
    database: {
      host: process.env.DB_HOST,
      port: process.env.DB_PORT,
      database: process.env.DB_NAME,
      username: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      ssl: process.env.DB_SSL,
      poolSize: process.env.DB_POOL_SIZE,
    },
    api: {
      port: process.env.PORT,
      host: process.env.HOST,
      corsOrigins: process.env.CORS_ORIGINS,
      rateLimitRpm: process.env.RATE_LIMIT_RPM,
    },
    services: {
      stripe: {
        apiKey: process.env.STRIPE_API_KEY,
        webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
      },
      sendgrid: process.env.SENDGRID_API_KEY ? {
        apiKey: process.env.SENDGRID_API_KEY,
        fromEmail: process.env.SENDGRID_FROM_EMAIL,
      } : undefined,
    },
    logLevel: process.env.LOG_LEVEL,
  };
}

let cachedConfig: Config | null = null;

export function loadConfig(): Config {
  if (cachedConfig) {
    return cachedConfig;
  }

  const rawConfig = loadFromEnv();
  const result = ConfigSchema.safeParse(rawConfig);

  if (!result.success) {
    const messages = result.error.errors.map(e =>
      `${e.path.join('.')}: ${e.message}`
    ).join('\n');

    throw new ConfigurationError(
      `Configuration validation failed:\n${messages}`,
      result.error.errors
    );
  }

  cachedConfig = result.data;
  return cachedConfig;
}

// For testing - reset cached config
export function resetConfig(): void {
  cachedConfig = null;
}

// config/index.ts - Export typed config
import { loadConfig } from './loader';

export const config = loadConfig();
export type { Config } from './schema';

// Usage in application
import { config } from './config';

const db = new Database({
  host: config.database.host,
  port: config.database.port,
  // ...
});
```

### Python

```python
# config/schema.py
from pydantic import BaseSettings, Field, validator
from typing import Optional, List
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"

class DatabaseConfig(BaseSettings):
    host: str
    port: int = 5432
    database: str
    username: str
    password: str
    ssl: bool = False
    pool_size: int = Field(default=10, ge=1, le=100)

    class Config:
        env_prefix = "DB_"

class ApiConfig(BaseSettings):
    port: int = 3000
    host: str = "0.0.0.0"
    cors_origins: List[str] = ["*"]
    rate_limit_rpm: int = 100

    @validator("cors_origins", pre=True)
    def parse_cors(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v

    class Config:
        env_prefix = "API_"

class StripeConfig(BaseSettings):
    api_key: str
    webhook_secret: str

    @validator("api_key")
    def validate_api_key(cls, v):
        if not v.startswith("sk_"):
            raise ValueError("Stripe API key must start with 'sk_'")
        return v

    class Config:
        env_prefix = "STRIPE_"

class Settings(BaseSettings):
    env: Environment = Environment.DEVELOPMENT
    database: DatabaseConfig = None
    api: ApiConfig = None
    stripe: StripeConfig = None
    log_level: str = "info"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load nested configs
        self.database = DatabaseConfig()
        self.api = ApiConfig()
        self.stripe = StripeConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# config/__init__.py
from functools import lru_cache
from .schema import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# Usage
from config import settings

db = Database(
    host=settings.database.host,
    port=settings.database.port,
)
```

### Go

```go
// config/config.go
package config

import (
    "fmt"
    "os"
    "strconv"
    "strings"
)

type Environment string

const (
    Development Environment = "development"
    Staging     Environment = "staging"
    Production  Environment = "production"
    Test        Environment = "test"
)

type DatabaseConfig struct {
    Host     string
    Port     int
    Database string
    Username string
    Password string
    SSL      bool
    PoolSize int
}

type APIConfig struct {
    Port         int
    Host         string
    CORSOrigins  []string
    RateLimitRPM int
}

type Config struct {
    Env      Environment
    Database DatabaseConfig
    API      APIConfig
    LogLevel string
}

func Load() (*Config, error) {
    cfg := &Config{}

    // Environment
    env := getEnv("NODE_ENV", "development")
    switch env {
    case "development", "staging", "production", "test":
        cfg.Env = Environment(env)
    default:
        return nil, fmt.Errorf("invalid environment: %s", env)
    }

    // Database
    cfg.Database = DatabaseConfig{
        Host:     requireEnv("DB_HOST"),
        Port:     getEnvInt("DB_PORT", 5432),
        Database: requireEnv("DB_NAME"),
        Username: requireEnv("DB_USER"),
        Password: requireEnv("DB_PASSWORD"),
        SSL:      getEnvBool("DB_SSL", false),
        PoolSize: getEnvInt("DB_POOL_SIZE", 10),
    }

    // API
    cfg.API = APIConfig{
        Port:         getEnvInt("PORT", 3000),
        Host:         getEnv("HOST", "0.0.0.0"),
        CORSOrigins:  strings.Split(getEnv("CORS_ORIGINS", "*"), ","),
        RateLimitRPM: getEnvInt("RATE_LIMIT_RPM", 100),
    }

    cfg.LogLevel = getEnv("LOG_LEVEL", "info")

    return cfg, nil
}

func requireEnv(key string) string {
    value := os.Getenv(key)
    if value == "" {
        panic(fmt.Sprintf("required environment variable %s is not set", key))
    }
    return value
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if i, err := strconv.Atoi(value); err == nil {
            return i
        }
    }
    return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
    if value := os.Getenv(key); value != "" {
        return value == "true" || value == "1"
    }
    return defaultValue
}
```

### Secret Management

```typescript
// secrets.ts - Separate secrets from config
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

interface Secrets {
  databasePassword: string;
  stripeApiKey: string;
  jwtSecret: string;
}

async function loadSecretsFromAWS(): Promise<Secrets> {
  const client = new SecretsManager({ region: 'us-east-1' });

  const response = await client.getSecretValue({
    SecretId: process.env.SECRETS_ARN,
  });

  if (!response.SecretString) {
    throw new Error('No secrets found');
  }

  return JSON.parse(response.SecretString);
}

// Local development fallback
async function loadSecretsFromEnv(): Promise<Secrets> {
  return {
    databasePassword: process.env.DB_PASSWORD!,
    stripeApiKey: process.env.STRIPE_API_KEY!,
    jwtSecret: process.env.JWT_SECRET!,
  };
}

export async function loadSecrets(): Promise<Secrets> {
  if (process.env.NODE_ENV === 'production') {
    return loadSecretsFromAWS();
  }
  return loadSecretsFromEnv();
}
```

---

## Common Mistakes to Avoid

### 1. No Validation at Startup
```typescript
// BAD - crashes later when config is used
const dbHost = process.env.DB_HOST;  // Might be undefined
// ... later in the app
await db.connect(dbHost);  // Crashes here, hard to debug

// GOOD - fail fast at startup
const config = loadConfig();  // Throws immediately if invalid
```

### 2. Accessing process.env Everywhere
```typescript
// BAD - env vars scattered throughout codebase
function createUser() {
  const apiKey = process.env.STRIPE_API_KEY;  // Direct access
  // ...
}

// GOOD - single source of truth
import { config } from './config';

function createUser() {
  const apiKey = config.services.stripe.apiKey;  // Typed, validated
}
```

### 3. Secrets in Config Files
```typescript
// BAD - secrets committed to repo
// config/production.json
{
  "database": {
    "password": "supersecret123"  // DON'T DO THIS
  }
}

// GOOD - secrets from environment/secrets manager
{
  "database": {
    "password": "${DB_PASSWORD}"  // Reference, not value
  }
}
```

### 4. No Type Safety
```typescript
// BAD - stringly typed config
const port = process.env.PORT;  // string | undefined
server.listen(port);  // Type error or runtime error

// GOOD - parsed and typed
const port = z.coerce.number().parse(process.env.PORT);  // number
server.listen(port);  // Works correctly
```

### 5. Mutable Configuration
```typescript
// BAD - config can be modified
export const config = {
  apiKey: process.env.API_KEY,
};
config.apiKey = 'hacked';  // Oops

// GOOD - frozen/immutable config
export const config = Object.freeze({
  apiKey: process.env.API_KEY,
});
config.apiKey = 'hacked';  // Throws in strict mode
```

---

## Validation Commands

```bash
# Verify all required env vars are set
node -e "require('./config')" || echo "Config validation failed"

# Check for hardcoded secrets
! grep -rE "(password|secret|api_key)\s*[:=]\s*['\"][^$]" src/ config/ \
  || echo "WARNING: Possible hardcoded secrets"

# Validate .env.example has all required vars
diff <(grep -oE '^[A-Z_]+=' .env.example | sort) \
     <(grep -oE '^[A-Z_]+=' .env | sort)

# Check config files don't contain secrets
! grep -rE "(sk_|SG\.|whsec_)" config/ || echo "WARNING: Secrets in config files"

# Verify schema matches actual config
npm run config:validate
```

---

## Related Conventions

- **Validation**: All configuration MUST be validated at startup
- **Typing**: Configuration MUST be typed (TypeScript/Pydantic/structs)
- **Secrets**: Secrets MUST NOT be in config files or committed to git
- **Defaults**: Provide sensible defaults for non-critical config
- **Documentation**: Document all environment variables in README or .env.example

---

## See Also

- [API Client](api-client.md) - For configuring API clients
- [Error Handling](error-handling.md) - For configuration validation errors
- [Database Patterns](database-patterns.md) - For database connection config
