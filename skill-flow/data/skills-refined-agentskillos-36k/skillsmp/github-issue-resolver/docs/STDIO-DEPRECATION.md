# stdio Transport Deprecation - 2025-12-17

## Summary

As of **2025-12-17**, the stdio transport is **DEPRECATED** and no longer supported. The OpenShift Cluster Health MCP Server now supports **HTTP/SSE transport only**.

## What Changed

### ADR-004 Updated
- **Status**: Changed from ACCEPTED to SUPERSEDED
- **Title**: Updated from "StreamableHTTP + stdio" to "HTTP/SSE for OpenShift Lightspeed"
- **Decision**: HTTP/SSE only, stdio deprecated
- **Revision**: Added deprecation notice and revision history

### Code Changes

#### `internal/server/config.go`
- Added deprecation comments to `TransportStdio` constant
- Updated default transport comment to clarify HTTP is default
- HTTP remains the default (no behavior change)

#### `internal/server/server.go`
- `startStdioTransport()`: Now returns error with deprecation message
- `Start()`: Updated comments to note stdio deprecation
- Added helpful error messages explaining why stdio is deprecated

#### `README.md`
- Updated "Run locally" section to use HTTP transport
- Added curl example for local testing

## Rationale

### Why Deprecate stdio?

1. ✅ **Primary use case**: OpenShift Lightspeed integration via HTTP/SSE
2. ✅ **Local development**: HTTP testing works fine (curl, Postman)
3. ✅ **Never implemented**: stdio was only a stub (server.go:322-335)
4. ✅ **Reduced complexity**: Single transport is easier to maintain and test

### Why HTTP/SSE is Sufficient

1. ✅ **Lightspeed requirement**: OLSConfig mandates HTTP endpoint
2. ✅ **Fully implemented**: Using official `mcp.NewSSEHandler()` from go-sdk
3. ✅ **Production ready**: Deployed and tested in OpenShift
4. ✅ **Local dev friendly**: Developers can test with HTTP locally

## Migration Guide

### For Local Development

**Before (stdio):**
```bash
# NOT SUPPORTED ANYMORE
MCP_TRANSPORT=stdio ./mcp-server
```

**After (HTTP):**
```bash
# Run with HTTP transport (now default)
MCP_TRANSPORT=http ./mcp-server

# Or just run without env var (HTTP is default)
./mcp-server

# Test with curl
curl http://localhost:8080/health
curl -X POST http://localhost:8080/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### For OpenShift Deployment

**No changes required** - HTTP transport was already the default in production.

```yaml
# Deployment still uses HTTP/SSE (unchanged)
env:
  - name: MCP_TRANSPORT
    value: "http"  # This was already the default
```

### For Claude Desktop Testing

**Not supported** - Claude Desktop integration via stdio is no longer available.

For local testing, use HTTP transport with curl or Postman instead.

## What If I Try to Use stdio?

If you attempt to use stdio transport, the server will:

1. Log an error message explaining the deprecation
2. Provide instructions to use HTTP transport
3. Return an error and **refuse to start**

**Error output:**
```
ERROR: stdio transport is DEPRECATED as of 2025-12-17
Please use HTTP/SSE transport instead:
  MCP_TRANSPORT=http ./mcp-server

Rationale for deprecation:
  - Primary use case is OpenShift Lightspeed integration via HTTP/SSE
  - Local development works fine with HTTP transport
  - stdio was never fully implemented (stub only)
  - Reduces codebase complexity and maintenance burden
```

## Impact Assessment

### ✅ No Breaking Changes for Production

- **OpenShift deployments**: Already using HTTP/SSE (no change)
- **Lightspeed integration**: Already using HTTP/SSE (no change)
- **Default behavior**: HTTP is already the default

### ⚠️ Breaking Change for stdio Users (If Any)

- **Local stdio testing**: Must switch to HTTP
- **Claude Desktop integration**: No longer supported (use HTTP)

**Expected impact**: **MINIMAL** - stdio was never fully implemented or used.

## Files Modified

| File | Change |
|------|--------|
| `docs/adrs/004-transport-layer-strategy.md` | Updated status to SUPERSEDED, added deprecation notice, updated decision to HTTP/SSE only |
| `internal/server/config.go` | Added deprecation comments to stdio constants |
| `internal/server/server.go` | Updated `startStdioTransport()` to return error with deprecation message |
| `README.md` | Updated local development section to use HTTP transport |
| `docs/STDIO-DEPRECATION.md` | **NEW** - This summary document |

## Related ADRs

- **ADR-002**: Official MCP Go SDK Adoption (✅ Fully implemented)
- **ADR-004**: Transport Layer Strategy (✅ Updated to HTTP/SSE only)
- **ADR-011**: ArgoCD and MCO Integration Boundaries
- **ADR-012**: Non-ArgoCD Application Remediation Strategy
- **ADR-013**: Multi-Layer Coordination Engine Design

## Next Steps

1. ✅ **stdio deprecated** - ADR-004 updated, code changed
2. ⏳ **Focus on Coordination Engine** - Implement ADR-011, 012, 013
3. ⏳ **OpenShift Lightspeed testing** - Validate HTTP/SSE integration
4. ⏳ **Production deployment** - Deploy MCP server with HTTP/SSE

## Approval

- **Decision Date**: 2025-12-17
- **Approved By**: Platform Team
- **ADR Reference**: ADR-004 v2.0

---

**Questions?** See ADR-004 for complete rationale and technical details.
