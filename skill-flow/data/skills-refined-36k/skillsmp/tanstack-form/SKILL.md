---
name: tanstack-form
description: Create forms with TanStack Form and React Aria Components. Use when building forms, implementing validation, handling form submissions, or creating reusable form fields.
---

# TanStack Form

## Quick Start

```sh
pnpm add @tanstack/react-form
```

## Two Patterns

| Pattern        | Use Case        | API                                |
| -------------- | --------------- | ---------------------------------- |
| **Basic**      | One-off forms   | `useForm` + `form.Field`           |
| **Composable** | Reusable fields | `createFormHook` + `form.AppField` |

## Basic Pattern

```tsx
import { useForm } from '@tanstack/react-form';
import { z } from 'zod';
import { TextField, Button } from '@oakoss/ui';

const schema = z.object({
  email: z.email(),
  name: z.string().min(1),
});

function MyForm() {
  const form = useForm({
    defaultValues: { email: '', name: '' },
    validators: { onSubmit: schema },
    onSubmit: async ({ value }) => console.log(value),
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      <form.Field
        name="email"
        children={(field) => {
          const isInvalid =
            field.state.meta.isTouched && !field.state.meta.isValid;
          return (
            <TextField
              label="Email"
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(value) => field.handleChange(value)}
              isInvalid={isInvalid}
              errorMessage={
                isInvalid ? field.state.meta.errors.join(', ') : undefined
              }
            />
          );
        }}
      />
      <Button type="submit">Submit</Button>
    </form>
  );
}
```

## Composable Pattern (Recommended)

### 1. Create contexts

```tsx
// apps/web/src/hooks/form-context.ts
import { createFormHookContexts } from '@tanstack/react-form';
export const { fieldContext, formContext, useFieldContext, useFormContext } =
  createFormHookContexts();
```

### 2. Create field component

```tsx
// apps/web/src/components/form/text-field.tsx
import { TextField as AriaTextField } from '@oakoss/ui';
import { useFieldContext } from '@/hooks/form-context';
import { useStore } from '@tanstack/react-form';

export function FormTextField({ label }: { label: string }) {
  const field = useFieldContext<string>();
  const errors = useStore(field.store, (s) => s.meta.errors);
  const isInvalid = field.state.meta.isTouched && errors.length > 0;

  return (
    <AriaTextField
      label={label}
      value={field.state.value}
      onBlur={field.handleBlur}
      onChange={(value) => field.handleChange(value)}
      isInvalid={isInvalid}
      errorMessage={isInvalid ? errors.join(', ') : undefined}
    />
  );
}
```

### 3. Create form hook

```tsx
// apps/web/src/hooks/use-app-form.ts
import { createFormHook } from '@tanstack/react-form';
import { fieldContext, formContext } from './form-context';
import {
  FormTextField,
  FormSelectField,
  SubmitButton,
} from '@/components/form';

export const { useAppForm } = createFormHook({
  fieldComponents: { TextField: FormTextField, SelectField: FormSelectField },
  formComponents: { SubmitButton },
  fieldContext,
  formContext,
});
```

### 4. Use in forms

```tsx
const form = useAppForm({ defaultValues: { name: '' }, onSubmit });

<form.AppField name="name" children={(f) => <f.TextField label="Name" />} />
<form.AppForm><form.SubmitButton label="Submit" /></form.AppForm>
```

## Validation

```tsx
// Form-level with Zod (or Valibot, ArkType, Yup)
validators: {
  onSubmit: schema;
}

// Field-level
<form.Field
  name="email"
  validators={{
    onChange: z.email(),
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => checkAvailable(value),
  }}
/>;

// Linked fields - re-validate when another field changes
<form.Field
  name="confirmPassword"
  validators={{
    onChangeListenTo: ['password'],
    onChange: ({ value, fieldApi }) =>
      value !== fieldApi.form.getFieldValue('password')
        ? 'Passwords must match'
        : undefined,
  }}
/>;
```

## Form State

```tsx
form.state.values; // Current values
form.state.isSubmitting;
form.state.isValid;
form.state.isDirty;
form.reset(); // Reset to defaults
form.handleSubmit(); // Submit programmatically
```

## Common Mistakes

| Mistake                             | Correct Pattern                                     |
| ----------------------------------- | --------------------------------------------------- |
| Using `e.target.value` directly     | Use `field.handleChange(e.target.value)`            |
| Missing `onBlur={field.handleBlur}` | Always add for validation timing                    |
| Not showing validation errors       | Check `field.state.meta.isTouched && errors.length` |
| Missing `id` on inputs              | Use `id={field.name}` for label association         |
| Missing `aria-invalid`              | Add for accessibility                               |
| Using interface keyword             | Use `type` for form value types                     |
| Using deprecated Zod syntax         | Use `z.email()` not `z.string().email()`            |
| Server validation only              | Always validate client-side first                   |

## Delegation

- **Form pattern discovery**: For finding existing form implementations, use `Explore` agent
- **Code review**: After creating forms, delegate to `code-reviewer` agent

## Topic References

- [Field Components](field-components.md) - Input types, array fields, field listeners, composable fields
- [Validation](validation.md) - Timing, linked fields, Standard Schema, async validation
- [Server Integration](server-integration.md) - Mutations, SSR, optimistic updates
- [Advanced Patterns](advanced-patterns.md) - Multi-step wizard, file upload, accessibility
