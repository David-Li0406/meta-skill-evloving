---
skill: nexus-enterprise-features
description: Enterprise features including authentication, authorization, rate limiting, monitoring
priority: MEDIUM
tags: [nexus, enterprise, auth, security, monitoring]
---

# Nexus Enterprise Features

Production-grade features for enterprise deployments.

## Authentication

### Enable Authentication

```python
from nexus import Nexus

app = Nexus(enable_auth=True)

# Configure authentication strategy
app.auth.strategy = "oauth2"       # oauth2, jwt, api_key, saml
app.auth.provider = "google"       # google, github, auth0, custom
app.auth.token_expiry = 3600       # 1 hour
app.auth.refresh_enabled = True
```

### OAuth2 Configuration

```python
app.auth.configure(
    provider="oauth2",
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    authorization_url="https://accounts.google.com/o/oauth2/auth",
    token_url="https://oauth2.googleapis.com/token",
    redirect_uri="http://localhost:8000/auth/callback"
)
```

### API Key Authentication

```python
app.auth.strategy = "api_key"
app.auth.api_keys = [
    {"key": "key123", "name": "Service A", "permissions": ["read", "write"]},
    {"key": "key456", "name": "Service B", "permissions": ["read"]}
]

# Use with API
curl -X POST http://localhost:8000/workflows/test/execute \
  -H "X-API-Key: key123" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {}}'
```

### JWT Authentication

```python
app.auth.strategy = "jwt"
app.auth.jwt_secret = os.getenv("JWT_SECRET")
app.auth.jwt_algorithm = "HS256"

# Use with API
curl -X POST http://localhost:8000/workflows/test/execute \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {}}'
```

## Authorization (RBAC)

```python
# Define roles and permissions
app.auth.rbac_enabled = True
app.auth.roles = {
    "admin": ["workflows:*"],
    "developer": ["workflows:read", "workflows:execute"],
    "viewer": ["workflows:read"]
}

# Assign roles to users
app.auth.assign_role("user123", "developer")

# Check permissions
@app.require_permission("workflows:execute")
def execute_workflow(workflow_name, inputs):
    return app.execute_workflow(workflow_name, inputs)
```

## Rate Limiting

### Basic Rate Limiting

```python
app = Nexus(
    enable_rate_limiting=True,
    rate_limit=1000,  # Requests per minute
    rate_limit_burst=100  # Burst capacity
)
```

### Per-User Rate Limiting

```python
app.rate_limiter.strategy = "per_user"
app.rate_limiter.limits = {
    "default": {"requests": 100, "window": 60},
    "premium": {"requests": 1000, "window": 60},
    "admin": {"requests": 10000, "window": 60}
}
```

### Custom Rate Limiting

```python
@app.rate_limit_handler
def custom_rate_limit(request):
    user = request.user
    if user.is_premium:
        return {"requests": 1000, "window": 60}
    return {"requests": 100, "window": 60}
```

## Circuit Breaker

```python
app = Nexus(enable_circuit_breaker=True)

# Configure circuit breaker
app.circuit_breaker.failure_threshold = 5  # Open after 5 failures
app.circuit_breaker.timeout = 60  # Try again after 60 seconds
app.circuit_breaker.half_open_max_calls = 3  # Test with 3 requests

# Per-workflow circuit breaker
app.circuit_breaker.enable_for_workflow("critical-workflow")
```

## Monitoring and Observability

### Prometheus Integration

```python
app = Nexus(
    enable_monitoring=True,
    monitoring_backend="prometheus"
)

# Metrics endpoint
# GET http://localhost:8000/metrics
```

### OpenTelemetry Integration

```python
app.monitoring.backend = "opentelemetry"
app.monitoring.otlp_endpoint = "http://localhost:4317"
app.monitoring.service_name = "nexus-platform"

# Distributed tracing
app.monitoring.enable_tracing = True
app.monitoring.trace_sampling_rate = 0.1  # 10% sampling
```

### Custom Metrics

```python
# Define custom metrics
app.monitoring.register_metric(
    name="workflow_custom_metric",
    type="counter",
    description="Custom workflow metric"
)

# Increment metric
app.monitoring.increment("workflow_custom_metric", labels={"workflow": "my-workflow"})
```

## Caching

```python
app = Nexus(enable_caching=True)

# Configure cache backend
app.cache.backend = "redis"
app.cache.redis_url = os.getenv("REDIS_URL")
app.cache.default_ttl = 300  # 5 minutes

# Per-workflow caching
app.cache.enable_for_workflow("expensive-workflow", ttl=600)

# Cache invalidation
app.cache.invalidate("workflow-name")
app.cache.invalidate_all()
```

## Load Balancing

```python
# Configure multi-instance deployment
app.configure_load_balancing({
    "api": {
        "instances": 3,
        "health_check": "/health",
        "strategy": "round_robin"
    },
    "mcp": {
        "instances": 2,
        "strategy": "least_connections"
    }
})
```

## High Availability

```python
# Configure for HA
app = Nexus(
    # Distributed sessions
    session_backend="redis",
    redis_url=os.getenv("REDIS_URL"),

    # Health checks
    health_check_interval=30,
    enable_readiness_probe=True,
    enable_liveness_probe=True,

    # Graceful shutdown
    graceful_shutdown_timeout=30,

    # Connection pooling
    connection_pool_size=20,
    connection_pool_timeout=30
)
```

## Security Hardening

```python
# Enable security features
app = Nexus(
    # HTTPS only
    force_https=True,
    ssl_cert="/path/to/cert.pem",
    ssl_key="/path/to/key.pem",

    # Security headers
    enable_security_headers=True,

    # CORS
    enable_cors=True,
    cors_origins=["https://app.example.com"],
    cors_credentials=True,

    # Request validation
    enable_request_validation=True,
    max_request_size=10 * 1024 * 1024,  # 10MB

    # Rate limiting
    enable_rate_limiting=True,

    # Authentication
    enable_auth=True
)

# Additional security
app.security.enable_csrf_protection = True
app.security.enable_xss_protection = True
app.security.enable_content_security_policy = True
```

## Audit Logging

```python
app = Nexus(enable_audit_logging=True)

# Configure audit log
app.audit.log_file = "/var/log/nexus/audit.log"
app.audit.log_format = "json"
app.audit.log_events = [
    "workflow_execute",
    "workflow_register",
    "user_login",
    "user_logout",
    "permission_denied"
]

# Custom audit handler
@app.on_audit_event
def handle_audit(event):
    print(f"AUDIT: {event.type} by {event.user} at {event.timestamp}")
    # Send to SIEM system
```

## Backup and Recovery

```python
# Backup configuration
app.backup.enable_auto_backup = True
app.backup.backup_interval = 3600  # Every hour
app.backup.backup_location = "/backups/nexus"
app.backup.retention_days = 7

# Manual backup
app.backup.create_backup("manual-backup-2024-01")

# Restore from backup
app.backup.restore("backup-2024-01-15")
```

## Production Deployment Example

```python
import os

def create_production_app():
    app = Nexus(
        # Server
        api_port=int(os.getenv("PORT", "8000")),
        api_host="0.0.0.0",

        # Security
        enable_auth=True,
        enable_rate_limiting=True,
        rate_limit=5000,
        force_https=True,
        ssl_cert=os.getenv("SSL_CERT_PATH"),
        ssl_key=os.getenv("SSL_KEY_PATH"),

        # Performance
        max_concurrent_workflows=200,
        enable_caching=True,
        enable_circuit_breaker=True,

        # Monitoring
        enable_monitoring=True,
        monitoring_backend="prometheus",
        enable_audit_logging=True,

        # High Availability
        session_backend="redis",
        redis_url=os.getenv("REDIS_URL"),
        health_check_interval=30,

        # Logging
        log_level="INFO",
        log_format="json",
        log_file="/var/log/nexus/app.log",

        # Discovery
        auto_discovery=False
    )

    # Configure components
    app.auth.strategy = "oauth2"
    app.auth.provider = "auth0"
    app.monitoring.enable_tracing = True
    app.cache.default_ttl = 300

    return app

# Create and start
app = create_production_app()
```

## Best Practices

1. **Enable Authentication** in production
2. **Use HTTPS** for all traffic
3. **Configure Rate Limiting** appropriately
4. **Enable Monitoring and Alerting**
5. **Use Redis for Distributed Sessions**
6. **Implement Circuit Breakers** for resilience
7. **Enable Audit Logging** for compliance
8. **Regular Security Audits**
9. **Backup Configuration** regularly
10. **Test Disaster Recovery** procedures

## Key Takeaways

- Enterprise features available out-of-the-box
- Multiple authentication strategies supported
- RBAC for fine-grained access control
- Rate limiting prevents abuse
- Circuit breakers improve resilience
- Comprehensive monitoring and observability
- Production-ready security hardening

## Related Skills

- [nexus-config-options](#) - Configuration reference
- [nexus-production-deployment](#) - Deploy to production
- [nexus-health-monitoring](#) - Monitor production
- [nexus-troubleshooting](#) - Fix production issues
