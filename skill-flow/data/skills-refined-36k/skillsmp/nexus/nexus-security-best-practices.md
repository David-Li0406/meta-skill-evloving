---
skill: nexus-security-best-practices
description: Security best practices for Nexus including authentication, rate limiting, input validation, and production deployment
priority: HIGH
tags: [nexus, security, authentication, rate-limiting, input-validation, production]
---

# Nexus Security Best Practices

Comprehensive security guide for Nexus v1.1.1+ production deployments.

## Overview

Nexus v1.1.1 includes critical P0 security fixes that provide production-safe defaults. This guide covers best practices for secure deployment and operations.

## Critical Security Fixes (v1.1.1+)

### P0-1: Environment-Aware Authentication
### P0-2: Rate Limiting Default (100 req/min)
### P0-3: Auto-Discovery Disabled by Default
### P0-5: Unified Input Validation

## Authentication Best Practices

### Production Environment Setup

**Recommended Approach** - Use `NEXUS_ENV` for automatic security:

```bash
# .env file
NEXUS_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://redis:6379
```

```python
import os
from nexus import Nexus
from dotenv import load_dotenv

load_dotenv()

# Auto-enables auth in production
app = Nexus()

# Verify auth is enabled
print(f"Auth Enabled: {app._enable_auth}")  # True in production
```

**What Happens**:
- `NEXUS_ENV=production` → Authentication automatically enabled
- `NEXUS_ENV=development` → Authentication disabled (default)
- Explicit `enable_auth=False` in production → **CRITICAL WARNING** logged

### Explicit Authentication Configuration

**Force Enable (Development Testing)**:
```python
# Test auth behavior in development
app = Nexus(enable_auth=True)
```

**Disable in Production (NOT RECOMMENDED)**:
```python
# Logs CRITICAL warning
app = Nexus(enable_auth=False)

# Output:
# ⚠️  SECURITY WARNING: Authentication is DISABLED in production environment!
#    Set enable_auth=True to secure your API endpoints.
#    Your API is exposed to unauthorized access.
```

### Multi-Environment Configuration

**Use environment-specific files**:

```python
# config/base.py
class BaseConfig:
    API_PORT = 8000
    MCP_PORT = 3001
    LOG_LEVEL = "INFO"

# config/development.py
class DevelopmentConfig(BaseConfig):
    ENABLE_AUTH = False
    RATE_LIMIT = None
    AUTO_DISCOVERY = True
    LOG_LEVEL = "DEBUG"

# config/production.py
class ProductionConfig(BaseConfig):
    ENABLE_AUTH = True
    RATE_LIMIT = 1000
    AUTO_DISCOVERY = False
    SESSION_BACKEND = "redis"

# app.py
import os
from nexus import Nexus

env = os.getenv("ENVIRONMENT", "development")
if env == "production":
    from config.production import ProductionConfig as Config
else:
    from config.development import DevelopmentConfig as Config

app = Nexus(
    enable_auth=Config.ENABLE_AUTH,
    rate_limit=Config.RATE_LIMIT,
    auto_discovery=Config.AUTO_DISCOVERY,
    log_level=Config.LOG_LEVEL
)
```

## Rate Limiting Best Practices

### Default Protection (v1.1.1+)

```python
# DoS protection enabled by default
app = Nexus()  # rate_limit=100 req/min

# Verify rate limiting
print(f"Rate Limit: {app._rate_limit} req/min")  # 100
```

### Production Rate Limits

**API Type-Based Limits**:

```python
# High-traffic public API
app = Nexus(rate_limit=1000)  # 1000 req/min

# Internal API
app = Nexus(rate_limit=500)   # 500 req/min

# Admin API
app = Nexus(rate_limit=100)   # 100 req/min (stricter)
```

### Per-Endpoint Rate Limiting

```python
from nexus import Nexus

app = Nexus(rate_limit=100)  # Global default

# Custom limits for specific endpoints
@app.endpoint("/api/search", rate_limit=50)
async def search(q: str):
    """Search with lower rate limit (expensive operation)."""
    return await app._execute_workflow("search", {"query": q})

@app.endpoint("/api/health", rate_limit=1000)
async def health():
    """Health check with higher limit."""
    return {"status": "healthy"}

@app.endpoint("/api/login", rate_limit=10)
async def login(username: str, password: str):
    """Login with very low limit (prevent brute force)."""
    return await app._execute_workflow("authenticate", {
        "username": username,
        "password": password
    })
```

### Rate Limiting Monitoring

```python
# Monitor rate limit hits (example implementation)
@app.middleware("rate_limit_logger")
async def log_rate_limits(request, call_next):
    response = await call_next(request)
    if response.status_code == 429:  # Too Many Requests
        logger.warning(
            f"Rate limit exceeded: {request.client.host} "
            f"-> {request.url.path}"
        )
    return response
```

### When to Disable Rate Limiting

**ONLY disable for**:
- Internal services with existing rate limiting (e.g., behind API gateway)
- Load testing environments
- Development with explicit acknowledgment of risks

```python
# Development only
if os.getenv("ENVIRONMENT") == "development":
    app = Nexus(rate_limit=None)
    logger.warning("Rate limiting DISABLED for development")
else:
    app = Nexus(rate_limit=1000)
```

## Input Validation (v1.1.1+)

### Automatic Validation

**All channels validated**:
- ✅ API endpoints
- ✅ MCP server (stdio, WebSocket)
- ✅ CLI commands

**Protections**:
```python
# These are automatically blocked
dangerous_inputs = {
    "__import__": "blocked",
    "eval": "blocked",
    "exec": "blocked",
    "compile": "blocked",
    "globals": "blocked",
    "locals": "blocked",
    "__builtins__": "blocked"
}

# Path traversal blocked
path_traversal = {
    "../etc/passwd": "blocked",
    "..\\windows\\system32": "blocked",
    "/etc/shadow": "blocked"
}

# Size limits enforced
large_input = "x" * (10 * 1024 * 1024 + 1)  # > 10MB: blocked
```

### Custom Input Size Limits

```python
# Default: 10MB
app = Nexus()

# Increase for file uploads
app._max_input_size = 50 * 1024 * 1024  # 50MB

# Decrease for strict APIs
app._max_input_size = 1 * 1024 * 1024   # 1MB
```

### Validation Error Handling

```python
from nexus.validation import validate_workflow_inputs
from nexus.exceptions import ValidationError

# Validation happens automatically, but you can also use it explicitly
try:
    validate_workflow_inputs(user_inputs, max_size=10*1024*1024)
except ValidationError as e:
    logger.error(f"Invalid input: {e}")
    # Return 400 Bad Request
```

## Production Deployment Security

### Checklist

**Before deploying to production**:

- [ ] Set `NEXUS_ENV=production` environment variable
- [ ] Configure authentication (`enable_auth=True` or auto-enabled)
- [ ] Set appropriate rate limits (default 100 req/min)
- [ ] Disable auto-discovery (`auto_discovery=False`)
- [ ] Use Redis for session management
- [ ] Enable HTTPS/TLS
- [ ] Configure secure secrets management
- [ ] Enable monitoring and logging
- [ ] Set up health checks
- [ ] Configure firewall rules
- [ ] Review input size limits
- [ ] Test security configurations

### Secure Configuration Example

```python
import os
from nexus import Nexus

# Load secrets from environment
def get_secret(key: str) -> str:
    """Get secret from environment or secret manager."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required secret: {key}")
    return value

# Production configuration
app = Nexus(
    # Server
    api_port=int(os.getenv("PORT", "8000")),
    api_host="0.0.0.0",

    # Security (P0 fixes)
    enable_auth=True,          # P0-1: Explicit enable
    rate_limit=1000,           # P0-2: DoS protection
    auto_discovery=False,      # P0-3: No blocking

    # TLS/HTTPS (if not behind reverse proxy)
    force_https=True,
    ssl_cert=get_secret("SSL_CERT_PATH"),
    ssl_key=get_secret("SSL_KEY_PATH"),

    # Sessions
    session_backend="redis",
    redis_url=get_secret("REDIS_URL"),
    session_timeout=3600,

    # Monitoring
    enable_monitoring=True,
    monitoring_backend="prometheus",
    monitoring_interval=30,

    # Logging
    log_level="INFO",
    log_format="json",
    log_file="/var/log/nexus/app.log",

    # Performance
    max_concurrent_workflows=200,
    request_timeout=60,
    enable_caching=True
)

# Verify security configuration
def verify_security():
    """Verify all security measures are active."""
    assert app._enable_auth, "Authentication MUST be enabled"
    assert app._rate_limit is not None, "Rate limiting MUST be enabled"
    assert not app._auto_discovery, "Auto-discovery MUST be disabled"
    assert app._session_backend == "redis", "Redis MUST be used for sessions"
    print("✅ Security configuration verified")

verify_security()
```

### Docker Security

**Dockerfile Best Practices**:

```dockerfile
FROM python:3.11-slim

# Security: Create non-root user
RUN useradd -m -u 1000 nexus && \
    mkdir -p /app /var/log/nexus && \
    chown -R nexus:nexus /app /var/log/nexus

WORKDIR /app

# Security: Install dependencies as non-root
COPY --chown=nexus:nexus requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=nexus:nexus . .

# Security: Set production environment
ENV NEXUS_ENV=production

# Security: Drop to non-root user
USER nexus

# Expose ports
EXPOSE 8000 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

### Kubernetes Security

**Security Context**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
spec:
  replicas: 3
  template:
    spec:
      # Security: Pod-level security
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      containers:
      - name: nexus
        image: nexus-app:latest

        # Security: Container-level security
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true

        env:
        - name: NEXUS_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: redis-url

        ports:
        - containerPort: 8000
          name: api
        - containerPort: 3001
          name: mcp

        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"

        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring Security Events

### Logging Security Events

```python
import logging

# Configure security-focused logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('/var/log/nexus/security.log'),
        logging.StreamHandler()
    ]
)

security_logger = logging.getLogger('nexus.security')

# Log security events
security_logger.critical("Authentication disabled in production")
security_logger.warning("Rate limit exceeded for IP: 1.2.3.4")
security_logger.info("Dangerous input blocked: __import__")
```

### Metrics to Monitor

**Key security metrics**:

1. **Authentication Failures**
   - Failed login attempts
   - Invalid token usage
   - Unauthorized access attempts

2. **Rate Limiting**
   - 429 (Too Many Requests) responses
   - Per-endpoint rate limit hits
   - Per-IP rate limit violations

3. **Input Validation**
   - Dangerous key detection count
   - Input size limit violations
   - Path traversal attempt count

4. **System Health**
   - Auth service availability
   - Redis session store health
   - Database connection status

### Prometheus Metrics Example

```python
from prometheus_client import Counter, Histogram

# Security metrics
auth_failures = Counter('nexus_auth_failures_total', 'Authentication failures')
rate_limit_hits = Counter('nexus_rate_limit_hits_total', 'Rate limit violations')
input_validation_blocks = Counter('nexus_input_blocked_total', 'Blocked inputs')

# Track security events
auth_failures.inc()
rate_limit_hits.inc()
input_validation_blocks.inc()
```

## Common Security Mistakes

### ❌ Mistake 1: Disabling Auth in Production

```python
# WRONG - Logs CRITICAL warning
app = Nexus(enable_auth=False)
```

**Fix**:
```python
# RIGHT - Use environment variable
export NEXUS_ENV=production
app = Nexus()  # Auth auto-enabled
```

### ❌ Mistake 2: No Rate Limiting

```python
# WRONG - Vulnerable to DoS
app = Nexus(rate_limit=None)
```

**Fix**:
```python
# RIGHT - Use appropriate limits
app = Nexus(rate_limit=1000)  # Or use default 100
```

### ❌ Mistake 3: Auto-Discovery in Production

```python
# WRONG - 5-10s blocking delay, potential security risk
app = Nexus(auto_discovery=True)
```

**Fix**:
```python
# RIGHT - Manual registration
app = Nexus(auto_discovery=False)
app.register("workflow_name", workflow.build())
```

### ❌ Mistake 4: Storing Secrets in Code

```python
# WRONG - Secrets in version control
app = Nexus(
    redis_url="redis://user:password123@host:6379"
)
```

**Fix**:
```python
# RIGHT - Use environment variables
import os
app = Nexus(
    redis_url=os.getenv("REDIS_URL")
)
```

### ❌ Mistake 5: No HTTPS in Production

```python
# WRONG - Plaintext HTTP
app = Nexus(force_https=False)
```

**Fix**:
```python
# RIGHT - Force HTTPS
app = Nexus(
    force_https=True,
    ssl_cert="/path/to/cert.pem",
    ssl_key="/path/to/key.pem"
)
# Or use reverse proxy (nginx, traefik)
```

## Security Checklist

### Development

- [ ] Understand security defaults (v1.1.1+)
- [ ] Use environment-specific configurations
- [ ] Test authentication flows
- [ ] Verify rate limiting behavior
- [ ] Test input validation with edge cases

### Staging

- [ ] Set `NEXUS_ENV=staging` or `production`
- [ ] Enable authentication
- [ ] Configure appropriate rate limits
- [ ] Test with production-like data
- [ ] Verify security warnings/errors

### Production

- [ ] Set `NEXUS_ENV=production`
- [ ] **REQUIRED**: Enable authentication
- [ ] **REQUIRED**: Configure rate limiting (≥100 req/min)
- [ ] **REQUIRED**: Disable auto-discovery
- [ ] Use Redis for sessions
- [ ] Enable HTTPS/TLS
- [ ] Configure monitoring
- [ ] Set up alerting
- [ ] Review logs regularly
- [ ] Implement secret rotation
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Test disaster recovery

## Version History

### v1.1.1 (2025-10-24)

**P0 Security Fixes**:
- P0-1: Environment-aware authentication (auto-enable in production)
- P0-2: Rate limiting default (100 req/min)
- P0-3: Auto-discovery disabled by default
- P0-5: Unified input validation (all channels)

**Impact**:
- Production deployments now secure by default
- DoS protection enabled automatically
- No blocking delays with DataFlow
- Input validation prevents code injection

### Pre-v1.1.1

**Security Risks**:
- ❌ No authentication by default
- ❌ No rate limiting by default
- ❌ Auto-discovery enabled (blocking, security risk)
- ❌ Inconsistent input validation

**Recommendation**: Upgrade to v1.1.1+ immediately.

## Additional Resources

### Related Skills

- [nexus-config-options](./nexus-config-options.md) - Configuration reference
- [nexus-production-deployment](./nexus-production-deployment.md) - Deployment guide
- [nexus-quickstart](./nexus-quickstart.md) - Getting started

### Security Documentation

- Authentication strategies
- Rate limiting algorithms
- Input validation rules
- Security monitoring
- Incident response

### External Resources

- OWASP API Security Top 10
- NIST Cybersecurity Framework
- Docker Security Best Practices
- Kubernetes Security Best Practices

## Key Takeaways

1. **v1.1.1+ provides secure defaults** - Use them
2. **Set `NEXUS_ENV=production`** - Auto-enables security
3. **Never disable auth in production** - Critical security risk
4. **Use rate limiting** - Prevents DoS attacks
5. **Disable auto-discovery** - Prevents blocking and security risks
6. **Input validation is automatic** - No configuration needed
7. **Monitor security events** - Log and alert on violations
8. **Use environment variables** - Never hardcode secrets
9. **Enable HTTPS** - Protect data in transit
10. **Regular security audits** - Stay ahead of threats

## Support

For security issues or questions:
- Check the [troubleshooting guide](./nexus-troubleshooting.md)
- Review [GitHub issues](https://github.com/kailash-sdk/nexus/issues)
- Contact security team for critical vulnerabilities
