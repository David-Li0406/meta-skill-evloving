---
name: frontend-code-quality
description: Provides code quality standards for frontend applications. This skill should be used when configuring linting rules, organizing file structures, or ensuring consistency across React applications.
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

- **Components**: PascalCase (e.g., `UserProfile.tsx`).
- **Hooks**: camelCase with use prefix (e.g., `useAuth.ts`).
- **Utilities**: camelCase (e.g., `formatDate.ts`).
- **Routes**: File-based routing conventions of TanStack Router (e.g., `posts/$postId.tsx`).

## Best Practices

1.  **Strict Props**: Define specific interfaces for props, avoid `any` or broad `object` types.
2.  **Server State separation**: Use TanStack Query for server data; use `React.useState`/`useReducer` only for local UI state.
3.  **Composition over Inheritance**: Build complex UIs by composing small, focused components.

## Checklist

- [ ] `pnpm lint` passes without errors.
- [ ] `pnpm test` passes.
- [ ] Component names match their filenames.
- [ ] Complex logic extracted to custom hooks.
