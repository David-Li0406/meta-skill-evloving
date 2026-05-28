---
name: frontend-code-quality
description: Use this skill when configuring linting rules, organizing file structures, or ensuring consistency across frontend applications, particularly those built with React.
---

# Frontend Code Quality

This skill defines the quality standards specific to frontend applications.

## Linting & Formatting

We use **ESLint 9** with a shared configuration (`@eridu/eslint-config`).

- **Command**: `pnpm lint` (runs `eslint . --fix`)
- **Rules**:
    - No `any` types.
    - React Hooks rules enforced (`react-hooks/rules-of-hooks`, `react-hooks/exhaustive-deps`).
    - Standard imports sorting.

## Absolute Imports

Always configure and use absolute imports to avoid messy relative paths like `../../../component`. This makes it easier to move files around without breaking imports.

**Configuration** (`tsconfig.json`):

```json
"compilerOptions": {
  "baseUrl": ".",
  "paths": {
    "@/*": ["./src/*"]
  }
}
```

**Usage**:

```typescript
// ✅ GOOD: Absolute import
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

// ❌ BAD: Relative import
import { Button } from '../../../components/Button';
```

**Benefits**:
- Files can be moved without updating imports.
- Clear distinction between workspace packages (`@eridu/ui`) and source code (`@/*`).
- More readable and maintainable.

## Testing

We use **Vitest** for unit and component testing.

- **Command**: `pnpm test`
- **Environment**: `happy-dom`
- **Testing Library**: `@testing-library/react` for component interactions.

### Component Test Example

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@eridu/ui/components/button';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
});
```

## File Structure & Naming

### Naming Conventions

- **Components**: PascalCase (e.g., `UserProfile.tsx`).
- **Hooks**: camelCase with use prefix (e.g., `useAuth.ts`).
- **Utilities**: camelCase (e.g., `formatDate.ts`).
- **Routes**: File-based routing conventions of TanStack Router (e.g., `posts/$postId.tsx`).
- **Folders**: kebab-case (e.g., `user-profile/`, `auth-forms/`).

### Enforcing Naming Conventions

Use ESLint to enforce consistent file naming:

```javascript
// .eslintrc.cjs
'check-file/filename-naming-convention': [
  'error',
  {
    '**/*.{ts,tsx}': 'KEBAB_CASE',
  },
  {
    ignore: ['**/node_modules/**'],
  },
],
```

## Best Practices

1. **Strict Props**: Define specific interfaces for props, avoid `any` or broad `object` types.
2. **Server State Separation**: Use TanStack Query for server data; use `React.useState`/`useReducer` only for local UI state.
3. **Composition over Inheritance**: Build complex UIs by composing small, focused components.

## Checklist

- [ ] `pnpm lint` passes without errors.
- [ ] `pnpm test` passes.
- [ ] Component names match their filenames.
- [ ] Complex logic extracted to custom hooks.