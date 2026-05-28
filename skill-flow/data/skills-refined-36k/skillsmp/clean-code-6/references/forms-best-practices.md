# Forms Best Practices (TanStack Form + Zod)

## Core Principles

- **Controlled Components**: Manage form inputs with React state
- **Form States**: Handle loading, success, and error states
- **Validation**: Client-side for UX, server-side for security
- **Accessibility**: Labels, error messages, keyboard navigation

---

## TanStack Form + Zod Setup

Use TanStack Form with Zod validation and Shadcn/ui components.

### Form Composition Helper

Always use `useForm` and `Form` from your form helper utility to create forms. This provides pre-bound UI components accessible via `field.*` in the render prop pattern.

```typescript
// lib/form/tanstack-form.ts
import { useForm as useTanStackForm } from "@tanstack/react-form";
import { zodValidator } from "@tanstack/zod-form-adapter";

export function useForm<T>(options: FormOptions<T>) {
  return useTanStackForm({
    ...options,
    validatorAdapter: zodValidator(),
  });
}
```

### Basic Form Example

```typescript
import { z } from "zod";
import { useForm, Form } from "~/lib/form/tanstack-form";

const schema = z.object({
  email: z.string().email("Invalid email"),
  name: z.string().min(2, "Name too short"),
});

function ContactForm() {
  const form = useForm({
    defaultValues: { email: "", name: "" },
    validators: { onChange: schema },
    onSubmit: async ({ value }) => {
      await submitForm(value);
    },
  });

  return (
    <Form form={form}>
      <form.Field name="email">
        {(field) => (
          <div>
            <field.Label>Email</field.Label>
            <field.Input type="email" />
            <field.Message />
          </div>
        )}
      </form.Field>

      <form.Field name="name">
        {(field) => (
          <div>
            <field.Label>Name</field.Label>
            <field.Input />
            <field.Message />
          </div>
        )}
      </form.Field>

      <button type="submit">Submit</button>
    </Form>
  );
}
```

---

## Accessibility

### Label Association

Labels must always be associated with inputs:

**Web:**

```tsx
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

**React Native (Expo):**

```tsx
<Text nativeID="email-label">Email</Text>
<TextInput
  nativeID="email"
  aria-labelledby="email-label"
  accessibilityLabel="Email input"
/>
```

### Submit Button

- **Always enabled**: Keep submit buttons enabled
- **Validate on submit**: Display inline error feedback
- **Reasoning**: Disabled buttons are harder to discover for screen reader users

### Error Messages

- Use `role="alert"` for critical errors
- Use `aria-live="polite"` for field validation messages

```tsx
{
  error && (
    <p role="alert" className="text-red-500">
      {error.message}
    </p>
  );
}
```

---

## Validation Patterns

### Zod Schema Examples

```typescript
const userSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain uppercase")
    .regex(/[0-9]/, "Must contain number"),
  age: z.number().min(18, "Must be 18 or older").optional(),
  website: z.string().url("Invalid URL").optional().or(z.literal("")),
});

// Transform & refine
const registrationSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  });
```

### Server-Side Validation

Always validate on the server, even with client-side validation:

```typescript
"use server";

import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export async function submitForm(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get("email"),
    name: formData.get("name"),
  });

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  // Process valid data
  await saveUser(result.data);
}
```

---

## Form States

### Loading State

```typescript
function Form() {
  const form = useForm({
    onSubmit: async ({ value }) => {
      // form.state.isSubmitting is true during this
      await saveData(value);
    },
  });

  return (
    <button type="submit" disabled={form.state.isSubmitting}>
      {form.state.isSubmitting ? "Saving..." : "Save"}
    </button>
  );
}
```

### Success & Error States

```typescript
function Form() {
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const form = useForm({
    onSubmit: async ({ value }) => {
      try {
        await saveData(value);
        setStatus("success");
      } catch {
        setStatus("error");
      }
    },
  });

  return (
    <>
      {status === "success" && <Alert>Saved successfully!</Alert>}
      {status === "error" && <Alert variant="error">Failed to save</Alert>}
      {/* form fields */}
    </>
  );
}
```

---

## React 19 Server Actions

### With useActionState

```typescript
"use client";

import { useActionState } from "react";
import { submitContact } from "./actions";

function ContactForm() {
  const [state, action, isPending] = useActionState(submitContact, null);

  return (
    <form action={action}>
      <input name="email" type="email" required />
      {state?.errors?.email && <p>{state.errors.email}</p>}

      <input name="message" required />
      {state?.errors?.message && <p>{state.errors.message}</p>}

      <button disabled={isPending}>
        {isPending ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
```

---

## Anti-Patterns

| Pattern                | Problem                | Solution                    |
| ---------------------- | ---------------------- | --------------------------- |
| Disabled submit button | A11y issues            | Always enabled + validate   |
| No label association   | Screen readers broken  | htmlFor/id or nativeID      |
| Client-only validation | Security vulnerability | Always validate server-side |
| Placeholder as label   | Disappears on focus    | Use visible labels          |
| No error states        | User confusion         | Show clear error messages   |
| Manual form state      | Boilerplate            | Use TanStack Form           |
| No loading indicator   | User uncertainty       | Show pending state          |
