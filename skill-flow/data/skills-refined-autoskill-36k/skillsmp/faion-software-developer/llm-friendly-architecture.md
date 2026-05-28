# LLM-Friendly Codebase Architecture

Architecture patterns optimized for AI-assisted development with LLMs like Claude, GPT-4, and Copilot.

## Why LLM-Friendly Architecture Matters

LLMs have constraints that traditional architecture doesn't address:
- **Context window limits**: 100K-200K tokens, but effective reasoning ~20K
- **File navigation**: LLMs grep/glob to find code, clear naming helps
- **Understanding speed**: Self-documenting code reduces back-and-forth
- **Modification accuracy**: Smaller, focused files = fewer edit errors

## Core Principles

### 1. Optimal File Size: 100-300 Lines

```
✅ Good: 150 lines - fits in context, easy to understand
✅ Good: 250 lines - still manageable, single responsibility
⚠️ Warning: 400 lines - consider splitting
❌ Bad: 800+ lines - too large, split required
```

**Why**: LLMs make fewer errors editing small files. Large files cause:
- Truncated context
- Wrong line numbers in edits
- Missed dependencies

### 2. Flat-ish Directory Structure (Max 3 Levels)

```
❌ Deep nesting (hard for LLM to navigate):
src/modules/features/user/components/forms/inputs/TextInput.tsx

✅ Flat structure (easy to grep/glob):
src/components/TextInput.tsx
src/components/UserForm.tsx
src/features/user/UserProfile.tsx
```

**Recommended structure**:
```
src/
├── components/          # Shared UI components (flat)
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Modal.tsx
├── features/            # Feature modules (1 level deep)
│   ├── auth/
│   ├── dashboard/
│   └── settings/
├── data/                # Constants, configs, static data
├── hooks/               # Custom React hooks
├── utils/               # Pure utility functions
├── types/               # TypeScript types/interfaces
└── pages/               # Route entry points (thin)
```

### 3. Self-Documenting File Names

```
❌ Bad names (require reading to understand):
utils.ts, helpers.ts, index.ts, types.ts, constants.ts

✅ Good names (intent is clear):
price-calculator.ts, format-date.ts, use-auth.ts
landing-data.ts, pricing-plans.ts, api-endpoints.ts
```

**Pattern**: `{what-it-does}.ts` or `{domain}-{what}.ts`

### 4. Explicit Imports (No Magic)

```typescript
// ❌ Bad: Barrel re-exports hide structure
import { Button, Input, Modal } from '@/components'

// ✅ Good: Direct imports show file location
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
```

**Exception**: Barrel exports OK for public API boundaries (library packages).

### 5. Data Extraction Pattern

Extract data from components into dedicated files:

```typescript
// ❌ Bad: Data mixed with rendering (800 line file)
const PricingPage = () => {
  const plans = [
    { name: 'Free', price: 0, features: [...] },
    { name: 'Pro', price: 35, features: [...] },
    // ... 50 more lines of data
  ]
  return <div>{/* 200 lines of JSX */}</div>
}

// ✅ Good: Data extracted (component is 50 lines)
// src/data/pricing.ts
export const pricingPlans = [
  { name: 'Free', price: 0, features: [...] },
  { name: 'Pro', price: 35, features: [...] },
]

// src/pages/pricing.tsx
import { pricingPlans } from '@/data/pricing'
const PricingPage = () => <PricingGrid plans={pricingPlans} />
```

### 6. Type Colocation vs Centralization

```typescript
// ✅ Colocated types (small, component-specific)
// components/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary'
  children: React.ReactNode
}

// ✅ Centralized types (shared across features)
// types/api.ts
export interface ApiResponse<T> {
  data: T
  error?: string
  status: number
}

// types/domain.ts
export interface User {
  id: string
  email: string
  plan: PricingPlan
}
```

**Rule**: If type is used in 3+ files, centralize it.

### 7. Single Responsibility Components

```typescript
// ❌ Bad: Component does too much
const Dashboard = () => {
  // 50 lines of data fetching
  // 30 lines of state management
  // 100 lines of calculations
  // 200 lines of JSX
}

// ✅ Good: Split by responsibility
// features/dashboard/Dashboard.tsx (orchestrator, 40 lines)
// features/dashboard/DashboardStats.tsx (display, 60 lines)
// features/dashboard/DashboardChart.tsx (chart, 80 lines)
// features/dashboard/use-dashboard-data.ts (data fetching, 50 lines)
```

### 8. Consistent Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase, use- prefix | `use-auth.ts` |
| Utils | kebab-case | `format-currency.ts` |
| Data files | kebab-case | `pricing-plans.ts` |
| Types | kebab-case or domain.types.ts | `user.types.ts` |
| Constants | SCREAMING_SNAKE in file | `API_BASE_URL` |

### 9. JSDoc for Complex Functions

```typescript
// ✅ Good: LLM understands intent without reading implementation
/**
 * Calculates prorated price for plan upgrade mid-billing cycle.
 * @param currentPlan - User's current subscription plan
 * @param newPlan - Target plan for upgrade
 * @param daysRemaining - Days left in current billing period
 * @returns Prorated amount to charge in cents
 */
export function calculateProratedUpgrade(
  currentPlan: PricingPlan,
  newPlan: PricingPlan,
  daysRemaining: number
): number {
  // Implementation...
}
```

### 10. Thin Page Components

Pages should be orchestrators, not implementors:

```typescript
// ✅ Good: Page is thin (~30-50 lines)
// pages/pricing.tsx
import { PricingHero } from '@/features/pricing/PricingHero'
import { PricingGrid } from '@/features/pricing/PricingGrid'
import { PricingFAQ } from '@/features/pricing/PricingFAQ'

export default function PricingPage() {
  return (
    <Layout>
      <PricingHero />
      <PricingGrid />
      <PricingFAQ />
    </Layout>
  )
}
```

## File Size Guidelines by Type

| File Type | Target | Max | Action if exceeded |
|-----------|--------|-----|-------------------|
| Page/Route | 30-50 | 100 | Extract sections to features/ |
| Feature component | 80-150 | 250 | Split into sub-components |
| UI component | 50-100 | 150 | Extract variants/logic |
| Hook | 30-80 | 120 | Split concerns |
| Utility | 20-50 | 80 | One function per file |
| Data file | 50-200 | 300 | Split by domain |
| Types file | 30-100 | 150 | Split by domain |

## Directory Structure Template

```
project/
├── src/
│   ├── components/              # Shared UI (flat, no nesting)
│   │   ├── Button.tsx          # 50-100 lines each
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── Card.tsx
│   │
│   ├── features/                # Feature modules
│   │   ├── landing/            # One folder per feature
│   │   │   ├── HeroSection.tsx
│   │   │   ├── PricingSection.tsx
│   │   │   └── FAQSection.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── use-auth.ts
│   │   └── dashboard/
│   │       ├── DashboardLayout.tsx
│   │       ├── StatsCard.tsx
│   │       └── use-dashboard.ts
│   │
│   ├── data/                    # Static data, constants
│   │   ├── navigation.ts       # Nav links, menu items
│   │   ├── pricing.ts          # Pricing plans, features
│   │   └── content.ts          # Copy, testimonials
│   │
│   ├── hooks/                   # Shared custom hooks
│   │   ├── use-media-query.ts
│   │   └── use-local-storage.ts
│   │
│   ├── utils/                   # Pure functions
│   │   ├── format-currency.ts
│   │   ├── format-date.ts
│   │   └── cn.ts               # className helper
│   │
│   ├── types/                   # Shared TypeScript types
│   │   ├── api.ts
│   │   └── domain.ts
│   │
│   ├── styles/                  # Global styles
│   │   └── globals.css
│   │
│   └── pages/                   # Route entry points (THIN)
│       ├── index.tsx           # 30-50 lines
│       ├── pricing.tsx
│       └── docs.tsx
│
├── CLAUDE.md                    # Project context for LLM
└── package.json
```

## Anti-Patterns to Avoid

### 1. God Components
```typescript
// ❌ 800+ line component doing everything
const App = () => { /* routing, auth, data, UI all mixed */ }
```

### 2. Utils Dumping Ground
```typescript
// ❌ utils/index.ts with 50 unrelated functions
export { formatDate, calculatePrice, validateEmail, parseQuery, ... }
```

### 3. Deep Re-exports
```typescript
// ❌ components/index.ts re-exporting from 20 files
export * from './Button'
export * from './Input'
// ... LLM can't find actual implementation
```

### 4. Inline Large Data
```typescript
// ❌ 200 lines of JSON inside component
const features = [{ id: 1, ... }, /* 50 more objects */]
```

### 5. Ambiguous File Names
```typescript
// ❌ What do these files do?
helpers.ts, utils.ts, common.ts, shared.ts, misc.ts
```

## CLAUDE.md Template for Projects

Every project should have a CLAUDE.md explaining structure:

```markdown
# Project Name

## Structure
- `src/components/` - Shared UI components
- `src/features/` - Feature modules (landing, auth, dashboard)
- `src/data/` - Static data and constants
- `src/pages/` - Route entry points (thin orchestrators)

## Key Files
- `src/data/pricing.ts` - Pricing plans and features
- `src/features/landing/` - Landing page sections

## Conventions
- Components: PascalCase, max 200 lines
- Data: Extract to src/data/, import in components
- Pages: Thin, compose from features/

## Commands
npm run dev    # Development
npm run build  # Production build
```

## Migration Checklist

When refactoring existing codebase:

1. [ ] Identify files > 300 lines
2. [ ] Extract data to `src/data/`
3. [ ] Split large components into features/
4. [ ] Flatten deep directory structures
5. [ ] Rename ambiguous files
6. [ ] Add JSDoc to complex functions
7. [ ] Create/update CLAUDE.md
8. [ ] Verify all imports are explicit

## Related Methodologies

- `react-component-architecture.md` - Component patterns
- `clean-architecture.md` - Layered architecture
- `typescript-strict-mode.md` - Type safety patterns
