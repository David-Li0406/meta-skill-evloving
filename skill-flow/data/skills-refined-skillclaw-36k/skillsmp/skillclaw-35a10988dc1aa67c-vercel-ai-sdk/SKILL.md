---
name: vercel-ai-sdk
description: Use this skill when building AI-powered applications with the Vercel AI SDK, including text generation, chatbots, and tool integration.
---

# Skill body

## Overview

The Vercel AI SDK is a TypeScript toolkit designed for creating AI-powered applications across various frameworks like React, Next.js, Vue, and Node.js. It provides a unified API for working with large language models (LLMs) and includes features for generating text, building chatbots, and integrating with AI providers.

## When to Use This Skill

Use this skill when:
- Generating text or structured data with LLMs.
- Building chatbot UIs with streaming capabilities.
- Implementing tool calling and function execution.
- Creating AI agents that utilize tools in a loop.
- Integrating with AI providers such as OpenAI, Anthropic, and Google.
- Working with hooks like `useChat`, `useCompletion`, or `useObject`.

## Key Features

- **Text Generation**: Use `generateText` and `streamText` for dynamic text outputs.
- **Structured Data Generation**: Utilize `generateObject` and `streamObject` for structured outputs.
- **Chatbot Development**: Implement chat interfaces using the `useChat` hook.
- **Tool Integration**: Define tools with Zod schemas and execute them using the `tool()` helper.
- **Agent Creation**: Build agents with `ToolLoopAgent` for complex workflows.

## Documentation

Refer to the following sections for detailed guidance:

### Getting Started
- Overview of core concepts and quickstarts for various frameworks.

### AI SDK Core
- Core API overview and documentation on generating text and structured data.
- Tool definitions and execution methods.

### Agents
- Fundamentals of agent creation and structured workflow patterns.

### UI Hooks
- Overview of UI hooks for building chat interfaces and handling tool usage.

### API Differences
- Important changes and improvements in SDK versions, including tool definitions and message handling.

## Example Code Snippets

### Tool Definition

```typescript
import { tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get weather for a city',
  inputSchema: z.object({
    city: z.string().describe('City name'),
  }),
  execute: async ({ city }) => {
    const weather = await fetchWeather(city);
    return weather;
  },
});
```

### Using the `useChat` Hook

```typescript
const { messages, sendMessage } = useChat();
sendMessage({ text: input });
```

### Rendering Messages

```typescript
{messages.map(m => (
  <div>
    {m.parts.map((part, i) => {
      if (part.type === 'text') return <span key={i}>{part.text}</span>;
      if (part.type === 'tool-call') return <ToolCall key={i} {...part} />;
      // Handle other message types as needed
    })}
  </div>
))}
```