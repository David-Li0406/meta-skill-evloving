# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **MCP (Model Context Protocol) server** that provides OpenShift cluster health monitoring and AI Ops integration. It exposes cluster health data, incident management, and ML-powered anomaly detection through a standardized MCP interface for OpenShift Lightspeed integration.

**Tech Stack**: Go 1.24+, Kubernetes client-go, MCP Go SDK (official)

## Core Architecture

### Transport Layer (HTTP/SSE Only)
- **stdio transport is DEPRECATED** as of 2025-12-17 (see `docs/adrs/004-transport-layer-strategy.md`)
- Only HTTP/SSE transport is supported for OpenShift Lightspeed integration
- Default transport: `http` (configured via `MCP_TRANSPORT` env var)
- MCP SSE handler at root endpoint using `mcp.NewSSEHandler()` from official Go SDK

### Project Structure
```
cmd/mcp-server/          # Main entry point (main.go)
internal/
  server/                # HTTP server and MCP protocol handling
    config.go            # Environment-based configuration
    server.go            # Core MCP server with tool/resource registration
  tools/                 # MCP tool implementations (6 tools)
  resources/             # MCP resource implementations (3 resources)
pkg/
  clients/               # External API clients (K8s, Coordination Engine, KServe)
    kubernetes.go        # K8s client with connection pooling
    coordination_engine.go
    kserve.go
  cache/                 # In-memory cache with TTL (default: 30s)
    memory_cache.go
```

### MCP Tools vs Resources
- **Tools** (internal/tools/): Active operations invoked by clients (6 total)
  - `get-cluster-health` - Cluster health snapshot
  - `list-pods` - Pod listing with filtering
  - `list-incidents` - Active incidents (requires Coordination Engine)
  - `trigger-remediation` - Automated remediation
  - `analyze-anomalies` - ML anomaly detection (requires KServe)
  - `get-model-status` - KServe model health

- **Resources** (internal/resources/): Passive data access with caching (3 total)
  - `cluster://health` - Cluster health (10s cache)
  - `cluster://nodes` - Node info (30s cache)
  - `cluster://incidents` - Active incidents (5s cache)

### Tool/Resource Registration Pattern
All tools and resources follow this interface pattern:
```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]interface{}
    Execute(ctx context.Context, args map[string]interface{}) (interface{}, error)
}
```

Registration happens in `internal/server/server.go:registerTools()` and `registerResources()`. Each tool/resource is:
1. Instantiated with required clients (K8s, CE, KServe)
2. Stored in internal registry map
3. Registered with MCP SDK via `mcp.AddTool()`

### Kubernetes Client Architecture
- Lives in `pkg/clients/kubernetes.go`
- **Connection priority**: in-cluster config → provided path → $KUBECONFIG → ~/.kube/config
- Configured with QPS limiting (50) and burst (100) for rate limiting
- Health check on startup validates cluster connectivity
- Used by all tools/resources for cluster operations

### Caching Strategy
- In-memory cache with TTL (pkg/cache/memory_cache.go)
- Default TTL: 30 seconds (configurable via `CACHE_TTL`)
- Background cleanup runs every minute
- Tools choose caching based on data volatility:
  - `get-cluster-health`: cached (data changes slowly)
  - `list-pods`: NOT cached (pod status changes frequently)
- Statistics endpoint at `/cache/stats` for monitoring

### Optional Integrations (Feature Flags)
All disabled by default, enabled via environment variables:
- **Coordination Engine**: `ENABLE_COORDINATION_ENGINE=true` + `COORDINATION_ENGINE_URL`
- **KServe**: `ENABLE_KSERVE=true` + `KSERVE_NAMESPACE`
- **Prometheus**: `ENABLE_PROMETHEUS=true` + `PROMETHEUS_URL` (Phase 3 - not implemented)

## Development Commands

### Build and Run
```bash
# Local development build
make build                    # Output: bin/mcp-server

# Production build (optimized, stripped)
make build-prod              # CGO_ENABLED=0, -ldflags="-s -w"

# Run locally (defaults to HTTP transport)
make run                     # Equivalent to: go run ./cmd/mcp-server
MCP_TRANSPORT=http ./bin/mcp-server

# Run with specific kubeconfig
KUBECONFIG=/path/to/kubeconfig ./bin/mcp-server
```

### Testing
```bash
# Run all unit tests
make test                    # Runs: go test -v ./...

# Run with coverage report
make test-coverage           # Outputs: coverage/coverage.html

# Single test execution
go test -v ./internal/tools -run TestClusterHealthTool
go test -v ./pkg/clients -run TestK8sClient
```

### Linting and Security
```bash
# Run linters (requires golangci-lint)
make lint

# Security scanning (requires gosec)
make security-gosec

# Container image security scan (requires trivy)
make security-scan           # Scans built Docker image
```

### Docker
```bash
# Build production image
make docker-build            # Uses Dockerfile (UBI 9 Micro base)

# Build debug image (includes shell)
make docker-build-debug      # Uses Dockerfile.debug

# Run container locally
make docker-run              # Mounts ~/.kube for K8s access

# Multi-arch build (amd64, arm64)
make docker-buildx
```

### Helm
```bash
# Lint Helm chart
make helm-lint

# Install to cluster
make helm-install            # Namespace: cluster-health-mcp-dev

# Upgrade deployment
make helm-upgrade

# Uninstall
make helm-uninstall
```

## Testing the MCP Server

### HTTP Endpoints (for manual testing)
```bash
# Health check
curl http://localhost:8080/health

# Server capabilities (MCP spec compliant)
curl http://localhost:8080/mcp

# Server info (detailed)
curl http://localhost:8080/mcp/info

# List available tools
curl http://localhost:8080/mcp/tools

# List available resources
curl http://localhost:8080/mcp/resources

# Cache statistics
curl http://localhost:8080/cache/stats
```

### Session Management (REST API)
The server provides session management endpoints for REST API clients. Sessions have a 30-minute TTL and are automatically cleaned up.

```bash
# Step 1: Create a session
curl -X POST http://localhost:8080/mcp/session \
  -H 'Content-Type: application/json' \
  -d '{"client": "my-client"}'
# Returns: { "session_id": "abc123...", "expires_at": "...", ... }

# Step 2: Execute a tool using session ID (query parameter)
curl -X POST "http://localhost:8080/mcp/tools/get-cluster-health/call?sessionid=abc123..." \
  -H 'Content-Type: application/json' \
  -d '{}'

# Or use X-MCP-Session-ID header instead
curl -X POST http://localhost:8080/mcp/tools/list-pods/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: abc123...' \
  -d '{"namespace": "default"}'

# Get session info
curl "http://localhost:8080/mcp/session?sessionid=abc123..."
# Or: curl http://localhost:8080/mcp/session/abc123...

# Get session statistics
curl http://localhost:8080/mcp/sessions/stats

# Delete a session
curl -X DELETE http://localhost:8080/mcp/session/abc123...
```

### REST API Endpoints Summary
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/ready` | GET | No | Readiness check |
| `/mcp` | GET | No | Server capabilities (MCP spec) |
| `/mcp/info` | GET | No | Server metadata |
| `/mcp/tools` | GET | No | List available tools |
| `/mcp/resources` | GET | No | List available resources |
| `/mcp/session` | POST | No | Create new session |
| `/mcp/session` | GET | Session | Get session info |
| `/mcp/session/{id}` | GET | No | Get session by ID |
| `/mcp/session/{id}` | DELETE | No | Delete session |
| `/mcp/sessions/stats` | GET | No | Session statistics |
| `/mcp/tools/{tool}/call` | POST | Session | Execute a tool |
| `/mcp/resources/{uri}/read` | POST/GET | Session | Read a resource |
| `/cache/stats` | GET | No | Cache statistics |

### MCP Protocol Testing (SSE)
The server also supports SSE (Server-Sent Events) at the root endpoint (`/`) for native MCP protocol communication. This is handled by `mcp.NewSSEHandler()` from the official Go SDK.

For SSE clients:
1. GET `/` - Establishes SSE connection, server sends `endpoint` event with session ID
2. POST `/?sessionid=...` - Send MCP messages to established session

## Configuration

### Environment Variables (see internal/server/config.go)
| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `MCP_TRANSPORT` | `http` | No | Transport mode (only 'http' supported) |
| `MCP_HTTP_HOST` | `0.0.0.0` | No | HTTP server bind address |
| `MCP_HTTP_PORT` | `8080` | No | HTTP server port |
| `CACHE_TTL` | `30s` | No | Cache expiration time |
| `REQUEST_TIMEOUT` | `10s` | No | HTTP client timeout |
| `ENABLE_COORDINATION_ENGINE` | `false` | No | Enable Coordination Engine integration |
| `COORDINATION_ENGINE_URL` | `http://coordination-engine:8080` | If CE enabled | CE endpoint |
| `ENABLE_KSERVE` | `false` | No | Enable KServe integration |
| `KSERVE_NAMESPACE` | `self-healing-platform` | If KServe enabled | KServe models namespace |
| `KSERVE_PREDICTOR_PORT` | `8080` | No | KServe predictor port (8080 for RawDeployment, 80 for Serverless) |
| `ENABLE_PROMETHEUS` | `false` | No | Enable Prometheus integration (Phase 3) |
| `PROMETHEUS_URL` | `https://prometheus-k8s.openshift-monitoring.svc:9091` | If Prom enabled | Prometheus endpoint |

### Kubernetes RBAC Requirements
The server requires a ServiceAccount with ClusterRole permissions:
- **Nodes**: `get`, `list`, `watch`
- **Pods**: `get`, `list`, `watch`
- **Namespaces**: `get`, `list`
- **InferenceServices** (KServe): `get`, `list` (if KServe enabled)

See `charts/openshift-cluster-health-mcp/templates/clusterrole.yaml` for full RBAC configuration.

## Important Implementation Details

### Adding New Tools
1. Create tool file in `internal/tools/` (e.g., `my_tool.go`)
2. Implement the Tool interface (Name, Description, InputSchema, Execute)
3. Register in `internal/server/server.go:registerTools()`
4. Add to type switch in `handleListTools()` for HTTP endpoint support
5. Add integration tests in `internal/tools/*_test.go`

### Adding New Resources
1. Create resource file in `internal/resources/` (e.g., `my_resource.go`)
2. Implement URI(), Name(), Description(), MimeType(), Read() methods
3. Register in `internal/server/server.go:registerResources()`
4. Add to type switch in `handleListResources()`
5. Consider caching strategy (cache TTL based on data volatility)

### Error Handling Pattern
- Client errors: Return errors from Execute(), MCP SDK converts to error response
- Kubernetes API errors: Use retry logic from `pkg/clients/retry.go`
- Context cancellation: Always respect `ctx.Done()` in long operations
- Logging: Use Go's log package (structured logging planned for Phase 3)

### Cache Usage Pattern
```go
// Check cache first
cacheKey := "my-data-key"
if cached, ok := cache.Get(cacheKey); ok {
    return cached, nil
}

// Fetch from source
data, err := fetchData()
if err != nil {
    return nil, err
}

// Store in cache
cache.Set(cacheKey, data)
return data, nil
```

### ADRs (Architecture Decision Records)
Critical ADRs to understand before making changes:
- **ADR-002**: Official MCP Go SDK adoption (why we use github.com/modelcontextprotocol/go-sdk)
- **ADR-004**: Transport layer strategy (why HTTP/SSE only, stdio deprecated)
- **ADR-005**: Stateless design (why no persistent storage)
- **ADR-006**: Integration architecture (optional Coordination Engine/KServe)

See `docs/adrs/` for all architectural decisions.

## Common Pitfalls

1. **stdio transport is deprecated**: Don't implement or fix stdio-related code. Only HTTP/SSE is supported.

2. **Cache misuse**: Don't cache data that changes frequently (like pod status). Only cache relatively stable data (cluster health, node info).

3. **Tool vs Resource confusion**:
   - Use Tools for active operations that take parameters
   - Use Resources for passive data access that clients subscribe to

4. **Kubernetes client creation**: Always use in-cluster config in production (automatically detected). Don't hardcode kubeconfig paths.

5. **Integration feature flags**: All integrations (CE, KServe, Prometheus) are disabled by default. Don't assume they're available in tests.

6. **MCP SDK integration**: All tool registration uses the official MCP Go SDK (`mcp.AddTool()`). Don't create custom MCP protocol handlers.

7. **OpenShift compatibility**: Use SecurityContext with `runAsNonRoot: true`, don't set `runAsUser` (let OpenShift assign).

## Branch Protection

All main and release branches are protected to ensure code quality and prevent unauthorized changes. See [`docs/BRANCH_PROTECTION.md`](docs/BRANCH_PROTECTION.md) for complete details and [`docs/adrs/014-branch-protection-strategy.md`](docs/adrs/014-branch-protection-strategy.md) for architectural decisions.

### Protected Branches
- **`main`** - Primary development branch (1 required approval)
- **`release-4.18`**, **`release-4.19`**, **`release-4.20`** - Release branches (2 required approvals)

### Making Changes
- **Direct pushes are blocked** - All changes must go through Pull Requests
- **Required CI checks must pass**: Test, Lint, Build, Security, Helm, Container Build
- **Code owner approval required** - See `.github/CODEOWNERS` for ownership mapping
- **All conversations must be resolved** before merging

### Contribution Workflow
1. Fork the repository and create a feature branch
2. Make changes and run local validation: `make test && make lint && make build`
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/) format
4. Push to your fork and open a Pull Request
5. Fill out the [PR template](.github/PULL_REQUEST_TEMPLATE.md)
6. Wait for CI checks to pass and code owner review
7. Address feedback and resolve conversations
8. Merge once approved and all checks pass

See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for detailed contribution guidelines.
