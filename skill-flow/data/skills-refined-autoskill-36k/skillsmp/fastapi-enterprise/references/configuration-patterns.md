# Configuration Patterns

Type-safe configuration using pydantic-settings with environment variables and YAML files.

## Architecture

```
┌─────────────────┐
│ OS Environment  │  ← Core settings (DB_URL, LOG_LEVEL, etc.)
└────────┬────────┘
         │
    ┌────▼──────┐
    │  .env     │  ← Development overrides
    └────┬──────┘
         │
    ┌────▼──────────────┐
    │ pydantic-settings │  ← Type validation, parsing
    └────┬──────────────┘
         │
    ┌────▼────────┐
    │ Settings    │  ← Singleton, cached
    └─────────────┘

┌──────────────┐
│ config/*.yml │  ← External API configs, feature flags
└──────┬───────┘
       │
  ┌────▼──────────┐
  │ Pydantic      │  ← Validate YAML with models
  │ Models        │
  └───────────────┘
```

## Core Settings (Environment Variables)

### core/config.py

```python
from functools import lru_cache
from typing import Any
from pathlib import Path

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from OS environment variables.
    
    Priority:
    1. OS environment variables
    2. .env file
    3. Default values
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # DB_URL = db_url
        extra="ignore",  # Ignore unknown env vars
    )
    
    # Application
    APP_NAME: str = "FastAPI Enterprise App"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(
        default="development",
        pattern="^(development|staging|production)$"
    )
    DEBUG: bool = Field(default=True)
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4  # Uvicorn workers
    
    # API
    API_PREFIX: str = "/api"
    ENABLE_DOCS: bool = True
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # Logging
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    LOG_JSON: bool = False  # True for production
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"
    DB_ECHO: bool = False  # Log SQL queries
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # Redis (optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = Field(
        default="changeme-in-production",
        min_length=32
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External configs
    CONFIG_DIR: str = "config"
    CONFIG_ENV: str = "development"  # development, staging, production
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse comma-separated string to list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure async driver for SQLAlchemy."""
        if "postgresql://" in v and "asyncpg" not in v:
            raise ValueError(
                "Use async driver: postgresql+asyncpg://..."
            )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance (singleton)."""
    return Settings()


settings = get_settings()
```

### Usage

```python
from core.config import settings

print(settings.DATABASE_URL)
print(settings.ENVIRONMENT)

if settings.DEBUG:
    print("Debug mode enabled")
```

## Environment Files

### .env (Development)

```bash
# Application
APP_NAME=My FastAPI App
ENVIRONMENT=development
DEBUG=true

# Server
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
DB_ECHO=true

# Logging
LOG_LEVEL=DEBUG
LOG_JSON=false

# Security
SECRET_KEY=dev-secret-key-change-in-production

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# External configs
CONFIG_ENV=development
```

### .env.example (Template)

```bash
# Application
APP_NAME=FastAPI Enterprise App
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Add all env vars here as template for new developers
```

## YAML Configuration Files

For external API configurations, feature flags, and environment-specific configs.

### config/development.yml

```yaml
# External API configurations
external_api:
  base_url: "https://api-dev.example.com"
  timeout: 30
  max_retries: 3
  api_key: "dev-api-key-123"

payment_gateway:
  base_url: "https://sandbox.payment.com"
  merchant_id: "dev_merchant"
  api_key: "dev_payment_key"

# Feature flags
features:
  enable_caching: false
  enable_rate_limiting: false
  enable_analytics: true
  new_feature_enabled: true

# Business rules
limits:
  max_file_size_mb: 10
  max_requests_per_minute: 100
  session_timeout_minutes: 30
```

### config/production.yml

```yaml
external_api:
  base_url: "https://api.example.com"
  timeout: 30
  max_retries: 3
  api_key: "${EXTERNAL_API_KEY}"  # Load from environment

payment_gateway:
  base_url: "https://api.payment.com"
  merchant_id: "${PAYMENT_MERCHANT_ID}"
  api_key: "${PAYMENT_API_KEY}"

features:
  enable_caching: true
  enable_rate_limiting: true
  enable_analytics: true
  new_feature_enabled: false  # Gradual rollout

limits:
  max_file_size_mb: 50
  max_requests_per_minute: 1000
  session_timeout_minutes: 60
```

### Load YAML with Pydantic Validation

```python
# core/config.py

from pydantic import BaseModel

class ExternalAPIConfig(BaseModel):
    """Pydantic model for external API configuration."""
    base_url: str
    timeout: int = 30
    max_retries: int = 3
    api_key: str
    
    model_config = {"extra": "forbid"}  # Reject unknown fields


class PaymentGatewayConfig(BaseModel):
    """Payment gateway configuration."""
    base_url: str
    merchant_id: str
    api_key: str


class FeatureFlags(BaseModel):
    """Feature flags."""
    enable_caching: bool = False
    enable_rate_limiting: bool = False
    enable_analytics: bool = True
    new_feature_enabled: bool = False


def load_yaml_config(config_name: str) -> dict[str, Any]:
    """
    Load YAML configuration file based on CONFIG_ENV.
    
    Args:
        config_name: Name of config section (e.g., "external_api")
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        KeyError: If config_name not in file
    """
    config_path = Path(settings.CONFIG_DIR) / f"{settings.CONFIG_ENV}.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        all_configs = yaml.safe_load(f)
    
    if config_name not in all_configs:
        raise KeyError(
            f"Configuration '{config_name}' not found in {config_path}"
        )
    
    # Substitute environment variables
    config = all_configs[config_name]
    config = _substitute_env_vars(config)
    
    return config


def _substitute_env_vars(config: dict) -> dict:
    """Replace ${VAR} placeholders with environment variables."""
    import os
    import re
    
    def substitute_value(value):
        if isinstance(value, str):
            # Find ${VAR} pattern
            matches = re.findall(r'\$\{([^}]+)\}', value)
            for match in matches:
                env_value = os.getenv(match)
                if env_value is None:
                    raise ValueError(
                        f"Environment variable {match} not set"
                    )
                value = value.replace(f"${{{match}}}", env_value)
        elif isinstance(value, dict):
            value = {k: substitute_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            value = [substitute_value(v) for v in value]
        return value
    
    return substitute_value(config)


# Usage examples
def get_external_api_config() -> ExternalAPIConfig:
    """Get validated external API configuration."""
    config_dict = load_yaml_config("external_api")
    return ExternalAPIConfig(**config_dict)


def get_feature_flags() -> FeatureFlags:
    """Get feature flags."""
    config_dict = load_yaml_config("features")
    return FeatureFlags(**config_dict)
```

### Usage in Code

```python
from core.config import get_external_api_config, get_feature_flags

# Load external API config
api_config = get_external_api_config()
print(api_config.base_url)
print(api_config.api_key)

# Feature flags
features = get_feature_flags()
if features.enable_caching:
    # Enable caching logic
    pass
```

## Configuration Priority

1. **OS Environment Variables** (highest priority)
2. **.env file** (development override)
3. **Default values in Settings class**
4. **YAML configs** (loaded separately, can reference env vars)

## Best Practices

### 1. Secrets Management

✅ **Good**:
```bash
# .env (not committed)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/db
SECRET_KEY=actual-secret-key
```

```yaml
# config/production.yml
external_api:
  api_key: "${EXTERNAL_API_KEY}"  # Reference env var
```

❌ **Bad**:
```yaml
# config/production.yml
external_api:
  api_key: "hardcoded-secret-key"  # Committed to git!
```

### 2. Environment-Specific Configs

Use `CONFIG_ENV` to switch between files:

```bash
# Development
CONFIG_ENV=development

# Production
CONFIG_ENV=production
```

### 3. Validation

Pydantic validates all settings:

```python
class Settings(BaseSettings):
    PORT: int = Field(gt=0, lt=65536)  # Must be valid port
    LOG_LEVEL: str = Field(pattern="^(DEBUG|INFO|WARNING|ERROR)$")
    DATABASE_URL: str = Field(min_length=1)
```

### 4. Type Safety

```python
# ✅ Type hints everywhere
def configure_database(settings: Settings) -> None:
    engine = create_async_engine(settings.DATABASE_URL)

# ❌ Avoid raw strings
DATABASE_URL = os.getenv("DATABASE_URL")  # No validation!
```

## Testing Configurations

### Override Settings in Tests

```python
# tests/conftest.py
import pytest
from core.config import Settings

@pytest.fixture
def test_settings():
    """Override settings for tests."""
    return Settings(
        DATABASE_URL="postgresql+asyncpg://test:test@localhost/testdb",
        ENVIRONMENT="test",
        DEBUG=True,
        LOG_LEVEL="DEBUG",
    )


def test_something(test_settings):
    assert test_settings.ENVIRONMENT == "test"
```

### Temp .env for Tests

```python
# tests/test_config.py
import pytest
from pathlib import Path

def test_env_loading(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("APP_NAME=Test App\nDEBUG=true")
    
    settings = Settings(_env_file=env_file)
    assert settings.APP_NAME == "Test App"
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Default env vars (override with docker-compose or -e)
ENV ENVIRONMENT=production
ENV LOG_JSON=true

CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://user:password@db:5432/mydb
      ENVIRONMENT: production
      LOG_JSON: "true"
      CONFIG_ENV: production
      SECRET_KEY: ${SECRET_KEY}  # From host environment
    env_file:
      - .env.production  # Additional env vars
```

## Configuration Checklist

- [ ] All secrets in environment variables (not YAML)
- [ ] .env in .gitignore
- [ ] .env.example committed as template
- [ ] Pydantic validation for all settings
- [ ] Type hints on all config classes
- [ ] Environment-specific YAML files
- [ ] ${VAR} substitution for secrets in YAML
- [ ] Singleton pattern for settings (`@lru_cache`)
- [ ] Tests for configuration loading

## Next Steps

- [Logging Patterns](logging-patterns.md) - Use settings for log configuration
- [Database Patterns](database-patterns.md) - DB URL from settings
- [HTTPX Client Patterns](httpx-patterns.md) - External API configs
