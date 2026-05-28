---
name: vercel-ai-sdk
description: Use this skill when building AI features with the Vercel AI SDK, particularly for streaming chat UIs, structured outputs, and multi-step workflows.
---

# Skill body

## When to Use

- Building streaming chat UIs
- Creating structured JSON outputs with Zod schemas
- Implementing multi-step agent workflows with tools
- Designing tool approval flows (human-in-the-loop)
- Integrating with Next.js App Router

## Version Guard

Target **AI SDK 6.x** APIs. Default packages:

```
ai@^6
@ai-sdk/react@^2
@ai-sdk/openai@^2 (or @ai-sdk/anthropic, etc.)
zod@^3
```

**Avoid v4/v5 holdovers:**
- `StreamingTextResponse` → use `result.toUIMessageStreamResponse()`
- Legacy `Message` shape → use `UIMessage`
- Input-managed `useChat` → use transport-based pattern

## Core Concepts

### Message Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| `UIMessage` | User-facing, persistence | Store in database, render in UI |
| `ModelMessage` | LLM-compatible | Convert at call sites only |

**Rule:** Persist `UIMessage[]`. Convert to `ModelMessage[]` only when calling the model.

### Streaming Patterns

| Function | Use Case |
|----------|----------|
| `streamText` | Streaming text responses |
| `generateText` | Non-streaming text |
| `streamObject` | Streaming JSON with partial updates |
| `generateObject` | Non-streaming JSON |
| `ToolLoopAgent` | Multi-step agent with tools |

## Golden Path: Streaming Chat

### API Route (App Router)

```typescript
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai';
import { streamText, convertToModelMessages, type UIMessage } from 'ai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: openai('gpt-4o-mini'),
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse({
    originalMessages: messages,
    getErrorMessage: (e) =>
      e instanceof Error ? e.message : 'An error occurred',
  });
}
```

### Client Hook

```tsx
'use client';
import { useState } from 'react';
import { useChat, type UIMessage } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

export function Chat({ initialMessages = [] }: { initialMessages?: UIMessage[] }) {
  const [input, setInput] = useState('');
  // Additional chat logic here
}
```