---
name: new-api-endpoint
description: Scaffold a new API endpoint following project patterns. Use when creating new API routes. Invoke with "/new-api-endpoint [path] [methods]".
model: sonnet
---

# New API Endpoint Skill

Create a new API endpoint following the project's established patterns.

## Usage

```
/new-api-endpoint students/[id]/grades GET,POST
/new-api-endpoint payments POST,PUT
/new-api-endpoint reports/attendance GET
```

## Process

1. **Parse the request** - Extract path and HTTP methods
2. **Create route file** - At `app/ui/app/api/[path]/route.ts`
3. **Implement handlers** - For each specified method
4. **Add types** - Request/response TypeScript types
5. **Add i18n keys** - If any user-facing error messages

## Template Structure

```typescript
import { NextRequest, NextResponse } from "next/server"
import { requireSession } from "@/lib/auth"
import prisma from "@/lib/prisma"

// Types
type RouteParams = {
  params: Promise<{ id: string }>
}

// GET - Fetch resource
export async function GET(
  req: NextRequest,
  { params }: RouteParams
) {
  const { session, error } = await requireSession()
  if (error) return error

  const { id } = await params

  try {
    const data = await prisma.model.findUnique({
      where: { id },
    })

    if (!data) {
      return NextResponse.json(
        { error: "Not found" },
        { status: 404 }
      )
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error("GET /api/path error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

// POST - Create resource
export async function POST(req: NextRequest) {
  const { session, error } = await requireSession()
  if (error) return error

  try {
    const body = await req.json()

    // Validate body
    if (!body.requiredField) {
      return NextResponse.json(
        { error: "Missing required field" },
        { status: 400 }
      )
    }

    const data = await prisma.model.create({
      data: {
        ...body,
        createdBy: session.user.id,
      },
    })

    return NextResponse.json(data, { status: 201 })
  } catch (error) {
    console.error("POST /api/path error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

// PUT - Update resource
export async function PUT(
  req: NextRequest,
  { params }: RouteParams
) {
  const { session, error } = await requireSession()
  if (error) return error

  const { id } = await params

  try {
    const body = await req.json()

    const data = await prisma.model.update({
      where: { id },
      data: {
        ...body,
        updatedBy: session.user.id,
      },
    })

    return NextResponse.json(data)
  } catch (error) {
    console.error("PUT /api/path error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

// DELETE - Remove resource
export async function DELETE(
  req: NextRequest,
  { params }: RouteParams
) {
  const { session, error } = await requireSession()
  if (error) return error

  const { id } = await params

  try {
    await prisma.model.delete({
      where: { id },
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("DELETE /api/path error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
```

## Checklist

Before completing:
- [ ] Route file created at correct path
- [ ] All requested HTTP methods implemented
- [ ] Session validation in place
- [ ] Proper error handling with status codes
- [ ] TypeScript types defined
- [ ] Console logging for errors
- [ ] Prisma queries correct

## Project Conventions

- Use `requireSession()` for auth
- Import Prisma from `@/lib/prisma`
- Use `cuid()` for IDs (Prisma default)
- Return proper HTTP status codes:
  - 200: Success
  - 201: Created
  - 400: Bad request
  - 401: Unauthorized
  - 404: Not found
  - 500: Server error
