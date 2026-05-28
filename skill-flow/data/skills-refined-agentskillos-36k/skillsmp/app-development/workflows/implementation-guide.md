# Feature Implementation Guide

Step-by-step checklist for implementing new features.

## Phase 1: Planning

- [ ] Understand requirements
- [ ] Review existing patterns in codebase
- [ ] Identify affected components
- [ ] Plan data flow
- [ ] Design schema (if needed)

## Phase 2: Schema & Types

- [ ] Create/update Zod schema (`src/lib/schema/zod-schema/*`)
- [ ] Create/update Mongoose schema (`src/lib/schema/mongoose-schema/*`)
- [ ] Export TypeScript types from Zod
- [ ] Test schema validation

### Zod Schema Template
```typescript
// src/lib/schema/zod-schema/my-feature.ts
import { z } from "zod";

export const MyFeatureSchema = z.object({
  id: z.string(),
  name: z.string(),
  // ... more fields
});

export type MyFeature = z.infer<typeof MyFeatureSchema>;
```

### Mongoose Schema Template
```typescript
// src/lib/schema/mongoose-schema/my-feature.ts
import mongoose from "mongoose";

const myFeatureSchema = new mongoose.Schema({
  name: String,
  // ... match Zod schema
});

export const MyFeatureModel = mongoose.models.MyFeature ||
  mongoose.model("MyFeature", myFeatureSchema);
```

## Phase 3: Backend Implementation

- [ ] Create server actions (`src/app/actions/*`)
- [ ] Implement database operations
- [ ] Add error handling with `handleServerError`
- [ ] Test with mongosh if needed

### Server Action Template
```typescript
// src/app/actions/my-feature/fetch-my-feature.ts
"use server";

import { withDbConnection } from "@server/withDbConnection";
import { MyFeatureModel } from "@mongoose-schema/my-feature";

export async function fetchMyFeature(id: string) {
  return withDbConnection(async () => {
    try {
      const feature = await MyFeatureModel.findById(id);
      return { success: true, data: feature?.toJSON() };
    } catch (error) {
      return { success: false, error: handleServerError(error, "Failed") };
    }
  });
}
```

## Phase 4: Frontend Implementation

- [ ] Create React Query hooks (if needed)
- [ ] Build UI components
- [ ] Implement forms/interactions
- [ ] Add loading/error states

### React Query Hook Template
```typescript
// src/query/my-feature/useMyFeatureQuery.ts
import { useQuery } from "@tanstack/react-query";
import { fetchMyFeature } from "@actions/my-feature/fetch-my-feature";

export function useMyFeatureQuery(id: string) {
  return useQuery({
    queryKey: ["myFeature", id],
    queryFn: () => fetchMyFeature(id),
    enabled: !!id,
  });
}
```

### Component Template
```typescript
// src/components/domain/my-feature/MyFeatureCard.tsx
"use client";

import { useMyFeatureQuery } from "@/query/my-feature/useMyFeatureQuery";

export function MyFeatureCard({ id }: { id: string }) {
  const { data, isLoading, error } = useMyFeatureQuery(id);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading feature</div>;

  return <div>{data?.data?.name}</div>;
}
```

## Phase 5: Testing & Polish

- [ ] Test all user flows
- [ ] Check responsive design
- [ ] Verify error handling
- [ ] Run `npm run lint`
- [ ] Run `npm run prebuild`

## Phase 6: Code Review

- [ ] Self-review changes
- [ ] Check for console logs
- [ ] Verify no `any` types
- [ ] Create PR with description
