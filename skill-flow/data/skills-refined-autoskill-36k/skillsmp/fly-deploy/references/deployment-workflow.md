# Deployment Workflow

## Quick Start: New App

For deploying a new application to fly.io:

```bash
# Initialize and deploy in one command
fly launch
```

This interactive command:
1. Detects your app type and suggests a configuration
2. Creates `fly.toml` configuration file
3. Builds and deploys your app
4. Provisions a `.fly.dev` domain

**Important flags:**
- `--no-deploy` - Create config without deploying
- `--name <app-name>` - Specify app name (default: generated from directory)
- `--region <code>` - Choose primary region (default: nearest to you)
- `--org <org-name>` - Deploy to specific organization

## Deploying Existing fly.io Apps

For apps with existing `fly.toml`:

```bash
fly deploy
```

**Key flags:**
- `--remote-only` - Build on fly.io servers (recommended for CI/CD)
- `--local-only` - Build locally and push image
- `--strategy <strategy>` - Deployment strategy: `rolling`, `immediate`, `canary`
- `--ha=false` - Deploy single instance (useful for cost savings during dev)

## Essential fly.toml Configuration

### Minimal Configuration

```toml
app = "my-app"
primary_region = "ord"  # Chicago

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero when idle

[[vm]]
  size = "shared-cpu-1x"  # 256MB RAM, 1x shared CPU
  memory = "256mb"
```

### HTTP Service Configuration

```toml
[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"  # or "suspend" for faster wake-up
  auto_start_machines = true
  min_machines_running = 0

  # Health checks
  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"
```

### Environment Variables

Non-sensitive values in `fly.toml`:

```toml
[env]
  NODE_ENV = "production"
  PORT = "8080"
  LOG_LEVEL = "info"
```

Sensitive values via secrets (see `secrets-and-env.md`).

### Build Configuration

**Dockerfile-based:**
```toml
[build]
  dockerfile = "Dockerfile"
  # Optional: specify different Dockerfile
  # dockerfile = "deployments/prod.Dockerfile"
```

**Buildpacks (alternative):**
```toml
[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/nodejs"]
```

### Compute Resources

```toml
[[vm]]
  size = "shared-cpu-1x"    # 256MB, $0.0000008/s (~$2/month)
  # size = "shared-cpu-2x"  # 512MB, ~$4/month
  # size = "shared-cpu-4x"  # 1GB, ~$8/month
  # size = "shared-cpu-8x"  # 2GB, ~$15/month

  memory = "256mb"
  cpus = 1
```

### Release Commands

Run migrations or setup tasks before deployment:

```toml
[deploy]
  release_command = "npm run migrate"
  # or for Python: "python manage.py migrate"
  # or for Rust: "./target/release/migrate"
```

## Multi-Region Deployment

Deploy additional instances in other regions:

```bash
# View current regions
fly regions list

# Add regions
fly scale count 2 --region ord,iad

# Remove region
fly regions remove iad
```

In `fly.toml`:
```toml
primary_region = "ord"  # Where new machines are created by default
```

## Scaling

**Manual scaling:**
```bash
# Scale to specific machine count
fly scale count 3

# Scale specific machine size
fly scale vm shared-cpu-2x

# Scale with memory
fly scale memory 512
```

**Auto-scaling (configured in fly.toml):**
```toml
[http_service]
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0
  max_machines_running = 10  # Optional limit

[[http_service.concurrency]]
  type = "requests"
  hard_limit = 250
  soft_limit = 200
```

## Common Patterns

### Development Setup

```toml
[http_service]
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero to save costs

[[vm]]
  size = "shared-cpu-1x"
```

### Production Setup

```toml
[http_service]
  min_machines_running = 2  # Always 2 instances for HA
  max_machines_running = 10

[[vm]]
  size = "shared-cpu-2x"  # 512MB minimum for production
```

## Deployment Strategies

**Rolling (default):**
```bash
fly deploy --strategy rolling
```
- Starts new machines
- Waits for health checks
- Stops old machines
- Zero downtime

**Immediate:**
```bash
fly deploy --strategy immediate
```
- Stops all old machines
- Starts new machines
- Brief downtime, faster deployment

**Canary:**
```bash
fly deploy --strategy canary
```
- Deploy to single instance first
- Monitor before full rollout
- Best for risky changes

## Viewing Deployment Status

```bash
# Check app status
fly status

# View recent deployments
fly releases

# View specific release
fly releases list --image

# Monitor deployment logs
fly logs
```
