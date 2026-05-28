# Layer Templates

## Repository Layer

```typescript
// app/{domain}/_repositories/{Domain}Repository.ts
import { createServerSupabaseClient } from '@/lib/supabase/server';
import type { Get{Domain}sParams, Get{Domain}sResponse } from '@/models/{domain}.model';

export class {Domain}Repository {
  async get{Domain}s(params: Get{Domain}sParams): Promise<Get{Domain}sResponse> {
    const supabase = await createServerSupabaseClient();

    // TODO: Implement using core-supabase RPC patterns
    // skill:fetch-supabase-example("{domain}", "read")

    throw new Error('Not implemented');
  }
}

// app/{domain}/_repositories/index.ts
export { {Domain}Repository } from './{Domain}Repository';
```

## API Client Layer

```typescript
// app/{domain}/_api-clients/{domain}.client.ts
import type { Get{Domain}sParams, Get{Domain}sResponse } from '@/models/{domain}.model';

const API_BASE = process.env.NEXT_PUBLIC_API_MODE === 'spring'
  ? process.env.NEXT_PUBLIC_SPRING_API_URL
  : '/api';

export class {Domain}ApiClient {
  async get{Domain}s(params: Get{Domain}sParams): Promise<Get{Domain}sResponse> {
    const query = new URLSearchParams(params as any);
    const response = await fetch(`${API_BASE}/{domain}?${query}`);

    if (!response.ok) {
      throw new Error('Failed to fetch {domain}');
    }

    return response.json();
  }
}

// Factory Pattern singleton
export const {domain}Client = new {Domain}ApiClient();

// app/{domain}/_api-clients/index.ts
export { {domain}Client, {Domain}ApiClient } from './{domain}.client';
```

## Hooks Layer

```typescript
// app/{domain}/_hooks/use{Domain}s.ts
import { useQuery } from '@tanstack/react-query';
import { {domain}Client } from '../_api-clients';
import type { Get{Domain}sParams } from '@/models/{domain}.model';

export function use{Domain}s(params: Get{Domain}sParams = {}) {
  return useQuery({
    queryKey: ['{domain}', params],
    queryFn: () => {domain}Client.get{Domain}s(params),
    staleTime: 60 * 1000, // 1 minute
  });
}

// app/{domain}/_hooks/index.ts
export { use{Domain}s } from './use{Domain}s';
```

## Components Layer

```typescript
// app/{domain}/_components/{Domain}Header.tsx
export function {Domain}Header() {
  return (
    <div>
      <h1>{Domain} Header</h1>
      {/* TODO: Implement header UI */}
    </div>
  );
}

// app/{domain}/_components/index.ts
export { {Domain}Header } from './{Domain}Header';
export { {Domain}Filter } from './{Domain}Filter';
export { {Domain}List } from './{Domain}List';
export { {Domain}EmptyState } from './{Domain}EmptyState';
export { {Domain}LoadingState } from './{Domain}LoadingState';
export { {Domain}ErrorState } from './{Domain}ErrorState';
```

## Page Component

```typescript
// app/{domain}/page.tsx
import {
  {Domain}Header,
  {Domain}Filter,
  {Domain}List,
  {Domain}EmptyState,
  {Domain}LoadingState,
  {Domain}ErrorState,
} from './_components';
import { use{Domain}s } from './_hooks';

export default function {Domain}Page() {
  const { data, isLoading, error } = use{Domain}s();

  if (isLoading) return <{Domain}LoadingState />;
  if (error) return <{Domain}ErrorState error={error} />;
  if (!data?.items?.length) return <{Domain}EmptyState />;

  return (
    <>
      <{Domain}Header />
      <{Domain}Filter />
      <{Domain}List items={data.items} />
    </>
  );
}
```

## Global Exports Update

```typescript
// lib/api-clients/index.ts
export { {domain}Client } from '@/app/{domain}/_api-clients';

// models/index.ts
export type * from './{domain}.model';
```
