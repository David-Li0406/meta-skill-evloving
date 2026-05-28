---
name: aspire-mcp
description: Use .NET Aspire MCP server to monitor, debug, and manage distributed application resources including services, databases, containers, logs, traces, and integrations
---

# Aspire MCP Server Integration

This skill enables AI agents to interact with .NET Aspire distributed applications through the Model Context Protocol (MCP) server. Use this skill to monitor resources, debug issues, analyze distributed traces, and manage your Aspire AppHost applications.

## Purpose

The Aspire MCP server provides programmatic access to:

- All running resources (services, containers, executables, databases)
- Console and structured logs for debugging
- Distributed traces for performance analysis
- Resource health status and endpoints
- Available Aspire hosting integrations
- AppHost management and resource commands

## When to Use This Skill

Use this skill when you need to:

- Check the health status of all Aspire resources
- Debug startup errors or runtime failures
- Analyze distributed tracing data across services
- Monitor console logs from specific resources
- Execute commands on running resources
- Discover available Aspire integrations
- Work with multiple AppHosts in a workspace

## Available MCP Tools

### Resource Management

#### `list_resources`

Lists all resources including their state, health status, source, endpoints, and commands.

**Use cases**:

- Check if all services are running
- Verify resource health before running tests
- Get endpoint URLs for API testing
- Check which commands are available for each resource

**Example queries**:

- "Are all my Aspire resources healthy?"
- "What endpoints are available for the API service?"
- "Show me the status of all containers"

#### `execute_resource_command`

Executes a command on a specific resource.

**Parameters**:

- `resource_name`: Name of the resource (e.g., "menlo-api", "postgres")
- `command_name`: Command to execute (e.g., "Restart", "Stop", "Start")

**Use cases**:

- Restart unhealthy services
- Stop containers for maintenance
- Execute custom resource commands

**Example queries**:

- "Restart the menlo-api service"
- "Stop the postgres container"

### Logging and Debugging

#### `list_console_logs`

Retrieves console output logs for a specific resource.

**Parameters**:

- `resource_name`: Name of the resource to get logs from

**Use cases**:

- Read startup errors and stack traces
- Debug application crashes
- Monitor console output from services
- Check database initialization logs

**Example queries**:

- "Show me the console logs for menlo-api"
- "What errors are in the postgres logs?"
- "Check the last 50 lines of console output for the frontend"

#### `list_structured_logs`

Gathers structured logs with optional filtering by resource name.

**Parameters**:

- `resource_name` (optional): Filter logs by specific resource

**Use cases**:

- Search for specific error messages
- Filter logs by severity level
- Analyze application behavior
- Track request flow through services

**Example queries**:

- "Show me all error-level structured logs"
- "Find logs containing 'authentication failed'"
- "What structured logs does menlo-api have?"

#### `list_traces`

Fetches distributed traces; can filter using an optional resource name.

**Parameters**:

- `resource_name` (optional): Filter traces by resource

**Use cases**:

- Analyze request performance across services
- Identify slow database queries
- Debug cross-service communication issues
- Track request flow through the system

**Example queries**:

- "Show me the slowest traces in the last 5 minutes"
- "Analyze HTTP request performance for menlo-api"
- "What traces involve the postgres database?"

#### `list_trace_structured_logs`

Extracts structured logs associated with a particular trace.

**Parameters**:

- `trace_id`: The trace ID to get logs for

**Use cases**:

- Correlate logs with specific requests
- Debug failed requests end-to-end
- Understand what happened during a slow request

**Example queries**:

- "Show me all logs for trace ID abc123"
- "What logs are associated with this slow request?"

### Integration Discovery

#### `list_integrations`

Lists all available Aspire hosting integrations with their package IDs and versions.

**Use cases**:

- Discover what integrations are available
- Check package versions for integrations
- Find the right integration for a new dependency

**Example queries**:

- "What Aspire integrations are available for Redis?"
- "List all database integrations"
- "What version of the PostgreSQL integration is available?"

#### `get_integration_docs`

Retrieves documentation for specific Aspire hosting integration packages.

**Parameters**:

- `package_id`: The NuGet package ID of the integration

**Use cases**:

- Learn how to configure an integration
- Check what options are available
- Get code examples for integration setup

**Example queries**:

- "Show me the documentation for Aspire.Hosting.PostgreSQL"
- "How do I configure the Redis integration?"
- "What are the options for the Ollama integration?"

### AppHost Management

#### `list_apphosts`

Shows all available AppHosts in the workspace.

**Use cases**:

- Work with monorepo containing multiple Aspire apps
- Switch between different application configurations
- Manage multiple environments (dev, staging, etc.)

**Example queries**:

- "What AppHosts are available?"
- "List all Aspire applications in this workspace"

#### `select_apphost`

Designates a specific AppHost as the active working context.

**Parameters**:

- `apphost_name`: Name of the AppHost to select

**Use cases**:

- Switch between multiple Aspire applications
- Focus on a specific application context
- Isolate operations to one AppHost

**Example queries**:

- "Switch to the Menlo.AppHost"
- "Make the staging AppHost active"

## Setup Instructions

### Prerequisites

1. .NET Aspire 13 or later installed
2. Aspire CLI installed (`dotnet tool install -g aspire`)
3. An Aspire AppHost project in your solution

### Configuration Steps

#### Option 1: Automatic Configuration (Recommended)

Run the Aspire CLI command in your project directory:

```bash
cd /path/to/your/aspire/project
aspire mcp init
```

This automatically detects Claude Code and creates `.mcp.json` configuration.

#### Option 2: Manual Configuration

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "aspire": {
      "command": "aspire",
      "args": ["mcp", "start"],
      "transport": "stdio"
    }
  }
}
```

### Verification

After configuration, restart Claude Code and verify:

1. Ask: "Are all my Aspire resources running?"
2. Ask: "Show me the console logs for [your-service-name]"
3. Ask: "List available Aspire integrations"

If the MCP server is configured correctly, you should get responses with actual resource data.

## Best Practices

### 1. Resource Monitoring Workflow

When starting a development session:

1. Check resource health: "Are all my Aspire resources healthy?"
2. Review any unhealthy services: "Show console logs for [unhealthy-service]"
3. Restart if needed: "Restart [service-name]"
4. Verify: "Check the status of [service-name]"

### 2. Debugging Workflow

When encountering errors:

1. Check recent logs: "Show me console logs for [failing-service]"
2. Look for structured errors: "Show error-level structured logs for [service]"
3. Analyze traces: "Show me recent traces involving [service]"
4. Correlate: "Show structured logs for trace [trace-id]"
5. Fix and restart: "Restart [service]"

### 3. Performance Analysis Workflow

When optimizing performance:

1. Get slow traces: "Show me the slowest traces in the last 10 minutes"
2. Analyze trace details: "Show structured logs for trace [trace-id]"
3. Check resource involvement: "What resources are involved in this trace?"
4. Identify bottlenecks: "Which service has the highest latency?"

### 4. Integration Discovery Workflow

When adding new dependencies:

1. Search for integration: "What Aspire integrations are available for [technology]?"
2. Get documentation: "Show me the docs for [integration-package-id]"
3. Check version: "What version of [integration] is available?"
4. Follow docs to add integration to AppHost

## Common Use Cases

### Use Case 1: Debugging Startup Failures

**Scenario**: Your API service won't start.

**Workflow**:

1. "List all resources and their status"
2. "Show console logs for menlo-api" (find startup error)
3. "Show structured logs for menlo-api" (get detailed error info)
4. Fix the code
5. "Restart menlo-api"
6. "Verify menlo-api is healthy"

### Use Case 2: Analyzing Slow Requests

**Scenario**: API responses are slow.

**Workflow**:

1. "Show me the slowest traces for menlo-api"
2. "Show structured logs for trace [slow-trace-id]"
3. "What database queries are in this trace?"
4. "Show postgres console logs" (check for slow queries)
5. Optimize query
6. "Compare trace performance before and after"

### Use Case 3: Adding a New Integration

**Scenario**: You want to add Redis caching.

**Workflow**:

1. "What Aspire integrations are available for Redis?"
2. "Show documentation for Aspire.Hosting.Redis"
3. Follow docs to add to AppHost
4. "List resources" (verify Redis appears)
5. "Show Redis console logs" (verify startup)

### Use Case 4: Multi-Service Debugging

**Scenario**: Request fails across multiple services.

**Workflow**:

1. "Show traces where status code is 500"
2. "Show structured logs for trace [failed-trace-id]"
3. "What resources are involved in this trace?"
4. "Show console logs for each involved service"
5. Identify root cause
6. "Restart affected services"

## Resource Exclusion

To exclude sensitive resources from MCP access, use `.ExcludeFromMcp()` in your AppHost:

```csharp
var secretsDb = builder.AddPostgres("secrets-db")
    .ExcludeFromMcp(); // Not visible to AI agents
```

This is useful for:

- Production databases
- Secrets managers
- Sensitive configuration services
- Resources with destructive commands

## Integration with Other Skills

This skill works well with:

- **mcp-builder**: Build custom MCP servers to extend Aspire
- **webapp-testing**: Use Aspire MCP to verify services before running tests
- **doc-coauthoring**: Document your AppHost configuration and resource dependencies

## Troubleshooting

### MCP Server Not Responding

1. Check Aspire CLI is installed: `aspire --version`
2. Verify AppHost is running: `dotnet run --project src/api/Menlo.AppHost`
3. Check `.mcp.json` is in project root
4. Restart Claude Code

### No Resources Listed

1. Verify AppHost is running
2. Check you're in the correct AppHost context: "List available AppHosts"
3. Switch if needed: "Select [apphost-name]"
4. Try: "List resources" again

### Cannot Execute Commands

1. Check resource supports the command: "List resources" (shows available commands)
2. Verify resource name is correct (case-sensitive)
3. Check resource state (some commands only work in specific states)

### Logs Not Available

1. Resources must be running to have logs
2. Some resources may not emit console logs (check structured logs instead)
3. Logs may be filtered by timestamp (request recent logs specifically)

## Limitations

- MCP server requires Aspire 13 or later
- Resources must be running to access logs and traces
- Trace retention is limited (typically last 15-30 minutes of activity)
- Some resource commands may require elevated permissions
- MCP server runs locally (no remote AppHost access)

## References

- [Aspire MCP Server Documentation](https://aspire.dev/dashboard/mcp-server/)
- [Configure the MCP Server](https://aspire.dev/get-started/configure-mcp/)
- [Scaling AI Agents with Aspire](https://devblogs.microsoft.com/aspire/scaling-ai-agents-with-aspire-isolation/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Examples

### Example 1: Complete Debugging Session

User: "My API isn't responding"

Agent (using aspire-mcp skill):

1. Calls list_resources
   Result: menlo-api state is "Failed"

2. Calls list_console_logs for menlo-api
   Result: "System.InvalidOperationException: Database connection failed"

3. Calls list_resources again
   Result: postgres state is "Running" but health is "Unhealthy"

4. Calls list_console_logs for postgres
   Result: "ERROR: max connections reached"

Agent response: "Your API failed because the PostgreSQL database reached max connections.
Restart postgres to clear connections, then restart menlo-api."

User: "Restart both services"

Agent:
5. Calls execute_resource_command(resource_name: "postgres", command_name: "Restart")
6. Calls execute_resource_command(resource_name: "menlo-api", command_name: "Restart")
7. Calls list_resources to verify
   Result: Both services now "Running" and "Healthy"

Agent response: "Both services restarted successfully and are now healthy."

### Example 2: Performance Investigation

User: "Why are API requests slow?"

Agent (using aspire-mcp skill):

1. Calls list_traces(resource_name: "menlo-api")
   Result: Shows traces with latencies from 50ms to 2500ms

2. Calls list_trace_structured_logs for slowest trace
   Result: Shows database query took 2.3 seconds

3. Calls list_structured_logs(resource_name: "postgres")
   Result: Shows query: "SELECT * FROM budgets JOIN transactions..." (no indexes)

Agent response: "Your slow requests are caused by an unindexed database query.
The query 'SELECT * FROM budgets JOIN transactions...' takes 2.3 seconds.
Consider adding indexes on the join columns."

## Notes

- This skill is specific to .NET Aspire projects with MCP server configured
- Always verify AppHost is running before using MCP tools
- Resource names are case-sensitive and must match AppHost configuration
- Trace data is ephemeral (typically retained for 15-30 minutes)
- For production environments, use .ExcludeFromMcp() on sensitive resources
