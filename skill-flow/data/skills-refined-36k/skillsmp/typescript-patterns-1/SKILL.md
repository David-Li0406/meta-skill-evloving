---
name: typescript-patterns
description: TypeScript patterns and best practices for Next.js projects. Use when writing TypeScript code, defining types, handling errors, or ensuring type safety in components, API routes, or utilities.
---

# TypeScript Patterns for Next.js

## Type Definitions

### Component Props

```tsx
// ✅ Explicit interface
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export default function Button({ label, onClick, variant = 'primary', disabled }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
}

// ✅ Using Readonly for props
interface PageProps {
  params: Readonly<{ slug: string }>;
  searchParams: Readonly<{ [key: string]: string | string[] | undefined }>;
}
```

### API Response Types

```tsx
// ✅ Define API response types
interface ApiResponse<T> {
  data: T;
  error?: string;
  status: number;
}

interface Product {
  id: string;
  name: string;
  price: number;
  description?: string;
}

type ProductsResponse = ApiResponse<Product[]>;
```

## Error Handling

### Custom Error Classes

```tsx
// lib/errors.ts
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### Type-Safe Error Handling

```tsx
// ✅ Result type pattern
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchProduct(id: string): Promise<Result<Product, ApiError>> {
  try {
    const response = await fetch(`/api/products/${id}`);
    if (!response.ok) {
      return { 
        success: false, 
        error: new ApiError('Failed to fetch', response.status) 
      };
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error : new Error('Unknown error') 
    };
  }
}

// Usage
const result = await fetchProduct('123');
if (result.success) {
  console.log(result.data.name); // TypeScript knows data exists
} else {
  console.error(result.error.message); // TypeScript knows error exists
}
```

## Utility Types

### Common Helpers

```tsx
// ✅ Extract types from functions
type GetProductsResponse = Awaited<ReturnType<typeof getProducts>>;

// ✅ Make specific fields optional
type PartialProduct = Partial<Product>;

// ✅ Make specific fields required
type RequiredProduct = Required<Product>;

// ✅ Pick specific fields
type ProductPreview = Pick<Product, 'id' | 'name' | 'price'>;

// ✅ Omit specific fields
type CreateProductInput = Omit<Product, 'id' | 'createdAt'>;

// ✅ Extract array element type
type ProductArray = Product[];
type ProductItem = ProductArray[number];
```

## Next.js Specific Types

### Route Parameters

```tsx
// ✅ Type-safe route params
interface PageProps {
  params: {
    slug: string;
    id: string;
  };
  searchParams: {
    page?: string;
    filter?: string;
  };
}

export default function Page({ params, searchParams }: PageProps) {
  // params and searchParams are typed
}
```

### Metadata Types

```tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};

// ✅ Dynamic metadata with type safety
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

## Form Data Types

### Server Actions

```tsx
'use server';

interface CreatePostInput {
  title: string;
  content: string;
  authorId: string;
}

export async function createPost(formData: FormData): Promise<Result<Post, ValidationError>> {
  const title = formData.get('title');
  const content = formData.get('content');
  
  // ✅ Type validation
  if (typeof title !== 'string' || title.trim().length === 0) {
    return {
      success: false,
      error: new ValidationError('Title is required', 'title'),
    };
  }
  
  const input: CreatePostInput = {
    title: title.trim(),
    content: typeof content === 'string' ? content : '',
    authorId: 'user-123',
  };
  
  // ... create post
}
```

## Type Guards

### Runtime Type Checking

```tsx
// ✅ Type guard functions
function isProduct(obj: unknown): obj is Product {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'price' in obj &&
    typeof (obj as Product).id === 'string' &&
    typeof (obj as Product).name === 'string' &&
    typeof (obj as Product).price === 'number'
  );
}

// Usage
const data = await fetch('/api/product').then(r => r.json());
if (isProduct(data)) {
  // TypeScript knows data is Product
  console.log(data.name);
}
```

## Generic Types

### Reusable Components

```tsx
// ✅ Generic component types
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={products}
  renderItem={(product) => <ProductCard product={product} />}
  keyExtractor={(product) => product.id}
/>
```

## Best Practices

1. **Enable strict mode** - Use `strict: true` in tsconfig.json
2. **Avoid `any`** - Use `unknown` and type guards instead
3. **Use type inference** - Let TypeScript infer types when possible
4. **Define interfaces for objects** - Prefer interfaces over type aliases for object shapes
5. **Use const assertions** - `as const` for literal types
6. **Type function returns** - Explicitly type function return values for complex functions
7. **Use discriminated unions** - For type-safe state machines
8. **Leverage utility types** - Use built-in utility types (Partial, Pick, Omit, etc.)

## Common Patterns

### Discriminated Unions

```tsx
type LoadingState = { status: 'loading' };
type SuccessState = { status: 'success'; data: Product[] };
type ErrorState = { status: 'error'; error: string };

type ProductsState = LoadingState | SuccessState | ErrorState;

function ProductsList({ state }: { state: ProductsState }) {
  switch (state.status) {
    case 'loading':
      return <div>Loading...</div>;
    case 'success':
      return <div>{state.data.map(p => p.name)}</div>;
    case 'error':
      return <div>Error: {state.error}</div>;
  }
}
```

### Const Assertions

```tsx
// ✅ Use const assertions for literal types
const themes = ['light', 'dark'] as const;
type Theme = typeof themes[number]; // 'light' | 'dark'

const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```
