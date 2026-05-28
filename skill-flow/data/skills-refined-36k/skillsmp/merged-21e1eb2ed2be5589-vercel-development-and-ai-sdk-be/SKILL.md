---
name: vercel-development-and-ai-sdk-best-practices
description: Use this skill when developing and deploying applications on Vercel with Next.js, focusing on best practices for performance, AI SDK integration, and error handling.
---

# Vercel Development and AI SDK Best Practices

## Overview

This skill provides comprehensive guidelines for developing and deploying applications on Vercel, with a focus on Next.js, React Server Components, Edge Functions, and the Vercel AI SDK.

## Core Principles

- Write concise, technical TypeScript code with accurate examples.
- Use functional and declarative programming patterns; avoid classes.
- Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC).
- Implement responsive design with Tailwind CSS using a mobile-first approach.
- Optimize for Core Web Vitals and performance.

## Project Structure

```
my-app/
├── app/                    # App Router pages and layouts
│   ├── (auth)/            # Route groups
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # UI primitives
│   └── features/         # Feature components
├── lib/                   # Utility functions
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript types
├── public/               # Static assets
└── vercel.json           # Vercel configuration
```

## Next.js App Router Guidelines

### File Naming Conventions
- Use lowercase with dashes for directories (e.g., `components/auth-wizard`).
- Prefer named exports for components and functions.
- Use `page.tsx` for route pages, `layout.tsx` for layouts.
- Use `loading.tsx` for loading states, `error.tsx` for error boundaries.

## TypeScript Standards

### Type Definitions
```typescript
// Use interfaces over types for object shapes
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// Use types for unions and complex types
type Status = 'pending' | 'active' | 'inactive';

// Avoid enums; use const objects instead
const STATUS = {
  PENDING: 'pending',
  ACTIVE: 'active',
  INACTIVE: 'inactive',
} as const;

type StatusValue = typeof STATUS[keyof typeof STATUS];
```

## Vercel AI SDK Integration

### Streaming Chat UI
```typescript
'use client';

import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto">
        {messages.map(message => (
          <div key={message.id} className={message.role === 'user' ? 'text-right' : ''}>
            <p>{message.content}</p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message..."
          disabled={isLoading}
        />
      </form>
    </div>
  );
}
```

### Error Handling for AI
```typescript
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(request: Request) {
  try {
    const { messages } = await request.json();

    const result = await streamText({
      model: openai('gpt-4-turbo'),
      messages,
    });

    return result.toDataStreamResponse();
  } catch (error) {
    // Handle rate limiting
    if (error.message?.includes('rate limit')) {
      return new Response('Rate limit exceeded. Please try again later.', {
        status: 429,
      });
    }

    // Handle quota exceeded
    if (error.message?.includes('quota')) {
      return new Response('API quota exceeded.', { status: 402 });
    }

    // Fallback to alternative model
    console.error('Primary model failed:', error);
    return new Response('Service temporarily unavailable.', { status: 503 });
  }
}
```

## Performance Optimization

### Image Optimization
```typescript
import Image from 'next/image';

export function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority // Load immediately for LCP
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}
```

### Dynamic Imports
```typescript
import dynamic from 'next/dynamic';

// Lazy load heavy components
const HeavyChart = dynamic(() => import('@/components/heavy-chart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Disable SSR if needed
});
```

## Deployment

### Preview Deployments
- Every pull request gets a preview deployment.
- Use preview URLs for testing and review.
- Share preview links with stakeholders.

### Production Deployment
```bash
# Connect repo to Vercel (one-click from GitHub)
# Or use Vercel CLI
vercel --prod
```

## Common Pitfalls to Avoid

1. Using 'use client' unnecessarily.
2. Not implementing proper error boundaries.
3. Ignoring Core Web Vitals optimization.
4. Not using TypeScript strictly.
5. Hardcoding environment variables.
6. Missing Suspense boundaries for async components.
7. Not optimizing images.
8. Ignoring accessibility requirements.

## Best Practices for Vercel AI SDK

- Use `streamText` for streaming text responses from AI models.
- Implement proper error handling with `onFinish` callback.
- Prefer server-side streaming for better performance and security.
- Use environment variables for API keys and sensitive configuration.
- Cache AI responses when appropriate to reduce costs.
- Implement proper logging for debugging and monitoring.