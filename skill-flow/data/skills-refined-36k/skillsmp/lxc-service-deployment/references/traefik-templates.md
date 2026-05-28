# Traefik Configuration Templates

## Router Template (routers.yml)

Add new routers to `/etc/traefik/dynamic/routers.yml`:

```yaml
http:
  routers:
    # Basic router - most services
    service-name-router:
      rule: "Host(`service-name.internal.lakehouse.wtf`)"
      entryPoints:
        - websecure
      service: service-name-service
      tls:
        certResolver: cloudflare

    # Router with middleware (security headers, etc.)
    service-name-router:
      rule: "Host(`service-name.internal.lakehouse.wtf`)"
      entryPoints:
        - websecure
      service: service-name-service
      middlewares:
        - secure-headers
      tls:
        certResolver: cloudflare

    # Router with path prefix
    service-name-router:
      rule: "Host(`service-name.internal.lakehouse.wtf`) && PathPrefix(`/api`)"
      entryPoints:
        - websecure
      service: service-name-service
      tls:
        certResolver: cloudflare
```

## Service Template (services.yml)

Add new services to `/etc/traefik/dynamic/services.yml`:

```yaml
http:
  services:
    # Basic service
    service-name-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.XXX:PORT"

    # Service with health check
    service-name-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.XXX:PORT"
        healthCheck:
          path: /health
          interval: 30s
          timeout: 5s

    # Service with sticky sessions
    service-name-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.XXX:PORT"
        sticky:
          cookie:
            name: service_session

    # Service with multiple backends (HA)
    service-name-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.XXX:PORT"
          - url: "http://192.168.1.YYY:PORT"
        healthCheck:
          path: /health
          interval: 10s
```

## Common Middleware (middlewares.yml)

```yaml
http:
  middlewares:
    # Security headers
    secure-headers:
      headers:
        stsSeconds: 31536000
        stsIncludeSubdomains: true
        stsPreload: true
        forceSTSHeader: true
        customFrameOptionsValue: "SAMEORIGIN"
        contentTypeNosniff: true
        browserXssFilter: true

    # Allow iframes (for dashboards)
    iframe-headers:
      headers:
        customFrameOptionsValue: "ALLOWALL"
        contentSecurityPolicy: "frame-ancestors *"

    # Basic auth
    basic-auth:
      basicAuth:
        users:
          - "user:$apr1$hash"

    # IP whitelist
    internal-only:
      ipWhiteList:
        sourceRange:
          - "192.168.1.0/24"
          - "10.0.0.0/8"

    # Rate limiting
    rate-limit:
      rateLimit:
        average: 100
        burst: 50
```

## Common Health Check Paths

| Application | Health Path | Expected Response |
|-------------|-------------|-------------------|
| Generic | `/health` | 200 OK |
| Django | `/api/health` | 200 OK |
| Node.js | `/healthz` | 200 OK |
| Grafana | `/api/health` | 200 OK |
| PostgreSQL (via pgAdmin) | `/misc/ping` | 200 OK |
| Redis Commander | `/` | 200 OK |
| Generic web | `/` | 200/302 |

## Verification Commands

```bash
# Check router exists
curl -sk https://traefik.internal.lakehouse.wtf/api/http/routers | jq '.[] | select(.name | contains("service-name"))'

# Check service exists
curl -sk https://traefik.internal.lakehouse.wtf/api/http/services | jq '.[] | select(.name | contains("service-name"))'

# Check service health
curl -sk https://traefik.internal.lakehouse.wtf/api/http/services | jq '.[] | select(.name | contains("service-name")) | .serverStatus'

# Test route
curl -kI https://service-name.internal.lakehouse.wtf

# Watch Traefik logs for errors
ssh root@192.168.1.110 "tail -f /var/log/traefik/traefik.log | grep -E 'error|service-name'"
```

## Troubleshooting

**404 Not Found:** Router rule doesn't match - check Host() rule

**502 Bad Gateway:** Backend not responding - check service URL and port

**503 Service Unavailable:** Health check failing - verify health path

**SSL Error:** Certificate issue - check certResolver and domain
