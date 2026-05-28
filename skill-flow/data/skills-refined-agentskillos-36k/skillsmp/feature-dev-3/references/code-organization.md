# Code Organization Conventions

Standard code layer organization for this project.

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Routes    │  │  Components │  │   State/Query       │  │
│  │ src/routes/ │  │ src/comp/   │  │ src/lib/query/      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │                                   │
│                    src/lib/api/                              │
│                    (API Client)                              │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────┴──────────────────────────────────┐
│                        Backend                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    functions/routes/                     ││
│  │                    (API Handlers)                        ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  functions/services/                     ││
│  │                  (Business Logic)                        ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    shared/schemas/                       ││
│  │                  (Zod Definitions)                       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## File Naming Conventions

| Layer | Pattern | Example |
|-------|---------|---------|
| Schema | `{feature}.schema.ts` | `timeline.schema.ts` |
| Types | `{feature}.ts` | `timeline.ts` |
| Service | `{feature}.service.ts` | `timeline.service.ts` |
| Route | `{feature}.ts` | `timeline.ts` |
| API Client | `{feature}.ts` | `timeline.ts` |
| Query Hooks | `{feature}.ts` | `timeline.ts` |
| Page | `{feature}.tsx` | `timeline.tsx` |
| Module | `{Feature}Module.tsx` | `TimelineModule.tsx` |

## Layer Responsibilities

### 1. Schema Layer (`shared/schemas/`)

**Purpose**: Define data shapes and validation rules.

**Contents**:
- Zod schemas for all data types
- Input validation schemas
- Type exports derived from schemas

**Example**:
```typescript
// shared/schemas/timeline.schema.ts
import { z } from 'zod';

export const TimelineInputSchema = z.object({
  birthdate: z.string().datetime(),
  gender: z.enum(['male', 'female']),
});

export type TimelineInput = z.infer<typeof TimelineInputSchema>;

export const TimelineOutputSchema = z.object({
  id: z.string(),
  periods: z.array(PeriodSchema),
});

export type TimelineOutput = z.infer<typeof TimelineOutputSchema>;
```

### 2. Service Layer (`functions/services/`)

**Purpose**: Business logic, data processing, external integrations.

**Contents**:
- Core business logic functions
- Data transformations
- External API calls
- Database operations

**Example**:
```typescript
// functions/services/timeline.service.ts
import { TimelineInput, TimelineOutput } from '@/shared/schemas/timeline.schema';

export async function generateTimeline(input: TimelineInput): Promise<TimelineOutput> {
  // Business logic here
  const periods = calculatePeriods(input);
  return { id: generateId(), periods };
}
```

### 3. Route Layer (`functions/routes/`)

**Purpose**: HTTP request handling, validation, response formatting.

**Contents**:
- Route definitions
- Request validation using schemas
- Response formatting
- Error handling

**Example**:
```typescript
// functions/routes/timeline.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { TimelineInputSchema } from '@/shared/schemas/timeline.schema';
import { generateTimeline } from '@/functions/services/timeline.service';

const app = new Hono();

app.post('/', zValidator('json', TimelineInputSchema), async (c) => {
  const input = c.req.valid('json');
  const result = await generateTimeline(input);
  return c.json({ success: true, data: result });
});

export default app;
```

### 4. API Client Layer (`src/lib/api/`)

**Purpose**: HTTP client functions for frontend.

**Contents**:
- Fetch wrapper functions
- Request/response type definitions
- Error handling

**Example**:
```typescript
// src/lib/api/timeline.ts
import { TimelineInput, TimelineOutput } from '@/shared/schemas/timeline.schema';
import { apiClient } from './client';

export async function createTimeline(input: TimelineInput): Promise<TimelineOutput> {
  const response = await apiClient.post<{ data: TimelineOutput }>('/api/timeline', input);
  return response.data;
}
```

### 5. Query Layer (`src/lib/query/`)

**Purpose**: TanStack Query hooks for data fetching and caching.

**Contents**:
- useQuery hooks
- useMutation hooks
- Query key definitions

**Example**:
```typescript
// src/lib/query/timeline.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import { createTimeline, getTimeline } from '@/lib/api/timeline';

export const timelineKeys = {
  all: ['timelines'] as const,
  detail: (id: string) => [...timelineKeys.all, id] as const,
};

export function useTimeline(id: string) {
  return useQuery({
    queryKey: timelineKeys.detail(id),
    queryFn: () => getTimeline(id),
  });
}

export function useCreateTimeline() {
  return useMutation({
    mutationFn: createTimeline,
  });
}
```

### 6. Component Layer (`src/components/`)

**Purpose**: Reusable UI components.

**Structure**:
```
src/components/
├── ui/              # Primitive components (Button, Input, etc.)
├── modules/         # Feature-specific components
└── layout/          # Layout components
```

**Naming**:
- Module components: `{Feature}Module.tsx`
- UI components: `{Component}.tsx`

### 7. Route Layer (`src/routes/`)

**Purpose**: Page components and routing.

**Contents**:
- Page components
- Route configuration
- Page-level state

## Import Conventions

**Preferred import order**:
1. External packages
2. Internal aliases (`@/`)
3. Relative imports

**Alias usage**:
```typescript
// Use aliases for cross-layer imports
import { TimelineSchema } from '@/shared/schemas/timeline.schema';
import { TimelineService } from '@/functions/services/timeline.service';

// Use relative for same-layer imports
import { formatDate } from './utils';
```

## Testing Conventions

| Layer | Test Location | Test Type |
|-------|---------------|-----------|
| Schema | `shared/schemas/*.test.ts` | Unit |
| Service | `functions/services/*.test.ts` | Unit/Integration |
| Route | `functions/routes/*.test.ts` | Integration |
| Component | `src/components/**/*.test.tsx` | Component |
| E2E | `tests/e2e/*.spec.ts` | E2E |
