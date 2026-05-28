---
name: vercel-ai-sdk
description: Use this skill when building AI-powered applications with the Vercel AI SDK, including text generation, chat interfaces, tool definitions, and agent creation.
---

# Vercel AI SDK

The Vercel AI SDK is a TypeScript toolkit for building AI-powered applications with frameworks like React, Next.js, Vue, and Node.js.

## When to Use This Skill

Use this skill when:
- Generating text or structured data with large language models (LLMs)
- Building chatbot UIs with streaming capabilities
- Implementing tool calling and function execution
- Creating AI agents that utilize tools in a loop
- Integrating with AI providers such as OpenAI, Anthropic, and Google

## Quick Reference

### Core Functions

```typescript
import { generateText, streamText, generateObject, streamObject } from 'ai';

// Generate text
const { text } = await generateText({
  model: anthropic('claude-sonnet-4-5-20241022'),
  prompt: 'Write a haiku about coding',
});

// Stream text
const result = streamText({
  model: anthropic('claude-sonnet-4-5-20241022'),
  prompt: 'Write a story',
});
for await (const chunk of result.textStream) {
  console.log(chunk);
}

// Generate structured data
const { object } = await generateObject({
  model: anthropic('claude-sonnet-4-5-20241022'),
  schema: z.object({
    name: z.string(),
    age: z.number(),
  }),
  prompt: 'Generate a person',
});

// Stream structured data
const { partialObjectStream } = streamObject({
  model: anthropic('claude-sonnet-4-5-20241022'),
  schema: z.object({ items: z.array(z.string()) }),
  prompt: 'List 5 fruits',
});
```

### Tool Definition

```typescript
import { tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get the weather for a location',
  inputSchema: z.object({
    location: z.string().describe('City name'),
  }),
  execute: async ({ location }) => {
    return { temperature: 72, condition: 'sunny' };
  },
});

// Use with generateText/streamText
const result = await generateText({
  model: anthropic('claude-sonnet-4-5-20241022'),
  tools: { weather: weatherTool },
  prompt: 'What is the weather in San Francisco?',
});
```

### Agent (ToolLoopAgent)

```typescript
import { ToolLoopAgent, stepCountIs, tool } from 'ai';

const agent = new ToolLoopAgent({
  model: anthropic('claude-sonnet-4-5-20241022'),
  tools: {
    search: tool({ /* ... */ }),
    calculate: tool({ /* ... */ }),
  },
  stopWhen: stepCountIs(10), // Max 10 steps
});

const result = await agent.generate({
  prompt: 'Research and calculate...',
});
```

### useChat Hook (React)

```typescript
import { useChat } from '@ai-sdk/react';

function Chat() {
  const { messages, sendMessage, status, stop } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });

  return (
    <>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.parts.map(p => p.type === 'text' ? p.text : null)}
        </div>
      ))}
      <form onSubmit={e => {
        e.preventDefault();
        sendMessage({ text: input });
      }}>
        <input disabled={status !== 'ready'} />
      </form>
    </>
  );
}
```

### Installation

```bash
# Core package
npm install ai

# Provider packages
npm install @ai-sdk/openai
npm install @ai-sdk/anthropic
npm install @ai-sdk/google

# For AI Elements (UI components)
npm install @anthropic-ai/ai-elements
```

## Best Practices

1. Always use the `tool()` helper for tool definitions.
2. Use `inputSchema` instead of `parameters` for defining tool inputs.
3. Use `sendMessage` instead of `append` in the `useChat` hook.
4. Utilize `message.parts` for rendering message content.

## Migration from v4 to v5/v6

| v4 Pattern | v5/v6 Pattern |
|------------|---------------|
| `parameters` | `inputSchema` |
| `append()` | `sendMessage()` |
| `message.content` | `message.parts` |

## Source

Documentation downloaded from: https://github.com/vercel/ai/tree/main/content/docs