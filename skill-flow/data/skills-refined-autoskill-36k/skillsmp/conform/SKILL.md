---
name: conform
description: Progressive enhancement form validation with Conform and Zod for Remix applications - type-safe forms that work without JavaScript
---

# Conform Forms

This skill covers Conform v1+ patterns for building accessible, progressively enhanced forms in Remix with Zod validation.

## Core Concepts

**Conform Benefits:**
- Progressive enhancement (works without JS)
- Type-safe with Zod integration
- Accessible by default (ARIA attributes)
- Controlled and uncontrolled modes
- File uploads
- Multi-step forms
- Field arrays (dynamic lists)

**Key Terms:**
- **Form**: Top-level form configuration
- **Field**: Individual form input
- **Constraint**: HTML5 validation attributes
- **Submission**: Form submission result
- **Field Array**: Dynamic list of fields

## Installation

```bash
npm install @conform-to/react @conform-to/zod zod
```

## Basic Form

### Simple Form with Validation

```typescript
// app/routes/login.tsx
import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { Form, useActionData } from "@remix-run/react";
import { json, redirect } from "@remix-run/node";
import { z } from "zod";

// Define schema
const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  remember: z.boolean().optional(),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  // Parse with Zod
  const submission = parseWithZod(formData, { schema: loginSchema });
  
  // Return errors if validation fails
  if (submission.status !== "success") {
    return json({ submission: submission.reply() });
  }
  
  // Process valid data
  const { email, password, remember } = submission.value;
  await login(email, password, remember);
  
  return redirect("/dashboard");
}

export default function Login() {
  const lastResult = useActionData<typeof action>();
  
  const [form, fields] = useForm({
    lastResult: lastResult?.submission,
    onValidate: ({ formData }) => {
      return parseWithZod(formData, { schema: loginSchema });
    },
    shouldValidate: "onBlur",
    shouldRevalidate: "onInput",
  });
  
  return (
    <Form method="post" {...getFormProps(form)}>
      <div>
        <label htmlFor={fields.email.id}>Email</label>
        <input
          {...getInputProps(fields.email, { type: "email" })}
          key={fields.email.key}
        />
        <div>{fields.email.errors}</div>
      </div>
      
      <div>
        <label htmlFor={fields.password.id}>Password</label>
        <input
          {...getInputProps(fields.password, { type: "password" })}
          key={fields.password.key}
        />
        <div>{fields.password.errors}</div>
      </div>
      
      <div>
        <label>
          <input
            {...getInputProps(fields.remember, { type: "checkbox" })}
            key={fields.remember.key}
          />
          Remember me
        </label>
      </div>
      
      <button type="submit">Login</button>
    </Form>
  );
}
```

## Form Configuration

### useForm Hook Options

```typescript
const [form, fields] = useForm({
  // ID for the form (required for nested forms)
  id: "login-form",
  
  // Last submission result from action
  lastResult: actionData?.submission,
  
  // Default values
  defaultValue: {
    email: "user@example.com",
    remember: true,
  },
  
  // Client-side validation
  onValidate: ({ formData }) => {
    return parseWithZod(formData, { schema: loginSchema });
  },
  
  // When to validate
  shouldValidate: "onBlur", // or "onInput" | "onSubmit"
  shouldRevalidate: "onInput", // after first validation
  
  // Callbacks
  onSubmit: (event, context) => {
    // Optional: custom submit handling
    // event.preventDefault() if you want to prevent submission
  },
  
  // Constraint validation (HTML5)
  constraint: getZodConstraint(loginSchema),
});
```

## Field Types

### Text Input

```typescript
const schema = z.object({
  name: z.string().min(1, "Name is required"),
  bio: z.string().max(500, "Bio is too long").optional(),
});

// In component
<div>
  <label htmlFor={fields.name.id}>Name</label>
  <input
    {...getInputProps(fields.name, { type: "text" })}
    key={fields.name.key}
  />
  <div id={fields.name.errorId}>{fields.name.errors}</div>
</div>

<div>
  <label htmlFor={fields.bio.id}>Bio</label>
  <textarea
    {...getTextareaProps(fields.bio)}
    key={fields.bio.key}
    rows={4}
  />
  <div>{fields.bio.errors}</div>
</div>
```

### Number Input

```typescript
const schema = z.object({
  age: z.number().min(18, "Must be 18 or older"),
  price: z.number().positive("Price must be positive"),
});

<input
  {...getInputProps(fields.age, { type: "number" })}
  key={fields.age.key}
  min={18}
  max={120}
/>
```

### Select/Dropdown

```typescript
const schema = z.object({
  role: z.enum(["STUDENT", "TEACHER", "ADMIN"]),
  country: z.string().min(1, "Country is required"),
});

<select
  {...getSelectProps(fields.role)}
  key={fields.role.key}
>
  <option value="">Select role</option>
  <option value="STUDENT">Student</option>
  <option value="TEACHER">Teacher</option>
  <option value="ADMIN">Admin</option>
</select>

<div>{fields.role.errors}</div>
```

### Checkbox

```typescript
const schema = z.object({
  terms: z.literal(true, {
    errorMap: () => ({ message: "You must accept terms" }),
  }),
  newsletter: z.boolean().optional(),
});

<label>
  <input
    {...getInputProps(fields.terms, { type: "checkbox" })}
    key={fields.terms.key}
  />
  I accept the terms and conditions
</label>
<div>{fields.terms.errors}</div>
```

### Radio Buttons

```typescript
const schema = z.object({
  plan: z.enum(["free", "pro", "enterprise"]),
});

<fieldset>
  <legend>Choose a plan</legend>
  
  <label>
    <input
      {...getInputProps(fields.plan, { type: "radio" })}
      value="free"
    />
    Free
  </label>
  
  <label>
    <input
      {...getInputProps(fields.plan, { type: "radio" })}
      value="pro"
    />
    Pro
  </label>
  
  <label>
    <input
      {...getInputProps(fields.plan, { type: "radio" })}
      value="enterprise"
    />
    Enterprise
  </label>
  
  <div>{fields.plan.errors}</div>
</fieldset>
```

### Date Input

```typescript
const schema = z.object({
  birthDate: z.string().refine(
    (date) => {
      const parsed = new Date(date);
      return !isNaN(parsed.getTime());
    },
    { message: "Invalid date" }
  ),
  scheduledDate: z.string().refine(
    (date) => new Date(date) > new Date(),
    { message: "Date must be in the future" }
  ),
});

<input
  {...getInputProps(fields.birthDate, { type: "date" })}
  key={fields.birthDate.key}
  max={new Date().toISOString().split("T")[0]} // Today or earlier
/>

<input
  {...getInputProps(fields.scheduledDate, { type: "datetime-local" })}
  key={fields.scheduledDate.key}
/>
```

## File Uploads

### Single File Upload

```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

const schema = z.object({
  avatar: z
    .instanceof(File)
    .refine(
      (file) => file.size <= MAX_FILE_SIZE,
      "File size must be less than 5MB"
    )
    .refine(
      (file) => ["image/jpeg", "image/png", "image/webp"].includes(file.type),
      "Only JPEG, PNG, and WebP images are allowed"
    ),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  const submission = parseWithZod(formData, {
    schema: schema.transform(async (data) => {
      // Upload to S3
      const url = await uploadToS3(data.avatar);
      return { avatarUrl: url };
    }),
    async: true, // Required for async transforms
  });
  
  if (submission.status !== "success") {
    return json({ submission: submission.reply() });
  }
  
  // Use submission.value.avatarUrl
  await updateUser(userId, { avatarUrl: submission.value.avatarUrl });
  
  return redirect("/profile");
}

// In component
<div>
  <label htmlFor={fields.avatar.id}>Avatar</label>
  <input
    {...getInputProps(fields.avatar, { type: "file" })}
    key={fields.avatar.key}
    accept="image/jpeg,image/png,image/webp"
  />
  <div>{fields.avatar.errors}</div>
</div>
```

### Multiple File Upload

```typescript
const schema = z.object({
  photos: z
    .array(z.instanceof(File))
    .min(1, "At least one photo is required")
    .max(5, "Maximum 5 photos allowed")
    .refine(
      (files) => files.every((file) => file.size <= MAX_FILE_SIZE),
      "Each file must be less than 5MB"
    ),
});

<input
  {...getInputProps(fields.photos, { type: "file" })}
  key={fields.photos.key}
  accept="image/*"
  multiple
/>
```

## Nested Objects

```typescript
const schema = z.object({
  name: z.string().min(1),
  address: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
    zipCode: z.string().regex(/^\d{5}$/, "Invalid ZIP code"),
  }),
});

export default function AddressForm() {
  const [form, fields] = useForm({
    onValidate: ({ formData }) => parseWithZod(formData, { schema }),
  });
  
  const address = fields.address.getFieldset();
  
  return (
    <Form method="post" {...getFormProps(form)}>
      <input {...getInputProps(fields.name, { type: "text" })} />
      
      <fieldset>
        <legend>Address</legend>
        
        <input
          {...getInputProps(address.street, { type: "text" })}
          placeholder="Street"
        />
        <div>{address.street.errors}</div>
        
        <input
          {...getInputProps(address.city, { type: "text" })}
          placeholder="City"
        />
        <div>{address.city.errors}</div>
        
        <input
          {...getInputProps(address.zipCode, { type: "text" })}
          placeholder="ZIP Code"
        />
        <div>{address.zipCode.errors}</div>
      </fieldset>
      
      <button type="submit">Submit</button>
    </Form>
  );
}
```

## Field Arrays (Dynamic Lists)

```typescript
import { useFieldList } from "@conform-to/react";

const schema = z.object({
  name: z.string().min(1),
  emails: z
    .array(
      z.object({
        address: z.string().email(),
        primary: z.boolean().optional(),
      })
    )
    .min(1, "At least one email is required"),
});

export default function EmailsForm() {
  const [form, fields] = useForm({
    onValidate: ({ formData }) => parseWithZod(formData, { schema }),
    defaultValue: {
      emails: [{ address: "", primary: true }],
    },
  });
  
  const emails = useFieldList(form.ref, fields.emails);
  
  return (
    <Form method="post" {...getFormProps(form)}>
      <input {...getInputProps(fields.name, { type: "text" })} />
      
      <fieldset>
        <legend>Email Addresses</legend>
        
        {emails.map((email, index) => {
          const emailFields = email.getFieldset();
          
          return (
            <div key={email.key}>
              <input
                {...getInputProps(emailFields.address, { type: "email" })}
                placeholder="Email address"
              />
              <div>{emailFields.address.errors}</div>
              
              <label>
                <input
                  {...getInputProps(emailFields.primary, { type: "checkbox" })}
                />
                Primary
              </label>
              
              <button
                {...form.remove.getButtonProps({
                  name: fields.emails.name,
                  index,
                })}
              >
                Remove
              </button>
            </div>
          );
        })}
        
        <button
          {...form.insert.getButtonProps({
            name: fields.emails.name,
          })}
        >
          Add Email
        </button>
      </fieldset>
      
      <button type="submit">Submit</button>
    </Form>
  );
}
```

## Multi-Step Forms

```typescript
const step1Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const step2Schema = z.object({
  name: z.string().min(1),
  bio: z.string().optional(),
});

const fullSchema = step1Schema.merge(step2Schema);

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const step = formData.get("_step");
  
  if (step === "1") {
    // Validate step 1
    const submission = parseWithZod(formData, { schema: step1Schema });
    
    if (submission.status !== "success") {
      return json({ submission: submission.reply(), step: 1 });
    }
    
    // Move to step 2
    return json({ submission: submission.reply(), step: 2 });
  }
  
  // Final submission - validate everything
  const submission = parseWithZod(formData, { schema: fullSchema });
  
  if (submission.status !== "success") {
    return json({ submission: submission.reply(), step: 2 });
  }
  
  // Create account
  await createAccount(submission.value);
  return redirect("/dashboard");
}

export default function Signup() {
  const actionData = useActionData<typeof action>();
  const [currentStep, setCurrentStep] = useState(actionData?.step ?? 1);
  
  const [form, fields] = useForm({
    lastResult: actionData?.submission,
    onValidate: ({ formData }) => {
      const schema = currentStep === 1 ? step1Schema : fullSchema;
      return parseWithZod(formData, { schema });
    },
  });
  
  return (
    <Form method="post" {...getFormProps(form)}>
      <input type="hidden" name="_step" value={currentStep} />
      
      {currentStep === 1 && (
        <>
          <h2>Step 1: Account Details</h2>
          <input {...getInputProps(fields.email, { type: "email" })} />
          <div>{fields.email.errors}</div>
          
          <input {...getInputProps(fields.password, { type: "password" })} />
          <div>{fields.password.errors}</div>
          
          <button type="button" onClick={() => setCurrentStep(2)}>
            Next
          </button>
        </>
      )}
      
      {currentStep === 2 && (
        <>
          <h2>Step 2: Profile</h2>
          <input {...getInputProps(fields.name, { type: "text" })} />
          <div>{fields.name.errors}</div>
          
          <textarea {...getTextareaProps(fields.bio)} />
          <div>{fields.bio.errors}</div>
          
          <button type="button" onClick={() => setCurrentStep(1)}>
            Back
          </button>
          <button type="submit">Create Account</button>
        </>
      )}
    </Form>
  );
}
```

## Advanced Patterns

### Dependent Fields

```typescript
const schema = z
  .object({
    hasShippingAddress: z.boolean(),
    shippingAddress: z.object({
      street: z.string(),
      city: z.string(),
    }).optional(),
  })
  .refine(
    (data) => {
      if (data.hasShippingAddress) {
        return data.shippingAddress?.street && data.shippingAddress?.city;
      }
      return true;
    },
    {
      message: "Shipping address is required",
      path: ["shippingAddress"],
    }
  );

export default function ShippingForm() {
  const [form, fields] = useForm({
    onValidate: ({ formData }) => parseWithZod(formData, { schema }),
  });
  
  const hasShipping = fields.hasShippingAddress.value === "on";
  const shippingFields = fields.shippingAddress.getFieldset();
  
  return (
    <Form method="post" {...getFormProps(form)}>
      <label>
        <input
          {...getInputProps(fields.hasShippingAddress, { type: "checkbox" })}
        />
        Use different shipping address
      </label>
      
      {hasShipping && (
        <fieldset>
          <input {...getInputProps(shippingFields.street, { type: "text" })} />
          <input {...getInputProps(shippingFields.city, { type: "text" })} />
        </fieldset>
      )}
      
      <button type="submit">Submit</button>
    </Form>
  );
}
```

### Custom Validation Messages

```typescript
const schema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain an uppercase letter")
    .regex(/[a-z]/, "Password must contain a lowercase letter")
    .regex(/[0-9]/, "Password must contain a number"),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  }
);
```

### Server-Side Only Validation

```typescript
const clientSchema = z.object({
  email: z.string().email(),
  username: z.string().min(3),
});

const serverSchema = clientSchema.extend({
  email: z.string().email().refine(
    async (email) => {
      const existing = await db.user.findUnique({ where: { email } });
      return !existing;
    },
    { message: "Email already registered" }
  ),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  // Server-side validation with async checks
  const submission = await parseWithZod(formData, {
    schema: serverSchema,
    async: true,
  });
  
  if (submission.status !== "success") {
    return json({ submission: submission.reply() });
  }
  
  // Create user
  await createUser(submission.value);
  return redirect("/login");
}

export default function Signup() {
  const actionData = useActionData<typeof action>();
  
  const [form, fields] = useForm({
    lastResult: actionData?.submission,
    // Client-side validation (no async checks)
    onValidate: ({ formData }) => parseWithZod(formData, { schema: clientSchema }),
  });
  
  return <Form method="post" {...getFormProps(form)}>...</Form>;
}
```

### Field-Level Intent (Blur/Change Events)

```typescript
import { useInputControl } from "@conform-to/react";

export default function UsernameField({ field }) {
  const control = useInputControl(field);
  const [availability, setAvailability] = useState<"available" | "taken" | null>(null);
  
  const checkAvailability = async (username: string) => {
    const response = await fetch(`/api/check-username?username=${username}`);
    const data = await response.json();
    setAvailability(data.available ? "available" : "taken");
  };
  
  return (
    <div>
      <input
        {...getInputProps(field, { type: "text" })}
        onBlur={() => {
          if (control.value) {
            checkAvailability(control.value);
          }
        }}
      />
      {availability === "available" && <span>✓ Available</span>}
      {availability === "taken" && <span>✗ Already taken</span>}
      <div>{field.errors}</div>
    </div>
  );
}
```

## Accessibility

Conform automatically generates accessible forms:

```typescript
// Generated HTML includes:
<form id="login-form" aria-invalid={form.errors ? true : undefined}>
  <label htmlFor="email-input">Email</label>
  <input
    id="email-input"
    name="email"
    type="email"
    aria-invalid={fields.email.errors ? true : undefined}
    aria-describedby={fields.email.errors ? "email-error" : undefined}
  />
  <div id="email-error" aria-live="polite">
    {fields.email.errors}
  </div>
</form>
```

### Manual Accessibility

```typescript
<div>
  <label htmlFor={fields.email.id}>
    Email
    <span aria-label="required">*</span>
  </label>
  <input
    {...getInputProps(fields.email, { type: "email" })}
    aria-required="true"
    aria-describedby={`${fields.email.errorId} email-hint`}
  />
  <div id="email-hint">We'll never share your email</div>
  <div id={fields.email.errorId} aria-live="polite">
    {fields.email.errors}
  </div>
</div>
```

## Testing

```typescript
import { parseWithZod } from "@conform-to/zod";
import { describe, test, expect } from "vitest";

describe("Login form", () => {
  test("validates email format", () => {
    const formData = new FormData();
    formData.set("email", "invalid");
    formData.set("password", "password123");
    
    const submission = parseWithZod(formData, { schema: loginSchema });
    
    expect(submission.status).toBe("error");
    expect(submission.reply().error?.email).toBeDefined();
  });
  
  test("accepts valid data", () => {
    const formData = new FormData();
    formData.set("email", "user@example.com");
    formData.set("password", "password123");
    
    const submission = parseWithZod(formData, { schema: loginSchema });
    
    expect(submission.status).toBe("success");
    expect(submission.value).toEqual({
      email: "user@example.com",
      password: "password123",
    });
  });
});
```

## Best Practices

1. **Always use key prop**: Prevents React state issues
2. **Use getInputProps helpers**: Ensures proper attributes
3. **Validate on blur first**: Better UX than validating on every keystroke
4. **Return submission.reply()**: Preserves form state on errors
5. **Use Zod constraints**: Enables HTML5 validation
6. **Handle file uploads properly**: Use async transforms
7. **Test validation logic**: Unit test your schemas
8. **Accessibility first**: Use semantic HTML and ARIA when needed
9. **Progressive enhancement**: Forms work without JavaScript
10. **Type safety**: Let TypeScript infer types from schemas

## Common Gotchas

1. **Missing key prop**: Causes hydration issues
2. **Not using reply()**: Loses form state on validation errors
3. **Async validation on client**: Use server-only schemas
4. **Large file uploads**: Need streaming for files >4.5MB
5. **Field array re-renders**: Use proper keys
6. **Nested object syntax**: Use getFieldset() for nested objects
7. **File validation**: Must use instanceof File, not z.string()
8. **Multi-step validation**: Validate current step, not full schema
9. **Default values**: Use defaultValue in useForm, not in schema
10. **Form reset**: Use form.reset() or navigate to clear state

## Resources

- [Conform Documentation](https://conform.guide/)
- [Conform GitHub](https://github.com/edmundhung/conform)
- [Zod Documentation](https://zod.dev)
- [Remix Forms Guide](https://remix.run/docs/en/main/guides/form-validation)
