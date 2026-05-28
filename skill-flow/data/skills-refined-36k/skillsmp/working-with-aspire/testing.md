# Testing with Aspire Reference

## Package Installation

```bash
dotnet add package Aspire.Hosting.Testing
```

## Basic Integration Test

```csharp
using Aspire.Hosting.Testing;

public class IntegrationTests
{
    [Fact]
    public async Task GetWebResourceRootReturnsOkStatusCode()
    {
        // Arrange
        var appHost = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.MyApp_AppHost>();

        appHost.Services.ConfigureHttpClientDefaults(clientBuilder =>
        {
            clientBuilder.AddStandardResilienceHandler();
        });

        await using var app = await appHost.BuildAsync();
        var resourceNotificationService = app.Services
            .GetRequiredService<ResourceNotificationService>();

        await app.StartAsync();

        // Act
        var httpClient = app.CreateHttpClient("webfrontend");
        await resourceNotificationService
            .WaitForResourceAsync("webfrontend", KnownResourceStates.Running)
            .WaitAsync(TimeSpan.FromSeconds(30));

        var response = await httpClient.GetAsync("/");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

## Test Project Setup

### Project File
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <IsAspireHost>true</IsAspireHost>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Aspire.Hosting.Testing" Version="*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="*" />
    <PackageReference Include="xunit" Version="*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="*" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\MyApp.AppHost\MyApp.AppHost.csproj" />
  </ItemGroup>
</Project>
```

## DistributedApplicationTestingBuilder

### Create Test Builder
```csharp
// Reference AppHost project
var appHost = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.MyApp_AppHost>();

// With arguments (flows to .NET configuration system)
var appHost = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.MyApp_AppHost>(
    [
        "--environment=Testing",
        "UseVolumes=false"
    ]);
```

### Passing Arguments to Disable Volumes
```csharp
// In test: disable volumes via arguments
using var builder = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.AppHost>(["UseVolumes=false"]);

// In AppHost: read from configuration
var builder = DistributedApplication.CreateBuilder(args);
var useVolumes = builder.Configuration["UseVolumes"] != "false";

var postgres = builder.AddPostgres("db");
if (useVolumes)
{
    postgres.WithDataVolume();
}
```

### Configure Services
```csharp
appHost.Services.AddHttpClient();

appHost.Services.ConfigureHttpClientDefaults(clientBuilder =>
{
    clientBuilder.AddStandardResilienceHandler();
});
```

### Build and Start
```csharp
await using var app = await appHost.BuildAsync();
await app.StartAsync();
```

## Creating HTTP Clients

### Get Client for Resource
```csharp
// Create client for specific resource
var httpClient = app.CreateHttpClient("api");

// Make requests
var response = await httpClient.GetAsync("/health");
```

### Get Connection String
```csharp
// Get connection string for resource
var connectionString = await app.GetConnectionStringAsync("db");
```

## Waiting for Resources

### Wait for Running State
```csharp
var resourceNotificationService = app.Services
    .GetRequiredService<ResourceNotificationService>();

await resourceNotificationService
    .WaitForResourceAsync("api", KnownResourceStates.Running)
    .WaitAsync(TimeSpan.FromSeconds(60));
```

### Wait for Healthy State
```csharp
await resourceNotificationService
    .WaitForResourceHealthyAsync("api")
    .WaitAsync(TimeSpan.FromSeconds(60));
```

### Known Resource States
```csharp
KnownResourceStates.Running
KnownResourceStates.Finished
KnownResourceStates.FailedToStart
KnownResourceStates.Exited
KnownResourceStates.Starting
KnownResourceStates.Stopping
KnownResourceStates.Waiting
KnownResourceStates.Hidden
```

## Test Fixtures

### xUnit Class Fixture
```csharp
public class AppHostFixture : IAsyncLifetime
{
    public DistributedApplication? App { get; private set; }

    public async Task InitializeAsync()
    {
        var appHost = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.MyApp_AppHost>();

        App = await appHost.BuildAsync();
        await App.StartAsync();

        var resourceNotificationService = App.Services
            .GetRequiredService<ResourceNotificationService>();

        await resourceNotificationService
            .WaitForResourceAsync("api", KnownResourceStates.Running)
            .WaitAsync(TimeSpan.FromSeconds(60));
    }

    public async Task DisposeAsync()
    {
        if (App != null)
        {
            await App.StopAsync();
            await App.DisposeAsync();
        }
    }
}

public class IntegrationTests : IClassFixture<AppHostFixture>
{
    private readonly AppHostFixture _fixture;

    public IntegrationTests(AppHostFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task ApiReturnsOk()
    {
        var client = _fixture.App!.CreateHttpClient("api");
        var response = await client.GetAsync("/health");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

## Testing with Containers

### Wait for Container Ready
```csharp
// Containers might take longer to start
await resourceNotificationService
    .WaitForResourceAsync("redis", KnownResourceStates.Running)
    .WaitAsync(TimeSpan.FromMinutes(2));
```

### Database Tests
```csharp
[Fact]
public async Task DatabaseConnectionWorks()
{
    var connectionString = await app.GetConnectionStringAsync("db");

    await using var connection = new NpgsqlConnection(connectionString);
    await connection.OpenAsync();

    var result = await connection.ExecuteScalarAsync<int>(
        "SELECT COUNT(*) FROM users");

    Assert.True(result >= 0);
}
```

## Configuration Override

### Override for Tests
```csharp
var appHost = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.MyApp_AppHost>();

// Add test configuration
appHost.Configuration["TestMode"] = "true";
appHost.Configuration["ConnectionStrings:Override"] = "test-connection";
```

### Environment Variables
```csharp
appHost.Services.Configure<EnvironmentOptions>(options =>
{
    options.Environment = "Testing";
});
```

## Resource Inspection

### Get Resource Information
```csharp
var resources = app.Services.GetRequiredService<DistributedApplicationModel>();

foreach (var resource in resources.Resources)
{
    Console.WriteLine($"Resource: {resource.Name}, Type: {resource.GetType().Name}");
}
```

### Get Endpoint URLs
```csharp
// Get allocated endpoints
var endpoints = resource.GetEndpoints();
foreach (var endpoint in endpoints)
{
    Console.WriteLine($"Endpoint: {endpoint.EndpointName} - {endpoint.Url}");
}
```

## Testing Patterns

### Health Check Test
```csharp
[Fact]
public async Task AllServicesHealthy()
{
    var client = app.CreateHttpClient("api");
    var response = await client.GetAsync("/health");

    response.EnsureSuccessStatusCode();

    var content = await response.Content.ReadAsStringAsync();
    Assert.Contains("Healthy", content);
}
```

### API Integration Test
```csharp
[Fact]
public async Task CreateItemReturnsCreated()
{
    var client = app.CreateHttpClient("api");

    var item = new { Name = "Test Item", Value = 42 };
    var response = await client.PostAsJsonAsync("/items", item);

    Assert.Equal(HttpStatusCode.Created, response.StatusCode);

    var created = await response.Content.ReadFromJsonAsync<Item>();
    Assert.Equal("Test Item", created!.Name);
}
```

### Database Seeding Test
```csharp
[Fact]
public async Task SeededDataExists()
{
    var connectionString = await app.GetConnectionStringAsync("db");
    await using var context = new AppDbContext(
        new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(connectionString)
            .Options);

    var count = await context.Users.CountAsync();
    Assert.True(count > 0, "Database should have seeded data");
}
```

## Troubleshooting Tests

### Enable Logging
```csharp
appHost.Services.AddLogging(builder =>
{
    builder.SetMinimumLevel(LogLevel.Debug);
    builder.AddConsole();
});
```

### Capture Container Logs
```csharp
var logs = await app.GetResourceLogsAsync("redis");
Console.WriteLine(logs);
```

### Increase Timeouts
```csharp
// For slow containers or CI environments
await resourceNotificationService
    .WaitForResourceAsync("db", KnownResourceStates.Running)
    .WaitAsync(TimeSpan.FromMinutes(5));
```

## DistributedApplicationFactory (Advanced)

For scenarios requiring more control over the AppHost lifecycle than `DistributedApplicationTestingBuilder` provides:

### When to Use
- Need to run code BEFORE the builder is created
- Need to intercept AFTER build but BEFORE start
- Need custom lifecycle hooks during test setup

### Custom Factory Class
```csharp
public class CustomAppHostFactory : DistributedApplicationFactory
{
    public CustomAppHostFactory()
        : base(typeof(Projects.MyApp_AppHost))
    {
    }

    protected override void OnBuilderCreating(DistributedApplicationOptions options)
    {
        // Before builder is created
        // Modify options here
    }

    protected override void OnBuilderCreated(IDistributedApplicationBuilder builder)
    {
        // After builder created, before resources added
        // Add test-specific services
        builder.Services.AddSingleton<ITestService, MockTestService>();
    }

    protected override void OnBuilding(DistributedApplicationBuilder builder)
    {
        // After resources added, before Build()
    }

    protected override void OnBuilt(DistributedApplication application)
    {
        // After Build() but before Start()
        // Good for final configuration
    }
}
```

### Usage in Tests
```csharp
public class AdvancedIntegrationTests : IAsyncLifetime
{
    private readonly CustomAppHostFactory _factory = new();
    private DistributedApplication? _app;

    public async Task InitializeAsync()
    {
        _app = await _factory.CreateAsync();
        await _app.StartAsync();
    }

    public async Task DisposeAsync()
    {
        if (_app != null)
        {
            await _app.StopAsync();
            await _app.DisposeAsync();
        }
        _factory.Dispose();
    }

    [Fact]
    public async Task TestWithCustomFactory()
    {
        var client = _app!.CreateHttpClient("api");
        // ...
    }
}
```

**Note:** `DistributedApplicationTestingBuilder` uses `DistributedApplicationFactory` internally. Use the factory directly only when you need the additional lifecycle hooks.
