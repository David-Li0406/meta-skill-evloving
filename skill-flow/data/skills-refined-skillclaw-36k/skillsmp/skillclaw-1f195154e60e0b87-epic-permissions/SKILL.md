---
name: epic-permissions
description: Use this skill when you need to implement role-based access control (RBAC) and manage permissions effectively in the Epic Stack.
---

# Epic Stack: Permissions

## When to use this skill

Use this skill when you need to:
- Implement role-based access control (RBAC)
- Validate permissions on server-side or client-side
- Create new permissions or roles
- Restrict access to routes or actions
- Implement granular permissions (`own` vs `any`)

## Patterns and conventions

### Permissions Philosophy

Following Epic Web principles:

**Explicit is better than implicit** - Always explicitly check permissions. Don't assume a user has access based on implicit rules or hidden logic. Every permission check should be visible and clear in the code.

**Example - Explicit permission checks:**
```typescript
// ✅ Good - Explicit permission check
export async function action({ request }: Route.ActionArgs) {
	const userId = await requireUserId(request)
	
	// Explicitly check permission - clear and visible
	await requireUserWithPermission(request, 'delete:note:own')
	
	// Permission check is explicit and obvious
	await prisma.note.delete({ where: { id: noteId } })
}

// ❌ Avoid - Implicit permission check
export async function action({ request }: Route.ActionArgs) {
	const userId = await requireUserId(request)
	const note = await prisma.note.findUnique({ where: { id: noteId } })
	
	// Implicit check - not clear what permission is being checked
	if (note.ownerId !== userId) {
		throw new Response('Forbidden', { status: 403 })
	}
	// What permission does this represent? Not explicit
}
```

**Example - Explicit permission strings:**
```typescript
// ✅ Good - Explicit permission string
const permission: PermissionString = 'delete:note:own'
// Clear: action (delete), entity (note), access (own)

await requireUserWithPermission(request, permission)

// ❌ Avoid - Implicit or unclear permissions
const canDelete = checkUserCanDelete(user, note)
// What permission is this checking? Not explicit
```

### RBAC Model

Epic Stack uses an RBAC (Role-Based Access Control) model where:
- **Users** have **Roles**
- **Roles** have **Permissions**
- A user's permissions are the union of all permissions from their roles

### Permission Structure

Permissions follow the format: `action:entity:access`

**Components:**
- `action`: The allowed action (`create`, `read`, `update`, `delete`)
- `entity`: The entity being acted upon (`user`, `note`, etc.)
- `access`: The access level (`own`, `any`, etc.)