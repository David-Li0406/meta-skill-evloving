# Traefik Kubernetes CRDs

## Available CRDs

| CRD | API Version | Purpose |
|-----|-------------|---------|
| IngressRoute | traefik.io/v1alpha1 | HTTP routing |
| IngressRouteTCP | traefik.io/v1alpha1 | TCP routing |
| IngressRouteUDP | traefik.io/v1alpha1 | UDP routing |
| Middleware | traefik.io/v1alpha1 | HTTP middleware |
| MiddlewareTCP | traefik.io/v1alpha1 | TCP middleware |
| TraefikService | traefik.io/v1alpha1 | Advanced load balancing |
| TLSOption | traefik.io/v1alpha1 | TLS parameters |
| TLSStore | traefik.io/v1alpha1 | Default certificates |
| ServersTransport | traefik.io/v1alpha1 | Backend transport settings |
| ServersTransportTCP | traefik.io/v1alpha1 | TCP backend transport |

## IngressRoute

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: myapp
  namespace: default
spec:
  entryPoints:
    - web
    - websecure
  routes:
    - match: Host(`myapp.example.com`)
      kind: Rule
      priority: 10
      services:
        - name: myapp-svc
          port: 80
          weight: 1
          passHostHeader: true
          sticky:
            cookie:
              name: myapp-sticky
      middlewares:
        - name: auth-middleware
          namespace: default  # Optional if same namespace
  tls:
    certResolver: letsencrypt
    domains:
      - main: myapp.example.com
        sans:
          - www.myapp.example.com
    options:
      name: modern-tls
      namespace: default
    secretName: myapp-tls  # Or use existing secret
```

## Middleware CRD

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: auth-middleware
  namespace: default
spec:
  basicAuth:
    secret: auth-secret
    removeHeader: true
---
apiVersion: v1
kind: Secret
metadata:
  name: auth-secret
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: password123
```

### Common Middleware Examples

```yaml
# Rate limiting
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: ratelimit
spec:
  rateLimit:
    average: 100
    burst: 50
    period: 1m
---
# Strip path prefix
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: strip-api
spec:
  stripPrefix:
    prefixes:
      - /api
---
# Add headers
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: security-headers
spec:
  headers:
    frameDeny: true
    browserXssFilter: true
    contentTypeNosniff: true
    stsSeconds: 31536000
    stsIncludeSubdomains: true
---
# Redirect to HTTPS
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: redirect-https
spec:
  redirectScheme:
    scheme: https
    permanent: true
---
# Forward auth
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: forward-auth
spec:
  forwardAuth:
    address: http://auth-service.default.svc.cluster.local/verify
    authResponseHeaders:
      - X-User-Id
      - X-User-Email
```

## TraefikService (Advanced Load Balancing)

### Weighted Round Robin

```yaml
apiVersion: traefik.io/v1alpha1
kind: TraefikService
metadata:
  name: weighted-service
spec:
  weighted:
    services:
      - name: app-v1
        port: 80
        weight: 80
      - name: app-v2
        port: 80
        weight: 20
```

### Mirroring

```yaml
apiVersion: traefik.io/v1alpha1
kind: TraefikService
metadata:
  name: mirror-service
spec:
  mirroring:
    name: main-service
    port: 80
    mirrors:
      - name: test-service
        port: 80
        percent: 10
```

### Failover

```yaml
apiVersion: traefik.io/v1alpha1
kind: TraefikService
metadata:
  name: failover-service
spec:
  failover:
    service:
      name: primary-service
      port: 80
    fallback:
      name: backup-service
      port: 80
```

## TLSOption

```yaml
apiVersion: traefik.io/v1alpha1
kind: TLSOption
metadata:
  name: modern-tls
spec:
  minVersion: VersionTLS12
  cipherSuites:
    - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
  curvePreferences:
    - CurveP521
    - CurveP384
  sniStrict: true
```

## Provider Configuration

```yaml
# In Traefik static config
providers:
  kubernetesCRD:
    namespaces:
      - default
      - production
    allowCrossNamespace: true
    allowEmptyServices: false
    labelselector: "app=traefik-managed"
```

| Option | Description | Default |
|--------|-------------|---------|
| `namespaces` | Watch specific namespaces (empty = all) | [] |
| `allowCrossNamespace` | Allow cross-namespace references | false |
| `allowEmptyServices` | Route to services with no endpoints | false |
| `labelselector` | Filter resources by label | "" |
| `ingressClass` | Filter by annotation value | "" |
