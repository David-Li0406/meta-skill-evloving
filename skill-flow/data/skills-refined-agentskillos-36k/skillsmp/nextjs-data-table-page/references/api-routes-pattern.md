# API Routes Pattern

Next.js API routes act as a proxy layer between frontend and backend, handling authentication.

## Directory Structure

```
app/api/[section]/[entity]/
├── route.ts                    # GET (list) + POST (create)
├── [entityId]/
│   ├── route.ts               # GET (single) + PUT (update) + DELETE
│   └── status/
│       └── route.ts           # PUT (toggle status)
├── status/
│   └── route.ts               # POST (bulk status update)
└── counts/
    └── route.ts               # GET (counts for status panel)
```

## Main Route (GET + POST)

```typescript
// app/api/[section]/[entity]/route.ts
import { NextRequest } from "next/server";
import { withAuth, backendGet, backendPost } from "@/lib/fetch/api-route-helper";

/**
 * GET /api/[section]/[entity]
 * Fetches list with pagination, filtering, and sorting
 */
export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams.toString();
  return withAuth(token =>
    backendGet(`/[section]/[entity]/?${params}`, token)
  );
}

/**
 * POST /api/[section]/[entity]
 * Creates a new entity
 */
export async function POST(request: NextRequest) {
  const body = await request.json();
  return withAuth(token =>
    backendPost('/[section]/[entity]/', token, body)
  );
}
```

## Individual Entity Route (PUT)

```typescript
// app/api/[section]/[entity]/[entityId]/route.ts
import { NextRequest } from "next/server";
import { withAuth, backendGet, backendPut, backendDelete } from "@/lib/fetch/api-route-helper";

/**
 * GET /api/[section]/[entity]/[entityId]
 * Fetches single entity
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ entityId: string }> }
) {
  const { entityId } = await params;
  return withAuth(token =>
    backendGet(`/[section]/[entity]/${entityId}`, token)
  );
}

/**
 * PUT /api/[section]/[entity]/[entityId]
 * Updates an existing entity
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ entityId: string }> }
) {
  const { entityId } = await params;
  const body = await request.json();
  return withAuth(token =>
    backendPut(`/[section]/[entity]/${entityId}`, token, body)
  );
}

/**
 * DELETE /api/[section]/[entity]/[entityId]
 * Deletes (or soft-deletes) an entity
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ entityId: string }> }
) {
  const { entityId } = await params;
  return withAuth(token =>
    backendDelete(`/[section]/[entity]/${entityId}`, token)
  );
}
```

## Status Toggle Route

```typescript
// app/api/[section]/[entity]/[entityId]/status/route.ts
import { NextRequest } from "next/server";
import { withAuth, backendPut } from "@/lib/fetch/api-route-helper";

/**
 * PUT /api/[section]/[entity]/[entityId]/status
 * Toggles entity active status
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ entityId: string }> }
) {
  const { entityId } = await params;
  const body = await request.json();
  return withAuth(token =>
    backendPut(`/[section]/[entity]/${entityId}/status`, token, body)
  );
}
```

## Bulk Status Route

```typescript
// app/api/[section]/[entity]/status/route.ts
import { NextRequest } from "next/server";
import { withAuth, backendPost } from "@/lib/fetch/api-route-helper";

/**
 * POST /api/[section]/[entity]/status
 * Updates status for multiple entities (bulk operation)
 */
export async function POST(request: NextRequest) {
  const body = await request.json();
  return withAuth(token =>
    backendPost('/[section]/[entity]/status', token, body)
  );
}
```

## Counts Route (Optional)

```typescript
// app/api/[section]/[entity]/counts/route.ts
import { NextRequest } from "next/server";
import { withAuth, backendGet } from "@/lib/fetch/api-route-helper";

/**
 * GET /api/[section]/[entity]/counts
 * Gets total counts (unaffected by filters)
 */
export async function GET(request: NextRequest) {
  return withAuth(token =>
    backendGet('/[section]/[entity]/counts', token)
  );
}
```

## API Route Helper Pattern

The helper functions (`withAuth`, `backendGet`, etc.) should exist in `@/lib/fetch/api-route-helper.ts`:

```typescript
import { auth } from "@/lib/auth/server-auth";
import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000/api";

export async function withAuth<T>(
  fn: (token: string) => Promise<T>
): Promise<NextResponse> {
  try {
    const session = await auth();
    if (!session?.accessToken) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    const result = await fn(session.accessToken);
    return NextResponse.json(result);
  } catch (error: any) {
    const status = error.status || 500;
    const message = error.message || "Internal server error";
    return NextResponse.json({ error: message }, { status });
  }
}

export async function backendGet(path: string, token: string) {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw { status: res.status, message: await res.text() };
  return res.json();
}

export async function backendPost(path: string, token: string, body: any) {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw { status: res.status, message: await res.text() };
  return res.json();
}

export async function backendPut(path: string, token: string, body: any) {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw { status: res.status, message: await res.text() };
  return res.json();
}

export async function backendDelete(path: string, token: string) {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw { status: res.status, message: await res.text() };
  return res.json();
}
```

## Key Points

1. **Thin proxy layer** - API routes just forward to backend with auth
2. **Consistent error handling** - Use try/catch with proper status codes
3. **Return full entity** - All mutations return the complete updated entity
4. **Use NextRequest** - For type-safe request handling
5. **Await params** - Next.js 15+ requires `await params`
