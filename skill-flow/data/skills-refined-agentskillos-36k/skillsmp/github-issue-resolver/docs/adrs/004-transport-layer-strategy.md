# ADR-004: Transport Layer Strategy (HTTP/SSE for OpenShift Lightspeed)

## Status

**SUPERSEDED** - 2025-12-17

**Original Decision (2025-12-09)**: Dual transport (HTTP/SSE + stdio)
**Updated Decision (2025-12-17)**: HTTP/SSE only, stdio DEPRECATED

## Deprecation Notice

**stdio transport is DEPRECATED as of 2025-12-17.**

**Rationale:**
- Primary use case is **OpenShift Lightspeed integration** via HTTP/SSE
- Local development can use HTTP transport (no need for stdio)
- Reduces codebase complexity and maintenance burden
- stdio was never implemented beyond stub (see server.go:322-335)

**Migration Path:**
- All deployments use HTTP/SSE transport (already the default)
- Local development: Use `MCP_TRANSPORT=http` and test with HTTP endpoints
- Claude Desktop testing: Not required for OpenShift Lightspeed use case

## Context

The Model Context Protocol (MCP) supports multiple transport mechanisms for client-server communication. The OpenShift Cluster Health MCP Server needs to support different MCP clients with varying transport requirements:

1. **OpenShift Lightspeed**: Enterprise AI assistant integrated with OpenShift Console
2. **Claude Desktop**: Local desktop application for development/testing
3. **VS Code / IDEs**: Developer tools with MCP support
4. **Future Clients**: Emerging MCP-compatible tools

### MCP Transport Options

MCP specification defines several transport protocols:

| Transport | Protocol | Use Case | Pros | Cons |
|-----------|----------|----------|------|------|
| **stdio** | Standard input/output pipes | Local process spawning | Simple, secure, no network | Client must spawn server |
| **HTTP/SSE** | HTTP with Server-Sent Events | Web-based clients | Standard HTTP, firewall-friendly | One-way streaming only |
| **StreamableHTTP** | HTTP with bidirectional streaming | Enterprise deployments | Full-duplex, stateful sessions | More complex than stdio |
| **WebSocket** | WebSocket protocol | Real-time web apps | Full-duplex, widely supported | Not in official MCP spec |

### OpenShift Lightspeed Requirements

Based on parent platform **ADR-016** (OpenShift Lightspeed OLSConfig Integration):

- **OLSConfig Format**: Requires HTTP endpoint URL, not stdio process
- **Transport**: StreamableHTTP (HTTP-based bidirectional communication)
- **Discovery**: Root endpoint (`/`) must return server capabilities JSON
- **Session Management**: `mcp-session-id` header for session tracking
- **Authentication**: Bearer token authentication via Kubernetes ServiceAccount

**Example OLSConfig**:
```yaml
apiVersion: ols.openshift.io/v1alpha1
kind: OLSConfig
spec:
  llm:
    providers:
      - name: openshift-cluster-health
        type: mcp
        url: http://cluster-health-mcp.self-healing-platform.svc:8080
        credentialsSecretRef:
          name: mcp-server-token
```

### Local Development Requirements

For local testing with Claude Desktop and IDE integrations:

- **Process Spawning**: Client spawns MCP server as subprocess
- **Transport**: stdio (standard input/output)
- **Configuration**: MCP client config file (JSON)
- **No Network**: Communication via pipes, no HTTP overhead

**Example Claude Desktop Config**:
```json
{
  "mcpServers": {
    "openshift-cluster-health": {
      "command": "./mcp-server",
      "args": ["--transport=stdio"],
      "env": {
        "KUBECONFIG": "/path/to/kubeconfig"
      }
    }
  }
}
```

## Decision

We will implement **HTTP/SSE transport only** in the MCP server:

1. **HTTP/SSE** (Server-Sent Events): Primary and ONLY transport for OpenShift Lightspeed
2. **stdio** (process pipes): ~~Secondary transport for local development~~ **DEPRECATED** - Not needed for OpenShift use case

### Transport Selection Strategy

```go
// Environment variable determines transport mode
// DEFAULT: http (for OpenShift Lightspeed)
transport := os.Getenv("MCP_TRANSPORT")

switch transport {
case "http":
    // HTTP/SSE for OpenShift Lightspeed (DEFAULT)
    server.StartHTTPTransport(":8080")
case "stdio":
    // DEPRECATED: stdio transport is no longer supported
    log.Fatal("stdio transport is DEPRECATED - use http transport")
default:
    // Default to HTTP (changed from stdio as of 2025-12-17)
    server.StartHTTPTransport(":8080")
}
```

### Key Design Principles (Updated 2025-12-17)

1. **Default to HTTP/SSE**: OpenShift Lightspeed primary use case
2. **Environment-based configuration**: `MCP_TRANSPORT=http` (default)
3. **Same business logic**: Transport layer is abstraction only
4. **Single binary**: One executable, HTTP/SSE transport only
5. **stdio DEPRECATED**: Removed to reduce complexity

## Rationale

### Why HTTP/SSE Only? (Updated 2025-12-17)

1. **OpenShift Lightspeed Requirement**: OLSConfig mandates HTTP endpoint (primary use case)
2. **Simplified Development**: HTTP testing with curl/Postman works for local development
3. **Reduced Complexity**: Single transport = easier maintenance and testing
4. **Production Focus**: stdio was never implemented (stub only), no value in completing it

### Why NOT stdio?

1. ❌ **Not needed for Lightspeed**: OpenShift Lightspeed uses HTTP/SSE exclusively
2. ❌ **Not implemented**: Only stub code exists (server.go:322-335)
3. ❌ **Local dev covered**: Developers can test with HTTP locally
4. ❌ **Maintenance burden**: Dual transport adds complexity without benefit

### Why HTTP/SSE (Server-Sent Events)?

1. **Bidirectional**: SSE supports server-initiated messages
2. **Stateful Sessions**: Maintains context across requests via `mcp-session-id` header
3. **Specification Compliance**: Part of MCP transport spec
4. **OpenShift Lightspeed**: Required by OLSConfig integration
5. **Production Ready**: Official `mcp.NewSSEHandler()` from go-sdk (line 257 in server.go)

## Alternatives Considered

### ✅ HTTP/SSE Only (CHOSEN - Updated 2025-12-17)

**Pros**:
- ✅ Simpler codebase (single transport)
- ✅ Perfect for enterprise deployment (OpenShift Lightspeed)
- ✅ Fully implemented and working (server.go:249-320)
- ✅ Local development works fine with HTTP

**Cons**:
- ⚠️ Deviates from MCP reference transport (stdio)
- ⚠️ Requires HTTP server for local testing

**Verdict**: **ACCEPTED** - Primary use case is OpenShift Lightspeed via HTTP/SSE

### ❌ stdio-Only

**Pros**:
- MCP canonical transport
- Simpler implementation
- Best security (no network)

**Cons**:
- ❌ **Cannot integrate with OpenShift Lightspeed OLSConfig**
- ❌ Requires client to spawn server process
- ❌ Not suitable for shared deployment

**Verdict**: Rejected - blocks primary use case (OpenShift Lightspeed)

### ❌ Dual Transport (Original ADR-004 Decision)

**Pros**:
- Support both OpenShift Lightspeed (HTTP) and Claude Desktop (stdio)
- Maximum flexibility

**Cons**:
- ❌ **stdio never implemented** (only stub exists)
- ❌ Added complexity without value
- ❌ Local HTTP testing sufficient for development

**Verdict**: Rejected (2025-12-17) - stdio provides no value for our use case

### WebSocket

**Pros**:
- Widely supported protocol
- Full-duplex communication
- Good browser support

**Cons**:
- ❌ Not in official MCP specification
- ❌ More complex than StreamableHTTP
- ❌ Not required by OpenShift Lightspeed

**Verdict**: Rejected - not standard MCP transport

### Separate Binaries (stdio vs HTTP)

**Pros**:
- Smaller binaries for each use case
- No conditional logic

**Cons**:
- ❌ Operational complexity (two binaries to maintain)
- ❌ Configuration confusion
- ❌ Duplicate code

**Verdict**: Rejected - unnecessary complexity

## Implementation Details

### HTTP Transport Implementation

```go
// internal/server/transport_http.go
package server

import (
    "net/http"
    "github.com/modelcontextprotocol/go-sdk/server"
)

func (s *MCPServer) StartHTTPTransport(addr string) error {
    http.HandleFunc("/", s.handleMCPRoot)           // Discovery endpoint
    http.HandleFunc("/message", s.handleMCPMessage) // MCP message endpoint
    http.HandleFunc("/health", s.handleHealth)      // K8s health probe

    log.Info("Starting HTTP transport", "addr", addr)
    return http.ListenAndServe(addr, nil)
}

func (s *MCPServer) handleMCPMessage(w http.ResponseWriter, r *http.Request) {
    // Extract session ID from header
    sessionID := r.Header.Get("mcp-session-id")

    // Parse MCP message from request body
    var msg server.MCPMessage
    if err := json.NewDecoder(r.Body).Decode(&msg); err != nil {
        http.Error(w, "Invalid MCP message", http.StatusBadRequest)
        return
    }

    // Process message through MCP SDK
    response, err := s.mcpServer.HandleMessage(r.Context(), sessionID, &msg)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Return MCP response as JSON
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

### stdio Transport Implementation

```go
// internal/server/transport_stdio.go
package server

import (
    "bufio"
    "os"
    "github.com/modelcontextprotocol/go-sdk/server"
)

func (s *MCPServer) StartStdioTransport() error {
    log.Info("Starting stdio transport")

    scanner := bufio.NewScanner(os.Stdin)
    writer := bufio.NewWriter(os.Stdout)

    for scanner.Scan() {
        line := scanner.Text()

        // Parse MCP message from stdin
        var msg server.MCPMessage
        if err := json.Unmarshal([]byte(line), &msg); err != nil {
            log.Error("Invalid MCP message", "error", err)
            continue
        }

        // Process message through MCP SDK
        response, err := s.mcpServer.HandleMessage(context.Background(), "", &msg)
        if err != nil {
            log.Error("Message handling error", "error", err)
            continue
        }

        // Write response to stdout
        responseBytes, _ := json.Marshal(response)
        writer.WriteString(string(responseBytes) + "\n")
        writer.Flush()
    }

    return scanner.Err()
}
```

### Transport Selection Logic

```go
// cmd/mcp-server/main.go
package main

import (
    "os"
    "openshift-cluster-health-mcp/internal/server"
)

func main() {
    mcpServer := server.NewMCPServer()

    // Environment-based transport selection
    transport := os.Getenv("MCP_TRANSPORT")
    if transport == "" {
        transport = "stdio" // Default
    }

    switch transport {
    case "http":
        port := os.Getenv("MCP_HTTP_PORT")
        if port == "" {
            port = "8080"
        }
        if err := mcpServer.StartHTTPTransport(":" + port); err != nil {
            log.Fatal("HTTP transport failed", "error", err)
        }

    case "stdio":
        if err := mcpServer.StartStdioTransport(); err != nil {
            log.Fatal("stdio transport failed", "error", err)
        }

    default:
        log.Fatal("Invalid transport", "transport", transport)
    }
}
```

## Deployment Configurations

### OpenShift Lightspeed Deployment (HTTP)

```yaml
# charts/openshift-cluster-health-mcp/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-health-mcp
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: mcp-server
        image: quay.io/openshift-aiops/cluster-health-mcp:0.1.0
        env:
        - name: MCP_TRANSPORT
          value: "http"
        - name: MCP_HTTP_PORT
          value: "8080"
        ports:
        - containerPort: 8080
          name: http
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
```

### Local Development (HTTP - Updated 2025-12-17)

```bash
# HTTP is now the default (changed from stdio)
./mcp-server --kubeconfig ~/.kube/config

# Or explicitly set HTTP
MCP_TRANSPORT=http ./mcp-server

# Test with curl
curl -X POST http://localhost:8080/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### ~~Claude Desktop Configuration~~ (DEPRECATED)

**stdio transport is no longer supported.**
Local development uses HTTP transport instead.

## Session Management

### HTTP Session Tracking

```go
// internal/server/session.go
type SessionManager struct {
    sessions map[string]*Session
    mu       sync.RWMutex
}

type Session struct {
    ID        string
    CreatedAt time.Time
    LastSeen  time.Time
    Context   map[string]interface{}
}

func (sm *SessionManager) GetOrCreate(sessionID string) *Session {
    sm.mu.Lock()
    defer sm.mu.Unlock()

    if session, exists := sm.sessions[sessionID]; exists {
        session.LastSeen = time.Now()
        return session
    }

    session := &Session{
        ID:        sessionID,
        CreatedAt: time.Now(),
        LastSeen:  time.Now(),
        Context:   make(map[string]interface{}),
    }
    sm.sessions[sessionID] = session
    return session
}

// Cleanup old sessions (run periodically)
func (sm *SessionManager) CleanupExpired(maxAge time.Duration) {
    sm.mu.Lock()
    defer sm.mu.Unlock()

    cutoff := time.Now().Add(-maxAge)
    for id, session := range sm.sessions {
        if session.LastSeen.Before(cutoff) {
            delete(sm.sessions, id)
        }
    }
}
```

### stdio Session Handling

stdio transport is inherently single-session (one process = one client):

```go
// No session management needed - process lifecycle = session lifecycle
func (s *MCPServer) StartStdioTransport() error {
    // Single implicit session for this process
    sessionContext := make(map[string]interface{})

    // Process messages until stdin closes (client disconnects)
    for scanner.Scan() {
        // ... process messages with shared sessionContext
    }
}
```

## Performance Considerations

### HTTP Transport

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Request Latency** | <50ms (p95) | HTTP request to response |
| **Session Overhead** | <1MB per session | Memory per active session |
| **Concurrent Sessions** | 20+ | Simultaneous Lightspeed users |
| **Throughput** | 200+ req/min | Tool invocations per minute |

### stdio Transport

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Message Latency** | <10ms (p95) | stdin to stdout |
| **Memory Footprint** | <30MB | Single process memory |
| **Startup Time** | <500ms | Process spawn to ready |

## Security Implications

### HTTP Transport Security

1. **Authentication**: Kubernetes ServiceAccount bearer tokens
2. **Authorization**: RBAC-based access control
3. **Network Policy**: Restrict to OpenShift Lightspeed namespace
4. **TLS**: Optional TLS termination via OpenShift Route

```yaml
# NetworkPolicy restricting access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cluster-health-mcp-ingress
spec:
  podSelector:
    matchLabels:
      app: cluster-health-mcp
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: openshift-lightspeed
    ports:
    - protocol: TCP
      port: 8080
```

### stdio Transport Security

1. **Process Isolation**: Each client spawns isolated process
2. **No Network**: Communication via local pipes only
3. **File System Permissions**: Relies on OS file permissions
4. **KUBECONFIG**: User's own Kubernetes credentials

## Testing Strategy

### HTTP Transport Tests

```go
// test/integration/http_transport_test.go
func TestHTTPTransport(t *testing.T) {
    server := setupTestServer()
    go server.StartHTTPTransport(":8888")

    // Test discovery endpoint
    resp, _ := http.Get("http://localhost:8888/")
    assert.Equal(t, 200, resp.StatusCode)

    // Test MCP message
    msg := mcpMessage{Method: "tools/list"}
    resp, _ := http.Post("http://localhost:8888/message",
        "application/json", toJSON(msg))
    assert.Equal(t, 200, resp.StatusCode)
}
```

### stdio Transport Tests

```go
// test/integration/stdio_transport_test.go
func TestStdioTransport(t *testing.T) {
    cmd := exec.Command("./mcp-server")
    stdin, _ := cmd.StdinPipe()
    stdout, _ := cmd.StdoutPipe()

    cmd.Start()

    // Send MCP message
    msg := mcpMessage{Method: "tools/list"}
    stdin.Write(toJSON(msg))

    // Read response
    scanner := bufio.NewScanner(stdout)
    scanner.Scan()
    response := scanner.Text()

    assert.Contains(t, response, "get-cluster-health")
}
```

## Success Criteria (Updated 2025-12-17)

### Phase 1 Success (Week 1) - ✅ COMPLETED
- ✅ HTTP/SSE transport compiles and runs
- ✅ HTTP transport responds to /health endpoint
- ✅ MCP SSE handler integrated (mcp.NewSSEHandler)
- ✅ Environment variable MCP_TRANSPORT=http works

### Phase 2 Success (Week 2) - ✅ COMPLETED
- ✅ OpenShift Lightspeed connects via HTTP/SSE transport
- ✅ Session management works for concurrent HTTP clients
- ✅ Integration tests pass for HTTP transport
- ✅ Official MCP Go SDK integrated

### Phase 3 Success (Week 3) - IN PROGRESS
- ✅ Production deployment with HTTP transport ready
- ⏳ Coordination Engine integration (ADR-011, 012, 013)
- ⏳ Performance targets validation
- ✅ Documentation complete

## Related ADRs

- [ADR-002: Official MCP Go SDK Adoption](002-official-mcp-go-sdk-adoption.md)
- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- **Parent Platform ADR-016**: OpenShift Lightspeed OLSConfig Integration

## References

- [MCP Specification - Transports](https://spec.modelcontextprotocol.io/specification/architecture/#transports)
- [OpenShift Lightspeed Documentation](https://docs.openshift.com/lightspeed/)
- [Parent Platform ADR-016](https://github.com/[your-org]/openshift-aiops-platform/blob/main/docs/adrs/016-openshift-lightspeed-olsconfig-integration.md)
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Transport confusion** | Clear env var naming, default to stdio |
| **Session memory leaks** | Periodic cleanup of expired sessions |
| **HTTP port conflicts** | Configurable port via env var |
| **stdio buffer overflow** | Limit message size, proper error handling |

## Approval

- **Architect**: Approved (Original: 2025-12-09, Updated: 2025-12-17)
- **Platform Team**: Approved (Original: 2025-12-09, Updated: 2025-12-17)
- **Date**: Original Decision: 2025-12-09, stdio Deprecation: 2025-12-17

## Revision History

| Date | Version | Change | Approver |
|------|---------|--------|----------|
| 2025-12-09 | 1.0 | Original ADR: Dual transport (HTTP/SSE + stdio) | Platform Team |
| 2025-12-17 | 2.0 | **stdio DEPRECATED**: HTTP/SSE only, focus on OpenShift Lightspeed | Platform Team |
