---
name: hono-htmx-architecture
description: Hono + HTMX architecture guidelines for Cloudflare Workers.  Use when developing server-rendered applications with Hono, HTMX, and Hono JSX.
---

# Hono + HTMX Architecture Guidelines

## Stack

- **Framework**: Hono
- **Runtime**: Cloudflare Workers
- **Template**: Hono JSX
- **Interactivity**: HTMX (partial updates)
- **Styling**: Tailwind CSS

## Core Principles

### HTMX Philosophy

- **Hypermedia-driven**: Server returns HTML, not JSON
- **Partial updates**: Use `hx-target`, `hx-swap` for granular DOM updates
- **Progressive enhancement**: Works without JS, enhanced with HTMX
- **Minimal client-side JS**: Let HTMX handle interactions

### State Management

- **No client-side state**: State lives on server
- **HTML represents state**: Server generates HTML reflecting current state
- **Stateless requests**: Each request contains all necessary context

## Project Structure

```
src/
├── index.tsx              # Entry point
├── routes/                # Route definitions (thin layer)
│   ├── index.ts           # Route registry
│   ├── posts.ts
│   └── users.ts
├── features/              # Business logic + presentation
│   ├── posts/
│   │   ├── postService.ts    # Business logic
│   │   ├── postPresenter.ts  # HTML generation
│   │   └── postValidator.ts  # Validation (optional)
│   └── users/
│       └── ...
├── views/                 # Full page templates (Hono JSX)
│   ├── layout.tsx         # Base layout
│   ├── home.tsx
│   └── posts/
│       ├── list.tsx
│       └── detail.tsx
├── components/            # Reusable HTMX partials (Hono JSX)
│   ├── PostCard.tsx
│   ├── UserProfile.tsx
│   └── ui/                # Atomic UI components
├── utils/                 # Utilities
│   └── types.ts           # Global types (Result<T,E>)
└── public/                # Static assets
    ├── styles.css         # Tailwind output
    └── htmx.min.js        # HTMX library
```

## Architecture Patterns

### Pattern 1: Simple Route Handlers

Route handler contains logic directly.

**Use when:**

- Simple CRUD operations
- 1-2 DB queries
- Minimal business logic

**Example:**

```typescript
// routes/posts.ts
posts.get('/', async (c) => {
  const postList = await db.posts.findMany()
  return c.html(<PostList posts={postList} />)
})

posts.delete('/:id', async (c) => {
  await db.posts.delete({ where: { id: c.req.param('id') } })
  return c.html('', 200)
})
```

**Trade-offs:** Simple, straightforward | Hard to test, logic scattered

### Pattern 2: Service Layer

Service handles business logic, route handler is thin.

**Use when:**

- Multiple data sources
- Business logic complexity
- Testing requirements

**Example:**

```typescript
// features/posts/postService.ts
export class PostService {
  async getAllPosts(): Promise<Result<Post[], string>> {
    try {
      const posts = await db.posts.findMany()
      const enriched = await this.enrichWithAuthor(posts)
      return { ok: true, value: enriched }
    } catch (error) {
      console.error('Get posts error:', error)
      return { ok: false, error: 'Failed to fetch posts' }
    }
  }

  async deletePost(id: string): Promise<Result<void, string>> {
    try {
      await db.posts.delete({ where: { id } })
      return { ok: true, value: undefined }
    } catch (error) {
      console.error('Delete post error:', error)
      return { ok: false, error: 'Failed to delete post' }
    }
  }
}

// routes/posts.ts
const service = new PostService()

posts.get('/', async (c) => {
  const result = await service.getAllPosts()
  if (!result.ok) return c.html(<ErrorMessage message={result.error} />, 500)
  return c.html(<PostList posts={result.value} />)
})

posts.delete('/:id', async (c) => {
  const result = await service.deletePost(c.req.param('id'))
  if (!result.ok) return c.html(<ErrorMessage message={result.error} />, 400)
  return c.html('', 200)
})
```

**Trade-offs:** Testable, organized logic | More files, added abstraction

### Pattern 3: Feature Layer (Service + Presenter)

Full separation: Service (logic) + Presenter (HTML generation).

**Use when:**

- Complex workflows
- Multiple HTMX endpoints per entity
- Team collaboration
- Managing HTMX attributes centrally

**Example:**

```typescript
// features/posts/postService.ts
export class PostService {
  async getAllPosts(): Promise<Result<Post[], string>> {
    try {
      const posts = await db.posts.findMany()
      return { ok: true, value: posts }
    } catch (error) {
      console.error('Get posts error:', error)
      return { ok: false, error: 'Failed to fetch posts' }
    }
  }
}

// features/posts/postPresenter.ts
import { Context } from 'hono'
import { PostList } from '@/views/posts/list'
import { PostCard } from '@/components/PostCard'
import { ErrorMessage } from '@/components/ui/ErrorMessage'

export class PostPresenter {
  renderList(c: Context, posts: Post[]) {
    return c.html(<PostList posts={posts} />)
  }

  renderCard(c: Context, post: Post) {
    return c.html(<PostCard post={post} />)
  }

  renderError(c: Context, message: string, status = 500) {
    return c.html(<ErrorMessage message={message} />, status)
  }

  // HTMX config management
  getDeleteButtonAttrs(postId: string) {
    return {
      'hx-delete': `/posts/${postId}`,
      'hx-target': 'closest article',
      'hx-swap': 'outerHTML',
      'hx-confirm': 'Are you sure?'
    }
  }
}

// routes/posts.ts
const service = new PostService()
const presenter = new PostPresenter()

posts.get('/', async (c) => {
  const result = await service.getAllPosts()
  if (!result.ok) return presenter.renderError(c, result.error)
  return presenter.renderList(c, result.value)
})

posts.post('/', async (c) => {
  const formData = await c.req.formData()
  const result = await service.createPost(formData)
  if (!result.ok) return presenter.renderError(c, result.error, 400)
  return presenter.renderCard(c, result.value)
})

posts.delete('/:id', async (c) => {
  const result = await service.deletePost(c.req.param('id'))
  if (!result.ok) return presenter.renderError(c, result.error, 400)
  return c.html('', 200)
})
```

**Trade-offs:** Highly organized, testable, HTMX centralized | Most boilerplate

### Decision Framework

Start with **Pattern 1**. Move to **Pattern 2** for medium complexity. Use **Pattern 3** for complex applications or when HTMX attribute management becomes unwieldy.

## Hono JSX Patterns

### Layout Component

```tsx
// views/layout.tsx
export const Layout = ({ children }: { children: any }) => (
  <html lang="ja">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>App</title>
      <script src="/htmx.min.js"></script>
      <link href="/styles.css" rel="stylesheet" />
    </head>
    <body>
      <main>{children}</main>
    </body>
  </html>
);
```

### Page Component

```tsx
// views/posts/list.tsx
import { Layout } from "../layout";

export const PostList = ({ posts }: { posts: Post[] }) => (
  <Layout>
    <div id="post-list">
      {posts.map((post) => (
        <PostCard post={post} />
      ))}
    </div>
  </Layout>
);
```

### Partial Component (HTMX target)

```tsx
// components/PostCard.tsx
export const PostCard = ({ post }: { post: Post }) => (
  <article class="card">
    <h2>{post.title}</h2>
    <p>{post.excerpt}</p>
    <button
      hx-delete={`/posts/${post.id}`}
      hx-target="closest article"
      hx-swap="outerHTML"
    >
      Delete
    </button>
  </article>
);
```

## Route Handlers

### Simple Pattern (Pattern 1)

```typescript
// routes/posts.ts
import { Hono } from 'hono';
import { PostList } from '../views/posts/list';
import { PostCard } from '../components/PostCard';

const posts = new Hono();

posts.get('/', async (c) => {
  const postList = await db.posts.findMany();
  return c.html(<PostList posts={postList} />);
});

posts.delete('/:id', async (c) => {
  await db.posts.delete({ where: { id: c.req.param('id') } });
  return c.html('', 200);
});

posts.post('/', async (c) => {
  const formData = await c.req.formData();
  const post = await db.posts.create({
    title: formData.get('title') as string
  });
  return c.html(<PostCard post={post} />);
});

export default posts;
```

### Main App

```typescript
// index.tsx
import { Hono } from "hono";
import { serveStatic } from "hono/cloudflare-workers";
import posts from "./routes/posts";

const app = new Hono();

app.use("/public/*", serveStatic({ root: "./" }));
app.route("/posts", posts);

export default app;
```

## HTMX Patterns

### Common Attributes

```html
<!-- GET request, replace target -->
<button hx-get="/posts/1" hx-target="#content">Load</button>

<!-- POST form, append to list -->
<form hx-post="/posts" hx-target="#post-list" hx-swap="afterbegin">
  <input name="title" required />
  <button type="submit">Create</button>
</form>

<!-- DELETE, remove element -->
<button hx-delete="/posts/1" hx-target="closest article" hx-swap="outerHTML">
  Delete
</button>

<!-- Polling -->
<div hx-get="/status" hx-trigger="every 2s">Status</div>
```

### Response Patterns

```typescript
// Return partial HTML
return c.html(<Component />);

// Return empty for deletions
return c.html('', 200);

// Return error message
return c.html(<ErrorMessage />, 400);

// Redirect (HTMX handles HX-Redirect header)
return c.redirect('/posts');
```

## Cloudflare Workers Considerations

### Environment Variables

```typescript
type Bindings = {
  DB: D1Database;
  BUCKET: R2Bucket;
  // Add your bindings
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/", (c) => {
  const db = c.env.DB; // Access bindings
});
```

### File Structure for Deployment

```
wrangler.toml          # Cloudflare config
src/
└── ...
public/
└── ...
```

## Testing

Focus on service layer and route handlers:

```typescript
// features/posts/postService.test.ts
import { describe, it, expect } from "vitest";
import { PostService } from "./postService";

describe("PostService", () => {
  it("should return posts on success", async () => {
    const service = new PostService();
    const result = await service.getAllPosts();
    expect(result.ok).toBe(true);
  });

  it("should handle errors", async () => {
    const service = new PostService();
    // Mock DB error
    const result = await service.getAllPosts();
    expect(result.ok).toBe(false);
  });
});

// routes/posts.test.ts
import { describe, it, expect } from "vitest";
import app from "./index";

describe("POST /posts", () => {
  it("creates post and returns card", async () => {
    const formData = new FormData();
    formData.append("title", "Test");

    const res = await app.request("/posts", {
      method: "POST",
      body: formData,
    });

    expect(res.status).toBe(200);
    const html = await res.text();
    expect(html).toContain("Test");
  });
});
```

## Key Differences from Next.js

| Aspect        | Next.js                 | Hono + HTMX                 |
| ------------- | ----------------------- | --------------------------- |
| Rendering     | RSC + Client Components | Server-rendered JSX         |
| Routing       | File-based              | Code-based (Hono)           |
| State         | Client + Server         | Server only                 |
| Interactivity | React hooks             | HTMX attributes             |
| Data flow     | Props + State           | Hypermedia (HTML responses) |
| Bundle        | React runtime           | Minimal (HTMX ~14KB)        |
| Feature Layer | Container Components    | Service + Presenter classes |
