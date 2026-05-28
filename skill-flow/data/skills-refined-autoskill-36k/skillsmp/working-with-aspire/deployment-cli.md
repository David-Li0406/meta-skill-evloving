# Deployment and CLI Reference

## Aspire CLI

### Installation
```bash
dotnet tool install -g aspire
```

### Self-Update (13.1+)
```bash
# Update CLI to latest version
aspire update --self

# Select channel (stable, preview, staging)
aspire update --self --channel preview
```

### Common Commands

| Command | Status | Description |
|---------|--------|-------------|
| `aspire new` | Stable | Create new Aspire project from template |
| `aspire init` | Stable | Initialize Aspire in existing project or create single-file AppHost |
| `aspire add` | Stable | Add integration package |
| `aspire run` | Stable | Run the AppHost for local development |
| `aspire do` | Preview | Execute specific pipeline step and dependencies |
| `aspire deploy` | Preview | Deploy to target environment |
| `aspire publish` | Preview | Generate deployment artifacts |
| `aspire exec` | Preview | Execute command with resource context |
| `aspire mcp` | Stable | Manage MCP server for AI assistants |
| `aspire update` | Preview | Update Aspire packages and templates |

### aspire new
```bash
# Create starter solution (with Web frontend + API)
aspire new aspire-starter -o MyApp

# Create empty solution (AppHost + ServiceDefaults only)
aspire new aspire --name MyApp

# List available templates
aspire new --list

# Create Python starter (FastAPI + React)
aspire new aspire-py-starter -n MyApp -o MyApp
```

**Available templates:**
| Template | Description |
|----------|-------------|
| `aspire` | Empty: AppHost + ServiceDefaults |
| `aspire-starter` | Web frontend + API backend |
| `aspire-py-starter` | Python (FastAPI) + React |

**VS Code Extension (GUI alternative):**
Instead of CLI, use the VS Code extension:
1. Open Command Palette (Cmd/Ctrl + Shift + P)
2. Run **Aspire: New Aspire project**
3. Select template and specify name/location

### aspire init (13.0+)
```bash
# Aspirify an existing solution (interactive)
aspire init

# Create single-file AppHost
aspire init --single-file

# Specify source and version
aspire init --source https://api.nuget.org/v3/index.json --version 13.1.0
```

The `aspire init` command:
- Detects existing projects in your solution
- Creates an AppHost project referencing them
- Sets up service defaults
- Supports single-file AppHost (`.cs` file without `.csproj`)

### aspire add
```bash
# Interactive search and add
aspire add redis

# Add specific package
aspire add Aspire.Hosting.Redis
```

### aspire run
```bash
# Run AppHost
aspire run

# Run with specific launch profile
aspire run --launch-profile Production

# Run specific project
aspire run --project ./src/MyApp.AppHost
```

### aspire exec
```bash
# Run command with resource's connection strings
aspire exec --resource api -- dotnet ef migrations add Init

# Apply migrations
aspire exec --resource api -- dotnet ef database update

# Run with specific project
aspire exec --project ./src/AppHost -- dotnet test
```

### aspire do (13.0+ Pipeline System)

The `aspire do` command executes specific pipeline steps:

```bash
# Generate manifest
aspire do publish-manifest --output-path ./aspire-manifest.json

# Build container images
aspire do build

# Push images to registry
aspire do push

# Provision infrastructure only
aspire do provision-infra

# Deploy specific service
aspire do deploy-apiservice

# View available steps
aspire do diagnostics

# Docker Compose operations
aspire do prepare-compose --environment staging
aspire do docker-compose-down-compose
```

**Well-Known Steps:**
| Step | Description |
|------|-------------|
| `deploy` | Full deployment (infra + images + deploy) |
| `publish` | Generate deployment artifacts |
| `build` | Build container images |
| `push` | Push images to registry |
| `publish-manifest` | Generate manifest.json |
| `provision-infra` | Provision infrastructure only |
| `diagnostics` | Show available pipeline steps |

### aspire deploy
```bash
# Deploy to Azure Container Apps
aspire deploy --publisher azure

# Deploy with prompts for configuration
aspire deploy

# Deploy specific project
aspire deploy --project ./src/MyApp.AppHost
```

### aspire publish
```bash
# Generate manifest.json
aspire publish --output-path ./publish

# Generate with specific publisher
aspire publish --publisher manifest --output-path ./publish

# Generate Kubernetes manifests
aspire publish --publisher kubernetes --output-path ./k8s
```

### aspire mcp (13.0+)
```bash
# Initialize MCP for AI assistants
aspire mcp init

# Start MCP server manually
aspire mcp start
```

See `mcp-integration.md` for detailed MCP configuration.

### aspire update
```bash
# Update packages in current project
aspire update

# Self-update the CLI
aspire update --self

# Select update channel
aspire update --self --channel preview
```

## Deployment Targets

### Azure Container Apps (Default)

```csharp
// Configure deployment target
builder.AddProject<Projects.Api>("api")
    .PublishAsAzureContainerApp((infra, app) =>
    {
        app.Template.Value!.Scale.MinReplicas = 1;
        app.Template.Value!.Scale.MaxReplicas = 10;
    });
```

```bash
# Deploy to Azure Container Apps
aspire deploy --publisher azure
```

### Docker Compose

```csharp
// Package: Aspire.Hosting.Docker
builder.AddDockerComposeEnvironment("compose");
```

```bash
# Generate and deploy with Docker Compose
aspire do prepare-compose --environment production
aspire deploy

# Clean up
aspire do docker-compose-down-compose
```

### Docker / Container Registry

```csharp
// Publish as Dockerfile
builder.AddProject<Projects.Api>("api")
    .PublishAsDockerFile();

// With custom registry
builder.AddAzureContainerRegistry("registry");
builder.AddAzureContainerAppEnvironment("env")
    .WithAzureContainerRegistry(registry);
```

### Kubernetes / Helm

```csharp
// Publish as Kubernetes resources
builder.AddProject<Projects.Api>("api")
    .PublishAsKubernetes();
```

```bash
# Generate Kubernetes manifests
aspire publish --publisher kubernetes --output-path ./k8s
```

## Manifest Format

The `manifest.json` file describes resources:

```json
{
  "resources": {
    "api": {
      "type": "project.v0",
      "path": "../Api/Api.csproj",
      "env": {
        "OTEL_DOTNET_EXPERIMENTAL_OTLP_EMIT_EXCEPTION_LOG_ATTRIBUTES": "true",
        "OTEL_DOTNET_EXPERIMENTAL_OTLP_EMIT_EVENT_LOG_ATTRIBUTES": "true"
      },
      "bindings": {
        "http": {
          "scheme": "http",
          "protocol": "tcp",
          "transport": "http"
        },
        "https": {
          "scheme": "https",
          "protocol": "tcp",
          "transport": "http"
        }
      }
    },
    "redis": {
      "type": "container.v0",
      "image": "docker.io/library/redis:7.4",
      "bindings": {
        "tcp": {
          "scheme": "tcp",
          "protocol": "tcp",
          "transport": "tcp",
          "targetPort": 6379
        }
      }
    }
  }
}
```

## Execution Context

### Check Run vs Publish Mode
```csharp
if (builder.ExecutionContext.IsRunMode)
{
    // Local development configuration
    redis.WithDataVolume();
}

if (builder.ExecutionContext.IsPublishMode)
{
    // Production configuration
    api.WithReplicas(3);
}
```

### Conditional Resources
```csharp
// Only in run mode (local dev)
if (builder.ExecutionContext.IsRunMode)
{
    builder.AddPostgres("db").WithPgAdmin();
}
```

## Azure Deployment Configuration

### Required Configuration
```json
{
  "Azure": {
    "SubscriptionId": "your-subscription-id",
    "Location": "eastus",
    "ResourceGroup": "rg-myapp",
    "AllowResourceGroupCreation": true
  }
}
```

### Or Environment Variables
```bash
export AZURE_SUBSCRIPTION_ID=...
export AZURE_LOCATION=eastus
export AZURE_RESOURCE_GROUP=rg-myapp
```

### Azure CLI Setup
```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Verify
az account show
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Deploy Aspire App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'

      - name: Install Aspire CLI
        run: dotnet tool install -g aspire

      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy
        run: aspire deploy --publisher azure
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          AZURE_LOCATION: eastus
          AZURE_RESOURCE_GROUP: rg-myapp
```

### Azure DevOps
```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UseDotNet@2
    inputs:
      version: '10.0.x'

  - script: dotnet tool install -g aspire
    displayName: 'Install Aspire CLI'

  - task: AzureCLI@2
    inputs:
      azureSubscription: 'MyAzureConnection'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        aspire deploy --publisher azure
    env:
      AZURE_LOCATION: eastus
      AZURE_RESOURCE_GROUP: rg-myapp
```

## Custom Publishers

### Create Custom Publisher (Deprecated in 13.0)
```csharp
// Note: IDistributedApplicationPublisher is deprecated
// Use PipelineStep instead for new code
public class MyCustomPublisher : IDistributedApplicationPublisher
{
    public async Task PublishAsync(
        DistributedApplicationModel model,
        CancellationToken ct)
    {
        foreach (var resource in model.Resources)
        {
            // Custom publishing logic
        }
    }
}
```

### Pipeline Steps (13.0+)
```csharp
// Modern approach using pipeline steps
builder.Services.AddPipelineStep<MyDeployStep>("my-deploy");
```

## Bicep Output

Aspire generates Bicep files for Azure resources:

```bash
# Generate Bicep
aspire publish --publisher azure --output-path ./infra

# Files generated:
# - main.bicep
# - main.parameters.json
# - <resource>.module.bicep (per resource)
```

### Customize Bicep
```csharp
builder.AddAzureStorage("storage")
    .ConfigureInfrastructure(infra =>
    {
        var storage = infra.GetProvisionableResources()
            .OfType<StorageAccount>()
            .Single();

        storage.Sku = new StorageSku(StorageSkuName.StandardGrs);
    });
```

## Single-File AppHost (13.0+)

Create a minimal AppHost without a project file:

**apphost.cs:**
```csharp
#:package Aspire.Hosting@*
#:package Aspire.Hosting.Redis@*

var builder = DistributedApplication.CreateBuilder(args);

var cache = builder.AddRedis("cache");
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(cache);

builder.Build().Run();
```

Run with:
```bash
aspire run --project ./apphost.cs
```
