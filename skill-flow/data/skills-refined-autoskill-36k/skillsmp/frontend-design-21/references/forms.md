# Forms & Validation

## Table of Contents
- [Form Setup](#form-setup)
- [Basic Fields](#basic-fields)
- [Validation with Zod](#validation-with-zod)
- [Form Patterns](#form-patterns)
- [Mobile Form UX](#mobile-form-ux)

## Form Setup

### React Hook Form + Zod
```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@ui/form";
import { Input } from "@ui/input";
import { Button } from "@ui/button";

// 1. Define schema
const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormValues = z.infer<typeof formSchema>;

// 2. Create form
function MyForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = (data: FormValues) => {
    console.log(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Submit
        </Button>
      </form>
    </Form>
  );
}
```

## Basic Fields

### Text Input
```tsx
<FormField
  control={form.control}
  name="name"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Name</FormLabel>
      <FormControl>
        <Input placeholder="Enter your name" {...field} />
      </FormControl>
      <FormDescription>Your display name.</FormDescription>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Textarea
```tsx
<FormField
  control={form.control}
  name="bio"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Bio</FormLabel>
      <FormControl>
        <Textarea
          placeholder="Tell us about yourself"
          className="resize-none"
          rows={4}
          {...field}
        />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Select
```tsx
<FormField
  control={form.control}
  name="role"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Role</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="admin">Admin</SelectItem>
          <SelectItem value="user">User</SelectItem>
          <SelectItem value="guest">Guest</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Checkbox
```tsx
<FormField
  control={form.control}
  name="terms"
  render={({ field }) => (
    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox
          checked={field.value}
          onCheckedChange={field.onChange}
        />
      </FormControl>
      <div className="space-y-1 leading-none">
        <FormLabel>Accept terms and conditions</FormLabel>
        <FormDescription>
          You agree to our Terms of Service.
        </FormDescription>
      </div>
    </FormItem>
  )}
/>
```

### Switch
```tsx
<FormField
  control={form.control}
  name="notifications"
  render={({ field }) => (
    <FormItem className="flex items-center justify-between rounded-lg border p-4">
      <div className="space-y-0.5">
        <FormLabel className="text-base">Notifications</FormLabel>
        <FormDescription>Receive email notifications.</FormDescription>
      </div>
      <FormControl>
        <Switch checked={field.value} onCheckedChange={field.onChange} />
      </FormControl>
    </FormItem>
  )}
/>
```

### Radio Group
```tsx
<FormField
  control={form.control}
  name="type"
  render={({ field }) => (
    <FormItem className="space-y-3">
      <FormLabel>Notification Type</FormLabel>
      <FormControl>
        <RadioGroup
          onValueChange={field.onChange}
          defaultValue={field.value}
          className="flex flex-col space-y-1"
        >
          <FormItem className="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="all" />
            </FormControl>
            <FormLabel className="font-normal">All notifications</FormLabel>
          </FormItem>
          <FormItem className="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="important" />
            </FormControl>
            <FormLabel className="font-normal">Important only</FormLabel>
          </FormItem>
        </RadioGroup>
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Validation with Zod

### Common Schemas
```tsx
import { z } from "zod";

// Email
const emailSchema = z.string().email("Invalid email");

// Password with requirements
const passwordSchema = z
  .string()
  .min(8, "Minimum 8 characters")
  .regex(/[A-Z]/, "Must contain uppercase")
  .regex(/[0-9]/, "Must contain number");

// Optional field
const optionalField = z.string().optional();

// Nullable field
const nullableField = z.string().nullable();

// Number with range
const ageSchema = z.number().min(0).max(120);

// Array
const tagsSchema = z.array(z.string()).min(1, "At least one tag required");

// Enum
const roleSchema = z.enum(["admin", "user", "guest"]);

// Object
const addressSchema = z.object({
  street: z.string().min(1, "Required"),
  city: z.string().min(1, "Required"),
  zip: z.string().regex(/^\d{5}$/, "Invalid ZIP code"),
});

// Conditional validation
const conditionalSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("email"), email: z.string().email() }),
  z.object({ type: z.literal("phone"), phone: z.string() }),
]);

// Custom validation
const usernameSchema = z
  .string()
  .min(3)
  .refine((val) => !val.includes(" "), "No spaces allowed");
```

### Full Form Schema Example
```tsx
const signupSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain at least one uppercase letter")
    .regex(/[0-9]/, "Must contain at least one number"),
  confirmPassword: z.string(),
  terms: z.boolean().refine((val) => val === true, "You must accept the terms"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

## Form Patterns

### Login Form
```tsx
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1, "Required"),
});

function LoginForm() {
  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Sign In
        </Button>
      </form>
    </Form>
  );
}
```

### Search Form
```tsx
function SearchForm({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSearch(query);
      }}
      className="flex gap-2"
    >
      <Input
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1"
      />
      <Button type="submit" size="icon">
        <Search className="h-4 w-4" />
      </Button>
    </form>
  );
}
```

### Settings Form
```tsx
function SettingsForm({ defaultValues, onSave }) {
  const form = useForm({
    resolver: zodResolver(settingsSchema),
    defaultValues,
  });

  const isDirty = form.formState.isDirty;

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSave)} className="space-y-6">
        {/* Form fields */}

        <div className="flex gap-2 justify-end">
          <Button
            type="button"
            variant="outline"
            onClick={() => form.reset()}
            disabled={!isDirty}
          >
            Reset
          </Button>
          <Button type="submit" disabled={!isDirty}>
            Save Changes
          </Button>
        </div>
      </form>
    </Form>
  );
}
```

## Mobile Form UX

### Touch-Friendly Inputs
```tsx
// Larger input for mobile
<Input className="h-12 text-base" />

// Full-width button
<Button className="w-full h-12">Submit</Button>

// Proper spacing between fields
<div className="space-y-6">
  {/* Fields */}
</div>
```

### Input Types for Mobile Keyboards
```tsx
// Email keyboard
<Input type="email" inputMode="email" />

// Number keyboard
<Input type="text" inputMode="numeric" pattern="[0-9]*" />

// Phone keyboard
<Input type="tel" inputMode="tel" />

// URL keyboard
<Input type="url" inputMode="url" />

// Search keyboard with "Search" button
<Input type="search" enterKeyHint="search" />
```

### Preventing Zoom on Focus (iOS)
```tsx
// Font size >= 16px prevents iOS zoom
<Input className="text-base" />  // 16px
```

### Error Display
```tsx
// Inline error
<FormMessage className="text-sm text-destructive mt-1" />

// Toast on submit error
const onError = (errors) => {
  toast.error("Please fix the errors in the form");
};

<form onSubmit={form.handleSubmit(onSubmit, onError)}>
```

### Loading State
```tsx
const [isSubmitting, setIsSubmitting] = useState(false);

<Button type="submit" disabled={isSubmitting}>
  {isSubmitting ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Saving...
    </>
  ) : (
    "Save"
  )}
</Button>
```

### Sticky Submit Button (Mobile)
```tsx
<form className="pb-20 md:pb-0">
  {/* Form fields */}

  {/* Fixed submit on mobile */}
  <div className="fixed bottom-0 left-0 right-0 p-4 bg-background border-t md:relative md:p-0 md:border-0 md:bg-transparent safe-area-bottom">
    <Button type="submit" className="w-full md:w-auto">
      Submit
    </Button>
  </div>
</form>
```
