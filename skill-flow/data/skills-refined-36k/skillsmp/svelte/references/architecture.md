# Architecture Reference

## src/lib Structures

### Basic

```
$lib/
├── utils/           # Pure utility functions
├── components/      # Shared UI components
├── data/            # DAL - *.remote.ts files
├── server/          # Server-only code
│   └── database/    # DB access layer
└── types/           # Shared types
```

### Route-Colocated

```
routes/
├── blog/
│   ├── +page.svelte
│   ├── +page.ts
│   ├── BlogList.svelte      # route-specific component
│   └── blog-rules.ts        # route-specific logic
lib/
├── components/              # shared components only
├── data/
└── server/database/
```

### DDD (Domain-Driven)

For large apps with clear domain boundaries.

```
$lib/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── data.remote.ts
│   │   ├── database.server.ts
│   │   └── types.ts
│   └── blog/
│       └── ...
└── shared/
    ├── utils/
    └── components/
```

## Auth Helpers

```ts
// $lib/server/auth.ts
export async function getUserFromCookies(cookies: Cookies) {
  const session = cookies.get("session_id");
  if (!session) return null;
  return await db.users.findBySession(session);
}

export async function requireUser() {
  const { cookies } = getRequestEvent();
  const user = await getUserFromCookies(cookies);
  if (!user) error(401, "Unauthorized");
  return user;
}

export async function requirePostOwner(postId: string) {
  const user = await requireUser();
  const post = await db.posts.findById(postId);
  if (post?.author_id !== user.id) error(403, "Forbidden");
  return { user, post };
}
```
