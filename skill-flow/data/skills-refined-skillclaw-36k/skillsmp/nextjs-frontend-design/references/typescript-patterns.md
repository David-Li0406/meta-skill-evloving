# TypeScript Patterns for Next.js

Advanced TypeScript patterns for production Next.js applications.

## Strict Type Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## API Response Types

```typescript
// types/api.ts

// Generic API response wrapper
type ApiResponse<T> = 
  | { success: true; data: T }
  | { success: false; error: ApiError };

interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

// Type-safe fetch wrapper
async function apiFetch<T>(
  url: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const error = await response.json();
      return { success: false, error };
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: { code: 'NETWORK_ERROR', message: 'Network request failed' },
    };
  }
}

// Usage with narrowing
const result = await apiFetch<User[]>('/api/users');
if (result.success) {
  // TypeScript knows result.data is User[]
  console.log(result.data);
} else {
  // TypeScript knows result.error is ApiError
  console.error(result.error.message);
}
```

## Server Action Patterns

```typescript
// types/actions.ts
import { z } from 'zod';

// Generic action result type
type ActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string; fieldErrors?: Record<string, string[]> };

// Type-safe action creator
function createAction<TInput, TOutput>(
  schema: z.ZodSchema<TInput>,
  handler: (input: TInput) => Promise<TOutput>
) {
  return async (formData: FormData): Promise<ActionResult<TOutput>> => {
    const raw = Object.fromEntries(formData.entries());
    const parsed = schema.safeParse(raw);

    if (!parsed.success) {
      return {
        success: false,
        error: 'Validation failed',
        fieldErrors: parsed.error.flatten().fieldErrors as Record<string, string[]>,
      };
    }

    try {
      const data = await handler(parsed.data);
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  };
}

// Usage
const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.coerce.boolean().default(false),
});

export const createPost = createAction(CreatePostSchema, async (input) => {
  const post = await db.post.create({ data: input });
  revalidatePath('/posts');
  return post;
});
```

## Component Props Patterns

```typescript
// Polymorphic component pattern
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProps<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

// Example: Polymorphic Box component
interface BoxOwnProps {
  padding?: 'sm' | 'md' | 'lg';
}

type BoxProps<C extends React.ElementType = 'div'> = PolymorphicComponentProps<C, BoxOwnProps>;

function Box<C extends React.ElementType = 'div'>({
  as,
  padding = 'md',
  children,
  className,
  ...props
}: BoxProps<C>) {
  const Component = as || 'div';
  return (
    <Component
      className={cn(
        padding === 'sm' && 'p-2',
        padding === 'md' && 'p-4',
        padding === 'lg' && 'p-8',
        className
      )}
      {...props}
    >
      {children}
    </Component>
  );
}

// Usage
<Box padding="lg">Default div</Box>
<Box as="section" padding="sm">Section element</Box>
<Box as="a" href="/about" padding="md">Link element</Box>
```

## Discriminated Unions for State

```typescript
// UI state machine pattern
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// Component using async state
function UserProfile({ userId }: { userId: string }) {
  const [state, setState] = useState<AsyncState<User>>({ status: 'idle' });

  useEffect(() => {
    setState({ status: 'loading' });
    fetchUser(userId)
      .then((data) => setState({ status: 'success', data }))
      .catch((error) => setState({ status: 'error', error }));
  }, [userId]);

  switch (state.status) {
    case 'idle':
    case 'loading':
      return <Skeleton />;
    case 'error':
      return <ErrorMessage error={state.error} />;
    case 'success':
      return <ProfileCard user={state.data} />;
  }
}
```

## Environment Variables with Type Safety

```typescript
// env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXTAUTH_URL: z.string().url(),
  // Client-side variables (must start with NEXT_PUBLIC_)
  NEXT_PUBLIC_API_URL: z.string().url(),
});

// Validate at build time
const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.flatten().fieldErrors);
  throw new Error('Invalid environment variables');
}

export const env = parsed.data;

// Usage
import { env } from '@/lib/env';
const apiUrl = env.NEXT_PUBLIC_API_URL;
```

## Database Types with Prisma

```typescript
// types/database.ts
import type { Prisma } from '@prisma/client';

// Reusable includes
const userWithPosts = Prisma.validator<Prisma.UserDefaultArgs>()({
  include: { posts: true },
});

type UserWithPosts = Prisma.UserGetPayload<typeof userWithPosts>;

// Function with typed return
async function getUserWithPosts(id: string): Promise<UserWithPosts | null> {
  return db.user.findUnique({
    where: { id },
    ...userWithPosts,
  });
}

// Input types for mutations
type CreateUserInput = Prisma.UserCreateInput;
type UpdateUserInput = Prisma.UserUpdateInput;
```

## Custom Hook Patterns

```typescript
// hooks/use-async.ts
function useAsync<T, Args extends unknown[]>(
  asyncFn: (...args: Args) => Promise<T>
) {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' });

  const execute = useCallback(
    async (...args: Args) => {
      setState({ status: 'loading' });
      try {
        const data = await asyncFn(...args);
        setState({ status: 'success', data });
        return data;
      } catch (error) {
        const err = error instanceof Error ? error : new Error('Unknown error');
        setState({ status: 'error', error: err });
        throw err;
      }
    },
    [asyncFn]
  );

  return { ...state, execute };
}

// hooks/use-debounce.ts
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// hooks/use-local-storage.ts
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const newValue = value instanceof Function ? value(prev) : value;
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(key, JSON.stringify(newValue));
        }
        return newValue;
      });
    },
    [key]
  );

  return [storedValue, setValue];
}
```

## Route Handler Types

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

type RouteContext = {
  params: Promise<{ id: string }>;
};

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get('page') || '1', 10);
  const limit = parseInt(searchParams.get('limit') || '10', 10);

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({ users, page, limit });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const parsed = CreateUserSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const user = await db.user.create({ data: parsed.data });
  return NextResponse.json(user, { status: 201 });
}

// Dynamic route
export async function GET(
  request: NextRequest,
  context: RouteContext
) {
  const { id } = await context.params;
  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(user);
}
```
