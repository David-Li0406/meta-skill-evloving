# Production Design Patterns

Practical patterns for building production-ready agent systems.

## Local Development with Ollama

Same code works locally with Ollama as with Azure OpenAI. Cost-effective for iteration.

```csharp
// Local development with Ollama (via OllamaSharp)
using OllamaSharp;

var ollama = new OllamaApiClient("http://localhost:11434");
IChatClient chatClient = ollama.AsChatClient("mistral"); // or llama3, deepseek, etc.

AIAgent agent = chatClient.CreateAIAgent(
    instructions: "You are a helpful assistant.",
    tools: [AIFunctionFactory.Create(GetWeather)]);

// Same code works for Azure OpenAI
var azureClient = new AzureOpenAIClient(
    new Uri("https://<resource>.openai.azure.com"),
    new DefaultAzureCredential())
    .GetChatClient("gpt-4o-mini")
    .AsIChatClient();

AIAgent cloudAgent = azureClient.CreateAIAgent(
    instructions: "You are a helpful assistant.",
    tools: [AIFunctionFactory.Create(GetWeather)]);
```

**Recommended local models:**
- `mistral` / `ministral3` - Good general purpose
- `llama3.2` - Solid performance, widely used
- `phi4` - Microsoft's small model, optimized for local
- `deepseek-r1` - Strong reasoning (larger)

**Tips:**
- Run Ollama in container for isolation: `docker run -d --gpus all -p 11434:11434 ollama/ollama`
- 8GB GPU can run 5B-7B models comfortably
- Test locally, deploy to cloud with same agent code

## Pattern 1: Stateless Service with Thread Injection

Thread state stored externally; agent instances are stateless and scalable.

```csharp
public class ConversationService
{
    private readonly AIAgent _agent;
    private readonly IThreadStore _threadStore;

    public ConversationService(IChatClient chatClient, IThreadStore threadStore)
    {
        _agent = chatClient.CreateAIAgent(
            instructions: "You are a helpful assistant.",
            name: "Assistant");
        _threadStore = threadStore;
    }

    public async Task<ConversationResponse> ProcessMessageAsync(
        string conversationId,
        string userMessage)
    {
        // Load thread from external store
        var threadJson = await _threadStore.GetAsync(conversationId);
        var thread = threadJson != null
            ? _agent.DeserializeThread(JsonSerializer.Deserialize<JsonElement>(threadJson))
            : _agent.GetNewThread();

        // Process message
        var response = await _agent.RunAsync(userMessage, thread);

        // Persist updated thread
        var serialized = await thread.SerializeAsync();
        await _threadStore.SaveAsync(conversationId, serialized.GetRawText());

        return new ConversationResponse
        {
            Text = response.Text,
            ConversationId = conversationId
        };
    }
}

// Usage in ASP.NET
app.MapPost("/chat", async (ChatRequest request, ConversationService service) =>
{
    return await service.ProcessMessageAsync(request.ConversationId, request.Message);
});
```

## Pattern 2: Agent Factory for DI

Register agent creation as factory for proper dependency injection.

```csharp
public static class AgentServiceExtensions
{
    public static IServiceCollection AddAgentServices(this IServiceCollection services)
    {
        services.AddSingleton<IChatClient>(sp =>
        {
            var config = sp.GetRequiredService<IConfiguration>();
            return new AzureOpenAIClient(
                new Uri(config["AzureOpenAI:Endpoint"]!),
                new DefaultAzureCredential())
                .GetChatClient(config["AzureOpenAI:Model"]!)
                .AsIChatClient();
        });

        services.AddTransient<AIAgent>(sp =>
        {
            var chatClient = sp.GetRequiredService<IChatClient>();
            var userRepo = sp.GetRequiredService<IUserRepository>();

            return chatClient.CreateAIAgent(new ChatClientAgentOptions
            {
                Instructions = "You are a helpful assistant.",
                Name = "Assistant",
                AIContextProviderFactory = ctx => new UserProfileProvider(
                    chatClient,
                    userRepo,
                    ctx.SerializedState,
                    ctx.JsonSerializerOptions)
            });
        });

        return services;
    }
}
```

## Pattern 3: Enriched Thread Builder

Standardize thread creation with appropriate context providers.

```csharp
public class ThreadBuilder
{
    private readonly IChatClient _chatClient;
    private readonly HttpClient _mem0Client;
    private readonly ITextSearch _textSearch;

    public ThreadBuilder(IChatClient chatClient, HttpClient mem0Client, ITextSearch textSearch)
    {
        _chatClient = chatClient;
        _mem0Client = mem0Client;
        _textSearch = textSearch;
    }

    public AgentThread CreateForUser(string userId, ThreadCapabilities capabilities)
    {
        var thread = new ChatHistoryAgentThread();

        if (capabilities.HasFlag(ThreadCapabilities.LongTermMemory))
        {
            thread.AIContextProviders.Add(new Mem0Provider(_mem0Client, new()
            {
                UserId = userId
            }));
        }

        if (capabilities.HasFlag(ThreadCapabilities.ConversationTracking))
        {
            thread.AIContextProviders.Add(new WhiteboardProvider(_chatClient));
        }

        if (capabilities.HasFlag(ThreadCapabilities.KnowledgeRetrieval))
        {
            thread.AIContextProviders.Add(new TextSearchProvider(_textSearch, new()
            {
                SearchTime = TextSearchProviderOptions.RagBehavior.OnDemandFunctionCalling
            }));
        }

        return thread;
    }
}

[Flags]
public enum ThreadCapabilities
{
    None = 0,
    LongTermMemory = 1,
    ConversationTracking = 2,
    KnowledgeRetrieval = 4,
    All = LongTermMemory | ConversationTracking | KnowledgeRetrieval
}

// Usage
var thread = threadBuilder.CreateForUser("user123", ThreadCapabilities.All);
```

## Pattern 4: Resilient Agent Wrapper

Add retry logic, circuit breaking, and observability.

```csharp
public class ResilientAgent
{
    private readonly AIAgent _agent;
    private readonly ILogger<ResilientAgent> _logger;
    private readonly ResiliencePipeline _pipeline;

    public ResilientAgent(AIAgent agent, ILogger<ResilientAgent> logger)
    {
        _agent = agent;
        _logger = logger;

        _pipeline = new ResiliencePipelineBuilder()
            .AddRetry(new RetryStrategyOptions
            {
                MaxRetryAttempts = 3,
                Delay = TimeSpan.FromSeconds(1),
                BackoffType = DelayBackoffType.Exponential,
                UseJitter = true,
                ShouldHandle = new PredicateBuilder()
                    .Handle<HttpRequestException>()
                    .Handle<TaskCanceledException>()
            })
            .AddCircuitBreaker(new CircuitBreakerStrategyOptions
            {
                FailureRatio = 0.5,
                MinimumThroughput = 10,
                BreakDuration = TimeSpan.FromSeconds(30)
            })
            .AddTimeout(TimeSpan.FromMinutes(2))
            .Build();
    }

    public async Task<AgentRunResponse> RunAsync(
        string message,
        AgentThread thread,
        CancellationToken ct = default)
    {
        using var activity = AgentDiagnostics.StartActivity("agent.run");

        return await _pipeline.ExecuteAsync(async token =>
        {
            var response = await _agent.RunAsync(message, thread, cancellationToken: token);

            activity?.SetTag("response.length", response.Text?.Length ?? 0);
            activity?.SetTag("messages.count", response.Messages.Count);

            return response;
        }, ct);
    }
}
```

## Error Handling Strategies

### Differentiate Error Types

```csharp
public async Task<AgentRunResponse> RunWithErrorHandlingAsync(
    string message,
    AgentThread thread)
{
    try
    {
        return await _agent.RunAsync(message, thread);
    }
    catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests)
    {
        // Rate limit - retry with backoff
        _logger.LogWarning("Rate limited, retrying...");
        await Task.Delay(TimeSpan.FromSeconds(5));
        return await _agent.RunAsync(message, thread);
    }
    catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.Unauthorized)
    {
        // Auth failure - fail fast, don't retry
        _logger.LogError("Authentication failed");
        throw;
    }
    catch (TaskCanceledException)
    {
        // Timeout - may retry with longer timeout
        _logger.LogWarning("Request timed out");
        throw;
    }
    catch (JsonException ex)
    {
        // Model returned garbage - retry with different temperature
        _logger.LogWarning(ex, "Model response parsing failed");
        throw;
    }
}
```

### Agent Failure Modes

| Failure Mode | Symptom | Recovery |
|--------------|---------|----------|
| Thinking failure | Model outputs garbage | Retry with lower temperature |
| Acting failure | Tool call fails | Retry tool, or skip and continue |
| Observing failure | Can't parse tool result | Simplify output format |
| Loop failure | Stuck in infinite loop | Add iteration limit, break condition |

## Testing Strategies

### Three-Tier Approach

```csharp
// 1. Unit Tests - Deterministic components
[Fact]
public async Task Tool_GetWeather_ReturnsFormattedString()
{
    var result = GetWeather("Seattle");
    Assert.Contains("Seattle", result);
}

// 2. Agent Evaluation - Behavioral tests
[Fact]
public async Task Agent_AnswersWeatherQuestion()
{
    var agent = CreateTestAgent();
    var thread = agent.GetNewThread();

    var response = await agent.RunAsync("What's the weather in Seattle?", thread);

    // Check behavior, not exact output
    Assert.Contains("Seattle", response.Text, StringComparison.OrdinalIgnoreCase);
    Assert.True(response.Messages.Any(m => m.Role == ChatRole.Tool),
        "Should have called weather tool");
}

// 3. Integration Tests - Full scenario
[Fact]
public async Task Workflow_ProcessesCustomerRequest()
{
    var workflow = CreateSupportWorkflow();
    var runtime = new InProcessRuntime();
    await runtime.StartAsync();

    var result = await workflow.InvokeAsync(
        "I need to return my order #12345",
        runtime);

    var output = await result.GetValueAsync();

    // Verify workflow completed with appropriate response
    Assert.Contains("return", output, StringComparison.OrdinalIgnoreCase);
}
```

### Multi-Trial Evaluation

```csharp
// Run multiple trials to assess consistency
public async Task<EvaluationResult> EvaluateAgentAsync(
    AIAgent agent,
    string prompt,
    Func<string, bool> successCriteria,
    int trials = 5)
{
    var results = new List<bool>();

    for (int i = 0; i < trials; i++)
    {
        var thread = agent.GetNewThread();
        var response = await agent.RunAsync(prompt, thread);
        results.Add(successCriteria(response.Text));
    }

    return new EvaluationResult
    {
        PassRate = results.Count(r => r) / (double)trials,
        AllPassed = results.All(r => r),  // pass^k - consistency
        AnyPassed = results.Any(r => r)   // pass@k - capability
    };
}
```

## Migration from Semantic Kernel

### Before (SK)

```csharp
// Semantic Kernel pattern
Kernel kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(modelId, apiKey)
    .Build();

KernelFunction weatherFunc = KernelFunctionFactory.CreateFromMethod(
    (string location) => $"Weather in {location}: Sunny",
    "GetWeather",
    "Gets weather for a location");

KernelPlugin plugin = KernelPluginFactory.CreateFromFunctions(
    "Weather", [weatherFunc]);
kernel.Plugins.Add(plugin);

ChatCompletionAgent agent = new()
{
    Instructions = "You help with weather queries.",
    Kernel = kernel
};

ChatHistory history = new();
await agent.InvokeAsync(history, "What's the weather in Seattle?");
```

### After (Agent Framework)

```csharp
// Agent Framework pattern
[Description("Gets weather for a location")]
static string GetWeather(string location) => $"Weather in {location}: Sunny";

AIAgent agent = new OpenAIClient(apiKey)
    .GetChatClient(modelId)
    .AsIChatClient()
    .CreateAIAgent(
        instructions: "You help with weather queries.",
        tools: [AIFunctionFactory.Create(GetWeather)]);

AgentThread thread = agent.GetNewThread();
await agent.RunAsync("What's the weather in Seattle?", thread);
```

### Migration Checklist

- [ ] Replace `Kernel` with `AIAgent` via `CreateAIAgent()`
- [ ] Replace `ChatHistory` with `AgentThread`
- [ ] Replace `[KernelFunction]` with `[Description]`
- [ ] Replace `KernelFunctionFactory` with `AIFunctionFactory`
- [ ] Replace `IPromptFilter` with `AIContextBehavior`
- [ ] Update namespace from `Microsoft.SemanticKernel.*` to `Microsoft.Extensions.AI.*`
- [ ] Implement thread serialization for state persistence
- [ ] Add context providers for memory (replaces separate memory stores)

## Observability

### Aspire Integration ("AI Sparkles")

Aspire dashboard shows AI operations with special sparkle icons (✨). Invaluable for debugging agent workflows.

**Setup:**
```csharp
var builder = DistributedApplication.CreateBuilder(args);

var backend = builder.AddProject<Projects.Backend>("backend")
    .WithOpenTelemetry();  // Enables AI trace collection

builder.Build().Run();
```

**What you see in Aspire traces:**
- Question/prompt submitted
- Semantic search operations
- Tool calls (function invocations)
- LLM responses
- Full timing breakdown

**Debugging workflow:**
1. Open Aspire dashboard → Traces
2. Look for sparkle icons (AI operations)
3. Expand to see: prompt → tool calls → response
4. Check timing for bottlenecks

### Custom Diagnostics

```csharp
public static class AgentDiagnostics
{
    private static readonly ActivitySource Source = new("AgentFramework");

    public static Activity? StartActivity(string name)
    {
        return Source.StartActivity(name, ActivityKind.Internal);
    }
}

// Configure in startup
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .AddSource("AgentFramework")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddOtlpExporter());
```

### Key Metrics to Track

| Metric | Why |
|--------|-----|
| Agent run duration | Performance baseline |
| Token consumption | Cost tracking |
| Tool call success rate | Reliability |
| Handoff frequency | Workflow efficiency |
| Context provider latency | Memory system health |
| Thread serialization size | Storage costs |

## Production Checklist

- [ ] Thread persistence implemented and tested
- [ ] Context providers have serialization constructors
- [ ] Error handling with appropriate retry strategies
- [ ] Circuit breaker for external dependencies
- [ ] Observability (traces, metrics, logs)
- [ ] Rate limiting for API calls
- [ ] Timeout configuration for long-running operations
- [ ] Graceful degradation when memory services unavailable
- [ ] Termination conditions for orchestrations
- [ ] Load testing with realistic conversation patterns
