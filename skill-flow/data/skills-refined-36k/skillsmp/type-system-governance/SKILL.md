---
name: type-system-governance
description: Enforce TypeScript type organization rules. Use when creating types, interfaces, or DTOs. All types MUST go in /types directory - never inline in components.
---

# Type System Governance

⚠️ **ALL types and interfaces MUST be defined in the `/types` directory.**

This skill enforces strict type organization to prevent duplication, maintain DRY principle, and ensure consistent type imports across the codebase.

---

## 🚨 THE GOLDEN RULE

```typescript
// ❌ FORBIDDEN: Type defined outside /types
// File: components/ui/Button.tsx
type ButtonProps = { variant: string }; // WRONG!

// ✅ REQUIRED: Type defined in /types
// File: types/props.ts
export interface ButtonProps {
  variant: ButtonVariant;
}

// File: components/ui/Button.tsx
import type { ButtonProps } from "types/props";
```

**ESLint enforces this rule** - you will get lint errors for inline types.

---

## 📁 Type Organization Structure

```text
types/
├── README.md              # Type organization guide (READ THIS FIRST)
├── common.ts              # Shared UI types
│   ├── NavigationItem
│   ├── SocialLinks
│   └── ...
├── props.ts               # Component props types
│   ├── ButtonProps
│   ├── CardProps
│   └── ...
├── event.ts               # Event domain types
│   ├── EventFilters
│   ├── EventCardData
│   └── distanceToRadius()
├── filters.ts             # Filter system types
│   ├── FilterConfig
│   ├── FilterState
│   └── ...
├── i18n.ts                # i18n types
│   ├── Locale
│   ├── SupportedLocale
│   └── ...
├── api/                   # API DTOs
│   ├── event.ts           # EventDTO, EventResponseDTO
│   ├── news.ts            # NewsDTO, NewsResponseDTO
│   ├── city.ts            # CitySummaryResponseDTO
│   ├── region.ts          # RegionDTO
│   └── category.ts        # CategoryDTO
└── index.ts               # Re-exports (optional)
```

---

## ✅ Step-by-Step: Adding a New Type

### 1. Determine the Canonical Location

| Type Category    | Location                | Example            |
| ---------------- | ----------------------- | ------------------ |
| API response DTO | `types/api/<domain>.ts` | `EventResponseDTO` |
| Component props  | `types/props.ts`        | `ButtonProps`      |
| Shared UI types  | `types/common.ts`       | `NavigationItem`   |
| Domain-specific  | `types/<domain>.ts`     | `FilterConfig`     |
| Utility types    | Near usage in `types/`  | `DateRange`        |

### 2. Check for Existing Types

```bash
# Search for existing types
grep -r "interface\|type " types/ --include="*.ts"

# Search for specific type name
grep -r "ButtonProps\|CardProps" types/

# Check canonical sources
cat types/common.ts | grep "export"
cat types/props.ts | grep "export"
```

### 3. Add Type to Correct File

```typescript
// types/props.ts
export interface NewComponentProps {
  variant: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
}
```

### 4. Import and Use

```typescript
// components/ui/NewComponent.tsx
import type { NewComponentProps } from "types/props";

export function NewComponent({
  variant,
  size = "md",
  children,
}: NewComponentProps) {
  // ...
}
```

---

## 🚫 Common Violations (And How to Fix)

### ❌ Violation 1: Inline Type Definition

```typescript
// WRONG: Type in component file
// components/ui/Card.tsx
type CardProps = {
  title: string;
  description: string;
};

export function Card({ title, description }: CardProps) {
  /* ... */
}
```

**Fix:**

```typescript
// types/props.ts
export interface CardProps {
  title: string;
  description: string;
}

// components/ui/Card.tsx
import type { CardProps } from "types/props";

export function Card({ title, description }: CardProps) {
  /* ... */
}
```

### ❌ Violation 2: Duplicate Type Definition

```typescript
// WRONG: Same type defined in multiple places
// components/ui/EventCard.tsx
interface Event {
  id: number;
  title: string;
}

// components/ui/EventList.tsx
interface Event {
  id: number;
  title: string;
} // Duplicate!
```

**Fix:**

```typescript
// types/event.ts
export interface Event {
  id: number;
  title: string;
}

// Both components import from same source
import type { Event } from "types/event";
```

### ❌ Violation 3: API DTO Not in /types/api

```typescript
// WRONG: DTO defined in lib/api
// lib/api/events.ts
interface EventResponse {
  content: Event[];
  totalPages: number;
}
```

**Fix:**

```typescript
// types/api/event.ts
export interface EventResponseDTO {
  content: EventDTO[];
  totalPages: number;
  totalElements: number;
  last: boolean;
}

// lib/api/events.ts
import type { EventResponseDTO } from "types/api/event";
```

### ❌ Violation 4: Using `any`

```typescript
// WRONG: Using any
const handleData = (data: any) => {
  /* ... */
};
```

**Fix:**

```typescript
// Use unknown with proper narrowing
const handleData = (data: unknown) => {
  if (isEventData(data)) {
    // data is now typed as EventData
  }
};

// Or define proper type
import type { EventData } from "types/event";
const handleData = (data: EventData) => {
  /* ... */
};
```

---

## 📋 Type Consolidation Workflow

When you find duplicate types:

### Step 1: Identify Duplicates

```bash
# Find all type definitions
grep -r "interface\|type " --include="*.ts" --include="*.tsx" | grep -v "types/"

# Check for specific duplicates
grep -rn "interface Event\|type Event" --include="*.ts"
```

### Step 2: Choose Canonical Location

- Is it a DTO? → `types/api/<domain>.ts`
- Is it UI props? → `types/props.ts`
- Is it shared? → `types/common.ts`
- Is it domain-specific? → `types/<domain>.ts`

### Step 3: Consolidate

```typescript
// Move to canonical location
// types/common.ts
export interface ConsolidatedType {
  // ...
}
```

### Step 4: Update All Imports

```bash
# Find all usages
grep -rn "ConsolidatedType" --include="*.ts" --include="*.tsx"

# Update imports in each file
import type { ConsolidatedType } from 'types/common';
```

### Step 5: Verify

```bash
yarn typecheck && yarn lint
```

---

## 🔧 Quick Reference: Canonical Sources

| Type                     | Canonical File       | Import Path       |
| ------------------------ | -------------------- | ----------------- |
| `NavigationItem`         | `types/common.ts`    | `types/common`    |
| `SocialLinks`            | `types/common.ts`    | `types/common`    |
| `ButtonProps`            | `types/props.ts`     | `types/props`     |
| `EventDTO`               | `types/api/event.ts` | `types/api/event` |
| `FilterConfig`           | `types/filters.ts`   | `types/filters`   |
| `CitySummaryResponseDTO` | `types/api/city.ts`  | `types/api/city`  |
| `Locale`                 | `types/i18n.ts`      | `types/i18n`      |

---

## ✅ Verification Checklist

Before submitting code with types:

- [ ] All types defined in `/types` directory
- [ ] No inline `type` or `interface` in components
- [ ] Checked `types/README.md` for existing patterns
- [ ] No duplicate type definitions
- [ ] Using `unknown` instead of `any` where needed
- [ ] Props types in `types/props.ts`
- [ ] API DTOs in `types/api/*.ts`
- [ ] `yarn typecheck` passes
- [ ] `yarn lint` passes (ESLint catches inline types)

---

## 🔍 ESLint Rule Enforcement

This project has ESLint rules that **block** type definitions outside `/types`:

```javascript
// eslint.config.mjs
{
  rules: {
    'no-restricted-syntax': [
      'error',
      {
        selector: 'TSTypeAliasDeclaration',
        message: 'Type aliases must be defined in /types directory'
      },
      {
        selector: 'TSInterfaceDeclaration',
        message: 'Interfaces must be defined in /types directory'
      }
    ]
  }
}
```

**If you see this error**, move your type to the appropriate file in `/types`.

---

## 💡 Pro Tips

### Use Path Aliases

```typescript
// ✅ Good: Use path alias
import type { Event } from "types/event";

// ❌ Avoid: Relative paths
import type { Event } from "../../../types/event";
```

### Export Types Properly

```typescript
// types/event.ts
export interface Event {
  /* ... */
}
export type EventStatus = "draft" | "published";

// Re-export if needed
// types/index.ts
export type { Event, EventStatus } from "./event";
```

### Type vs Interface

```typescript
// Use interface for objects (extendable)
export interface Event {
  id: number;
  title: string;
}

// Use type for unions, primitives, computed types
export type EventStatus = "draft" | "published" | "archived";
export type EventId = Event["id"];
```

---

**Remember**: Types in `/types` directory = maintainable codebase.

**Last Updated**: January 15, 2026
