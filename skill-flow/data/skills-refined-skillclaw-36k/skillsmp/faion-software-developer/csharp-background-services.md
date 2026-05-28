---
id: csharp-background-services
name: "Background Services"
domain: CSHARP
skill: faion-software-developer
category: "backend"
---

## Background Services

### Problem
Process background tasks in ASP.NET Core.

### Framework: Hosted Service

```csharp
// Services/BackgroundOrderProcessor.cs

namespace MyApp.Services;

public class BackgroundOrderProcessor : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<BackgroundOrderProcessor> _logger;
    private readonly Channel<int> _orderChannel;

    public BackgroundOrderProcessor(
        IServiceProvider serviceProvider,
        ILogger<BackgroundOrderProcessor> logger,
        Channel<int> orderChannel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _orderChannel = orderChannel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processor started");

        await foreach (var orderId in _orderChannel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessOrderAsync(orderId, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order {OrderId}", orderId);
            }
        }
    }

    private async Task ProcessOrderAsync(int orderId, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();

        _logger.LogInformation("Processing order {OrderId}", orderId);
        await orderService.ProcessAsync(orderId, ct);
        _logger.LogInformation("Order {OrderId} processed", orderId);
    }
}

// Queue service
public interface IOrderQueue
{
    ValueTask QueueOrderAsync(int orderId);
}

public class OrderQueue : IOrderQueue
{
    private readonly Channel<int> _channel;

    public OrderQueue(Channel<int> channel)
    {
        _channel = channel;
    }

    public async ValueTask QueueOrderAsync(int orderId)
    {
        await _channel.Writer.WriteAsync(orderId);
    }
}
```

### Timed Background Service

```csharp
// Services/CleanupService.cs

namespace MyApp.Services;

public class CleanupService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CleanupService> _logger;
    private readonly TimeSpan _period = TimeSpan.FromHours(1);

    public CleanupService(
        IServiceProvider serviceProvider,
        ILogger<CleanupService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(_period);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            try
            {
                await DoCleanupAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during cleanup");
            }
        }
    }

    private async Task DoCleanupAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var cutoff = DateTime.UtcNow.AddDays(-30);

        var deleted = await context.AuditLogs
            .Where(a => a.CreatedAt < cutoff)
            .ExecuteDeleteAsync(ct);

        _logger.LogInformation("Deleted {Count} old audit logs", deleted);
    }
}
```

### Agent

faion-backend-agent
