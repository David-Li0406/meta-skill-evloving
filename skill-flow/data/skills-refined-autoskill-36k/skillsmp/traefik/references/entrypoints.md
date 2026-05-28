# Traefik EntryPoints

## Basic Configuration

```yaml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"
```

## Address Format

```
[host]:port[/protocol]
```

| Example | Description |
|---------|-------------|
| `:80` | Listen on all interfaces, port 80, TCP |
| `:443/tcp` | Explicit TCP |
| `:53/udp` | UDP traffic |
| `192.168.1.1:80` | Specific interface |
| `:8080-8085` | Port range |

## HTTP to HTTPS Redirect

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true
  websecure:
    address: ":443"
```

## Default TLS on EntryPoint

```yaml
entryPoints:
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt
        # Or specify options:
        # options: modern
```

## Forwarded Headers

For Traefik behind another proxy:

```yaml
entryPoints:
  web:
    address: ":80"
    forwardedHeaders:
      trustedIPs:
        - 10.0.0.0/8
        - 172.16.0.0/12
        - 192.168.0.0/16
      # Or trust all (not recommended for production):
      # insecure: true
```

## Proxy Protocol

For load balancers that use PROXY protocol:

```yaml
entryPoints:
  web:
    address: ":80"
    proxyProtocol:
      trustedIPs:
        - 10.0.0.0/8
      # Or trust all (not recommended):
      # insecure: true
```

## Transport Options

```yaml
entryPoints:
  web:
    address: ":80"
    transport:
      lifeCycle:
        requestAcceptGraceTimeout: 10s  # Wait before accepting
        graceTimeOut: 30s               # Shutdown grace period
      respondingTimeouts:
        readTimeout: 60s
        writeTimeout: 0s   # 0 = no timeout
        idleTimeout: 180s
```

## Default EntryPoints

```yaml
entryPoints:
  web:
    address: ":80"
    asDefault: true  # Use as default for routers without explicit entryPoints
  websecure:
    address: ":443"
    asDefault: true
```

## HTTP/3 (QUIC)

```yaml
entryPoints:
  websecure:
    address: ":443"
    http:
      tls: {}
    http3:
      advertisedPort: 443  # Port advertised in Alt-Svc header
```

Requires TLS. Automatically listens on UDP.

## EntryPoint Middlewares

Apply middlewares to all routers on an entrypoint:

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      middlewares:
        - security-headers@file
        - ratelimit@file
```

## Complete Example

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true

  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt
      middlewares:
        - security-headers@file
    forwardedHeaders:
      trustedIPs:
        - 10.0.0.0/8
    transport:
      respondingTimeouts:
        readTimeout: 60s
        idleTimeout: 180s

  traefik:
    address: ":8080"  # Dashboard

  metrics:
    address: ":8082"  # Prometheus metrics

  tcp:
    address: ":3306/tcp"

  udp:
    address: ":53/udp"
```

## Kubernetes Helm Values

```yaml
# values.yaml
ports:
  web:
    port: 8000
    exposedPort: 80
    expose: true
    protocol: TCP
  websecure:
    port: 8443
    exposedPort: 443
    expose: true
    protocol: TCP
    tls:
      enabled: true
      certResolver: letsencrypt
  traefik:
    port: 9000
    expose: false  # Internal only

additionalArguments:
  - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
  - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
```
