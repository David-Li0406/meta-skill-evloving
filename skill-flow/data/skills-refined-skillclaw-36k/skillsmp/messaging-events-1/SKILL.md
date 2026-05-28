---
name: messaging-events
description: RabbitMQ pub/sub patterns for asynchronous processing of entity changes and system events.
---
# Messaging & Events (RabbitMQ)

RabbitMQ pub/sub patterns from rx-erp for async processing.

## Overview

| Component | Description |
|-----------|-------------|
| Exchange | Topic exchange for routing |
| Queue | Message destination |
| Routing Key | `{Entity}.{Crud}.{Operation}` |
| Message | BrokeredMessage with Entity payload |

## Message Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  SubmitChanges  │────>│  RabbitMQ       │────>│  Subscriber     │
│  ("CheckIn")    │     │  Exchange       │     │  (Handler)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  Rental.Changed.CheckIn   Route by key      Update inventory,
                                             Send notification
```

## BrokeredMessage

```csharp
public class BrokeredMessage
{
    public string RoutingKey => $"{Entity}.{Crud}.{Operation}";

    public Entity? Item { get; set; }
    public string? Operation { get; set; }
    public CrudOperation Crud { get; set; }
    public int? TryCount { get; set; }
    public string? Username { get; set; }
    public Dictionary<string, object> Headers { get; } = new();
    public TimeSpan RetryDelay { get; set; }

    public void Accept() => m_acknowledge(this, MessageReceiveStatus.Accepted);
    public void Reject() => m_acknowledge(this, MessageReceiveStatus.Rejected);
    public void Delay(TimeSpan ttl) { /* retry with delay */ }
}

public enum CrudOperation
{
    Added,
    Changed,
    Deleted
}
```

## Publishing Messages

Messages are automatically published when calling `SubmitChanges`:

```csharp
using var session = context.OpenSession();
session.Attach(rental);
await session.SubmitChanges("CheckIn");
// Publishes: Rental.Changed.CheckIn
```

### Routing Key Format

| Example | Entity | Crud | Operation |
|---------|--------|------|-----------|
| `Rental.Changed.CheckIn` | Rental | Changed | CheckIn |
| `Rental.Changed.CheckOut` | Rental | Changed | CheckOut |
| `Motorbike.Changed.StatusUpdate` | Motorbike | Changed | StatusUpdate |
| `Payment.Added.Rental` | Payment | Added | Rental |
| `Renter.Added.Registration` | Renter | Added | Registration |

## Subscriber Base Pattern

```csharp
public abstract class Subscriber<T> : Subscriber where T : Entity
{
    public abstract override string QueueName { get; }
    public abstract override string[] RoutingKeys { get; }

    protected abstract Task ProcessMessage(T item, BrokeredMessage message);

    public override void Run(IMessageBroker broker)
    {
        broker.OnMessageDeliveredAsync(async message =>
        {
            try
            {
                var item = message.Item as T;
                await ProcessMessage(item!, message);
                return MessageReceiveStatus.Accepted;
            }
            catch (Exception ex)
            {
                Logger.LogError(ex, "Failed to process message");
                return MessageReceiveStatus.Rejected;
            }
        }, new SubscriberOption
        {
            QueueName = QueueName,
            RoutingKeys = RoutingKeys
        });
    }
}
```

## Example Subscribers

### Rental Check-Out Handler

```csharp
public class RentalCheckOutSubscriber : Subscriber<Rental>
{
    public override string QueueName => nameof(RentalCheckOutSubscriber);
    public override string[] RoutingKeys => [$"{nameof(Rental)}.{CrudOperation.Changed}.CheckOut"];

    protected override async Task ProcessMessage(Rental rental, BrokeredMessage message)
    {
        var context = new RentalDataContext();

        // Update motorbike status back to Available
        var motorbike = await context.LoadOneAsync<Motorbike>(
            m => m.MotorbikeId == rental.MotorbikeId);

        motorbike!.Status = "Available";

        using var session = context.OpenSession();
        session.Attach(motorbike);
        await session.SubmitChanges("StatusUpdate");

        // Send thank you notification
        await SendThankYouEmail(rental);

        message.Accept();
    }

    private async Task SendThankYouEmail(Rental rental)
    {
        // Email service call
    }
}
```

### Expiry Warning Handler

```csharp
public class RentalExpirySubscriber : Subscriber<Rental>
{
    public override string QueueName => nameof(RentalExpirySubscriber);
    public override string[] RoutingKeys => [$"{nameof(Rental)}.{CrudOperation.Changed}.ExpiryCheck"];

    protected override async Task ProcessMessage(Rental rental, BrokeredMessage message)
    {
        if (rental.Status != "Active")
        {
            message.Accept();
            return;
        }

        var daysRemaining = (rental.ExpectedEndDate - DateTimeOffset.Now).TotalDays;

        if (daysRemaining <= 1)
        {
            await SendExpiryWarning(rental);
        }

        message.Accept();
    }
}
```

### Damage Report Handler

```csharp
public class DamageReportSubscriber : Subscriber<DamageReport>
{
    public override string QueueName => nameof(DamageReportSubscriber);
    public override string[] RoutingKeys => [$"{nameof(DamageReport)}.{CrudOperation.Added}.*"];

    protected override async Task ProcessMessage(DamageReport damage, BrokeredMessage message)
    {
        // Notify shop owner
        await NotifyShopOwner(damage);

        // If major damage, flag motorbike for maintenance
        if (damage.Severity == "Major")
        {
            var context = new RentalDataContext();
            var motorbike = await context.LoadOneAsync<Motorbike>(
                m => m.MotorbikeId == damage.MotorbikeId);

            motorbike!.Status = "Maintenance";
            motorbike.Notes = $"Major damage reported: {damage.Description}";

            using var session = context.OpenSession();
            session.Attach(motorbike);
            await session.SubmitChanges("MaintenanceFlag");
        }

        message.Accept();
    }
}
```

## Subscriber Registration

```csharp
// Program.cs or HostedService
public class SubscriberHostedService : BackgroundService
{
    private readonly IMessageBroker m_broker;
    private readonly IServiceProvider m_services;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var subscribers = new Subscriber[]
        {
            new RentalCheckOutSubscriber(),
            new RentalExpirySubscriber(),
            new DamageReportSubscriber()
        };

        foreach (var subscriber in subscribers)
        {
            subscriber.Run(m_broker);
        }

        await Task.Delay(Timeout.Infinite, stoppingToken);
    }
}
```

## Error Handling & Retry

```csharp
protected override async Task ProcessMessage(Rental rental, BrokeredMessage message)
{
    try
    {
        await ProcessRentalAsync(rental);
        message.Accept();
    }
    catch (TransientException ex)
    {
        // Retry with delay
        if (message.TryCount < 3)
        {
            message.Delay(TimeSpan.FromMinutes(5));
        }
        else
        {
            Logger.LogError(ex, "Max retries exceeded");
            message.Reject();  // Move to dead letter queue
        }
    }
    catch (Exception ex)
    {
        Logger.LogError(ex, "Unrecoverable error");
        message.Reject();
    }
}
```

## RabbitMQ Configuration

```csharp
// appsettings.json
{
  "RabbitMQ": {
    "Host": "localhost",
    "Port": 5672,
    "Username": "guest",
    "Password": "guest",
    "VirtualHost": "/",
    "Exchange": "motorent.events"
  }
}
```

## Common Use Cases

| Event | Subscriber Action |
|-------|-------------------|
| Rental.CheckIn | Send confirmation SMS |
| Rental.CheckOut | Send receipt email |
| Rental.Expiring | Send reminder notification |
| DamageReport.Added | Notify shop owner |
| Payment.Completed | Generate invoice |
| Motorbike.Maintenance | Update availability |

## Source
- From: `D:\project\work\rx-erp` messaging patterns

