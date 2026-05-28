# TypeScript Patterns Reference

## Let Inference Work

The most important pattern: **type your queryFn return, not the useQuery generics**.

```tsx
// BAD: Manual generics
const { data } = useQuery<Todo[], Error>({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

// GOOD: Let inference work
async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  return response.json();
}

const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
}); // data is inferred as Todo[] | undefined
```

**Why:** TypeScript lacks partial type argument inference. Specifying one generic forces you to specify all four.

## useQuery Generic Parameters

`useQuery` accepts four generics (rarely needed to specify manually):

| Generic        | Purpose                        | Default        |
| -------------- | ------------------------------ | -------------- |
| `TQueryFnData` | Return type of queryFn         | Inferred       |
| `TError`       | Error type                     | `Error`        |
| `TData`        | Final data type (after select) | `TQueryFnData` |
| `TQueryKey`    | Query key type                 | Inferred       |

## Type Narrowing Without Destructuring

Keep the query object intact for proper type narrowing:

```tsx
// BAD: Destructuring breaks narrowing
const { data, isSuccess } = useQuery({...});
if (isSuccess) {
  data; // Still Todo[] | undefined
}

// GOOD: Keep object intact
const query = useQuery({...});
if (query.isSuccess) {
  query.data; // Narrowed to Todo[]
}
```

**Note:** TypeScript 4.6+ improved this, but keeping the object intact is still more reliable.

## skipToken for Type-Safe Disabling

Use `skipToken` instead of `enabled: false` for better type safety:

```tsx
import { skipToken, useQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string | undefined }) {
  const { data } = useQuery({
    queryKey: ['user', userId],
    queryFn: userId ? () => fetchUser(userId) : skipToken,
  });
}
```

**Benefits:**

- No need for `enabled` option
- TypeScript understands the query won't run when userId is undefined
- Cleaner than `enabled: !!userId`

## Runtime Validation with Zod

TypeScript types don't exist at runtime. Validate API responses:

```tsx
import { z } from 'zod';

const todoSchema = z.object({
  id: z.string(),
  name: z.string(),
  completed: z.boolean(),
});

const todosSchema = z.array(todoSchema);

type Todo = z.infer<typeof todoSchema>;

async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  const data = await response.json();
  return todosSchema.parse(data); // Throws on invalid data
}
```

**Behavior:** Parse errors become query failures, triggering React Query's error handling.

## QueryFunctionContext Typing

Type the context parameter for queries using factory keys:

```tsx
import { type QueryFunctionContext, queryOptions } from '@tanstack/react-query';

const todoKeys = {
  all: ['todos'] as const,
  list: (filters: { status: string }) =>
    [...todoKeys.all, 'list', filters] as const,
};

type TodoListKey = ReturnType<typeof todoKeys.list>;

async function fetchTodos({
  queryKey,
}: QueryFunctionContext<TodoListKey>): Promise<Todo[]> {
  const [, , { status }] = queryKey; // Fully typed!
  return fetch(`/api/todos?status=${status}`).then((r) => r.json());
}
```

## Typing select Functions

When using `select`, the output type differs from `TQueryFnData`:

```tsx
// Inference works automatically
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos, // Returns Todo[]
  select: (todos) => todos.length, // data is number | undefined
});
```

For reusable query options with custom selectors:

```tsx
function todoOptions<TData = Todo[]>(select?: (data: Todo[]) => TData) {
  return queryOptions({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select,
  });
}

// Full data
useQuery(todoOptions());

// Selected data
useQuery(todoOptions((todos) => todos.length));
```

## Typing Mutations

Type both the input variables and return type:

```tsx
type CreateTodoInput = {
  name: string;
  completed?: boolean;
};

const createTodo = async (input: CreateTodoInput): Promise<Todo> => {
  const response = await fetch('/api/todos', {
    method: 'POST',
    body: JSON.stringify(input),
  });
  return response.json();
};

const mutation = useMutation({
  mutationFn: createTodo,
}); // Variables typed as CreateTodoInput, data as Todo
```

## Error Type Handling

Handle errors defensively since anything can be thrown:

```tsx
const { error } = useQuery({...});

// Type guard
if (error instanceof Error) {
  console.error(error.message);
}

// Or use custom error type with Zod
const apiErrorSchema = z.object({
  message: z.string(),
  code: z.string(),
});

function isApiError(error: unknown): error is z.infer<typeof apiErrorSchema> {
  return apiErrorSchema.safeParse(error).success;
}
```

## Avoid any

Configure strict TypeScript and ESLint:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true
  }
}
```

```js
// eslint.config.js
{
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
  }
}
```

## End-to-End Type Safety

For full-stack TypeScript projects, consider:

- **tRPC**: Auto-infers frontend types from backend definitions
- **Zodios**: REST API client with Zod schema validation
- **OpenAPI/Swagger**: Generate types from API specs
