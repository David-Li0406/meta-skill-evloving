---
name: vercel-ai-sdk
description: Use this skill when building AI-powered applications with Vercel AI SDK, including text generation, chatbot development, tool integrations, and agent workflows.
---

# Vercel AI SDK

The Vercel AI SDK is a comprehensive toolkit for building AI-powered applications using JavaScript/TypeScript across various frameworks like React, Next.js, Vue, and Svelte.

## When to Use This Skill

Use this skill when:
- Generating text or structured data with LLMs
- Building chatbot UIs with streaming capabilities
- Implementing tool calling and function execution
- Creating AI agents that utilize tools in a loop
- Integrating with AI providers (OpenAI, Anthropic, Google, etc.)
- Troubleshooting AI SDK errors or implementing backend features

## Core Functions

### Text Generation

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4'),
  prompt: 'Hello, world!',
});
```

### Streaming Text Generation

```typescript
import { streamText } from 'ai';

const result = streamText({
  model: openai('gpt-4'),
  prompt: 'Tell me a story.',
});
for await (const chunk of result.textStream) {
  console.log(chunk);
}
```

### Structured Output

```typescript
import { generateText, Output } from 'ai';
import { z } from 'zod';

const { output } = await generateText({
  model: openai('gpt-4'),
  output: Output.object({
    schema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative']),
      topics: z.array(z.string()),
    }),
  }),
  prompt: 'Analyze this feedback...',
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
```

### Agent Class

```typescript
import { ToolLoopAgent } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const agent = new ToolLoopAgent({
  model: anthropic('claude-sonnet-4-5'),
  tools: { /* tool definitions */ },
});

const result = await agent.generate({ prompt: 'Research and calculate...' });
```

### useChat Hook (Client)

```typescript
import { useChat } from '@ai-sdk/react';

export function Chat() {
  const { messages, sendMessage, status } = useChat();

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.parts.map(part => part.type === 'text' ? part.text : null)}
        </div>
      ))}
      <form onSubmit={e => {
        e.preventDefault();
        sendMessage({ text: input });
      }}>
        <input disabled={status !== 'ready'} />
      </form>
    </div>
  );
}
```

## Best Practices

- Always use the `tool()` helper for defining tools.
- Use `inputSchema` instead of `parameters` for tool definitions.
- Handle errors appropriately using specific error types.
- Validate API keys at startup and implement retry logic for rate limits.

## References

- [AI SDK Documentation](https://ai-sdk.dev/docs/overview) - For detailed information on all features and usage patterns.
- [Error Handling](https://ai-sdk.dev/docs/reference/ai-sdk-errors) - Common error solutions and troubleshooting.

## Installation

```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google
```

## Conclusion

This skill provides a unified approach to building AI applications with Vercel AI SDK, covering essential functions, best practices, and integration patterns for both frontend and backend development.