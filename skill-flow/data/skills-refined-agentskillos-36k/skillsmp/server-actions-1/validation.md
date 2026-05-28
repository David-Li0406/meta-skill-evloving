# Zod Validation for Server Actions

## Table of Contents

1. [Basic Schema Patterns](#basic-schema-patterns)
2. [Field Validation Patterns](#field-validation-patterns)
3. [Cross-Field Validation](#cross-field-validation)
4. [Array and Nested Schemas](#array-and-nested-schemas)
5. [Form Data Parsing](#form-data-parsing)
6. [Error Handling](#error-handling)
7. [Type Inference](#type-inference)
8. [Schema Organization](#schema-organization)

---

## Basic Schema Patterns

### Simple Form Schema

```typescript
// features/users/schemas/user.ts
import { z } from "zod";

export const createUserSchema = z.object({
  name: z
    .string({ required_error: "Name is required" })
    .min(2, "Name must be at least 2 characters")
    .max(100, "Name must be less than 100 characters"),

  email: z
    .string({ required_error: "Email is required" })
    .email("Please enter a valid email address"),

  age: z
    .number({ required_error: "Age is required" })
    .int("Age must be a whole number")
    .min(18, "Must be at least 18 years old")
    .max(120, "Please enter a valid age")
});

// Infer TypeScript types
export type CreateUserData = z.infer<typeof createUserSchema>;
```

### Update Schema (Partial)

```typescript
// All fields optional for updates
export const updateUserSchema = createUserSchema.partial();

export type UpdateUserData = z.infer<typeof updateUserSchema>;

// Or make specific fields required
export const updateUserSchema = createUserSchema.partial().required({
  name: true // Name is still required for updates
});
```

### Schema with Defaults

```typescript
export const settingsSchema = z.object({
  theme: z.enum(["light", "dark", "system"]).default("system"),
  notifications: z.boolean().default(true),
  language: z.string().default("en")
});
```

---

## Field Validation Patterns

### String Validations

```typescript
const stringExamples = z.object({
  // Required string
  required: z.string({ required_error: "This field is required" }),

  // Optional string
  optional: z.string().optional(),

  // Nullable string
  nullable: z.string().nullable(),

  // String with length constraints
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username must be at most 20 characters")
    .regex(/^[a-z0-9_]+$/, "Username can only contain lowercase letters, numbers, and underscores"),

  // Email
  email: z.string().email("Invalid email address"),

  // URL
  website: z.string().url("Invalid URL"),

  // UUID
  id: z.string().uuid("Invalid ID format"),

  // Trim whitespace
  trimmed: z.string().trim(),

  // Transform to lowercase
  lowercased: z.string().toLowerCase(),

  // Non-empty string
  nonEmpty: z.string().min(1, "Cannot be empty")
});
```

### Number Validations

```typescript
const numberExamples = z.object({
  // Basic number
  count: z.number(),

  // Integer only
  quantity: z.number().int("Must be a whole number"),

  // Positive number
  price: z.number().positive("Price must be positive"),

  // Range
  rating: z
    .number()
    .min(1, "Rating must be at least 1")
    .max(5, "Rating must be at most 5"),

  // Percentage
  percentage: z
    .number()
    .min(0, "Cannot be negative")
    .max(100, "Cannot exceed 100%"),

  // Currency (2 decimal places)
  amount: z
    .number()
    .multipleOf(0.01, "Amount must have at most 2 decimal places")
});
```

### Enum and Literal

```typescript
// Enum validation
const statusSchema = z.enum(["draft", "published", "archived"], {
  errorMap: () => ({ message: "Please select a valid status" })
});

// Union of literals
const prioritySchema = z.union([
  z.literal("low"),
  z.literal("medium"),
  z.literal("high")
]);

// Native enum
enum UserRole {
  Admin = "admin",
  User = "user",
  Guest = "guest"
}
const roleSchema = z.nativeEnum(UserRole);
```

### Date Validations

```typescript
const dateExamples = z.object({
  // Date object
  createdAt: z.date(),

  // ISO date string to Date
  birthDate: z.coerce.date(),

  // Date in the past
  birthDate: z
    .date()
    .max(new Date(), "Birth date cannot be in the future"),

  // Date in the future
  scheduledFor: z
    .date()
    .min(new Date(), "Scheduled date must be in the future"),

  // Date range
  eventDate: z
    .date()
    .min(new Date("2024-01-01"), "Date must be after Jan 1, 2024")
    .max(new Date("2024-12-31"), "Date must be before Dec 31, 2024")
});
```

### Boolean and Checkbox

```typescript
const checkboxExamples = z.object({
  // Simple boolean
  isActive: z.boolean(),

  // Required to be true (like terms acceptance)
  acceptTerms: z.literal(true, {
    errorMap: () => ({ message: "You must accept the terms" })
  }),

  // Boolean with default
  newsletter: z.boolean().default(false),

  // Coerce from string (for form checkboxes)
  rememberMe: z.coerce.boolean()
});
```

---

## Cross-Field Validation

### Password Confirmation

```typescript
export const passwordSchema = z
  .object({
    password: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
      .regex(/[a-z]/, "Password must contain at least one lowercase letter")
      .regex(/[0-9]/, "Password must contain at least one number"),
    confirmPassword: z.string()
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"] // Error appears on confirmPassword field
  });
```

### Conditional Required Fields

```typescript
export const contactSchema = z
  .object({
    contactMethod: z.enum(["email", "phone"]),
    email: z.string().email().optional(),
    phone: z.string().optional()
  })
  .refine(
    (data) => {
      if (data.contactMethod === "email") {
        return !!data.email;
      }
      if (data.contactMethod === "phone") {
        return !!data.phone;
      }
      return true;
    },
    {
      message: "Please provide the selected contact method",
      path: ["email"] // Or dynamically set based on contactMethod
    }
  );
```

### Budget Allocation Validation

```typescript
export const budgetSchema = z
  .object({
    totalBudget: z.number().positive("Budget must be positive"),
    categories: z.array(
      z.object({
        name: z.string().min(1, "Category name is required"),
        amount: z.number().min(0, "Amount cannot be negative")
      })
    )
  })
  .refine(
    (data) => {
      const totalAllocated = data.categories.reduce(
        (sum, cat) => sum + cat.amount,
        0
      );
      return totalAllocated <= data.totalBudget;
    },
    {
      message: "Total allocations exceed budget",
      path: ["categories"]
    }
  );
```

### Date Range Validation

```typescript
export const dateRangeSchema = z
  .object({
    startDate: z.date(),
    endDate: z.date()
  })
  .refine((data) => data.endDate > data.startDate, {
    message: "End date must be after start date",
    path: ["endDate"]
  });
```

---

## Array and Nested Schemas

### Array Validation

```typescript
export const tagsSchema = z.object({
  // Array with min/max length
  tags: z
    .array(z.string().min(1, "Tag cannot be empty"))
    .min(1, "At least one tag is required")
    .max(10, "Maximum 10 tags allowed"),

  // Array of objects
  items: z.array(
    z.object({
      id: z.string().uuid(),
      quantity: z.number().int().positive()
    })
  ),

  // Non-empty array
  categories: z.array(z.string()).nonempty("Select at least one category")
});
```

### Nested Object Schema

```typescript
const addressSchema = z.object({
  street: z.string().min(1, "Street is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().length(2, "Use 2-letter state code"),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, "Invalid ZIP code")
});

export const customerSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email(),
  billingAddress: addressSchema,
  shippingAddress: addressSchema.optional()
});
```

### Discriminated Union

```typescript
const paymentSchema = z.discriminatedUnion("method", [
  z.object({
    method: z.literal("credit_card"),
    cardNumber: z.string().length(16, "Card number must be 16 digits"),
    cvv: z.string().length(3, "CVV must be 3 digits"),
    expiryMonth: z.number().min(1).max(12),
    expiryYear: z.number().min(2024)
  }),
  z.object({
    method: z.literal("bank_transfer"),
    accountNumber: z.string().min(8, "Invalid account number"),
    routingNumber: z.string().length(9, "Routing number must be 9 digits")
  }),
  z.object({
    method: z.literal("paypal"),
    paypalEmail: z.string().email("Invalid PayPal email")
  })
]);
```

---

## Form Data Parsing

### Basic FormData Parsing

```typescript
export async function createPost(formData: FormData): ActionResponse<Post> {
  const rawData = {
    title: formData.get("title"),
    content: formData.get("content"),
    published: formData.get("published") === "true"
  };

  const parsed = postSchema.safeParse(rawData);

  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Use parsed.data (typed and validated)
  const [error, post] = await createPostInDb(parsed.data);
  // ...
}
```

### FormData with Coercion

```typescript
// Schema with coercion for form values (always strings)
export const productSchema = z.object({
  name: z.string().min(1),
  price: z.coerce.number().positive(), // Converts "19.99" to 19.99
  quantity: z.coerce.number().int().positive(), // Converts "5" to 5
  available: z.coerce.boolean(), // Converts "true"/"on" to true
  releaseDate: z.coerce.date() // Converts ISO string to Date
});

export async function createProduct(formData: FormData): ActionResponse<Product> {
  const rawData = Object.fromEntries(formData.entries());
  const parsed = productSchema.safeParse(rawData);
  // ...
}
```

### File Upload Validation

```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

export const uploadSchema = z.object({
  file: z
    .instanceof(File)
    .refine((file) => file.size <= MAX_FILE_SIZE, "File size must be less than 5MB")
    .refine(
      (file) => ACCEPTED_IMAGE_TYPES.includes(file.type),
      "Only .jpg, .png, and .webp files are accepted"
    )
});
```

---

## Error Handling

### Flatten Errors for Forms

```typescript
const parsed = schema.safeParse(data);

if (!parsed.success) {
  const flattened = parsed.error.flatten();

  // flattened.formErrors - array of errors not associated with a specific field
  // flattened.fieldErrors - object mapping field names to arrays of errors

  return {
    success: false,
    error: flattened.formErrors[0] || "Validation failed",
    fieldErrors: flattened.fieldErrors
  };
}
```

### Custom Error Messages

```typescript
export const userSchema = z.object({
  email: z.string({
    required_error: "Email address is required",
    invalid_type_error: "Email must be a string"
  }).email({
    message: "Please enter a valid email address"
  }),

  age: z.number({
    required_error: "Age is required",
    invalid_type_error: "Age must be a number"
  }).int({
    message: "Age must be a whole number"
  })
});
```

### Error Map for Complex Schemas

```typescript
export const formSchema = z.object({
  items: z
    .array(
      z.object({
        name: z.string(),
        price: z.number()
      })
    )
    .min(1, "Add at least one item")
}, {
  errorMap: (issue, ctx) => {
    if (issue.code === "too_small" && issue.path[0] === "items") {
      return { message: "Your cart is empty. Please add at least one item." };
    }
    return { message: ctx.defaultError };
  }
});
```

---

## Type Inference

### Input vs Output Types

```typescript
const userSchema = z.object({
  name: z.string().transform((val) => val.trim()),
  email: z.string().email().toLowerCase(),
  birthDate: z.coerce.date()
});

// Input type (what the form sends)
type UserInput = z.input<typeof userSchema>;
// { name: string; email: string; birthDate: string | Date }

// Output type (after parsing and transforms)
type UserOutput = z.output<typeof userSchema>;
// { name: string; email: string; birthDate: Date }

// z.infer is alias for z.output
type User = z.infer<typeof userSchema>;
// Same as UserOutput
```

### Partial and Required

```typescript
const baseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().optional()
});

// All fields optional
type PartialUser = z.infer<typeof baseSchema.partial()>;

// All fields required
type RequiredUser = z.infer<typeof baseSchema.required()>;

// Pick specific fields
type UserEmail = z.infer<typeof baseSchema.pick({ email: true })>;

// Omit specific fields
type UserWithoutId = z.infer<typeof baseSchema.omit({ id: true })>;
```

---

## Schema Organization

### File Structure

```text
features/
  users/
    schemas/
      user.ts           # User-related schemas
      profile.ts        # Profile schemas
      index.ts          # Re-exports
```

### Schema Re-exports

```typescript
// features/users/schemas/index.ts
export {
  createUserSchema,
  updateUserSchema,
  type CreateUserData,
  type UpdateUserData
} from "./user";

export {
  profileSchema,
  type ProfileData
} from "./profile";
```

### Shared Schema Utilities

```typescript
// lib/schemas/common.ts
import { z } from "zod";

// Common patterns
export const idSchema = z.string().uuid("Invalid ID format");

export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
});

export const timestampsSchema = z.object({
  createdAt: z.date(),
  updatedAt: z.date()
});

// Compose with feature schemas
export const userSchema = z.object({
  id: idSchema,
  name: z.string().min(1),
  email: z.string().email()
}).merge(timestampsSchema);
```

### Schema with Documentation

```typescript
/**
 * Schema for creating a new blog post
 *
 * @example
 * ```typescript
 * const data: CreatePostData = {
 *   title: "My First Post",
 *   content: "Hello, world!",
 *   tags: ["intro", "welcome"]
 * };
 * ```
 */
export const createPostSchema = z.object({
  /** Post title, 5-100 characters */
  title: z.string().min(5).max(100),

  /** Post content in markdown format */
  content: z.string().min(10),

  /** Optional tags for categorization */
  tags: z.array(z.string()).max(5).default([])
});

export type CreatePostData = z.infer<typeof createPostSchema>;
```
