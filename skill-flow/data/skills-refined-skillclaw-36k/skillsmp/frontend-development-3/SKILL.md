---
name: frontend-development
description: Provides specialized guidance for frontend development including UI/UX best practices, performance optimization, component architecture, and modern tooling recommendations. Use when working on frontend code, React components, UI design, styling, user interfaces, or when the user mentions frontend, UI, UX, or client-side development.
---

# Frontend Development

## Core Principles

When developing frontend code:

1. **Simplicity First**: Keep interfaces clean and intuitive; avoid unnecessary complexity
2. **Performance**: Optimize for fast load times, smooth animations, and responsive interactions
3. **Beauty Through Function**: Design should enhance usability, not hinder it
4. **Accessibility**: Ensure interfaces work for all users (WCAG compliance)
5. **Mobile-First**: Design for mobile devices first, then enhance for larger screens

## Starting from Scratch

When creating a new frontend project, consider these proven stacks:

### React-Based Stacks

**Vite + React + TypeScript** (Recommended for most projects)
- Fast build tool with excellent DX
- Hot module replacement
- Type safety with TypeScript
- Packages: `vite`, `react`, `react-dom`, `typescript`

**Next.js** (For full-stack or SSR needs)
- Server-side rendering and static generation
- Built-in routing and API routes
- Excellent performance out of the box
- Packages: `next`, `react`, `react-dom`

### Styling Solutions

**Tailwind CSS** (Recommended for rapid, consistent styling)
- Utility-first CSS framework
- Small bundle size with purging
- Excellent documentation
- Packages: `tailwindcss`, `autoprefixer`, `postcss`

**CSS Modules** (For component-scoped styles)
- Scoped styles without runtime overhead
- Works with any build tool
- No additional packages needed (built into most tools)

**Styled Components** (For CSS-in-JS)
- Component-level styling with JavaScript
- Dynamic styling based on props
- Packages: `styled-components`

### UI Component Libraries

**shadcn/ui** (Highly recommended - copy/paste components)
- Beautiful, accessible components
- Fully customizable
- Built on Radix UI primitives
- No runtime dependencies
- Repository: https://github.com/shadcn-ui/ui

**Radix UI** (Headless, accessible primitives)
- Unstyled, accessible components
- Full control over styling
- Packages: `@radix-ui/react-*`

**Mantine** (Complete component library)
- Comprehensive component set
- Built-in theming and dark mode
- Packages: `@mantine/core`, `@mantine/hooks`

### State Management

**Zustand** (Simple, lightweight)
- Minimal boilerplate
- Works great with React
- Packages: `zustand`

**React Query / TanStack Query** (For server state)
- Excellent for API data fetching
- Built-in caching and synchronization
- Packages: `@tanstack/react-query`

**Context API** (For simple global state)
- Built into React
- No additional packages needed

### Form Handling

**React Hook Form** (Recommended)
- Minimal re-renders
- Great performance
- Easy validation
- Packages: `react-hook-form`, `@hookform/resolvers` (for Zod/Yup)

**Zod** (Schema validation)
- TypeScript-first validation
- Works great with React Hook Form
- Packages: `zod`

## Component Architecture

### Component Structure

```typescript
// ✅ GOOD - Clear separation of concerns
components/
  Button/
    Button.tsx          # Component logic
    Button.test.tsx     # Tests
    Button.module.css   # Styles (if using CSS Modules)
    index.ts            # Export
```

### Component Patterns

```typescript
// ✅ GOOD - Simple, focused component
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  );
};
```

### Composition Pattern

```typescript
// ✅ GOOD - Composable components
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

## Performance Optimization

### Code Splitting

```typescript
// ✅ GOOD - Lazy load routes
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Memoization

```typescript
// ✅ GOOD - Memoize expensive components
import { memo, useMemo } from 'react';

const ExpensiveComponent = memo(({ data }) => {
  const processedData = useMemo(
    () => expensiveCalculation(data),
    [data]
  );
  
  return <div>{processedData}</div>;
});
```

### Image Optimization

```typescript
// ✅ GOOD - Optimize images
// Use next/image for Next.js
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={500}
  height={300}
  loading="lazy"
/>

// Or use a library like react-lazy-load-image-component
```

## Styling Best Practices

### CSS Organization

```css
/* ✅ GOOD - Organized CSS */
/* 1. Variables */
:root {
  --color-primary: #3b82f6;
  --spacing-md: 1rem;
}

/* 2. Base styles */
* {
  box-sizing: border-box;
}

/* 3. Component styles */
.button {
  padding: var(--spacing-md);
  background: var(--color-primary);
}
```

### Responsive Design

```css
/* ✅ GOOD - Mobile-first approach */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 3rem;
  }
}
```

### Tailwind CSS Patterns

```typescript
// ✅ GOOD - Tailwind utility classes
<button className="
  px-4 py-2 
  bg-blue-500 hover:bg-blue-600 
  text-white font-semibold 
  rounded-lg 
  transition-colors
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Click me
</button>
```

## Accessibility

### Semantic HTML

```typescript
// ✅ GOOD - Semantic elements
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>
```

### ARIA Attributes

```typescript
// ✅ GOOD - Proper ARIA usage
<button
  aria-label="Close dialog"
  aria-expanded={isOpen}
  onClick={handleClose}
>
  ×
</button>

<div role="alert" aria-live="polite">
  {errorMessage}
</div>
```

### Keyboard Navigation

```typescript
// ✅ GOOD - Keyboard support
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Escape') {
    onClose();
  }
  if (e.key === 'Enter' || e.key === ' ') {
    onClick();
  }
};
```

## Animation & Interactions

### CSS Transitions

```css
/* ✅ GOOD - Smooth transitions */
.button {
  transition: all 0.2s ease-in-out;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Animation Libraries

**Framer Motion** (Recommended for React)
- Declarative animations
- Great performance
- Packages: `framer-motion`

**React Spring** (Physics-based animations)
- Natural motion
- Packages: `@react-spring/web`

## Testing

### Component Testing

```typescript
// ✅ GOOD - Test user interactions
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);
  
  fireEvent.click(screen.getByText('Click me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

## Recommended Open Source Repositories

### UI Component Libraries
- **shadcn/ui**: https://github.com/shadcn-ui/ui (Copy/paste components)
- **Radix UI**: https://github.com/radix-ui/primitives (Accessible primitives)
- **Headless UI**: https://github.com/tailwindlabs/headlessui (Unstyled components)

### Starter Templates
- **Vite React Template**: https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts
- **Next.js Examples**: https://github.com/vercel/next.js/tree/canary/examples

### Design Systems
- **Material UI**: https://github.com/mui/material-ui
- **Chakra UI**: https://github.com/chakra-ui/chakra-ui
- **Ant Design**: https://github.com/ant-design/ant-design

### Utilities
- **clsx**: https://github.com/lukeed/clsx (Conditional className utility)
- **date-fns**: https://github.com/date-fns/date-fns (Date manipulation)
- **react-icons**: https://github.com/react-icons/react-icons (Icon library)

## Common Patterns

### Custom Hooks

```typescript
// ✅ GOOD - Reusable logic
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    setStoredValue(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  };

  return [storedValue, setValue] as const;
}
```

### Error Boundaries

```typescript
// ✅ GOOD - Catch component errors
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

## Performance Checklist

- [ ] Code splitting for routes and large components
- [ ] Lazy loading images
- [ ] Memoization for expensive calculations
- [ ] Virtual scrolling for long lists
- [ ] Debounce/throttle for frequent events
- [ ] Bundle size optimization (tree shaking)
- [ ] Minimize re-renders with React.memo
- [ ] Use production builds for performance testing

## Quick Start Checklist

When starting a new project:

1. **Choose your stack**: Vite + React + TypeScript (or Next.js)
2. **Add styling**: Tailwind CSS or CSS Modules
3. **Add components**: shadcn/ui or your preferred library
4. **Add state management**: Zustand or Context API
5. **Add forms**: React Hook Form + Zod
6. **Add routing**: React Router (or Next.js routing)
7. **Add testing**: Vitest + React Testing Library
8. **Configure build**: Optimize for production
