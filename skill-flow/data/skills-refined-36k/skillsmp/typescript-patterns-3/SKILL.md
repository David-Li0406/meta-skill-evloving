---
name: typescript-patterns
description: "WHAT: TypeScript type patterns and Zod schema-first validation. WHEN: defining types, validating API data, creating type guards, using generics. KEYWORDS: typescript, types, interface, zod, schema, validation, generics, discriminated unions, type guards, const assertions."
---

# TypeScript Patterns Standards

Standards for TypeScript type definitions, runtime validation with Zod, generics, and type safety patterns.

## When to Use

Use these standards when:
- Defining types, interfaces, or type aliases
- Validating API responses or user input
- Creating generic functions or components
- Implementing state machines or reducers
- Writing type guards or utility types
- Ensuring type safety at runtime

## Core Principles

### Zero Tolerance for `any`

**Never use `any` type. Use `unknown` with type guards or generics instead.**

✅ **Good:**
```typescript
// Use unknown and type guards
const processData = (data: unknown) => {
  if (isRecipeDetail(data)) {
    return data.title; // Type-safe
  }
  throw new Error('Invalid data');
};

// Or use generics
const processData = <T extends { value: string }>(data: T) => {
  return data.value;
};
```

❌ **Bad:**
```typescript
const processData = (data: any) => {
  return data.value; // No type safety
};
```

**Why:** `any` disables all type checking, defeating the purpose of TypeScript. `unknown` requires explicit type narrowing, catching errors at compile time.

### Zod Schema-First Types

Define Zod schemas first, then infer TypeScript types. Single source of truth.

✅ **Good:**
```typescript
import { z } from 'zod';

// 1. Define Zod schema with validation rules
export const RecipeDetailSchema = z.object({
  id: z.string().min(1, 'Recipe ID cannot be empty').trim(),
  title: z.string().min(1, 'Recipe title cannot be empty').trim(),
  heroImageUrl: z.string().url('Invalid hero image URL'),
  savedDate: z.string().datetime({ offset: true }),
  ingredients: z.array(RecipeIngredientSchema).min(1, 'At least one ingredient required'),
});

// 2. Infer TypeScript type from schema
export type RecipeDetail = z.infer<typeof RecipeDetailSchema>;

// 3. Create type guard
export const isRecipeDetail = (obj: unknown): obj is RecipeDetail => {
  return RecipeDetailSchema.safeParse(obj).success;
};

// 4. Create parse function
export const parseRecipeDetail = (obj: unknown) => {
  return RecipeDetailSchema.safeParse(obj);
};
```

❌ **Bad:**
```typescript
// Separate type and schema - can drift
type RecipeDetail = {
  id: string;
  title: string;
};

const schema = z.object({ id: z.string(), title: z.string() });
```

**Why:** Schema-first ensures runtime validation matches TypeScript types. Prevents drift between validation and types.

### Type Aliases vs Interfaces

Use `type` for unions and primitives. Use `interface` for object shapes that may be extended.

✅ **Good:**
```typescript
// Types for unions, primitives, aliases
export type ProductId = Scalars['ShoppableProductId']['output'];
export type Action = 'onDecreaseProduct' | 'onRemoveProduct' | 'onSwapCourse';
export type Source = 'LIST' | 'CAROUSEL' | 'WIDGET' | 'POPUP';

// Interface for object shapes that may be extended
export interface UserProfileProps {
  userId: string;
  onEdit: () => void;
}

// Type for complex object shapes (no extension needed)
export type TrackingParams = {
  recipePosition?: number;
  widgetName?: string;
  source?: Source;
  topLayer?: TopLayer;
  screenName?: ScreenName;
};
```

❌ **Bad:**
```typescript
// Interface for union types
interface Action {
  type: 'onDecreaseProduct' | 'onRemoveProduct';
}

// Type for extendable object shapes
type UserProfileProps = {
  userId: string;
};
```

**Why:** Types are more flexible for unions/primitives. Interfaces enable declaration merging and better error messages for objects.

**When to use type:**
- Union types
- Type aliases for primitives
- Complex object shapes with mapped/conditional types
- Function types

**When to use interface:**
- Object shapes that may be extended
- Class contracts
- Declaration merging

### Const Assertions Over Enums

Use `as const` for immutable constant objects instead of enums.

✅ **Good:**
```typescript
// Const assertion for constants
export const SCREEN_NAME = {
  HOME: 'Home',
  STORE: 'Store',
  UPSELL: 'Upsell',
} as const;

// Derive type from const
export type ScreenName = (typeof SCREEN_NAME)[keyof typeof SCREEN_NAME];
```

❌ **Bad:**
```typescript
// Plain object without 'as const'
export const SCREEN_NAME = {
  HOME: 'Home', // Type is string, not literal 'Home'
};

// Enum (rarely needed)
export enum ScreenName {
  Home = 'Home',
  Store = 'Store',
}
```

**Why:** `as const` creates readonly literal types with better type inference and tree-shaking. Enums generate runtime code.

**Use enums only when:**
- You need reverse mapping (enum value to key name)
- You have sequential numeric values with meaning
- You need to iterate over all values

### Import Type Syntax

Use `import type` for type-only imports to reduce bundle size.

✅ **Good:**
```typescript
import type { User, Subscription } from '@data-access/graphql';
import type { ComponentProps } from './types';

// Inline type imports (when importing values too)
import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
import { View, type ViewStyle } from 'react-native';
```

❌ **Bad:**
```typescript
import { User, ComponentProps } from './types'; // Unclear which are types
```

**Why:** `import type` is erased at runtime, reducing bundle size. Signals to readers these are type-only imports.

## Discriminated Unions

Use discriminated unions for state machines and action types.

✅ **Good:**
```typescript
// State machine with discriminated union
type AsyncData<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// TypeScript narrows types based on discriminant
const renderData = (state: AsyncData<Recipe>) => {
  switch (state.status) {
    case 'idle':
      return null;
    case 'loading':
      return <LoadingSpinner />;
    case 'success':
      return <RecipeList recipes={state.data} />; // data is Recipe
    case 'error':
      return <ErrorMessage error={state.error} />; // error is Error
  }
};
```

❌ **Bad:**
```typescript
// No discriminant - can't narrow types
type AsyncData<T> = {
  loading: boolean;
  data?: T;
  error?: Error;
};
```

**Why:** Discriminated unions enable exhaustive type checking and prevent invalid state combinations (e.g., both data and error present).

## Generics

Use generics for reusable type-safe functions and components.

✅ **Good:**
```typescript
// Generic function with constraints
const findById = <T extends { id: string }>(items: T[], id: string): T | undefined => {
  return items.find((item) => item.id === id);
};

// Generic component
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
};

export const List = <T,>({ items, renderItem, keyExtractor }: ListProps<T>) => {
  return (
    <FlatList
      data={items}
      renderItem={({ item }) => renderItem(item)}
      keyExtractor={(item) => keyExtractor(item)}
    />
  );
};
```

❌ **Bad:**
```typescript
// Using any when generics would work
const findById = (items: any[], id: string): any => {
  return items.find((item) => item.id === id);
};
```

**Why:** Generics preserve type information through function calls without duplication or loss of type safety.

## Utility Types

Use TypeScript utility types for type transformations.

**Built-in Utility Types:**
```typescript
// Pick - Select specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit - Exclude specific properties
type UserWithoutPassword = Omit<User, 'password'>;

// Partial - Make all properties optional
type PartialUser = Partial<User>;

// Required - Make all properties required
type RequiredUser = Required<User>;

// Record - Create object type with specific keys
type ErrorMessages = Record<string, string>;

// ReturnType - Extract return type of function
type QueryResult = ReturnType<typeof useRecipeQuery>;

// Parameters - Extract parameter types of function
type FetchParams = Parameters<typeof fetchRecipeDetail>;
```

**Custom Utility Types:**
```typescript
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type Maybe<T> = T | null | undefined;
```

## Strict Null Checks

Handle null/undefined explicitly with optional chaining and nullish coalescing.

✅ **Good:**
```typescript
type User = {
  name: string;
  email: string;
  avatar?: string; // Optional property
};

const getUserAvatar = (user: User): string => {
  return user.avatar ?? 'default-avatar.png';
};

// Use optional chaining
const userName = user?.profile?.name ?? 'Unknown';
```

❌ **Bad:**
```typescript
// Non-null assertion without validation
const userName = user!.profile!.name; // Dangerous if null/undefined
```

**Why:** Strict null checks prevent null/undefined errors at compile time. Optional chaining and nullish coalescing handle undefined gracefully.

## Function Type Annotations

Explicitly type function parameters and return types for public APIs.

✅ **Good:**
```typescript
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

const fetchUser = async (userId: string): Promise<User | null> => {
  try {
    const response = await apiClient.getUser(userId);
    return response.data;
  } catch (error) {
    return null;
  }
};
```

❌ **Bad:**
```typescript
// Implicit return type (not self-documenting)
const calculateTotal = (items: Item[]) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};
```

**Why:** Explicit return types serve as documentation and catch errors where return values don't match expectations.

## Type Guards with Zod

Create type guards using Zod validation for runtime safety.

✅ **Good:**
```typescript
export const isRecipeDetail = (obj: unknown): obj is RecipeDetail => {
  return RecipeDetailSchema.safeParse(obj).success;
};

// Use type guards for validation
const validateRecipe = (data: unknown) => {
  if (isRecipeDetail(data)) {
    // data is now typed as RecipeDetail
    console.log(data.title);
  }
};
```

❌ **Bad:**
```typescript
// Manual type narrowing without validation
const validateRecipe = (data: any) => {
  if (data.title) {
    // Unsafe - no validation
    console.log(data.title);
  }
};
```

**Why:** Zod-based type guards provide both runtime validation and TypeScript type narrowing.

## Common Mistakes

### ❌ Don't Use `any`
```typescript
// ❌ Bad
const processData = (data: any): any => {};

// ✅ Good
const processData = (data: unknown) => {
  if (isValidData(data)) {
    // Type is narrowed
  }
};
```

### ❌ Don't Disable Strict Mode
```json
// ❌ Bad: tsconfig.json
{ "strict": false }

// ✅ Good: tsconfig.json
{ "strict": true }
```

### ❌ Don't Assert Types Without Validation
```typescript
// ❌ Bad
const user = apiResponse as User; // Unsafe

// ✅ Good
const result = UserSchema.safeParse(apiResponse);
if (result.success) {
  const user = result.data; // Safe and typed
}
```

### ❌ Don't Overuse Enums
```typescript
// ❌ Bad
enum Color {
  Red = 'RED',
  Blue = 'BLUE',
}

// ✅ Good
export const COLOR = {
  RED: 'RED',
  BLUE: 'BLUE',
} as const;
export type Color = (typeof COLOR)[keyof typeof COLOR];
```

## Testing

### Runtime Zod Schema Testing
```typescript
describe('RecipeDetailSchema', () => {
  it('should validate valid recipe detail', () => {
    const validRecipe = {
      id: 'recipe-123',
      title: 'Pasta Carbonara',
      heroImageUrl: 'https://example.com/pasta.jpg',
      savedDate: '2025-01-01T12:00:00Z',
      ingredients: [
        { name: 'Pasta', measurement: '500g' },
      ],
    };

    const result = RecipeDetailSchema.safeParse(validRecipe);

    expect(result.success).toBe(true);
  });

  it('should reject invalid URL', () => {
    const invalidRecipe = {
      id: 'recipe-123',
      title: 'Pasta',
      heroImageUrl: 'not-a-url',
      savedDate: '2025-01-01T12:00:00Z',
      ingredients: [],
    };

    const result = RecipeDetailSchema.safeParse(invalidRecipe);
    expect(result.success).toBe(false);
  });
});
```

### Testing Type Guards
```typescript
describe('isRecipeDetail', () => {
  it('should return true for valid data', () => {
    const validData = {
      id: 'recipe-123',
      title: 'Test Recipe',
      heroImageUrl: 'https://example.com/image.jpg',
      savedDate: '2025-01-01T00:00:00Z',
      ingredients: [{ name: 'Test', measurement: '1 cup' }],
    };

    expect(isRecipeDetail(validData)).toBe(true);
  });

  it('should return false for null/undefined', () => {
    expect(isRecipeDetail(null)).toBe(false);
    expect(isRecipeDetail(undefined)).toBe(false);
  });
});
```

## Quick Reference

**Type Decisions:**
- Union types → `type`
- Extendable objects → `interface`
- Constants → `as const` (not enums)
- Unknown data → `unknown` (not `any`)

**Validation:**
- Define Zod schema first
- Infer TypeScript type with `z.infer<>`
- Create type guards with `schema.safeParse()`
- Create parse functions for detailed errors

**Type Safety:**
- Never use `any`
- Enable strict mode
- Explicit function return types
- Optional chaining for null checks
- `import type` for type-only imports

## Additional Resources

For detailed examples and patterns, see:
- [references/examples.md](references/examples.md) - Real Zod schemas and type patterns
- [references/patterns.md](references/patterns.md) - TypeScript patterns and anti-patterns
