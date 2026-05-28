---
name: remix-patterns
description: Best practices, patterns, and conventions for working with Remix - the web framework that embraces web fundamentals and progressive enhancement
---

# Remix Development Patterns

This skill provides comprehensive guidance for building Remix applications following best practices and framework conventions.

## Core Philosophy

Remix embraces:
- **Web Fundamentals**: Work with HTTP, not against it
- **Progressive Enhancement**: Apps should work without JavaScript
- **Server-First**: Do the work on the server, send HTML
- **Nested Routes**: Compose UIs with route hierarchy
- **No Client State**: Use the URL and server as the source of truth

## Route Structure

### Basic Route Module

Every route module can export these functions:

```typescript
// app/routes/posts.$id.tsx
import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData, Form } from "@remix-run/react";

// Loader: Fetch data on GET requests
export async function loader({ params, request }: LoaderFunctionArgs) {
  const post = await getPost(params.id);
  if (!post) {
    throw new Response("Not Found", { status: 404 });
  }
  return json({ post });
}

// Action: Handle mutations (POST, PUT, DELETE)
export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  const title = formData.get("title");
  
  await updatePost(params.id, { title });
  return json({ success: true });
}

// Component: Render the UI
export default function Post() {
  const { post } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <h1>{post.title}</h1>
      <Form method="post">
        <input name="title" defaultValue={post.title} />
        <button type="submit">Update</button>
      </Form>
    </div>
  );
}
```

## Data Loading Patterns

### Pattern 1: Simple Data Fetching

```typescript
export async function loader({ params }: LoaderFunctionArgs) {
  const [user, posts] = await Promise.all([
    db.user.findUnique({ where: { id: params.userId } }),
    db.post.findMany({ where: { userId: params.userId } })
  ]);
  
  return json({ user, posts });
}
```

### Pattern 2: Authentication Checks

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const userId = await requireAuth(request);
  const user = await db.user.findUnique({ where: { id: userId } });
  
  return json({ user });
}

// Helper function
async function requireAuth(request: Request) {
  const userId = await getUserId(request);
  if (!userId) {
    throw redirect("/login");
  }
  return userId;
}
```

### Pattern 3: Search with URL Params

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const query = url.searchParams.get("q") || "";
  const page = Number(url.searchParams.get("page")) || 1;
  
  const results = await searchPosts({ query, page });
  
  return json({ results, query, page });
}

export default function Search() {
  const { results, query } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <Form method="get">
        <input name="q" defaultValue={query} />
        <button type="submit">Search</button>
      </Form>
      {/* Results */}
    </div>
  );
}
```

### Pattern 4: Dependent Loaders (Parent/Child)

```typescript
// app/routes/users.$userId.tsx (parent)
export async function loader({ params }: LoaderFunctionArgs) {
  const user = await db.user.findUnique({ where: { id: params.userId } });
  return json({ user });
}

// app/routes/users.$userId.posts.tsx (child)
export async function loader({ params }: LoaderFunctionArgs) {
  // Can access parent data via useRouteLoaderData
  const posts = await db.post.findMany({ where: { userId: params.userId } });
  return json({ posts });
}

export default function UserPosts() {
  const { posts } = useLoaderData<typeof loader>();
  const { user } = useRouteLoaderData<typeof parentLoader>("routes/users.$userId");
  
  return <div>{/* ... */}</div>;
}
```

## Form Handling Patterns

### Pattern 1: Basic Form Submission

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const title = formData.get("title");
  const content = formData.get("content");
  
  const post = await db.post.create({
    data: { title, content }
  });
  
  return redirect(`/posts/${post.id}`);
}

export default function NewPost() {
  return (
    <Form method="post">
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </Form>
  );
}
```

### Pattern 2: Form with Validation

```typescript
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);
  
  const result = schema.safeParse(data);
  if (!result.success) {
    return json(
      { errors: result.error.flatten() },
      { status: 400 }
    );
  }
  
  await createUser(result.data);
  return redirect("/dashboard");
}

export default function Signup() {
  const actionData = useActionData<typeof action>();
  
  return (
    <Form method="post">
      <input name="email" />
      {actionData?.errors.fieldErrors.email && (
        <span>{actionData.errors.fieldErrors.email}</span>
      )}
      
      <input name="password" type="password" />
      {actionData?.errors.fieldErrors.password && (
        <span>{actionData.errors.fieldErrors.password}</span>
      )}
      
      <button type="submit">Sign Up</button>
    </Form>
  );
}
```

### Pattern 3: Optimistic UI

```typescript
import { useFetcher } from "@remix-run/react";

export default function Todo({ todo }) {
  const fetcher = useFetcher();
  
  // Optimistic state
  const isComplete = fetcher.formData
    ? fetcher.formData.get("complete") === "true"
    : todo.complete;
  
  return (
    <fetcher.Form method="post" action={`/todos/${todo.id}`}>
      <input type="hidden" name="complete" value={String(!isComplete)} />
      <button type="submit">
        {isComplete ? "✓" : "○"} {todo.title}
      </button>
    </fetcher.Form>
  );
}
```

### Pattern 4: Multiple Actions per Route

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent");
  
  switch (intent) {
    case "delete":
      await deletePost(formData.get("id"));
      return json({ success: true });
      
    case "update":
      await updatePost(formData.get("id"), {
        title: formData.get("title")
      });
      return json({ success: true });
      
    default:
      throw new Response("Invalid intent", { status: 400 });
  }
}

export default function Post() {
  return (
    <>
      <Form method="post">
        <input type="hidden" name="intent" value="update" />
        <input name="title" />
        <button type="submit">Update</button>
      </Form>
      
      <Form method="post">
        <input type="hidden" name="intent" value="delete" />
        <button type="submit">Delete</button>
      </Form>
    </>
  );
}
```

## Error Handling

### Pattern 1: Error Boundaries

```typescript
// app/routes/posts.$id.tsx
export async function loader({ params }: LoaderFunctionArgs) {
  const post = await db.post.findUnique({ where: { id: params.id } });
  
  if (!post) {
    throw new Response("Post not found", { status: 404 });
  }
  
  return json({ post });
}

export function ErrorBoundary() {
  const error = useRouteError();
  
  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }
  
  return <div>Something went wrong!</div>;
}
```

### Pattern 2: Nested Error Boundaries

```typescript
// Root error boundary (app/root.tsx)
export function ErrorBoundary() {
  return (
    <html>
      <body>
        <h1>Application Error</h1>
        <p>Sorry, something went wrong.</p>
      </body>
    </html>
  );
}

// Route-specific error boundary
export function ErrorBoundary() {
  return (
    <div>
      <h1>Post Error</h1>
      <p>Couldn't load this post.</p>
    </div>
  );
}
```

## Nested Routes

### Pattern 1: Layout Routes

```typescript
// app/routes/dashboard.tsx (layout)
import { Outlet } from "@remix-run/react";

export default function Dashboard() {
  return (
    <div>
      <nav>{/* Dashboard navigation */}</nav>
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}

// app/routes/dashboard.settings.tsx (child)
export default function Settings() {
  return <div>Settings content</div>;
}

// app/routes/dashboard.profile.tsx (child)
export default function Profile() {
  return <div>Profile content</div>;
}
```

### Pattern 2: Pathless Layouts

```typescript
// app/routes/_auth.tsx (pathless layout - note the underscore)
export default function AuthLayout() {
  return (
    <div className="auth-container">
      <Outlet />
    </div>
  );
}

// app/routes/_auth.login.tsx
// URL: /login (not /_auth/login)
export default function Login() {
  return <Form>{/* login form */}</Form>;
}

// app/routes/_auth.signup.tsx
// URL: /signup
export default function Signup() {
  return <Form>{/* signup form */}</Form>;
}
```

## Resource Routes

### Pattern 1: Image Generation

```typescript
// app/routes/og.$id.tsx
import { LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ params }: LoaderFunctionArgs) {
  const post = await getPost(params.id);
  const image = await generateOGImage(post);
  
  return new Response(image, {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=31536000, immutable"
    }
  });
}
```

### Pattern 2: File Downloads

```typescript
// app/routes/downloads.$fileId.tsx
export async function loader({ params }: LoaderFunctionArgs) {
  const file = await getFile(params.fileId);
  const stream = await getFileStream(file.path);
  
  return new Response(stream, {
    headers: {
      "Content-Type": file.mimeType,
      "Content-Disposition": `attachment; filename="${file.name}"`
    }
  });
}
```

## Best Practices

### 1. Prefer Server-Side Logic

❌ **Don't fetch on the client:**
```typescript
export default function Posts() {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    fetch("/api/posts").then(r => r.json()).then(setPosts);
  }, []);
}
```

✅ **Do use loaders:**
```typescript
export async function loader() {
  const posts = await db.post.findMany();
  return json({ posts });
}

export default function Posts() {
  const { posts } = useLoaderData<typeof loader>();
  return <div>{/* render posts */}</div>;
}
```

### 2. Use Form Component

❌ **Don't use fetch for mutations:**
```typescript
function handleSubmit(e) {
  e.preventDefault();
  fetch("/api/posts", { method: "POST", body: formData });
}
```

✅ **Do use Form:**
```typescript
export default function NewPost() {
  return (
    <Form method="post">
      <input name="title" />
      <button type="submit">Create</button>
    </Form>
  );
}
```

### 3. Colocate Related Code

✅ **Keep route concerns together:**
```typescript
// app/routes/posts.$id.tsx
// - loader (data fetching)
// - action (mutations)
// - component (UI)
// - ErrorBoundary (error handling)
// All in one file!
```

### 4. Use Type Safety

```typescript
import type { LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ params }: LoaderFunctionArgs) {
  // TypeScript knows about params, request, etc.
}

export default function Component() {
  // Automatic type inference from loader!
  const data = useLoaderData<typeof loader>();
  //    ^? data is typed based on loader return
}
```

### 5. Handle Loading States

```typescript
import { useNavigation } from "@remix-run/react";

export default function Component() {
  const navigation = useNavigation();
  const isSubmitting = navigation.state === "submitting";
  
  return (
    <Form method="post">
      <button disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save"}
      </button>
    </Form>
  );
}
```

## Common Gotchas

### 1. Loader Return Types

Always use `json()` or `Response`:

```typescript
✅ return json({ data });
✅ return new Response(data);
❌ return { data };  // Won't work correctly
```

### 2. Form Data is Always Strings

```typescript
const formData = await request.formData();
const age = formData.get("age");  // This is a string!

// Convert to number
const ageNumber = Number(age);
```

### 3. Redirects Stop Execution

```typescript
export async function action({ request }: ActionFunctionArgs) {
  if (!isValid) {
    return json({ error: "Invalid" });  // Continues execution
  }
  
  throw redirect("/login");  // Stops execution immediately
}
```

## Performance Tips

### 1. Parallel Data Loading

```typescript
export async function loader() {
  // These load in parallel!
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments()
  ]);
  
  return json({ user, posts, comments });
}
```

### 2. Cache Headers

```typescript
export async function loader() {
  const data = await getStaticData();
  
  return json(data, {
    headers: {
      "Cache-Control": "public, max-age=3600"
    }
  });
}
```

### 3. Defer for Streaming

```typescript
import { defer } from "@remix-run/node";
import { Await, useLoaderData } from "@remix-run/react";
import { Suspense } from "react";

export async function loader() {
  return defer({
    critical: await getCriticalData(),  // Wait for this
    deferred: getDeferredData()          // Don't wait
  });
}

export default function Component() {
  const { critical, deferred } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <div>{critical}</div>
      
      <Suspense fallback={<div>Loading...</div>}>
        <Await resolve={deferred}>
          {(data) => <div>{data}</div>}
        </Await>
      </Suspense>
    </div>
  );
}
```

## Further Reading

- Remix Docs: https://remix.run/docs
- Remix Guide: https://remix.run/guide
- Remix Examples: https://github.com/remix-run/examples
