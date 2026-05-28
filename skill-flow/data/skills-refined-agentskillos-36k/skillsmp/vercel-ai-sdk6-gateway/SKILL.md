---
name: vercel-ai-sdk6-gateway
description: "Master integration of Vercel AI Gateway + AI SDK v6 for production AI applications. Use when (1) Building multi-model AI apps with unified routing (2) Creating autonomous agents with ToolLoopAgent (3) Implementing streaming, structured output, or tool calling (4) Setting up provider fallbacks and routing (5) Adding observability, cost tracking, ZDR compliance (6) Integrating MCP servers or web search (7) Building human-in-the-loop approval flows. Covers January 2026 patterns including Output.object(), elementStream, provider metadata, and agent architectures."
---

# Vercel AI SDK v6 + AI Gateway Integration

Unified system for building production AI applications with multi-model access, intelligent routing, and agent workflows.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Your Application                             │
├─────────────────────────────────────────────────────────────────┤
│  AI SDK v6 Layer                                                 │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌────────────────┐    │
│  │streamText│ │generateText│ │ToolLoop  │ │Output.object() │    │
│  │          │ │          │ │  Agent   │ │Output.array()  │    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬────────┘    │
│       └────────────┴────────────┴───────────────┘              │
│                              │                                   │
├──────────────────────────────┼──────────────────────────────────┤
│  AI Gateway Layer            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Unified Endpoint: https://ai-gateway.vercel.sh/v1      │   │
│  │  • Provider Routing (order, only, fallbacks)            │   │
│  │  • Cost Tracking & Observability                        │   │
│  │  • BYOK Support                                         │   │
│  │  • Zero Data Retention (ZDR)                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
├──────────────────────────────┼──────────────────────────────────┤
│  Provider Layer              ▼                                   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │OpenAI  │ │Anthropic│ │Google  │ │xAI     │ │DeepSeek│       │
│  │Azure   │ │Vertex   │ │Bedrock │ │Groq    │ │Mistral │       │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Reference

**Gateway Base URL:** `https://ai-gateway.vercel.sh/v1`
**API Key Env:** `AI_GATEWAY_API_KEY`
**Model Format:** `provider/model-name` (e.g., `anthropic/claude-sonnet-4`)
**Package:** `ai` (v6+), `@ai-sdk/gateway`

## Core Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `generateText` | Non-streaming text + tools | `{ text, output, toolCalls, steps, usage }` |
| `streamText` | Streaming text + tools | `{ textStream, fullStream, partialOutputStream }` |
| `embed` / `embedMany` | Vector embeddings | `{ embedding }` / `{ embeddings }` |
| `generateImage` | Image generation | `{ image }` |
| `ToolLoopAgent` | Autonomous agent | `generate()` / `stream()` |

## Structured Output (AI SDK v6)

SDK v6 deprecates `generateObject`/`streamObject` in favor of unified `Output.*`:

### Object Output
```typescript
import { generateText, Output } from 'ai';
import { z } from 'zod';

const { output } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  output: Output.object({
    schema: z.object({
      name: z.string(),
      ingredients: z.array(z.string()),
      steps: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a pasta recipe',
});
```

### Array Output with Element Streaming
```typescript
import { streamText, Output } from 'ai';
import { z } from 'zod';

const { elementStream } = streamText({
  model: 'openai/gpt-5',
  output: Output.array({
    element: z.object({
      name: z.string(),
      description: z.string(),
    }),
  }),
  prompt: 'Generate 5 product ideas',
});

for await (const item of elementStream) {
  console.log(item); // Each complete, validated item
}
```

### Unstructured JSON
```typescript
const { output } = await generateText({
  model: 'openai/gpt-5',
  output: Output.json(), // Any valid JSON
  prompt: 'Return city temperatures as JSON',
});
```

## Tool Calling

### Basic Tool Definition
```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const { text, toolCalls } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  tools: {
    getWeather: tool({
      description: 'Get weather for a location',
      parameters: z.object({ location: z.string() }),
      execute: async ({ location }) => ({ temp: 72, condition: 'sunny' }),
    }),
  },
  prompt: 'What is the weather in SF?',
});
```

### Human-in-the-Loop Approval
```typescript
const dangerousTool = tool({
  description: 'Delete a file',
  parameters: z.object({ path: z.string() }),
  needsApproval: true, // Requires user confirmation
  execute: async ({ path }) => { /* ... */ },
});
```

### Tool Choice Control
```typescript
// Auto: model decides (default)
toolChoice: 'auto'

// Required: must use a tool before text
toolChoice: 'required'

// Force specific tool first
toolChoice: { type: 'tool', toolName: 'checkInventory' }
```

## ToolLoopAgent (Autonomous Agents)

### Agent Definition
```typescript
import { ToolLoopAgent, stepCountIs, hasToolCall } from 'ai';

const agent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  id: 'research-agent',
  instructions: 'You research topics and synthesize findings.',
  tools: {
    search: searchTool,
    analyze: analyzeTool,
    finalAnswer: tool({
      description: 'Provide final answer',
      parameters: z.object({ answer: z.string() }),
      execute: async ({ answer }) => answer,
    }),
  },
  stopWhen: hasToolCall('finalAnswer'), // Or: stepCountIs(10)
  maxOutputTokens: 4096,
});
```

### Agent Execution
```typescript
// Non-streaming
const result = await agent.generate({ prompt: 'Research quantum computing' });
console.log(result.text, result.steps.length);

// Streaming
const stream = agent.stream({ prompt: 'Research AI trends' });
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

### API Route Integration
```typescript
import { createAgentUIStreamResponse } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  return createAgentUIStreamResponse({
    agent: myAgent,
    messages,
  });
}
```

## Gateway Provider Options

### Provider Routing
```typescript
import { streamText } from 'ai';
import type { GatewayProviderOptions } from '@ai-sdk/gateway';

const result = streamText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Hello',
  providerOptions: {
    gateway: {
      // Provider order (try vertex first, then anthropic)
      order: ['vertex', 'anthropic'],
      
      // Restrict to specific providers only
      only: ['anthropic', 'vertex'],
      
      // Model fallback chain
      models: ['openai/gpt-5-nano', 'google/gemini-2.0-flash'],
      
      // Usage attribution
      user: 'user-123',
      tags: ['chat', 'production'],
      
      // Zero Data Retention
      zeroDataRetention: true,
    } satisfies GatewayProviderOptions,
  },
});
```

### BYOK (Bring Your Own Key)
```typescript
providerOptions: {
  gateway: {
    byok: {
      anthropic: [{ apiKey: process.env.ANTHROPIC_API_KEY }],
      openai: [{ apiKey: process.env.OPENAI_API_KEY }],
    },
  },
}
```

### Combined Provider + Model Options
```typescript
import type { AnthropicProviderOptions } from '@ai-sdk/anthropic';

providerOptions: {
  gateway: {
    order: ['vertex', 'anthropic'],
  } satisfies GatewayProviderOptions,
  anthropic: {
    thinking: { type: 'enabled', budgetTokens: 12000 },
  } satisfies AnthropicProviderOptions,
}
```

## Provider Metadata & Observability

```typescript
const result = streamText({ model: 'openai/gpt-5', prompt: '...' });

const metadata = await result.providerMetadata;
// metadata.gateway.routing - Provider selection info
// metadata.gateway.cost - Credits debited
// metadata.gateway.marketCost - Market rate
// metadata.gateway.generationId - Unique ID for tracking

console.log(`Used: ${metadata.gateway.routing.finalProvider}`);
console.log(`Cost: $${metadata.gateway.cost}`);
```

## Streaming Patterns

### Full Stream Processing
```typescript
const result = streamText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Complex task',
  tools: { /* ... */ },
});

for await (const chunk of result.fullStream) {
  switch (chunk.type) {
    case 'text-delta':
      process.stdout.write(chunk.text);
      break;
    case 'tool-call':
      console.log('Tool:', chunk.toolName, chunk.input);
      break;
    case 'tool-result':
      console.log('Result:', chunk.result);
      break;
    case 'reasoning':
      console.log('Thinking:', chunk.text);
      break;
  }
}
```

### Stream Callbacks
```typescript
streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  onChunk: ({ chunk }) => { /* per-chunk processing */ },
  onFinish: async ({ text, toolCalls, usage, steps }) => {
    console.log('Done:', steps.length, 'steps');
  },
});
```

## MCP Server Integration

```typescript
import { createMCPClient } from '@ai-sdk/mcp';
import { streamText } from 'ai';

// Connect to MCP servers
const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'https://mcp.example.com/sse',
  },
});

const tools = await mcpClient.tools();

const response = await streamText({
  model: 'openai/gpt-5',
  tools,
  prompt: 'Use MCP tools to complete this task',
  onFinish: async () => {
    await mcpClient.close();
  },
});
```

## Next.js Integration

### API Route (App Router)
```typescript
// app/api/chat/route.ts
import { streamText, convertToModelMessages, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  
  const result = streamText({
    model: 'anthropic/claude-sonnet-4',
    messages: await convertToModelMessages(messages),
  });
  
  return result.toUIMessageStreamResponse();
}
```

### Client Hook
```typescript
'use client';
import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  // ... render chat UI
}
```

## Model Discovery

```typescript
import { gateway } from '@ai-sdk/gateway';

const { models } = await gateway.getAvailableModels();

models.forEach(m => {
  console.log(`${m.id}: $${m.pricing?.input}/input`);
});

// Use discovered model
const { text } = await generateText({
  model: models[0].id,
  prompt: 'Hello',
});
```

## Stop Conditions

```typescript
import { stepCountIs, hasToolCall } from 'ai';

// Stop after N steps
stopWhen: stepCountIs(10)

// Stop when specific tool called
stopWhen: hasToolCall('finalAnswer')

// Custom condition
stopWhen: async ({ steps }) => {
  return steps.length >= 10 || 
         steps.at(-1)?.finishReason === 'stop';
}
```

## Error Handling

```typescript
try {
  const { text } = await generateText({ /* ... */ });
} catch (error) {
  if (error.status === 401) {
    // Invalid API key
  } else if (error.status === 429) {
    // Rate limited - Gateway auto-retries
  } else if (error.status === 503) {
    // Provider unavailable - uses fallbacks
  }
}
```

## Popular Models (January 2026)

| Model | Use Case |
|-------|----------|
| `openai/gpt-5` | General, coding |
| `openai/gpt-5-mini` | Fast, cost-effective |
| `anthropic/claude-sonnet-4` | Coding, analysis |
| `anthropic/claude-opus-4` | Complex reasoning |
| `google/gemini-2.0-flash` | Fast multimodal |
| `xai/grok-4` | Real-time knowledge |
| `deepseek/deepseek-r1` | Deep reasoning |

## References

- `references/agent-patterns.md` - ToolLoopAgent architectures and multi-agent systems
- `references/streaming-protocols.md` - Data stream protocol and UI message streams
- `references/openai-compat.md` - Python/Rust/curl Gateway integration
