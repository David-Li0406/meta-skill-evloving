---
name: prepare-otterstack-deployment
description: Analyze a codebase and prepare it for OtterStack deployment by checking Docker Compose compatibility, scanning for environment variables, and validating configurations for zero-downtime deployments.
---

# Prepare OtterStack Deployment

Analyze a codebase and validate it's ready for OtterStack deployment by checking Docker Compose compatibility, scanning for environment variables, and detecting common failure patterns.

## Quick Start

Run these checks to verify OtterStack readiness:

```bash
# 1. Scan for environment variables
grep -rE '\$\{[A-Z_]+\}|\$[A-Z_]+' docker-compose.yml

# 2. Check compose compatibility
grep -E "container_name:|env_file:" docker-compose.yml  # Should be empty

# 3. Validate syntax
docker compose config --quiet
```

If all checks pass → ready to deploy. If issues found → follow the detailed workflow below.

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

Find all variables referenced in compose file:

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
grep -A 10 "^networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

**Identify default network:**
1. If networks section exists, use the first network listed as default.
2. If no networks section, Docker Compose creates a default network named `{project}_default`.
3. Recommend explicit network definition for clarity.

**Check service network attachments:**
```bash
grep -B 5 "networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

**Network configuration requirements:**
- All services should attach to the same network for inter-service communication.
- Network name should use variable substitution: `${NETWORK_NAME:-app-network}`.
- Network should be defined explicitly at the bottom of compose file.

**Example network configuration:**
```yaml
services:
  web:
    networks:
      - ${NETWORK_NAME:-app-network}

  api:
    networks:
      - ${NETWORK_NAME:-app-network}

networks:
  app-network:
    name: ${NETWORK_NAME:-app-network}
    external: false
```

### Scan Dockerfile

Check for ARG and ENV declarations:

```bash
grep -E "^(ENV|ARG)\s+" Dockerfile
```

### Consolidate Results

For each variable found:
1. Determine if it's **required** (no default) or **optional** (has default).
2. Identify the **purpose** (database URL, API key, port, etc).
3. Flag **sensitive** variables (passwords, keys, tokens).
4. Note any **default values** from code.

## Compose File Validation

### Critical OtterStack Requirements

#### ❌ 1. No Hardcoded Container Names

**Check:**
```bash
grep "container_name:" docker-compose.yml
```

**Why it fails**: OtterStack creates unique container names per deployment (e.g., `myapp-abc1234-web-1`). Hardcoded names prevent parallel deployments and zero-downtime updates.

**Fix**: Remove all `container_name:` directives.

**Before:**
```yaml
services:
  web:
    container_name: myapp-web  # ❌ Remove this
    image: myapp:latest
```

**After:**
```yaml
services:
  web:
    # ✅ Let Docker Compose generate names
    image: myapp:latest
```

#### ✅ 2. Use Environment Section (Not env_file)

**Check:**
```bash
grep "env_file:" docker-compose.yml
```

**Why it fails**: OtterStack passes `--env-file` to Docker Compose for variable substitution in the compose file itself. Variables must be in the `environment:` section to be injected into containers.

**Fix**: Move to `environment:` section with variable substitution.

**Before:**
```yaml
services:
  web:
    env_file: .env  # ❌ This doesn't work with OtterStack
```

**After:**
```yaml
services:
  web:
    environment:  # ✅ Use environment section
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}  # With default
```

#### ❌ 3. No Static Traefik Priority Labels

**Check:**
```bash
grep "traefik.http.routers.*.priority" docker-compose.yml
```

**Why it fails**: OtterStack manages Traefik priority labels automatically for zero-downtime deployments. Static priorities conflict with this mechanism.

**Fix**: Remove priority labels, keep other Traefik labels.

**Before:**
```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`example.com`)"
  - "traefik.http.routers.myapp.priority=100"  # ❌ Remove this
```

**After:**
```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`example.com`)"
  # ✅ OtterStack manages priorities automatically
```

#### ✅ 4. Health Checks Defined

**Check:**
```bash
grep -A5 "healthcheck:" docker-compose.yml
```

**Why it matters**: OtterStack waits for containers to be healthy before routing traffic. Without health checks, containers are immediately considered healthy (which may not be accurate).

**Best practice**: Define explicit health checks.

**Example:**
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s
```

**Critical**: Use `127.0.0.1` not `localhost` to avoid IPv6 issues.

#### ✅ 5. Syntax Validation

**Check:**
```bash
docker compose config --quiet
```

If this command fails, the compose file has syntax errors that must be fixed before deployment.

## Common Failure Detection

### 1. Native Module Bindings (Node.js)

**Check:**
```bash
grep -E "node-gyp|native|binding|better-sqlite3|bcrypt|sharp" package.json
```

**Problem**: Native modules compiled on your dev machine won't work in the production container due to different architectures.

**Solution**: Use multi-stage build and rebuild in production stage.

**Example fix in Dockerfile:**
```dockerfile
# Production stage
FROM node:20-slim

# Install build tools for native modules
RUN apt-get update && \
    apt-get install -y build-essential python3 && \
    apt-get clean

# Copy node_modules from builder
COPY --from=builder /build/node_modules ./node_modules

# Rebuild native modules for production architecture
RUN npm rebuild better-sqlite3

# Rest of dockerfile...
```

### 2. Database Path Permissions

**Check:**
```bash
grep -A2 "volumes:" docker-compose.yml | grep -E "\.db|/data"
```

**Problem**: Container user may not have write permissions to database directory.

**Solution**: Use named volumes OR ensure directory ownership in Dockerfile.

**Named volume approach (recommended):**
```yaml
volumes:
  - db-data:/app/data  # Named volume with correct permissions

volumes:
  db-data:
    name: myapp-db-data
```

**Dockerfile ownership approach:**
```dockerfile
# Create directories with correct ownership
RUN mkdir -p /app/data && chown -R app:app /app/data

# Switch to non-root user
USER app
```

### 3. Migration File Paths

**Check:**
```bash
grep "COPY.*migrations\|COPY.*prisma\|COPY.*db" Dockerfile
```

**Problem**: Migration files not copied to container or copied to wrong location.

**Solution**: Ensure migrations are copied to where your application expects them.

**Example**:
```dockerfile
# If your app looks for migrations relative to dist/index.js:
COPY src/migrations ./dist/migrations

# Not:
COPY src/migrations ./src/migrations  # ❌ Wrong location
```

### 4. IPv6/IPv4 Health Check Conflicts

**Check:**
```bash
grep -A3 "healthcheck:" docker-compose.yml | grep "localhost"
```

**Problem**: BusyBox `wget` and some `curl` versions try IPv6 (::1) first when resolving `localhost`, but app may only bind to IPv4 (0.0.0.0).

**Solution**: Use `127.0.0.1` instead of `localhost` in health checks.

**Before:**
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://localhost:80/health"]  # ❌
```

**After:**
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://127.0.0.1:80/health"]  # ✅
```

### 5. Missing Build Context

**Check:**
```bash
grep -A2 "build:" docker-compose.yml | grep -v "context:"
```

**Problem**: Build may fail or use wrong directory if context not explicit.

**Solution**: Always specify `context:` and `dockerfile:`.

**Before:**
```yaml
build: .  # ❌ Implicit context
```

**After:**
```yaml
build:  # ✅ Explicit context
  context: .
  dockerfile: Dockerfile
```

### 6. Missing Network Definition

**Check:**
```bash
# Check if networks are defined
grep "^networks:" docker-compose.yml

# Check if services specify network
grep -A 2 "services:" docker-compose.yml | grep "networks:"
```

**Problem**: Services on different networks (or default networks) may have connectivity issues in complex deployments. OtterStack needs to know which network containers communicate on.

**Solution**: Define an explicit network and use variable substitution for flexibility.

**Before:**
```yaml
services:
  web:
    image: myapp:latest
    # No network specified - uses auto-generated default
```

**After:**
```yaml
services:
  web:
    image: myapp:latest
    networks:
      - ${NETWORK_NAME:-app-network}

networks:
  app-network:
    name: ${NETWORK_NAME:-app-network}
    external: false
```

## Traefik Exposure Detection

For services that need to be publicly accessible, detect existing Traefik configuration and prepare for enhanced labels:

### Scan for Traefik Labels

**Check for Traefik-enabled services:**
```bash
grep -B 5 "traefik.enable" docker-compose.yml | grep -E "^  [a-z].*:" | sed 's/:$//'
```

**Extract router names:**
```bash
grep "traefik.http.routers" docker-compose.yml | sed -E 's/.*traefik\.http\.routers\.([^.]+)\..*/\1/' | sort -u
```

**Identify exposed services:**
For each service with Traefik labels:
1. Extract service name from docker-compose.yml structure.
2. Extract router name from labels.
3. Check if domain variable is used (e.g., `${API_DOMAIN}`).
4. Note the exposed port from load balancer configuration.

### Required Traefik Configuration

Services exposed via Traefik should have these labels at minimum:

```yaml
labels:
  - "traefik.enable=true"
  # Routing
  - "traefik.http.routers.{service}.rule=Host(`${SERVICE_DOMAIN}`)"
  - "traefik.http.routers.{service}.entrypoints=web,websecure"
  # TLS
  - "traefik.http.routers.{service}.tls=true"
  - "traefik.http.routers.{service}.tls.certresolver=myresolver"
  # Load balancer
  - "traefik.http.services.{service}.loadbalancer.server.port={PORT}"
  # CrowdSec middleware (security)
  - "traefik.http.routers.{service}.middlewares=crowdsec-{service}@docker"
  - "traefik.http.middlewares.crowdsec-{service}.plugin.crowdsec-bouncer.enabled=true"
  - "traefik.http.middlewares.crowdsec-{service}.plugin.crowdsec-bouncer.crowdseclapikey=${CROWDSEC_API_KEY}"
```

### Environment Variables for Exposure

For each exposed service, these environment variables are required:

1. **`${SERVICE}_DOMAIN`** - The domain name for the service (e.g., `API_DOMAIN=api.example.com`)
   - Type: String (domain format)
   - Validation: Must be a valid domain without protocol
   - Example: `aperture.example.com`, `api.myapp.io`

2. **`CROWDSEC_API_KEY`** - CrowdSec bouncer API key for security middleware
   - Type: String (sensitive)
   - Validation: Non-empty string
   - Shared across all exposed services
   - Obtain from: CrowdSec dashboard → Bouncers → Add bouncer

3. **`NETWORK_NAME`** - The Docker network name for Traefik communication
   - Type: String
   - Default: Detected from compose file or `app-network`
   - Traefik must be on the same network to route traffic

## Output Format

Generate a readiness report following this template:

```markdown
## OtterStack Readiness Report for [Project Name]

### ✅ Compatible Checks
- Docker Compose syntax validation passed
- Health checks defined for all services
- Uses environment: section for variables
- No hardcoded container names

### 🌐 Networks Detected

**Default network:** `app-network`

**All networks:**
- `app-network` (default)
- `traefik-network` (external, for Traefik communication)

**Service attachments:**
- `web` → app-network, traefik-network
- `api` → app-network, traefik-network
- `db` → app-network (internal only)

**Recommendations:**
- Add `NETWORK_NAME` environment variable for flexibility
- Ensure Traefik is on `traefik-network` for routing

### 🔒 Traefik Exposure

**Exposed services:**

1. **API Service** (`api`)
   - Router: `aperture-api`
   - Port: 8080
   - Domain variable: `API_DOMAIN`
   - CrowdSec: Enabled

2. **Web Service** (`web`)
   - Router: `aperture-web`
   - Port: 3000
   - Domain variable: `WEB_DOMAIN`
   - CrowdSec: Enabled

**Required for exposure:**
- `API_DOMAIN` - Domain for API service (e.g., api.example.com)
- `WEB_DOMAIN` - Domain for web service (e.g., app.example.com)
- `CROWDSEC_API_KEY` - CrowdSec bouncer key (shared)
- `NETWORK_NAME` - Network for Traefik communication

### ⚠️  Issues Found

1. **Container name conflict** (docker-compose.yml:15)
   - Found: `container_name: myapp