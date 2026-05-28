# MCP Integration Reference

## Overview

Aspire provides Model Context Protocol (MCP) integration, enabling AI assistants (Claude Code, GitHub Copilot, Cursor, VS Code) to interact with your running Aspire applications. This enables *agentic development* where AI can query resources, access telemetry, and execute commands.

## AI Assistants: Use These Tools

**When debugging Aspire apps, ALWAYS use MCP tools instead of curl or external commands.**

```
User: "Is my api service running?"
→ Use: list_resources (shows all resource states)
→ DON'T: curl, docker ps, or suggest checking dashboard manually

User: "Show me the logs for my api"
→ Use: list_console_logs with resource name "api"
→ DON'T: docker logs, curl to dashboard API

User: "What errors happened recently?"
→ Use: list_traces to find failed traces, then list_trace_structured_logs
→ DON'T: grep log files, curl OTLP endpoints

User: "Which integrations can I use for Redis?"
→ Use: list_integrations, then get_integration_docs
→ DON'T: web search (MCP has current docs)
```

## Quick Setup

### Using `aspire mcp init` (Recommended)

```bash
# Navigate to your AppHost directory
cd ./MyApp.AppHost

# Initialize MCP configuration
aspire mcp init
```

The command detects supported agent environments and creates configuration files:

```plaintext
Which agent environments do you want to configure?
[ ] Configure VS Code to use the Aspire MCP server
[ ] Configure GitHub Copilot CLI to use Aspire MCP server
[ ] Configure Claude Code to use Aspire MCP server
[ ] Configure Open Code to use Aspire MCP server

Which additional options do you want to enable?
[ ] Create an agent instructions file (AGENTS.md)
[ ] Configure Playwright MCP server
```

### Manual Configuration

1. Run your Aspire app
2. Open the Dashboard and click the MCP button (top right)
3. Use the dialog details to configure your AI assistant

Required settings:
- `url`: Aspire MCP endpoint address
- `type`: `http` (streamable-HTTP MCP server)
- `x-mcp-api-key`: HTTP header for authentication

## AI Assistant Configuration

### Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "aspire": {
      "type": "http",
      "url": "https://localhost:16036/mcp",
      "headers": {
        "x-mcp-api-key": "${input:aspire-api-key}"
      }
    }
  }
}
```

### VS Code (GitHub Copilot)

Add to your VS Code settings or `mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "aspire": {
        "type": "http",
        "url": "https://localhost:16036/mcp",
        "headers": {
          "x-mcp-api-key": "${input:aspire-api-key}"
        }
      }
    }
  }
}
```

### Cursor

Add to your Cursor MCP configuration following Cursor's MCP server documentation.

## MCP Tools

The Aspire MCP server provides these tools:

### Resource Management

| Tool | Description |
|------|-------------|
| `list_resources` | Lists all resources with state, health, endpoints, and commands |
| `execute_resource_command` | Executes a command on a resource (start, stop, restart) |

### Telemetry

| Tool | Description |
|------|-------------|
| `list_console_logs` | Lists console logs for a resource |
| `list_structured_logs` | Lists structured logs, optionally filtered by resource |
| `list_traces` | Lists distributed traces, optionally filtered by resource |
| `list_trace_structured_logs` | Lists structured logs for a specific trace |

### AppHost Management

| Tool | Description |
|------|-------------|
| `list_apphosts` | Lists all AppHosts in the workspace |
| `select_apphost` | Selects which AppHost to use when multiple exist |

### Integration Discovery (13.1+)

| Tool | Description |
|------|-------------|
| `list_integrations` | Lists available Aspire hosting integrations |
| `get_integration_docs` | Gets documentation for a specific integration package |

## Excluding Resources from MCP

Exclude sensitive resources from MCP access:

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// This resource won't be visible to AI assistants
var secrets = builder.AddProject<Projects.SecretsService>("secrets")
    .ExcludeFromMcp();

// This resource is visible (default)
var api = builder.AddProject<Projects.Api>("api");

builder.Build().Run();
```

## Dashboard MCP Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ASPIRE_DASHBOARD_MCP_ENDPOINT_URL` | MCP endpoint URL (e.g., `https://localhost:16036`) |
| `Dashboard:Mcp:AuthMode` | `ApiKey` or `Unsecured` (default: `Unsecured`) |
| `Dashboard:Mcp:PrimaryApiKey` | Primary API key for authentication |
| `Dashboard:Mcp:SecondaryApiKey` | Optional secondary API key |
| `Dashboard:Mcp:Disabled` | Set to `true` to disable MCP server |
| `Dashboard:Mcp:PublicUrl` | Public URL when behind a proxy |

### Configuration in appsettings.json

```json
{
  "Dashboard": {
    "Mcp": {
      "AuthMode": "ApiKey",
      "PrimaryApiKey": "your-secure-api-key"
    }
  }
}
```

## Troubleshooting

### HTTPS Certificate Issues

Some AI assistants don't support self-signed certificates. Configure HTTP-only MCP:

**launchSettings.json**:
```json
{
  "profiles": {
    "https": {
      "environmentVariables": {
        "ASPIRE_DASHBOARD_MCP_ENDPOINT_URL": "http://localhost:16036",
        "ASPIRE_ALLOW_UNSECURED_TRANSPORT": "true"
      }
    }
  }
}
```

### Connection Issues

1. Ensure Aspire app is running
2. Verify MCP endpoint URL matches dashboard configuration
3. Check API key is correctly configured
4. Review AI assistant logs for connection errors

### Data Truncation

AI models have token limits. Aspire MCP may truncate:
- Large exception stack traces
- Large telemetry collections (older items omitted)

## Example Prompts

Once configured, try these prompts with your AI assistant:

- "Are all my resources running?"
- "Show me the logs for the api resource"
- "What errors have occurred in the last 5 minutes?"
- "List the traces for slow requests"
- "What integrations are available for Redis?"

## CLI Commands

### Start MCP Server Manually

```bash
aspire mcp start
```

### Initialize MCP Configuration

```bash
# Interactive setup
aspire mcp init

# With specific project
aspire mcp init --project ./MyApp.AppHost
```
