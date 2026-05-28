---
name: kamal-deployment
description: Use this skill when deploying Rails applications with Kamal, configuring deploy.yml, managing secrets, or executing deployment commands.
---

# Kamal Deployment

## Overview

Kamal deploys containerized Rails applications to bare metal or VMs using Docker, ensuring zero-downtime deployments with Traefik as a reverse proxy.

## Server Requirements

Before deploying with Kamal, ensure the following server requirements are met:

| Requirement | Purpose |
|-------------|---------|
| Docker | Container runtime |
| SSH access | Kamal connects via SSH |
| Ports 80, 443 open | HTTP/HTTPS traffic |
| Port 22 open | SSH for deployments |

**Provision with:** Ansible or cloud-init at boot time.

## Configuration: config/deploy.yml

### Minimal Setup

```yaml
service: <service_name>
image: <docker_image>

servers:
  web:
    hosts:
      - <web_server_ip>
    labels:
      traefik.http.routers.<service_name>.rule: Host(`<domain_name>`)

registry:
  username: <docker_username>
  password:
    - <registry_password>

env:
  clear:
    RAILS_ENV: production
    RAILS_LOG_TO_STDOUT: "true"
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
```

### Multi-Role Setup

```yaml
service: <service_name>
image: <docker_image>

servers:
  web:
    hosts:
      - <web_server_ip>
      - <additional_web_server_ip>
    labels:
      traefik.http.routers.<service_name>.rule: Host(`<domain_name>`)
  worker:
    hosts:
      - <worker_server_ip>
    cmd: bundle exec sidekiq
    traefik: false  # No HTTP traffic

registry:
  username: <docker_username>
  password:
    - <registry_password>

env:
  clear:
    RAILS_ENV: production
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
    - REDIS_URL
```

### With Accessories (Databases, Redis)

```yaml
service: <service_name>
image: <docker_image>

servers:
  web:
    hosts:
      - <web_server_ip>

accessories:
  db:
    image: postgres:<version>
    host: <db_host>
    port: <db_port>
    env:
      clear:
        POSTGRES_DB: <db_name>
      secret:
        - POSTGRES_PASSWORD
    directories:
      - data:/var/lib/postgresql/data
    options:
      shm-size: 256m

  redis:
    image: redis:<version>
    host: <redis_host>
    port: <redis_port>
    directories:
      - data:/data
    cmd: redis-server --appendonly yes
```

## Secrets Management

Kamal reads secrets from `.kamal/secrets` (git-ignored).

### With 1Password CLI

```bash
# .kamal/secrets
KAMAL_REGISTRY_PASSWORD=$(op read "op://Infrastructure/DockerHub/password")
RAILS_MASTER_KEY=$(op read "op://MyApp/production/master_key")
DATABASE_URL=$(op read "op://MyApp/production/database_url")
POSTGRES_PASSWORD=$(op read "op://MyApp/production-db/password")
```

### With Environment Variables

```bash
# .kamal/secrets
KAMAL_REGISTRY_PASSWORD=$DOCKERHUB_TOKEN
RAILS_MASTER_KEY=$RAILS_MASTER_KEY
DATABASE_URL=$DATABASE_URL
```

## Deployment Workflow

1. Run `kamal setup` for the first deployment or new servers.
2. Use `kamal deploy` for routine releases.
3. Use `kamal rollback [VERSION]` for fast recovery.

## Common Commands

- Help: `kamal --help`
- Show merged config: `kamal config`
- Deploy: `kamal deploy`
- Redeploy without bootstrap: `kamal redeploy`
- Rollback: `kamal rollback [VERSION]`
- Remove app/proxy/accessories: `kamal remove`
- Cleanup: `kamal prune`
- Manage app: `kamal app` (see `kamal app --help`)
- Manage accessories: `kamal accessory` (see `kamal accessory --help`)
- Manage proxy: `kamal proxy`
- Server bootstrap only: `kamal server`

## Health Checks and Troubleshooting

### Health Checks

```yaml
healthcheck:
  path: /up
  port: 3000
  interval: 10s
  max_attempts: 30
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Connection refused | Docker not running | `kamal server bootstrap` |
| Permission denied | SSH key not authorized | Check server's authorized_keys |
| Health check failing | App not starting | Check `kamal app logs` |
| Registry auth failed | Wrong credentials | Verify `.kamal/secrets` |
| Traefik 502 | Container not healthy | Increase `max_attempts` |

## Directory Structure

```
<app_name>/
├── config/
│   └── deploy.yml        # Main Kamal config
├── .kamal/
│   ├── secrets           # Secret values (git-ignored)
│   ├── secrets.staging   # Staging secrets (git-ignored)
│   └── hooks/
│       ├── pre-deploy
│       └── post-deploy
└── Dockerfile            # Application container
```

## Hooks

### Pre-Deploy

```bash
# .kamal/hooks/pre-deploy
#!/bin/sh
echo "Running pre-deploy tasks..."
bundle exec rails assets:precompile
```

### Post-Deploy

```bash
# .kamal/hooks/post-deploy
#!/bin/sh
echo "Running migrations..."
kamal app exec "bin/rails db:migrate"
```