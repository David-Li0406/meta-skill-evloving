# Form Validation Reference

## Validation Timing

```tsx
validators: {
  onSubmit: schema,    // Validate on submit
  onBlur: schema,      // Validate on blur
  onChange: schema,    // Validate on change
}

// Field-level async
<form.Field
  name="email"
  validators={{
    onChange: z.email(),
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const exists = await checkEmail(value);
      return !exists ? undefined : 'Email taken';
    },
  }}
/>
```

## Zod Schema Patterns

```tsx
// Basic
const schema = z.object({
  username: z.string().min(3).max(20),
  email: z.email(),
});

// Array
const schema = z.object({
  emails: z
    .array(z.object({ address: z.email() }))
    .min(1)
    .max(5),
});

// Enum
const schema = z.object({
  plan: z.enum(['basic', 'pro', 'enterprise']),
});

// Password confirmation
const schema = z
  .object({
    password: z.string().min(8),
    confirm: z.string(),
  })
  .refine((d) => d.password === d.confirm, {
    message: 'Passwords must match',
    path: ['confirm'],
  });
```

## Linked Fields

Use `onChangeListenTo` to re-validate a field when another field changes:

```tsx
<form.Field
  name="password"
  children={(field) => (
    <TextField
      label="Password"
      type="password"
      value={field.state.value}
      onChange={(value) => field.handleChange(value)}
    />
  )}
/>

<form.Field
  name="confirmPassword"
  validators={{
    onChangeListenTo: ['password'],
    onChange: ({ value, fieldApi }) => {
      if (value !== fieldApi.form.getFieldValue('password')) {
        return 'Passwords do not match';
      }
      return undefined;
    },
  }}
  children={(field) => (
    <TextField
      label="Confirm Password"
      type="password"
      value={field.state.value}
      onChange={(value) => field.handleChange(value)}
      isInvalid={field.state.meta.isTouched && !field.state.meta.isValid}
      errorMessage={field.state.meta.errors.join(', ')}
    />
  )}
/>
```

## Cross-Field Validation

Form-level validators can return targeted field errors:

```tsx
const form = useForm({
  defaultValues: { password: '', confirmPassword: '' },
  validators: {
    onSubmit: ({ value }) => {
      if (value.password !== value.confirmPassword) {
        return {
          form: 'Passwords do not match',
          fields: { confirmPassword: 'Must match password' },
        };
      }
      return undefined;
    },
  },
});
```

## Async Field Validation

### Debounce Configuration

Set a default debounce for all async validators on a field, then override per-validator:

```tsx
<form.Field
  name="username"
  asyncDebounceMs={500} // Default for all async validators
  validators={{
    onChange: z.string().min(3),
    onChangeAsyncDebounceMs: 1000, // Override for onChangeAsync only
    onChangeAsync: async ({ value }) => {
      const available = await checkUsername(value);
      return available ? undefined : 'Username taken';
    },
    onBlurAsync: async ({ value }) => {
      // Uses field's asyncDebounceMs (500ms)
      return validateWithServer(value);
    },
  }}
/>
```

### Debounced Server Validation

```tsx
const checkUsername = createServerFn({ method: 'GET' })
  .inputValidator(z.object({ username: z.string() }))
  .handler(async ({ data }) => {
    const existing = await db.query.users.findFirst({
      where: eq(users.username, data.username),
    });
    return { available: !existing };
  });

<form.Field
  name="username"
  validators={{
    onChange: z
      .string()
      .min(3)
      .max(20)
      .regex(/^[a-z0-9_]+$/),
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const result = await checkUsername({ data: { username: value } });
      return result.available ? undefined : 'Username already taken';
    },
  }}
  children={(field) => (
    <div className="relative">
      <TextField
        label="Username"
        value={field.state.value}
        onChange={(value) => field.handleChange(value)}
        isInvalid={field.state.meta.isTouched && !field.state.meta.isValid}
        errorMessage={field.state.meta.errors.join(', ')}
      />
      {field.state.meta.isValidating && (
        <Spinner className="absolute right-3 top-3 size-4" />
      )}
    </div>
  )}
/>;
```

## Standard Schema Support

TanStack Form natively supports any library following the Standard Schema spec:

| Library | Minimum Version |
| ------- | --------------- |
| Zod     | v3.24.0+        |
| Valibot | v1.0.0+         |
| ArkType | v2.1.20+        |
| Yup     | v1.7.0+         |

No adapter needed - pass schemas directly to validators.

## Notes

- Always add server-side validation too
- Use `form.reset()` to reset to `defaultValues`
- Validation returns errors, not transformed values - use `onSubmit` for transforms
