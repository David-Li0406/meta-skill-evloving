---
name: do-yaml
description: "Create and configure do.yaml files for the Docker Compose wrapper CLI. Use when the user asks to: (1) Create or set up a do.yaml configuration file, (2) Add profiles, aliases, or hooks to their Docker Compose setup, (3) Configure environment-specific compose files like dev/prod/staging, (4) Set up automation hooks for container lifecycle events, (5) Define command shortcuts for common Docker Compose operations. The do.yaml file is the project-local configuration for the 'do' CLI tool that simplifies multi-file Docker Compose setups."
---

# do.yaml Configuration Creator

Create and configure `do.yaml` files for the Docker Compose wrapper CLI.

## Quick Start

Ask the user what they need:

1. **Project structure** - How many compose files? What naming pattern?
2. **Environments** - dev, prod, staging, etc.?
3. **Automation needs** - Pre/post hooks? Command aliases?

Then create `do.yaml` in the project root.

## Schema Reference

### File Structure

```yaml
version: 1                    # Required

defaults:                     # Optional
  profile: "dev"             # Default profile to use
  slice: "dev"               # Default slice (fallback)
  auto_detect: true          # Detect profile from git branch

profiles:                     # Environment configurations
  dev:
    slices: [dev]            # compose.dev.yaml
  prod:
    slices: [prod]
    extends: dev             # Inherit dev's slices

env_files:                    # Reusable env file mappings
  dev: ".env.dev"
  prod: ".env.prod"

aliases:                      # Command shortcuts
  fresh: "down -v && up --build -d"

hooks:                        # Lifecycle hooks
  pre_up:
    - echo "Starting..."
  post_up:
    - echo "Ready!"
```

### Discovery Configuration

```yaml
discovery:
  enabled: true              # Auto-discover compose files
  pattern: "compose.*.yaml"  # File pattern
  base: "compose.yaml"       # Base file name
```

Auto-discovery finds:
- Base: `compose.yaml` (preferred), `docker-compose.yaml`
- Slices: `compose.<name>.yaml` (alphabetical)

### Profile Inheritance

Child profiles inherit parent slices (prepended, de-duplicated):

```yaml
profiles:
  base:
    slices: [base]
  dev:
    slices: [dev]
    extends: base            # Result: [base, dev]
  full:
    slices: [extra]
    extends: dev             # Result: [base, dev, extra]
```

### Aliases

Chain docker compose commands with `&&`:

```yaml
aliases:
  fresh: "down -v && up --build -d"
  restart-all: "down && up -d"
  full-start: "down -v && up --build -d && logs -f"
  clean: "down -v --remove-orphans"
```

Usage: `do c fresh`, `do c restart-all`

### Hooks

Available hooks: `pre_up`, `post_up`, `pre_down`, `post_down`

```yaml
hooks:
  pre_up:
    - docker network prune -f
    - echo "Starting services..."
  post_up:
    - echo "Services running at http://localhost:3000"
  pre_down:
    - echo "Stopping..."
  post_down:
    - echo "Cleanup complete"
```

Hooks:
- Run in shell context (`sh -c`)
- Stop on first failure
- Pre hooks: failure blocks main command
- Post hooks: only run on success

## File Discovery Priority

1. Explicit `-f` flags (highest)
2. `do.yaml` profile configuration
3. Auto-discovery

## Common Patterns

### Simple Project

```yaml
version: 1

defaults:
  profile: dev

profiles:
  dev:
    slices: [dev]
  prod:
    slices: [prod]
```

Corresponding files: `compose.yaml`, `compose.dev.yaml`, `compose.prod.yaml`

### With Environment Files

```yaml
version: 1

env_files:
  dev: .env.dev
  prod: .env.prod
  staging: .env.staging

profiles:
  dev:
    slices: [dev]
    env: dev
  prod:
    slices: [prod]
    env: prod
```

### Multi-Service Stacks

```yaml
version: 1

profiles:
  base:
    slices: [base]
  app:
    slices: [app]
    extends: base
  db:
    slices: [db]
    extends: base
  full:
    slices: [monitoring]
    extends: app
```

Files: `compose.yaml`, `compose.base.yaml`, `compose.app.yaml`, `compose.db.yaml`, `compose.monitoring.yaml`

## Creation Workflow

1. Ask about project structure and environments
2. Determine needed profiles and slices
3. Add optional features (aliases, hooks, env_files)
4. Create `do.yaml` in project root
5. Verify the file exists and is valid YAML
