---
name: memory-mcp
description: Use and troubleshoot the Memory MCP server for episodic memory retrieval and pattern analysis. This skill is applicable when working with MCP server tools, validating the MCP implementation, or debugging server issues.
---

# Memory MCP Server

Interact with and troubleshoot the Memory Model Context Protocol (MCP) server for the self-learning memory system.

## When to Use

- Starting or configuring the memory-mcp server
- Using MCP tools for memory retrieval and pattern analysis
- Validating the MCP server implementation
- Debugging MCP server issues (connection, tool execution, performance)
- Testing MCP tools using the MCP inspector
- Understanding MCP configuration and environment variables

## MCP Server Overview

The memory-mcp server exposes episodic memory functionality through the Model Context Protocol, allowing AI agents to:
- Query past experiences and learned patterns
- Analyze successful strategies from historical episodes
- Execute code in a secure sandbox environment
- Perform advanced statistical and predictive analysis
- Monitor server health and metrics

**Location**: `./target/release/memory-mcp-server`  
**Configuration**: `.mcp.json`  
**Transport**: stdio (Standard Input/Output)

## Available MCP Tools

### 1. query_memory

Query episodic memory for relevant past experiences and learned patterns.

**Parameters**:
- `query` (required): Search query describing the task or context
- `domain` (required): Task domain (e.g., 'web-api', 'data-processing')
- `task_type` (optional): Type of task - `code_generation`, `debugging`, `refactoring`, `testing`, `analysis`, `documentation`
- `limit` (default: 10): Maximum number of episodes to retrieve

**Use when**: You need relevant past experiences to inform current work.

### 2. analyze_patterns

Analyze patterns from past episodes to identify successful strategies.

**Parameters**:
- `task_type` (required): Type of task to analyze patterns for
- `min_success_rate` (default: 0.7): Minimum success rate (0.0-1.0)
- `limit` (default: 20): Maximum number of patterns to return

**Use when**: You want to identify proven successful approaches for a task type.

### 3. advanced_pattern_analysis

Perform advanced statistical analysis, predictive modeling, and causal inference on time series data.

**Parameters**:
- `analysis_type` (required): `statistical`, `predictive`, or `comprehensive`
- `time_series_data` (required): Object mapping variable names to numeric arrays
- `config` (optional): Analysis configuration

**Use when**: You need deep statistical insights and predictions from historical data.

### 4. execute_agent_code

Execute TypeScript/JavaScript code in a secure sandbox environment.

**Parameters**:
- `code` (required): TypeScript/JavaScript code to execute
- `context` (required): Execution context

**Use when**: You need to safely execute user-provided or generated code.

### 5. health_check

Check the health status of the MCP server and its components.

**Use when**: Diagnosing server issues or verifying operational status.

### 6. get_metrics

Get comprehensive monitoring metrics and statistics.

**Parameters**:
- `metric_type` (default: "all"): `all`, `performance`, `episodes`, or `system`

**Use when**: Monitoring server performance or gathering operational insights.

## Configuration

### .mcp.json Structure

```json
{
  "mcpServers": {
    "memory-mcp": {
      "type": "stdio",
      "command": "./target/release/memory-mcp-server",
      "args": [],
      "env": {
        "TURSO_DATABASE_URL": "file:/path/to/data/memory.db",
        "LOCAL_DATABASE_URL": "sqlite:/path/to/data/memory.db",
        "REDB_CACHE_PATH": "/path/to/data/cache.redb",
        "REDB_MAX_CACHE_SIZE": "1000",
        "MCP_CACHE_WARMING_ENABLED": "true",
        "MEMORY_MAX_EPISODES_CACHE": "1000",
        "MEMORY_CACHE_TTL_SECONDS": "1800",
        "RUST_LOG": "off"
      }
    }
  }
}
```

### Environment Variables

- **TURSO_DATABASE_URL**: Primary database URL (file:// for local)
- **LOCAL_DATABASE_URL**: Local SQLite database URL
- **REDB_CACHE_PATH**: Path to redb cache file
- **REDB_MAX_CACHE_SIZE**: Maximum cache entries (default: 1000)
- **MCP_CACHE_WARMING_ENABLED**: Enable cache warming on startup
- **MEMORY_MAX_EPISODES_CACHE**: Maximum episodes in cache
- **MEMORY_CACHE_TTL_SECONDS**: Cache time-to-live in seconds
- **RUST_LOG**: Logging level (off, error, warn, info, debug, trace)

## Starting the MCP Server

### Build the Server

```bash
cargo build --release --bin memory-mcp-server
```

### Run Directly

```bash
# With environment variables
export TURSO_DATABASE_URL="file:./data/memory.db"
export LOCAL_DATABASE_URL="sqlite:./data/memory.db"
export REDB_CACHE_PATH="./data/cache.redb"
export RUST_LOG=info

./target/release/memory-mcp-server
```

### Run via MCP Inspector

The MCP Inspector is the recommended tool for testing and validation.

```bash
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```

## Validation Workflow

Use the MCP Inspector to validate implementation against best practices:

1. **Build and Prepare**: Build the server.
2. **Launch Inspector**: Start the MCP Inspector.
3. **Validate Tools**: List tools, check schemas, test execution, and verify responses.
4. **Test Core Workflows**: Validate memory retrieval, pattern analysis, and health checks.
5. **Performance Testing**: Test with large datasets and monitor performance.

## Troubleshooting

### Common Issues

#### Server Won't Start

**Symptoms**: Process exits immediately or hangs

**Checks**: Verify binary existence, executability, database files, and environment variables.

**Solutions**: Rebuild, create data directory, and set environment variables.

#### Tool Execution Fails

**Symptoms**: Tool returns errors or unexpected results

**Checks**: Enable debug logging, validate input JSON, check database connectivity.

**Debug Commands**: Run with debug logging and check database.

#### Performance Issues

**Symptoms**: Slow responses, timeouts

**Checks**: Cache size configuration, database size, number of cached episodes.

**Solutions**: Adjust cache settings and monitor response times.

#### Connection Issues

**Symptoms**: Inspector can't connect, stdio communication fails

**Checks**: Ensure server process is running and no other process is using the same stdio.

**Solutions**: Kill existing processes and restart the inspector.

## Best Practices

### Tool Usage

✓ **DO**:
- Use `query_memory` before starting new tasks.
- Set appropriate `limit` values.
- Use `analyze_patterns` to identify proven strategies.

✗ **DON'T**:
- Query without a clear domain/task context.
- Ignore min_success_rate when analyzing patterns.

### Configuration

✓ **DO**:
- Use environment variables for all configuration.
- Set RUST_LOG=off in production.

✗ **DON'T**:
- Hardcode database paths in code.
- Enable debug logging in production.

### Testing

✓ **DO**:
- Always use MCP Inspector for validation.
- Test all tools before deploying.

✗ **DON'T**:
- Deploy without inspector validation.
- Skip schema validation.

## Related Resources

- **MCP Inspector**: https://modelcontextprotocol.io/docs/tools/inspector
- **MCP Specification**: https://modelcontextprotocol.io/
- **Project Configuration**: `.mcp.json`
- **Server Source**: `memory-mcp/src/bin/server.rs`
- **Tool Definitions**: `memory-mcp/src/server.rs`

## Summary

The memory-mcp skill helps you:
- ✓ Start and configure the MCP server
- ✓ Use all available MCP tools effectively
- ✓ Validate implementation with MCP Inspector
- ✓ Troubleshoot common issues
- ✓ Follow best practices for production deployment
- ✓ Integrate memory retrieval into workflows

Always validate using the MCP Inspector before deploying to production.