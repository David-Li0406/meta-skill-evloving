# TypeScript Patterns Examples

Real-world TypeScript patterns from the YourCompany shared-mobile-modules project.

## Zod Schema-First Type Definitions

From `src/data-access/query/external-recipes/types.ts`:

### Basic Zod Schemas with Validation

```typescript
import { z } from 'zod';

/**
 * Ingredient schema for external recipes (backend-aligned)
 */
export const IngredientSchema = z.object({
  /** Name of the ingredient */
  name: z.string().min(1, 'Ingredient name cannot be empty').trim(),
  /** Quantity of the ingredient */
  quantity: z
    .string()
    .optional()
    .transform((val) => val ?? null),
  /** Unit of measurement for the ingredient */
  unit: z
    .string()
    .optional()
    .transform((val) => val ?? null),
});

/**
 * Cooking step schema for external recipes (backend-aligned)
 */
export const StepSchema = z.object({
  /** Index/step number (0-based) */
  index: z.number().int().min(0, 'Step index must be non-negative'),
  /** Instructions for this step */
  instructions: z.string().min(1, 'Instructions cannot be empty').trim(),
});
```

**Key patterns:**
- JSDoc comments above each schema
- Field-level JSDoc comments for IDE tooltips
- Validation rules: `.min()`, `.trim()`, `.int()`, `.url()`, `.datetime()`
- Transforms: `.transform((val) => val ?? null)` for optional → nullable
- Defaults: `.default([])`, `.default(false)`

### Enum with Zod

```typescript
export const SourcePlatformSchema = z.enum([
  'instagram',
  'pinterest',
  'youtube',
  'tiktok',
  'unsupported',
]);

export type SourcePlatform = z.infer<typeof SourcePlatformSchema>;
```

**Pattern:** Use `z.enum()` for string unions, then infer the TypeScript type.

### Complex Nested Schema

```typescript
/**
 * External Recipe schema for backend API validation
 */
export const ExternalRecipeSchema = z.object({
  /** Unique identifier for the external recipe */
  id: z.string().min(1, 'Recipe ID cannot be empty').trim(),
  /** Owner ID of the recipe */
  owner_id: z.string().min(1, 'Owner ID cannot be empty').trim(),
  /** Owner type of the recipe */
  owner_type: z.string().min(1, 'Owner type cannot be empty').trim(),
  /** Original URL of the recipe from social media platform */
  url: z.string().url('Invalid recipe URL'),
  /** Title of the recipe */
  title: z.string().min(1, 'Recipe title cannot be empty').trim(),
  /** Headline of the recipe */
  headline: z
    .string()
    .min(1, 'Recipe headline cannot be empty')
    .trim()
    .optional(),
  /** URL of the recipe thumbnail image */
  thumbnail_url: z.string().url('Invalid thumbnail URL').optional(),
  /** Recipe description (if available) */
  description: z.string().trim().optional(),
  /** List of recipe ingredients */
  ingredients: z.array(IngredientSchema).default([]),
  /** List of cooking steps */
  steps: z.array(StepSchema).default([]),
  /** Whether the recipe has been extracted and has detailed information */
  has_recipe_extracted: z.boolean().default(false),
  /** Source platform of the recipe */
  source_platform: SourcePlatformSchema.default('unsupported'),
  /** ISO 8601 timestamp when the recipe was created */
  created_at: z.string().datetime({ offset: true }),
  /** ISO 8601 timestamp when the recipe was last updated */
  updated_at: z.string().datetime({ offset: true }),
});
```

**Key patterns:**
- Nested schemas: `z.array(IngredientSchema)`
- Optional fields: `.optional()` after validation
- URL validation: `z.string().url('Invalid recipe URL')`
- Datetime validation: `z.string().datetime({ offset: true })`
- Defaults: `.default([])`, `.default(false)`, `.default('unsupported')`

### Pagination Schema

```typescript
export const PaginationMetaSchema = z.object({
  /** Limit of the recipes per page */
  limit: z.number().int().min(1, 'Limit must be positive'),
  /** Cursor token for the next page of results */
  next_cursor: z.string().optional(),
  /** Whether there are more results available */
  has_more: z.boolean(),
});

export const GetExternalRecipesResponseSchema = z.object({
  data: z.array(ExternalRecipeListItemBackendSchema).optional().default([]),
  pagination: PaginationMetaSchema,
});
```

**Pattern:** Compose smaller schemas into larger ones for API responses.

## Type Inference from Zod Schemas

```typescript
// Infer types from schemas
export type Ingredient = z.infer<typeof IngredientSchema>;
export type Step = z.infer<typeof StepSchema>;
export type SourcePlatform = z.infer<typeof SourcePlatformSchema>;
export type ExternalRecipe = z.infer<typeof ExternalRecipeSchema>;
export type ExternalRecipeListItem = z.infer<typeof ExternalRecipeListItemBackendSchema>;
export type GetExternalRecipesResponse = z.infer<typeof GetExternalRecipesResponseSchema>;
```

**Pattern:** Use `z.infer<typeof Schema>` to derive TypeScript types from Zod schemas. Single source of truth.

## Validation Functions

```typescript
/**
 * Validates and parses an ExternalRecipe from unknown data
 */
export const validateExternalRecipe = (data: unknown): ExternalRecipe => {
  return ExternalRecipeSchema.parse(data);
};

/**
 * Validates backend data and returns frontend format
 * This is the main function components should use
 */
export const validateExternalRecipeListItem = (
  data: unknown
): ExternalRecipeListItem => {
  // Validate against backend schema first
  return ExternalRecipeListItemBackendSchema.parse(data);
};

/**
 * Validates and transforms an array of ExternalRecipeListItems from backend data
 */
export const validateExternalRecipeListItems = (
  data: unknown
): ExternalRecipeListItem[] => {
  return z.array(ExternalRecipeListItemBackendSchema).parse(data);
};

export const validateGetExternalRecipesResponse = (
  data: unknown
): GetExternalRecipesResponse => {
  return GetExternalRecipesResponseSchema.parse(data);
};
```

**Pattern:** Export validation functions that accept `unknown` and return typed data or throw on validation errors.

## Error Schema

```typescript
/**
 * Error response schema from backend validation
 */
export const UpdateExternalRecipeErrorSchema = z.object({
  /** General error message */
  message: z.string(),
  /** Field-specific validation errors */
  errors: z.record(z.string(), z.array(z.string())).optional(),
});

export type UpdateExternalRecipeError = z.infer<
  typeof UpdateExternalRecipeErrorSchema
>;
```

**Pattern:** Define error schemas for API error responses. `z.record()` for dynamic keys with typed values.

## Non-Zod Types for Request/Response

```typescript
/**
 * Pagination metadata for paginated responses
 */
export interface Pagination {
  /** Limit of the recipes per page */
  limit: number;
  /** Cursor token for the next page of results */
  next_cursor?: string;
  /** Whether there are more results available */
  has_more: boolean;
}

// CREATE External Recipe API Types
export interface CreateExternalRecipeRequest {
  /** Original URL of the recipe from social media platform */
  url: string;
  /** Title of the recipe */
  title?: string;
  /** URL of the recipe thumbnail image */
  thumbnail_url?: string;
}

// GET External Recipes API Types
export interface GetExternalRecipesRequest {
  /** Search query string */
  search?: string;
  /** Cursor token for pagination (optional for first page) */
  cursor?: string;
  /** Number of recipes to return per page (default: 20, max: 100) */
  limit?: number;
}

// DELETE External Recipe API Types
export interface DeleteExternalRecipeRequest {
  /** ID of the external recipe to delete */
  id: string;
}

export interface DeleteExternalRecipeResponse {
  /** Whether the deletion was successful */
  success: boolean;
}
```

**Pattern:** Use interfaces for simple request/response types that don't need runtime validation. Zod schemas for responses that need validation.

## Type Aliases for Unions

From navigation and analytics types:

```typescript
// Type aliases for string literals
export type ProductId = Scalars['ShoppableProductId']['output'];
export type Action = 'onDecreaseProduct' | 'onRemoveProduct' | 'onSwapCourse';
export type Source = 'LIST' | 'CAROUSEL' | 'WIDGET' | 'POPUP';

// Type alias for complex object (no extension needed)
export type TrackingParams = {
  recipePosition?: number;
  widgetName?: string;
  source?: Source;
  topLayer?: TopLayer;
  screenName?: ScreenName;
};
```

**Pattern:** Use `type` for unions, primitives, and complex objects that won't be extended.

## Const Assertions

From analytics constants:

```typescript
export const SCREEN_NAME = {
  HOME: 'Home',
  STORE: 'Store',
  UPSELL: 'Upsell',
  PROMOTION: 'Promotion',
} as const;

export const SOURCE = {
  LIST: 'LIST',
  CAROUSEL: 'CAROUSEL',
  WIDGET: 'WIDGET',
  POPUP: 'POPUP',
} as const;

// Derive types from const
export type ScreenName = (typeof SCREEN_NAME)[keyof typeof SCREEN_NAME];
export type Source = (typeof SOURCE)[keyof typeof SOURCE];
```

**Pattern:** Use `as const` for immutable constant objects, then derive union types with `typeof` and `keyof`.

## String Enums

From navigation routing:

```typescript
export enum SocialRecipeBridgeStackRoutes {
  SocialRecipeBridge = 'SocialRecipeBridge',
  CookbookFaq = 'CookbookFaq',
  RecipeDetail = 'RecipeDetail',
  AddRecipeLinkDrawer = 'AddRecipeLinkDrawer',
}

export enum Status {
  Active = 'ACTIVE',
  Inactive = 'INACTIVE',
  Pending = 'PENDING',
}
```

**Pattern:** Use string enums only when you need reverse mapping or iteration. Prefer const assertions for most cases.

## Discriminated Unions

State machine pattern:

```typescript
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
      return <RecipeList recipes={state.data} />; // state.data is Recipe
    case 'error':
      return <ErrorMessage error={state.error} />; // state.error is Error
  }
};
```

**Pattern:** Use discriminated unions with `status` field for state machines. Exhaustive type checking in switch statements.

## Action Types

```typescript
type RecipeAction =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Recipe[] }
  | { type: 'FETCH_ERROR'; error: string }
  | { type: 'ADD_RECIPE'; payload: Recipe }
  | { type: 'DELETE_RECIPE'; recipeId: string };

const recipeReducer = (state: RecipeState, action: RecipeAction) => {
  switch (action.type) {
    case 'FETCH_SUCCESS':
      return { ...state, recipes: action.payload }; // payload is Recipe[]
    case 'ADD_RECIPE':
      return { ...state, recipes: [...state.recipes, action.payload] };
    case 'DELETE_RECIPE':
      return {
        ...state,
        recipes: state.recipes.filter((r) => r.id !== action.recipeId),
      };
    default:
      return state;
  }
};
```

**Pattern:** Discriminated unions ensure action payloads match action types in reducers.

## Generic Functions

```typescript
// Generic with constraint
const findById = <T extends { id: string }>(items: T[], id: string): T | undefined => {
  return items.find((item) => item.id === id);
};

// Generic query key creator
const createQueryKey = <T extends string>(domain: string, id: T): [string, T] => {
  return [domain, id];
};

// Usage
const key = createQueryKey('recipes', '123'); // Type: [string, '123']
const recipe = findById(recipes, 'recipe-123'); // Type: Recipe | undefined
```

**Pattern:** Generics preserve type information through function calls without duplication.

## Generic Components

```typescript
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

// Usage - types are inferred
<List
  items={recipes}
  renderItem={(recipe) => <RecipeCard recipe={recipe} />}
  keyExtractor={(recipe) => recipe.id}
/>
```

**Pattern:** Generic components work with any data type while maintaining type safety.

## Utility Types

```typescript
// Built-in utility types
type UserCredentials = Pick<User, 'email' | 'password'>;
type UserWithoutPassword = Omit<User, 'password'>;
type PartialUser = Partial<User>;
type RequiredUser = Required<User>;
type ErrorMessages = Record<string, string>;
type QueryResult = ReturnType<typeof useRecipeQuery>;
type FetchParams = Parameters<typeof fetchRecipeDetail>;

// Custom utility types
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type Maybe<T> = T | null | undefined;
```

**Pattern:** Use built-in utility types for common transformations. Define custom utilities for project-specific patterns.

## Type-Safe Component Props

```typescript
// src/features/recipe-card/RecipeCard.tsx
import type { Recipe } from '@modules/social-recipe-bridge/types';

import { Button, Text, useZestStyles } from '@zest/react-native';

interface RecipeCardProps {
  recipe: Recipe;
  onPress?: (recipeId: string) => void;
  testID?: string;
}

export const RecipeCard = ({ recipe, onPress, testID }: RecipeCardProps) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <Button
      variant="tertiary"
      onPress={() => onPress?.(recipe.id)}
      testID={testID}
    >
      <Text type="headline-md">{recipe.title}</Text>
      <Text type="body-sm">{recipe.author.name}</Text>
    </Button>
  );
};
```

**Pattern:** Interface for component props, type imports with `import type`, optional callbacks with `?.()`.

## Schema Validation in Components

```typescript
// src/modules/social-recipe-bridge/screens/recipe-detail/RecipeDetail.tsx
import { useEffect } from 'react';
import { View } from 'react-native';

import { useRecipeDetail } from '@data-access/query';

import { Text } from '@zest/react-native';

import { isRecipeDetail } from '../../types';
import type { RecipeDetail } from '../../types';

interface RecipeDetailScreenProps {
  recipeId: string;
}

export const RecipeDetailScreen = ({ recipeId }: RecipeDetailScreenProps) => {
  const { data, isLoading, error } = useRecipeDetail(recipeId);

  useEffect(() => {
    // Validate data at runtime using Zod type guard
    if (data && !isRecipeDetail(data)) {
      console.error('Invalid recipe data received:', data);
    }
  }, [data]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data || !isRecipeDetail(data)) return <DataValidationError />;

  // data is now guaranteed to be RecipeDetail type
  return (
    <View>
      <Text type="headline-lg">{data.title}</Text>
      <RecipeIngredients ingredients={data.ingredients} />
      <CookingSteps steps={data.cookingSteps} />
    </View>
  );
};
```

**Pattern:** Runtime validation with type guards before rendering. Ensures data conforms to expected types.

## Generic Hook with Zod

```typescript
// src/libs/api/useValidatedQuery.ts
import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
import type { z } from 'zod';

export const useValidatedQuery = <TSchema extends z.ZodType>(
  queryKey: string[],
  fetcher: () => Promise<unknown>,
  schema: TSchema,
  options?: UseQueryOptions<z.infer<TSchema>>
) => {
  return useQuery({
    queryKey,
    queryFn: async () => {
      const data = await fetcher();
      const result = schema.safeParse(data);

      if (!result.success) {
        throw new Error(`Validation failed: ${result.error.message}`);
      }

      return result.data;
    },
    ...options,
  });
};

// Usage
const { data } = useValidatedQuery(
  ['recipe', recipeId],
  () => fetchRecipe(recipeId),
  RecipeDetailSchema
); // data is typed as RecipeDetail
```

**Pattern:** Generic hooks with Zod validation provide type-safe, validated data access.

## Type Guards with Zod

```typescript
// Create type guard using Zod validation
export const isRecipeDetail = (obj: unknown): obj is RecipeDetail => {
  return RecipeDetailSchema.safeParse(obj).success;
};

export const isRecipeListItem = (obj: unknown): obj is RecipeListItem => {
  return RecipeListItemSchema.safeParse(obj).success;
};

// Use type guards for runtime validation
const validateRecipe = (data: unknown) => {
  if (isRecipeDetail(data)) {
    // data is now typed as RecipeDetail
    console.log(data.title);
    console.log(data.ingredients);
  }
};
```

**Pattern:** Zod-based type guards provide both runtime validation and TypeScript type narrowing.

## Parse Functions for Detailed Errors

```typescript
// Export parse functions for detailed error information
export const parseRecipeListItem = (obj: unknown) => {
  return RecipeListItemSchema.safeParse(obj);
};

export const parseRecipeDetail = (obj: unknown) => {
  return RecipeDetailSchema.safeParse(obj);
};

// Usage - get detailed error information
const result = parseRecipeDetail(apiResponse);
if (result.success) {
  const recipe = result.data; // Typed as RecipeDetail
  console.log('Valid recipe:', recipe.title);
} else {
  console.error('Validation errors:', result.error.errors);
  // Log field-specific errors for debugging
  result.error.errors.forEach((err) => {
    console.error(`Field ${err.path.join('.')}: ${err.message}`);
  });
}
```

**Pattern:** Parse functions with `safeParse()` return detailed error information for debugging validation failures.

## Strict Null Checks

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

// Type guards for nullable values
const displayName = (user: User | null) => {
  if (user === null) {
    return 'Guest';
  }
  return user.name;
};
```

**Pattern:** Optional chaining (`?.`), nullish coalescing (`??`), and type guards for null/undefined handling.

## Function Type Annotations

```typescript
// Explicit return types for public APIs
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// Async functions with Promise
const fetchUser = async (userId: string): Promise<User | null> => {
  try {
    const response = await apiClient.getUser(userId);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
};

// Function type alias
type TransformFunction<T, U> = (input: T) => U;

const transform: TransformFunction<Recipe, RecipeListItem> = (recipe) => {
  return {
    id: recipe.id,
    title: recipe.title,
    heroImageUrl: recipe.heroImageUrl,
  };
};
```

**Pattern:** Explicit return types serve as documentation and catch mismatches between expected and actual return values.

## JSDoc with Types

```typescript
/**
 * Lightweight recipe schema for recipe list display
 * Contains minimal data needed for list rendering and navigation decisions
 */
export type RecipeListItem = {
  /** Unique identifier for the recipe */
  id: string;
  /** Display title of the recipe */
  title: string;
  /** URL to the hero/thumbnail image */
  heroImageUrl: string;
  /** Whether this recipe has detailed information available */
  hasDetail: boolean;
};

/**
 * Validates if an object is a valid RecipeListItem using Zod schema
 * @param obj - Unknown object to validate
 * @returns Type guard result
 */
export const isRecipeListItem = (obj: unknown): obj is RecipeListItem => {
  return RecipeListItemSchema.safeParse(obj).success;
};
```

**Pattern:** JSDoc comments provide documentation that appears in IDE tooltips and generated docs.
