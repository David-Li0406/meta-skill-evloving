---
title: Call revalidatePath/revalidateTag After Mutations
impact: HIGH
impactDescription: Keeps cached data fresh after changes
tags: revalidation, cache, mutations, freshness
---

## Call revalidatePath/revalidateTag After Mutations

Server Actions that modify data must revalidate relevant cached content. Otherwise, users see stale data until the cache naturally expires.

**Incorrect (forgetting to revalidate):**

```typescript
'use server'

export async function createPost(formData: FormData) {
  await db.posts.create({
    data: {
      title: formData.get('title'),
      content: formData.get('content')
    }
  })

  // ❌ Blog listing still shows old cached data
  redirect('/blog')
}
```

**Correct (revalidate after mutation):**

```typescript
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.posts.create({
    data: {
      title: formData.get('title'),
      content: formData.get('content')
    }
  })

  // Option 1: Revalidate by path
  revalidatePath('/blog')

  // Option 2: Revalidate by tag (more granular)
  revalidateTag('posts')

  redirect(`/blog/${post.slug}`)
}

export async function updatePost(id: string, formData: FormData) {
  const post = await db.posts.update({
    where: { id },
    data: {
      title: formData.get('title'),
      content: formData.get('content')
    }
  })

  // Revalidate both the listing and the specific post
  revalidateTag('posts')
  revalidateTag(`post-${id}`)

  // Or by paths
  revalidatePath('/blog')
  revalidatePath(`/blog/${post.slug}`)
}

export async function deletePost(id: string) {
  await db.posts.delete({ where: { id } })

  revalidateTag('posts')
  revalidatePath('/blog')

  redirect('/blog')
}
```

**Setting up tags for fetches:**

```typescript
// lib/data.ts
export async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })
  return res.json()
}

export async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: { tags: ['posts', `post-${id}`] }
  })
  return res.json()
}
```

**Layout revalidation:**

```typescript
// Revalidate layout and all pages using it
revalidatePath('/dashboard', 'layout')

// Revalidate specific page only
revalidatePath('/dashboard', 'page')

// Revalidate entire route segment
revalidatePath('/dashboard')
```

Reference: [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
