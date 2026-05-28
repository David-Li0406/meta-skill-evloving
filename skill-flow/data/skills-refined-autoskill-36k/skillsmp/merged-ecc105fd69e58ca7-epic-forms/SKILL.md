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

### Basic setup with Conform

Epic Stack uses [Conform](https://conform.guide/) to handle forms with progressive enhancement.

**Basic setup:**
```typescript
import { getFormProps, useForm } from '@conform-to/react'
import { getZodConstraint, parseWithZod } from '@conform-to/zod'
import { z } from 'zod'
import { Form } from 'react-router'

const SignupSchema = z.object({
	email: z.string().email(),
	password: z.string().min(6),
})

export default function SignupRoute({ actionData }: Route.ComponentProps) {
	const [form, fields] = useForm({
		id: 'signup-form',
		constraint: getZodConstraint(SignupSchema),
		lastResult: actionData?.result,
		onValidate({ formData }) {
			return parseWithZod(formData, { schema: SignupSchema })
		},
		shouldRevalidate: 'onBlur',
	})

	return (
		<Form method="POST" {...getFormProps(form)}>
			{/* Form fields */}
		</Form>
	)
}
```

### Integration with Zod

Conform integrates seamlessly with Zod for validation.

**Define schema:**
```typescript
import { z } from 'zod'

const SignupSchema = z.object({
	email: z.string().email('Invalid email'),
	password: z.string().min(6, 'Password must be at least 6 characters'),
	confirmPassword: z.string(),
}).superRefine(({ confirmPassword, password }, ctx) => {
	if (confirmPassword !== password) {
		ctx.addIssue({
			path: ['confirmPassword'],
			code: 'custom',
			message: 'Passwords must match',
		})
	}
})
```

### Async validation

For validations that require querying the database:

```typescript
export async function action({ request }: Route.ActionArgs) {
	const formData = await request.formData()

	const submission = await parseWithZod(formData, {
		schema: SignupSchema.superRefine(async (data, ctx) => {
			const existingUser = await prisma.user.findUnique({
				where: { email: data.email },
				select: { id: true },
			})
			if (existingUser) {
				ctx.addIssue({
					path: ['email'],
					code: z.ZodIssueCode.custom,
					message: 'A user already exists with this email',
				})
			}
		}),
		async: true, // Important: enable async validation
	})

	if (submission.status !== 'success') {
		return data(
			{ result: submission.reply() },
			{ status: submission.status === 'error' ? 400 : 200 },
		)
	}

	// ...
}
```

### Field Components

Epic Stack provides pre-built field components:

**Basic Field:**
```typescript
import { Field, ErrorList } from '#app/components/forms.tsx'
import { getInputProps } from '@conform-to/react'

<Field
	labelProps={{
		htmlFor: fields.email.id,
		children: 'Email',
	}}
	inputProps={{
		...getInputProps(fields.email, { type: 'email' }),
		autoFocus: true,
		autoComplete: 'email',
	}}
	errors={fields.email.errors}
/>
```

### Error Handling

**Display field errors:**
```typescript
<Field
	// ... props
	errors={fields.email.errors} // Specific field errors
/>
```

**Display form errors:**
```typescript
import { ErrorList } from '#app/components/forms.tsx'

<ErrorList errors={form.errors} id={form.errorId} />
```

### Honeypot Fields

Epic Stack includes spam protection with honeypot fields.

**In the form:**
```typescript
import { HoneypotInputs } from 'remix-utils/honeypot/react'

<Form method="POST" {...getFormProps(form)}>
	<HoneypotInputs /> {/* Always include in public forms */}
	{/* Rest of fields */}
</Form>
```

### File Uploads

For forms with file uploads, use `encType="multipart/form-data"`.

**Schema for files:**
```typescript
const MAX_UPLOAD_SIZE = 1024 * 1024 * 3 // 3MB

const ImageFieldsetSchema = z.object({
	id: z.string().optional(),
	file: z
		.instanceof(File)
		.optional()
		.refine((file) => {
			return !file || file.size <= MAX_UPLOAD_SIZE
		}, 'File must be less than 3MB'),
	altText: z.string().optional(),
})

const NoteEditorSchema = z.object({
	title: z.string().min(1).max(100),
	content: z.string().min(1).max(10000),
	images: z.array(ImageFieldsetSchema).max(5).optional(),
})
```

**Form with file upload:**
```typescript
<Form
	method="POST"
	encType="multipart/form-data"
	{...getFormProps(form)}
>
	{/* Fields */}
</Form>
```

### Common examples

#### Example 1: Simple login form

```typescript
// app/routes/_auth/login.tsx
import { getFormProps, getInputProps, useForm } from '@conform-to/react'
import { getZodConstraint, parseWithZod } from '@conform-to/zod'
import { z } from 'zod'
import { Field, ErrorList } from '#app/components/forms.tsx'
import { StatusButton } from '#app/components/ui/status-button.tsx'

const LoginSchema = z.object({
	email: z.string().email(),
	password: z.string().min(1),
})

export default function LoginRoute({ actionData }: Route.ComponentProps) {
	const isPending = useIsPending()

	const [form, fields] = useForm({
		id: 'login-form',
		constraint: getZodConstraint(LoginSchema),
		lastResult: actionData?.result,
		onValidate({ formData }) {
			return parseWithZod(formData, { schema: LoginSchema })
		},
		shouldRevalidate: 'onBlur',
	})

	return (
		<Form method="POST" {...getFormProps(form)}>
			<Field
				labelProps={{ htmlFor: fields.email.id, children: 'Email' }}
				inputProps={{
					...getInputProps(fields.email, { type: 'email' }),
					autoFocus: true,
					autoComplete: 'email',
				}}
				errors={fields.email.errors}
			/>
			<Field
				labelProps={{ htmlFor: fields.password.id, children: 'Password' }}
				inputProps={{
					...getInputProps(fields.password, { type: 'password' }),
					autoComplete: 'current-password',
				}}
				errors={fields.password.errors}
			/>
			<ErrorList errors={form.errors} id={form.errorId} />
			<StatusButton
				status={isPending ? 'pending' : (form.status ?? 'idle')}
				type="submit"
			>
				Login
			</StatusButton>
		</Form>
	)
}
```

### Common mistakes to avoid

- ❌ **Implicit validation**: Always use explicit Zod schemas with clear error messages, not hidden validation logic.
- ❌ **Delayed validation**: Validate input immediately and fail fast - don't wait until the end of the function.
- ❌ **Generic error messages**: Use specific, helpful error messages that tell users exactly what's wrong.
- ❌ **Forgetting `async: true` in async validation**: Always include `async: true` when using `superRefine` with async.
- ❌ **Not including `HoneypotInputs` in public forms**: Always include honeypot in forms accessible without authentication.
- ❌ **Forgetting `encType="multipart/form-data"`**: Required for file uploads.
- ❌ **Not validating file sizes**: Always validate size in the schema.
- ❌ **Not using `getZodConstraint`**: Required for native HTML5 validation.
- ❌ **Forgetting `lastResult` in `useForm`**: Required to display server errors.
- ❌ **Not using `shouldRevalidate: 'onBlur'`**: Improves UX by validating on field blur.
- ❌ **Not using pre-built field components**: `Field`, `TextareaField`, etc. already handle accessibility and errors.

## References

- [Conform Documentation](https://conform.guide/)
- [Zod Documentation](https://zod.dev/)
- [Epic Web Principles](https://www.epicweb.dev/principles)
- `app/components/forms.tsx` - Field components
- `app/routes/_auth/signup.tsx` - Complete signup example
- `app/routes/_auth/onboarding/index.tsx` - Complex form example
- `app/routes/users/$username/notes/+shared/note-editor.tsx` - File uploads example
- `app/utils/user-validation.ts` - Reusable schemas
- `docs/decisions/033-honeypot.md` - Honeypot documentation