---
title: Configure Static Export When Applicable
impact: LOW-MEDIUM
impactDescription: Deploy anywhere, no server required
tags: deployment, static, export, hosting
---

## Configure Static Export When Applicable

Static export generates plain HTML/CSS/JS that can be hosted anywhere. Use it when you don't need server-side features.

**When to use static export:**

```typescript
// next.config.js
module.exports = {
  output: 'export', // Enable static export
}

// Works with:
// ✓ Static pages (no server-side data fetching at request time)
// ✓ Client-side data fetching (useEffect, SWR, React Query)
// ✓ Static site generators (generateStaticParams)
// ✓ CDN hosting (S3, CloudFront, Netlify, GitHub Pages)
```

**Features NOT available with static export:**

```typescript
// ❌ Dynamic Server Components
export default async function Page() {
  const data = await fetch(url, { cache: 'no-store' }) // Won't work
}

// ❌ Server Actions
'use server'
export async function submitForm() { } // Won't work

// ❌ Middleware
// middleware.ts won't run

// ❌ ISR / Revalidation
export const revalidate = 60 // Ignored

// ❌ Dynamic routes without generateStaticParams
// app/posts/[id]/page.tsx without generateStaticParams won't work

// ❌ Route handlers that aren't GET
export async function POST() { } // Won't work
```

**Making your app compatible:**

```typescript
// app/posts/[id]/page.tsx
// ✓ Must pre-render all dynamic routes
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map(post => ({ id: post.id }))
}

// ✓ Data fetching at build time only
export default async function PostPage({ params }) {
  const post = await getPost(params.id) // Runs at build time
  return <Article post={post} />
}

// ✓ Client-side fetching for dynamic data
'use client'
export function Comments({ postId }) {
  const { data } = useSWR(`/api/comments/${postId}`)
  // API must be external or use separate backend
  return <CommentList comments={data} />
}
```

**Static export configuration:**

```typescript
// next.config.js
module.exports = {
  output: 'export',
  trailingSlash: true, // URLs end with /
  images: {
    unoptimized: true, // No image optimization server
  },
  // Or use external image loader
  images: {
    loader: 'custom',
    loaderFile: './image-loader.js',
  },
}
```

**When NOT to use static export:**

- User authentication with server sessions
- Real-time features
- Frequent content updates (use ISR instead)
- API routes that modify data
- Server Actions

Reference: [Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
