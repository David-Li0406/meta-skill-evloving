---
name: copilot-sdk
description: Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, or integrating with MCP servers. Triggers on Copilot SDK, GitHub SDK, agentic app, embed Copilot, programmable agent.
---

# GitHub Copilot SDK

Embed Copilot's agentic workflows in any application using Python, TypeScript, Go, or .NET.

## Overview

The GitHub Copilot SDK exposes the same engine behind Copilot CLI: a production-tested agent runtime you can invoke programmatically. No need to build your own orchestration - you define agent behavior, Copilot handles planning, tool invocation, file edits, and more.

## Prerequisites

1. **GitHub Copilot CLI** installed and authenticated
2. **Language runtime**: Node.js 18+, Python 3.8+, Go 1.21+, or .NET 8.0+

Verify CLI: `copilot --version`

## Installation

### Node.js/TypeScript
```bash
npm install @github/copilot-sdk
```

### Python
```bash
pip install github-copilot-sdk
```

### Go
```bash
go get github.com/github/copilot-sdk/go
```

### .NET
```bash
dotnet add package GitHub.Copilot.SDK
```

## Quick Start

### TypeScript
```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({
  model: "gpt-5"
});

const response = await session.sendAndWait({
  prompt: "What is 2+2?"
});

console.log(response);
await client.stop();
```

### Python
```python
import asyncio
from copilot import CopilotClient

async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({"model": "gpt-5"})

    done = asyncio.Event()
    def on_event(event):
        if event.type.value == "assistant.message":
            print(event.data.content)
        elif event.type.value == "session.idle":
            done.set()

    session.on(on_event)
    await session.send({"prompt": "What is 2+2?"})
    await done.wait()
    await session.destroy()
    await client.stop()

asyncio.run(main())
```

### Go
```go
package main

import (
    "fmt"
    "log"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient(&copilot.ClientOptions{LogLevel: "error"})
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, _ := client.CreateSession(&copilot.SessionConfig{Model: "gpt-5"})
    defer session.Destroy()

    done := make(chan bool)
    session.On(func(event copilot.SessionEvent) {
        if event.Type == "assistant.message" && event.Data.Content != nil {
            fmt.Println(*event.Data.Content)
        }
        if event.Type == "session.idle" {
            close(done)
        }
    })
    session.Send(copilot.MessageOptions{Prompt: "What is 2+2?"})
    <-done
}
```

### .NET (C#)
```csharp
await using var client = new CopilotClient();
await client.StartAsync();

await using var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });

var done = new TaskCompletionSource();
session.On(evt => {
    if (evt is AssistantMessageEvent msg) Console.WriteLine(msg.Data.Content);
    else if (evt is SessionIdleEvent) done.SetResult();
});

await session.SendAsync(new MessageOptions { Prompt = "What is 2+2?" });
await done.Task;
```

## Client Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `cliPath` | Path to Copilot CLI executable | System PATH |
| `cliUrl` | Connect to existing server (e.g., "localhost:8080") | None |
| `port` | Server communication port | Random |
| `useStdio` | Use stdio transport instead of TCP | true |
| `logLevel` | Logging verbosity | "info" |
| `autoStart` | Launch server automatically | true |
| `autoRestart` | Restart on crashes | true |
| `cwd` | Working directory for CLI process | Inherited |

### TypeScript Example
```typescript
const client = new CopilotClient({
  cliPath: "/custom/path/to/copilot",
  port: 8080,
  logLevel: "debug",
  autoStart: true
});
```

## Session Configuration

| Option | Description |
|--------|-------------|
| `model` | LLM to use ("gpt-5", "claude-sonnet-4.5", etc.) |
| `sessionId` | Custom session identifier |
| `tools` | Custom tool definitions |
| `systemMessage` | Override default system prompt |
| `streaming` | Enable incremental response chunks |
| `availableTools` | Whitelist of permitted tools |
| `excludedTools` | Blacklist of disabled tools |

## Streaming Responses

Enable real-time output by setting `streaming: true`:

### TypeScript
```typescript
const session = await client.createSession({
  model: "gpt-5",
  streaming: true
});

session.on("assistant.message_delta", (event) => {
  process.stdout.write(event.data.deltaContent);
});

session.on("session.idle", () => {
  console.log("\nDone!");
});

await session.send({ prompt: "Explain quantum computing" });
```

### Python
```python
session = await client.create_session({
    "model": "gpt-5",
    "streaming": True
})

def on_event(event):
    if event.type.value == "assistant.message_delta":
        print(event.data.delta_content, end="", flush=True)
    elif event.type.value == "session.idle":
        print("\nDone!")

session.on(on_event)
await session.send({"prompt": "Explain quantum computing"})
```

## Event Types

| Event | Description |
|-------|-------------|
| `user.message` | User input added |
| `assistant.message` | Complete model response |
| `assistant.message_delta` | Streaming response chunk |
| `assistant.reasoning` | Model reasoning (model-dependent) |
| `assistant.reasoning_delta` | Streaming reasoning chunk |
| `tool.execution_start` | Tool invocation started |
| `tool.execution_complete` | Tool execution finished |
| `session.idle` | No active processing |
| `session.error` | Error occurred |

## Custom Tools

Define tools that Copilot can invoke during reasoning:

### TypeScript (with Zod)
```typescript
import { defineTool } from "@github/copilot-sdk";
import { z } from "zod";

const weatherTool = defineTool({
  name: "get_weather",
  description: "Get current weather for a city",
  parameters: z.object({
    city: z.string().describe("City name"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius")
  }),
  handler: async ({ city, units }) => {
    const weather = await fetchWeather(city);
    return { temperature: weather.temp, conditions: weather.conditions };
  }
});

const session = await client.createSession({
  model: "gpt-5",
  tools: [weatherTool]
});
```

### Python (with Pydantic)
```python
from pydantic import BaseModel, Field
from copilot import CopilotClient, define_tool

class WeatherParams(BaseModel):
    city: str = Field(description="City name")
    units: str = Field(default="celsius", description="Temperature units")

@define_tool(description="Get current weather for a city")
async def get_weather(params: WeatherParams) -> dict:
    weather = await fetch_weather(params.city)
    return {"temperature": weather.temp, "conditions": weather.conditions}

session = await client.create_session({
    "model": "gpt-5",
    "tools": [get_weather]
})
```

### Go
```go
type WeatherParams struct {
    City  string `json:"city" jsonschema:"City name"`
    Units string `json:"units" jsonschema:"Temperature units"`
}

weatherTool := copilot.DefineTool("get_weather",
    "Get current weather for a city",
    func(params WeatherParams, inv copilot.ToolInvocation) (any, error) {
        weather, err := fetchWeather(params.City)
        if err != nil {
            return nil, err
        }
        return map[string]any{
            "temperature": weather.Temp,
            "conditions":  weather.Conditions,
        }, nil
    })

session, _ := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    Tools: []copilot.Tool{weatherTool},
})
```

### .NET (with Microsoft.Extensions.AI)
```csharp
using Microsoft.Extensions.AI;
using System.ComponentModel;

var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Tools = [
        AIFunctionFactory.Create(
            async ([Description("City name")] string city) => {
                var weather = await FetchWeatherAsync(city);
                return new { weather.Temp, weather.Conditions };
            },
            "get_weather",
            "Get current weather for a city"),
    ]
});
```

## Session Persistence

Save and resume conversations across restarts:

### Create with Custom ID
```typescript
const session = await client.createSession({
  sessionId: "user-123-conversation",
  model: "gpt-5"
});
```

### Resume Session
```typescript
const session = await client.resumeSession("user-123-conversation");
// Conversation context is restored
await session.send({ prompt: "What did we discuss earlier?" });
```

### List and Delete Sessions
```typescript
const sessions = await client.listSessions();
await client.deleteSession("old-session-id");
```

## Error Handling

```typescript
try {
  await client.start();
  const session = await client.createSession({ model: "gpt-5" });
  const response = await session.sendAndWait(
    { prompt: "Hello!" },
    30000 // timeout in ms
  );
} catch (error) {
  if (error.code === "ENOENT") {
    console.error("Copilot CLI not installed");
  } else if (error.code === "ECONNREFUSED") {
    console.error("Cannot connect to Copilot server");
  } else {
    console.error("Error:", error.message);
  }
} finally {
  await client.stop();
}
```

## Graceful Shutdown

```typescript
process.on("SIGINT", async () => {
  console.log("Shutting down...");
  await client.stop();
  process.exit(0);
});
```

## Architecture

```
Your Application
       |
  SDK Client
       | JSON-RPC
  Copilot CLI (server mode)
       |
  GitHub (models, auth)
```

The SDK manages the CLI process lifecycle automatically. All communication happens via JSON-RPC over stdio or TCP.

## BYOK (Bring Your Own Key)

The SDK supports using your own API keys:

```typescript
const session = await client.createSession({
  model: "gpt-5",
  provider: {
    apiKey: process.env.OPENAI_API_KEY,
    endpoint: "https://api.openai.com/v1"
  }
});
```

## Available Models

Query available models at runtime:

```typescript
const models = await client.getModels();
// Returns: ["gpt-5", "gpt-4.1", "claude-sonnet-4.5", ...]
```

## Best Practices

1. **Always cleanup**: Use `try-finally` or `defer` to ensure `client.stop()` is called
2. **Set timeouts**: Use `sendAndWait` with timeout for long operations
3. **Handle events**: Subscribe to error events for robust error handling
4. **Use streaming**: Enable streaming for better UX on long responses
5. **Persist sessions**: Use custom session IDs for multi-turn conversations
6. **Define clear tools**: Write descriptive tool names and descriptions

## Common Patterns

### Multi-turn Conversation
```typescript
const session = await client.createSession({ model: "gpt-5" });

await session.sendAndWait({ prompt: "My name is Alice" });
await session.sendAndWait({ prompt: "What's my name?" });
// Response: "Your name is Alice"
```

### File Attachments
```typescript
await session.send({
  prompt: "Analyze this file",
  attachments: [{
    type: "file",
    path: "./data.csv",
    displayName: "Sales Data"
  }]
});
```

### Abort Long Operations
```typescript
const timeoutId = setTimeout(() => {
  session.abort();
}, 60000);

session.on("session.idle", () => {
  clearTimeout(timeoutId);
});
```

## Resources

- **GitHub Repository**: https://github.com/github/copilot-sdk
- **Getting Started**: https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md
- **Cookbook**: https://github.com/github/copilot-sdk/tree/main/cookbook
- **Samples**: https://github.com/github/copilot-sdk/tree/main/samples
- **Custom Instructions**: https://github.com/github/awesome-copilot

## Status

This SDK is in **Technical Preview** and may have breaking changes. Not recommended for production use yet.
