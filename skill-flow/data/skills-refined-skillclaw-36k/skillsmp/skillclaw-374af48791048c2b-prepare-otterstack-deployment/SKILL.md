---
name: prepare-otterstack-deployment
description: Use this skill when analyzing a codebase to ensure it is ready for OtterStack deployment, including checking Docker Compose compatibility and scanning for environment variables.
---

# Prepare OtterStack Deployment

Analyze a codebase and validate its readiness for OtterStack deployment by checking Docker Compose compatibility, scanning for environment variables, and detecting common failure patterns.

## Quick Start

Run these three checks to verify OtterStack readiness:

```bash
# 1. Scan for environment variables
grep -rE '\$\{[A-Z_]+\}|\$[A-Z_]+' docker-compose.yml

# 2. Check compose compatibility
grep -E "container_name:|env_file:" docker-compose.yml  # Should be empty

# 3. Validate syntax
docker compose config --quiet
```

If all checks pass → ready to deploy. If issues are found → follow the detailed workflow below.

## Environment Variable Discovery

### Scan Application Code

Different languages use different patterns for environment variables:

**Node.js / TypeScript:**
```bash
grep -r "process\.env\." --include="*.js" --include="*.ts"
```

**Python:**
```bash
grep -r "os\.getenv\|os\.environ" --include="*.py"
```

**Ruby:**
```bash
grep -r "ENV\[" --include="*.rb"
```

**Go:**
```bash
grep -r "os\.Getenv" --include="*.go"
```

### Scan Docker Compose File

Find all variables referenced in the compose file:

```bash
grep -oE '\$\{[A-Z_][A-Z0-9_]*\}' docker-compose.yml | sort -u
```

### Network Detection

Detect networks defined in the Docker Compose file to ensure proper container connectivity:

**Find network definitions:**
```bash
grep -A 5 "^networks:" docker-compose.yml
```

**Extract network names:**
```bash
# Get all network names from the networks section
grep -A 10 "^networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

**Identify default network:**
1. If a networks section exists, use the first network listed as default.
2. If no networks section exists, Docker Compose creates a default network named `{project}_default`.
3. Recommend explicit network definition for clarity.

**Check service network attachments:**
```bash
# Find services that specify networks
grep -B 5 "networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

## Compose File Validation

### Critical OtterStack Requirements

#### ❌ 1. No Hardcoded Container Names

**Check:**
```bash
grep "container_name:" docker-compose.yml
```

**Why it fails**: OtterStack creates unique container names per deployment (e.g., `myapp-abc1234-web-1`). Hardcoded names prevent parallel deployments and zero-downtime updates.

**Fix**: Remove all `container_name:` directives.