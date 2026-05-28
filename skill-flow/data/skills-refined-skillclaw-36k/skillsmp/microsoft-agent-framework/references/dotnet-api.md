# .NET API Reference

## Installation

```bash
dotnet add package Microsoft.Agents.AI --prerelease
dotnet add package Microsoft.Agents.AI.OpenAI --prerelease
dotnet add package Azure.AI.OpenAI --prerelease
dotnet add package Azure.Identity
```

---

## ChatClientAgent

Primary agent class. DO NOT create custom agent classes.

```csharp
using Microsoft.Agents.AI;

public class ChatClientAgent : AIAgent
{
    public ChatClientAgent(
        IChatClient chatClient,
        string? instructions = null,
        string? name = null,
        IEnumerable<AITool>? tools = null
    );
    
    public Task<AgentResult> InvokeAsync(
        string input,
        AgentThread? thread = null,
        CancellationToken cancellationToken = default
    );
    
    public IAsyncEnumerable<StreamingUpdate> InvokeStreamingAsync(
        string input,
        AgentThread? thread = null,
        CancellationToken cancellationToken = default
    );
}
```

### Basic Usage

```csharp
using Microsoft.Agents.AI;
using Azure.AI.OpenAI;
using Azure.Identity;

// Create OpenAI client
var azureClient = new AzureOpenAIClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!),
    new AzureCliCredential()
);
var chatClient = azureClient.GetChatClient("gpt-4o");

// Create agent
var agent = new ChatClientAgent(
    chatClient,
    instructions: "You are a helpful assistant.",
    name: "my-agent"
);

// Run
var result = await agent.InvokeAsync("Hello!");
Console.WriteLine(result.Text);
```

---

## Creating Agents from Clients

Factory extension methods:

```csharp
using Microsoft.Agents.AI;

// Direct from chat client
var agent = chatClient.CreateAIAgent(
    instructions: "You help with code.",
    name: "code-helper",
    tools: new[] { myTool }
);
```

---

## Function Tools

```csharp
using Microsoft.Agents.AI;
using System.ComponentModel;

// Define tool as static method with attributes
[Description("Get weather for a location")]
static string GetWeather(
    [Description("City name")] string location,
    [Description("Units: celsius or fahrenheit")] string units = "celsius")
{
    return $"Weather in {location}: 22°{units[0].ToString().ToUpper()}";
}

// Create AITool from method
var weatherTool = AIFunctionFactory.Create(GetWeather);

// Use with agent
var agent = new ChatClientAgent(
    chatClient,
    instructions: "You help with weather queries.",
    tools: new[] { weatherTool }
);
```

### Async Tools

```csharp
[Description("Fetch data from URL")]
static async Task<string> FetchData(
    [Description("URL to fetch")] string url)
{
    using var client = new HttpClient();
    return await client.GetStringAsync(url);
}

var fetchTool = AIFunctionFactory.Create(FetchData);
```

---

## MCP Tools

Using the MCP C# SDK:

```csharp
using ModelContextProtocol.Client;
using Microsoft.Agents.AI;

// Create MCP client
await using var mcpClient = await McpClientFactory.CreateAsync(
    new StdioClientTransport(new()
    {
        Name = "filesystem",
        Command = "npx",
        Arguments = new[] { "-y", "@modelcontextprotocol/server-filesystem", "/path" }
    })
);

// Get tools from MCP server
var mcpTools = await mcpClient.ListToolsAsync();
var tools = mcpTools.Cast<AITool>().ToArray();

// Create agent with MCP tools
var agent = chatClient.CreateAIAgent(
    instructions: "You can browse files.",
    tools: tools
);
```

---

## AgentThread

State management for conversations:

```csharp
using Microsoft.Agents.AI;

var thread = new AgentThread();

// First turn
var result1 = await agent.InvokeAsync("Hello", thread);

// Second turn (has context)
var result2 = await agent.InvokeAsync("What did I say?", thread);
```

---

## Streaming

```csharp
await foreach (var update in agent.InvokeStreamingAsync("Tell me a story"))
{
    if (update.TextDelta != null)
    {
        Console.Write(update.TextDelta);
    }
}
```

---

## Custom Agent (Advanced)

Only if ChatClientAgent doesn't meet your needs:

```csharp
using Microsoft.Agents.AI;

public class MyCustomAgent : AIAgent
{
    public override async Task<AgentResult> InvokeAsync(
        ChatMessage input,
        AgentThread? thread = null,
        CancellationToken cancellationToken = default)
    {
        // Custom logic here
        // But prefer ChatClientAgent when possible
    }
}
```

---

## Middleware

```csharp
using Microsoft.Agents.AI;

public class LoggingMiddleware : IAgentMiddleware
{
    public async Task<AgentResult> InvokeAsync(
        MiddlewareContext context,
        Func<MiddlewareContext, Task<AgentResult>> next)
    {
        Console.WriteLine($"Input: {context.Input}");
        var result = await next(context);
        Console.WriteLine($"Output: {result.Text}");
        return result;
    }
}
```

---

## ASP.NET Integration

```csharp
// Program.cs
builder.Services.AddSingleton<IChatClient>(sp =>
{
    var client = new AzureOpenAIClient(
        new Uri(config["AzureOpenAI:Endpoint"]!),
        new AzureCliCredential()
    );
    return client.GetChatClient(config["AzureOpenAI:Deployment"]!);
});

// Controller
[ApiController]
[Route("api/[controller]")]
public class AgentController : ControllerBase
{
    private readonly IChatClient _chatClient;
    
    public AgentController(IChatClient chatClient)
    {
        _chatClient = chatClient;
    }
    
    [HttpPost("chat")]
    public async Task<IActionResult> Chat([FromBody] ChatRequest request)
    {
        var agent = new ChatClientAgent(
            _chatClient,
            instructions: "You are a helpful assistant."
        );
        
        var result = await agent.InvokeAsync(request.Message);
        return Ok(new { response = result.Text });
    }
}
```

---

## Local Model Configuration

For self-hosted OpenAI-compatible models:

```csharp
using OpenAI;

var client = new OpenAIClient(
    new ApiKeyCredential("not-needed"),
    new OpenAIClientOptions
    {
        Endpoint = new Uri("http://localhost:8000/v1")
    }
);

var chatClient = client.GetChatClient("local-model");
var agent = new ChatClientAgent(chatClient, instructions: "...");
```
