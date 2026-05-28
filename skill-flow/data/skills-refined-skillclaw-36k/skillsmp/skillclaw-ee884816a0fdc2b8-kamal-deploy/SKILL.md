---
name: kamal-deploy
description: Use this skill when deploying Rails applications with Kamal, configuring deploy.yml, managing secrets, or executing deployment commands.
---

# Kamal Deploy

## Overview

Kamal deploys containerized Rails applications to bare metal or VMs using Docker, ensuring zero-downtime deployments with Traefik as a reverse proxy.

## Server Requirements

Before deploying with Kamal, ensure your servers meet the following requirements:

| Requirement | Purpose |
|-------------|---------|
| Docker | Container runtime |
| SSH access | Kamal connects via SSH |
| Ports 80, 443 open | HTTP/HTTPS traffic |
| Port 22 open | SSH for deployments |

**Provision with:** Ansible or cloud-init at boot time.

## Installation and Initialization

1. Install Kamal: 
   ```bash
   gem install kamal
   ```
2. Initialize in your Rails application:
   ```bash
   kamal init
   ```
   This creates `config/deploy.yml` and `.kamal/secrets`.

## Configuration: config/deploy.yml

### Minimal Setup

```yaml
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1
    labels:
      traefik.http.routers.myapp.rule: Host(`myapp.com`)

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

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
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1
      - 192.168.1.2
    labels:
      traefik.http.routers.myapp.rule: Host(`myapp.com`)
  worker:
    hosts:
      - 192.168.1.3
    cmd: bundle exec sidekiq
    traefik: false  # No HTTP traffic

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

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
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1

accessories:
  db:
    image: postgres:16
    host: 192.168.1.1
    port: 5432
    env:
      clear:
        POSTGRES_DB: myapp_production
      secret:
        - POSTGRES_PASSWORD
    directories:
      - data:/var/lib/postgresql/data
    options:
      shm-size: 256m

  redis:
    image: redis:7-alpine
    host: 192.168.1.1
    port: 6379
    directories:
      - data:/data
    cmd: redis-server --appendonly yes
```

## Deployment Workflow

1. Run `kamal setup` for initial deployments or new servers.
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

## Secrets Management

Kamal reads secrets from `.kamal/secrets` (which should be git-ignored) or from environment variables. Example entries in `.kamal/secrets`:

```
DATABASE_URL=postgres://...
RAILS_MASTER_KEY=...
KAMAL_REGISTRY_PASSWORD=...
```

Note: `kamal config` prints the merged configuration including secrets.