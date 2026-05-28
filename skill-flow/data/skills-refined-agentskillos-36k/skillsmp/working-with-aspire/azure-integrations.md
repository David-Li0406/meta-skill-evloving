# Azure Integrations Reference

## Overview

Azure integrations in Aspire provide two main capabilities:
1. **Hosting integrations**: Model Azure resources in AppHost for local dev and deployment
2. **Client integrations**: Configure .NET clients with proper defaults

## Local Development Patterns

### Emulators vs Containers vs Real Azure

| Pattern | API | Use Case |
|---------|-----|----------|
| Real Azure | `AddAzure*()` | Test with actual Azure services |
| Emulator | `.RunAsEmulator()` | Official Azure emulators |
| Container | `.RunAsContainer()` | Open-source container alternatives |

### Emulator Support

```csharp
// Cosmos DB Emulator
builder.AddAzureCosmosDB("cosmos").RunAsEmulator();

// Service Bus Emulator
builder.AddAzureServiceBus("messaging").RunAsEmulator();

// Event Hubs Emulator
builder.AddAzureEventHubs("events").RunAsEmulator();

// Storage (Azurite)
builder.AddAzureStorage("storage").RunAsEmulator();

// App Configuration Emulator
builder.AddAzureAppConfiguration("config").RunAsEmulator();

// SignalR Emulator
builder.AddAzureSignalR("signalr").RunAsEmulator();

// AI Foundry Local
builder.AddAzureAIFoundry("ai").RunAsFoundryLocal();
```

### Container Substitution

```csharp
// Azure Cache for Redis → Local Redis container
builder.AddAzureRedis("cache").RunAsContainer();

// Azure PostgreSQL → Local PostgreSQL container
builder.AddAzurePostgresFlexibleServer("db").RunAsContainer();

// Azure SQL → Local SQL Server container
builder.AddAzureSqlServer("sql").RunAsContainer();
```

### Run vs Publish Behavior

| API | Local (Run) | Deploy (Publish) |
|-----|-------------|------------------|
| `AddAzureRedis("r").RunAsContainer()` | Redis container | Azure Cache for Redis |
| `AddRedis("r")` | Redis container | Container App with Redis |
| `AddAzurePostgresFlexibleServer("p").RunAsContainer()` | PostgreSQL container | Azure PostgreSQL Flexible |
| `AddPostgres("p")` | PostgreSQL container | Container App with PostgreSQL |

## Existing Resources

### Use Existing in All Modes
```csharp
var nameParam = builder.AddParameter("cosmosName");
var rgParam = builder.AddParameter("resourceGroup");

builder.AddAzureCosmosDB("cosmos")
    .AsExisting(nameParam, rgParam);
```

### Use Existing in Run Mode Only
```csharp
builder.AddAzureServiceBus("messaging")
    .RunAsExisting(nameParam, rgParam);
```

### Use Existing in Publish Mode Only
```csharp
builder.AddAzureServiceBus("messaging")
    .PublishAsExisting(nameParam, rgParam);
```

## Common Azure Services

### Azure Cosmos DB

```csharp
// Package: Aspire.Hosting.Azure.CosmosDB

// Provision new
var cosmos = builder.AddAzureCosmosDB("cosmos");
var db = cosmos.AddCosmosDatabase("mydb");
var container = db.AddCosmosContainer("items", "/partitionKey");

// With emulator
var cosmos = builder.AddAzureCosmosDB("cosmos")
    .RunAsEmulator();

// Reference in project
builder.AddProject<Projects.Api>("api")
    .WithReference(cosmos);
```

**Client Integration:**
```csharp
// Package: Aspire.Microsoft.Azure.Cosmos
builder.AddAzureCosmosClient("cosmos");
```

### Azure Service Bus

```csharp
// Package: Aspire.Hosting.Azure.ServiceBus

var serviceBus = builder.AddAzureServiceBus("messaging");

// Add queue
serviceBus.AddServiceBusQueue("orders");

// Add topic with subscription
var topic = serviceBus.AddServiceBusTopic("notifications");
topic.AddServiceBusSubscription("email-handler");

// With emulator
builder.AddAzureServiceBus("messaging")
    .RunAsEmulator();
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.Messaging.ServiceBus
builder.AddAzureServiceBusClient("messaging");
```

### Azure Storage

```csharp
// Package: Aspire.Hosting.Azure.Storage

var storage = builder.AddAzureStorage("storage");
var blobs = storage.AddBlobs("blobs");
var queues = storage.AddQueues("queues");
var tables = storage.AddTables("tables");

// With Azurite emulator
builder.AddAzureStorage("storage")
    .RunAsEmulator();
```

**Client Integrations:**
```csharp
// Package: Aspire.Azure.Storage.Blobs
builder.AddAzureBlobClient("blobs");

// Package: Aspire.Azure.Storage.Queues
builder.AddAzureQueueClient("queues");

// Package: Aspire.Azure.Data.Tables
builder.AddAzureTableClient("tables");
```

### Azure Event Hubs

```csharp
// Package: Aspire.Hosting.Azure.EventHubs

var eventHubs = builder.AddAzureEventHubs("events");
eventHubs.AddEventHub("telemetry");

// With emulator
builder.AddAzureEventHubs("events")
    .RunAsEmulator();
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.Messaging.EventHubs
builder.AddAzureEventHubProducerClient("events", "telemetry");
builder.AddAzureEventHubConsumerClient("events", "telemetry");
```

### Azure Key Vault

```csharp
// Package: Aspire.Hosting.Azure.KeyVault

var keyVault = builder.AddAzureKeyVault("secrets");

builder.AddProject<Projects.Api>("api")
    .WithReference(keyVault);
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.Security.KeyVault
builder.AddAzureKeyVaultClient("secrets");
```

### Azure PostgreSQL Flexible Server

```csharp
// Package: Aspire.Hosting.Azure.PostgreSQL

var postgres = builder.AddAzurePostgresFlexibleServer("pg")
    .AddDatabase("mydb");

// Run as container locally
builder.AddAzurePostgresFlexibleServer("pg")
    .RunAsContainer()
    .AddDatabase("mydb");
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.Npgsql
builder.AddAzureNpgsqlDataSource("mydb");
```

### Azure SQL Database

```csharp
// Package: Aspire.Hosting.Azure.Sql

var sql = builder.AddAzureSqlServer("sql")
    .AddDatabase("mydb");

// Run as container locally
builder.AddAzureSqlServer("sql")
    .RunAsContainer()
    .AddDatabase("mydb");
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.Data.SqlClient
builder.AddAzureSqlClient("mydb");
```

### Azure Managed Redis (13.1+)

```csharp
// Package: Aspire.Hosting.Azure.Redis

// New API (13.1+)
var redis = builder.AddAzureManagedRedis("cache");

// Run as container locally
builder.AddAzureManagedRedis("cache")
    .RunAsContainer();
```

**Migration from older APIs:**
```csharp
// Before (13.0) - DEPRECATED
var redis = builder.AddAzureRedisEnterprise("cache");

// Before - OBSOLETE
var redis = builder.AddAzureRedis("cache");

// After (13.1+)
var redis = builder.AddAzureManagedRedis("cache");
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.StackExchange.Redis
builder.AddAzureRedisClient("cache");
```

### Azure OpenAI

```csharp
// Package: Aspire.Hosting.Azure.CognitiveServices

var openai = builder.AddAzureOpenAI("openai");
openai.AddDeployment(new("gpt-4o", "gpt-4o", "2024-08-06"));

builder.AddProject<Projects.Api>("api")
    .WithReference(openai);
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.AI.OpenAI
builder.AddAzureOpenAIClient("openai");
```

### Azure App Configuration

```csharp
// Package: Aspire.Hosting.Azure.AppConfiguration

var config = builder.AddAzureAppConfiguration("config");

// With emulator
builder.AddAzureAppConfiguration("config")
    .RunAsEmulator();
```

**Client Integration:**
```csharp
// Package: Aspire.Azure.AppConfiguration
builder.AddAzureAppConfigurationClient("config");
```

### Azure SignalR

```csharp
// Package: Aspire.Hosting.Azure.SignalR

var signalr = builder.AddAzureSignalR("signalr");

// With emulator
builder.AddAzureSignalR("signalr")
    .RunAsEmulator();
```

### Azure Functions

```csharp
// Package: Aspire.Hosting.Azure.Functions

builder.AddAzureFunctionsProject<Projects.MyFunctions>("functions")
    .WithReference(storage)
    .WithReference(serviceBus);
```

## Customizing Azure Resources

### Configure Infrastructure
```csharp
builder.AddAzureStorage("storage")
    .ConfigureInfrastructure(infra =>
    {
        var storageAccount = infra.GetProvisionableResources()
            .OfType<StorageAccount>()
            .Single();
        
        storageAccount.Sku = new StorageSku(StorageSkuName.StandardGrs);
        storageAccount.Tags.Add("Environment", "Production");
    });
```

### Role Assignments
```csharp
var storage = builder.AddAzureStorage("storage");

builder.AddProject<Projects.Api>("api")
    .WithRoleAssignments(storage, StorageBuiltInRole.StorageBlobDataContributor);
```

## Container App Environment

```csharp
// Configure Azure Container Apps deployment
var acr = builder.AddAzureContainerRegistry("registry");

builder.AddAzureContainerAppEnvironment("env")
    .WithAzureContainerRegistry(acr);

builder.AddProject<Projects.Api>("api")
    .PublishAsAzureContainerApp();
```

## Local Provisioning Configuration

Required in `appsettings.json` for real Azure resources:
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

Or via environment variables:
```bash
AZURE_SUBSCRIPTION_ID=...
AZURE_LOCATION=eastus
AZURE_RESOURCE_GROUP=rg-myapp
```

## Troubleshooting

### Authentication Failures
```bash
az login
az account set --subscription "your-subscription-id"
```

### Enable Debug Logging
```json
{
  "Logging": {
    "LogLevel": {
      "Aspire.Hosting.Azure": "Debug"
    }
  }
}
```

### Common Issues
- **Missing configuration**: Ensure `SubscriptionId`, `Location`, `ResourceGroup` are set
- **Insufficient permissions**: Need Contributor role on resource group
- **Emulator not starting**: Check Docker is running and port conflicts
