# Messaging Integrations Reference

## Quick Reference

| Messaging | Hosting Package | Client Package | Add Method |
|-----------|----------------|----------------|------------|
| RabbitMQ | `Aspire.Hosting.RabbitMQ` | `Aspire.RabbitMQ.Client` | `AddRabbitMQ()` |
| Kafka | `Aspire.Hosting.Kafka` | `Aspire.Confluent.Kafka` | `AddKafka()` |
| NATS | `Aspire.Hosting.NATS` | `Aspire.NATS.Net` | `AddNats()` |
| Azure Service Bus | `Aspire.Hosting.Azure.ServiceBus` | `Aspire.Azure.Messaging.ServiceBus` | `AddAzureServiceBus()` |
| Azure Event Hubs | `Aspire.Hosting.Azure.EventHubs` | `Aspire.Azure.Messaging.EventHubs` | `AddAzureEventHubs()` |

## RabbitMQ

### Hosting Integration
```csharp
// Package: Aspire.Hosting.RabbitMQ
var rabbitmq = builder.AddRabbitMQ("messaging")
    .WithDataVolume()                           // Persist data
    .WithLifetime(ContainerLifetime.Persistent) // Keep across restarts
    .WithManagementPlugin();                    // Enable management UI

builder.AddProject<Projects.Api>("api")
    .WithReference(rabbitmq)
    .WaitFor(rabbitmq);
```

### Client Integration
```csharp
// Package: Aspire.RabbitMQ.Client
builder.AddRabbitMQClient("messaging");
```

### Use in Services
```csharp
public class MessagePublisher(IConnection connection)
{
    public void Publish(string queue, string message)
    {
        using var channel = connection.CreateModel();
        channel.QueueDeclare(queue, durable: true, exclusive: false, autoDelete: false);
        
        var body = Encoding.UTF8.GetBytes(message);
        channel.BasicPublish(exchange: "", routingKey: queue, body: body);
    }
}
```

### With MassTransit
```csharp
// Package: MassTransit.RabbitMQ
builder.Services.AddMassTransit(x =>
{
    x.UsingRabbitMq((context, cfg) =>
    {
        var connectionString = context.GetRequiredService<IConfiguration>()
            .GetConnectionString("messaging");
        cfg.Host(new Uri(connectionString!));
        cfg.ConfigureEndpoints(context);
    });
});
```

## Apache Kafka

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Kafka
var kafka = builder.AddKafka("kafka")
    .WithDataVolume()
    .WithKafkaUI();  // Add Kafka UI

builder.AddProject<Projects.Api>("api")
    .WithReference(kafka)
    .WaitFor(kafka);
```

### Client Integration
```csharp
// Package: Aspire.Confluent.Kafka

// Producer
builder.AddKafkaProducer<string, string>("kafka");

// Consumer
builder.AddKafkaConsumer<string, string>("kafka", consumerBuilder =>
{
    consumerBuilder.Config.GroupId = "my-consumer-group";
    consumerBuilder.Config.AutoOffsetReset = AutoOffsetReset.Earliest;
});
```

### Use in Services
```csharp
// Producer
public class EventPublisher(IProducer<string, string> producer)
{
    public async Task PublishAsync(string topic, string key, string value)
    {
        await producer.ProduceAsync(topic, new Message<string, string>
        {
            Key = key,
            Value = value
        });
    }
}

// Consumer
public class EventConsumer(IConsumer<string, string> consumer) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        consumer.Subscribe("my-topic");
        
        while (!ct.IsCancellationRequested)
        {
            var result = consumer.Consume(ct);
            // Process message
        }
    }
}
```

## NATS

### Hosting Integration
```csharp
// Package: Aspire.Hosting.NATS
var nats = builder.AddNats("nats")
    .WithDataVolume()
    .WithJetStream();  // Enable JetStream for persistence

builder.AddProject<Projects.Api>("api")
    .WithReference(nats)
    .WaitFor(nats);
```

### Client Integration
```csharp
// Package: Aspire.NATS.Net
builder.AddNatsClient("nats");
```

### Use in Services
```csharp
public class NatsPublisher(INatsConnection nats)
{
    public async Task PublishAsync(string subject, string data)
    {
        await nats.PublishAsync(subject, data);
    }
}

public class NatsSubscriber(INatsConnection nats) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        await foreach (var msg in nats.SubscribeAsync<string>("events.*", cancellationToken: ct))
        {
            Console.WriteLine($"Received: {msg.Data}");
        }
    }
}
```

## Azure Service Bus

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Azure.ServiceBus
var serviceBus = builder.AddAzureServiceBus("messaging");

// Add queue
serviceBus.AddServiceBusQueue("orders");

// Add topic with subscription
var topic = serviceBus.AddServiceBusTopic("notifications");
topic.AddServiceBusSubscription("email-handler");

// Use emulator locally
builder.AddAzureServiceBus("messaging").RunAsEmulator();
```

### Client Integration
```csharp
// Package: Aspire.Azure.Messaging.ServiceBus
builder.AddAzureServiceBusClient("messaging");
```

### Use in Services
```csharp
public class OrderPublisher(ServiceBusClient client)
{
    public async Task SendOrderAsync(Order order)
    {
        var sender = client.CreateSender("orders");
        await sender.SendMessageAsync(new ServiceBusMessage(
            JsonSerializer.Serialize(order)));
    }
}

public class OrderProcessor(ServiceBusClient client) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        var processor = client.CreateProcessor("orders");
        processor.ProcessMessageAsync += async args =>
        {
            var order = JsonSerializer.Deserialize<Order>(args.Message.Body);
            // Process order
            await args.CompleteMessageAsync(args.Message);
        };
        processor.ProcessErrorAsync += args => Task.CompletedTask;
        
        await processor.StartProcessingAsync(ct);
    }
}
```

## Azure Event Hubs

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Azure.EventHubs
var eventHubs = builder.AddAzureEventHubs("events");
eventHubs.AddEventHub("telemetry");

// Use emulator locally
builder.AddAzureEventHubs("events").RunAsEmulator();
```

### Client Integration
```csharp
// Package: Aspire.Azure.Messaging.EventHubs

// Producer
builder.AddAzureEventHubProducerClient("events", "telemetry");

// Consumer
builder.AddAzureEventHubConsumerClient("events", "telemetry");
```

## LavinMQ (Lightweight RabbitMQ Alternative)

### Hosting Integration
```csharp
// Package: CommunityToolkit.Aspire.Hosting.LavinMQ
var lavinmq = builder.AddLavinMQ("messaging")
    .WithDataVolume()
    .WithManagementPlugin();
```

## Common Patterns

### Persistent Messaging Container
```csharp
builder.AddRabbitMQ("messaging")
    .WithDataVolume()
    .WithLifetime(ContainerLifetime.Persistent);
```

### Management UIs
```csharp
// RabbitMQ Management
builder.AddRabbitMQ("messaging").WithManagementPlugin();

// Kafka UI
builder.AddKafka("kafka").WithKafkaUI();
```

### Health Checks
```csharp
// Wait for messaging to be ready
builder.AddProject<Projects.Api>("api")
    .WithReference(messaging)
    .WaitFor(messaging);
```

## Environment Variables

When using `WithReference(messaging)`:

| Service | Variable | Example |
|---------|----------|---------|
| RabbitMQ | `ConnectionStrings__messaging` | `amqp://guest:guest@localhost:5672` |
| Kafka | `ConnectionStrings__kafka` | `localhost:9092` |
| NATS | `ConnectionStrings__nats` | `nats://localhost:4222` |
