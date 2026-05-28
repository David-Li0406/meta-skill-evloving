# Context Providers: Policy-Based Memory

Context providers are not "memory injection" — they're **policy enforcement**. RAG answers "what's semantically similar?" — Policy answers "should this enter the prompt at all, in what form, and should it decay?"

## The Capsule Pattern

Bounded, fixed-budget context chunks injected as system messages:

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Run                            │
├─────────────────────────────────────────────────────────┤
│  1. AF collects: current turn + thread history         │
│  2. For each ContextProvider (ordered):                │
│     └─ OnModelInvokeAsync() → returns AIContextPart    │
│        └─ Provider applies POLICY: budget, gating,     │
│           retrieval, compression → "capsule"           │
│  3. Capsules prepended as system messages              │
│  4. Model inference                                     │
│  5. OnNewMessageAsync() for each provider              │
│     └─ Provider applies POLICY: selection,             │
│        schema, decay, dedup → WRITE memories           │
└─────────────────────────────────────────────────────────┘
```

**Pattern characteristics:**
- Each provider controls its own token budget
- Context assembly is **deterministic and composable**
- You can audit exactly what's in prompts (compliance/debugging)

## Policy Decisions

| Policy | What It Decides |
|--------|-----------------|
| Selection | What becomes memory |
| Schema | How it's compressed/represented |
| Scope | Where it lives (user/thread/global) |
| Gating | When it's retrieved |
| Decay | When it mutates or expires |
| Noise avoidance | When it should NOT be used |

## Two-Plane Architecture

| Plane | Carrier | Scope | Example |
|-------|---------|-------|---------|
| **Ephemeral** | AgentThread | Session | Current conversation |
| **Persistent** | Mem0 + Vector Store | Cross-session | User preferences |

Both connect through the **same Context Provider hooks**.

## RED FLAG: Serialization Constructor Required

**Thread deserialization WILL FAIL without a serialization constructor.** This is the #1 cause of "memory lost between sessions" bugs.

```csharp
// ❌ BROKEN - thread persistence fails silently
public class MyProvider : AIContextBehavior
{
    public MyProvider(IChatClient client) { }
}

// ✅ WORKS - supports thread persistence
public class MyProvider : AIContextBehavior
{
    public MyProvider(IChatClient client) { }

    // REQUIRED for thread serialization
    public MyProvider(
        IChatClient client,
        string? serializedState,        // Restored state (may be null)
        JsonSerializerOptions? options) // Serialization options
    {
        if (!string.IsNullOrEmpty(serializedState))
        {
            _state = JsonSerializer.Deserialize<MyState>(serializedState, options);
        }
    }
}
```

If your context provider has state that must persist across sessions, you MUST implement both constructors.

## AIContextBehavior Interface

```csharp
public abstract class AIContextBehavior
{
    // Called when thread is created
    public virtual Task OnThreadCreatedAsync(string? threadId, CancellationToken ct) { }

    // Called for each new message - use for WRITING memories
    public virtual Task OnNewMessageAsync(string? threadId, ChatMessage msg, CancellationToken ct) { }

    // Called before model invoke - use for READING/INJECTING context
    public abstract Task<AIContextPart> OnModelInvokeAsync(
        ICollection<ChatMessage> newMessages, CancellationToken ct);

    // Called when thread is deleted
    public virtual Task OnThreadDeleteAsync(string? threadId, CancellationToken ct) { }

    // Suspend/Resume for long-running operations
    public virtual Task OnSuspendAsync(string? threadId, CancellationToken ct) { }
    public virtual Task OnResumeAsync(string? threadId, CancellationToken ct) { }
}
```

## Built-in Providers

### Mem0Provider (Long-Term Cross-Session Memory)

Mem0 is not just a vector store — it's the **policy layer**:

```csharp
using var httpClient = new HttpClient { BaseAddress = new Uri("https://api.mem0.ai") };
httpClient.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Token", "<API_Key>");

var mem0Provider = new Mem0Provider(httpClient, new Mem0ProviderOptions
{
    UserId = "user123",           // Required: scope memories to user
    // Optional additional scoping:
    // ApplicationId = "myapp",
    // AgentId = "support-agent",
    // ThreadId = thread.Id
});

thread.AIContextProviders.Add(mem0Provider);
```

**Mem0 vs Azure AI Search:**

| Mem0 Does | Azure AI Search Does |
|-----------|---------------------|
| Extract "user prefers dark mode" from "I hate bright screens" | Store embeddings |
| Decide if new info or duplicate | Return top-k similar |
| Compress 5 similar memories into 1 | Index management |
| Expire memories after TTL | Nothing |
| Decide "this query doesn't need memory" | Always returns results |

**Azure AI Search as Mem0 backend:**

```python
# Python example - C# pattern similar
config = {
    "vector_store": {
        "provider": "azure_ai_search",
        "config": {
            "service_name": "my-search-service",
            "collection_name": "agent-memories",
        },
    },
    "llm": {"provider": "azure_openai", "config": {"model": "gpt-4o-mini"}},
    "embeddings": {"provider": "azure_openai", "config": {"deployment_name": "text-embedding-ada-002"}},
}
memory = Memory.from_config(config)
```

### WhiteboardProvider (Short-Term Conversation Context)

Captures requirements, proposals, decisions, actions within a conversation:

```csharp
var whiteboardProvider = new WhiteboardProvider(chatClient);
thread.AIContextProviders.Add(whiteboardProvider);

await agent.InvokeAsync("I want to book a trip to Paris for 2 people.", thread);
// Whiteboard now contains: "Requirement: Trip to Paris, 2 travelers"
```

### TextSearchProvider (RAG Integration)

```csharp
var options = new TextSearchProviderOptions
{
    SearchTime = TextSearchProviderOptions.RagBehavior.OnDemandFunctionCalling,
    // Or: RagBehavior.BeforeModelInvoke for automatic retrieval
};
var provider = new TextSearchProvider(textSearch, options);
thread.AIContextProviders.Add(provider);
```

### ContextualFunctionProvider (Dynamic Function Selection)

Selects only relevant functions based on semantic similarity:

```csharp
var embeddingGenerator = new AzureOpenAIClient(endpoint, credential)
    .GetEmbeddingClient("text-embedding-ada-002")
    .AsIEmbeddingGenerator();

thread.AIContextProviders.Add(new ContextualFunctionProvider(
    vectorStore: new InMemoryVectorStore(new InMemoryVectorStoreOptions {
        EmbeddingGenerator = embeddingGenerator
    }),
    vectorDimensions: 1536,
    functions: GetAllAvailableFunctions(),  // e.g., 100 functions
    maxNumberOfFunctions: 3                  // Only top 3 advertised to model
));

// REQUIRED: Set this flag when using ContextualFunctionProvider
agent.Options.UseImmutableKernel = true;
```

**CRITICAL**: You MUST set `UseImmutableKernel = true` when using `ContextualFunctionProvider`. Without this flag, the provider cannot dynamically modify which functions are advertised to the model. Omitting this causes silent failures where function selection doesn't work.

## Combining Providers (Layered Context)

```csharp
public AgentThread CreateEnrichedThread(string userId)
{
    var thread = new ChatHistoryAgentThread();

    // Layer 1: Long-term user memory (cross-session)
    thread.AIContextProviders.Add(new Mem0Provider(httpClient, new() { UserId = userId }));

    // Layer 2: Short-term conversation context (within session)
    thread.AIContextProviders.Add(new WhiteboardProvider(chatClient));

    // Layer 3: RAG for external knowledge
    thread.AIContextProviders.Add(new TextSearchProvider(textSearch));

    // Layer 4: Dynamic function selection
    thread.AIContextProviders.Add(new ContextualFunctionProvider(...));

    return thread;
}
```

## Custom Provider Implementation

```csharp
public class UserProfileProvider : AIContextBehavior
{
    private readonly IChatClient _chatClient;
    private readonly IUserRepository _userRepo;
    private UserProfile _profile = new();

    // Standard constructor
    public UserProfileProvider(IChatClient chatClient, IUserRepository userRepo)
    {
        _chatClient = chatClient;
        _userRepo = userRepo;
    }

    // REQUIRED: Serialization constructor for thread persistence
    public UserProfileProvider(
        IChatClient chatClient,
        IUserRepository userRepo,
        string? serializedState,
        JsonSerializerOptions? options)
    {
        _chatClient = chatClient;
        _userRepo = userRepo;
        if (!string.IsNullOrEmpty(serializedState))
        {
            _profile = JsonSerializer.Deserialize<UserProfile>(serializedState, options) ?? new();
        }
    }

    // READ: Inject context before model invoke
    public override async Task<AIContextPart> OnModelInvokeAsync(
        ICollection<ChatMessage> newMessages,
        CancellationToken ct)
    {
        // Apply POLICY: gating, budget, compression
        if (_profile.IsEmpty)
            return new AIContextPart(); // No context to inject

        return new AIContextPart
        {
            Instructions = $"User: {_profile.Name}, Preferences: {_profile.PreferencesSummary}"
        };
    }

    // WRITE: Extract memories after model response
    public override async Task OnNewMessageAsync(
        string? threadId,
        ChatMessage message,
        CancellationToken ct)
    {
        if (message.Role != ChatRole.User) return;

        // Apply POLICY: selection, schema, dedup
        var extracted = await ExtractUserInfo(message.Text, ct);
        if (extracted != null)
        {
            _profile.Merge(extracted);
            await _userRepo.SaveAsync(_profile, ct);
        }
    }

    // Serialize for thread persistence
    public string Serialize(JsonSerializerOptions? options = null)
        => JsonSerializer.Serialize(_profile, options);
}

// Register via factory for proper deserialization
AIAgent agent = chatClient.CreateAIAgent(new ChatClientAgentOptions
{
    Instructions = "You are a helpful assistant.",
    AIContextProviderFactory = ctx => new UserProfileProvider(
        chatClient.AsIChatClient(),
        userRepo,
        ctx.SerializedState,
        ctx.JsonSerializerOptions
    )
});
```

## Context Window Management

### Truncation

```csharp
var reducer = new ChatHistoryTruncationReducer(
    targetCount: 15,     // Ideal maximum messages
    thresholdCount: 5    // Buffer before triggering
);
```

**Use when**: Real-time chatbots, resource-constrained environments

### Summarization

Merges older messages into concise summary tagged with `__summary__` metadata.

**Use when**: Long dialogues where historical context matters

## Common Gotchas

### Missing Serialization Constructor

```csharp
// ❌ Thread deserialization will FAIL
public class MyProvider : AIContextBehavior
{
    public MyProvider(IChatClient client) { }
    // Missing: constructor with serializedState parameter
}

// ✅ Supports thread persistence
public class MyProvider : AIContextBehavior
{
    public MyProvider(IChatClient client) { }
    public MyProvider(IChatClient client, string? serializedState, JsonSerializerOptions? options)
    {
        // Restore state
    }
}
```

### Blocking in Async Methods

```csharp
// ❌ Blocks thread pool
public override async Task<AIContextPart> OnModelInvokeAsync(...)
{
    var data = httpClient.GetStringAsync(url).Result; // BLOCKS!
}

// ✅ Properly async
public override async Task<AIContextPart> OnModelInvokeAsync(...)
{
    var data = await httpClient.GetStringAsync(url);
}
```

### Unhandled Exceptions Crash Agent Run

```csharp
// ❌ Exception propagates, fails entire run
public override async Task OnNewMessageAsync(...)
{
    await externalService.SaveAsync(data); // Can throw!
}

// ✅ Graceful degradation
public override async Task OnNewMessageAsync(...)
{
    try
    {
        await externalService.SaveAsync(data);
    }
    catch (Exception ex)
    {
        _logger.LogWarning(ex, "Memory save failed, continuing");
    }
}
```

### Provider Ordering

Order of `AIContextProviders` may affect how contexts combine. Place more critical providers earlier.

## When to Use What

| Scenario | Provider |
|----------|----------|
| Simple RAG over documents | `TextSearchProvider` or AI Search directly |
| Conversational memory that evolves | `Mem0Provider` |
| Track conversation goals/decisions | `WhiteboardProvider` |
| Large function catalog | `ContextualFunctionProvider` |
| Custom business rules | Custom `AIContextBehavior` |
| Full control, custom policies | Custom provider + your own vector store |
