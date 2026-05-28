# Advanced YAML Patterns

## Table of Contents

- [Overview](#overview)
- [Nested Configuration Structures](#nested-configuration-structures)
- [Complex Data Types](#complex-data-types)
- [Specialized Patterns](#specialized-patterns)
- [Validation Patterns](#validation-patterns)
- [Environment-Specific Configuration](#environment-specific-configuration)
- [Dynamic Configuration](#dynamic-configuration)
- [Best Practices](#best-practices)
- [Advanced Parsing Examples](#advanced-parsing-examples)

## Overview

This guide covers advanced YAML patterns for plugin settings, including nested structures, complex types, and specialized configurations.

## Nested Configuration Structures

### Multi-Level Nesting

```yaml
---
# Environment-specific configuration
environment:
  development:
    debug: true
    log_level: debug
    database:
      host: localhost
      port: 5432
      pool_size: 5
  
  staging:
    debug: false
    log_level: info
    database:
      host: db.staging.example.com
      port: 5432
      pool_size: 10
  
  production:
    debug: false
    log_level: warning
    database:
      host: db.prod.example.com
      port: 5432
      pool_size: 20
      ssl_mode: require
---

Development environment configuration with local database.
```

### Feature Flags

```yaml
---
# Feature toggles
features:
  authentication:
    enabled: true
    method: jwt
    expiry_seconds: 3600
  
  caching:
    enabled: true
    ttl_seconds: 300
    backend: redis
  
  analytics:
    enabled: false
    provider: google_analytics
    tracking_id: null
  
  experimental:
    new_ui: false
    beta_features: false
---

Feature flags for enabling/disabling functionality.
```

### Plugin Ecosystem Configuration

```yaml
---
# Inter-plugin communication
plugins:
  auth_service:
    enabled: true
    connection_string: "plugin://auth-service"
    timeout_seconds: 30
  
  notification_service:
    enabled: true
    channels:
      - slack
      - email
      - webhook
    webhook_url: "${SLACK_WEBHOOK_URL}"
  
  database_migrations:
    enabled: true
    auto_apply: false
    require_approval: true
---

Cross-plugin integration settings.
```

## Complex Data Types

### Multi-Type Arrays

```yaml
---
# Mixed-type array (can use in Python, not pure YAML)
# In YAML, use explicit typing or tags
settings_list:
  - type: string
    value: "database_config"
  - type: integer
    value: 42
  - type: boolean
    value: true
  - type: array
    value: [1, 2, 3]

# Alternative: Tagged values
settings_typed:
  str_field: !!str "42"  # Force string type
  int_field: !!int "42"  # Force integer type
  bool_field: !!bool "true"  # Force boolean
---

Multi-type array with explicit typing.
```

### Maps with Dynamic Keys

```yaml
---
# Dynamic key mapping
api_endpoints:
  user_service:
    url: "https://api.example.com/users"
    timeout: 30
    retry_count: 3
  
  order_service:
    url: "https://api.example.com/orders"
    timeout: 60
    retry_count: 5

# Conditional keys
conditional_config:
  production:
    database_url: "postgresql://..."
    redis_url: "redis://..."
  development:
    database_url: "sqlite:///:memory:"
    redis_url: null
---

Dynamic endpoint configuration.
```

### Merge and Alias References

```yaml
---
# Base configuration
default_settings: &default_settings
  timeout: 30
  retry_count: 3
  log_level: info

# Inherited configuration
api_config:
  <<: *default_settings
  url: "https://api.example.com"
  timeout: 60  # Override

# Multiple inheritance
service_base: &service_base
  auth_required: true
  ssl_verify: true

user_service:
  <<: *service_base
  endpoint: "/users"

order_service:
  <<: *service_base
  endpoint: "/orders"
---

YAML anchors and aliases for reusability.
```

## Specialized Patterns

### Time-Based Configuration

```yaml
---
# Time-based settings
scheduling:
  cleanup_interval: "24h"
  backup_schedule: "0 2 * * *"  # Cron format
  maintenance_window:
    start: "02:00"
    end: "04:00"
    timezone: "UTC"

# Relative times
timeouts:
  short: "30s"
  medium: "5m"
  long: "1h"

# Duration parsing (in scripts)
# Use: parse_duration() function
---

Time-based configuration with intervals.
```

### Resource Limits

```yaml
---
# Resource constraints
limits:
  memory:
    max_mb: 1024
    warning_threshold: 768
  
  cpu:
    max_percent: 80
    warning_threshold: 70
  
  disk:
    max_gb: 10
    warning_threshold: 8
    cleanup_threshold: 9
  
  network:
    max_connections: 100
    rate_limit: "1000/hour"

# Quota management
quotas:
  daily:
    api_calls: 10000
    storage_mb: 5120
  
  monthly:
    api_calls: 100000
    storage_gb: 50
---

Resource allocation and limits.
```

### Security Configuration

```yaml
---
# Security settings
security:
  encryption:
    algorithm: "AES-256"
    key_rotation_days: 90
  
  authentication:
    methods:
      - jwt
      - oauth2
    session_timeout: "8h"
    max_failed_attempts: 5
  
  authorization:
    rbac_enabled: true
    default_role: "viewer"
    roles:
      admin:
        permissions: ["read", "write", "delete"]
      editor:
        permissions: ["read", "write"]
      viewer:
        permissions: ["read"]
  
  network:
    allowed_hosts:
      - "https://api.example.com"
      - "https://admin.example.com"
    blocked_ips:
      - "192.168.1.100"
  
  audit:
    enabled: true
    log_level: "info"
    retention_days: 90
---

Comprehensive security configuration.
```

### Monitoring and Observability

```yaml
---
# Monitoring setup
monitoring:
  metrics:
    enabled: true
    collection_interval: "60s"
    export_format: "prometheus"
    endpoint: "http://prometheus:9090"
  
  logging:
    level: "info"
    format: "json"
    outputs:
      - type: "file"
        path: "/var/log/app.log"
        max_size_mb: 100
        rotate_count: 10
      - type: "stdout"
        level: "debug"
  
  tracing:
    enabled: true
    jaeger_endpoint: "http://jaeger:14268/api/traces"
    sampling_rate: 0.1
  
  alerts:
    enabled: true
    channels:
      email:
        - "ops@example.com"
      slack:
        webhook: "${SLACK_ALERTS_WEBHOOK}"
    
    rules:
      - name: "high_error_rate"
        condition: "error_rate > 5%"
        duration: "5m"
        severity: "critical"
      - name: "high_latency"
        condition: "p95_latency > 1s"
        duration: "10m"
        severity: "warning"
---

Monitoring and observability configuration.
```

## Validation Patterns

### Schema Definition

```yaml
---
# Schema version for tracking
schema_version: "2.0.0"

# Field definitions with types
fields:
  enabled:
    type: boolean
    required: true
    default: true
  
  mode:
    type: string
    required: true
    allowed_values: ["strict", "standard", "lenient"]
    default: "standard"
  
  timeout:
    type: integer
    required: false
    min_value: 1
    max_value: 3600
    default: 30
  
  allowed_hosts:
    type: array
    required: false
    items_type: string
    pattern: "^https?://"
  
  retry_policy:
    type: object
    required: false
    fields:
      max_attempts:
        type: integer
        min: 0
        max: 10
        default: 3
      backoff_multiplier:
        type: number
        min: 1.0
        default: 2.0
---

Schema validation definition.
```

### Conditional Validation

```yaml
---
# Conditional requirements
validation_rules:
  # Rule 1: Production requires strict mode
  - condition: "environment == 'production'"
    requires: 
      - field: "mode"
        value: "strict"
  
  # Rule 2: SSL required for production
  - condition: "environment == 'production'"
    requires:
      - field: "ssl_enabled"
        value: true
  
  # Rule 3: OAuth requires client credentials
  - condition: "auth_method == 'oauth2'"
    requires:
      - field: "oauth_client_id"
      - field: "oauth_client_secret"
  
  # Rule 4: Redis caching requires Redis URL
  - condition: "caching.enabled == true"
    requires:
      - field: "redis_url"
---

Conditional validation rules.
```

### Cross-Field Validation

```yaml
---
# Cross-reference validation
validation:
  # Timeout must be less than max_execution_time
  - field: "timeout"
    constraint: "timeout < max_execution_time"
    message: "Timeout must be less than max_execution_time"
  
  # Retry attempts must be positive
  - field: "retry_count"
    constraint: "retry_count >= 0"
    message: "Retry count cannot be negative"
  
  # Email list must be valid emails
  - field: "notification_emails"
    constraint: "all(item matches email_pattern)"
    message: "All emails must be valid"

# Email pattern (used in validation)
email_pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
---

Cross-field validation constraints.
```

## Environment-Specific Configuration

### Hierarchical Overrides

```yaml
---
# Base configuration
base: &base_config
  debug: false
  log_level: info
  timeout: 30
  retry_count: 3

# Development overrides
development:
  <<: *base_config
  debug: true
  log_level: debug
  timeout: 60  # Override base value

# Staging inherits from base
staging:
  <<: *base_config
  log_level: info

# Production overrides
production:
  <<: *base_config
  debug: false
  timeout: 120
  retry_count: 5

# Active environment
environment: development

# Environment selection
config:
  <<: *base_config
  # Select environment-specific config
  <<: *development  # Or: *staging, *production
---

Hierarchical configuration with environment inheritance.
```

### Environment Variable Substitution

```yaml
---
# Database configuration with env vars
database:
  url: "${DATABASE_URL}"
  host: "${DB_HOST:-localhost}"  # Default if not set
  port: "${DB_PORT:-5432}"
  username: "${DB_USER}"
  password: "${DB_PASSWORD}"
  ssl_mode: "${DB_SSL_MODE:-disable}"

# API configuration
api:
  key: "${API_KEY}"  # Required
  secret: "${API_SECRET}"  # Required
  base_url: "${API_BASE_URL:-https://api.example.com}"

# Optional configuration with defaults
cache:
  enabled: "${CACHE_ENABLED:-true}"
  ttl_seconds: "${CACHE_TTL:-300}"
  redis_url: "${REDIS_URL}"

# Sensitive data (should be in env vars, not file)
secrets:
  jwt_secret: "${JWT_SECRET}"
  encryption_key: "${ENCRYPTION_KEY}"
---

Environment variable substitution with defaults.
```

## Dynamic Configuration

### Runtime Updates

```yaml
---
# Dynamic configuration management
runtime:
  # Hot-reload settings
  hot_reload: true
  watch_file: ".claude/my-plugin.local.md"
  reload_debounce_seconds: 5
  
  # Configuration versioning
  version: "1"
  last_updated: "2026-01-20T10:30:00Z"
  
  # Change tracking
  changes:
    - timestamp: "2026-01-20T10:30:00Z"
      field: "timeout"
      old_value: 30
      new_value: 60
      reason: "Performance issue"
  
  # Backup of previous config
  previous_config:
    timeout: 30
    mode: "standard"
---

Runtime configuration management.
```

### Feature Rollout

```yaml
---
# Feature rollout configuration
rollout:
  features:
    new_ui:
      enabled: true
      rollout_percentage: 50
      start_date: "2026-01-20"
      end_date: "2026-02-20"
      target_users: ["beta_testers", "early_adopters"]
    
    advanced_analytics:
      enabled: false
      rollout_percentage: 0
      requires_approval: true
  
  # Gradual rollout rules
  gradual_rollout:
    enabled: true
    increment_percentage: 10
    evaluation_period_days: 7
    success_criteria:
      - metric: "error_rate"
        threshold: "< 1%"
      - metric: "user_satisfaction"
        threshold: "> 4.0"

# A/B testing configuration
experiments:
  - name: "new_dashboard"
    variants:
      control:
        percentage: 50
        config:
          dashboard_version: "v1"
      treatment:
        percentage: 50
        config:
          dashboard_version: "v2"
    metrics:
      - "conversion_rate"
      - "task_completion_time"
    duration_days: 30
---

Feature rollout and A/B testing configuration.
```

## Best Practices

### 1. Use Meaningful Structure

```yaml
# Good: Logical grouping
authentication:
  method: jwt
  timeout: 3600
  refresh_token: true

# Bad: Flat structure
auth_method: jwt
auth_timeout: 3600
auth_refresh: true
```

### 2. Provide Defaults

```yaml
---
timeout: 30  # Has default
mode: standard  # Has default
# logging: not specified, use hardcoded default
```

### 3. Document Complex Fields

```yaml
---
# Cron expression for scheduled tasks
# Format: second minute hour day month weekday
cleanup_schedule: "0 2 * * *"  # Daily at 2 AM

# Duration format
# Use: number + unit (s=seconds, m=minutes, h=hours, d=days)
cache_ttl: "5m"  # 5 minutes
session_timeout: "8h"  # 8 hours
---

See README for duration and cron format specifications.
```

### 4. Validate Before Use

```bash
#!/bin/bash
validate_config() {
    local config_file="$1"
    
    # Check YAML syntax
    if ! python3 -c "import yaml; yaml.safe_load(open('$config_file'))"; then
        echo "❌ Invalid YAML syntax" >&2
        return 1
    fi
    
    # Check required fields
    if [[ "$(yq eval '.enabled' "$config_file")" == "null" ]]; then
        echo "⚠️ Missing 'enabled' field, defaulting to true" >&2
    fi
    
    return 0
}
```

### 5. Keep Secrets in Environment

```yaml
# Good: Reference environment variable
database:
  url: "${DATABASE_URL}"

# Bad: Hardcoded secret
database:
  url: "postgresql://user:password@host/db"
```

## Advanced Parsing Examples

### Python Complex Parser

```python
#!/usr/bin/env python3
import yaml
from typing import Any, Dict, List, Optional, Union

class AdvancedConfigParser:
    """Advanced configuration parser with validation."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = {}
        self.body = ""
        self.load()
    
    def load(self):
        """Load and parse configuration file."""
        with open(self.file_path, 'r') as f:
            content = f.read()
        
        if content.startswith('---'):
            _, frontmatter, self.body = content.split('---', 2)
            self.config = yaml.safe_load(frontmatter) or {}
        else:
            self.config = {}
            self.body = content
    
    def get_nested(self, path: str, default: Any = None) -> Any:
        """Get nested value using dot notation."""
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_typed(self, path: str, expected_type: type, default: Any = None) -> Any:
        """Get value with type validation."""
        value = self.get_nested(path, default)
        
        if value is None:
            return default
        
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type.__name__} for {path}, got {type(value).__name__}")
        
        return value
    
    def validate_schema(self, schema: Dict[str, Any]):
        """Validate configuration against schema."""
        errors = []
        
        for field, rules in schema.items():
            value = self.get_nested(field)
            
            # Required check
            if rules.get('required', False) and value is None:
                errors.append(f"Required field '{field}' is missing")
                continue
            
            if value is None:
                continue
            
            # Type check
            if 'type' in rules:
                expected_type = rules['type']
                if not isinstance(value, expected_type):
                    errors.append(f"Field '{field}' must be of type {expected_type.__name__}")
            
            # Range check
            if isinstance(value, (int, float)):
                if 'min' in rules and value < rules['min']:
                    errors.append(f"Field '{field}' must be >= {rules['min']}")
                if 'max' in rules and value > rules['max']:
                    errors.append(f"Field '{field}' must be <= {rules['max']}")
            
            # Pattern check
            if 'pattern' in rules and isinstance(value, str):
                import re
                if not re.match(rules['pattern'], value):
                    errors.append(f"Field '{field}' does not match pattern {rules['pattern']}")
        
        return errors

# Usage
parser = AdvancedConfigParser('.claude/my-plugin.local.md')

# Get nested value
db_host = parser.get_nested('database.host', 'localhost')

# Get typed value
timeout = parser.get_typed('timeout', int, 30)

# Validate against schema
schema = {
    'enabled': {'type': bool, 'required': True},
    'timeout': {'type': int, 'min': 1, 'max': 3600},
    'mode': {'type': str, 'allowed_values': ['strict', 'standard', 'lenient']}
}

errors = parser.validate_schema(schema)
if errors:
    print("Configuration errors:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    sys.exit(1)
```

### yq Complex Queries

```bash
#!/bin/bash
# Get environment-specific config
get_env_config() {
    local env="$1"
    local field="$2"
    
    yq eval ".${env}.${field} // .base.${field} // null" "$STATE_FILE"
}

# Check if field exists and has value
check_condition() {
    local path="$1"
    local expected="$2"
    
    local actual
    actual=$(yq eval "$path" "$STATE_FILE")
    
    [[ "$actual" == "$expected" ]]
}

# Complex conditional logic
if check_condition ".security.encryption.enabled" "true"; then
    ALGORITHM=$(yq eval ".security.encryption.algorithm" "$STATE_FILE")
    echo "Encryption enabled with algorithm: $ALGORITHM"
fi

# Merge configurations
BASE_CONFIG=$(yq eval '.base' "$STATE_FILE")
ENV_CONFIG=$(yq eval ".${ENVIRONMENT:-development}" "$STATE_FILE")
MERGED=$(echo -e "$BASE_CONFIG\n$ENV_CONFIG" | yq eval '. *d .' -)

echo "Merged config: $MERGED"
```

These advanced patterns provide powerful ways to structure, validate, and manage complex plugin configurations while maintaining readability and maintainability.
