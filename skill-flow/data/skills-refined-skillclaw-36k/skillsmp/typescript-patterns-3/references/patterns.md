# TypeScript Patterns

Implementation patterns and anti-patterns for TypeScript type safety.

## Pattern: Zod Schema-First Type Definitions

Define Zod schemas first with validation rules, then infer TypeScript types.

✅ **Good:**
```typescript
import { z } from 'zod';

// 1. Define schema with validation
export const RecipeDetailSchema = z.object({
  id: z.string().min(1, 'Recipe ID cannot be empty').trim(),
  title: z.string().min(1, 'Recipe title cannot be empty').trim(),
  heroImageUrl: z.string().url('Invalid hero image URL'),
  savedDate: z.string().datetime({ offset: true }),
  ingredients: z.array(IngredientSchema).min(1, 'At least one ingredient required'),
});

// 2. Infer type from schema
export type RecipeDetail = z.infer<typeof RecipeDetailSchema>;

// 3. Create type guard
export const isRecipeDetail = (obj: unknown): obj is RecipeDetail => {
  return RecipeDetailSchema.safeParse(obj).success;
};

// 4. Create parse function for detailed errors
export const parseRecipeDetail = (obj: unknown) => {
  return RecipeDetailSchema.safeParse(obj);
};
```

❌ **Bad:**
```typescript
// Defining type and schema separately
type RecipeDetail = {
  id: string;
  title: string;
  heroImageUrl: string;
};

const schema = z.object({
  id: z.string(),
  title: z.string(),
  heroImageUrl: z.string(),
});
```

**Why:** Schema-first ensures runtime validation matches TypeScript types. Single source of truth prevents drift between validation logic and type definitions.

**When to use:**
- API responses that need validation
- User input forms
- External data sources (files, databases)
- Any data from untrusted sources

## Pattern: Type Aliases for Unions and Primitives

Use `type` for unions, primitives, and complex objects that won't be extended.

✅ **Good:**
```typescript
// Union types
export type Action = 'onDecreaseProduct' | 'onRemoveProduct' | 'onSwapCourse';
export type Source = 'LIST' | 'CAROUSEL' | 'WIDGET' | 'POPUP';

// Type aliases
export type ProductId = Scalars['ShoppableProductId']['output'];

// Complex object with no extension
export type TrackingParams = {
  recipePosition?: number;
  widgetName?: string;
  source?: Source;
  screenName?: ScreenName;
};

// Function types
export type TransformFunction<T, U> = (input: T) => U;
export type EventHandler = (event: Event) => void;
```

❌ **Bad:**
```typescript
// Using interface for union types
interface Action {
  type: 'onDecreaseProduct' | 'onRemoveProduct';
}

// Using any for primitives
const productId: any = '123';
```

**Why:** Types are more flexible for unions, primitives, and function types. They support all TypeScript type features (unions, intersections, conditional types).

## Pattern: Interfaces for Extendable Objects

Use `interface` for object shapes that may be extended by other code.

✅ **Good:**
```typescript
// Base interface
export interface UserProfileProps {
  userId: string;
  onEdit: () => void;
}

// Extended interface
export interface AdminProfileProps extends UserProfileProps {
  permissions: string[];
  onDelete: () => void;
}

// Class implementing interface
export class UserProfile implements UserProfileProps {
  constructor(
    public userId: string,
    public onEdit: () => void
  ) {}
}
```

❌ **Bad:**
```typescript
// Using type when extension is needed
export type UserProfileProps = {
  userId: string;
  onEdit: () => void;
};

// Can't extend types the same way
export type AdminProfileProps = UserProfileProps & {
  permissions: string[];
};
```

**Why:** Interfaces support declaration merging and provide better error messages for objects. They're the idiomatic choice for object shapes in TypeScript.

**When to use interface:**
- Component props that may be extended
- Class contracts
- Public APIs that consumers might extend
- Objects with methods

## Pattern: Const Assertions Over Enums

Use `as const` for immutable constant objects instead of enums.

✅ **Good:**
```typescript
// Const assertion
export const SCREEN_NAME = {
  HOME: 'Home',
  STORE: 'Store',
  UPSELL: 'Upsell',
} as const;

// Derive type from const
export type ScreenName = (typeof SCREEN_NAME)[keyof typeof SCREEN_NAME];

// Usage
const navigate = (screen: ScreenName) => {
  // screen can only be 'Home' | 'Store' | 'Upsell'
};

navigate(SCREEN_NAME.HOME); // ✓ Type-safe
```

❌ **Bad:**
```typescript
// Plain object without 'as const'
export const SCREEN_NAME = {
  HOME: 'Home', // Type is string, not literal 'Home'
};

// Enum (generates runtime code)
export enum ScreenName {
  Home = 'Home',
  Store = 'Store',
}
```

**Why:** `as const` creates readonly literal types with better type inference. No runtime code generated. Better tree-shaking than enums.

**When to still use enums:**
- You need reverse mapping (get key from value)
- You need to iterate over all enum values
- Sequential numeric values with meaning

## Pattern: Discriminated Unions for State Machines

Use discriminated unions with a `status` or `type` field for state machines.

✅ **Good:**
```typescript
// Discriminated union with status field
type AsyncData<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// TypeScript narrows types automatically
const renderData = (state: AsyncData<Recipe>) => {
  switch (state.status) {
    case 'idle':
      return null;
    case 'loading':
      return <LoadingSpinner />;
    case 'success':
      // state.data is accessible here (type Recipe)
      return <RecipeList recipes={state.data} />;
    case 'error':
      // state.error is accessible here (type Error)
      return <ErrorMessage error={state.error} />;
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

// Manual checks, no type narrowing
const renderData = (state: AsyncData<Recipe>) => {
  if (state.loading) return <LoadingSpinner />;
  if (state.error) return <ErrorMessage error={state.error} />;
  // state.data might be undefined - no type safety
  return <RecipeList recipes={state.data} />;
};
```

**Why:** Discriminated unions:
- Enable exhaustive type checking (TypeScript ensures all cases are handled)
- Prevent invalid state combinations (e.g., both data and error present)
- Provide automatic type narrowing based on discriminant field

**Common discriminant fields:**
- `status`: 'idle' | 'loading' | 'success' | 'error'
- `type`: 'fetch' | 'update' | 'delete'
- `kind`: 'user' | 'admin' | 'guest'

## Pattern: Action Types with Discriminated Unions

Use discriminated unions for action types in reducers.

✅ **Good:**
```typescript
type RecipeAction =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Recipe[] }
  | { type: 'FETCH_ERROR'; error: string }
  | { type: 'ADD_RECIPE'; payload: Recipe }
  | { type: 'DELETE_RECIPE'; recipeId: string };

const recipeReducer = (state: RecipeState, action: RecipeAction): RecipeState => {
  switch (action.type) {
    case 'FETCH_SUCCESS':
      // action.payload is typed as Recipe[]
      return { ...state, recipes: action.payload };
    case 'ADD_RECIPE':
      // action.payload is typed as Recipe
      return { ...state, recipes: [...state.recipes, action.payload] };
    case 'DELETE_RECIPE':
      // action.recipeId is typed as string
      return {
        ...state,
        recipes: state.recipes.filter((r) => r.id !== action.recipeId),
      };
    default:
      return state;
  }
};
```

❌ **Bad:**
```typescript
// Loose action type - no payload type safety
type RecipeAction = {
  type: string;
  payload?: any;
};

const recipeReducer = (state: RecipeState, action: RecipeAction) => {
  switch (action.type) {
    case 'FETCH_SUCCESS':
      // action.payload could be anything - no type safety
      return { ...state, recipes: action.payload };
  }
};
```

**Why:** Discriminated union actions ensure payload types match action types. TypeScript catches mismatches at compile time.

## Pattern: Generics for Reusable Type-Safe Functions

Use generics to preserve type information through function calls.

✅ **Good:**
```typescript
// Generic with constraint
const findById = <T extends { id: string }>(
  items: T[],
  id: string
): T | undefined => {
  return items.find((item) => item.id === id);
};

// Usage - type is preserved
const recipes: Recipe[] = [...];
const recipe = findById(recipes, '123'); // Type: Recipe | undefined

const users: User[] = [...];
const user = findById(users, '456'); // Type: User | undefined

// Generic with multiple type parameters
const mapArray = <T, U>(items: T[], mapper: (item: T) => U): U[] => {
  return items.map(mapper);
};

// Usage
const ids = mapArray(recipes, (recipe) => recipe.id); // Type: string[]
```

❌ **Bad:**
```typescript
// Using any - loses type information
const findById = (items: any[], id: string): any => {
  return items.find((item) => item.id === id);
};

// No type safety
const recipe = findById(recipes, '123'); // Type: any
```

**Why:** Generics maintain type safety while allowing code reuse. TypeScript infers types at call site, providing autocomplete and type checking.

## Pattern: Generic Components

Use generics for reusable React components that work with any data type.

✅ **Good:**
```typescript
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
};

export const List = <T,>({
  items,
  renderItem,
  keyExtractor,
}: ListProps<T>) => {
  return (
    <FlatList
      data={items}
      renderItem={({ item }) => renderItem(item)}
      keyExtractor={(item) => keyExtractor(item)}
    />
  );
};

// Usage - types are inferred
<List
  items={recipes} // T inferred as Recipe
  renderItem={(recipe) => <RecipeCard recipe={recipe} />}
  keyExtractor={(recipe) => recipe.id}
/>
```

❌ **Bad:**
```typescript
// Non-generic component - limited to one type
type ListProps = {
  items: Recipe[];
  renderItem: (item: Recipe) => ReactNode;
  keyExtractor: (item: Recipe) => string;
};

// Need duplicate components for each type
type UserListProps = {
  items: User[];
  renderItem: (item: User) => ReactNode;
  keyExtractor: (item: User) => string;
};
```

**Why:** Generic components eliminate duplication while maintaining type safety. TypeScript infers the type parameter from the `items` prop.

**Note:** The trailing comma in `<T,>` is required for JSX to distinguish generic syntax from JSX tags.

## Pattern: Utility Types for Transformations

Use TypeScript utility types for type transformations.

✅ **Good:**
```typescript
// Pick specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit specific properties
type UserWithoutPassword = Omit<User, 'password'>;

// Make all properties optional
type PartialUser = Partial<User>;

// Make all properties required
type RequiredConfig = Required<Config>;

// Create object with specific keys
type ErrorMessages = Record<string, string>;
type StatusMap = Record<Status, boolean>;

// Extract return type
type QueryResult = ReturnType<typeof useRecipeQuery>;

// Extract parameter types
type FetchParams = Parameters<typeof fetchRecipeDetail>;

// Custom utility type
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type Maybe<T> = T | null | undefined;
```

❌ **Bad:**
```typescript
// Duplicating type definitions
type UserCredentials = {
  email: string;
  password: string;
};

type UserWithoutPassword = {
  id: string;
  email: string;
  name: string;
  // Missing password property - manual duplication
};
```

**Why:** Utility types prevent duplication and automatically update when source types change. They're part of TypeScript's standard library.

## Pattern: Type Guards with Zod

Create type guards using Zod schema validation.

✅ **Good:**
```typescript
// Type guard using Zod
export const isRecipeDetail = (obj: unknown): obj is RecipeDetail => {
  return RecipeDetailSchema.safeParse(obj).success;
};

// Usage in function
const processRecipe = (data: unknown) => {
  if (isRecipeDetail(data)) {
    // data is now typed as RecipeDetail
    console.log(data.title);
    console.log(data.ingredients);
  } else {
    throw new Error('Invalid recipe data');
  }
};

// Usage in component
const RecipeScreen = ({ data }: { data: unknown }) => {
  if (!isRecipeDetail(data)) {
    return <ErrorScreen />;
  }

  // data is guaranteed to be RecipeDetail
  return <RecipeDisplay recipe={data} />;
};
```

❌ **Bad:**
```typescript
// Manual type narrowing without validation
const processRecipe = (data: any) => {
  if (data.title && data.ingredients) {
    // Unsafe - no actual validation
    console.log(data.title);
  }
};

// Type assertion without validation
const processRecipe = (data: unknown) => {
  const recipe = data as RecipeDetail; // Dangerous
  console.log(recipe.title); // Could crash if data is invalid
};
```

**Why:** Zod-based type guards provide:
- Runtime validation (catches invalid data)
- TypeScript type narrowing (type safety after guard)
- Detailed error messages (when validation fails)

## Pattern: Parse Functions for Detailed Errors

Export parse functions that return detailed validation errors.

✅ **Good:**
```typescript
export const parseRecipeDetail = (obj: unknown) => {
  return RecipeDetailSchema.safeParse(obj);
};

// Usage with detailed error handling
const result = parseRecipeDetail(apiResponse);

if (result.success) {
  const recipe = result.data; // Typed as RecipeDetail
  console.log('Valid recipe:', recipe.title);
} else {
  // Access detailed error information
  console.error('Validation errors:', result.error.errors);

  // Log field-specific errors
  result.error.errors.forEach((err) => {
    console.error(`Field ${err.path.join('.')}: ${err.message}`);
  });

  // Send to error tracking
  trackValidationError({
    schema: 'RecipeDetail',
    errors: result.error.format(),
  });
}
```

❌ **Bad:**
```typescript
// Using .parse() which throws
export const parseRecipeDetail = (obj: unknown): RecipeDetail => {
  return RecipeDetailSchema.parse(obj); // Throws on error
};

// Can't handle errors gracefully
try {
  const recipe = parseRecipeDetail(apiResponse);
} catch (error) {
  // Limited error information
  console.error('Validation failed:', error);
}
```

**Why:** `safeParse()` returns a result object with either `success: true, data: T` or `success: false, error: ZodError`. This allows detailed error handling without try/catch.

## Pattern: Strict Null Checks with Optional Chaining

Handle null/undefined explicitly using optional chaining and nullish coalescing.

✅ **Good:**
```typescript
type User = {
  name: string;
  email: string;
  avatar?: string; // Optional property
  profile?: {
    bio?: string;
  };
};

// Nullish coalescing for defaults
const getUserAvatar = (user: User): string => {
  return user.avatar ?? 'default-avatar.png';
};

// Optional chaining for nested properties
const userName = user?.profile?.bio ?? 'No bio';

// Type guard for nullable types
const displayName = (user: User | null): string => {
  if (user === null) {
    return 'Guest';
  }
  return user.name;
};
```

❌ **Bad:**
```typescript
// Non-null assertion without validation
const userName = user!.profile!.bio; // Crashes if null/undefined

// Truthy checks (wrong for empty strings, 0, false)
const avatar = user.avatar || 'default-avatar.png'; // Wrong for ''

// Manual null checks (verbose)
const userName = user && user.profile && user.profile.bio
  ? user.profile.bio
  : 'No bio';
```

**Why:**
- Optional chaining (`?.`) safely accesses nested properties
- Nullish coalescing (`??`) only checks for null/undefined (not falsy values)
- Type guards provide explicit null checking

## Pattern: Explicit Function Return Types

Always specify return types for public APIs and exported functions.

✅ **Good:**
```typescript
// Explicit return type
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// Async function with Promise
const fetchUser = async (userId: string): Promise<User | null> => {
  try {
    const response = await apiClient.getUser(userId);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
};

// Void return type
const logMessage = (message: string): void => {
  console.log(message);
};
```

❌ **Bad:**
```typescript
// Implicit return type (not self-documenting)
const calculateTotal = (items: Item[]) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// Can accidentally return wrong type
const fetchUser = async (userId: string) => {
  const response = await apiClient.getUser(userId);
  return response; // Oops - returned Response instead of User
};
```

**Why:** Explicit return types:
- Serve as documentation (readers know what function returns)
- Catch errors where implementation doesn't match intent
- Enable better IDE autocomplete
- Make refactoring safer

**Exception:** Implicit return types are OK for:
- Private helper functions (not exported)
- Callbacks where type is inferred from context
- One-liners where return type is obvious

## Anti-Pattern: Using `any`

Never use `any` type. Use `unknown` with type guards or generics instead.

❌ **Bad:**
```typescript
// any disables all type checking
const processData = (data: any): any => {
  return data.value; // No type safety, no autocomplete
};

// Function signatures with any
const handleEvent = (event: any) => {
  event.preventDefault(); // Could crash if event has no preventDefault
};

// any in type definitions
type Config = {
  settings: any; // Loses all type information
};
```

✅ **Good:**
```typescript
// Use unknown with type guards
const processData = (data: unknown) => {
  if (isValidData(data)) {
    return data.value; // Type-safe after guard
  }
  throw new Error('Invalid data');
};

// Use specific event types
const handleEvent = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault(); // Type-safe
};

// Use generic types
type Config<T> = {
  settings: T;
};
```

**Why:** `any`:
- Disables all type checking (defeats purpose of TypeScript)
- Prevents IDE autocomplete and refactoring
- Allows runtime errors that TypeScript should catch
- Spreads through codebase ("contagious any")

**Alternative:** Use `unknown` which requires explicit type narrowing, forcing you to validate data.

## Anti-Pattern: Type Assertions Without Validation

Don't use type assertions (`as`) without runtime validation.

❌ **Bad:**
```typescript
// Unsafe type assertion
const user = apiResponse as User;
console.log(user.name); // Could crash if apiResponse is invalid

// Double assertion (even more dangerous)
const data = unknownData as any as SpecificType;

// Non-null assertion without check
const firstName = user!.profile!.firstName!;
```

✅ **Good:**
```typescript
// Validate with Zod schema
const result = UserSchema.safeParse(apiResponse);
if (result.success) {
  const user = result.data; // Safe and typed
  console.log(user.name);
}

// Use type guard
if (isUser(apiResponse)) {
  const user = apiResponse; // Type narrowed safely
  console.log(user.name);
}

// Check for null before accessing
if (user?.profile?.firstName) {
  console.log(user.profile.firstName);
}
```

**Why:** Type assertions tell TypeScript "trust me, I know better" without checking. If the data doesn't match the asserted type, you get runtime errors.

**When assertions are OK:**
- Narrowing types you just validated
- Working with DOM types (`event.target as HTMLInputElement`)
- `as const` assertions (readonly literals)

## Anti-Pattern: Disabling Strict Mode

Never disable TypeScript strict mode.

❌ **Bad:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": false,
    "strictNullChecks": false
  }
}
```

✅ **Good:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Why:** Strict mode enables critical checks:
- `noImplicitAny`: Prevents implicit any types
- `strictNullChecks`: Catches null/undefined errors
- `strictFunctionTypes`: Ensures function type safety
- `strictPropertyInitialization`: Requires class property initialization

## Anti-Pattern: Overusing Enums

Don't use enums for simple string unions. Use const assertions instead.

❌ **Bad:**
```typescript
// Enum generates runtime code
enum Color {
  Red = 'RED',
  Blue = 'BLUE',
  Green = 'GREEN',
}

// Numeric enums (confusing values)
enum Status {
  Active, // 0
  Inactive, // 1
}
```

✅ **Good:**
```typescript
// Const assertion (no runtime code)
export const COLOR = {
  RED: 'RED',
  BLUE: 'BLUE',
  GREEN: 'GREEN',
} as const;

export type Color = (typeof COLOR)[keyof typeof COLOR];

// Usage is identical
const myColor: Color = COLOR.RED;
```

**Why:** Const assertions:
- Generate no runtime code (better tree-shaking)
- Provide same type safety as enums
- Support better type inference
- Are more flexible (can be used in template literals)

**When to use enums:**
- You need reverse mapping (value → key)
- You need to iterate over all values
- Sequential numeric values have meaning

## Summary

**Type System Choices:**
- `type` for unions, primitives, complex objects
- `interface` for extendable objects, class contracts
- `as const` for constants (not enums)
- `unknown` for unknown data (not `any`)

**Zod Patterns:**
- Define schema first with validation rules
- Infer types with `z.infer<typeof Schema>`
- Create type guards with `.safeParse()`
- Export parse functions for detailed errors

**Type Safety:**
- Never use `any`
- Keep strict mode enabled
- Explicit function return types
- Optional chaining for null checks
- Type assertions only after validation

**Advanced Patterns:**
- Discriminated unions for state machines
- Generics for reusable type-safe code
- Utility types for transformations
- Type guards with runtime validation
