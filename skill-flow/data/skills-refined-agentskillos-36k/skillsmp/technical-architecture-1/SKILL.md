---
name: technical-architecture
description: Technical patterns for React/Next.js + n8n + Airtable dashboard stack. Covers data layer design, frontend architecture, state management, performance optimisation, and deployment patterns.
user-invocable: false
---

# Technical Architecture Skill for React/Next.js + n8n Dashboard Stack

## Purpose

Comprehensive technical architecture guidance for building market intelligence dashboards on a hybrid "low-code" stack: Airtable (data layer) + n8n (workflow automation) + React/Next.js (frontend). Prioritises rapid development, maintainability, and real-time responsiveness.

## Related Skills

- UK Police Design System Skill — For frontend component specifications
- Action-Oriented UX Skill — For interaction patterns the architecture must support
- Notification System Skill — For alert delivery infrastructure
- ADHD Interface Design Skill — For performance requirements (sub-100ms)


## Data Layer (Airtable)

### Schema Design Principles

1. **Normalise for clarity, denormalise for performance**
   - Core entities in separate tables
   - Pre-computed rollups for dashboard views

2. **Use formula fields for derived values**
   - Computed at read time, always fresh
   - Example: `Days Since Last Contact = DATETIME_DIFF(NOW(), {Last Contact Date}, 'days')`

3. **Use views as "API endpoints"**
   - Create views for specific use cases
   - Views handle filtering and sorting server-side

4. **Linked records for relationships**
   - Contact → Organisation (many-to-one)
   - Lead → Organisation + Contact (many-to-one)

### Materialised Views Pattern

For dashboard performance, pre-compute aggregations:

**Why:**
- Formula fields compute on read (slow for complex queries)
- Rollups across large tables are expensive
- Dashboard needs fast responses (<500ms)

**Implementation:**
- n8n workflow runs on schedule (e.g., hourly)
- Aggregates data from source tables
- Writes to "dashboard" tables with pre-computed values
- Frontend reads from materialised tables only

```
Raw Tables                    Materialised Views
──────────────                ──────────────────
Forces           ────┐
Contacts         ────┼──▶ n8n ──▶  DailyScores
Interactions     ────┤              WeeklyTrends
JobPostings      ────┘              AlertFeed
```


## Frontend Architecture (Next.js 14)

### Why Next.js + shadcn/ui

| Feature | Benefit |
|---------|---------|
| App Router | Server Components, streaming, layouts |
| TypeScript | Type safety, better DX |
| shadcn/ui | Accessible components, Tailwind integration |
| Zustand | Simple state management |
| Server Actions | Secure data mutations |

### Project Structure

```
/dashboard-react
├── app/
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Home/redirect
│   ├── board/
│   │   └── page.tsx            # Board dashboard (5 tabs)
│   ├── focus/
│   │   └── page.tsx            # Focus mode
│   └── api/
│       └── board/              # API routes
│           ├── pipeline/route.ts
│           ├── leads/route.ts
│           └── signals/route.ts
├── components/
│   ├── ui/                     # shadcn/ui components
│   ├── board/                  # Board-specific components
│   │   ├── pipeline-tab.tsx
│   │   ├── lead-table.tsx
│   │   └── signal-feed.tsx
│   └── shared/                 # Shared components
├── lib/
│   ├── stores/                 # Zustand stores
│   │   └── board-store.ts
│   ├── types/                  # TypeScript types
│   │   └── board.ts
│   ├── utils/                  # Utility functions
│   └── api/                    # API client functions
└── styles/
    └── globals.css             # Tailwind + custom styles
```

### State Management with Zustand

**Use Zustand for:**
- Current tab selection
- Filter settings
- UI state (modals, toasts)
- Cached data with timestamps

```typescript
// lib/stores/board-store.ts
import { create } from 'zustand'

interface BoardState {
  activeTab: number
  setActiveTab: (tab: number) => void
  filters: FilterState
  setFilters: (filters: Partial<FilterState>) => void
}

export const useBoardStore = create<BoardState>((set) => ({
  activeTab: 0,
  setActiveTab: (tab) => set({ activeTab: tab }),
  filters: defaultFilters,
  setFilters: (filters) => set((state) => ({
    filters: { ...state.filters, ...filters }
  })),
}))
```

### Data Fetching Patterns

**Server Components (preferred for initial load):**
```typescript
// app/board/page.tsx
async function BoardPage() {
  const data = await fetchBoardData()
  return <BoardDashboard initialData={data} />
}
```

**Client-side with SWR (for real-time updates):**
```typescript
// components/board/pipeline-tab.tsx
'use client'
import useSWR from 'swr'

export function PipelineTab() {
  const { data, error, isLoading } = useSWR('/api/board/pipeline', fetcher, {
    refreshInterval: 30000, // 30 second refresh
  })
  // ...
}
```

### API Routes

**Pattern for n8n proxy:**
```typescript
// app/api/board/pipeline/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const res = await fetch(`${process.env.N8N_WEBHOOK_URL}/pipeline`, {
    headers: {
      'X-Dashboard-Secret': process.env.DASHBOARD_SECRET!,
    },
    next: { revalidate: 60 }, // Cache for 60 seconds
  })

  const data = await res.json()
  return NextResponse.json(data)
}
```

### Optimistic Updates

```typescript
// Using SWR's mutate
const handleAction = async (leadId: string) => {
  // 1. Optimistic update
  mutate('/api/leads',
    (current) => current?.filter(l => l.id !== leadId),
    { revalidate: false }
  )

  // 2. Server update
  await fetch(`/api/leads/${leadId}/action`, { method: 'POST' })

  // 3. Revalidate to sync
  mutate('/api/leads')
}
```


## Performance Optimisation

### Frontend Performance

| Technique | Implementation |
|-----------|----------------|
| Server Components | Default in App Router, reduces JS |
| Streaming | Suspense boundaries for progressive load |
| Pre-fetch | `<Link prefetch>` for navigation |
| Skeleton loaders | Show layout immediately |
| Virtual scrolling | `@tanstack/react-virtual` for long lists |
| Image optimisation | Next.js `<Image>` component |

### API Performance

| Technique | Implementation |
|-----------|----------------|
| Response caching | `next: { revalidate: N }` in fetch |
| Field selection | Only return needed fields |
| Pagination | 20-50 records per request |
| Batch operations | Update multiple in single call |

### Airtable Performance

| Technique | Implementation |
|-----------|----------------|
| Materialised views | Pre-compute aggregations |
| View-based queries | Use views instead of complex filters |
| Rate limit handling | Queue requests, respect 5 req/sec |


## Deployment

### Infrastructure

VPS (UK-based) with Docker Compose:
- **Caddy** (Reverse proxy, HTTPS) on port 443
- **n8n** (Workflows) on port 5678
- **Next.js** (Frontend) on port 3000

### Docker Configuration

```dockerfile
# dashboard-react/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

### Environment Variables

```bash
# .env.local (local development)
# .env.production (VPS)

# n8n Webhook URL
N8N_WEBHOOK_URL=https://n8n.yourdomain.com/webhook

# Dashboard auth
DASHBOARD_SECRET=<32-char-token>

# Airtable (for direct API routes if needed)
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=appEEWaGtGUwOyOhm
```


## Architecture Decision Records

### ADR 1: Proxy Layer
**Decision:** Use n8n webhooks + Next.js API routes as API proxy
**Rationale:** Flexibility — n8n for complex workflows, API routes for simple queries

### ADR 2: State Management
**Decision:** Zustand for client state, SWR for server state
**Rationale:** Simple, lightweight, good TypeScript support

### ADR 3: UI Components
**Decision:** shadcn/ui with Tailwind
**Rationale:** Accessible, customisable, no runtime overhead

### ADR 4: Caching Strategy
**Decision:** Next.js fetch cache + SWR client cache
**Rationale:** Built-in, no additional infrastructure
