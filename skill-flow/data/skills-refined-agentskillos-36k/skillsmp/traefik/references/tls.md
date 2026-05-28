# Traefik TLS & Certificates

## ACME (Let's Encrypt)

### Basic Configuration

```yaml
certificateResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /data/acme.json
      caServer: https://acme-v02.api.letsencrypt.org/directory
      keyType: RSA4096  # EC256, EC384, RSA2048, RSA4096, RSA8192

      # Choose ONE challenge type
      httpChallenge:
        entryPoint: web
      # OR
      tlsChallenge: {}
      # OR
      dnsChallenge:
        provider: cloudflare
```

### Challenge Types

| Challenge | Port | Wildcard | Notes |
|-----------|------|----------|-------|
| HTTP-01 | 80 | No | Most common, requires port 80 |
| TLS-ALPN-01 | 443 | No | Uses TLS handshake |
| DNS-01 | None | Yes | Only option for wildcards |

### HTTP Challenge

```yaml
certificateResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /data/acme.json
      httpChallenge:
        entryPoint: web  # Must listen on :80
```

### DNS Challenge

```yaml
certificateResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /data/acme.json
      dnsChallenge:
        provider: cloudflare
        delayBeforeCheck: 10s
        resolvers:
          - 1.1.1.1:53
          - 8.8.8.8:53
```

**Environment variables for Cloudflare:**
```bash
CF_API_EMAIL=user@example.com
CF_API_KEY=your-api-key
# Or use API token:
CF_DNS_API_TOKEN=your-token
```

Common providers: `cloudflare`, `route53`, `gcloud`, `digitalocean`, `azure`, `namecheap`

### Wildcard Certificates

```yaml
# Router config
http:
  routers:
    wildcard:
      rule: HostRegexp(`[a-z]+\.example\.com`)
      tls:
        certResolver: letsencrypt
        domains:
          - main: example.com
            sans:
              - "*.example.com"
```

### Staging Server

```yaml
certificateResolvers:
  letsencrypt-staging:
    acme:
      email: admin@example.com
      storage: /data/acme-staging.json
      caServer: https://acme-staging-v02.api.letsencrypt.org/directory
      httpChallenge:
        entryPoint: web
```

## Manual Certificates

### File Provider

```yaml
tls:
  certificates:
    - certFile: /certs/example.com.crt
      keyFile: /certs/example.com.key
    - certFile: /certs/other.com.crt
      keyFile: /certs/other.com.key
```

### Kubernetes Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-tls
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: myapp
spec:
  routes:
    - match: Host(`myapp.example.com`)
      kind: Rule
      services:
        - name: myapp
          port: 80
  tls:
    secretName: myapp-tls
```

## Default Certificate

```yaml
tls:
  stores:
    default:
      defaultCertificate:
        certFile: /certs/default.crt
        keyFile: /certs/default.key
```

Or generate from ACME:

```yaml
tls:
  stores:
    default:
      defaultGeneratedCert:
        resolver: letsencrypt
        domain:
          main: example.com
```

## TLS Options

```yaml
tls:
  options:
    default:
      minVersion: VersionTLS12

    modern:
      minVersion: VersionTLS13

    intermediate:
      minVersion: VersionTLS12
      cipherSuites:
        - TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
        - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
        - TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
        - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
      curvePreferences:
        - CurveP521
        - CurveP384
```

### Kubernetes TLSOption CRD

```yaml
apiVersion: traefik.io/v1alpha1
kind: TLSOption
metadata:
  name: modern
spec:
  minVersion: VersionTLS13
  sniStrict: true
  alpnProtocols:
    - h2
    - http/1.1
```

Reference in IngressRoute:
```yaml
spec:
  tls:
    options:
      name: modern
      namespace: default
```

## Client Authentication (mTLS)

```yaml
tls:
  options:
    mtls:
      clientAuth:
        caFiles:
          - /certs/client-ca.crt
        clientAuthType: RequireAndVerifyClientCert
        # Options: NoClientCert, RequestClientCert,
        # RequireAnyClientCert, VerifyClientCertIfGiven,
        # RequireAndVerifyClientCert
```

## Router TLS Configuration

```yaml
http:
  routers:
    secure:
      rule: Host(`example.com`)
      tls:
        certResolver: letsencrypt
        options: modern
        domains:
          - main: example.com
            sans:
              - www.example.com
```

## IngressRoute TLS

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: secure-app
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`app.example.com`)
      kind: Rule
      services:
        - name: app
          port: 80
  tls:
    certResolver: letsencrypt
    # Or manual:
    # secretName: app-tls
    options:
      name: modern
    domains:
      - main: app.example.com
        sans:
          - api.example.com
```

## TCP TLS Passthrough

```yaml
tcp:
  routers:
    passthrough:
      rule: HostSNI(`db.example.com`)
      tls:
        passthrough: true
      service: database
```
