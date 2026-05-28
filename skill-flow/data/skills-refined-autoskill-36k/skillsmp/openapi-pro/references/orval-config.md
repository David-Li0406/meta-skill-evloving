# Client Generation with Orval

## Why Orval?
Orval is the most flexible generator in 2026 for projects using **React Query** (TanStack Query) or **SWR**. It transforms an OpenAPI spec into ready-to-use hooks and Fetch clients.

---

## 1. `orval.config.ts`
```typescript
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: './openapi.yaml',
    output: {
      target: './src/generated/api.ts',
      client: 'react-query', // Generates useQuery/useMutation hooks
      mode: 'tags-split',    // Splits files by OpenAPI tags
      httpClient: 'fetch',   // Uses native Fetch API
      baseUrl: 'process.env.NEXT_PUBLIC_API_URL',
      override: {
        mutator: {
          path: './src/lib/custom-fetch.ts',
          name: 'customFetch',
        },
      },
    },
  },
});
```

---

## 2. Custom Mutator (Interceptors)
Instead of relying on Orval's default fetch, use a mutator to add auth headers and global error handling.

`src/lib/custom-fetch.ts`:
```typescript
export const customFetch = async <T>(
  url: string,
  method: string,
  params?: any,
  data?: any,
  headers?: any
): Promise<T> => {
  const response = await fetch(`${url}${new URLSearchParams(params)}`, {
    method,
    headers: { ...headers, Authorization: `Bearer ${getToken()}` },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('API Error');
  return response.json();
};
```

---

## 3. Usage in React
```tsx
import { useGetUser } from './generated/api';

function Profile({ id }: { id: string }) {
  const { data, isLoading } = useGetUser(id);
  
  if (isLoading) return <p>Loading...</p>;
  return <h1>{data?.name}</h1>;
}
```
