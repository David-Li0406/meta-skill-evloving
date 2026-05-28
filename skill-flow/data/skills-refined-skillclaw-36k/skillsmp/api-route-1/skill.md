---
name: api-route
description: Create Next.js API routes with Better Auth, RBAC, and error handling using Drizzle ORM
allowed-tools: [Write, Read, Edit, Bash]
---

## Purpose
Generate Next.js 16 API routes following project conventions for Better Auth authentication, authorization, error handling, and Drizzle ORM database operations.

## Guidelines

### 1. API Route Structure
Location: `src/app/api/<resource>/route.ts`

### 2. Standard Template
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { z } from 'zod';
import { db } from '@/infrastructure/database/drizzle';
import { resourceTable } from '@/infrastructure/database/schema';
import { eq, and } from 'drizzle-orm';
import { hasPermission } from '@/lib/rbac';

// Request validation schema
const RequestSchema = z.object({
  field: z.string().min(1, 'Field is required'),
  // Add more fields...
});

export async function GET(request: NextRequest) {
  try {
    // 1. Authentication check
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 2. Authorization check (if needed)
    if (!hasPermission(session.user.role, 'resource:read')) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    // 3. Parse query params
    const { searchParams } = new URL(request.url);
    const paramValue = searchParams.get('param');

    // 4. Database operations with Drizzle
    const results = await db
      .select()
      .from(resourceTable)
      .where(eq(resourceTable.userId, session.user.id));

    // 5. Return success response
    return NextResponse.json({ data: results }, { status: 200 });
  } catch (error) {
    console.error('GET /api/resource error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    // 1. Authentication
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 2. Authorization
    if (!hasPermission(session.user.role, 'resource:create')) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    // 3. Validate request body
    const body = await request.json();
    const validationResult = RequestSchema.safeParse(body);

    if (!validationResult.success) {
      return NextResponse.json(
        {
          error: 'Validation failed',
          details: validationResult.error.errors,
        },
        { status: 400 }
      );
    }

    const data = validationResult.data;

    // 4. Database operation with Drizzle
    const [newResource] = await db
      .insert(resourceTable)
      .values({
        field: data.field,
        userId: session.user.id,
        createdAt: new Date(),
        updatedAt: new Date(),
      })
      .returning();

    // 5. Return created resource
    return NextResponse.json({ data: newResource }, { status: 201 });
  } catch (error) {
    console.error('POST /api/resource error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PATCH(request: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { id, ...updates } = body;

    // Verify ownership or admin
    const [resource] = await db
      .select()
      .from(resourceTable)
      .where(eq(resourceTable.id, id))
      .limit(1);

    if (!resource) {
      return NextResponse.json({ error: 'Resource not found' }, { status: 404 });
    }

    const isOwner = resource.userId === session.user.id;
    const isAdmin = session.user.role === 'admin';

    if (!isOwner && !isAdmin) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    // Update resource
    const [updated] = await db
      .update(resourceTable)
      .set({
        ...updates,
        updatedAt: new Date(),
      })
      .where(eq(resourceTable.id, id))
      .returning();

    return NextResponse.json({ data: updated }, { status: 200 });
  } catch (error) {
    console.error('PATCH /api/resource error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { error: 'Missing resource ID' },
        { status: 400 }
      );
    }

    // Check ownership/authorization
    const [resource] = await db
      .select()
      .from(resourceTable)
      .where(eq(resourceTable.id, id))
      .limit(1);

    if (!resource) {
      return NextResponse.json({ error: 'Resource not found' }, { status: 404 });
    }

    const isOwner = resource.userId === session.user.id;
    const isAdmin = session.user.role === 'admin';

    if (!isOwner && !isAdmin) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    // Delete resource
    await db.delete(resourceTable).where(eq(resourceTable.id, id));

    return NextResponse.json(
      { message: 'Deleted successfully' },
      { status: 200 }
    );
  } catch (error) {
    console.error('DELETE /api/resource error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 3. Authentication Patterns (Better Auth)

**Require authentication:**
```typescript
import { auth } from '@/lib/auth';

const session = await auth();
if (!session?.user?.id) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}
```

**Optional authentication:**
```typescript
const session = await auth();
const userId = session?.user?.id;
// Proceed with optional user context
```

**Access user info:**
```typescript
const session = await auth();
const { id, email, name, role, subscriptionStatus } = session.user;
```

### 4. Authorization Patterns

**Role-based:**
```typescript
import { hasPermission } from '@/lib/rbac';

if (!hasPermission(session.user.role, 'resource:action')) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
}
```

**Ownership-based:**
```typescript
const [resource] = await db
  .select()
  .from(resourceTable)
  .where(eq(resourceTable.id, id))
  .limit(1);

const isOwner = resource.userId === session.user.id;
const isAdmin = session.user.role === 'admin';

if (!isOwner && !isAdmin) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
}
```

**Group-based:**
```typescript
import { groupMembers } from '@/infrastructure/database/schema';

const [membership] = await db
  .select()
  .from(groupMembers)
  .where(
    and(
      eq(groupMembers.groupId, groupId),
      eq(groupMembers.userId, session.user.id)
    )
  )
  .limit(1);

if (!membership || !['admin', 'owner'].includes(membership.role)) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
}
```

### 5. Validation with Zod
```typescript
import { z } from 'zod';

const Schema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
  role: z.enum(['user', 'admin', 'teacher']),
});

const result = Schema.safeParse(body);
if (!result.success) {
  return NextResponse.json(
    {
      error: 'Validation failed',
      details: result.error.errors,
    },
    { status: 400 }
  );
}
```

### 6. Error Handling
```typescript
// Success responses
return NextResponse.json({ data: result }, { status: 200 });
return NextResponse.json({ data: result }, { status: 201 }); // Created

// Error responses
return NextResponse.json({ error: 'Message' }, { status: 400 }); // Bad Request
return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
return NextResponse.json({ error: 'Not Found' }, { status: 404 });
return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
```

### 7. Drizzle ORM Database Patterns

**Read operations:**
```typescript
import { db } from '@/infrastructure/database/drizzle';
import { users, posts } from '@/infrastructure/database/schema';
import { eq, and, or, like, gte, desc } from 'drizzle-orm';

// Select all
const allUsers = await db.select().from(users);

// Select with condition
const user = await db.select().from(users).where(eq(users.id, userId));

// Select with multiple conditions
const results = await db
  .select()
  .from(posts)
  .where(
    and(
      eq(posts.userId, userId),
      gte(posts.createdAt, new Date('2024-01-01'))
    )
  )
  .orderBy(desc(posts.createdAt));

// Select specific fields
const userEmails = await db
  .select({ email: users.email, name: users.name })
  .from(users);

// Joins
const postsWithUsers = await db
  .select()
  .from(posts)
  .leftJoin(users, eq(posts.userId, users.id));
```

**Write operations:**
```typescript
// Insert single record
const [newUser] = await db
  .insert(users)
  .values({
    email: 'test@example.com',
    name: 'Test User',
  })
  .returning();

// Insert multiple records
await db.insert(posts).values([
  { title: 'Post 1', userId: '123' },
  { title: 'Post 2', userId: '123' },
]);

// Update
await db
  .update(users)
  .set({ name: 'New Name', updatedAt: new Date() })
  .where(eq(users.id, userId));

// Delete
await db.delete(users).where(eq(users.id, userId));
```

**Transactions:**
```typescript
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ ... }).returning();
  await tx.insert(profiles).values({ userId: user.id, ... });
});
```

### 8. Dynamic Routes
For routes like `/api/resource/[id]/route.ts`:

```typescript
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  // Use id in your queries
  const [resource] = await db
    .select()
    .from(resourceTable)
    .where(eq(resourceTable.id, id))
    .limit(1);
}
```

## Best Practices
- ✅ Always validate input with Zod
- ✅ Check authentication before authorization
- ✅ Use Drizzle's query builder for type-safe queries
- ✅ Log errors with context
- ✅ Return appropriate HTTP status codes
- ✅ Use transactions for multi-step operations
- ✅ Use `.returning()` to get inserted/updated data
- ✅ Use `.limit(1)` when selecting single records
- ✅ Import operators (eq, and, or, etc.) from 'drizzle-orm'
- ⚠️ Never trust user input
- ⚠️ Always check ownership before modifications
- ⚠️ Sanitize error messages sent to client
- ⚠️ Handle database connection errors gracefully
