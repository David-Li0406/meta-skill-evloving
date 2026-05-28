# API Design Framework

## Purpose

Design clean, consistent APIs that are easy to use, maintain, and evolve. Optimized for Next.js API routes and Supabase integration.

---

## Design Principles

### 1. Consistency

Same patterns everywhere:
- URL structure
- Request/response format
- Error handling
- Authentication

### 2. Simplicity

- REST over GraphQL (for most cases)
- Intuitive endpoints
- Minimal nesting

### 3. Type Safety

- Zod validation on all inputs
- TypeScript types for all responses
- Generated client types

---

## URL Structure

### RESTful Resource Patterns

```
# Collection operations
GET    /api/v1/projects          # List projects
POST   /api/v1/projects          # Create project

# Single resource operations
GET    /api/v1/projects/{id}     # Get project
PATCH  /api/v1/projects/{id}     # Update project
DELETE /api/v1/projects/{id}     # Delete project

# Nested resources
GET    /api/v1/projects/{id}/tasks      # List project tasks
POST   /api/v1/projects/{id}/tasks      # Create task in project

# Actions (when CRUD doesn't fit)
POST   /api/v1/projects/{id}/archive    # Archive project
POST   /api/v1/projects/{id}/duplicate  # Duplicate project
```

### Naming Conventions

| Convention | Example | Why |
|------------|---------|-----|
| Plural nouns | `/projects` not `/project` | Collections are plural |
| Lowercase | `/api/v1/projects` | URL consistency |
| Hyphens for multi-word | `/api/v1/user-settings` | URL readability |
| No verbs in URL | `/projects` not `/getProjects` | HTTP methods are verbs |

---

## Request/Response Format

### Standard Request

```typescript
// POST /api/v1/projects
{
  "name": "My Project",
  "description": "A description",
  "settings": {
    "isPublic": false
  }
}
```

### Standard Success Response

```typescript
// Single resource
{
  "data": {
    "id": "uuid",
    "name": "My Project",
    "createdAt": "2024-01-15T10:00:00Z"
  }
}

// Collection
{
  "data": [
    { "id": "uuid1", "name": "Project 1" },
    { "id": "uuid2", "name": "Project 2" }
  ],
  "meta": {
    "total": 50,
    "page": 1,
    "pageSize": 20
  }
}
```

### Standard Error Response

```typescript
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

---

## Implementation Patterns

### Route Handler Structure

```typescript
// app/api/v1/projects/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { z } from 'zod'

// Validation schemas
const createProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional()
})

// GET /api/v1/projects
export async function GET(request: Request) {
  try {
    const supabase = await createClient()
    const { searchParams } = new URL(request.url)

    const page = parseInt(searchParams.get('page') || '1')
    const pageSize = parseInt(searchParams.get('pageSize') || '20')
    const offset = (page - 1) * pageSize

    const { data, error, count } = await supabase
      .from('projects')
      .select('*', { count: 'exact' })
      .range(offset, offset + pageSize - 1)
      .order('created_at', { ascending: false })

    if (error) throw error

    return NextResponse.json({
      data,
      meta: {
        total: count,
        page,
        pageSize
      }
    })
  } catch (error) {
    return handleError(error)
  }
}

// POST /api/v1/projects
export async function POST(request: Request) {
  try {
    const supabase = await createClient()
    const body = await request.json()

    // Validate
    const result = createProjectSchema.safeParse(body)
    if (!result.success) {
      return NextResponse.json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: result.error.issues.map(i => ({
            field: i.path.join('.'),
            message: i.message
          }))
        }
      }, { status: 400 })
    }

    // Create
    const { data, error } = await supabase
      .from('projects')
      .insert(result.data)
      .select()
      .single()

    if (error) throw error

    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    return handleError(error)
  }
}
```

### Dynamic Route Handler

```typescript
// app/api/v1/projects/[id]/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

type Params = { params: Promise<{ id: string }> }

// GET /api/v1/projects/{id}
export async function GET(request: Request, { params }: Params) {
  try {
    const { id } = await params
    const supabase = await createClient()

    const { data, error } = await supabase
      .from('projects')
      .select('*')
      .eq('id', id)
      .single()

    if (error) {
      if (error.code === 'PGRST116') {
        return NextResponse.json({
          error: { code: 'NOT_FOUND', message: 'Project not found' }
        }, { status: 404 })
      }
      throw error
    }

    return NextResponse.json({ data })
  } catch (error) {
    return handleError(error)
  }
}

// PATCH /api/v1/projects/{id}
export async function PATCH(request: Request, { params }: Params) {
  try {
    const { id } = await params
    const supabase = await createClient()
    const body = await request.json()

    const { data, error } = await supabase
      .from('projects')
      .update(body)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error

    return NextResponse.json({ data })
  } catch (error) {
    return handleError(error)
  }
}

// DELETE /api/v1/projects/{id}
export async function DELETE(request: Request, { params }: Params) {
  try {
    const { id } = await params
    const supabase = await createClient()

    const { error } = await supabase
      .from('projects')
      .delete()
      .eq('id', id)

    if (error) throw error

    return new Response(null, { status: 204 })
  } catch (error) {
    return handleError(error)
  }
}
```

---

## Error Handling

### Error Utility

```typescript
// lib/utils/api-errors.ts
import { NextResponse } from 'next/server'

export const ErrorCodes = {
  VALIDATION_ERROR: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  INTERNAL_ERROR: 500
} as const

type ErrorCode = keyof typeof ErrorCodes

export function apiError(
  code: ErrorCode,
  message: string,
  details?: unknown
) {
  return NextResponse.json({
    error: { code, message, details }
  }, { status: ErrorCodes[code] })
}

export function handleError(error: unknown) {
  console.error('API Error:', error)

  // Supabase errors
  if (error && typeof error === 'object' && 'code' in error) {
    const supaError = error as { code: string; message: string }

    if (supaError.code === 'PGRST116') {
      return apiError('NOT_FOUND', 'Resource not found')
    }
    if (supaError.code === '23505') {
      return apiError('CONFLICT', 'Resource already exists')
    }
    if (supaError.code === '42501') {
      return apiError('FORBIDDEN', 'Access denied')
    }
  }

  return apiError('INTERNAL_ERROR', 'An unexpected error occurred')
}
```

### HTTP Status Codes

| Status | When to Use |
|--------|-------------|
| 200 OK | Successful GET, PATCH |
| 201 Created | Successful POST creating resource |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Validation error |
| 401 Unauthorized | Not authenticated |
| 403 Forbidden | Authenticated but not allowed |
| 404 Not Found | Resource doesn't exist |
| 409 Conflict | Duplicate resource |
| 500 Internal Error | Server error |

---

## Authentication

### Middleware Pattern

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  // Skip for public routes
  if (request.nextUrl.pathname.startsWith('/api/v1/public')) {
    return NextResponse.next()
  }

  const response = NextResponse.next()

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options)
          })
        }
      }
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  if (!user && request.nextUrl.pathname.startsWith('/api/v1')) {
    return NextResponse.json(
      { error: { code: 'UNAUTHORIZED', message: 'Authentication required' } },
      { status: 401 }
    )
  }

  return response
}

export const config = {
  matcher: '/api/:path*'
}
```

---

## Pagination

### Offset-Based (Simple)

```typescript
// Good for small-medium datasets

GET /api/v1/projects?page=2&pageSize=20

// Response
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 2,
    "pageSize": 20,
    "totalPages": 5
  }
}
```

### Cursor-Based (Scalable)

```typescript
// Good for large datasets, real-time feeds

GET /api/v1/projects?cursor=abc123&limit=20

// Response
{
  "data": [...],
  "meta": {
    "nextCursor": "def456",
    "hasMore": true
  }
}
```

---

## Query Parameters

### Filtering

```
GET /api/v1/projects?status=active
GET /api/v1/projects?status=active,archived
GET /api/v1/projects?createdAfter=2024-01-01
```

### Sorting

```
GET /api/v1/projects?sort=createdAt:desc
GET /api/v1/projects?sort=name:asc,createdAt:desc
```

### Field Selection

```
GET /api/v1/projects?fields=id,name,status
```

### Search

```
GET /api/v1/projects?q=my%20project
```

---

## Validation with Zod

```typescript
// lib/validations/project.ts
import { z } from 'zod'

export const createProjectSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters'),
  description: z.string().max(500).optional(),
  settings: z.object({
    isPublic: z.boolean().default(false),
    allowComments: z.boolean().default(true)
  }).optional()
})

export const updateProjectSchema = createProjectSchema.partial()

export const queryParamsSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  pageSize: z.coerce.number().min(1).max(100).default(20),
  status: z.enum(['active', 'archived', 'all']).optional(),
  sort: z.string().optional()
})

export type CreateProject = z.infer<typeof createProjectSchema>
export type UpdateProject = z.infer<typeof updateProjectSchema>
```

---

## API Versioning

### URL Versioning (Recommended)

```
/api/v1/projects
/api/v2/projects
```

**In Next.js:**
```
app/
  api/
    v1/
      projects/
        route.ts
    v2/
      projects/
        route.ts
```

### When to Version

- Breaking changes to response shape
- Removing fields
- Changing field types
- Removing endpoints

### When NOT to Version

- Adding new fields (backwards compatible)
- Adding new endpoints
- Bug fixes
