# React Hook Form Integration

Comprehensive guide for integrating React Hook Form with Next.js Server Actions.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Form Component Patterns](#form-component-patterns)
3. [Error Handling](#error-handling)
4. [Field Types](#field-types)
5. [Dynamic Fields (useFieldArray)](#dynamic-fields-usefieldarray)
6. [Multi-Step Forms](#multi-step-forms)
7. [Form Reset and Default Values](#form-reset-and-default-values)
8. [Integration with UI Libraries](#integration-with-ui-libraries)

---

## Basic Setup

### Dependencies

```bash
npm install react-hook-form @hookform/resolvers zod
```

### Basic Form Structure

```typescript
// features/users/components/user-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useTransition } from "react";
import { z } from "zod";

// 1. Define schema
const userSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address")
});

// 2. Infer type from schema
type UserFormData = z.infer<typeof userSchema>;

// 3. Create form component
export function UserForm() {
  const [isPending, startTransition] = useTransition();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
    reset
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      name: "",
      email: ""
    }
  });

  async function onSubmit(data: UserFormData) {
    startTransition(async () => {
      const result = await createUser(data);

      if (!result.success) {
        // Handle server errors
        setError("root", { message: result.error });
      } else {
        reset();
      }
    });
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          {...register("name")}
          disabled={isPending}
        />
        {errors.name && <span className="error">{errors.name.message}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register("email")}
          disabled={isPending}
        />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      {errors.root && <p className="error">{errors.root.message}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

---

## Form Component Patterns

### Pattern 1: Action Passed as Prop

Preferred pattern - allows server component to bind data to action.

```typescript
// Page component (Server Component)
// app/users/new/page.tsx
import { auth } from "@clerk/nextjs/server";
import { UserForm } from "~/features/users/components/user-form";
import { createUser } from "~/features/users/server/actions/users";
import type { CreateUserData } from "~/features/users/schemas/user";
import type { ActionResponse } from "~/lib/action-types";
import type { User } from "~/features/users/types/user";

export default async function NewUserPage() {
  const { userId } = await auth();

  // Bind authenticated user to action
  async function handleCreateUser(data: CreateUserData): ActionResponse<User> {
    "use server";
    return await createUser(data, userId!);
  }

  return (
    <main>
      <h1>Create User</h1>
      <UserForm onSubmitAction={handleCreateUser} />
    </main>
  );
}
```

```typescript
// Form component (Client Component)
// features/users/components/user-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useTransition } from "react";
import { userSchema, type CreateUserData } from "../schemas/user";
import type { ActionResponse } from "~/lib/action-types";
import type { User } from "../types/user";

type UserFormProps = {
  onSubmitAction: (data: CreateUserData) => ActionResponse<User>;
  defaultValues?: Partial<CreateUserData>;
  onSuccess?: (user: User) => void;
};

export function UserForm({ onSubmitAction, defaultValues, onSuccess }: UserFormProps) {
  const [isPending, startTransition] = useTransition();

  const form = useForm<CreateUserData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      name: "",
      email: "",
      ...defaultValues
    }
  });

  async function onSubmit(data: CreateUserData) {
    startTransition(async () => {
      const result = await onSubmitAction(data);

      if (result.success) {
        form.reset();
        onSuccess?.(result.data);
      } else {
        // Map server errors to form
        if (result.fieldErrors) {
          Object.entries(result.fieldErrors).forEach(([field, messages]) => {
            form.setError(field as keyof CreateUserData, {
              type: "server",
              message: messages[0]
            });
          });
        } else {
          form.setError("root", { message: result.error });
        }
      }
    });
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### Pattern 2: Redirect Action

For forms that navigate after successful submission.

```typescript
// types/action-types.ts
export type RedirectAction = Promise<never | { success: false; error: string; fieldErrors?: Record<string, string[]> }>;
```

```typescript
// Page component
// app/onboarding/preferences/page.tsx
import { PreferencesForm } from "~/features/onboarding/components/preferences-form";
import { submitPreferences } from "~/features/onboarding/server/actions/submit-preferences";
import { getOnboarding } from "~/features/onboarding/server/db/onboarding";
import type { PreferencesFormData } from "~/features/onboarding/schemas/preferences";

export default async function PreferencesPage() {
  const onboarding = await getOnboarding();

  async function handleSubmit(data: PreferencesFormData) {
    "use server";
    return await submitPreferences(data, onboarding);
  }

  return (
    <PreferencesForm
      onSubmitAction={handleSubmit}
      defaultValues={onboarding.preferences}
    />
  );
}
```

```typescript
// Form component for RedirectAction
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useTransition } from "react";
import { preferencesSchema, type PreferencesFormData } from "../schemas/preferences";
import type { RedirectAction } from "~/lib/action-types";

type PreferencesFormProps = {
  onSubmitAction: (data: PreferencesFormData) => RedirectAction;
  defaultValues?: Partial<PreferencesFormData>;
};

export function PreferencesForm({ onSubmitAction, defaultValues }: PreferencesFormProps) {
  const [isPending, startTransition] = useTransition();

  const form = useForm<PreferencesFormData>({
    resolver: zodResolver(preferencesSchema),
    defaultValues
  });

  async function onSubmit(data: PreferencesFormData) {
    startTransition(async () => {
      const result = await onSubmitAction(data);

      // If we reach here, it's an error (redirect would have thrown)
      if (!result.success) {
        if (result.fieldErrors) {
          Object.entries(result.fieldErrors).forEach(([field, messages]) => {
            form.setError(field as keyof PreferencesFormData, {
              type: "server",
              message: messages[0]
            });
          });
        } else {
          form.setError("root", { message: result.error });
        }
      }
    });
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### Pattern 3: Edit Form with Existing Data

```typescript
// Page component
// app/users/[id]/edit/page.tsx
import { notFound } from "next/navigation";
import { EditUserForm } from "~/features/users/components/edit-user-form";
import { getUserById, updateUser } from "~/features/users/server/db/users";
import type { UpdateUserData } from "~/features/users/schemas/user";

type PageProps = {
  params: Promise<{ id: string }>;
};

export default async function EditUserPage({ params }: PageProps) {
  const { id } = await params;
  const [error, user] = await getUserById(id);

  if (error?.isNotFound) notFound();
  if (error) throw error;

  async function handleUpdate(data: UpdateUserData) {
    "use server";
    return await updateUser(id, data);
  }

  return (
    <EditUserForm
      onSubmitAction={handleUpdate}
      defaultValues={{
        name: user.name,
        email: user.email,
        bio: user.bio ?? ""
      }}
    />
  );
}
```

---

## Error Handling

### Mapping Server Errors to Fields

```typescript
"use client";

import { useForm } from "react-hook-form";
import type { ActionResponse } from "~/lib/action-types";

type FormData = {
  email: string;
  username: string;
  password: string;
};

export function SignupForm({ onSubmitAction }: {
  onSubmitAction: (data: FormData) => ActionResponse<void>;
}) {
  const form = useForm<FormData>();

  async function onSubmit(data: FormData) {
    const result = await onSubmitAction(data);

    if (!result.success) {
      // Handle field-specific errors
      if (result.fieldErrors) {
        Object.entries(result.fieldErrors).forEach(([field, messages]) => {
          if (field in data) {
            // Known form field
            form.setError(field as keyof FormData, {
              type: "server",
              message: messages[0]
            });
          }
        });

        // Check for specific field errors
        if (result.fieldErrors.email?.includes("Email already exists")) {
          form.setError("email", {
            type: "server",
            message: "This email is already registered"
          });
        }
      }

      // Handle general error
      if (!result.fieldErrors) {
        form.setError("root.serverError", {
          type: "server",
          message: result.error
        });
      }
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Fields */}

      {/* Display root error */}
      {form.formState.errors.root?.serverError && (
        <div className="alert alert-error">
          {form.formState.errors.root.serverError.message}
        </div>
      )}
    </form>
  );
}
```

### Error Display Component

```typescript
// components/form-error.tsx
"use client";

import type { FieldError } from "react-hook-form";

type FormErrorProps = {
  error?: FieldError;
  id?: string;
};

export function FormError({ error, id }: FormErrorProps) {
  if (!error) return null;

  return (
    <p
      id={id}
      className="text-sm text-red-500 mt-1"
      role="alert"
    >
      {error.message}
    </p>
  );
}

// Usage
<input
  {...register("email")}
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
<FormError error={errors.email} id="email-error" />
```

### Clear Errors on Change

```typescript
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  mode: "onChange" // Validates on every change, clears errors
});

// Or manually clear specific error
<input
  {...register("email", {
    onChange: () => form.clearErrors("email")
  })}
/>

// Or clear all server errors when form changes
useEffect(() => {
  const subscription = form.watch(() => {
    if (form.formState.errors.root?.serverError) {
      form.clearErrors("root.serverError");
    }
  });
  return () => subscription.unsubscribe();
}, [form]);
```

---

## Field Types

### Text Input

```typescript
<input
  type="text"
  {...register("name")}
  placeholder="Enter name"
  disabled={isPending}
  className={errors.name ? "border-red-500" : ""}
/>
```

### Number Input

```typescript
// Schema
const schema = z.object({
  age: z.coerce.number().min(18).max(120),
  price: z.coerce.number().positive().multipleOf(0.01)
});

// Input
<input
  type="number"
  step="0.01"
  {...register("price", { valueAsNumber: true })}
/>
```

### Checkbox

```typescript
// Schema
const schema = z.object({
  terms: z.literal(true, {
    errorMap: () => ({ message: "You must accept the terms" })
  }),
  newsletter: z.boolean().default(false)
});

// Single checkbox
<label>
  <input type="checkbox" {...register("terms")} />
  I accept the terms and conditions
</label>
{errors.terms && <span>{errors.terms.message}</span>}

// Boolean checkbox
<label>
  <input type="checkbox" {...register("newsletter")} />
  Subscribe to newsletter
</label>
```

### Radio Buttons

```typescript
// Schema
const schema = z.object({
  plan: z.enum(["free", "pro", "enterprise"])
});

// Radio group
<fieldset>
  <legend>Select a plan</legend>

  <label>
    <input type="radio" value="free" {...register("plan")} />
    Free
  </label>

  <label>
    <input type="radio" value="pro" {...register("plan")} />
    Pro
  </label>

  <label>
    <input type="radio" value="enterprise" {...register("plan")} />
    Enterprise
  </label>

  {errors.plan && <span>{errors.plan.message}</span>}
</fieldset>
```

### Select

```typescript
// Schema
const schema = z.object({
  country: z.string().min(1, "Please select a country")
});

// Select input
<select {...register("country")} defaultValue="">
  <option value="" disabled>Select country</option>
  <option value="us">United States</option>
  <option value="uk">United Kingdom</option>
  <option value="pl">Poland</option>
</select>
```

### Textarea

```typescript
// Schema
const schema = z.object({
  bio: z.string().max(500, "Bio must be 500 characters or less").optional()
});

// Textarea with character count
const bio = form.watch("bio") ?? "";

<div>
  <textarea
    {...register("bio")}
    rows={4}
    maxLength={500}
  />
  <span className="text-sm text-gray-500">
    {bio.length}/500 characters
  </span>
</div>
```

### Date Input

```typescript
// Schema
const schema = z.object({
  birthDate: z.coerce.date().max(new Date(), "Cannot be in the future"),
  eventDate: z.string().refine((val) => !isNaN(Date.parse(val)), "Invalid date")
});

// Date input
<input
  type="date"
  {...register("birthDate")}
  max={new Date().toISOString().split("T")[0]}
/>
```

### File Input

```typescript
// Schema
const MAX_SIZE = 5 * 1024 * 1024;
const ACCEPTED_TYPES = ["image/jpeg", "image/png"];

const schema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length === 1, "Please select a file")
    .refine((files) => files[0]?.size <= MAX_SIZE, "Max size is 5MB")
    .refine(
      (files) => ACCEPTED_TYPES.includes(files[0]?.type),
      "Only .jpg and .png files"
    )
});

// File input
<input
  type="file"
  accept=".jpg,.jpeg,.png"
  {...register("avatar")}
/>
```

---

## Dynamic Fields (useFieldArray)

### Basic Array Field

```typescript
"use client";

import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  tasks: z.array(
    z.object({
      title: z.string().min(1, "Title is required"),
      completed: z.boolean().default(false)
    })
  ).min(1, "Add at least one task")
});

type FormData = z.infer<typeof schema>;

export function TaskListForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      tasks: [{ title: "", completed: false }]
    }
  });

  const { fields, append, remove, move } = useFieldArray({
    control: form.control,
    name: "tasks"
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id} className="flex gap-2">
          <input
            {...form.register(`tasks.${index}.title`)}
            placeholder="Task title"
          />
          {form.formState.errors.tasks?.[index]?.title && (
            <span className="error">
              {form.formState.errors.tasks[index]?.title?.message}
            </span>
          )}

          <label>
            <input
              type="checkbox"
              {...form.register(`tasks.${index}.completed`)}
            />
            Done
          </label>

          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>

          {index > 0 && (
            <button type="button" onClick={() => move(index, index - 1)}>
              Move Up
            </button>
          )}
        </div>
      ))}

      {form.formState.errors.tasks?.root && (
        <p className="error">{form.formState.errors.tasks.root.message}</p>
      )}

      <button
        type="button"
        onClick={() => append({ title: "", completed: false })}
      >
        Add Task
      </button>

      <button type="submit">Save</button>
    </form>
  );
}
```

### Nested Array Fields

```typescript
const schema = z.object({
  categories: z.array(
    z.object({
      name: z.string().min(1),
      items: z.array(
        z.object({
          name: z.string().min(1),
          amount: z.coerce.number().positive()
        })
      ).min(1, "Add at least one item")
    })
  )
});

type FormData = z.infer<typeof schema>;

export function BudgetForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      categories: [{ name: "", items: [{ name: "", amount: 0 }] }]
    }
  });

  const { fields: categoryFields, append: appendCategory, remove: removeCategory } =
    useFieldArray({
      control: form.control,
      name: "categories"
    });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {categoryFields.map((category, categoryIndex) => (
        <div key={category.id} className="category">
          <input
            {...form.register(`categories.${categoryIndex}.name`)}
            placeholder="Category name"
          />

          {/* Nested items array */}
          <CategoryItems
            control={form.control}
            register={form.register}
            categoryIndex={categoryIndex}
            errors={form.formState.errors}
          />

          <button type="button" onClick={() => removeCategory(categoryIndex)}>
            Remove Category
          </button>
        </div>
      ))}

      <button
        type="button"
        onClick={() => appendCategory({ name: "", items: [{ name: "", amount: 0 }] })}
      >
        Add Category
      </button>

      <button type="submit">Save Budget</button>
    </form>
  );
}

// Nested component for items
function CategoryItems({ control, register, categoryIndex, errors }) {
  const { fields, append, remove } = useFieldArray({
    control,
    name: `categories.${categoryIndex}.items`
  });

  return (
    <div className="items">
      {fields.map((item, itemIndex) => (
        <div key={item.id} className="item">
          <input
            {...register(`categories.${categoryIndex}.items.${itemIndex}.name`)}
            placeholder="Item name"
          />
          <input
            type="number"
            {...register(`categories.${categoryIndex}.items.${itemIndex}.amount`, {
              valueAsNumber: true
            })}
            placeholder="Amount"
          />
          <button type="button" onClick={() => remove(itemIndex)}>×</button>
        </div>
      ))}

      <button
        type="button"
        onClick={() => append({ name: "", amount: 0 })}
      >
        Add Item
      </button>
    </div>
  );
}
```

---

## Multi-Step Forms

### Wizard Form with Steps

```typescript
"use client";

import { useState } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// Step schemas
const step1Schema = z.object({
  name: z.string().min(2),
  email: z.string().email()
});

const step2Schema = z.object({
  company: z.string().min(1),
  role: z.string().min(1)
});

const step3Schema = z.object({
  plan: z.enum(["free", "pro", "enterprise"]),
  terms: z.literal(true)
});

// Combined schema
const fullSchema = step1Schema.merge(step2Schema).merge(step3Schema);
type FormData = z.infer<typeof fullSchema>;

const steps = [
  { schema: step1Schema, title: "Personal Info" },
  { schema: step2Schema, title: "Company Info" },
  { schema: step3Schema, title: "Plan Selection" }
];

export function WizardForm({ onSubmitAction }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPending, startTransition] = useTransition();

  const methods = useForm<FormData>({
    resolver: zodResolver(fullSchema),
    mode: "onChange",
    defaultValues: {
      name: "",
      email: "",
      company: "",
      role: "",
      plan: "free",
      terms: false
    }
  });

  const { trigger, handleSubmit, formState } = methods;

  async function goToNextStep() {
    const currentSchema = steps[currentStep].schema;
    const fieldsToValidate = Object.keys(currentSchema.shape) as (keyof FormData)[];

    const isValid = await trigger(fieldsToValidate);

    if (isValid) {
      setCurrentStep((prev) => prev + 1);
    }
  }

  function goToPreviousStep() {
    setCurrentStep((prev) => prev - 1);
  }

  async function onSubmit(data: FormData) {
    startTransition(async () => {
      const result = await onSubmitAction(data);

      if (!result.success) {
        methods.setError("root", { message: result.error });
      }
    });
  }

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Progress indicator */}
        <div className="steps">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`step ${index === currentStep ? "active" : ""} ${index < currentStep ? "completed" : ""}`}
            >
              {step.title}
            </div>
          ))}
        </div>

        {/* Step content */}
        {currentStep === 0 && <Step1 />}
        {currentStep === 1 && <Step2 />}
        {currentStep === 2 && <Step3 />}

        {/* Error display */}
        {formState.errors.root && (
          <p className="error">{formState.errors.root.message}</p>
        )}

        {/* Navigation */}
        <div className="flex gap-2">
          {currentStep > 0 && (
            <button type="button" onClick={goToPreviousStep}>
              Previous
            </button>
          )}

          {currentStep < steps.length - 1 ? (
            <button type="button" onClick={goToNextStep}>
              Next
            </button>
          ) : (
            <button type="submit" disabled={isPending}>
              {isPending ? "Submitting..." : "Submit"}
            </button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}

// Step components
function Step1() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <input {...register("name")} placeholder="Name" />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register("email")} placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}
    </div>
  );
}

function Step2() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <input {...register("company")} placeholder="Company" />
      {errors.company && <span>{errors.company.message}</span>}

      <input {...register("role")} placeholder="Role" />
      {errors.role && <span>{errors.role.message}</span>}
    </div>
  );
}

function Step3() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <select {...register("plan")}>
        <option value="free">Free</option>
        <option value="pro">Pro</option>
        <option value="enterprise">Enterprise</option>
      </select>

      <label>
        <input type="checkbox" {...register("terms")} />
        I accept the terms
      </label>
      {errors.terms && <span>{errors.terms.message}</span>}
    </div>
  );
}
```

---

## Form Reset and Default Values

### Reset After Success

```typescript
async function onSubmit(data: FormData) {
  const result = await onSubmitAction(data);

  if (result.success) {
    // Reset to initial default values
    form.reset();

    // Or reset to specific values
    form.reset({
      name: "",
      email: result.data.email // Keep email
    });
  }
}
```

### Update Default Values

```typescript
// When defaultValues change (e.g., data loaded)
useEffect(() => {
  if (userData) {
    form.reset({
      name: userData.name,
      email: userData.email
    });
  }
}, [userData, form]);
```

### Keep Form Dirty State

```typescript
// Reset but keep dirty fields
form.reset(undefined, {
  keepDirty: true,
  keepDirtyValues: true
});

// Reset specific field
form.resetField("email");

// Reset and keep errors
form.reset(undefined, {
  keepErrors: true
});
```

---

## Integration with UI Libraries

### With Design System Components

```typescript
"use client";

import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Input,
  Select,
  Checkbox,
  Button,
  FormField,
  FormError
} from "@szum-tech/design-system";
import { userSchema, type UserFormData } from "../schemas/user";

export function UserForm({ onSubmitAction }) {
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<UserFormData>({
    resolver: zodResolver(userSchema)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormField label="Name" error={errors.name?.message}>
        <Controller
          name="name"
          control={control}
          render={({ field }) => (
            <Input
              {...field}
              placeholder="Enter name"
              error={!!errors.name}
            />
          )}
        />
      </FormField>

      <FormField label="Role" error={errors.role?.message}>
        <Controller
          name="role"
          control={control}
          render={({ field }) => (
            <Select
              {...field}
              options={[
                { value: "admin", label: "Admin" },
                { value: "user", label: "User" }
              ]}
              error={!!errors.role}
            />
          )}
        />
      </FormField>

      <Controller
        name="newsletter"
        control={control}
        render={({ field: { value, onChange, ...field } }) => (
          <Checkbox
            {...field}
            checked={value}
            onCheckedChange={onChange}
            label="Subscribe to newsletter"
          />
        )}
      />

      <Button type="submit" loading={isSubmitting}>
        Save
      </Button>
    </form>
  );
}
```

### Reusable Form Field Component

```typescript
// components/form-field.tsx
"use client";

import { useFormContext, Controller } from "react-hook-form";
import { Input, FormError } from "@szum-tech/design-system";

type FormInputProps = {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
};

export function FormInput({ name, label, type = "text", placeholder }: FormInputProps) {
  const { control, formState: { errors } } = useFormContext();

  const error = errors[name];

  return (
    <div className="form-field">
      <label htmlFor={name}>{label}</label>
      <Controller
        name={name}
        control={control}
        render={({ field }) => (
          <Input
            {...field}
            id={name}
            type={type}
            placeholder={placeholder}
            error={!!error}
            aria-invalid={!!error}
            aria-describedby={error ? `${name}-error` : undefined}
          />
        )}
      />
      {error && (
        <FormError id={`${name}-error`}>
          {error.message as string}
        </FormError>
      )}
    </div>
  );
}

// Usage
<FormProvider {...methods}>
  <form onSubmit={handleSubmit(onSubmit)}>
    <FormInput name="name" label="Name" placeholder="Enter name" />
    <FormInput name="email" label="Email" type="email" />
    <FormInput name="password" label="Password" type="password" />
  </form>
</FormProvider>
```
