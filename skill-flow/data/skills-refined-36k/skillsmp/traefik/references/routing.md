# Traefik HTTP Routing

## Rule Matchers

| Matcher | Description | Example |
|---------|-------------|---------|
| `Host()` | Match request host | `Host(\`example.com\`)` |
| `HostRegexp()` | Match host with regex | `HostRegexp(\`[a-z]+\.example\.com\`)` |
| `Path()` | Exact path match | `Path(\`/api/users\`)` |
| `PathPrefix()` | Path prefix match | `PathPrefix(\`/api\`)` |
| `PathRegexp()` | Path with regex | `PathRegexp(\`/api/v[0-9]+\`)` |
| `Header()` | Match header value | `Header(\`X-Custom\`, \`value\`)` |
| `HeaderRegexp()` | Header with regex | `HeaderRegexp(\`Content-Type\`, \`application/.*\`)` |
| `Method()` | Match HTTP method | `Method(\`GET\`, \`POST\`)` |
| `Query()` | Match query param | `Query(\`debug\`, \`true\`)` |
| `QueryRegexp()` | Query with regex | `QueryRegexp(\`id\`, \`[0-9]+\`)` |
| `ClientIP()` | Match client IP/CIDR | `ClientIP(\`192.168.1.0/24\`)` |

## Rule Syntax

```yaml
# Use backticks for values (single quotes not allowed)
match: Host(`example.com`)

# Combine with logical operators
match: Host(`example.com`) && PathPrefix(`/api`)
match: Host(`example.com`) || Host(`example.org`)
match: !Host(`admin.example.com`)

# Complex rules
match: Host(`example.com`) && (PathPrefix(`/api`) || PathPrefix(`/v2`))
```

## Priority

Default: Longer rules = higher priority. Override with explicit priority:

```yaml
# IngressRoute
spec:
  routes:
    - match: Host(`example.com`)
      kind: Rule
      priority: 10  # Higher number = higher priority
```

```yaml
# File provider
http:
  routers:
    catch-all:
      rule: PathPrefix(`/`)
      priority: 1  # Low priority catch-all
    specific:
      rule: Host(`example.com`) && PathPrefix(`/api`)
      priority: 100  # High priority specific route
```

## Router Configuration

### HTTP Router (File Provider)

```yaml
http:
  routers:
    my-router:
      entryPoints:
        - web
        - websecure
      rule: Host(`example.com`) && PathPrefix(`/api`)
      service: my-service
      middlewares:
        - auth
        - ratelimit
      tls:
        certResolver: letsencrypt
        options: modern
        domains:
          - main: example.com
            sans:
              - www.example.com
```

### Router Options

| Option | Description |
|--------|-------------|
| `entryPoints` | List of listening entrypoints |
| `rule` | Matching rule expression |
| `service` | Target service name |
| `middlewares` | Ordered list of middlewares |
| `tls` | TLS configuration |
| `priority` | Route priority (default: rule length) |

## Rule Examples

```yaml
# Single domain
Host(`example.com`)

# Multiple domains
Host(`example.com`) || Host(`www.example.com`)

# Domain with path
Host(`api.example.com`) && PathPrefix(`/v1`)

# Specific path and method
Host(`example.com`) && Path(`/users`) && Method(`POST`)

# Header-based routing
Host(`example.com`) && Header(`X-API-Version`, `2`)

# Wildcard subdomain (regex)
HostRegexp(`[a-z]+\.example\.com`)

# Path with variable segment (regex)
PathRegexp(`/users/[0-9]+/profile`)

# Internal traffic only
ClientIP(`10.0.0.0/8`, `192.168.0.0/16`)
```

## TCP/UDP Routing

### TCP Router

```yaml
tcp:
  routers:
    my-tcp-router:
      entryPoints:
        - tcp
      rule: HostSNI(`example.com`)  # Requires TLS
      service: my-tcp-service
      tls:
        passthrough: true  # TLS passthrough to backend
```

### TCP Matchers

| Matcher | Description |
|---------|-------------|
| `HostSNI()` | Match TLS SNI (requires TLS) |
| `HostSNIRegexp()` | SNI with regex |
| `ClientIP()` | Match client IP |
| `ALPN()` | Match TLS ALPN protocol |

### UDP Router

```yaml
udp:
  routers:
    my-udp-router:
      entryPoints:
        - udp
      service: my-udp-service
```

UDP routers have no rules - they forward all traffic on the entrypoint.
