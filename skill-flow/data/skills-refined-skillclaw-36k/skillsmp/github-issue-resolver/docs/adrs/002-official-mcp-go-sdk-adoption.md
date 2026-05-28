# ADR-002: Official MCP Go SDK Adoption

## Status

**ACCEPTED** - 2025-12-09

## Context

The Model Context Protocol (MCP) is an open standard developed by Anthropic for enabling AI assistants to interact with external tools and data sources. Implementing MCP compliance requires careful protocol adherence to ensure compatibility with MCP clients like OpenShift Lightspeed, Claude Desktop, and other AI assistants.

### MCP Implementation Options

1. **Official modelcontextprotocol/go-sdk**: Anthropic's official Go SDK
2. **Custom Implementation**: Build MCP protocol handler from scratch
3. **Third-Party Libraries**: Community-maintained MCP implementations

### Protocol Compliance Requirements

- **MCP Version**: 2025-03-26 (latest specification)
- **Transport Support**: StreamableHTTP (for OpenShift Lightspeed) and stdio (for local clients)
- **Protocol Features**: Tools, Resources, Prompts, Session Management
- **Error Handling**: Proper MCP error responses with correct status codes
- **Discovery**: Root endpoint returning server capabilities in MCP format

### Current OpenShift Cluster Environment

- **OpenShift Version**: 4.18.21
- **Kubernetes Version**: v1.31.10
- **OpenShift Lightspeed**: Deployed with OLSConfig support
- **Integration Target**: OpenShift AI Ops Platform Coordination Engine

## Decision

We will use the **official modelcontextprotocol/go-sdk** maintained by Anthropic as the foundation for MCP protocol implementation.

### Key Factors in Decision

1. **Official Support**: Maintained by Anthropic (creators of MCP specification)
2. **Protocol Compliance**: Guaranteed compatibility with latest MCP spec
3. **Proven in Production**: Used by containers/kubernetes-mcp-server (856 stars, Red Hat/containers team)
4. **Active Maintenance**: Regular updates aligned with spec changes
5. **Type Safety**: Go structs for all MCP message types
6. **Transport Abstraction**: Built-in support for stdio and HTTP transports
7. **Community Trust**: Reference implementation for Go ecosystem

### Reference Implementation Validation

The **containers/kubernetes-mcp-server** project validates our approach:

- ✅ Uses modelcontextprotocol/go-sdk successfully
- ✅ Deployed in production Kubernetes environments
- ✅ 856 GitHub stars indicates community validation
- ✅ Maintained by Red Hat containers team (reputable source)
- ✅ Implements tools and resources similar to our requirements

## Alternatives Considered

### Custom MCP Implementation

**Pros**:
- Full control over protocol implementation
- No external dependencies
- Optimized for specific use cases

**Cons**:
- ❌ High development effort (weeks of work)
- ❌ Risk of protocol non-compliance
- ❌ Maintenance burden for spec updates
- ❌ Compatibility issues with MCP clients
- ❌ Requires deep protocol expertise

**Verdict**: Rejected due to unnecessary complexity and compliance risk

### Third-Party Community Libraries

**Pros**:
- Potentially more features than official SDK
- Community-driven enhancements

**Cons**:
- ❌ No third-party Go SDKs with significant adoption
- ❌ Uncertain maintenance and support
- ❌ Risk of abandonment
- ❌ Potential protocol deviations

**Verdict**: Rejected due to lack of mature alternatives

### TypeScript SDK (with Go wrapper)

**Pros**:
- More mature TypeScript ecosystem
- Cross-language code reuse

**Cons**:
- ❌ Requires Node.js runtime in container
- ❌ Defeats purpose of Go selection (ADR-001)
- ❌ Complex FFI or subprocess communication
- ❌ Increased container size and complexity

**Verdict**: Rejected as it contradicts ADR-001

## Consequences

### Positive

- ✅ **Protocol Compliance**: Guaranteed MCP spec adherence
- ✅ **Reduced Development Time**: No need to implement protocol from scratch
- ✅ **Automatic Updates**: SDK updates track spec changes
- ✅ **OpenShift Lightspeed Compatibility**: Verified by containers/kubernetes-mcp-server
- ✅ **Type Safety**: Go structs for all message types prevent errors
- ✅ **Transport Flexibility**: Built-in stdio and HTTP support
- ✅ **Testing Support**: SDK includes test utilities
- ✅ **Community Support**: Reference implementation for troubleshooting

### Negative

- ⚠️ **External Dependency**: Reliance on Anthropic SDK releases
- ⚠️ **API Changes**: Breaking changes in SDK require updates
- ⚠️ **Limited Customization**: Must work within SDK abstractions

### Neutral

- **Documentation**: SDK documentation is comprehensive but Go-specific
- **Learning Curve**: Team must learn SDK patterns and conventions
- **Versioning**: Must track SDK versions carefully for compatibility

## Implementation Plan

### Phase 1: SDK Integration (Week 1)

1. **Dependency Setup**
   ```go
   // go.mod
   require (
       github.com/modelcontextprotocol/go-sdk v0.x.x
   )
   ```

2. **Server Initialization**
   ```go
   import "github.com/modelcontextprotocol/go-sdk/server"

   mcpServer := server.NewMCPServer(
       server.WithName("openshift-cluster-health"),
       server.WithVersion("0.1.0"),
   )
   ```

3. **Transport Configuration**
   ```go
   // stdio transport (default)
   transport := server.NewStdioTransport()

   // HTTP transport (for OpenShift Lightspeed)
   transport := server.NewHTTPTransport(":8080")
   ```

### Phase 2: Tools and Resources Implementation (Week 1-2)

1. **Register MCP Tools**
   ```go
   mcpServer.RegisterTool("get-cluster-health",
       getClusterHealthHandler)
   mcpServer.RegisterTool("analyze-anomalies",
       analyzeAnomaliesHandler)
   mcpServer.RegisterTool("trigger-remediation",
       triggerRemediationHandler)
   mcpServer.RegisterTool("list-pods",
       listPodsHandler)
   ```

2. **Register MCP Resources**
   ```go
   mcpServer.RegisterResource("cluster://health",
       clusterHealthResourceHandler)
   mcpServer.RegisterResource("cluster://nodes",
       clusterNodesResourceHandler)
   mcpServer.RegisterResource("cluster://incidents",
       clusterIncidentsResourceHandler)
   ```

### Phase 3: Testing and Validation (Week 2-3)

1. **Protocol Compliance Testing**
   - Use MCP Inspector tool for validation
   - Test with OpenShift Lightspeed
   - Verify message format correctness

2. **Integration Testing**
   - Test stdio transport with Claude Desktop
   - Test HTTP transport with OpenShift Lightspeed
   - Validate error handling

## Technical Details

### MCP Message Flow

```
Client (Lightspeed)  →  HTTP POST /message  →  MCP Server (Go SDK)
                                                      ↓
                                                 Process Request
                                                      ↓
                                              Execute Tool/Resource
                                                      ↓
Client (Lightspeed)  ←  HTTP Response (JSON) ←  MCP Server (Go SDK)
```

### Supported MCP Features

| Feature | Support | Implementation |
|---------|---------|----------------|
| **Tools** | ✅ Yes | 5 tools (cluster-health, anomalies, remediation, list-pods, model-status) |
| **Resources** | ✅ Yes | 3 resources (cluster://health, cluster://nodes, cluster://incidents) |
| **Prompts** | ⏳ Future | Not required for Phase 1 |
| **Sampling** | ❌ No | Not applicable for our use case |
| **Logging** | ✅ Yes | slog integration |
| **Session Management** | ✅ Yes | Built into SDK |

### SDK Version Strategy

- **Initial Version**: Use latest stable release at project start
- **Update Policy**: Review SDK updates monthly
- **Breaking Changes**: Test thoroughly before upgrading
- **Pinning**: Pin to specific version in go.mod for reproducibility

## Success Criteria

### Phase 1 Success (Week 1)
- ✅ SDK integrated and compiling
- ✅ Basic server starts with stdio transport
- ✅ HTTP transport working
- ✅ Root discovery endpoint functional

### Phase 2 Success (Week 2)
- ✅ All 5 tools registered and working
- ✅ All 3 resources registered and working
- ✅ MCP Inspector validation passing

### Phase 3 Success (Week 3)
- ✅ OpenShift Lightspeed integration confirmed
- ✅ Claude Desktop integration confirmed
- ✅ E2E tests passing

## Monitoring and Maintenance

### SDK Update Process

1. **Monthly Review**: Check for new SDK releases
2. **Changelog Analysis**: Review breaking changes and new features
3. **Testing**: Test updates in development environment
4. **Gradual Rollout**: Deploy to dev → staging → production

### Compatibility Matrix

| Component | Version | Compatibility |
|-----------|---------|--------------|
| **MCP Spec** | 2025-03-26 | Required |
| **Go SDK** | Latest stable | Track monthly |
| **OpenShift Lightspeed** | Latest | Test integration |
| **Claude Desktop** | Latest | Test integration |

## Related ADRs

- [ADR-001: Go Language Selection](001-go-language-selection.md)
- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- [ADR-004: Transport Layer Strategy (StreamableHTTP + stdio)](004-transport-layer-strategy.md)

## References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk) - Official Go SDK
- [containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) - Reference implementation
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Protocol validation tool
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **SDK breaking changes** | Medium | Medium | Pin versions, test updates before production |
| **SDK bugs** | Low | Medium | Report to Anthropic, contribute fixes |
| **Spec evolution** | High | Low | SDK tracks spec automatically |
| **Performance issues** | Low | Low | containers/kubernetes-mcp-server proves performance |

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
