# Dynamic Routes Reference (Next.js 15/16)

## CRITICAL CHANGE: Async Params

In Next.js 15/16, `params` and `searchParams` are **Promises** and must be awaited.

## Before vs After

```tsx
// BEFORE (Next.js 14) - DEPRECATED
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>;
}

// AFTER (Next.js 15/16) - REQUIRED
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

## Dynamic Route Patterns

### Single Parameter

```tsx
// app/posts/[id]/page.tsx
// URL: /posts/123

type Props = {
  params: Promise<{ id: string }>;
};

export default async function PostPage({ params }: Props) {
  const { id } = await params;
  const post = await db.post.findUnique({ where: { id } });

  if (!post) notFound();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

### Multiple Parameters

```tsx
// app/[category]/[slug]/page.tsx
// URL: /technology/nextjs-tutorial

type Props = {
  params: Promise<{ category: string; slug: string }>;
};

export default async function Page({ params }: Props) {
  const { category, slug } = await params;

  return (
    <div>
      <span>Category: {category}</span>
      <span>Slug: {slug}</span>
    </div>
  );
}
```

### Catch-All Routes

```tsx
// app/docs/[...slug]/page.tsx
// URL: /docs/getting-started/installation
// slug = ["getting-started", "installation"]

type Props = {
  params: Promise<{ slug: string[] }>;
};

export default async function DocsPage({ params }: Props) {
  const { slug } = await params;
  const path = slug.join("/");

  return <div>Path: {path}</div>;
}
```

### Optional Catch-All Routes

```tsx
// app/shop/[[...categories]]/page.tsx
// URL: /shop → categories = undefined
// URL: /shop/electronics → categories = ["electronics"]
// URL: /shop/electronics/phones → categories = ["electronics", "phones"]

type Props = {
  params: Promise<{ categories?: string[] }>;
};

export default async function ShopPage({ params }: Props) {
  const { categories } = await params;

  if (!categories) {
    return <div>All Products</div>;
  }

  return <div>Categories: {categories.join(" > ")}</div>;
}
```

## SearchParams (Query String)

```tsx
// app/search/page.tsx
// URL: /search?q=nextjs&page=2

type Props = {
  searchParams: Promise<{
    q?: string;
    page?: string;
    sort?: "asc" | "desc";
  }>;
};

export default async function SearchPage({ searchParams }: Props) {
  const { q, page = "1", sort = "desc" } = await searchParams;

  const results = await search({
    query: q,
    page: Number(page),
    sort,
  });

  return <SearchResults results={results} />;
}
```

## Combined Params and SearchParams

```tsx
// app/posts/[id]/page.tsx
// URL: /posts/123?comments=true

type Props = {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ comments?: string }>;
};

export default async function PostPage({ params, searchParams }: Props) {
  const { id } = await params;
  const { comments } = await searchParams;

  const post = await getPost(id);
  const showComments = comments === "true";

  return (
    <article>
      <h1>{post.title}</h1>
      {showComments && <Comments postId={id} />}
    </article>
  );
}
```

## Layout with Params

```tsx
// app/dashboard/[teamId]/layout.tsx

type Props = {
  children: React.ReactNode;
  params: Promise<{ teamId: string }>;
};

export default async function TeamLayout({ children, params }: Props) {
  const { teamId } = await params;
  const team = await getTeam(teamId);

  return (
    <div>
      <header>
        <h1>{team.name}</h1>
        <TeamNav teamId={teamId} />
      </header>
      <main>{children}</main>
    </div>
  );
}
```

## generateMetadata

```tsx
// app/posts/[id]/page.tsx
import { Metadata } from "next";

type Props = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const post = await getPost(id);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  };
}

export default async function PostPage({ params }: Props) {
  const { id } = await params;
  // ...
}
```

## generateStaticParams

For static generation of dynamic routes:

```tsx
// app/posts/[id]/page.tsx

export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map((post) => ({
    id: post.id.toString(),
  }));
}

// With multiple params
// app/[category]/[slug]/page.tsx

export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map((post) => ({
    category: post.category,
    slug: post.slug,
  }));
}
```

## Route Handlers with Params

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";

type Props = {
  params: Promise<{ id: string }>;
};

export async function GET(request: NextRequest, { params }: Props) {
  const { id } = await params;
  const post = await getPost(id);

  if (!post) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(post);
}

export async function DELETE(request: NextRequest, { params }: Props) {
  const { id } = await params;
  await deletePost(id);

  return new NextResponse(null, { status: 204 });
}
```

## Client Components with Params

Client components cannot directly receive async params. Use `use()` hook or pass as props:

```tsx
// app/posts/[id]/page.tsx (Server Component)
export default async function PostPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return <PostClient id={id} />;
}

// components/post-client.tsx (Client Component)
"use client";

export function PostClient({ id }: { id: string }) {
  // Use the id directly - it's already resolved
  return <div>Post ID: {id}</div>;
}
```

## Common Mistakes

### Missing await

```tsx
// WRONG - Will cause runtime error
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  return <div>{params.id}</div>; // params is a Promise!
}

// CORRECT
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

### Non-async function

```tsx
// WRONG - Can't use await without async
export default function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params; // Error!
  return <div>{id}</div>;
}

// CORRECT - Add async
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

### Wrong type definition

```tsx
// WRONG - Old type definition
type Props = {
  params: { id: string }; // Not a Promise!
};

// CORRECT - New type definition
type Props = {
  params: Promise<{ id: string }>;
};
```
