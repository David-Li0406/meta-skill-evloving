# VS Code Extension Reference

## Overview

The Aspire VS Code extension brings Aspire CLI features directly into VS Code, providing commands for project creation, integration management, multi-language debugging, and deployment.

## Prerequisites

- [Aspire CLI](/reference/cli/overview/) installed and available on PATH
- Verify with: `aspire --version`

## Installation

1. Open VS Code
2. Open Extensions view: **View** > **Extensions** (or `Cmd+Shift+X` / `Ctrl+Shift+X`)
3. Search for "aspire"
4. Select **Aspire** extension by **Microsoft**
5. Click **Install**

Or install from [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=microsoft-aspire.aspire-vscode).

## Available Commands

Access commands via Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), then type "Aspire":

| Command | Description | Status |
|---------|-------------|--------|
| **Aspire: New Aspire project** | Create new AppHost or starter app from template | Available |
| **Aspire: Add an integration** | Add hosting integration (`Aspire.Hosting.*`) | Available |
| **Aspire: Configure launch.json** | Add Aspire debugger launch configuration | Available |
| **Aspire: Manage configuration settings** | Manage settings including feature flags | Available |
| **Aspire: Open Aspire terminal** | Open terminal for Aspire CLI commands | Available |
| **Aspire: Publish deployment artifacts** | Generate deployment artifacts | Preview |
| **Aspire: Deploy app** | Deploy to defined targets | Preview |

## Key Features

### Project Creation

Use **Aspire: New Aspire project** to create:

- **Starter projects**: Full solutions with frontend, API, and AppHost
- **Empty projects**: Minimal AppHost for existing solutions
- **Language-specific starters**: Python + React, FastAPI, etc.

### Integration Management

Use **Aspire: Add an integration** to add integrations interactively:

1. Search for integration (e.g., "redis", "postgres")
2. Select from available packages
3. Extension updates your AppHost project

### Multi-Language Debugging

Debug C#, Python, and JavaScript resources simultaneously:

1. Run **Aspire: Configure launch.json** to set up debugging
2. Press `F5` to start debugging
3. Set breakpoints in any supported language
4. Debug across service boundaries

**Supported debugging scenarios:**
- .NET projects (C#)
- Python scripts and modules
- Python Flask applications
- Uvicorn/FastAPI applications
- Node.js/JavaScript applications

### Deployment

Preview features for deployment:

- **Publish deployment artifacts**: Generate Docker Compose, Kubernetes manifests, or Azure Bicep
- **Deploy app**: Deploy directly to configured targets

## launch.json Configuration

The extension generates launch configurations automatically. Example:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Aspire: MyApp.AppHost",
      "type": "aspire",
      "request": "launch",
      "project": "${workspaceFolder}/MyApp.AppHost/MyApp.AppHost.csproj"
    }
  ]
}
```

### Manual Configuration

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Aspire App",
      "type": "aspire",
      "request": "launch",
      "project": "${workspaceFolder}/src/MyApp.AppHost/MyApp.AppHost.csproj",
      "launchProfile": "https"
    }
  ]
}
```

## Aspire Terminal

The **Aspire: Open Aspire terminal** command opens a preconfigured terminal for Aspire CLI commands:

- Environment variables set correctly
- PATH includes Aspire CLI
- Ready for commands like `aspire run`, `aspire deploy`

## Debugging Workflows

### Debug All Resources

1. Set breakpoints in C#, Python, or JavaScript files
2. Press `F5` or click **Run and Debug**
3. Extension launches AppHost and attaches to all debuggable resources
4. Hit breakpoints in any language

### Debug Specific Resource

1. In the Debug view, click the resource dropdown
2. Select specific resource to debug
3. Only that resource will have debugger attached

### Python Debugging Tips

Python resources are automatically configured for debugging:

```csharp
// Python debugging is enabled by default
var api = builder.AddUvicornApp("api", "../api", "main:app");
// VS Code can attach debugger automatically
```

### JavaScript Debugging Tips

JavaScript debugging requires Node.js inspect mode:

```csharp
var frontend = builder.AddJavaScriptApp("frontend", "../frontend")
    .WithArgs("--inspect");  // Enable Node.js debugging
```

## Working with MCP

The extension integrates with MCP for AI-assisted development:

1. Run `aspire mcp init` in the Aspire terminal
2. Select VS Code when prompted
3. GitHub Copilot can now query your Aspire application

## Tips and Best Practices

### Workspace Setup

- Open folder containing your `.sln` or AppHost project
- Extension auto-detects Aspire projects

### Multiple AppHosts

If workspace contains multiple AppHosts:
- Extension prompts which to use
- Or specify in launch.json: `"project": "path/to/specific/AppHost.csproj"`

### Troubleshooting

**Extension commands not appearing:**
- Verify CLI installed: `aspire --version`
- Restart VS Code after CLI installation

**Debugging not attaching:**
- Ensure launch.json is configured
- Check Debug Console for errors
- Verify resource supports debugging (not all containers do)

**Integration not found:**
- Run `aspire add` in terminal for interactive search
- Check NuGet for package name

## Feedback

Report issues or request features:
1. Visit [Aspire GitHub repository](https://github.com/dotnet/aspire/issues)
2. Create new issue with `area-extension` label
