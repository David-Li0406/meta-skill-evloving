# AppHost Reference

## Core Concepts

The AppHost is the orchestration entry point for Aspire applications. It defines resources, their relationships, and how they communicate.

### Basic Structure

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Define resources
var db = builder.AddPostgres("db").AddDatabase("appdata");
var api = builder.AddProject<Projects.Api>("api");
var frontend = builder.AddViteApp("frontend", "../frontend");

// Wire dependencies
api.WithReference(db).WaitFor(db);
frontend.WithReference(api);

builder.Build().Run();
```

## Resource Types

| Method | Resource Type | Description |
|--------|---------------|-------------|
| `AddProject<T>()` | .NET Project | References a .NET project |
| `AddContainer()` | Container | Generic container from image |
| `AddDockerfile()` | Dockerfile | Build from Dockerfile (see Dockerfiles section) |
| `AddExecutable()` | Executable | External executable (see Executables section) |
| `AddParameter()` | Parameter | External configuration value |
| `AddConnectionString()` | Connection | External connection string |

## API Patterns

### AddX Pattern (Create Resources)
```csharp
// Returns IResourceBuilder<TResource>
var redis = builder.AddRedis("cache");
var postgres = builder.AddPostgres("db").AddDatabase("mydb");
var api = builder.AddProject<Projects.Api>("api");
```

### WithX Pattern (Configure Resources)
```csharp
builder.AddProject<Projects.Api>("api")
    .WithReference(db)           // Inject connection string
    .WithEnvironment("KEY", val) // Add env var
    .WithEndpoint(port: 8080)    // Expose endpoint
    .WithReplicas(3)             // Scale replicas
    .WaitFor(db);                // Startup ordering
```

## Dependency Wiring

### WithReference - Connection Injection
```csharp
var db = builder.AddPostgres("db").AddDatabase("appdata");
var cache = builder.AddRedis("cache");

// Injects ConnectionStrings__appdata and ConnectionStrings__cache
builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WithReference(cache);
```

### WaitFor - Startup Ordering
```csharp
// WaitFor: waits for resource to be running
api.WaitFor(db);

// WaitForHealthy: waits for health check to pass (requires health check)
api.WaitForHealthy(cache);

// WaitForCompletion: waits for resource to complete (jobs)
api.WaitForCompletion(migration);
```

### HTTP Health Probes (Kubernetes-Style)

Configure startup, readiness, and liveness probes for Kubernetes deployments:

```csharp
// Single probe
var api = builder.AddProject<Projects.Api>("api")
    .WithHttpProbe(ProbeType.Readiness, "/health/ready");

// Multiple probes with custom settings
var service = builder.AddProject<Projects.Service>("service")
    .WithHttpProbe(ProbeType.Startup, "/health/startup",
        initialDelaySeconds: 15, failureThreshold: 10)
    .WithHttpProbe(ProbeType.Readiness, "/health/ready",
        periodSeconds: 5, timeoutSeconds: 3)
    .WithHttpProbe(ProbeType.Liveness, "/health/live",
        periodSeconds: 30, failureThreshold: 3);
```

| Probe Type | Purpose | When It Runs |
|------------|---------|--------------|
| `ProbeType.Startup` | Detect slow-starting containers | During startup only |
| `ProbeType.Readiness` | Control traffic routing | Continuously after startup |
| `ProbeType.Liveness` | Detect hung processes | Continuously after startup |

**Target specific endpoint:**
```csharp
// Probe a named endpoint (e.g., management port)
var api = builder.AddProject<Projects.Api>("api")
    .WithHttpEndpoint(8080, name: "management")
    .WithHttpProbe(ProbeType.Readiness, "/actuator/health",
        endpointName: "management");
```

> **Note:** `WithHttpProbe` is in preview. Suppress warnings with:
> ```csharp
> #pragma warning disable ASPIREPROBES001
> .WithHttpProbe(ProbeType.Readiness, "/health/ready")
> #pragma warning restore ASPIREPROBES001
> ```

## Environment Variables

### Static Values
```csharp
.WithEnvironment("DEBUG", "true")
.WithEnvironment("LOG_LEVEL", "info")
```

### Dynamic Values (Callback)
```csharp
.WithEnvironment(context =>
{
    context.EnvironmentVariables["COMPUTED"] = ComputeValue();
})
```

### From Endpoints
```csharp
var api = builder.AddProject<Projects.Api>("api");
builder.AddProject<Projects.Web>("web")
    .WithEnvironment("API_URL", api.GetEndpoint("http"));
```

### From Parameters
```csharp
var secret = builder.AddParameter("api-key", secret: true);
builder.AddProject<Projects.Api>("api")
    .WithEnvironment("API_KEY", secret);
```

## Endpoints and Networking

### Define Endpoints
```csharp
// HTTP endpoint with specific port
.WithHttpEndpoint(port: 5000)

// HTTPS endpoint
.WithHttpsEndpoint(port: 5001)

// Named endpoint
.WithHttpEndpoint(port: 8080, name: "admin")

// Container port mapping (host:container)
.WithHttpEndpoint(port: 8000, targetPort: 8080)

// Environment variable for port
.WithHttpEndpoint(env: "PORT")
```

### Endpoint Configuration
```csharp
.WithEndpoint(endpointName: "grpc", callback: endpoint =>
{
    endpoint.Port = 5000;
    endpoint.UriScheme = "http";
    endpoint.Transport = "http2";
})
```

### External Endpoints (Dashboard Access)
```csharp
.WithExternalHttpEndpoints()  // Expose HTTP endpoints externally
```

### Custom URLs
```csharp
// Add custom URL to dashboard
api.WithUrl("/swagger", "Swagger UI");
api.WithUrlForEndpoint("https", url => {
    url.DisplayText = "Admin Portal";
    url.Url = "/admin";
});
```

## Parameters and Secrets

### Define Parameters
```csharp
// Regular parameter (non-sensitive)
var rows = builder.AddParameter("insertion-rows");

// Secret parameter (sensitive)
var apiKey = builder.AddParameter("api-key", secret: true);
```

### Where to Store Values

**Regular parameters** → `appsettings.json`:
```json
{
  "Parameters": {
    "insertion-rows": "100"
  }
}
```

**Secret parameters** → User Secrets (**NEVER appsettings.json**):
```bash
# Initialize user secrets (once per project)
dotnet user-secrets init

# Set the secret value
dotnet user-secrets set "Parameters:api-key" "my-secret-key"
```

> **WARNING:** Never put secret values in `appsettings.json`. This file is committed to source control. Use `dotnet user-secrets` for development and Azure Key Vault or environment variables for production.

### Pass Parameters to Resources
```csharp
var secret = builder.AddParameter("api-key", secret: true);
var rows = builder.AddParameter("max-rows");

builder.AddUvicornApp("api", "../api", "main:app")
    .WithEnvironment("API_KEY", secret)      // Secret as env var
    .WithEnvironment("MAX_ROWS", rows);       // Regular param as env var
```

### Connection String Parameters
```csharp
// External connection string from config
var redis = builder.AddConnectionString("redis");

// Composed connection string
var secret = builder.AddParameter("key", secret: true);
var conn = builder.AddConnectionString("api",
    ReferenceExpression.Create($"Endpoint=https://api.com;Key={secret}"));
```

## Volumes and Data Persistence

### Data Volumes (Recommended)
```csharp
// Auto-named volume
builder.AddPostgres("db").WithDataVolume();

// Custom volume
builder.AddSqlServer("sql")
    .WithVolume(name: "sql-data", target: "/var/opt/mssql");
```

### Bind Mounts
```csharp
builder.AddPostgres("db")
    .WithDataBindMount(source: @"C:\Data\postgres");
```

### Persistent Passwords
```bash
# Set persistent password in user secrets
dotnet user-secrets set Parameters:db-password "my-password"
```

```csharp
var password = builder.AddParameter("db-password", secret: true);
builder.AddPostgres("db", password: password).WithDataVolume();
```

## Lifecycle Events

### AppHost Events (Order)
1. `BeforeStartEvent` - Before AppHost starts
2. `ResourceEndpointsAllocatedEvent` - Per resource, after endpoints allocated
3. `AfterResourcesCreatedEvent` - After all resources created

### Subscribe to Events
```csharp
builder.Eventing.Subscribe<BeforeStartEvent>((@event, ct) =>
{
    var logger = @event.Services.GetRequiredService<ILogger<Program>>();
    logger.LogInformation("Starting...");
    return Task.CompletedTask;
});
```

### Resource Events (Order)
1. `InitializeResourceEvent` - Resource initialization
2. `ResourceEndpointsAllocatedEvent` - Endpoints allocated
3. `ConnectionStringAvailableEvent` - Connection string ready
4. `BeforeResourceStartedEvent` - Before resource starts
5. `ResourceReadyEvent` - Resource is ready

### Subscribe to Resource Events
```csharp
var cache = builder.AddRedis("cache");

cache.OnResourceReady((resource, @event, ct) =>
{
    // Cache is ready
    return Task.CompletedTask;
});

cache.OnBeforeResourceStarted((resource, @event, ct) =>
{
    // About to start
    return Task.CompletedTask;
});
```

### Lifecycle Hook Interface
```csharp
builder.Services.AddLifecycleHook<MyLifecycleHook>();

class MyLifecycleHook : IDistributedApplicationLifecycleHook
{
    public Task BeforeStartAsync(DistributedApplicationModel appModel, CancellationToken ct)
    {
        // Before start
        return Task.CompletedTask;
    }

    public Task AfterEndpointsAllocatedAsync(DistributedApplicationModel appModel, CancellationToken ct)
    {
        // After endpoints allocated
        return Task.CompletedTask;
    }

    public Task AfterResourcesCreatedAsync(DistributedApplicationModel appModel, CancellationToken ct)
    {
        // After resources created
        return Task.CompletedTask;
    }
}
```

## Container Lifetime

### Persistent Containers
```csharp
// Container persists across AppHost restarts
builder.AddRedis("cache")
    .WithLifetime(ContainerLifetime.Persistent);
```

## Execution Context

### Check Run vs Publish Mode
```csharp
if (builder.ExecutionContext.IsRunMode)
{
    // Local development
}

if (builder.ExecutionContext.IsPublishMode)
{
    // Publishing/deployment
}
```

## Common Patterns

### Full Stack Example
```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Infrastructure
var db = builder.AddPostgres("db")
    .WithDataVolume()
    .AddDatabase("appdata");

var cache = builder.AddRedis("cache")
    .WithLifetime(ContainerLifetime.Persistent);

// Backend
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WithReference(cache)
    .WaitFor(db)
    .WaitFor(cache);

// Frontend
builder.AddViteApp("frontend", "../frontend")
    .WithHttpEndpoint(env: "PORT")
    .WithReference(api)
    .WaitFor(api);

builder.Build().Run();
```

### Microservices Pattern
```csharp
var messaging = builder.AddRabbitMQ("messaging");

var orderService = builder.AddProject<Projects.Orders>("orders")
    .WithReference(messaging);

var inventoryService = builder.AddProject<Projects.Inventory>("inventory")
    .WithReference(messaging);

var gateway = builder.AddProject<Projects.Gateway>("gateway")
    .WithReference(orderService)
    .WithReference(inventoryService);
```

## Executables (AddExecutable)

Run external executables (Python scripts, Go binaries, etc.) as Aspire resources:

```csharp
// Basic executable
builder.AddExecutable("processor", "python", workingDirectory: "../scripts", "process_data.py");

// With arguments
builder.AddExecutable("worker", "python", "../scripts", "worker.py", "--mode", "production");

// With dependencies
var redis = builder.AddRedis("cache");
builder.AddExecutable("processor", "python", "../scripts", "process.py")
    .WithReference(redis)  // Injects ConnectionStrings__cache
    .WithEnvironment("LOG_LEVEL", "debug");

// With HTTP endpoint (if it exposes a server)
builder.AddExecutable("api", "python", "../api", "server.py")
    .WithHttpEndpoint(port: 8000, env: "PORT")
    .WithReference(db);
```

## Dockerfiles

### AddDockerfile - New Container from Dockerfile
```csharp
// Build container from Dockerfile in directory
builder.AddDockerfile("goservice", "./go-service");

// Specify custom Dockerfile name
builder.AddDockerfile("service", "./path", "Dockerfile.custom");

// With dependencies and endpoints
var db = builder.AddPostgres("db").AddDatabase("appdata");
builder.AddDockerfile("goservice", "./go-service")
    .WithReference(db)
    .WithHttpEndpoint(port: 8080);
```

### WithDockerfile - Customize Existing Resource
Use a custom Dockerfile while keeping resource-specific extension methods:

```csharp
// Use custom Postgres image with PostGIS extensions
builder.AddPostgres("db")
    .WithDockerfile("./postgres-postgis")  // Path to directory with Dockerfile
    .AddDatabase("geodata");

// Still has all PostgreSQL methods available
builder.AddPostgres("db")
    .WithDockerfile("./custom-postgres")
    .WithDataVolume()
    .WithPgAdmin();
```

**Key difference:**
- `AddDockerfile()` - Creates new generic container resource
- `WithDockerfile()` - Customizes image for existing typed resource (keeps extension methods)

## Bind Mounts

Mount local files or directories into containers:

```csharp
// Mount single file
builder.AddContainer("nginx", "nginx:latest")
    .WithBindMount("./nginx.conf", "/etc/nginx/nginx.conf");

// Mount directory
builder.AddContainer("nginx", "nginx:latest")
    .WithBindMount("./html", "/usr/share/nginx/html");

// Read-only mount
builder.AddContainer("app", "myapp:latest")
    .WithBindMount("./config", "/app/config", isReadOnly: true);

// Multiple mounts
builder.AddContainer("nginx", "nginx:latest")
    .WithBindMount("./nginx.conf", "/etc/nginx/nginx.conf", isReadOnly: true)
    .WithBindMount("./html", "/usr/share/nginx/html", isReadOnly: true)
    .WithBindMount("./logs", "/var/log/nginx");  // Writable for logs
```

**Note:** Bind mounts use host paths. For named Docker volumes, use `WithVolume()` instead.

## Replicas and Proxy Behavior

### WithReplicas
```csharp
// Run 3 instances of the API
builder.AddProject<Projects.Api>("api")
    .WithReplicas(3);
```

**How it works:**
- Aspire creates a **proxy** on the specified port
- Each replica gets a **randomly assigned** port
- Other services using `WithReference(api)` get the **proxy URL**, not individual replicas
- Proxy handles load balancing between replicas
- Dashboard shows replicas nested under the parent resource

### Endpoint Proxy Behavior (IsProxied)

By default, Aspire proxies endpoints. For executables that manage their own ports:

```csharp
// Problem: App listens on 3000, but not accessible on that port
builder.AddExecutable("app", "node", "../app", "server.js")
    .WithHttpEndpoint(port: 3000);  // Port 3000 is for PROXY, not app!

// Solution 1: Disable proxy
builder.AddExecutable("app", "node", "../app", "server.js")
    .WithEndpoint("http", endpoint =>
    {
        endpoint.Port = 3000;
        endpoint.IsProxied = false;  // App manages its own port
    });

// Solution 2: Use environment variable for dynamic port
builder.AddExecutable("app", "node", "../app", "server.js")
    .WithHttpEndpoint(env: "PORT");  // App reads PORT env var
```

**When to disable proxy:**
- External executables with hardcoded ports
- Apps that don't read port from environment
- When you need the exact port the app binds to

## WaitForCompletion (Job/Migration Pattern)

For containers that should run once and exit (migrations, seed scripts, init jobs):

```csharp
// Migration container runs EF Core migrations
var migration = builder.AddDockerfile("migration", "./migrations")
    .WithReference(db);

// API waits for migration to COMPLETE (exit successfully), not just start
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WaitForCompletion(migration);  // Not WaitFor!
```

**Key difference:**
- `WaitFor(resource)` - Waits for resource to reach **Running** state
- `WaitForCompletion(resource)` - Waits for resource to **exit successfully**

Use `WaitForCompletion` for:
- Database migrations
- Seed data scripts
- Init containers
- One-time setup jobs

## Custom Dashboard Commands (WithCommand)

Add custom commands to resources that appear in the Aspire dashboard:

```csharp
var redis = builder.AddRedis("cache")
    .WithCommand("clear-cache", "Clear All Keys", async context =>
    {
        var connectionString = await context.Resource.GetConnectionStringAsync();
        // Use connection string to clear cache
        using var redis = ConnectionMultiplexer.Connect(connectionString!);
        var server = redis.GetServer(redis.GetEndPoints().First());
        await server.FlushAllDatabasesAsync();
        return CommandResults.Success("Cache cleared");
    });
```

Commands appear in the dashboard resource actions menu.

### Custom HTTP Commands (WithHttpCommand)

For commands that need to call HTTP endpoints on resources (like cache invalidation), use `WithHttpCommand`:

```csharp
var apiCacheInvalidationKey = builder.AddParameter("ApiCacheInvalidationKey", secret: true);

var api = builder.AddProject<Projects.Api>("api")
    .WithEnvironment("ApiCacheInvalidationKey", apiCacheInvalidationKey)
    .WithHttpCommand(
        path: "/cache/invalidate",
        displayName: "Invalidate cache",
        commandOptions: new HttpCommandOptions()
        {
            Description = "Invalidates the API cache. All cached values are cleared!",
            PrepareRequest = (context) =>
            {
                var key = apiCacheInvalidationKey.Resource.GetValueAsync(context.CancellationToken);
                context.Request.Headers.Add("X-CacheInvalidation-Key", $"Key: {key}");
                return Task.CompletedTask;
            },
            IconName = "DocumentLightning",
            IsHighlighted = true
        });
```

**Key difference:**
- `WithCommand()` - Execute custom code in the AppHost process
- `WithHttpCommand()` - Send HTTP request to resource's endpoint (requires endpoint to handle it)

**HttpCommandOptions properties:**
| Property | Description |
|----------|-------------|
| `Description` | Shown in dashboard UI |
| `PrepareRequest` | Callback to configure request headers (e.g., auth tokens) |
| `IconName` | Fluent UI icon name |
| `IsHighlighted` | Show prominently in UI |

**Security:** Use `PrepareRequest` to add authentication headers with shared secrets from parameters. The endpoint should validate these to prevent unauthorized access.

## Container Runtime Arguments

Pass Docker-specific flags (not container entrypoint args):

```csharp
// Resource limits
builder.AddContainer("app", "myapp:latest")
    .WithContainerRuntimeArgs("--memory=512m", "--cpus=2");

// Security options
builder.AddContainer("app", "myapp:latest")
    .WithContainerRuntimeArgs("--cap-drop=ALL", "--read-only");

// Network mode
builder.AddContainer("app", "myapp:latest")
    .WithContainerRuntimeArgs("--network=host");
```

**Key difference:**
- `WithArgs()` - Arguments passed to the container's **entrypoint/command**
- `WithContainerRuntimeArgs()` - Arguments passed to **Docker runtime** (`docker run`)
