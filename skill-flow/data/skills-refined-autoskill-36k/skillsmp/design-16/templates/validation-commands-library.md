# Validation Commands Library

> Reusable bash command snippets for PRP validation. Copy and customize for your specific project.

---

## Purpose

Every PRP should include a "Validation Commands" section with concrete, copy-pasteable bash commands. This library provides templates organized by category.

---

## Testing Commands

### Unit Tests

```bash
# Python (pytest)
pytest tests/ -v --cov=src --cov-report=term-missing
pytest tests/unit/ -v -x  # Stop on first failure
pytest tests/ -k "test_feature_name" -v  # Run specific tests

# JavaScript/TypeScript (Jest)
npm test -- --coverage
npm test -- --testPathPattern="feature.test"
npx jest --watch  # Development mode

# Go
go test ./... -v -cover
go test ./... -race  # Race condition detection
go test -bench=. ./...  # Benchmarks
```

### Integration Tests

```bash
# Run integration tests (typically slower, may need services)
pytest tests/integration/ -v --timeout=300
npm run test:integration
go test ./... -tags=integration -v

# With Docker services
docker-compose -f docker-compose.test.yml up -d
pytest tests/integration/ -v
docker-compose -f docker-compose.test.yml down
```

### End-to-End Tests

```bash
# Playwright
npx playwright test
npx playwright test --headed  # Visual debugging
npx playwright test --project=chromium

# Cypress
npx cypress run
npx cypress run --spec "cypress/e2e/checkout.cy.ts"

# Selenium
pytest tests/e2e/ -v --browser=chrome
```

---

## Type Checking

### Python

```bash
# mypy (strict)
mypy src/ --strict
mypy src/ --ignore-missing-imports
mypy src/ --show-error-codes

# pyright
pyright src/
```

### TypeScript

```bash
# TypeScript compiler
npx tsc --noEmit
npx tsc --noEmit --strict

# With project config
npx tsc -p tsconfig.json --noEmit
```

### Go

```bash
# Go vet (built-in)
go vet ./...

# staticcheck (recommended)
staticcheck ./...
```

---

## Linting

### Python

```bash
# ruff (fast, recommended)
ruff check src/
ruff check src/ --fix  # Auto-fix

# flake8
flake8 src/ --max-line-length=100

# black (formatting)
black src/ --check
black src/  # Apply formatting
```

### JavaScript/TypeScript

```bash
# ESLint
npx eslint src/ --ext .js,.ts,.tsx
npx eslint src/ --fix

# Prettier (formatting)
npx prettier --check "src/**/*.{js,ts,tsx}"
npx prettier --write "src/**/*.{js,ts,tsx}"
```

### Go

```bash
# gofmt
gofmt -l .
gofmt -w .  # Apply formatting

# golangci-lint (comprehensive)
golangci-lint run
golangci-lint run --fix
```

---

## API Validation

### curl Commands

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health

# GET request with headers
curl -X GET "http://localhost:8080/api/v1/resource" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# POST request with body
curl -X POST "http://localhost:8080/api/v1/resource" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Verify response contains expected data
curl -s "http://localhost:8080/api/v1/resource/1" | jq '.status == "active"'
```

### httpie Commands

```bash
# GET request
http GET localhost:8080/api/v1/resource Authorization:"Bearer $TOKEN"

# POST request
http POST localhost:8080/api/v1/resource key=value

# Check response status
http --check-status GET localhost:8080/health
```

### API Contract Testing

```bash
# OpenAPI validation
npx @stoplight/spectral-cli lint openapi.yaml

# Dredd (API Blueprint)
dredd api-description.apib http://localhost:8080

# Postman/Newman
newman run collection.json -e environment.json
```

---

## Database Validation

### PostgreSQL

```bash
# Check connection
psql "$DATABASE_URL" -c "SELECT 1"

# Row count verification
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM table_name"

# Schema verification
psql "$DATABASE_URL" -c "\d+ table_name"

# Data integrity check
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM orders WHERE status IS NULL"
```

### MySQL

```bash
# Check connection
mysql -h host -u user -p -e "SELECT 1"

# Row count
mysql -h host -u user -p database -e "SELECT COUNT(*) FROM table_name"
```

### SQLite

```bash
# Check database
sqlite3 database.db "SELECT COUNT(*) FROM table_name"

# Schema check
sqlite3 database.db ".schema table_name"
```

### Redis

```bash
# Check connection
redis-cli ping

# Key count
redis-cli DBSIZE

# Specific key check
redis-cli GET key_name
redis-cli EXISTS key_name
```

---

## File System Validation

### File Existence

```bash
# Single file
test -f path/to/file.txt && echo "EXISTS" || echo "MISSING"

# Multiple files
for f in config.yaml schema.sql init.sh; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done

# Directory exists
test -d path/to/directory && echo "EXISTS" || echo "MISSING"
```

### File Permissions

```bash
# Check executable
test -x script.sh && echo "EXECUTABLE" || echo "NOT EXECUTABLE"

# Check readable
test -r config.yaml && echo "READABLE" || echo "NOT READABLE"

# Check write permission
test -w output/ && echo "WRITABLE" || echo "NOT WRITABLE"
```

### File Content

```bash
# Contains expected string
grep -q "expected_string" file.txt && echo "FOUND" || echo "NOT FOUND"

# Does NOT contain forbidden string
! grep -q "forbidden" file.txt && echo "OK" || echo "VIOLATION FOUND"

# Line count
wc -l < file.txt
```

---

## Service Health Checks

### HTTP Services

```bash
# Basic health check
curl -sf http://localhost:8080/health > /dev/null && echo "HEALTHY" || echo "UNHEALTHY"

# With timeout
curl -sf --max-time 5 http://localhost:8080/health

# Multiple services
for svc in api:8080 web:3000 worker:8081; do
  name=${svc%:*}
  port=${svc#*:}
  curl -sf "http://localhost:$port/health" > /dev/null \
    && echo "$name: HEALTHY" || echo "$name: UNHEALTHY"
done
```

### Docker Services

```bash
# Container running
docker ps --filter "name=service_name" --format "{{.Status}}"

# Container health
docker inspect --format='{{.State.Health.Status}}' container_name

# All services healthy
docker-compose ps --filter "status=running"
```

### Process Checks

```bash
# Process running
pgrep -f "process_name" > /dev/null && echo "RUNNING" || echo "NOT RUNNING"

# Port in use
lsof -i :8080 > /dev/null && echo "PORT IN USE" || echo "PORT FREE"

# netstat alternative
ss -tlnp | grep :8080
```

---

## Configuration Validation

### YAML

```bash
# Syntax check
python -c "import yaml; yaml.safe_load(open('config.yaml'))" \
  && echo "VALID YAML" || echo "INVALID YAML"

# Or with yq
yq eval '.' config.yaml > /dev/null && echo "VALID" || echo "INVALID"
```

### JSON

```bash
# Syntax check
python -c "import json; json.load(open('config.json'))" \
  && echo "VALID JSON" || echo "INVALID JSON"

# Or with jq
jq '.' config.json > /dev/null && echo "VALID" || echo "INVALID"

# Required fields present
jq -e '.database_url and .api_key' config.json > /dev/null \
  && echo "REQUIRED FIELDS PRESENT" || echo "MISSING REQUIRED FIELDS"
```

### Environment Variables

```bash
# Required env vars set
for var in DATABASE_URL API_KEY SECRET_KEY; do
  [ -n "${!var}" ] && echo "$var: SET" || echo "$var: MISSING"
done

# .env file exists and has required vars
test -f .env && grep -q "^DATABASE_URL=" .env \
  && echo "OK" || echo "MISSING DATABASE_URL in .env"
```

---

## Security Validation

### Secrets Detection

```bash
# Check for hardcoded secrets (basic)
! grep -rE "(password|secret|api_key)\s*=\s*['\"][^'\"]+['\"]" src/ \
  && echo "NO HARDCODED SECRETS" || echo "POTENTIAL SECRETS FOUND"

# Gitleaks
gitleaks detect --source . --verbose

# Trufflehog
trufflehog filesystem --directory=.
```

### Dependency Vulnerabilities

```bash
# Python
pip-audit
safety check

# JavaScript
npm audit
npm audit --audit-level=high

# Go
govulncheck ./...
```

### SSL/TLS Checks

```bash
# Certificate validity
openssl s_client -connect domain.com:443 -servername domain.com </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# SSL Labs grade (via API)
curl -s "https://api.ssllabs.com/api/v3/analyze?host=domain.com" | jq '.endpoints[0].grade'
```

---

## Performance Validation

### Load Testing

```bash
# hey (simple HTTP load testing)
hey -n 1000 -c 50 http://localhost:8080/api/endpoint

# wrk
wrk -t12 -c400 -d30s http://localhost:8080/api/endpoint

# k6
k6 run loadtest.js
```

### Memory/CPU Checks

```bash
# Process memory usage
ps -o rss= -p $(pgrep -f "process_name") | awk '{print $1/1024 " MB"}'

# Docker container stats
docker stats --no-stream container_name --format "{{.MemUsage}}"
```

---

## Build Validation

### Build Success

```bash
# Node.js
npm run build && echo "BUILD SUCCESS" || echo "BUILD FAILED"

# Go
go build ./... && echo "BUILD SUCCESS" || echo "BUILD FAILED"

# Python (wheel)
python -m build && echo "BUILD SUCCESS" || echo "BUILD FAILED"

# Docker
docker build -t app:test . && echo "BUILD SUCCESS" || echo "BUILD FAILED"
```

### Artifact Verification

```bash
# Check build output exists
test -d dist/ && ls -la dist/

# Check binary exists and runs
./bin/app --version

# Check Docker image
docker images app:test --format "{{.Size}}"
```

---

## Composite Validation Scripts

### Pre-Commit Validation

```bash
#!/bin/bash
# Run all pre-commit checks

set -e

echo "=== Linting ==="
ruff check src/

echo "=== Type Checking ==="
mypy src/ --strict

echo "=== Unit Tests ==="
pytest tests/unit/ -v

echo "=== All checks passed ==="
```

### Pre-Deploy Validation

```bash
#!/bin/bash
# Run all pre-deployment checks

set -e

echo "=== Running Tests ==="
pytest tests/ -v --cov=src

echo "=== Checking Dependencies ==="
pip-audit

echo "=== Building ==="
docker build -t app:$(git rev-parse --short HEAD) .

echo "=== Health Check ==="
docker run -d --name test-container -p 8080:8080 app:$(git rev-parse --short HEAD)
sleep 5
curl -sf http://localhost:8080/health && echo "HEALTHY"
docker rm -f test-container

echo "=== Ready for deployment ==="
```

---

## Usage in PRPs

When adding validation commands to a PRP, include 3-5 specific commands that verify:

1. **Tests pass** - Unit and/or integration tests
2. **Code quality** - Linting and type checking
3. **Integration works** - API or service health checks
4. **Data integrity** - Database or file checks (if applicable)
5. **Build succeeds** - Compilation or packaging

Example PRP section:

```markdown
## 8. Validation Commands

Run these commands to verify the implementation:

```bash
# 1. Run tests
pytest tests/ -v --cov=src

# 2. Type checking
mypy src/ --strict

# 3. Linting
ruff check src/

# 4. API health check
curl -sf http://localhost:8080/health

# 5. Build verification
docker build -t feature:test .
```
```

---

*Template version: 1.0*
*Last updated: 2026-01-19*
