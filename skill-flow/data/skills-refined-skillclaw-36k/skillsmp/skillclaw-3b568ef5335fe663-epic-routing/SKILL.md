---
name: epic-routing
description: Use this skill when you need to create and manage routes in an Epic Stack application using React Router and react-router-auto-routes.
---

# Epic Stack: Routing

## When to use this skill

Use this skill when you need to:
- Create new routes or pages in an Epic Stack application
- Implement nested layouts
- Configure resource routes (routes without UI)
- Work with route parameters and search params
- Understand Epic Stack's file-based routing conventions
- Implement loaders and actions in routes

## Patterns and conventions

### Routing Philosophy

Following Epic Web principles:

**Do as little as possible** - Keep your route structure simple. Don't create complex nested routes unless you actually need them. Start simple and add complexity only when there's a clear benefit.

**Avoid over-engineering** - Don't create abstractions or complex route structures "just in case". Use the simplest structure that works for your current needs.

**Example - Simple route structure:**
```typescript
// ✅ Good - Simple, straightforward route
// app/routes/users/$username.tsx
export async function loader({ params }: Route.LoaderArgs) {
	const user = await prisma.user.findUnique({
		where: { username: params.username },
		select: { id: true, username: true, name: true },
	})
	return { user }
}

export default function UserRoute({ loaderData }: Route.ComponentProps) {
	return <div>{loaderData.user.name}</div>
}

// ❌ Avoid - Over-engineered route structure
// app/routes/users/$username/_layout.tsx
// app/routes/users/$username/index.tsx
// app/routes/users/$username/_components/UserHeader.tsx
// app/routes/users/$username/_components/UserDetails.tsx
// Unnecessary complexity for a simple user page
```

**Example - Add complexity only when needed:**
```typescript
// ✅ Good - Add nested routes only when you actually need them
// If you have user notes, then nested routes make sense:
// app/routes/users/$username/notes/_layout.tsx
// app/routes/users/$username/notes/index.tsx
// app/routes/users/$username/notes/$noteId.tsx

// ❌ Avoid - Creating nested routes "just in case"
// Don't create complex structures before you need them
```

### File-based routing with react-router-auto-routes

Epic Stack uses `react-router-auto-routes` instead of React Router's standard convention. This enables better organization and code co-location.

**Basic structure:**
```
app/routes/
├── _layout.tsx        # Layout for child routes
├── index.tsx      
```