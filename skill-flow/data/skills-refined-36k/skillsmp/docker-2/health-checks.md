# Docker Automated Health Checks

Comprehensive health monitoring for Docker development containers.

---

## Container Healthcheck in docker-compose.yml

Add healthchecks to your services for reliable container monitoring:

```yaml
services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-project-dev-1
    ports:
      - '${DEV_PORT:-3000}:3000'
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    environment:
      - NODE_ENV=development
    command: tail -f /dev/null
    healthcheck:
      test: ['CMD', 'node', '-e', "console.log('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    profiles:
      - dev

  test:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-project-test-1
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    environment:
      - NODE_ENV=test
    command: npm test
    healthcheck:
      test: ['CMD', 'node', '-e', "console.log('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    profiles:
      - test

volumes:
  node_modules:
```

---

## Health Check Script (scripts/docker-health.sh)

Create a reusable health check script for pre-test verification:

```bash
#!/bin/bash
# Docker Health Check Script
# Ensures the development container is running and healthy before operations

set -e

CONTAINER_NAME="${CONTAINER_NAME:-my-project-dev-1}"
COMPOSE_PROFILE="${COMPOSE_PROFILE:-dev}"
MAX_WAIT_SECONDS=60
CHECK_INTERVAL=2

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
}

is_container_running() {
    docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" 2>/dev/null | grep -q "$CONTAINER_NAME"
}

is_container_healthy() {
    local status
    status=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "none")
    [ "$status" = "healthy" ]
}

start_container() {
    log_info "Starting Docker container with profile '$COMPOSE_PROFILE'..."
    docker compose --profile "$COMPOSE_PROFILE" up -d
}

wait_for_healthy() {
    local elapsed=0
    log_info "Waiting for container to be healthy..."
    while [ $elapsed -lt $MAX_WAIT_SECONDS ]; do
        if is_container_healthy; then
            log_info "Container is healthy!"
            return 0
        fi
        if ! is_container_running; then
            log_error "Container stopped unexpectedly"
            docker logs "$CONTAINER_NAME" --tail 20 2>/dev/null || true
            return 1
        fi
        sleep $CHECK_INTERVAL
        elapsed=$((elapsed + CHECK_INTERVAL))
        echo -n "."
    done
    echo ""
    log_warn "Container did not become healthy within ${MAX_WAIT_SECONDS}s"
    # Fallback: check if responsive
    if docker exec "$CONTAINER_NAME" node -e "console.log('ready')" &>/dev/null; then
        log_info "Container is responsive"
        return 0
    fi
    log_error "Container is not responsive"
    return 1
}

main() {
    log_info "Checking Docker environment..."
    check_docker
    if is_container_running; then
        log_info "Container '$CONTAINER_NAME' is already running"
        if is_container_healthy; then
            log_info "Container is healthy"
        elif docker exec "$CONTAINER_NAME" node -e "console.log('ready')" &>/dev/null; then
            log_info "Container is responsive"
        else
            log_warn "Container is running but not responsive, restarting..."
            docker compose --profile "$COMPOSE_PROFILE" restart
            wait_for_healthy
        fi
    else
        log_info "Container '$CONTAINER_NAME' is not running"
        start_container
        wait_for_healthy
    fi
    log_info "Docker environment ready!"
}

main "$@"
```

Make it executable: `chmod +x scripts/docker-health.sh`

---

## NPM Scripts Integration

Add health check to your package.json scripts:

```json
{
  "scripts": {
    "pretest": "bash scripts/docker-health.sh 2>/dev/null || true",
    "test": "vitest run",
    "docker:health": "bash scripts/docker-health.sh"
  }
}
```

**Benefits:**
- `npm test` automatically ensures container is running
- `npm run docker:health` for manual verification
- Silent failure in pretest prevents blocking when Docker unavailable

---

## Usage Patterns

```bash
# Manual health check
npm run docker:health

# Health check + tests (automatic via pretest)
npm test

# Custom container/profile
CONTAINER_NAME=custom-dev-1 COMPOSE_PROFILE=staging npm run docker:health
```

---

## Healthcheck Configuration Options

| Option | Description | Recommended Value |
|--------|-------------|-------------------|
| `test` | Command to run | `['CMD', 'node', '-e', "console.log('healthy')"]` |
| `interval` | Time between checks | `30s` |
| `timeout` | Max time per check | `10s` |
| `retries` | Failures before unhealthy | `3` |
| `start_period` | Grace period on start | `10s` |

---

## Troubleshooting Health Check Failures

### Container Shows "unhealthy"

```bash
# Check health check logs
docker inspect --format='{{json .State.Health}}' <container-name> | jq

# View recent health check output
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' <container-name>
```

### Health Check Never Passes

1. Verify Node.js is accessible in container:
   ```bash
   docker exec <container> which node
   docker exec <container> node --version
   ```

2. Check if command runs manually:
   ```bash
   docker exec <container> node -e "console.log('healthy')"
   ```

3. Increase `start_period` if container needs more initialization time

### Script Hangs Waiting for Healthy

- Increase `MAX_WAIT_SECONDS` in the script
- Check container logs for startup errors
- Verify the healthcheck command works inside container
