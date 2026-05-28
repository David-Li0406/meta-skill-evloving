---
name: epic-security
description: Use this skill when you need to implement security best practices for the Epic Stack, including CSP, rate limiting, and session security.
---

# Epic Stack: Security

## When to use this skill

Use this skill when you need to:
- Configure Content Security Policy (CSP)
- Implement spam protection (honeypot)
- Configure rate limiting
- Manage session security
- Implement input validation
- Configure secure headers
- Manage secrets

## Patterns and conventions

### Security Philosophy

Following Epic Web principles:

**Design to fail fast and early** - Validate security constraints as early as possible. Check authentication, authorization, and input validation before processing requests. Fail immediately with clear error messages rather than allowing potentially malicious data to flow through the system.

**Optimize for the debugging experience** - When security checks fail, provide clear, actionable error messages that help developers understand what went wrong. Log security events with enough context to debug issues without exposing sensitive information.

### Example - Fail fast validation:
```typescript
// ✅ Good - Validate security constraints early
export async function action({ request }: Route.ActionArgs) {
	// 1. Authenticate immediately - fail fast if not authenticated
	const userId = await requireUserId(request)
	
	// 2. Validate input early - fail fast if invalid
	const formData = await request.formData()
	const submission = await parseWithZod(formData, {
		schema: NoteSchema,
	})
	
	if (submission.status !== 'success') {
		return data({ result: submission.reply() }, { status: 400 })
	}
	
	// 3. Check permissions early - fail fast if unauthorized
	await requireUserWithPermission(request, 'create:note:own')
	
	// Only proceed if all security checks pass
	const { title, content } = submission.value
	// ... create note
}

// ❌ Avoid - Security checks scattered or delayed
export async function action({ request }: Route.ActionArgs) {
	const formData = await request.formData()
	// ... process data first
	
	// Security check at the end - too late!
	const userId = await getUserId(request)
	if (!userId) {
		// Already processed potentially malicious data
		return json({ error: 'Unauthorized' }, { status: 401 })
	}
}
```

### Example - Debugging-friendly error messages:
```typescript
// ✅ Good - Clear error messages for debugging
export async function checkHoneypot(formData: FormData) {
	try {
		// Implementation for checking honeypot
	} catch (error) {
		console.error('Honeypot check failed:', error);
		throw new Error('Honeypot validation error');
	}
}
```