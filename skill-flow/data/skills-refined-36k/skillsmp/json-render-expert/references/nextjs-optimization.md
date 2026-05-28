# Next.js 16 Optimization Guide for json-render

This guide covers advanced integration of `json-render` with **Next.js 16.2+** and **React 19.3**.

## 🚀 Edge Runtime & Streaming
For minimum Time to First Byte (TTFB), always use the `edge` runtime for your AI streaming endpoints.

```typescript
// app/api/render/route.ts
export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  // ... streaming logic
}
```

## 🏗 Partial Prerendering (PPR)
Next.js 16 stabilizes PPR. You can wrap the `JSONRender` component in a `<Suspense>` boundary to allow the shell of your page to render instantly while the AI JSON stream is being established.

```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <main>
      <h1>AI Dashboard</h1>
      <Suspense fallback={<DashboardSkeleton />}>
        <DynamicAIRenderer />
      </Suspense>
    </main>
  );
}
```

## 📦 Zero-Runtime Export
Use `@json-render/codegen` to transform AI-generated JSON into static React components. This is critical for performance-sensitive pages where you don't want the `json-render` runtime overhead.

### Workflow:
1. Generate UI with AI in development.
2. Run `json-render export <session-id>`.
3. Codegen produces a clean `.tsx` file.
4. Import and use like a regular component.

## 🔒 Security & Guardrails
- **Environment Variables**: Never pass sensitive env vars directly to components rendered by AI.
- **Server Actions**: When using `Actions` in `json-render`, ensure they are validated on the server using Next.js Server Actions with strict Zod parsing.

## 📉 Performance Benchmarks (2026)
- **JSONL Streaming**: ~150ms to first component render.
- **Standard JSON**: ~1.2s (depending on payload size).
- **Bundle Impact**: `@json-render/react` adds ~12kb gzipped (highly optimized).

*Updated: January 22, 2026 - 17:35*
