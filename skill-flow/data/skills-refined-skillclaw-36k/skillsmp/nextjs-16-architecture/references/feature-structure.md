# Feature Structure

## Project Layout
```
features/
├── agents/           # AI chat feature
├── auth/             # Authentication
├── marketing/        # Landing pages
├── shared/           # Cross-cutting concerns
└── i18n/             # Internationalization
```

## Feature Anatomy
```
features/{feature}/
├── components/
│   ├── server/           # Server Components (async, data fetching)
│   ├── client/           # Client Components ('use client')
│   ├── skeletons/        # Loading skeletons
│   └── ui/               # Compound components (optional)
├── data/                 # Database queries
├── actions/              # Server Actions
├── types/                # TypeScript types
├── schemas/              # Zod validation schemas
├── hooks/                # Client hooks
├── lib/                  # Utilities
├── agents/               # AI agents (domain-specific)
├── emails/               # Email templates (domain-specific)
└── prompts/              # AI prompts (domain-specific)
```

## Rules

### Feature Independence
- Each feature is self-contained
- Features can import from `shared/`
- Features **cannot** import from other features (except `shared/`)
- `app/` imports from `features/`, never the reverse

### One File Per Concern
- **Types**: 1 file = 1 type (`types/agent.ts`)
- **Schemas**: 1 file = 1 schema (`schemas/agent-schema.ts`)
- **Queries**: 1 file = 1 query (`data/get-agent.ts`)
- **Actions**: 1 file = 1 action (`actions/delete-agent-action.ts`)
- **Hooks**: 1 file = 1 hook (`hooks/use-agent-form.ts`)

### File Naming Conventions

**Components:**
- Server: `components/server/agent-header.tsx`
- Client: `components/client/login-form.tsx`
- Skeleton: `components/skeletons/agent-header-skeleton.tsx`

**Data:**
- Single entity: `get-agent.ts`
- Multiple entities: `get-agents.ts`
- Create: `create-agent.ts`
- Update: `update-agent.ts`
- Delete: `delete-agent.ts`
- Upsert: `upsert-message.ts`

**Actions:**
- Pattern: `{verb}-{entity}-action.ts`
- Examples: `delete-agent-action.ts`, `create-agent-action.ts`

## Import Structure
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Dependency Direction
```
app/              → features/
features/{name}/  → features/shared/
features/shared/  → (nothing, base layer)
db/               → (external, imported by features)
```

### Examples
```typescript
// ✅ Correct
import { Button } from '@/features/shared/components/ui/button'
import { getAgent } from '@/features/agents/data/get-agent'
import type { Agent } from '@/db/schemas/agents'

// ❌ Wrong - NEVER use relative imports
import { Button } from '../../../shared/components/ui/button'

// ❌ Wrong - features cannot import from other features
import { getUser } from '@/features/users/data/get-user' // from agents feature
```
