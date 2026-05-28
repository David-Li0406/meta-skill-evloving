# ADR-001: Go Language Selection for MCP Server

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server requires a programming language that aligns with Kubernetes-native tooling, provides excellent performance, and produces lightweight, self-contained binaries for container deployment.

### Language Options Evaluated

We evaluated three primary language options for implementing the MCP server:

1. **TypeScript/Node.js**
2. **Python**
3. **Go**

### Current Ecosystem Analysis

- **OpenShift AI Ops Platform**: Currently uses TypeScript for MCP server implementation
- **Coordination Engine**: Python/Flask-based service
- **Kubernetes Ecosystem**: Predominantly Go-based (kubectl, operators, controllers)
- **MCP SDK Support**: Official SDKs available for TypeScript, Python, and Go

### Requirements

1. **Performance**: Low latency (<100ms p95), minimal memory footprint (<50MB at rest)
2. **Container Size**: Small container images (<50MB)
3. **Kubernetes Integration**: Native client-go support
4. **Deployment**: Single binary deployment model
5. **Maintainability**: Strong typing, good tooling, active community
6. **Ecosystem Alignment**: Fit with Kubernetes-native patterns

## Decision

We will use **Go 1.21+** as the implementation language for the OpenShift Cluster Health MCP Server.

### Key Factors in Decision

1. **Kubernetes-Native**: Go is the native language of Kubernetes, with official client-go library
2. **Performance**: Compiled binaries with excellent runtime performance and low memory overhead
3. **Single Binary**: Produces self-contained binaries with no runtime dependencies
4. **Container Size**: Distroless images can be <20MB (vs 100MB+ for Node.js, 150MB+ for Python)
5. **Reference Implementation**: containers/kubernetes-mcp-server (856 stars) proves Go viability for MCP
6. **Official SDK**: modelcontextprotocol/go-sdk provides official MCP protocol support
7. **Type Safety**: Strong static typing prevents runtime errors
8. **Concurrency**: Native goroutines for handling concurrent MCP sessions

## Alternatives Considered

### TypeScript/Node.js

**Pros**:
- Official @modelcontextprotocol/sdk with mature ecosystem
- Team familiarity (current TypeScript MCP server exists)
- Rich npm package ecosystem
- Good developer experience with VS Code

**Cons**:
- ❌ Large container images (>100MB base)
- ❌ Runtime dependency (Node.js runtime required)
- ❌ Higher memory footprint (>100MB typical)
- ❌ Not Kubernetes-native (requires third-party K8s clients)
- ❌ Slower startup times compared to compiled binaries

**Verdict**: Rejected due to container size, memory overhead, and lack of Kubernetes ecosystem alignment

### Python

**Pros**:
- Coordination Engine already uses Python (team familiarity)
- Official MCP SDK available
- Excellent for data science/ML integrations
- Rich ecosystem for observability and monitoring

**Cons**:
- ❌ Large container images (>150MB base)
- ❌ Runtime dependency (Python interpreter required)
- ❌ Global Interpreter Lock (GIL) limits concurrency
- ❌ Not Kubernetes-native (third-party clients like kubernetes-python)
- ❌ Dynamic typing increases risk of runtime errors

**Verdict**: Rejected due to container size, performance concerns, and lack of Kubernetes ecosystem fit

## Consequences

### Positive

- ✅ **Native Kubernetes Integration**: Direct use of client-go for K8s API access
- ✅ **Minimal Container Size**: Distroless images <20MB (vs 100MB+ alternatives)
- ✅ **Performance**: <50MB memory at rest, <100ms tool response times
- ✅ **Single Binary**: No runtime dependencies, simplified deployment
- ✅ **Proven Pattern**: containers/kubernetes-mcp-server validates approach
- ✅ **Strong Typing**: Compile-time error detection reduces bugs
- ✅ **Standard Library**: Comprehensive stdlib (net/http, slog, context, testing)
- ✅ **Ecosystem Alignment**: Follows Kubernetes operator patterns

### Negative

- ⚠️ **Team Learning Curve**: Team familiar with TypeScript/Python, not Go
- ⚠️ **Separate Codebase**: Cannot share code with Python Coordination Engine
- ⚠️ **SDK Maturity**: Go SDK newer than TypeScript SDK (but proven by containers/kubernetes-mcp-server)
- ⚠️ **Development Speed**: May be slower initially due to learning curve

### Neutral

- **Testing**: Go testing package is comprehensive but different from Jest/pytest
- **Dependency Management**: Go modules are robust but require different workflow
- **Error Handling**: Explicit error handling (no exceptions) requires discipline

## Implementation Notes

### Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Language** | Go 1.21+ | Native K8s support, performance, single binary |
| **MCP SDK** | modelcontextprotocol/go-sdk | Official Anthropic SDK |
| **K8s Client** | k8s.io/client-go v0.29+ | Official Kubernetes client |
| **HTTP Server** | net/http (stdlib) | No dependencies, production-ready |
| **Logging** | slog (stdlib) | Structured logging, zero dependencies |
| **Metrics** | prometheus/client_golang | Standard Prometheus integration |
| **Testing** | testing (stdlib) + testify | Unit and integration testing |

### Dependencies Intentionally Excluded

- ❌ **Web Frameworks** (Gin, Echo): stdlib net/http sufficient
- ❌ **ORMs** (GORM, sqlc): Stateless design, no database
- ❌ **DI Containers**: Simple manual dependency injection
- ❌ **Heavy Libraries**: Keep dependency tree minimal

### Performance Targets

| Metric | Target | Comparison to Alternatives |
|--------|--------|---------------------------|
| **Binary Size** | <20MB | Node.js: N/A, Python: N/A |
| **Container Image** | <50MB | Node.js: >100MB, Python: >150MB |
| **Memory (Rest)** | <50MB | Node.js: >100MB, Python: >80MB |
| **Startup Time** | <1s | Node.js: 2-3s, Python: 1-2s |
| **Tool Latency** | <100ms p95 | Comparable across languages |

### Migration Path from TypeScript

As documented in PRD Phase 5 (Month 2-6):

1. **Month 2**: Run both servers in parallel, verify feature parity
2. **Month 3**: Migrate Lightspeed integration to Go server
3. **Month 4**: Internal testing and feedback
4. **Month 5**: Deprecate TypeScript server (EOL announcement)
5. **Month 6**: Archive TypeScript implementation

## Related ADRs

- [ADR-002: Official MCP Go SDK Adoption](002-official-mcp-go-sdk-adoption.md)
- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- [ADR-008: Distroless Container Images](008-distroless-container-images.md)

## References

- [Go Official Website](https://go.dev/)
- [client-go Kubernetes Client](https://github.com/kubernetes/client-go)
- [containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) - Go MCP reference implementation (856 stars)
- [modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk) - Official MCP Go SDK
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| **Go expertise gap** | 1-week learning period, leverage containers/kubernetes-mcp-server as reference |
| **SDK immaturity** | containers/kubernetes-mcp-server proves Go SDK viability |
| **Development velocity** | Accept slower initial development for long-term performance gains |
| **Code reuse with Python** | Share patterns/architecture, not code (different languages inevitable) |

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
