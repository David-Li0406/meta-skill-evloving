# Tunnel Command Reference

Complete reference for all Buddy tunnel commands and options.

## Table of Contents
- [Quick Start Commands](#quick-start-commands)
- [HTTP Tunnel Command](#http-tunnel-command)
- [TCP Tunnel Command](#tcp-tunnel-command)
- [TLS Tunnel Command](#tls-tunnel-command)
- [Configuration Management](#configuration-management)
- [Starting Saved Tunnels](#starting-saved-tunnels)

## Quick Start Commands

### HTTP Tunnel

```bash
bdy tunnel http [protocol://host:port]
```

Start tunnel for HTTP/HTTPS traffic with a specific hostname.

**Arguments:**
- `protocol://host:port` - Target address (default: `http://localhost:80`)
  - Protocol: `http://` or `https://` (optional)
  - Host: Target hostname (default: `localhost`)
  - Port: Target port (default: `80`)

**Examples:**
```bash
bdy tunnel http localhost:3000
bdy tunnel http http://127.0.0.1:8080
bdy tunnel http :5000  # Shorthand for localhost:5000
```

### TCP Tunnel

```bash
bdy tunnel tcp [host:port]
```

Forward all TCP traffic on a public port to a local address.

**Arguments:**
- `host:port` - Target address (default: `localhost:80`)
  - Host: Target hostname (default: `localhost`)
  - Port: Target port (default: `80`)

**Examples:**
```bash
bdy tunnel tcp localhost:5432
bdy tunnel tcp :3306  # Shorthand for localhost:3306
```

### TLS Tunnel

```bash
bdy tunnel tls [host:port]
```

Listen for TLS traffic on port 443 with a specific hostname.

**Arguments:**
- `host:port` - Target address (default: `localhost:80`)
  - Host: Target hostname (default: `localhost`)
  - Port: Target port (default: `80`)

**Examples:**
```bash
bdy tunnel tls localhost:8443
bdy tunnel tls :443
```

## HTTP Tunnel Command

### Full Syntax

```bash
bdy tunnel http [options] [protocol://host:port]
```

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `-n, --name <name>` | Tunnel name for identification | `-n my-api` |
| `-r, --region <region>` | Region selection (eu, us, as) | `-r us` |
| `-w, --whitelist <cidrs...>` | IP CIDR whitelist. Use "*" for all | `-w 203.0.113.0/24` |
| `-t, --timeout <seconds>` | Connection timeout in seconds | `-t 300` |
| `-a, --auth <user:pass>` | HTTP basic authorization | `-a admin:secret` |
| `-b, --buddy` | Enforce Buddy authorization | `-b` |
| `-l, --log` | Log HTTP requests | `-l` |

### HTTP-Specific Options

| Option | Description | Example |
|--------|-------------|---------|
| `-h, --host <host>` | Custom HTTP host header | `-h example.com` |
| `--header <headers...>` | Add request headers (key:value) | `--header X-Custom:value` |
| `--response-header <headers...>` | Add response headers (key:value) | `--response-header X-Frame-Options:DENY` |
| `--useragent <useragent...>` | Whitelist user-agents (text or regex) | `--useragent /Mozilla/` |
| `-v, --verify` | Enforce TLS verify | `-v` |
| `-2, --http2` | Enforce HTTP/2 | `-2` |
| `-c, --compression` | Enable HTTP response compression | `-c` |
| `--ca <ca>` | Path to TLS PEM CA certificate | `--ca /path/to/ca.pem` |
| `--circuit-breaker <threshold>` | Circuit breaker threshold (0-1) | `--circuit-breaker 0.5` |
| `-s, --serve <directory>` | Serve files from directory | `-s ./public` |
| `--token <token>` | Token to authorize agent | `--token abc123` |

### HTTP Examples

**Basic HTTP tunnel:**
```bash
bdy tunnel http localhost:3000
```

**With basic authentication:**
```bash
bdy tunnel http localhost:3000 -a admin:password
```

**With IP whitelist:**
```bash
bdy tunnel http localhost:3000 -w 203.0.113.0/24 198.51.100.0/24
```

**With custom headers:**
```bash
bdy tunnel http localhost:3000 \
  --header X-API-Key:secret \
  --response-header X-Frame-Options:DENY
```

**With request logging:**
```bash
bdy tunnel http localhost:3000 -l -n api-debug
```

**Serve static files:**
```bash
bdy tunnel http -s ./dist -n static-site
```

**With compression and HTTP/2:**
```bash
bdy tunnel http localhost:3000 -c -2
```

**User-agent restriction:**
```bash
bdy tunnel http localhost:3000 \
  --useragent /Chrome/ /Firefox/ /Safari/
```

**Circuit breaker for fault tolerance:**
```bash
bdy tunnel http localhost:3000 --circuit-breaker 0.5
```

## TCP Tunnel Command

### Full Syntax

```bash
bdy tunnel tcp [options] [host:port]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `-n, --name <name>` | Tunnel name for identification | `-n postgres-tunnel` |
| `-r, --region <region>` | Region selection (eu, us, as) | `-r eu` |
| `-w, --whitelist <cidrs...>` | IP CIDR whitelist. Use "*" for all | `-w 203.0.113.0/32` |
| `-t, --timeout <seconds>` | Connection timeout in seconds | `-t 600` |
| `--token <token>` | Token to authorize agent | `--token abc123` |

### TCP Examples

**Expose PostgreSQL:**
```bash
bdy tunnel tcp localhost:5432 -n postgres-db
```

**Expose MySQL with IP restriction:**
```bash
bdy tunnel tcp localhost:3306 -n mysql-db -w 203.0.113.0/24
```

**Expose SSH server:**
```bash
bdy tunnel tcp localhost:22 -n ssh-tunnel
```

**Game server with timeout:**
```bash
bdy tunnel tcp localhost:25565 -n minecraft -t 3600
```

**Redis with whitelist:**
```bash
bdy tunnel tcp localhost:6379 -n redis -w 198.51.100.0/24
```

## TLS Tunnel Command

### Full Syntax

```bash
bdy tunnel tls [options] [host:port]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `-n, --name <name>` | Tunnel name for identification | `-n secure-api` |
| `-r, --region <region>` | Region selection (eu, us, as) | `-r us` |
| `-w, --whitelist <cidrs...>` | IP CIDR whitelist. Use "*" for all | `-w 203.0.113.0/24` |
| `-t, --timeout <seconds>` | Connection timeout in seconds | `-t 300` |
| `-k, --key <key>` | Path to TLS key | `-k /path/to/key.pem` |
| `-c, --cert <cert>` | Path to TLS PEM certificate | `-c /path/to/cert.pem` |
| `--ca <ca>` | Path to TLS PEM CA certificate | `--ca /path/to/ca.pem` |
| `-i, --terminate <at>` | TLS termination location | `-i target` |
| `--token <token>` | Token to authorize agent | `--token abc123` |

### TLS Termination Options

The `-i, --terminate` flag controls where TLS is terminated:

| Value | Description | Use Case |
|-------|-------------|----------|
| `region` | Terminate at Buddy region (default) | Standard HTTPS |
| `agent` | Terminate at local agent | Custom certs |
| `target` | No termination, pass through | End-to-end encryption |

### TLS Examples

**Basic TLS tunnel:**
```bash
bdy tunnel tls localhost:8443
```

**With custom certificate:**
```bash
bdy tunnel tls localhost:8443 \
  -k /path/to/key.pem \
  -c /path/to/cert.pem
```

**With CA for client authentication:**
```bash
bdy tunnel tls localhost:8443 \
  -k /path/to/key.pem \
  -c /path/to/cert.pem \
  --ca /path/to/ca.pem
```

**Terminate at agent:**
```bash
bdy tunnel tls localhost:8443 -i agent \
  -k /path/to/key.pem \
  -c /path/to/cert.pem
```

**Pass-through (no termination):**
```bash
bdy tunnel tls localhost:8443 -i target
```

## Configuration Management

Save and manage tunnel configurations for easy reuse.

### Config Set Command

Set global configuration values.

```bash
bdy tunnel config set <command> [value]
```

**Subcommands:**

**Set token:**
```bash
bdy tunnel config set token YOUR_TUNNEL_TOKEN
```

**Set region:**
```bash
bdy tunnel config set region eu  # or us, as
```

**Set IP whitelist:**
```bash
bdy tunnel config set whitelist 203.0.113.0/24 198.51.100.0/24
```

**Set timeout:**
```bash
bdy tunnel config set timeout 300  # seconds
```

### Config Add Command

Add named tunnel configurations.

```bash
bdy tunnel config add <type> <name> [options] [address]
```

**Add HTTP tunnel:**
```bash
bdy tunnel config add http dev-api http://localhost:3000
bdy tunnel config add http staging https://localhost:8080 -a user:pass
```

**Add TCP tunnel:**
```bash
bdy tunnel config add tcp postgres localhost:5432
bdy tunnel config add tcp mysql localhost:3306 -w 203.0.113.0/24
```

**Add TLS tunnel:**
```bash
bdy tunnel config add tls secure-api localhost:8443 \
  -k /path/to/key.pem \
  -c /path/to/cert.pem
```

### Config Get Command

View configuration values.

```bash
bdy tunnel config get <command> [name]
```

**Get region:**
```bash
bdy tunnel config get region
```

**Get token:**
```bash
bdy tunnel config get token
```

**Get whitelist:**
```bash
bdy tunnel config get whitelist
```

**Get timeout:**
```bash
bdy tunnel config get timeout
```

**List all tunnels:**
```bash
bdy tunnel config get tunnels
```

**Get specific tunnel:**
```bash
bdy tunnel config get tunnel dev-api
```

### Config Remove Command

Remove tunnel configurations.

```bash
bdy tunnel config rm tunnel <name>
```

**Examples:**
```bash
bdy tunnel config rm tunnel dev-api
bdy tunnel config rm tunnel postgres
```

## Starting Saved Tunnels

Start tunnels using saved configurations.

```bash
bdy tunnel start <name>
```

**Examples:**
```bash
# Start HTTP tunnel from config
bdy tunnel start dev-api

# Start TCP tunnel from config
bdy tunnel start postgres

# Start TLS tunnel from config
bdy tunnel start secure-api
```

The tunnel starts with all options from the saved configuration.

## Global Options

These options apply to all tunnel commands:

| Option | Description |
|--------|-------------|
| `-h, --help` | Display help for command |
| `--verbose` | Verbose output for debugging |
| `--quiet` | Minimal output |

**Examples:**
```bash
# Show help for HTTP tunnels
bdy tunnel http --help

# Verbose output
bdy tunnel http localhost:3000 --verbose

# Quiet mode
bdy tunnel http localhost:3000 --quiet
```

## Environment Variables

Configure tunnels using environment variables:

```bash
# Tunnel token
export BUDDY_TUNNEL_TOKEN="your-tunnel-token"

# Region
export BUDDY_REGION="eu"  # or us, as

# Use in commands
bdy tunnel http localhost:3000
```

## Configuration File Location

Tunnel configurations are stored in:

```
~/.buddy/tunnel-config.json
```

Manual editing is possible but not recommended. Use `bdy tunnel config` commands instead.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Authentication error |
| 3 | Configuration error |
| 4 | Connection error |

## Tips and Best Practices

### Naming Conventions

Use descriptive names for saved tunnels:
```bash
bdy tunnel config add http dev-api-v2 http://localhost:3000
bdy tunnel config add tcp prod-postgres localhost:5432
```

### Security Defaults

Always use whitelisting for production:
```bash
bdy tunnel http localhost:3000 -w your-office-ip/24
```

### Timeout Configuration

Set appropriate timeouts for service type:
```bash
# Short timeout for APIs
bdy tunnel http localhost:3000 -t 60

# Long timeout for websockets
bdy tunnel http localhost:8080 -t 3600
```

### Regional Performance

Choose region closest to users:
```bash
# Users in Europe
bdy tunnel http localhost:3000 -r eu

# Users in US
bdy tunnel http localhost:3000 -r us

# Users in Asia
bdy tunnel http localhost:3000 -r as
```

### Logging for Debugging

Enable logging when troubleshooting:
```bash
bdy tunnel http localhost:3000 -l -n debug-api
```

### Configuration Reuse

Save frequently used configurations:
```bash
# Save configuration
bdy tunnel config add http main-api http://localhost:3000 \
  -a admin:secret \
  -w 203.0.113.0/24 \
  -t 300

# Reuse easily
bdy tunnel start main-api
```
