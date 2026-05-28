---
name: epic-auth
description: Use this skill when you need to implement user authentication, manage sessions, configure OAuth, and enhance security with 2FA and passkeys in the Epic Stack.
---

# Epic Stack: Authentication

## When to use this skill

Use this skill when you need to:
- Implement user authentication
- Work with sessions and cookies
- Configure OAuth providers (GitHub, Google, etc.)
- Implement 2FA (Two-Factor Authentication)
- Implement WebAuthn/Passkeys
- Handle login, signup, logout flows
- Manage email verification
- Implement password reset

## Patterns and conventions

### Authentication Philosophy

Following Epic Web principles:

**Least privilege** - Users should only have access to what they need, when they need it. Sessions should have minimal permissions and expire appropriately. Don't grant more access than necessary.

**Design to fail fast and early** - Validate authentication and authorization as early as possible. Check session validity immediately, verify permissions before processing requests, and return clear errors quickly.

### Example - Least privilege in sessions:
```typescript
// ✅ Good - Minimal session data, explicit permissions
const session = await prisma.session.create({
	data: {
		expirationDate: getSessionExpirationDate(),
		userId, // Only store user ID, not full user data
	},
})

// Session only grants access to this specific user
// Permissions checked separately when needed

// ❌ Avoid - Storing too much in session
const session = await prisma.session.create({
	data: {
		expirationDate: getSessionExpirationDate(),
		userId,
		userRole: 'admin', // Don't store roles in session
		permissions: ['all'], // Don't store permissions in session
	},
})
// Roles and permissions should be checked from database, not session
```

### Example - Fail fast authentication:
```typescript
// ✅ Good - Validate authentication early
export async function loader({ request }: Route.LoaderArgs) {
	// Check authentication immediately - fail fast
	const userId = await requireUserId(request)
	
	// Check permissions early - fail fast
	await requireUserWithPermission(request, 'read:note:own')
	
	// Only proceed if authenticated and authorized
	const notes = await prisma.note.findMany({
		where: { ownerId: userId },
	})
	
	return { notes }
}

// ❌ Avoid - Delayed authentication check
export async function loader({ request }: Route.LoaderArgs) {
	// Process request first...
	const notes = await prisma.note.findMany()
	
	// Check authentication at the end
}
```