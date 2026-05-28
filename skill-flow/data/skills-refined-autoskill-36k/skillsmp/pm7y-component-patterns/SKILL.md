---
name: pm7y-component-patterns
description: |
  Discovers existing React component patterns (file structure, state management, naming conventions, prop patterns, TypeScript conventions) in a codebase before writing new components. Produces a "use these patterns" summary to ensure consistency.

  Use this skill when:
  - About to write a new React component
  - Before creating a new feature with multiple components
  - When unsure what patterns or conventions exist in a codebase
  - Before a code review to understand existing patterns
allowed-tools: Read, Glob, Grep
---

# React Component Pattern Discovery Skill

Discovers existing React component patterns in a codebase to ensure new components follow established conventions.

---

## Overview

This skill scans a codebase to build a comprehensive inventory of:

- **File structure** - How components are organized and named
- **Component patterns** - Functional vs class, hooks usage, composition patterns
- **State management** - Local state, context, Redux, Zustand, etc.
- **Prop patterns** - TypeScript interfaces, default props, destructuring
- **Naming conventions** - Files, components, props, handlers, types

**Output:** A "Use These Patterns" summary that provides actionable guidance for writing new components.

**When to use:**

- Before writing a new React component
- Before creating a feature with multiple components
- When onboarding to an unfamiliar React codebase
- Before reviewing component code to understand expectations

---

## Discovery Process

### Step 1: Find All Component Files

Locate React component files in the project:

```
# Search patterns
**/components/**/*.tsx
**/components/**/*.jsx
**/*.component.tsx
**/pages/**/*.tsx
**/views/**/*.tsx
**/features/**/*.tsx

# Exclude patterns
node_modules/
dist/
build/
.next/
coverage/
**/*.test.tsx
**/*.spec.tsx
**/*.stories.tsx
```

Record the file structure - note organizational patterns like:
- Feature-based: `features/[Feature]/components/`
- Flat: `components/[Component].tsx`
- Nested: `components/[Component]/[Component].tsx`
- Atomic design: `atoms/`, `molecules/`, `organisms/`

### Step 2: Analyze File Structure Patterns

For each component directory, identify:

**Colocated files:**
- `Component.tsx` - Main component
- `Component.styles.ts` or `Component.scss` - Styles
- `Component.test.tsx` - Tests
- `Component.types.ts` - TypeScript types
- `index.ts` - Barrel export
- `hooks/` - Component-specific hooks
- `utils/` - Component-specific utilities

**Naming patterns:**
| Pattern | Example |
|---------|---------|
| PascalCase files | `UserProfile.tsx` |
| kebab-case files | `user-profile.tsx` |
| Index exports | `components/Button/index.tsx` |
| Suffixed files | `UserProfile.component.tsx` |

### Step 3: Analyze Component Patterns

Search for component definition patterns:

**Functional components:**
```
Pattern: (export const|export default function|const) \w+ = \(|: (React\.)?FC
```

**Class components:**
```
Pattern: class \w+ extends (React\.)?(Component|PureComponent)
```

**Component patterns to identify:**

| Pattern | Indicator |
|---------|-----------|
| Arrow function | `const Component = () =>` |
| Function declaration | `function Component()` |
| Typed FC | `const Component: FC<Props>` or `React.FC<Props>` |
| forwardRef | `forwardRef<Ref, Props>` |
| memo | `React.memo(Component)` |

### Step 4: Analyze Props and TypeScript Patterns

Search for prop type definitions:

**Interface patterns:**
```
Pattern: interface \w+Props
Pattern: type \w+Props =
```

Identify TypeScript conventions:

| Convention | Example |
|------------|---------|
| Props interface | `interface ButtonProps { ... }` |
| Props type | `type ButtonProps = { ... }` |
| Inline props | `({ label, onClick }: { label: string; onClick: () => void })` |
| Generic props | `interface ListProps<T> { items: T[] }` |

**Common prop patterns:**
- Children handling: `children: React.ReactNode` vs `children: ReactNode`
- Event handlers: `onClick`, `onSubmit`, `onChange` naming
- Render props: `render*` or `*Renderer` props
- Ref forwarding: `forwardRef` usage

### Step 5: Analyze State Management

**Local state:**
```
Pattern: useState<
Pattern: useReducer<
```

**Context usage:**
```
Pattern: createContext
Pattern: useContext
Pattern: \.Provider
```

**External state libraries:**

| Library | Indicators |
|---------|------------|
| Redux | `useSelector`, `useDispatch`, `connect` |
| Redux Toolkit | `createSlice`, `configureStore` |
| Zustand | `create()`, `useStore` |
| Jotai | `atom(`, `useAtom` |
| Recoil | `atom({`, `useRecoilState` |
| MobX | `observer(`, `makeObservable` |
| TanStack Query | `useQuery`, `useMutation`, `QueryClient` |

### Step 6: Analyze Hooks Patterns

Search for custom hooks:

```
Pattern: (export )?(const|function) use[A-Z]
```

Identify hook patterns:
- Location: `hooks/` directory vs colocated
- Naming: `use[Feature]` convention
- Return type: tuple, object, or single value

**Common hook patterns:**
- Data fetching hooks: `useFetch*`, `useGet*`, `useLoad*`
- Form hooks: `useForm`, `useField`, `useValidation`
- UI state hooks: `useToggle`, `useModal`, `useDisclosure`
- Side effect hooks: `useDebounce`, `useInterval`, `useEventListener`

### Step 7: Analyze Import/Export Patterns

**Import organization:**
```
# Check first 20-30 lines of component files for patterns
```

Identify ordering conventions:
1. React imports
2. Third-party imports
3. Internal imports (absolute paths)
4. Relative imports
5. Type imports
6. Style imports

**Export patterns:**
- Default exports: `export default Component`
- Named exports: `export { Component }`
- Barrel exports: `index.ts` files

### Step 8: Analyze Composition Patterns

**Children patterns:**
```
Pattern: {children}
Pattern: React\.Children
Pattern: cloneElement
```

**Render prop patterns:**
```
Pattern: render[A-Z]\w*=
```

**Compound components:**
```
Pattern: \w+\.\w+ =
Example: Menu.Item, Dialog.Title
```

---

## Output Format

After completing discovery, produce a summary in this format:

```markdown
## Use These Patterns

### File Structure

**Component organization:**
- Location: `src/components/[Category]/[Component]/`
- Files per component: `Component.tsx`, `Component.styles.ts`, `index.ts`

**Naming conventions:**
- Files: PascalCase (`UserProfile.tsx`)
- Components: PascalCase (`UserProfile`)
- Props interfaces: `[Component]Props`
- Hooks: `use[Feature]`

### Component Definition

**Preferred pattern:**
```tsx
interface ComponentProps {
  // props
}

export const Component = ({ prop1, prop2 }: ComponentProps) => {
  return (...)
}
```

**Common patterns used:**
- [ ] Arrow functions with explicit return
- [ ] Arrow functions with implicit return
- [ ] Function declarations
- [ ] React.FC type annotation
- [ ] forwardRef for ref forwarding
- [ ] memo for optimization

### Props Patterns

**TypeScript conventions:**
- Props defined as: `interface [Component]Props`
- Optional props: `prop?: type`
- Children type: `React.ReactNode`
- Event handlers: `on[Event]: () => void`

**Common prop patterns:**
- Destructuring in function signature
- Default values via destructuring: `{ prop = defaultValue }`
- Spread props for flexibility: `...rest`

### State Management

**Local state:**
- `useState` for simple state
- `useReducer` for complex state

**Global state:**
- [Library name] for [use case]
- Context for [use case]

### Hooks

**Custom hooks location:** `src/hooks/` or colocated

**Existing hooks:**
| Hook | Purpose |
|------|---------|
| `useAuth` | Authentication state |
| `useFetch` | Data fetching |
| [list discovered hooks] |

### Import Organization

```tsx
// 1. React
import { useState, useEffect } from 'react'

// 2. Third-party
import { motion } from 'framer-motion'

// 3. Internal (absolute)
import { Button } from '@/components/Button'

// 4. Relative
import { useLocalHook } from './hooks'

// 5. Types
import type { ComponentProps } from './types'

// 6. Styles
import styles from './Component.module.css'
```

### Export Patterns

**Preferred export style:** [named/default]

**Barrel exports:** [yes/no, pattern if yes]
```
```

---

## Discovery Checklist

Before producing the summary:

- [ ] Found all component files (excluding tests, stories, node_modules)
- [ ] Identified file structure pattern (flat, nested, feature-based)
- [ ] Identified file naming convention
- [ ] Identified component definition pattern (arrow, function, FC)
- [ ] Found TypeScript props patterns (interface, type, inline)
- [ ] Identified state management approach (local, context, library)
- [ ] Found custom hooks and their patterns
- [ ] Identified import organization convention
- [ ] Identified export pattern (named, default, barrel)
- [ ] Noted composition patterns (children, render props, compound)
- [ ] Summary uses consistent formatting
- [ ] Summary includes code examples matching codebase style

---

## Constraints

### DO:
- Focus on discovery only - do not modify any files
- Include actual code examples from the codebase
- Group related patterns together
- Note the most common pattern when multiple exist
- Identify any inconsistencies (but don't judge or try to fix them)

### DO NOT:
- Create new components or patterns
- Modify existing files
- Make recommendations for changes
- Judge the quality of existing patterns
- Spend time on files in node_modules, dist, or build directories
- Include test files, stories, or mocks in pattern analysis

---

## Example Output

For a typical React TypeScript project:

```markdown
## Use These Patterns

### File Structure

**Component organization:**
- Location: `src/components/[Component]/`
- Files: `[Component].tsx`, `[Component].styles.ts`, `[Component].test.tsx`, `index.ts`

**Naming conventions:**
- Files: PascalCase (`Button.tsx`)
- Components: PascalCase (`Button`)
- Props interfaces: `[Component]Props` (`ButtonProps`)
- Event handlers: `on[Event]` (`onClick`, `onSubmit`)
- Boolean props: `is[State]` or `has[Thing]` (`isDisabled`, `hasError`)

### Component Definition

**Preferred pattern:**
```tsx
import { forwardRef } from 'react'
import type { ButtonProps } from './Button.types'
import styles from './Button.styles'

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', isDisabled = false, onClick, ...rest }, ref) => {
    return (
      <button
        ref={ref}
        className={styles.button}
        data-variant={variant}
        disabled={isDisabled}
        onClick={onClick}
        {...rest}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

**Patterns observed:**
- forwardRef for all interactive elements
- Destructuring props with defaults in signature
- Spread rest props to underlying element
- displayName set for debugging

### Props Patterns

**TypeScript conventions:**
```tsx
// Props interface in separate .types.ts file
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}
```

- Extends native HTML element props
- Optional props have defaults in component
- Union types for variants
- Boolean props prefixed with `is` or `has`

### State Management

**Local state:** `useState` for UI state, `useReducer` for complex forms

**Global state:**
- Zustand for client state (`src/store/`)
- TanStack Query for server state

**Context:**
- `ThemeContext` for theming
- `AuthContext` for authentication

### Hooks

**Location:** `src/hooks/` for shared, colocated for component-specific

**Existing shared hooks:**
| Hook | Purpose | Returns |
|------|---------|---------|
| `useAuth` | Auth state & methods | `{ user, login, logout, isLoading }` |
| `useMediaQuery` | Responsive breakpoints | `boolean` |
| `useLocalStorage` | Persistent state | `[value, setValue]` |
| `useDebounce` | Debounced values | `debouncedValue` |

### Import Organization

```tsx
// React (no 'react' package - using automatic JSX transform)
import { useState, useCallback } from 'react'

// Third-party
import { motion, AnimatePresence } from 'framer-motion'
import clsx from 'clsx'

// Internal - absolute (@/ alias)
import { Button } from '@/components/Button'
import { useAuth } from '@/hooks/useAuth'
import { api } from '@/lib/api'

// Internal - relative
import { useLocalState } from './hooks'
import { formatData } from './utils'

// Types (type-only imports)
import type { User } from '@/types'

// Styles
import styles from './Component.module.css'
```

### Export Patterns

**Style:** Named exports preferred

**Barrel pattern:**
```tsx
// components/Button/index.ts
export { Button } from './Button'
export type { ButtonProps } from './Button.types'
```
```

---

## When Discovery Finds Minimal Patterns

If the codebase has few established React patterns:

```markdown
## Use These Patterns

### Status: Minimal existing patterns

This codebase has few established component patterns. Consider establishing:
- Consistent file structure (recommend: colocated files with index barrel)
- Component definition style (recommend: arrow functions with typed props)
- Props interface convention (recommend: `[Component]Props` interface)
- Import organization order

### Files Found
- [list any component files found]

### Framework: [React version detected]

### TypeScript: [yes/no, strict mode status]
```

This allows the user to make informed decisions about establishing new patterns.
