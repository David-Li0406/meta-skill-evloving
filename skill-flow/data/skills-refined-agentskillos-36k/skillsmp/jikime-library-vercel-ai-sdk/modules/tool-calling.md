# Tool Calling Patterns

Detailed patterns for implementing tool calling in Vercel AI SDK v5/v6.

## Define Tools with inputSchema

```typescript
// lib/tools.ts
import { tool } from 'ai'
import { z } from 'zod'

export const weatherTool = tool({
  description: 'Get the current weather for a location',
  inputSchema: z.object({
    city: z.string().describe('The city to get weather for'),
    unit: z.enum(['celsius', 'fahrenheit']).default('celsius'),
  }),
  execute: async ({ city, unit }) => {
    const weather = await fetchWeatherAPI(city)
    return {
      city,
      temperature: unit === 'celsius' ? weather.tempC : weather.tempF,
      condition: weather.condition,
    }
  },
})

export const searchTool = tool({
  description: 'Search the web for information',
  inputSchema: z.object({
    query: z.string().describe('Search query'),
    maxResults: z.number().default(5),
  }),
  execute: async ({ query, maxResults }) => {
    const results = await searchAPI(query, maxResults)
    return results
  },
})
```

## Use Tools in API Route

```typescript
// app/api/chat/route.ts
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'
import { weatherTool, searchTool } from '@/lib/tools'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      weather: weatherTool,
      search: searchTool,
    },
    maxSteps: 5,  // Allow multi-step tool use
  })

  return result.toDataStreamResponse()
}
```

## Display Tool Results

```tsx
// components/message.tsx
'use client'

import type { Message } from '@ai-sdk/react'

export function ChatMessage({ message }: { message: Message }) {
  return (
    <div className={`message ${message.role}`}>
      {message.parts.map((part, index) => {
        switch (part.type) {
          case 'text':
            return <p key={index}>{part.text}</p>

          case 'tool-call':
            return (
              <div key={index} className="tool-call">
                <span className="tool-name">{part.toolName}</span>
                <pre>{JSON.stringify(part.args, null, 2)}</pre>
              </div>
            )

          case 'tool-result':
            return (
              <div key={index} className="tool-result">
                <span className="tool-name">{part.toolName}</span>
                <pre>{JSON.stringify(part.result, null, 2)}</pre>
              </div>
            )

          default:
            return null
        }
      })}
    </div>
  )
}
```

## Complex Tool Patterns

### Tool with Database Access

```typescript
export const getUserTool = tool({
  description: 'Get user information from database',
  inputSchema: z.object({
    userId: z.string().describe('User ID'),
  }),
  execute: async ({ userId }) => {
    const user = await db.user.findUnique({
      where: { id: userId },
      select: { id: true, name: true, email: true },
    })
    if (!user) throw new Error('User not found')
    return user
  },
})
```

### Tool with External API

```typescript
export const translateTool = tool({
  description: 'Translate text to another language',
  inputSchema: z.object({
    text: z.string().describe('Text to translate'),
    targetLanguage: z.string().describe('Target language code (e.g., "ko", "ja")'),
  }),
  execute: async ({ text, targetLanguage }) => {
    const response = await fetch('https://api.translation.service/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, target: targetLanguage }),
    })
    return response.json()
  },
})
```

### Tool with File Operations

```typescript
export const analyzeImageTool = tool({
  description: 'Analyze an image and return description',
  inputSchema: z.object({
    imageUrl: z.string().url().describe('URL of the image to analyze'),
  }),
  execute: async ({ imageUrl }) => {
    const analysis = await analyzeImage(imageUrl)
    return {
      description: analysis.description,
      objects: analysis.objects,
      text: analysis.extractedText,
    }
  },
})
```

---

Version: 1.0.0
Source: jikime-library-vercel-ai-sdk SKILL.md
