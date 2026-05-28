---
name: form-patterens-and-best-practices
description: This skill provides guidance for creating consistent, well-structured forms in Next.js/react applications using shadcn UI components, react-hook-form, and Zod validation.
---

# Form Patterns and Best Practices

## Overview
This skill provides guidance for creating consistent, well-structured forms in Next.js/react applications using shadcn UI components, react-hook-form, and Zod validation.

## Form Structure Pattern

### Required Imports
Every form should import the following components and libraries:

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { formSchema, type FormDataType } from "@/features/feature-name/schema"; // Adjust import path
import Link from "next/link"; // If needed for navigation
```

### Form Component Structure
All forms should follow this structure with the shadcn Form components:

```tsx
export const FormComponentName = () => {
  const form = useForm<FormDataType>({
    resolver: zodResolver(formSchema),
    // Optionally set default values
    // defaultValues: {
    //   fieldName: "defaultValue"
    // }
  });

  const onSubmit = async (data: FormDataType) => {
    // Handle form submission
    // This could be a mutation call, API request, etc.
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">

        <FormField
          name="fieldName"
          control={form.control}
          render={({ field }) => (
            <FormItem>
              <FormLabel>Field Label</FormLabel>
              <FormControl>
                <Input placeholder="Placeholder text" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Add more FormField components as needed */}

        <Button type="submit" className="w-full">
          Submit
        </Button>
      </form>
    </Form>
  );
}
```

## Feature Hook Integration

When creating forms that interact with feature-specific hooks (authentication, tasks, todos, etc.), integrate the hook's mutation functions:

### Required Additional Imports
```tsx
import { useFeatureName } from "@/features/feature-name/hooks"; // e.g., useAuth, useTasks, useTodos
```

### Integration Pattern
```tsx
export function FeatureFormComponent() {
  const { featureFunction: {  // e.g., signIn/signUp/forgotPassword for auth, createTask/updateTask for tasks
    mutateAsync: featureFunction,
    isPending: isLoading,
  } } = useFeatureName(); // e.g., useAuth, useTasks, useTodos

  // ... rest of the form structure remains the same, just with loading state in the button
  <Button type="submit" className="w-full" disabled={isLoading}>
    {isLoading ? "Submitting..." : "Action Text"}
  </Button>
}
```

## Form Location and Organization

### File Location
- All form components MUST be placed in `src/components/forms` folder
- Organize forms by feature or purpose
- Keep form components separate from other UI components

### File Naming Convention
- Use descriptive names that reflect the form's purpose
- Use kebab-case for file names (e.g., `sign-in-form.tsx`, `user-profile-form.tsx`)
- Include "form" in the name to clearly identify it as a form component

## Validation Schema Pattern

### Schema Location
- Form validation schemas MUST be placed in `src/features/[feature-name]/schema.ts`
- Use Zod for schema validation
- Export both the schema and the inferred type

### Schema Example
```tsx
import { z } from "zod";

export const formSchema = z.object({
  fieldName: z.string().min(1, { message: "Field is required" }),
  email: z.email({ message: "Invalid email address" }),
  password: z.string().min(8, { message: "Password must be at least 8 characters" }),
});

// For forms with confirm password validation
export const formWithConfirmPasswordSchema = z.object({
  password: z.string().min(8, { message: "Password must be at least 8 characters" }),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

export type FormDataType = z.infer<typeof formSchema>;
```

## Loading States and Error Handling

### Loading States
- Use the loading state from mutations when available (e.g., `isPending` from useFeatureName hooks)
- Disable the submit button when loading
- Show loading text in the button

### Error Handling
- Form validation errors are automatically handled by FormMessage components
- API/mutation errors should be handled by the mutation's error handling in the hooks
- Use toast notifications for user feedback when needed


## Testing and Validation

### Form Validation
- All forms MUST use Zod schema validation
- Validation errors MUST be displayed using FormMessage components
- Client-side validation should match server-side validation rules

### Accessibility
- All form fields MUST have associated labels
- Use proper ARIA attributes when needed
- Ensure proper focus management
