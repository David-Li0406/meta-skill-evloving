# Caching Integrations Reference

## Quick Reference

| Cache | Hosting Package | Client Package | Add Method |
|-------|----------------|----------------|------------|
| Redis | `Aspire.Hosting.Redis` | `Aspire.StackExchange.Redis` | `AddRedis()` |
| Valkey | `Aspire.Hosting.Valkey` | `Aspire.StackExchange.Redis` | `AddValkey()` |
| Garnet | `Aspire.Hosting.Garnet` | `Aspire.StackExchange.Redis` | `AddGarnet()` |

## Redis

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Redis
var redis = builder.AddRedis("cache")
    .WithDataVolume()                           // Persist data
    .WithLifetime(ContainerLifetime.Persistent) // Keep across restarts
    .WithRedisCommander();                      // Add Redis Commander UI

builder.AddProject<Projects.Api>("api")
    .WithReference(redis)
    .WaitFor(redis);
```

### Client Integration
```csharp
// Package: Aspire.StackExchange.Redis
builder.AddRedisClient("cache");
```

### Use in Services
```csharp
public class CacheService(IConnectionMultiplexer redis)
{
    public async Task<string?> GetAsync(string key)
    {
        var db = redis.GetDatabase();
        return await db.StringGetAsync(key);
    }
    
    public async Task SetAsync(string key, string value, TimeSpan? expiry = null)
    {
        var db = redis.GetDatabase();
        await db.StringSetAsync(key, value, expiry);
    }
}
```

### Distributed Cache
```csharp
// Package: Aspire.StackExchange.Redis.DistributedCaching
builder.AddRedisDistributedCache("cache");

// Use via IDistributedCache
public class MyService(IDistributedCache cache)
{
    public async Task<byte[]?> GetAsync(string key)
    {
        return await cache.GetAsync(key);
    }
}
```

### Output Caching
```csharp
// Package: Aspire.StackExchange.Redis.OutputCaching
builder.AddRedisOutputCache("cache");

// Configure in Program.cs
app.UseOutputCache();

// Use on endpoints
app.MapGet("/data", () => GetData())
    .CacheOutput(policy => policy.Expire(TimeSpan.FromMinutes(5)));
```

### Redis Configuration
```json
{
  "Aspire": {
    "StackExchange": {
      "Redis": {
        "DisableHealthChecks": false,
        "DisableTracing": false
      }
    }
  }
}
```

## Valkey (Redis Fork)

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Valkey
var valkey = builder.AddValkey("cache")
    .WithDataVolume()
    .WithLifetime(ContainerLifetime.Persistent);

builder.AddProject<Projects.Api>("api")
    .WithReference(valkey);
```

### Client Integration
```csharp
// Same as Redis - uses StackExchange.Redis
builder.AddRedisClient("cache");
```

## Garnet (Microsoft Redis Alternative)

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Garnet
var garnet = builder.AddGarnet("cache")
    .WithDataVolume()
    .WithLifetime(ContainerLifetime.Persistent);

builder.AddProject<Projects.Api>("api")
    .WithReference(garnet);
```

### Client Integration
```csharp
// Same as Redis - uses StackExchange.Redis
builder.AddRedisClient("cache");
```

## Azure Cache for Redis

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Azure.Redis
var redis = builder.AddAzureRedis("cache");

// Run as container locally
builder.AddAzureRedis("cache").RunAsContainer();
```

### Client Integration
```csharp
// Package: Aspire.Azure.StackExchange.Redis
builder.AddAzureRedisClient("cache");
```

## Common Patterns

### Persistent Container
```csharp
// Keep Redis running across AppHost restarts
builder.AddRedis("cache")
    .WithLifetime(ContainerLifetime.Persistent);
```

### Redis Commander UI
```csharp
// Add web-based Redis management
builder.AddRedis("cache").WithRedisCommander();
```

### Redis Insight
```csharp
// Add RedisInsight for visualization
builder.AddRedis("cache").WithRedisInsight();
```

### Data Persistence
```csharp
// Docker volume (recommended)
builder.AddRedis("cache").WithDataVolume();

// Bind mount
builder.AddRedis("cache")
    .WithDataBindMount(source: "./data/redis");
```

### Custom Configuration
```csharp
builder.AddRedis("cache")
    .WithEndpoint(port: 6380, name: "redis")
    .WithEnvironment("REDIS_ARGS", "--maxmemory 256mb");
```

## Caching Patterns

### Cache-Aside Pattern
```csharp
public class ProductService(IConnectionMultiplexer redis, IProductRepository repo)
{
    public async Task<Product?> GetProductAsync(int id)
    {
        var db = redis.GetDatabase();
        var key = $"product:{id}";
        
        // Try cache first
        var cached = await db.StringGetAsync(key);
        if (cached.HasValue)
            return JsonSerializer.Deserialize<Product>(cached!);
        
        // Load from database
        var product = await repo.GetAsync(id);
        if (product != null)
        {
            await db.StringSetAsync(key, 
                JsonSerializer.Serialize(product),
                TimeSpan.FromMinutes(10));
        }
        
        return product;
    }
}
```

### Distributed Lock
```csharp
public class LockService(IConnectionMultiplexer redis)
{
    public async Task<bool> AcquireLockAsync(string resource, TimeSpan expiry)
    {
        var db = redis.GetDatabase();
        return await db.StringSetAsync(
            $"lock:{resource}",
            Environment.MachineName,
            expiry,
            When.NotExists);
    }
    
    public async Task ReleaseLockAsync(string resource)
    {
        var db = redis.GetDatabase();
        await db.KeyDeleteAsync($"lock:{resource}");
    }
}
```

## Environment Variables

When using `WithReference(cache)`:

| Variable | Value |
|----------|-------|
| `ConnectionStrings__cache` | `localhost:6379` |
| `CACHE_HOST` | `localhost` |
| `CACHE_PORT` | `6379` |
