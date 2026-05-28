# Anthropic Configuration

Provider setup, extended thinking, and Anthropic-specific features.

## Provider Setup

```typescript
import { anthropic, createAnthropic } from '@ai-sdk/anthropic'

// Default instance (uses ANTHROPIC_API_KEY env var)
const model = anthropic('claude-sonnet-4-20250514')

// Custom instance
const customAnthropic = createAnthropic({
  apiKey: process.env.CUSTOM_ANTHROPIC_KEY,
  baseURL: 'https://custom-proxy.example.com/v1',
  headers: {
    'X-Custom-Header': 'value',
  },
})
```

## Model Options

| Model | Use Case |
|-------|----------|
| `claude-sonnet-4-20250514` | Best balance of speed/quality |
| `claude-opus-4-20250514` | Highest quality, supports effort levels |
| `claude-haiku-4-5-20251001` | Fast, cost-effective |

## Extended Thinking (Reasoning)

Enable reasoning for complex tasks:

```typescript
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic'
import { streamText } from 'ai'

const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: convertToModelMessages(messages),
  providerOptions: {
    anthropic: {
      thinking: { 
        type: 'enabled', 
        budgetTokens: 10000 // Max tokens for reasoning
      },
    } satisfies AnthropicProviderOptions,
  },
})

// Stream reasoning to client
return result.toUIMessageStreamResponse({
  sendReasoning: true,
})
```

### Rendering Reasoning

```typescript
// Client-side
{message.parts.map((part, idx) => {
  if (part.type === 'reasoning') {
    return (
      <details key={idx} className="text-gray-500 text-sm my-2">
        <summary className="cursor-pointer hover:text-gray-700">
          View reasoning
        </summary>
        <pre className="mt-2 p-2 bg-gray-100 rounded whitespace-pre-wrap">
          {part.text}
        </pre>
      </details>
    )
  }
  // ... other parts
})}
```

### Accessing Reasoning Details

```typescript
const { text, reasoning, reasoningDetails } = await generateText({
  model: anthropic('claude-opus-4-20250514'),
  prompt: 'Complex analysis question...',
  providerOptions: {
    anthropic: {
      thinking: { type: 'enabled', budgetTokens: 12000 },
    },
  },
})

console.log(reasoning) // Full reasoning text
console.log(reasoningDetails) // Includes redacted reasoning info
```

## Effort Levels (Claude Opus)

Control quality vs speed/cost:

```typescript
const result = streamText({
  model: anthropic('claude-opus-4-20250514'),
  messages: convertToModelMessages(messages),
  providerOptions: {
    anthropic: {
      effort: 'medium', // 'high' | 'medium' | 'low'
    } satisfies AnthropicProviderOptions,
  },
})
```

| Effort | Tokens | Latency | Use Case |
|--------|--------|---------|----------|
| `high` | Most | Highest | Complex analysis, accuracy critical |
| `medium` | Balanced | Moderate | General use |
| `low` | Fewest | Lowest | Simple tasks, cost-sensitive |

## Cache Control

Reduce costs for repeated context:

```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: [
    {
      role: 'user',
      content: [
        { 
          type: 'text', 
          text: longSystemContext, // Will be cached
          providerOptions: {
            anthropic: { cacheControl: { type: 'ephemeral' } },
          },
        },
        { type: 'text', text: userQuestion },
      ],
    },
  ],
})

// Check cache usage
console.log(result.providerMetadata?.anthropic)
// { cacheCreationInputTokens: 2118, cacheReadInputTokens: 0 }
```

### Cache for System Messages

```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: [
    {
      role: 'system',
      content: 'Large system prompt to cache...',
      providerOptions: {
        anthropic: { cacheControl: { type: 'ephemeral' } },
      },
    },
    {
      role: 'system',
      content: 'Additional uncached instructions',
    },
    {
      role: 'user',
      content: 'User message',
    },
  ],
})
```

### Cache for Tools

```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: {
    complexTool: tool({
      description: 'Tool with large schema',
      inputSchema: largeSchema,
      providerOptions: {
        anthropic: { cacheControl: { type: 'ephemeral' } },
      },
      execute: async (input) => { ... },
    }),
  },
  messages,
})
```

### Longer Cache TTL

```typescript
providerOptions: {
  anthropic: { 
    cacheControl: { type: 'ephemeral', ttl: '1h' } // 1-hour cache
  },
}
```

### Cache Limitations

- Minimum cacheable: 1024 tokens (Sonnet/Opus), 2048 tokens (Haiku)
- Shorter prompts are processed without caching

## Tool Streaming

Enable incremental tool input streaming:

```typescript
const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: convertToModelMessages(messages),
  tools,
  headers: {
    'anthropic-beta': 'fine-grained-tool-streaming-2025-05-14',
  },
})
```

## Structured Output Mode

Control how structured outputs are generated:

```typescript
providerOptions: {
  anthropic: {
    structuredOutputMode: 'auto', // 'outputFormat' | 'jsonTool' | 'auto'
  },
}
```

## Complete Example

```typescript
// app/api/agent/route.ts
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic'
import {
  streamText,
  createUIMessageStream,
  createUIMessageStreamResponse,
  convertToModelMessages,
  stepCountIs,
} from 'ai'
import { tools } from '@/ai/tools'
import type { MyUIMessage } from '@/features/agents/types/message'

export async function POST(req: Request) {
  const { message, agentId } = await req.json()

  await upsertMessage({ agentId, id: message.id, message })
  const messages = await loadAgent(agentId)

  const stream = createUIMessageStream<MyUIMessage>({
    execute: ({ writer }) => {
      const result = streamText({
        model: anthropic('claude-sonnet-4-20250514'),
        system: `You are an AI assistant for insurance proposals.
                 Think through complex requests carefully.`,
        messages: convertToModelMessages(messages),
        tools,
        stopWhen: stepCountIs(5),
        providerOptions: {
          anthropic: {
            thinking: { type: 'enabled', budgetTokens: 10000 },
            sendReasoning: true,
          } satisfies AnthropicProviderOptions,
        },
        headers: {
          'anthropic-beta': 'fine-grained-tool-streaming-2025-05-14',
        },
      })

      result.consumeStream()

      writer.merge(result.toUIMessageStream())
    },
    originalMessages: messages,
    onFinish: async ({ responseMessage }) => {
      await upsertMessage({
        agentId,
        id: responseMessage.id,
        message: responseMessage,
      })
    },
  })

  return createUIMessageStreamResponse({ stream })
}
```

## Provider Options Reference

```typescript
interface AnthropicProviderOptions {
  // Extended thinking
  thinking?: { 
    type: 'enabled'
    budgetTokens: number 
  }
  
  // Include reasoning in requests
  sendReasoning?: boolean
  
  // Effort level (Opus only)
  effort?: 'high' | 'medium' | 'low'
  
  // Tool streaming
  toolStreaming?: boolean
  
  // Structured output mode
  structuredOutputMode?: 'outputFormat' | 'jsonTool' | 'auto'
  
  // Disable parallel tool calls
  disableParallelToolUse?: boolean
}
```

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional for custom setup
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1
```
