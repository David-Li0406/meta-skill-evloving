# Manyfold Configuration Reference

Complete environment variable reference for Manyfold deployment.

## Required Variables

### PUID and PGID
User and group IDs for running the application. Get values with `id` command.
```
PUID=1000
PGID=1000
```

### SECRET_KEY_BASE
Secret key for signing browser cookies. Generate with:
```bash
openssl rand -hex 64
```
Changing this invalidates all user sessions.

### REDIS_URL
Redis connection string (not needed for manyfold-solo).
```
REDIS_URL=redis://redis-server:6379/1
```

## Database Configuration

### DATABASE_URL (Recommended)
Single connection string containing all database info:
- **PostgreSQL**: `postgresql://user:pass@host:port/dbname?pool=5`
- **MySQL/MariaDB**: `mysql2://user:pass@host:port/dbname?pool=5`
- **SQLite**: `sqlite3:/config/manyfold.sqlite3?pool=5`

### Individual Database Variables
Alternative to DATABASE_URL:
| Variable | Description |
|----------|-------------|
| `DATABASE_ADAPTER` | postgresql, mysql2, or sqlite3 |
| `DATABASE_HOST` | Database server hostname |
| `DATABASE_PORT` | Port (optional, uses default) |
| `DATABASE_USER` | Database username |
| `DATABASE_PASSWORD` | Database password |
| `DATABASE_NAME` | Database name (or file path for SQLite) |
| `DATABASE_CONNECTION_POOL` | Connection pool size (default: 16) |

## Feature Toggles

### MULTIUSER
Enable multi-user features: login, signup, roles, permissions.
```
MULTIUSER=enabled
```
Recommended for public instances even for single users.

### FEDERATION
Enable ActivityPub/Fediverse features: remote following, webfinger discovery.
```
FEDERATION=enabled
```
Requires `PUBLIC_HOSTNAME`, `PUBLIC_PORT`, and domain root (no subpath).

### DEMO_MODE
Disable all destructive operations (deletion, upload, admin features).
```
DEMO_MODE=enabled
```

## Authentication (OIDC)

OpenID Connect single sign-on configuration:
```
OIDC_CLIENT_ID=<your-client-id>
OIDC_CLIENT_SECRET=<your-secret>
OIDC_ISSUER=https://auth.example.com/
OIDC_NAME=Provider Name
FORCE_OIDC=enabled  # Disable local accounts
```
Callback URL: `https://{PUBLIC_HOSTNAME}/users/auth/openid_connect/callback`

## Network

### HTTPS_ONLY
Force HTTPS mode with automatic redirect, HSTS headers, secure cookies.
```
HTTPS_ONLY=enabled
```
**Warning**: HSTS has long expiry. Ensure HTTPS works before enabling.

### RAILS_RELATIVE_URL_ROOT
For reverse proxy with non-root path (e.g., `/manyfold`).
```
RAILS_RELATIVE_URL_ROOT=/manyfold
```
**Incompatible with FEDERATION**.

### PUBLIC_HOSTNAME / PUBLIC_PORT
Public-facing hostname and port for email links and federation.
```
PUBLIC_HOSTNAME=manyfold.example.com
PUBLIC_PORT=443
```

## Email (SMTP)

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | SMTP server hostname | localhost |
| `SMTP_PORT` | SMTP port | 25 |
| `SMTP_USERNAME` | Auth username | - |
| `SMTP_PASSWORD` | Auth password | - |
| `SMTP_FROM_ADDRESS` | From address | notifications@{PUBLIC_HOSTNAME} |
| `SMTP_DOMAIN` | HELO domain | - |
| `SMTP_AUTHENTICATION` | plain, login, or cram_md5 | plain |
| `SMTP_OPENSSL_VERIFY_MODE` | none or peer | peer |
| `SMTP_OPEN_TIMEOUT` | Connection timeout seconds | 5 |
| `SMTP_READ_TIMEOUT` | Read timeout seconds | 5 |

## Performance

| Variable | Default | Description |
|----------|---------|-------------|
| `WEB_CONCURRENCY` | 4 | Number of web workers (match CPU cores) |
| `RAILS_MAX_THREADS` | 16 | Threads per worker |
| `DEFAULT_WORKER_CONCURRENCY` | 4 | Standard background job threads |
| `PERFORMANCE_WORKER_CONCURRENCY` | 1 | Heavy job threads (analysis, conversion) |

Max concurrent requests = `WEB_CONCURRENCY` × `RAILS_MAX_THREADS`

## Security

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_FILE_UPLOAD_SIZE` | 268435456 (256MB) | Max upload size in bytes |
| `MAX_FILE_EXTRACT_SIZE` | 1073741824 (1GB) | Max extracted file size in bytes |
| `MIN_PASSWORD_SCORE` | 4 | Password strength (0=weak, 4=strong) |
| `SUDO_RUN_UNSAFELY` | - | Suppress root warning (use with caution) |

## Miscellaneous

| Variable | Description |
|----------|-------------|
| `MANYFOLD_LOG_LEVEL` | Log verbosity: debug, info, warn, error, fatal |
| `USAGE_REPORTING_URL` | Custom analytics endpoint |
| `EXPERIMENTAL_LANGUAGES` | Show incomplete translations |

## Docker Security Options

Recommended docker-compose security settings:
```yaml
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
cap_add:
  - CHOWN
  - DAC_OVERRIDE
  - SETUID
  - SETGID
```

### Read-only Filesystem
For maximum security, mount these as writable:
```yaml
read_only: true
tmpfs:
  - /run:exec
volumes:
  - /var/manyfold/sys_tmp:/tmp
  - /var/manyfold/app_tmp:/usr/src/app/tmp
  - /var/manyfold/log:/usr/src/app/log
```
Set sticky bit: `chmod 1777 /var/manyfold/sys_tmp/`
