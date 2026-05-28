---
name: add-api-route
description: Scaffolds Next.js API routes with authentication, restaurant access control, validation, and error handling patterns. Use /api-route [path] [methods] to create routes following project conventions.
allowed-tools: Read, Write, Glob
---

# Add API Route Skill

## Overview

Scaffolds API routes that follow the project's established patterns:
- NextAuth session authentication
- Restaurant access verification via UserRestaurant junction table
- Role-based access control (Manager/Editor)
- Standard error handling and responses
- TypeScript with proper typing

## Command

`/api-route [path] [methods]`

**Examples:**
- `/api-route orders GET,POST` - Creates app/api/orders/route.ts
- `/api-route orders/[id] GET,PUT,DELETE` - Creates app/api/orders/[id]/route.ts
- `/api-route orders/[id]/items GET,POST` - Creates nested route

## Route Template

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

// GET /api/{path} - [Description]
export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const restaurantId = searchParams.get('restaurantId')

    if (!restaurantId) {
      return NextResponse.json(
        { error: 'restaurantId is required' },
        { status: 400 }
      )
    }

    // Verify user has access to this restaurant
    const userRestaurant = await prisma.userRestaurant.findUnique({
      where: {
        userId_restaurantId: {
          userId: session.user.id,
          restaurantId
        }
      }
    })

    if (!userRestaurant) {
      return NextResponse.json(
        { error: 'Access denied to this restaurant' },
        { status: 403 }
      )
    }

    // TODO: Implement query logic
    const data = await prisma.modelName.findMany({
      where: { restaurantId },
      orderBy: { createdAt: 'desc' }
    })

    return NextResponse.json({ data })
  } catch (error) {
    console.error('Error fetching data:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

## Dynamic Route Template ([id])

For routes with dynamic parameters, use this pattern:

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

interface RouteParams {
  params: Promise<{ id: string }>
}

// GET /api/{path}/[id]
export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id } = await params

    // Fetch item and verify restaurant access
    const item = await prisma.modelName.findUnique({
      where: { id },
      include: { restaurant: true }
    })

    if (!item) {
      return NextResponse.json({ error: 'Not found' }, { status: 404 })
    }

    // Verify user has access to this restaurant
    const userRestaurant = await prisma.userRestaurant.findUnique({
      where: {
        userId_restaurantId: {
          userId: session.user.id,
          restaurantId: item.restaurantId
        }
      }
    })

    if (!userRestaurant) {
      return NextResponse.json(
        { error: 'Access denied' },
        { status: 403 }
      )
    }

    return NextResponse.json({ item })
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

## POST with Manager-Only Access

```typescript
// POST /api/{path} - Create new item (Manager only)
export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Check Manager role
    const user = await prisma.user.findUnique({
      where: { id: session.user.id },
      select: { role: true }
    })

    if (user?.role !== 'Manager') {
      return NextResponse.json(
        { error: 'Only managers can perform this action' },
        { status: 403 }
      )
    }

    const body = await request.json()

    // Validate required fields
    if (!body.restaurantId) {
      return NextResponse.json(
        { error: 'restaurantId is required' },
        { status: 400 }
      )
    }

    // Verify user has access to this restaurant
    const userRestaurant = await prisma.userRestaurant.findUnique({
      where: {
        userId_restaurantId: {
          userId: session.user.id,
          restaurantId: body.restaurantId
        }
      }
    })

    if (!userRestaurant) {
      return NextResponse.json(
        { error: 'Access denied to this restaurant' },
        { status: 403 }
      )
    }

    // TODO: Add field validation

    // Create item
    const item = await prisma.modelName.create({
      data: {
        restaurantId: body.restaurantId,
        // ... other fields
      }
    })

    return NextResponse.json({ item }, { status: 201 })
  } catch (error) {
    console.error('Error creating item:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

## Process

When user invokes `/api-route [path] [methods]`:

1. Parse the path to determine:
   - File location (app/api/{path}/route.ts)
   - Dynamic segments (e.g., [id])
   - Related Prisma model (infer from path or ask)

2. Generate route file with:
   - All requested HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Proper authentication checks
   - Restaurant access verification
   - Role checks for write operations
   - TypeScript types

3. Create the file and report:
   - File path created
   - Methods implemented
   - TODOs for customization

## Validation Patterns

Use these validation patterns as needed:

```typescript
// Email validation
if (body.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email)) {
  return NextResponse.json({ error: 'Invalid email format' }, { status: 400 })
}

// Enum validation
const validTypes = ['TypeA', 'TypeB', 'TypeC']
if (body.type && !validTypes.includes(body.type)) {
  return NextResponse.json({ error: 'Invalid type' }, { status: 400 })
}

// Positive number validation
if (body.amount && body.amount < 0) {
  return NextResponse.json({ error: 'Amount must be positive' }, { status: 400 })
}

// Required string validation
if (!body.name || !body.name.trim()) {
  return NextResponse.json({ error: 'Name is required' }, { status: 400 })
}
```

## Response Patterns

```typescript
// Success responses
return NextResponse.json({ data })                    // 200 OK (default)
return NextResponse.json({ item }, { status: 201 })   // 201 Created
return new NextResponse(null, { status: 204 })        // 204 No Content (DELETE)

// Error responses
return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
return NextResponse.json({ error: 'Not found' }, { status: 404 })
return NextResponse.json({ error: 'Validation error' }, { status: 400 })
return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
```

## Tips

- Always use `restaurantId` for multi-tenant queries
- Use `await params` for dynamic route parameters (Next.js 15+)
- Manager role required for: create, update, delete, approve operations
- Editor role can: submit items for approval, view data
- Include `console.error` for debugging in catch blocks
