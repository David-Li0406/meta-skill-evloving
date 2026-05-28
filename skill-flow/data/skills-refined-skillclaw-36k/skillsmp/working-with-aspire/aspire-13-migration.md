# Aspire 13 Migration Guide

## Overview

Aspire 13.0 is a major release with significant changes. The framework has been rebranded from ".NET Aspire" to simply "Aspire" to reflect its polyglot nature.

**Requirements:** .NET 10 SDK or later

## Upgrade Methods

### Using Aspire CLI (Recommended)

```bash
# Update CLI first
aspire update --self

# Update project packages
aspire update
```

### From Aspire 8.x

If upgrading from Aspire 8.x, first upgrade to 9.x, then to 13.0:

```bash
# Remove legacy workload
dotnet workload uninstall aspire
```

### Manual Upgrade

Update your AppHost project file:

```xml
<!-- Before (9.x) -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Aspire.Hosting.AppHost" Version="9.*" />
  </ItemGroup>
</Project>

<!-- After (13.0) -->
<Project Sdk="Aspire.AppHost.Sdk/13.0.0">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```

## Breaking Changes in 13.0

### Network Context Changes

**`containerHostName` parameter removed:**

```csharp
// Before (9.x)
await resource.ProcessArgumentValuesAsync(
    executionContext, processValue, logger,
    containerHostName: "localhost", cancellationToken);

// After (13.0)
await resource.ProcessArgumentValuesAsync(
    executionContext, processValue, logger, cancellationToken);
```

**Use `NetworkIdentifier` instead:**

```csharp
var builder = DistributedApplication.CreateBuilder(args);

var api = builder.AddProject<Projects.Api>("api");

// Get endpoint with specific network context
var localhostEndpoint = api.GetEndpoint("http", KnownNetworkIdentifiers.LocalhostNetwork);
var containerEndpoint = api.GetEndpoint("http", KnownNetworkIdentifiers.DefaultAspireContainerNetwork);
```

**`AllocatedEndpoint` constructor changed:**

```csharp
// Before (9.x)
var endpoint = new AllocatedEndpoint(
    endpointAnnotation, "http", 8080);

// After (13.0)
var endpoint = new AllocatedEndpoint(
    endpointAnnotation, "http", 8080,
    networkIdentifier: KnownNetworkIdentifiers.LocalhostNetwork);
```

### JavaScript/Node.js API Changes

**`AddNpmApp` removed - use `AddJavaScriptApp`:**

```csharp
// Before (9.x) - REMOVED
builder.AddNpmApp("frontend", "../app", scriptName: "dev", args: ["--no-open"]);

// After (13.0) - Option 1: WithArgs
builder.AddJavaScriptApp("frontend", "../app")
    .WithRunScript("dev")
    .WithArgs("--no-open");

// After (13.0) - Option 2: package.json script
// Define in package.json: "dev:custom": "vite --no-open"
builder.AddJavaScriptApp("frontend", "../app")
    .WithRunScript("dev:custom");
```

**Package renamed:**

```csharp
// Before (9.x)
// Package: Aspire.Hosting.NodeJs

// After (13.0)
// Package: Aspire.Hosting.JavaScript
```

### Azure Credential Behavior Change

**`DefaultAzureCredential` now defaults to `ManagedIdentityCredential`** on Azure Container Apps and App Service.

If you rely on other credential types in these environments, explicitly configure them:

```csharp
builder.Services.AddAzureClients(clients =>
{
    clients.UseCredential(new DefaultAzureCredential(new DefaultAzureCredentialOptions
    {
        ExcludeManagedIdentityCredential = true // If needed
    }));
});
```

### Publishing API Changes

**`IDistributedApplicationPublisher` deprecated:**

```csharp
// Before (9.x)
public class MyPublisher : IDistributedApplicationPublisher { }
builder.Services.AddKeyedSingleton<IDistributedApplicationPublisher, MyPublisher>("my");

// After (13.0) - Use PipelineStep
public class MyDeployStep : PipelineStep { }
```

### Lifecycle Hook Changes

```csharp
// Before (9.x)
builder.Services.AddLifecycleHook<MyHook>();
builder.Services.TryAddLifecycleHook<MyHook>();

// After (13.0)
builder.Services.AddEventingSubscriber<MySubscriber>();
builder.Services.TryAddEventingSubscriber<MySubscriber>();
```

## Breaking Changes in 13.1

### Azure Redis API Rename

```csharp
// Before (13.0) - DEPRECATED
var redis = builder.AddAzureRedisEnterprise("cache");

// After (13.1)
var redis = builder.AddAzureManagedRedis("cache");
```

**Note:** `AddAzureRedis` is now obsolete. Use `AddAzureManagedRedis` for new projects.

## Migration Checklist

### From 9.x to 13.0

- [ ] Install .NET 10 SDK
- [ ] Update AppHost SDK: `Aspire.AppHost.Sdk/13.0.0`
- [ ] Update `TargetFramework` to `net10.0`
- [ ] Replace `AddNpmApp` with `AddJavaScriptApp`
- [ ] Update `Aspire.Hosting.NodeJs` to `Aspire.Hosting.JavaScript`
- [ ] Replace `containerHostName` with `NetworkIdentifier`
- [ ] Update `AllocatedEndpoint` constructors
- [ ] Replace `IDistributedApplicationPublisher` with `PipelineStep`
- [ ] Replace lifecycle hooks with eventing subscribers
- [ ] Test Azure credential behavior in cloud environments

### From 13.0 to 13.1

- [ ] Run `aspire update --self`
- [ ] Run `aspire update` in project directory
- [ ] Replace `AddAzureRedisEnterprise` with `AddAzureManagedRedis`
- [ ] Run `aspire mcp init` to set up AI coding agent support

## New Features to Adopt

### Polyglot Improvements

```csharp
// Unified JavaScript method
var frontend = builder.AddJavaScriptApp("frontend", "./frontend")
    .WithYarn()  // or WithPnpm()
    .WithRunScript("dev")
    .WithBuildScript("build");
```

### Certificate Trust Automation

```csharp
// Automatic certificate trust (no configuration needed)
var pythonApi = builder.AddUvicornApp("api", "./api", "main:app");
var nodeApi = builder.AddJavaScriptApp("frontend", "./frontend");
var container = builder.AddContainer("service", "myimage");
// All automatically trust development certificates
```

### MCP Integration

```bash
# Set up AI assistant integration
aspire mcp init
```

### Pipeline System

```bash
# Use aspire do for granular control
aspire do build
aspire do push
aspire do deploy-apiservice
```

## Troubleshooting Migration

### "Package not found" errors

Ensure you've updated package names:
- `Aspire.Hosting.NodeJs` → `Aspire.Hosting.JavaScript`

### "Method not found" errors

Check for removed APIs:
- `AddNpmApp` → `AddJavaScriptApp`
- `containerHostName` parameter → `NetworkIdentifier`

### Container networking issues

If containers can't communicate:
```csharp
// Use network identifiers explicitly
var endpoint = api.GetEndpoint("http", KnownNetworkIdentifiers.DefaultAspireContainerNetwork);
builder.AddProject<Projects.Worker>("worker")
    .WithEnvironment("API_URL", endpoint);
```

### Azure authentication failures

If Azure resources fail in cloud:
```csharp
// Check DefaultAzureCredential behavior change
// May need to explicitly configure credential options
```

## Resources

- [Official Upgrade Guide](https://learn.microsoft.com/dotnet/aspire/get-started/upgrade-to-aspire-13)
- [Breaking Changes Reference](https://learn.microsoft.com/dotnet/aspire/compatibility/13.0/)
- [What's New in Aspire 13](https://aspire.dev/whats-new/aspire-13/)
- [What's New in Aspire 13.1](https://aspire.dev/whats-new/aspire-13-1/)
