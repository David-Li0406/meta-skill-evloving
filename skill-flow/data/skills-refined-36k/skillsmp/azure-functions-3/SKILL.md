---
name: azure-functions
description: Helps create, debug, and deploy Azure Functions using the Python v2 programming model. Use this skill when working with HTTP triggers, MCP triggers, timer triggers, or any Azure Functions development including local testing with func start and Azurite.
---

# Azure Functions Development Skill

## Overview

This skill helps you build Azure Functions using the **Python v2 programming model** with decorators.

## Key Patterns

### HTTP Trigger Function

```python
import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="my_function")
@app.route(route="api/endpoint", methods=["GET", "POST"])
def my_function(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function with proper error handling."""
    try:
        # Parse request
        data = req.get_json() if req.method == "POST" else dict(req.params)
        
        # Your logic here
        result = {"status": "success", "data": data}
        
        return func.HttpResponse(
            body=json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
```

### MCP Tool Trigger

```python
@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="my_tool",
    description="What this tool does and when to use it",
    toolProperties='[{"propertyName": "input", "propertyType": "string", "description": "The input parameter"}]'
)
def my_tool(context) -> str:
    """MCP tool function."""
    content = json.loads(context)
    input_value = content["arguments"].get("input", "")
    return json.dumps({"result": input_value})
```

## Configuration Files

### host.json (Runtime Config)
```json
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "extensions": {
    "mcp": {
      "enabled": true
    }
  }
}
```

### local.settings.json (Local Development)
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing"
  }
}
```

## Local Development Commands

```bash
# Start Azurite storage emulator (required)
azurite --silent --location /tmp/azurite

# Start the function app locally
cd src/function_app_directory
func start

# Install Azure Functions Core Tools (macOS)
brew tap azure/functions
brew install azure-functions-core-tools@4
```

## Deployment with Azure Developer CLI

```bash
# Initialize project from template
azd init --template <template-name> -e <environment-name>

# Deploy to Azure
azd up

# Get function keys
az functionapp keys list --resource-group <rg> --name <app-name>
```

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `AzureWebJobsStorage` error | Start Azurite: `azurite --silent` |
| Functions not discovered | Ensure `host.json` has correct extension bundle |
| MCP tools not showing | Check `mcp.enabled: true` in host.json extensions |
| 401 Unauthorized | Include `x-functions-key` header for FUNCTION auth level |

## Best Practices

1. **Always use type hints** for better IDE support
2. **Log important operations** with `logging.info()` and `logging.error()`
3. **Return JSON responses** with appropriate status codes
4. **Use FUNCTION auth level** for production (not ANONYMOUS)
5. **Test locally** with `func start` before deploying
