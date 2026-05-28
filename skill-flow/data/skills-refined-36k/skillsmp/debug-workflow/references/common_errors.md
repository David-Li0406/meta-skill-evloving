# Common Agentic Workflow Errors

This document catalogs common error patterns found in agentic workflow runs and how to identify them.

## MCP Server Failures

### DNS Resolution Failures

**Pattern:**
```
ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Client(reqwest::Error { kind: Request, url: "http://host.docker.internal/mcp/<server>", source: hyper_util::client::legacy::Error(Connect, ConnectError("dns error", Custom { kind: Uncategorized, error: "failed to lookup address information: Name does not resolve" })) })
```

**Symptoms:**
- Workflow shows as successful (green)
- All MCP servers fail to start
- Agent cannot use any MCP tools
- Errors contain "host.docker.internal" and "Name does not resolve"

**Search pattern:**
```bash
grep -E "mcp:.*failed|dns error.*host.docker.internal" agent-stdio.log
```

**Root cause:** Docker container cannot resolve `host.docker.internal` hostname

**Impact:** Complete MCP functionality failure (silent)

### OAuth Token Failures

**Pattern:**
```
WARN codex_rmcp_client::oauth: failed to read OAuth tokens from keyring: Platform secure storage failure: zbus error: org.freedesktop.DBus.Error.ServiceUnknown: The name org.freedesktop.secrets was not provided by any .service files
```

**Symptoms:**
- Multiple warnings about keyring access
- OAuth discovery failures
- MCP servers may fail to authenticate

**Search pattern:**
```bash
grep "WARN codex_rmcp_client::oauth" agent-stdio.log
```

**Root cause:** Missing `org.freedesktop.secrets` service in container

**Impact:** Authentication failures for MCP servers requiring OAuth

### Session Not Found

**Pattern:**
```
HTTP error: status=404, body={"jsonrpc":"2.0","error":{"code":-32001,"message":"Session not found"},"id":2}
```

**Symptoms:**
- Appears in MCP Gateway logs (gateway.md)
- Specific MCP server returns 404
- Tools from that server unavailable

**Search pattern:**
```bash
grep "Session not found" mcp-logs/gateway.md
```

**Root cause:** MCP server session expired or not initialized

**Impact:** Specific MCP server tools unavailable

## Firewall Issues

### Blocked Domains

**Pattern:**
```
TCP_DENIED/403
```

**Search pattern:**
```bash
grep "TCP_DENIED" sandbox/firewall/logs/access.log
```

**Symptoms:**
- Network requests blocked
- 403 errors in firewall logs

**Root cause:** Domain not in firewall allowlist

**Impact:** Network requests fail silently or with permission errors

### DNS Resolution in Firewall

**Pattern:**
```
TAG_NONE/503
```

**Search pattern:**
```bash
grep "TAG_NONE/503" sandbox/firewall/logs/access.log
```

**Symptoms:**
- Service unavailable errors
- DNS resolution issues

**Root cause:** DNS resolution failed through proxy

**Impact:** Network requests timeout or fail

## Agent Execution Errors

### Tool Call Failures

**Pattern:**
```
Error: Tool <tool-name> is not available
```

**Search pattern:**
```bash
grep -i "tool.*not available\|tool.*failed" agent-stdio.log
```

**Symptoms:**
- Agent attempts to use unavailable tools
- Workflow may complete with partial results

**Root cause:** MCP server failed to load or tool not exposed

**Impact:** Agent cannot complete requested tasks

### Timeout Errors

**Pattern:**
```
timeout waiting for
```

**Search pattern:**
```bash
grep -i "timeout" agent-stdio.log
```

**Symptoms:**
- Long-running operations fail
- Incomplete workflow results

**Root cause:** Operation exceeded timeout limit

**Impact:** Workflow fails or produces incomplete results

## GitHub Actions Errors

### Job Failures

**Pattern:** Check workflow-logs/ directory for job-specific errors

**Search pattern:**
```bash
ls -la workflow-logs/
cat workflow-logs/<job-name>/system.txt
```

**Symptoms:**
- Specific job shows as failed
- Error messages in job logs

**Root cause:** Various (dependency installation, permission issues, etc.)

**Impact:** Workflow execution blocked at specific job

### Artifact Upload Failures

**Pattern:**
```
Error: Unable to upload artifact
```

**Search pattern:**
```bash
grep "Unable to upload artifact" workflow-logs/*/system.txt
```

**Symptoms:**
- Missing artifacts
- Warning messages in conclusion job

**Root cause:** Artifact size limits, permission issues, or file path problems

**Impact:** Logs or outputs not available for analysis
