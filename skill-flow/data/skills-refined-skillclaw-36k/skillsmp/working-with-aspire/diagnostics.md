# Diagnostics and Troubleshooting Reference

## Common Error Codes

### ASPIRE001 - Resource Name Invalid
```
error ASPIRE001: Resource name 'my-resource!' contains invalid characters
```

**Fix:** Use only alphanumeric characters and hyphens in resource names.
```csharp
// Bad
builder.AddRedis("my-cache!")

// Good
builder.AddRedis("my-cache")
```

### ASPIRE002 - Duplicate Resource Name
```
error ASPIRE002: Resource 'api' already exists
```

**Fix:** Use unique names for all resources.

### ASPIRE003 - Missing Reference
```
error ASPIRE003: Resource 'db' referenced but not defined
```

**Fix:** Ensure the referenced resource is added before referencing it.

### ASPIRE004 - Circular Dependency
```
error ASPIRE004: Circular dependency detected between resources
```

**Fix:** Review `WithReference` and `WaitFor` chains to remove cycles.

## Container Issues

### Container Won't Start
```
Resource 'redis' failed to start: port already in use
```

**Fixes:**
1. Stop conflicting containers: `docker ps` and `docker stop <id>`
2. Use random ports: `.WithHttpEndpoint()` without port number
3. Change to a different port: `.WithHttpEndpoint(port: 6380)`

### Container Pull Failed
```
Failed to pull image: docker.io/library/postgres:15
```

**Fixes:**
1. Check Docker is running: `docker info`
2. Check network connectivity
3. Try pulling manually: `docker pull postgres:15`
4. Check Docker Hub rate limits

### Container Keeps Restarting
```
Container 'db' restarted 5 times
```

**Fixes:**
1. Check container logs in Dashboard
2. Verify environment variables
3. Check resource limits
4. Ensure health checks aren't too aggressive

## Service Discovery Issues

### Connection String Not Found
```
ConnectionStrings__db not found in configuration
```

**Causes:**
- Missing `WithReference(db)` call
- Resource not started yet

**Fix:**
```csharp
builder.AddProject<Projects.Api>("api")
    .WithReference(db)  // Add this
    .WaitFor(db);       // And this
```

### Service URL Format
Aspire uses specific environment variable patterns:
```
services__<name>__<scheme>__<index>
```

Example: `services__api__http__0` = `http://localhost:5001`

### Debug Service Discovery
```csharp
// In consuming app, log all env vars
foreach (var env in Environment.GetEnvironmentVariables())
{
    Console.WriteLine($"{env.Key}={env.Value}");
}
```

## Port Conflicts

### Port Already in Use
```
Address already in use: 0.0.0.0:5432
```

**Fixes:**
1. Find process: `lsof -i :5432` or `netstat -ano | findstr :5432`
2. Kill process or use different port
3. Use dynamic ports: `.WithHttpEndpoint()` without port

### Proxy Port Issues
```
IsProxied endpoint not binding correctly
```

**Fix:** Set `IsProxied` to false for external executables:
```csharp
.WithEndpoint(callback: e => e.IsProxied = false)
```

## Database Issues

### Database Not Created
```
Database 'mydb' does not exist
```

**Cause:** Database creation relies on `ResourceReadyEvent`

**Fixes:**
1. Ensure container is fully started
2. Use `WaitFor` before referencing
3. Check container logs for errors

### Migration Errors
```
Cannot apply migrations: connection refused
```

**Fix:** Use `aspire exec` with proper context:
```bash
aspire exec --resource api -- dotnet ef database update
```

## Azure Issues

### Authentication Failed
```
Azure authentication failed: no valid credentials found
```

**Fixes:**
1. Run `az login`
2. Set subscription: `az account set --subscription "..."`
3. Check environment variables: `AZURE_*`

### Provisioning Failed
```
Resource provisioning failed: insufficient permissions
```

**Fixes:**
1. Verify Contributor role on resource group
2. Check subscription limits/quotas
3. Review Azure Activity Log for details

### Missing Configuration
```
Azure configuration not found: SubscriptionId
```

**Fix:** Add to `appsettings.json`:
```json
{
  "Azure": {
    "SubscriptionId": "your-subscription-id",
    "Location": "eastus",
    "ResourceGroup": "rg-myapp"
  }
}
```

## Dashboard Issues

### Dashboard Not Loading
```
Dashboard not accessible at https://localhost:17043
```

**Fixes:**
1. Check if port is blocked by firewall
2. Try different browser
3. Clear browser cache
4. Check AppHost console for login URL with token

### Telemetry Not Showing
```
No traces/metrics appearing in dashboard
```

**Fixes:**
1. Verify OTEL env vars are set
2. Check service is actually running
3. Wait for data to propagate (few seconds)
4. Verify correct endpoints in service

## Health Check Failures

### Resource Never Becomes Healthy
```
Timeout waiting for 'db' to become healthy
```

**Causes:**
- Resource is unhealthy
- Health check misconfigured
- Network issues

**Fixes:**
1. Check container logs
2. Verify health check endpoint exists
3. Increase timeout:
```csharp
.WaitForHealthy(db, timeout: TimeSpan.FromMinutes(5))
```

## Debugging Techniques

### Enable Verbose Logging
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Aspire": "Debug",
      "Aspire.Hosting": "Debug",
      "Aspire.Hosting.Dcp": "Debug"
    }
  }
}
```

### View Container Logs
1. Open Aspire Dashboard
2. Navigate to Resources
3. Click on resource
4. View Console Logs tab

### Check Resource State
```csharp
builder.Eventing.Subscribe<ResourceReadyEvent>((@event, ct) =>
{
    Console.WriteLine($"Resource {event.Resource.Name} is ready");
    return Task.CompletedTask;
});
```

### Environment Variable Inspection
```csharp
// Add to consuming service
app.MapGet("/debug/env", () =>
    Environment.GetEnvironmentVariables()
        .Cast<DictionaryEntry>()
        .Where(e => e.Key.ToString()!.StartsWith("ConnectionStrings") ||
                    e.Key.ToString()!.StartsWith("services"))
        .ToDictionary(e => e.Key.ToString()!, e => e.Value?.ToString()));
```

## Common Warnings

### ASPIREINTERACTION001
```
warning ASPIREINTERACTION001: Type is for evaluation purposes only
```

**Context:** Using preview/experimental APIs

**Fix:** Suppress if intentional:
```csharp
#pragma warning disable ASPIREINTERACTION001
// Your code
#pragma warning restore ASPIREINTERACTION001
```

### Resource Not Starting
Check these in order:
1. Docker running? `docker info`
2. Image exists? `docker images`
3. Port available? `lsof -i :<port>`
4. Container logs in Dashboard
5. AppHost console output

## Performance Issues

### Slow Container Startup
```csharp
// Use persistent containers for frequently-used resources
builder.AddRedis("cache")
    .WithLifetime(ContainerLifetime.Persistent);
```

### Large Context/Memory
- Reduce number of resources
- Use external services instead of containers
- Increase Docker memory limits

## Getting Help

1. Check Aspire Dashboard logs
2. Review container logs
3. Enable debug logging
4. Check GitHub Issues: https://github.com/dotnet/aspire/issues
5. Use `aspire --help` for CLI options
