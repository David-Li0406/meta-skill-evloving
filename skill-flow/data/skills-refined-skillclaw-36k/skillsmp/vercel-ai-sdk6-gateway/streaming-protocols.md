# Streaming Protocols Reference

Data stream protocols, UI message streams, and real-time event handling for AI SDK v6.

## Stream Types

### textStream
Simple async iterable of text chunks:
```typescript
const result = streamText({ model: 'openai/gpt-5', prompt: '...' });

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

### fullStream
Complete stream with all event types:
```typescript
for await (const chunk of result.fullStream) {
  switch (chunk.type) {
    case 'text-delta':
      // Incremental text
      console.log(chunk.text);
      break;
    case 'reasoning':
      // Model thinking/reasoning
      console.log('Thinking:', chunk.text);
      break;
    case 'tool-call':
      // Complete tool invocation
      console.log('Tool:', chunk.toolName, chunk.input);
      break;
    case 'tool-result':
      // Tool execution result
      console.log('Result:', chunk.result);
      break;
    case 'file':
      // Generated file
      console.log('File:', chunk.mediaType, chunk.data);
      break;
    case 'finish':
      // Stream complete
      console.log('Done:', chunk.finishReason, chunk.usage);
      break;
  }
}
```

### partialOutputStream
Streaming structured data:
```typescript
const { partialOutputStream } = streamText({
  model: 'openai/gpt-5',
  output: Output.object({
    schema: z.object({
      name: z.string(),
      steps: z.array(z.string()),
    }),
  }),
  prompt: '...',
});

for await (const partial of partialOutputStream) {
  // Incrementally built object
  console.log(partial);
}
```

### elementStream
Complete array elements:
```typescript
const { elementStream } = streamText({
  model: 'openai/gpt-5',
  output: Output.array({
    element: z.object({ name: z.string(), desc: z.string() }),
  }),
  prompt: 'Generate 5 items',
});

for await (const item of elementStream) {
  // Each item is complete and validated
  console.log(item);
}
```

## Stream Part Types (v6)

### Text Lifecycle
```typescript
// Start of text block
{ type: 'text-start', id: string }

// Text increments
{ type: 'text-delta', id: string, delta: string }

// End of text block
{ type: 'text-end', id: string }
```

### Reasoning Lifecycle
```typescript
// Start reasoning
{ type: 'reasoning-start', id: string }

// Reasoning increments
{ type: 'reasoning-delta', id: string, delta: string }

// End reasoning
{ type: 'reasoning-end', id: string }
```

### Tool Input Streaming
```typescript
// Start tool input generation
{ type: 'tool-input-start', id: string, toolName: string }

// Input JSON increments
{ type: 'tool-input-delta', id: string, delta: string }

// Input complete
{ type: 'tool-input-end', id: string }

// Complete tool call
{ type: 'tool-call', toolCallId: string, toolName: string, input: string }
```

### Stream Lifecycle
```typescript
// Stream initialized
{ type: 'stream-start', warnings: Warning[] }

// Stream complete
{ 
  type: 'finish',
  finishReason: FinishReason,
  usage: { inputTokens: number, outputTokens: number }
}
```

## Server-Sent Events Protocol

### Event Format
```
data: {"type":"text-delta","id":"text-1","delta":"Hello"}

data: {"type":"tool-call","toolCallId":"call_xyz","toolName":"search","input":"{\"q\":\"ai\"}"}

data: {"type":"tool-output-available","toolCallId":"call_xyz","output":{"results":[]}}

data: {"type":"finish","finishReason":"stop","usage":{"promptTokens":10,"completionTokens":50}}
```

### Response Helpers

#### toDataStreamResponse
Standard data stream for API routes:
```typescript
export async function POST(req: Request) {
  const { messages } = await req.json();
  
  const result = streamText({
    model: 'openai/gpt-5',
    messages,
  });
  
  return result.toDataStreamResponse();
}
```

#### toUIMessageStreamResponse
UI-optimized message stream:
```typescript
export async function POST(req: Request) {
  const { messages } = await req.json();
  
  const result = streamText({
    model: 'openai/gpt-5',
    messages: await convertToModelMessages(messages),
  });
  
  return result.toUIMessageStreamResponse();
}
```

## Stream Callbacks

### onChunk
Process each chunk:
```typescript
streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  onChunk: ({ chunk }) => {
    if (chunk.type === 'text-delta') {
      logger.log('text', chunk.text);
    } else if (chunk.type === 'tool-call') {
      logger.log('tool', chunk.toolName);
    }
  },
});
```

### onFinish
Handle completion:
```typescript
streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  onFinish: async ({ text, toolCalls, usage, steps }) => {
    await db.saveGeneration({
      text,
      toolCalls,
      tokens: usage.totalTokens,
      stepCount: steps.length,
    });
  },
});
```

### onError
Error handling:
```typescript
streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  onError: async (error) => {
    logger.error('Stream error:', error);
    await cleanup();
  },
});
```

## UI Message Stream

### Creating UI Streams
```typescript
import { 
  createUIMessageStream, 
  createUIMessageStreamResponse,
  convertToModelMessages,
} from 'ai';

const stream = createUIMessageStream({
  originalMessages: messages,
  execute: async ({ writer }) => {
    const result = streamText({
      model: 'openai/gpt-5',
      messages: await convertToModelMessages(messages),
      tools: { /* ... */ },
    });
    
    writer.merge(result.toUIMessageStream({ 
      originalMessages: messages 
    }));
  },
});

return createUIMessageStreamResponse({ stream });
```

### UI Message Structure
```typescript
interface UIMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  parts: UIMessagePart[];
}

type UIMessagePart = 
  | { type: 'text'; text: string }
  | { type: 'tool-call'; toolName: string; input: any }
  | { type: 'tool-result'; toolCallId: string; result: any }
  | { type: 'reasoning'; text: string };
```

## LangChain Adapter

### Convert Messages
```typescript
import { toBaseMessages, toUIMessageStream } from '@ai-sdk/langchain';
import { createUIMessageStreamResponse } from 'ai';

const langchainMessages = await toBaseMessages(uiMessages);

const stream = await langchainAgent.stream(
  { messages: langchainMessages },
  { streamMode: ['values', 'messages'] }
);

return createUIMessageStreamResponse({
  stream: toUIMessageStream(stream),
});
```

### Stream Events
```typescript
const streamEvents = agent.streamEvents(langchainMessages, { version: 'v2' });

return createUIMessageStreamResponse({
  stream: toUIMessageStream(streamEvents),
});
```

## Stream Transformations

### Middleware
```typescript
import { simulateStreamingMiddleware, wrapLanguageModel } from 'ai';

const model = wrapLanguageModel({
  model: openai('gpt-5'),
  middleware: simulateStreamingMiddleware(),
});

const result = streamText({ model, prompt: '...' });
```

### Custom Transform
```typescript
streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  experimental_transform: (stream) => {
    return stream.pipeThrough(new TransformStream({
      transform(chunk, controller) {
        // Modify chunk
        controller.enqueue(chunk);
      },
    }));
  },
});
```

## Client-Side Consumption

### React useChat
```typescript
import { useChat } from 'ai/react';

function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    onFinish: (message) => {
      console.log('Complete:', message);
    },
    onError: (error) => {
      console.error('Chat error:', error);
    },
  });
  
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.parts.map((part, i) => {
            if (part.type === 'text') return <p key={i}>{part.text}</p>;
            if (part.type === 'tool-call') return <ToolUI key={i} {...part} />;
            return null;
          })}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} disabled={isLoading} />
      </form>
    </div>
  );
}
```

### Vue useChat
```typescript
import { Chat } from '@ai-sdk/vue';

const chat = new Chat({ api: '/api/chat' });

const handleSubmit = () => {
  chat.sendMessage({ text: input.value });
  input.value = '';
};
```

## Abort & Timeout

### AbortSignal
```typescript
const controller = new AbortController();

const result = streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  abortSignal: controller.signal,
});

// Cancel after 10s
setTimeout(() => controller.abort(), 10000);
```

### Timeout
```typescript
const result = streamText({
  model: 'openai/gpt-5',
  prompt: '...',
  timeout: { totalMs: 30000 }, // 30s max
});
```

## Backpressure Handling

### Pipe to Response
```typescript
const result = streamText({ model: 'openai/gpt-5', prompt: '...' });

// Express
result.pipeTextStreamToResponse(res);

// Fetch Response
return new Response(result.textStream);
```

### Manual Consumption
```typescript
const reader = result.textStream.getReader();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  // Handle backpressure by processing slowly
  await processChunk(value);
}
```
