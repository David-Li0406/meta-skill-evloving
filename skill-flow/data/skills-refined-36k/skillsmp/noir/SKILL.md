---
name: noir
description: Run OWASP Noir for attack surface analysis and API endpoint discovery. Use when mapping API endpoints, finding shadow APIs, discovering hidden routes, or analyzing attack surface across multiple frameworks.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# OWASP Noir - API & Attack Surface Scanner

## When to Use Noir

**Ideal scenarios:**

- API endpoint discovery and inventory
- Attack surface mapping
- Shadow API detection
- Pre-pentest reconnaissance
- API security assessment preparation
- Microservices endpoint cataloging
- REST/GraphQL/WebSocket endpoint discovery
- Framework-specific route analysis

**Complements other tools:**

- Use before manual penetration testing for endpoint discovery
- Combine with vulnerability scanners (Semgrep, CodeQL) for deeper analysis
- Use with API testing tools (Burp, ZAP) for complete coverage
- Pair with SARIF Issue Reporter for findings analysis

## When NOT to Use

Do NOT use this skill for:

- Vulnerability scanning (use Semgrep, CodeQL, or DAST tools)
- Dependency scanning (use OSV-Scanner or Depscan)
- Secrets detection (use Gitleaks)
- IaC analysis (use KICS)
- Runtime API discovery (use API gateways or proxies)

## Installation

```bash
# Homebrew (macOS/Linux)
brew install noir

# Download binary (Linux)
wget https://github.com/owasp-noir/noir/releases/latest/download/noir-linux-x86_64
chmod +x noir-linux-x86_64
sudo mv noir-linux-x86_64 /usr/local/bin/noir

# Download binary (macOS)
wget https://github.com/owasp-noir/noir/releases/latest/download/noir-macos-arm64
chmod +x noir-macos-arm64
sudo mv noir-macos-arm64 /usr/local/bin/noir

# Build from source (requires Crystal)
git clone https://github.com/owasp-noir/noir.git
cd noir
shards install
shards build --release --no-debug
sudo cp bin/noir /usr/local/bin/

# Docker
docker pull ghcr.io/owasp-noir/noir:latest

# Verify
noir --version
```

## Core Workflow

### 1. Quick Scan

```bash
# Scan current directory
noir

# Scan specific path
noir -b /path/to/source

# Verbose output
noir -b /path/to/source -v

# Quiet mode
noir -b /path/to/source -q
```

### 2. Output Formats

```bash
# JSON output (default)
noir -b /path/to/source -o endpoints.json

# YAML output
noir -b /path/to/source --format yaml -o endpoints.yaml

# SARIF output
noir -b /path/to/source --format sarif -o results.sarif

# OpenAPI Specification
noir -b /path/to/source --format oas3 -o openapi.json

# HAR (HTTP Archive)
noir -b /path/to/source --format har -o endpoints.har

# Markdown Report
noir -b /path/to/source --format markdown -o report.md

# Plain text
noir -b /path/to/source --format plain
```

### 3. Technology-Specific Scanning

```bash
# Specify technologies to scan
noir -b /path/to/source -T express,django,spring

# Exclude specific technologies
noir -b /path/to/source --exclude fastapi

# List supported technologies
noir --list-techs
```

### 4. Advanced Options

```bash
# No color output (for CI)
noir -b /path/to/source --no-color

# Include technical details
noir -b /path/to/source --include-path

# Send results to URL
noir -b /path/to/source --send-req https://api.example.com/endpoints

# Proxy through Burp/ZAP
noir -b /path/to/source --send-proxy http://127.0.0.1:8080
```

## Supported Frameworks

### Web Frameworks

| Language | Frameworks |
|----------|-----------|
| **JavaScript/TypeScript** | Express.js, NestJS, Koa, Fastify, Hapi |
| **Python** | Django, Flask, FastAPI, Tornado, Bottle |
| **Java** | Spring Boot, JAX-RS, Micronaut, Quarkus |
| **Ruby** | Rails, Sinatra, Grape |
| **Go** | Gin, Echo, Fiber, Chi, Gorilla Mux |
| **PHP** | Laravel, Symfony, Slim, CodeIgniter |
| **C#** | ASP.NET Core, Nancy |
| **Rust** | Actix, Rocket, Axum, Warp |
| **Kotlin** | Ktor, Spring Boot |

### API Types

- REST APIs
- GraphQL endpoints
- WebSocket routes
- gRPC services (limited)
- OpenAPI/Swagger definitions

## Output Analysis

### SARIF Format

```bash
# Generate SARIF for integration
noir -b /path/to/source \
  --format sarif \
  -o endpoints.sarif \
  --no-color

# SARIF structure includes:
# - Each endpoint as a "result"
# - HTTP methods (GET, POST, PUT, DELETE, etc.)
# - Route paths
# - Parameters
# - Source file location
```

### JSON Output Structure

```json
{
  "endpoints": [
    {
      "method": "POST",
      "url": "/api/users",
      "params": ["username", "email", "password"],
      "protocol": "http",
      "details": {
        "file": "src/routes/users.js",
        "line": 42,
        "code_type": "javascript"
      }
    }
  ]
}
```

### OpenAPI Output

```bash
# Generate OpenAPI spec from discovered endpoints
noir -b /path/to/source --format oas3 -o openapi.json

# Use with API testing tools
swagger-cli validate openapi.json
openapi-generator generate -i openapi.json -g postman-collection
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Noir API Discovery

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  noir:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install Noir
        run: |
          wget -q https://github.com/owasp-noir/noir/releases/latest/download/noir-linux-x86_64
          chmod +x noir-linux-x86_64
          sudo mv noir-linux-x86_64 /usr/local/bin/noir

      - name: Run Noir
        run: |
          noir -b ${{ github.workspace }} \
            --format sarif \
            -o noir-results.sarif \
            --no-color

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: noir-results.sarif
          category: noir-api-discovery

      - name: Generate OpenAPI
        run: |
          noir -b ${{ github.workspace }} \
            --format oas3 \
            -o openapi.json

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: noir-results
          path: |
            noir-results.sarif
            openapi.json
```

## Common Use Cases

### 1. Pre-Pentest Reconnaissance

```bash
# Discover all endpoints
noir -b /app/source \
  --format json \
  -o endpoints.json \
  -v

# Generate attack surface report
noir -b /app/source \
  --format markdown \
  -o attack-surface.md

# Create OpenAPI for tools
noir -b /app/source \
  --format oas3 \
  -o openapi.json
```

### 2. Microservices Inventory

```bash
# Scan multiple services
for service in services/*/; do
  noir -b "$service" \
    --format json \
    -o "inventory/$(basename $service).json"
done

# Combine results
jq -s 'add' inventory/*.json > complete-inventory.json
```

### 3. Shadow API Detection

```bash
# Scan codebase
noir -b /path/to/source -o discovered-endpoints.json

# Compare with documented API
diff <(jq -r '.endpoints[].url' discovered-endpoints.json | sort) \
     <(jq -r '.paths | keys[]' openapi-spec.json | sort)

# Undocumented endpoints are "shadow APIs"
```

### 4. Framework Migration Analysis

```bash
# Before migration - discover all routes
noir -b /old/app -T express -o old-endpoints.json

# After migration - verify parity
noir -b /new/app -T fastify -o new-endpoints.json

# Compare
diff <(jq -r '.endpoints[].url' old-endpoints.json | sort) \
     <(jq -r '.endpoints[].url' new-endpoints.json | sort)
```

### 5. Baldwin.sh Integration

```bash
# Match baldwin.sh justfile pattern
noir \
  -b /workspace/src \
  --format sarif \
  -o /workspace/output/sarif/noir.sarif \
  -T \
  --no-color
```

## Advanced Features

### Technology Detection

```bash
# Auto-detect technologies
noir -b /path/to/source --list-techs

# Show detected frameworks
noir -b /path/to/source -v | grep "Detected"
```

### Filtering Results

```bash
# Only GET endpoints
jq '.endpoints[] | select(.method == "GET")' endpoints.json

# Only authenticated endpoints (heuristic)
jq '.endpoints[] | select(.url | contains("auth") or contains("login"))' endpoints.json

# High-risk endpoints
jq '.endpoints[] | select(.method == "DELETE" or .method == "PUT")' endpoints.json
```

### Proxy Integration

```bash
# Send discovered endpoints to Burp Suite
noir -b /path/to/source \
  --send-proxy http://127.0.0.1:8080 \
  --send-req http://target.example.com

# Creates Burp site map automatically
```

## Security Analysis Workflow

### Step 1: Discover

```bash
noir -b /app/source --format json -o endpoints.json
```

### Step 2: Categorize

```bash
# Extract by risk level
jq '.endpoints[] | select(.method == "DELETE")' endpoints.json > high-risk.json
jq '.endpoints[] | select(.params | length > 0)' endpoints.json > with-params.json
jq '.endpoints[] | select(.url | test("/admin|/api/internal"))' endpoints.json > privileged.json
```

### Step 3: Test

```bash
# Generate test scripts
jq -r '.endpoints[] | "curl -X \(.method) http://target.com\(.url)"' endpoints.json > test-requests.sh

# Or convert to OpenAPI and use Postman/Newman
noir -b /app/source --format oas3 -o openapi.json
```

### Step 4: Report

```bash
# Create comprehensive report
noir -b /app/source --format markdown -o report.md

# Add SARIF for tracking
noir -b /app/source --format sarif -o findings.sarif
```

## Performance Considerations

```bash
# Large codebases - use specific technology
noir -b /large/repo -T express -q

# Exclude unnecessary paths
noir -b /repo --exclude "node_modules,vendor,test"

# Minimal output for CI
noir -b /repo -q --format sarif -o results.sarif
```

## Limitations

- **Static analysis only**: Can't discover runtime-generated routes
- **Framework coverage**: Limited to supported frameworks
- **Dynamic routing**: May miss programmatically generated endpoints
- **Annotations required**: Some frameworks need proper route decorators
- **No validation**: Doesn't verify if endpoints are accessible
- **No authentication**: Doesn't detect auth requirements

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "Noir found all endpoints = complete coverage" | Dynamic routes, runtime-generated endpoints, and some frameworks may be missed |
| "Skip endpoint discovery, review code manually" | Manual review misses endpoints; automated discovery is faster and more complete |
| "Only scan main application, skip microservices" | Microservices often expose attack surface; comprehensive scan needed |
| "OpenAPI docs are enough" | Documentation often lags code; Noir finds actual implemented endpoints |
| "Don't need SARIF output" | SARIF enables integration with security workflows and issue tracking |

## References

- Repository: <https://github.com/owasp-noir/noir>
- Documentation: <https://owasp-noir.github.io/noir/>
- OWASP Project: <https://owasp.org/www-project-noir/>
- Supported Technologies: <https://owasp-noir.github.io/noir/techs/>
- SARIF Output: <https://owasp-noir.github.io/noir/usage/output_formats/sarif/>

