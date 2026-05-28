# Streaming Responses with OpenAI

Streaming provides a better user experience by showing responses token-by-token instead of waiting for the entire completion.

## Basic Streaming

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function* streamChatCompletion(userMessage: string) {
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful Physical AI tutor.' },
      { role: 'user', content: userMessage },
    ],
    stream: true,
  });
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    if (content) {
      yield content;
    }
  }
}

// Usage
for await (const text of streamChatCompletion('What is ROS 2?')) {
  process.stdout.write(text);
}
```

## React Component (Frontend)

```tsx
import { useState } from 'react';

export function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);

  const sendMessage = async () => {
    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    // Start streaming
    setStreaming(true);
    let aiResponse = '';
    
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage }),
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const text = decoder.decode(value);
      aiResponse += text;
      
      // Update UI in real-time
      setMessages(prev => {
        const lastMsg = prev[prev.length - 1];
        if (lastMsg?.role === 'assistant') {
          return [...prev.slice(0, -1), { role: 'assistant', content: aiResponse }];
        } else {
          return [...prev, { role: 'assistant', content: aiResponse }];
        }
      });
    }
    
    setStreaming(false);
  };
  
  return (
    <div>
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>
            {msg.content}
          </div>
        ))}
        {streaming && <div className="typing-indicator">...</div>}
      </div>
      
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && sendMessage()}
        disabled={streaming}
      />
      <button onClick={sendMessage} disabled={streaming}>
        {streaming ? 'Streaming...' : 'Send'}
      </button>
    </div>
  );
}
```

## API Route (Next.js/Vercel)

```typescript
// app/api/chat/stream/route.ts
import { OpenAI } from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: Request) {
  const { message } = await req.json();
  
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a Physical AI tutor.' },
      { role: 'user', content: message },
    ],
    stream: true,
  });
  
  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
```

## Server-Sent Events (SSE)

```typescript
// Express.js API
import express from 'express';
import OpenAI from 'openai';

const app = express();
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post('/api/chat/stream', async (req, res) => {
  const { message } = req.body;
  
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful AI assistant.' },
      { role: 'user', content: message },
    ],
    stream: true,
  });
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    if (content) {
      res.write(`data: ${JSON.stringify({ content })}\n\n`);
    }
  }
  
  res.write('data: [DONE]\n\n');
  res.end();
});
```

## With RAG Context

```typescript
async function* streamRAGResponse(userQuestion: string) {
  // 1. Get context from RAG
  const relevantChunks = await searchQdrant(userQuestion);
  const context = relevantChunks.map(c => c.text).join('\n\n');
  
  // 2. Stream with context
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: `You are a Physical AI tutor. Use this context:\n\n${context}`,
      },
      { role: 'user', content: userQuestion },
    ],
    stream: true,
  });
  
  let fullResponse = '';
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    if (content) {
      fullResponse += content;
      yield content;
    }
  }
  
  // 3. Save conversation after streaming completes
  await saveConversation(userQuestion, fullResponse);
}
```

## Error Handling

```typescript
async function* safeStreamChat(message: string) {
  try {
    const stream = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: message }],
      stream: true,
    });
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) yield content;
    }
  } catch (error) {
    if (error instanceof OpenAI.APIError) {
      if (error.status === 429) {
        yield '\n\n[Rate limit reached. Please try again in a few seconds.]';
      } else {
        yield '\n\n[An error occurred. Please try again.]';
      }
    }
    console.error('Streaming error:', error);
  }
}
```

## Progress Indicators

```typescript
async function* streamWithProgress(message: string) {
  yield '[Searching textbook...]\n\n';
  
  const chunks = await searchQdrant(message);
  
  yield `[Found ${chunks.length} relevant sections]\n\n`;
  
  const context = chunks.map(c => c.text).join('\n\n');
  
  yield '[Generating response...]\n\n';
  
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: `Context:\n${context}` },
      { role: 'user', content: message },
    ],
    stream: true,
  });
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    if (content) yield content;
  }
  
  yield `\n\n---\nSources: ${chunks.map(c => c.chapter).join(', ')}`;
}
```

## Best Practices

1. **Show progress**: Let users know what's happening
2. **Handle errors gracefully**: Don't let streams hang
3. **Set timeouts**: Prevent infinite waits
4. **Buffer efficiently**: Don't send single characters
5. **Clean up**: Close streams properly
6. **Test reconnection**: Handle network issues
