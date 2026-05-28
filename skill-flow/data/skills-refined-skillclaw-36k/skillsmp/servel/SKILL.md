---
name: servel
description: Self-hosted deployment platform via Docker Swarm. Use when deploying applications, managing infrastructure (databases, queues, caches), viewing logs, managing secrets, or performing server operations. Triggers on deployment, infrastructure, databases, redis, postgres, backup, restore, logs, secrets, SSL, domains, or server management tasks.
---

# Servel

Servel is a self-hosted deployment platform that brings Vercel-like simplicity to your own VPS. Deploy any application with a single command—Servel auto-detects your project type, builds it, provisions SSL certificates, and deploys to Docker Swarm with zero-downtime rolling updates.

## Architecture

- **Client-Server Model**: CLI runs locally, communicates via SSH to server daemon
- **Orchestration**: Docker Swarm with Traefik for routing and auto-HTTPS
- **State**: Filesystem-based (`/var/servel/`), no database dependency
- **Secrets**: Age encryption, injected at runtime

## Core Capabilities

- **Zero-Config Deployments**: Auto-detects from lockfiles (bun.lockb, package-lock.json, requirements.txt, go.mod)
- **Automatic HTTPS**: Traefik provisions Let's Encrypt certificates
- **44+ Infrastructure Types**: Databases, caches, queues, platforms with one command
- **Infrastructure Linking**: Connection strings auto-injected as environment variables
- **Preview Deployments**: Isolated environments with configurable TTL
- **Rolling Updates**: Zero-downtime with health checks and auto-rollback
- **Image Caching**: Hashes dependencies, skips unchanged builds

## Deployment

```bash
servel deploy                              # Deploy current project
servel deploy --preview                    # Preview with unique URL
servel deploy --preview --ttl 24h          # Preview with 24h auto-cleanup
servel deploy --dry-run                    # Show plan without deploying
servel deploy --link-infra mydb,redis      # Inject infra connection vars
servel deploy -n myapp -d app.example.com  # Custom name and domain
servel deploy --verbose                    # Show full build output
servel deploy --no-registry                # Skip registry (faster single-node)
servel deploy --memory 1g --cpu 0.5        # Set resource limits
servel ps                                  # List deployments
servel logs <name> -f                      # Follow logs
servel rm <name>                           # Remove deployment
servel rollback <name>                     # Rollback to previous version
servel scale <name> 3                      # Scale replicas
servel inspect <name>                      # View details
servel exec <name> sh                      # Shell into container
servel watch <name>                        # Watch deployment progress
```

**Detection priority:** `servel.yaml` → `docker-compose.yml` → `Dockerfile` → preset → Nixpacks

**Key flags:**
- `--name, -n` — Deployment name
- `--domain, -d` — Domain for routing
- `--preview` — Preview environment
- `--ttl` — Preview lifetime (1h, 6h, 1d, 7d, 2w)
- `--link-infra` — Link infrastructure (comma-separated)
- `--no-registry` — Skip registry push
- `--memory` — Memory limit (512m, 1g, none)
- `--cpu` — CPU limit (0.5, 1.0)
- `--build-on <node>` — Build on specific node
- `--local-build` — Build locally, push to registry
- `--abort` — Ctrl+C kills deployment (default: detaches)

**Cancellation behavior:** By default, Ctrl+C detaches (deployment continues on server). Use `--abort` to kill. Resume with `servel logs <name>`.

## Context Detection

Servel auto-detects project context from `.servel/state.json` in project directory:
- Created by `servel deploy` and `servel rollback`
- Contains: project name, server, environment, deployment ID
- Environment-specific: `.servel/state.{env}.json`

**Best practice:** In CI/CD, always specify app name explicitly (auto-detection is local-only).

## Infrastructure

44+ types across 9 categories with health monitoring, backups, and auto-generated credentials.

| Category | Types |
|----------|-------|
| **Database** | postgres, mysql, mongodb, clickhouse, libsql + HA variants |
| **Cache/Queue** | redis, rabbitmq, kafka, nats |
| **Search** | meilisearch, typesense, elasticsearch |
| **Storage** | minio, seaweedfs |
| **Monitoring** | prometheus, grafana, loki, uptimekuma, gatus, plausible |
| **Platform** | supabase, chatwoot, typebot, affine, convex, n8n |
| **Realtime** | livekit, hocuspocus, y-sweet |
| **Email** | posteio |
| **CI** | woodpecker |

```bash
servel add postgres --name mydb            # Create PostgreSQL
servel add redis,postgres --prefix app     # Bundle: app-redis, app-postgres
servel add supabase --name supa            # Full Supabase stack
servel add postgres --name db --ha         # High-availability (3+ nodes)
servel link myapp --infra mydb             # Link → injects DATABASE_URL
servel infra status                        # Health check all
servel infra vars mydb                     # View connection variables
servel infra backup mydb                   # Create backup
servel infra restore mydb backup.sql.gz    # Restore from backup
servel infra logs mydb -f                  # Follow logs
servel infra rotate mydb                   # Rotate credentials
servel deps myapp                          # Show linked infrastructure
```

**Linking injects:** DATABASE_URL, REDIS_URL, MONGODB_URI, etc. based on infrastructure type.

**Node pinning:**
- `--node hostname` — By hostname
- `--alias db-node` — By alias (stable reference)
- `--label storage=ssd` — By node label

**HA requirements:** 3+ nodes minimum. Uses Patroni (Postgres), Sentinel (Redis), Group Replication (MySQL).

## Server Management

```bash
servel ssh <server>                   # SSH into server
servel server status                  # Cluster health (CPU, memory, disk)
servel server provision               # Provision new server
servel server add <name> user@host    # Add server to config
servel server use <name>              # Set default server
servel df                             # Disk usage
servel df --volumes                   # Volume usage by category
servel df --nodes                     # Per-node usage
servel node ls                        # List swarm nodes
servel node add <name> user@host      # Add node to cluster
servel doctor                         # Diagnose issues
servel verify                         # Verify configuration
servel cleanup                        # Remove expired environments
servel cleanup --force                # No confirmation
servel prune                          # Remove dangling images/containers
servel prune --all                    # Remove unused images/networks/cache
servel prune --all --volumes          # ⚠️ DATA LOSS: removes unused volumes
```

**Health thresholds:** Critical >90%, Warning >75% (color-coded).

**Maintenance schedule:** Run `servel cleanup --force` + `servel prune --all --force` weekly in CI.

## Secrets

Encrypted with Age, stored at `/var/servel/deployments/<app>/.env.age`.

```bash
servel secrets set API_KEY              # Set (prompted input)
servel secrets set API_KEY "value"      # Set with value
servel secrets list                     # List keys
servel secrets get API_KEY              # Get value
servel secrets rm API_KEY               # Remove
servel secrets rotate API_KEY           # Rotate
servel deploy --migrate-secrets         # Auto-detect *_KEY, *_SECRET, *_PASSWORD
```

**In servel.yaml:** Use key-only format:
```yaml
secrets:
  - API_KEY
  - DB_PASSWORD
```

## Domains

Auto-SSL via Let's Encrypt through Traefik.

```bash
servel domains add myapp app.example.com   # Add domain
servel domains ls                          # List domains
servel domains rm myapp app.example.com    # Remove domain
servel domains redirect old.com new.com    # Create redirect
```

## Development Mode

```bash
servel dev                       # File sync with hot reload
servel dev --team                # Bidirectional sync
servel dev --port 3001           # Custom port
servel dev list                  # View active sessions
servel dev logs <session> -f     # Follow session logs
servel dev stop <session>        # Stop session
servel tunnel                    # Expose local service publicly
servel port-forward mydb 5432    # Forward remote port locally
```

**Port auto-detection:** Next.js=3000, Vite=5173, Go=8080, Django=8000.

**Domain handling:**
- Subdomain only: `my-app` → `dev-my-app.example.com`
- Full domain: `staging.custom.com` → used as-is

**File sync:** 300ms debounce, rsync for batches >5 files. Default ignores: `.git/`, `node_modules/`, `.env*`, `dist/`, `build/`.

## Configuration

Optional `servel.yaml`. Full schema: https://servel.dev/docs/configuration

```yaml
name: myapp
domain: app.example.com

build:
  preset: bun                    # bun, node, python, go, rust
  dockerfile: Dockerfile
  buildCommand: bun run build
  startCommand: bun run start
  context: .
  args:
    NODE_ENV: production

env:
  NODE_ENV: production
  LOG_LEVEL: info

secrets:
  - API_KEY
  - DB_PASSWORD

resources:
  memory: 512M
  cpus: 0.5

replicas: 2

healthcheck:
  type: http                     # http, tcp, cmd, none
  path: /health
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s

update:
  order: start-first             # start-first, stop-first
  parallelism: 1
  delay: 5s
  failure_action: rollback       # rollback, pause, continue

infra:
  - name: mydb
    prefix: DB                   # → DB_HOST, DB_PORT, DB_PASSWORD
  - name: cache
    prefix: REDIS

routes:
  - type: http
    domain: app.example.com
    port: 3000
  - type: http
    domain: api.example.com
    path: /v1/*
    port: 3001

persist:
  - /app/data
  - /app/uploads

dev:
  command: bun run dev
  port: 3000
  sync:
    ignore:
      - "*.log"
      - ".cache"
```

**Environment variable priority:** CLI flags → servel.yaml `env:` → `.env` files. `.env.local` never loaded (security).

**Build-time vs runtime:** `NEXT_PUBLIC_*` extracted locally as build args. Sensitive vars available at runtime only.

## Command Aliases

| Command | Aliases |
|---------|---------|
| `deploy` | `d`, `push` |
| `remove` | `rm`, `delete` |
| `logs` | `log` |
| `exec` | `x`, `run` |
| `inspect` | `i`, `info` |
| `rollback` | `rb` |
| `ps` | `ls`, `list` |
| `verify` | `v`, `check` |
| `doctor` | `dr` |
| `server` | `srv` |
| `port-forward` | `pf` |
| `watch` | `w` |
| `add` | `create`, `new` |
| `infra` | `infrastructure` |

## Common Workflows

**Deploy with database:**
```bash
servel add postgres --name mydb
servel deploy --link-infra mydb
# App receives DATABASE_URL, DB_HOST, DB_PORT, DB_PASSWORD
```

**Preview for PR:**
```bash
servel deploy --preview --ttl 24h
# Returns: https://myapp-pr42.example.com
```

**Backup and restore:**
```bash
servel infra backup mydb
servel infra restore mydb backup-2024-01-15.sql.gz
```

**Scale for traffic:**
```bash
servel scale myapp 5
```

**CI/CD deploy keys:**
```bash
servel server keys add prod --name github-actions --key-file pubkey.pub
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Nixpacks misdetects project | Create Dockerfile or use `--provider` |
| Port already in use | Override with `--port` flag |
| File sync not working | Check ignore patterns, SSH, restart session |
| Container exits immediately | Check logs, verify start command and port |
| Domain not accessible | Verify DNS, container status, Traefik routing |
| Context detection fails | Ensure `.servel/state.json` exists or specify app name |

**Diagnostic commands:**
```bash
servel doctor              # System health check
servel verify              # Configuration validation
servel logs <name>         # Application logs
servel inspect <name>      # Deployment details
servel server status       # Cluster health
```

## Documentation

- Full docs: https://servel.dev/docs
- Configuration: https://servel.dev/docs/configuration
- Infrastructure Hub: https://hub.servel.dev (explore 44+ pre-defined types)
- Dev mode: https://servel.dev/docs/dev-mode
