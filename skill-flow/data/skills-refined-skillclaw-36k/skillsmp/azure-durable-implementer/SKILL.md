---
name: azure-durable-implementer
description: "Implement Azure Durable Functions following opus45design.md architecture. Use for creating orchestrations, activities, entities, event ingress functions, and Service Bus/Cosmos DB integrations. Triggers on: implement, create, build, add function, new orchestration, new activity, new entity."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Azure Durable Functions Implementer

You are a specialist in implementing Azure Durable Functions for .NET 10 / C# 13 following the architecture defined in `opus45design.md`.

## Before Implementation

**ALWAYS read `opus45design.md` first** to understand the established architecture patterns.

## Architecture Patterns

### Layer Structure
```
Event Ingress Function → Durable Entities → Config-Driven Orchestrator → Activity Functions → Database
```

### 1. Event Ingress Function (Start-or-Route Pattern)

```csharp
[Function(nameof(EventIngressFunction))]
public async Task Run(
    [ServiceBusTrigger("device-events", IsSessionsEnabled = true)] ServiceBusReceivedMessage message,
    ServiceBusMessageActions messageActions,
    [DurableClient] DurableTaskClient client)
{
    var entityId = message.SessionId; // Device ID from session
    var orchestrationId = $"workflow-{entityId}";

    // Check if orchestration exists
    var status = await client.GetInstanceAsync(orchestrationId);

    if (status is null || status.RuntimeStatus is OrchestrationRuntimeStatus.Completed or OrchestrationRuntimeStatus.Failed)
    {
        // Start new orchestration
        await client.ScheduleNewOrchestrationInstanceAsync(
            nameof(WorkflowOrchestrator),
            new WorkflowInput(entityId, message.Body.ToObjectFromJson<EventData>()),
            new StartOrchestrationOptions { InstanceId = orchestrationId });
    }

    // Signal entity to accumulate event
    await client.Entities.SignalEntityAsync(
        new EntityInstanceId(nameof(EventAccumulatorEntity), entityId),
        nameof(EventAccumulatorEntity.RecordEvent),
        message.Body.ToObjectFromJson<EventData>());

    // Raise event if orchestration is waiting
    if (status?.RuntimeStatus is OrchestrationRuntimeStatus.Running)
    {
        await client.RaiseEventAsync(orchestrationId, "NewEvent", message.Body.ToObjectFromJson<EventData>());
    }

    await messageActions.CompleteMessageAsync(message);
}
```

### 2. Durable Entities (Event Accumulation)

```csharp
public class EventAccumulatorEntity : TaskEntity<EventAccumulatorState>
{
    public void RecordEvent(EventData eventData)
    {
        State.Events.Add(new AccumulatedEvent
        {
            Data = eventData,
            Timestamp = DateTime.UtcNow
        });
        State.LastActivityTime = DateTime.UtcNow;
    }

    public List<AccumulatedEvent> GetEvents() => State.Events;

    public void Clear()
    {
        State.Events.Clear();
    }

    public EventAccumulatorState GetState() => State;

    [Function(nameof(EventAccumulatorEntity))]
    public static Task RunEntityAsync([EntityTrigger] TaskEntityDispatcher dispatcher)
        => dispatcher.DispatchAsync<EventAccumulatorEntity>();
}

public class EventAccumulatorState
{
    public List<AccumulatedEvent> Events { get; set; } = [];
    public DateTime LastActivityTime { get; set; }
}
```

### 3. Config-Driven Orchestrator

```csharp
[Function(nameof(WorkflowOrchestrator))]
public async Task<WorkflowResult> RunOrchestrator(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    var input = context.GetInput<WorkflowInput>()!;
    var logger = context.CreateReplaySafeLogger<WorkflowOrchestrator>();

    // Load workflow definition ONCE at start (determinism requirement)
    var workflowDef = await context.CallActivityAsync<WorkflowDefinition>(
        nameof(LoadWorkflowDefinitionActivity),
        input.WorkflowType);

    var state = new WorkflowState { EntityId = input.EntityId };
    var currentStep = workflowDef.StartAt;

    while (currentStep is not null)
    {
        var stepDef = workflowDef.States[currentStep];

        currentStep = stepDef.Type switch
        {
            "task" => await ExecuteTaskStep(context, stepDef, state),
            "wait" => await ExecuteWaitStep(context, stepDef, state),
            "choice" => EvaluateChoiceStep(stepDef, state),
            "succeed" => null,
            "fail" => throw new WorkflowFailedException(state),
            _ => throw new InvalidOperationException($"Unknown step type: {stepDef.Type}")
        };
    }

    return new WorkflowResult { Success = true, State = state };
}
```

### 4. Activity Functions (Idempotent)

```csharp
[Function(nameof(ProcessDeviceEventsActivity))]
public async Task<ProcessingResult> Run(
    [ActivityTrigger] ProcessEventsInput input,
    CancellationToken cancellationToken)
{
    // Idempotency check - use idempotency key
    var existingResult = await _repository.GetProcessingResultAsync(input.IdempotencyKey, cancellationToken);
    if (existingResult is not null)
    {
        return existingResult;
    }

    // Process events
    var result = await _eventProcessor.ProcessAsync(input.Events, cancellationToken);

    // Store result for idempotency
    await _repository.SaveProcessingResultAsync(input.IdempotencyKey, result, cancellationToken);

    return result;
}
```

## Durable Function Patterns

### Function Chaining
```csharp
var result1 = await context.CallActivityAsync<string>("Step1", input);
var result2 = await context.CallActivityAsync<string>("Step2", result1);
var result3 = await context.CallActivityAsync<string>("Step3", result2);
```

### Fan-Out/Fan-In
```csharp
var tasks = items.Select(item =>
    context.CallActivityAsync<Result>("ProcessItem", item));
var results = await Task.WhenAll(tasks);
```

### Async HTTP API
```csharp
[Function("StartWorkflow")]
public async Task<HttpResponseData> Start(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
    [DurableClient] DurableTaskClient client)
{
    var instanceId = await client.ScheduleNewOrchestrationInstanceAsync(nameof(MyOrchestrator), input);
    return await client.CreateCheckStatusResponseAsync(req, instanceId);
}
```

### External Event Wait with Timeout
```csharp
using var cts = new CancellationTokenSource();
var timeout = context.CreateTimer(context.CurrentUtcDateTime.AddHours(48), cts.Token);
var eventTask = context.WaitForExternalEvent<EventData>("ExternalProcessComplete");

var winner = await Task.WhenAny(timeout, eventTask);
if (winner == timeout)
{
    // Handle timeout
    return await context.CallActivityAsync<Result>("HandleTimeout", input);
}

cts.Cancel();
var eventData = await eventTask;
```

### Monitoring (Polling)
```csharp
while (true)
{
    var status = await context.CallActivityAsync<Status>("CheckStatus", jobId);
    if (status.IsComplete) break;

    await context.CreateTimer(context.CurrentUtcDateTime.AddMinutes(5), CancellationToken.None);
}
```

### Human Interaction
```csharp
var approvalTask = context.WaitForExternalEvent<ApprovalResult>("ApprovalReceived");
var timeout = context.CreateTimer(context.CurrentUtcDateTime.AddDays(7), CancellationToken.None);

var winner = await Task.WhenAny(approvalTask, timeout);
if (winner == timeout)
{
    await context.CallActivityAsync("Escalate", requestId);
}
```

### Sub-Orchestrations
```csharp
var subResult = await context.CallSubOrchestratorAsync<Result>(
    nameof(SubOrchestrator),
    subInput,
    new SubOrchestrationOptions { InstanceId = $"{context.InstanceId}-sub" });
```

## Integration Patterns

### Service Bus with Sessions
```csharp
[Function(nameof(SessionHandler))]
public async Task Run(
    [ServiceBusTrigger("queue", IsSessionsEnabled = true)] ServiceBusReceivedMessage message,
    ServiceBusMessageActions actions)
{
    // Session ID guarantees FIFO per entity
    var entityId = message.SessionId;
    // Process in order...
}
```

### Cosmos DB Integration
```csharp
[Function(nameof(CosmosActivity))]
public async Task<Document> Run(
    [ActivityTrigger] string id,
    [CosmosDBInput("database", "container", Id = "{id}", PartitionKey = "{id}")] Document document)
{
    return document;
}
```

### Retry Policies
```csharp
var options = new TaskOptions(new TaskRetryOptions(
    new RetryPolicy(
        maxNumberOfAttempts: 3,
        firstRetryInterval: TimeSpan.FromSeconds(5),
        backoffCoefficient: 2.0)));

await context.CallActivityAsync("UnreliableActivity", input, options);
```

## Saga Pattern with Compensation

```csharp
var completedSteps = new List<string>();

try
{
    await context.CallActivityAsync("Step1", input);
    completedSteps.Add("Step1");

    await context.CallActivityAsync("Step2", input);
    completedSteps.Add("Step2");

    await context.CallActivityAsync("Step3", input);
    completedSteps.Add("Step3");
}
catch (Exception)
{
    // Compensate in reverse order
    foreach (var step in completedSteps.AsEnumerable().Reverse())
    {
        await context.CallActivityAsync($"Compensate{step}", input);
    }
    throw;
}
```

## Critical Rules

1. **Determinism in Orchestrators**
   - NO `DateTime.Now` - use `context.CurrentUtcDateTime`
   - NO `Guid.NewGuid()` - use `context.NewGuid()`
   - NO random numbers
   - NO I/O operations
   - Load config ONCE at start

2. **Replay-Safe Logging**
   ```csharp
   var logger = context.CreateReplaySafeLogger<MyOrchestrator>();
   ```

3. **Idempotent Activities**
   - Use idempotency keys
   - Check for existing results before processing
   - Store results after processing

4. **Isolated Worker Model** (.NET 10)
   - Use `Microsoft.Azure.Functions.Worker` packages
   - Use `TaskOrchestrationContext` not `IDurableOrchestrationContext`

5. **host.json Optimization**
   ```json
   {
     "extensions": {
       "durableTask": {
         "storageProvider": { "type": "AzureStorage" },
         "extendedSessionsEnabled": true,
         "maxConcurrentActivityFunctions": 10,
         "maxConcurrentOrchestratorFunctions": 10
       }
     }
   }
   ```
