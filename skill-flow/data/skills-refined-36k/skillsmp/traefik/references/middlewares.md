# Traefik Middlewares

## Available HTTP Middlewares

| Middleware | Purpose |
|------------|---------|
| AddPrefix | Adds path prefix to request |
| BasicAuth | HTTP Basic Authentication |
| Buffering | Buffers request/response |
| Chain | Combines multiple middlewares |
| CircuitBreaker | Prevents calling unhealthy services |
| Compress | Compresses responses (gzip, brotli) |
| ContentType | Handles Content-Type auto-detection |
| DigestAuth | HTTP Digest Authentication |
| Errors | Custom error pages |
| ForwardAuth | Delegates auth to external service |
| GrpcWeb | Converts gRPC-Web to HTTP/2 gRPC |
| Headers | Adds/modifies headers |
| IPAllowList | Restricts by client IP |
| InFlightReq | Limits concurrent connections |
| PassTLSClientCert | Passes client cert in header |
| RateLimit | Limits request rate |
| RedirectScheme | Redirects HTTP to HTTPS |
| RedirectRegex | Redirects based on regex |
| ReplacePath | Replaces request path |
| ReplacePathRegex | Replaces path with regex |
| Retry | Retries failed requests |
| StripPrefix | Removes path prefix |
| StripPrefixRegex | Removes prefix with regex |

## BasicAuth

```yaml
http:
  middlewares:
    auth:
      basicAuth:
        users:
          - "admin:$apr1$xyz..."  # htpasswd format
        usersFile: /path/to/users  # Or external file
        realm: "My Realm"
        removeHeader: true  # Remove auth header from backend
```

Generate password: `htpasswd -nb admin password`

**Kubernetes Secret:**
```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: auth
spec:
  basicAuth:
    secret: auth-secret
```

## ForwardAuth

```yaml
http:
  middlewares:
    forward-auth:
      forwardAuth:
        address: https://auth.example.com/verify
        trustForwardHeader: true
        authResponseHeaders:
          - X-User-Id
          - X-User-Email
        authRequestHeaders:
          - Authorization
```

Headers sent to auth service: `X-Forwarded-Method`, `X-Forwarded-Proto`, `X-Forwarded-Host`, `X-Forwarded-Uri`, `X-Forwarded-For`

## RateLimit

```yaml
http:
  middlewares:
    ratelimit:
      rateLimit:
        average: 100      # Requests per period
        burst: 50         # Max concurrent
        period: 1m        # Time period
        sourceCriterion:
          requestHost: true  # Group by host
          # Or by header:
          # requestHeaderName: X-API-Key
          # Or by IP:
          # ipStrategy:
          #   depth: 1
```

## Headers

```yaml
http:
  middlewares:
    security:
      headers:
        # Security headers
        frameDeny: true
        browserXssFilter: true
        contentTypeNosniff: true
        stsSeconds: 31536000
        stsIncludeSubdomains: true
        stsPreload: true

        # Custom headers
        customRequestHeaders:
          X-Custom: "value"
        customResponseHeaders:
          X-Response: "value"

        # CORS
        accessControlAllowOriginList:
          - "https://example.com"
        accessControlAllowMethods:
          - GET
          - POST
        accessControlAllowHeaders:
          - Authorization
        accessControlMaxAge: 100
```

## StripPrefix

```yaml
http:
  middlewares:
    strip:
      stripPrefix:
        prefixes:
          - /api
          - /v1
```

Request `/api/users` → Backend sees `/users`
Sets `X-Forwarded-Prefix: /api` header.

## RedirectScheme

```yaml
http:
  middlewares:
    https-redirect:
      redirectScheme:
        scheme: https
        permanent: true  # 301 vs 302
        port: "443"
```

## RedirectRegex

```yaml
http:
  middlewares:
    redirect:
      redirectRegex:
        regex: "^https://example.com/(.*)"
        replacement: "https://www.example.com/${1}"
        permanent: true
```

## Chain (Combine Middlewares)

```yaml
http:
  middlewares:
    secured:
      chain:
        middlewares:
          - https-redirect
          - security-headers
          - ratelimit
          - auth
```

## IPAllowList

```yaml
http:
  middlewares:
    internal:
      ipAllowList:
        sourceRange:
          - 10.0.0.0/8
          - 192.168.0.0/16
        ipStrategy:
          depth: 1  # Use X-Forwarded-For depth
```

## CircuitBreaker

```yaml
http:
  middlewares:
    circuit:
      circuitBreaker:
        expression: NetworkErrorRatio() > 0.30 || ResponseCodeRatio(500, 600, 0, 600) > 0.25
        checkPeriod: 10s
        fallbackDuration: 30s
        recoveryDuration: 60s
```

## Retry

```yaml
http:
  middlewares:
    retry:
      retry:
        attempts: 3
        initialInterval: 100ms
```

## Compress

```yaml
http:
  middlewares:
    compress:
      compress:
        excludedContentTypes:
          - text/event-stream
        minResponseBodyBytes: 1024
```

## InFlightReq

```yaml
http:
  middlewares:
    inflight:
      inFlightReq:
        amount: 100
        sourceCriterion:
          requestHost: true
```

## Errors (Custom Error Pages)

```yaml
http:
  middlewares:
    errors:
      errors:
        status:
          - 500-599
        service: error-service
        query: /{status}.html
```
