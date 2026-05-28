---
name: react-components
description: Use this skill when creating or modifying React components and hooks with TypeScript, following best practices for structure and performance.
---

# React Components

You write modern React components and hooks using TypeScript, adhering to best practices for structure, performance, and accessibility. This skill covers the creation of functional components, custom hooks, and efficient coding patterns.

## Tech Stack Assumptions

| Technology | Default |
|------------|---------|
| React | 18+ with concurrent features |
| TypeScript | For type safety |
| Components | Functional with hooks |
| Package Manager | pnpm |
| Build Tool | Vite or Next.js |
| Styling | Tailwind CSS |
| Testing | Vitest or Jest |

## Component Structure

- Use functional components only (no classes).
- Avoid `import React from 'react'` — import components individually.
- Do not use the `React.*` namespace (e.g., `React.useState`).
- Export default in a single expression.
- TypeScript infers return types for components.

### Example

```tsx
import { useState, type ReactNode } from 'react';

export default function MyComponent() {
  return <div>Hello</div>;
}
```

## Component Patterns

### Basic Functional Component

```tsx
import { FC } from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  const baseClasses = 'px-4 py-2 rounded-md font-medium transition-colors';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-400',
    secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]}`}
    >
      {label}
    </button>
  );
};
```

### Component with Children

```tsx
import { FC, ReactNode } from 'react';

interface CardProps {
  title: string;
  children: ReactNode;
  footer?: ReactNode;
}

export const Card: FC<CardProps> = ({ title, children, footer }) => {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      </div>
      <div className="px-6 py-4">{children}</div>
      {footer && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          {footer}
        </div>
      )}
    </div>
  );
};
```

## Hooks

- Use `useState` generics only for unions or complex types (not for `string`, `boolean`, `number`).
- Avoid `useCallback` for same-component functions; it's acceptable for functions returned from custom hooks.
- Use named functions (not arrow functions) for async or complex logic inside hooks.

### Example

```tsx
const [name, setName] = useState(''); // no generic needed
const [status, setStatus] = useState<'a' | 'b'>('a'); // union needs generic

useEffect(() => {
  async function fetchData() {
    const res = await fetch('/api');
  }
  void fetchData();
}, []);
```

## Performance Optimization

| Technique | Use Case |
|-----------|----------|
| `useMemo` | Expensive calculations (sorting, filtering) |
| `useCallback` | Functions passed to memoized children |
| `memo` | Pure components that re-render often with same props |
| `lazy` + `Suspense` | Code splitting routes and heavy components |

## File Organization

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   ├── forms/           # Form components
│   └── layout/          # Layout components
├── hooks/               # Custom hooks
│   ├── useApi.ts
│   ├── useForm.ts
│   └── useLocalStorage.ts
├── pages/               # Page components
├── types/               # TypeScript types
└── utils/               # Utility functions
```

## Output Format

After creating components:

1. **Files Created** - List of new files with paths.
2. **Components** - Key components and their purpose.
3. **Hooks** - Custom hooks created.
4. **Types** - TypeScript interfaces/types defined.
5. **Next Steps** - Testing, integration, styling.

## Other Rules

- Follow accessibility best practices.
- Use `displayName` only for `forwardRef` components.
- Use fragments `<>` only for multiple siblings.

### Example

```tsx
const MyInput = forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
));
MyInput.displayName = 'MyInput';
```