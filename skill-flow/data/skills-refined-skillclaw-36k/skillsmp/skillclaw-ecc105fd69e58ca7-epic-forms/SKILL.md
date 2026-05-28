---
name: epic-forms
description: Use this skill when you need to create and validate forms in an Epic Stack application using Conform and Zod.
---

# Epic Stack: Forms

## When to use this skill

Use this skill when you need to:
- Create forms in an Epic Stack application
- Implement form validation with Zod
- Work with Conform for progressively enhanced forms
- Handle file uploads
- Implement honeypot fields for spam protection
- Handle form errors
- Work with complex forms (fieldsets, arrays)

## Patterns and conventions

### Validation Philosophy

Following Epic Web principles:

**Explicit is better than implicit** - Make validation rules clear and explicit using Zod schemas. Every validation rule should be visible in the schema, not hidden in business logic. Error messages should be specific and helpful, telling users exactly what went wrong and how to fix it.

**Design to fail fast and early** - Validate input as early as possible, ideally on the client side before submission, and always on the server side. Return clear, specific error messages immediately so users can fix issues without frustration.

### Example - Explicit validation:
```typescript
// ✅ Good - Explicit validation with clear error messages
const SignupSchema = z.object({
	email: z
		.string({ required_error: 'Email is required' })
		.email({ message: 'Please enter a valid email address' })
		.min(3, { message: 'Email must be at least 3 characters' })
		.max(100, { message: 'Email must be less than 100 characters' })
		.transform((val) => val.toLowerCase().trim()),
	password: z
		.string({ required_error: 'Password is required' })
		.min(6, { message: 'Password must be at least 6 characters' })
		.max(72, { message: 'Password must be less than 72 characters' }),
})

// ❌ Avoid - Implicit validation
const SignupSchema = z.object({
	email: z.string().email(), // No clear error messages
	password: z.string().min(6), // Generic error
})
```

### Example - Fail fast validation:
```typescript
// ✅ Good - Validate early and return specific errors immediately
export async function action({ request }: Route.ActionArgs) {
	const formData = await request.formData()

	// Validate immediately - fail fast
	const submission = await parseWithZod(formData, {
		schema: SignupSchema,
	})

	// Return errors immediately if validation fails
	if (submission.status !== 'success') {
		return data(
			{ result: submission.reply() },
			{ status: 400 }, // Clear error status
		)
	}

	// Continue processing if validation succeeds
}
```