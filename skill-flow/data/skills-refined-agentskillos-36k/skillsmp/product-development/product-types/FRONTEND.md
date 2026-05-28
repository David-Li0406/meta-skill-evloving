# Frontend Applications

Specific guidance for building web applications, SPAs, and user interfaces.

## Product Requirements Focus

### Typical Personas
- **End User**: Primary user of the application
- **Power User**: Heavy user needing efficiency features
- **Administrator**: Manages settings, users, configurations
- **Mobile User**: Uses on mobile devices
- **Accessibility User**: Uses assistive technologies

### Key Questions to Ask
1. What devices and browsers must be supported?
2. What are the accessibility requirements (WCAG level)?
3. Is offline capability needed?
4. What's the expected interaction complexity?
5. Are there existing design systems to follow?

### Frontend-Specific User Stories

```markdown
**As a** user
**I expect to** see feedback immediately when I take an action
**So that** I know the system is responding

**As a** mobile user
**I expect to** complete tasks with touch interactions
**So that** I can use the app on my phone

**As a** user with visual impairments
**I expect to** navigate using a screen reader
**So that** I can access all functionality

**As a** user on slow connections
**I expect to** see progressive loading
**So that** I know content is coming
```

## Design Principles

### UI/UX Best Practices

1. **Immediate Feedback**: Respond to every user action
2. **Clear Hierarchy**: Visual structure guides attention
3. **Consistent Patterns**: Same actions look the same
4. **Error Prevention**: Guide users to success
5. **Accessible by Default**: Not an afterthought
6. **Mobile-First**: Design for constraints first

### Performance Budgets

| Metric | Target | Tool |
|--------|--------|------|
| First Contentful Paint | < 1.8s | Lighthouse |
| Largest Contentful Paint | < 2.5s | Lighthouse |
| Time to Interactive | < 3.8s | Lighthouse |
| Cumulative Layout Shift | < 0.1 | Lighthouse |
| Total Bundle Size | < 200KB (gzipped) | webpack-bundle-analyzer |

### Accessibility Requirements

| Level | Requirements |
|-------|-------------|
| **WCAG A** | Basic accessibility, minimum legal requirement |
| **WCAG AA** | Standard for most applications (recommended) |
| **WCAG AAA** | Highest level, specialized applications |

Key requirements:
- [ ] Keyboard navigation for all interactions
- [ ] Screen reader compatibility
- [ ] Color contrast ratios (4.5:1 for text)
- [ ] Focus indicators visible
- [ ] Alt text for images
- [ ] Form labels and error messages
- [ ] Skip links for navigation

## Architecture Patterns

### Decision: Frontend Architecture

| Pattern | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **SPA (React/Vue/Angular)** | Complex interactions, app-like | Rich UX, state management | SEO challenges, bundle size |
| **SSR (Next.js/Nuxt)** | SEO important, content-heavy | Better SEO, fast initial load | Server required, complexity |
| **Static (Astro/11ty)** | Content sites, documentation | Fast, cheap hosting | Limited interactivity |
| **Hybrid (Islands)** | Mix of static and dynamic | Best of both | Architecture complexity |

### Component Architecture

```
src/
├── components/
│   ├── ui/                    # Generic UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.styles.ts
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── Modal/
│   ├── features/              # Feature-specific components
│   │   ├── auth/
│   │   │   ├── LoginForm/
│   │   │   └── UserMenu/
│   │   └── dashboard/
│   └── layouts/               # Page layouts
│       ├── MainLayout/
│       └── AuthLayout/
├── hooks/                     # Custom React hooks
│   ├── useAuth.ts
│   └── useApi.ts
├── services/                  # API and external services
│   ├── api.ts
│   └── auth.ts
├── store/                     # State management
│   ├── slices/
│   └── store.ts
├── pages/                     # Route pages
│   ├── index.tsx
│   └── dashboard.tsx
├── styles/                    # Global styles
│   ├── variables.css
│   └── global.css
├── types/                     # TypeScript types
│   └── index.ts
└── utils/                     # Utility functions
    └── format.ts
```

### State Management Decision

| Solution | When to Use | Complexity |
|----------|-------------|------------|
| **Local State** | Component-specific state | Low |
| **Context** | Theme, auth, small shared state | Low |
| **React Query/SWR** | Server state, caching | Medium |
| **Redux/Zustand** | Complex client state | Medium-High |
| **Jotai/Recoil** | Atomic state needs | Medium |

```typescript
// State location decision tree
function whereToManageState(state) {
  if (usedByOneComponent) return "useState";
  if (isServerData) return "React Query/SWR";
  if (usedByFewNearbyComponents) return "lift state up";
  if (usedAcrossApp) return "Context or global store";
}
```

## Interface Contracts

### Component Contract Template

```typescript
/**
 * @component Button
 * @description Primary action button with multiple variants
 */

interface ButtonProps {
  /** Button content */
  children: React.ReactNode;

  /** Visual variant */
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';

  /** Size variant */
  size?: 'sm' | 'md' | 'lg';

  /** Full width button */
  fullWidth?: boolean;

  /** Loading state */
  loading?: boolean;

  /** Disabled state */
  disabled?: boolean;

  /** Click handler */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;

  /** HTML type attribute */
  type?: 'button' | 'submit' | 'reset';

  /** Accessible label when content is icon-only */
  'aria-label'?: string;
}

// Usage examples
<Button variant="primary" onClick={handleSave}>Save</Button>
<Button variant="danger" loading={isDeleting}>Delete</Button>
<Button variant="ghost" aria-label="Close"><CloseIcon /></Button>
```

### API Integration Contract

```typescript
// API client types
interface ApiResponse<T> {
  data: T;
  meta?: {
    pagination?: Pagination;
  };
}

interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

// Hook contract
interface UseResourcesReturn {
  data: Resource[] | undefined;
  isLoading: boolean;
  error: ApiError | null;
  refetch: () => void;
  hasNextPage: boolean;
  fetchNextPage: () => void;
}

// Usage
const { data, isLoading, error } = useResources({ filter: 'active' });
```

## Testing Strategy

### Frontend Test Pyramid

```
            /\
           /  \     E2E: Playwright/Cypress
          /----\    - Critical user journeys only
         /      \   - Login, checkout, core flows
        /--------\
       /          \  Integration: Testing Library
      /            \ - Component + context/state
     /              \- API mocking
    /----------------\
   /                  \ Unit: Jest/Vitest
  /                    \- Pure functions
 /                      \- Hooks in isolation
/________________________\
```

### Component Testing

```typescript
// Unit test - isolated component
describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', async () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading spinner when loading', () => {
    render(<Button loading>Save</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });
});
```

### Integration Testing

```typescript
// Integration test - with providers and mocks
describe('LoginForm', () => {
  it('logs in successfully and redirects', async () => {
    const mockLogin = jest.fn().mockResolvedValue({ user: testUser });

    render(
      <AuthProvider>
        <Router>
          <LoginForm onLogin={mockLogin} />
        </Router>
      </AuthProvider>
    );

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password'
      });
    });
  });

  it('shows validation errors for invalid input', async () => {
    render(<LoginForm />);

    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

### E2E Testing

```typescript
// Playwright E2E test
test.describe('Authentication', () => {
  test('user can login and access dashboard', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'password');
    await page.click('[data-testid="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]')).toContainText('Welcome');
  });
});
```

### Accessibility Testing

```typescript
// Automated a11y testing
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Dashboard', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Dashboard />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Code Scaffolding

### Recommended Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── robots.txt
├── src/
│   ├── components/           # See component architecture above
│   ├── hooks/
│   ├── services/
│   ├── store/
│   ├── pages/
│   ├── styles/
│   ├── types/
│   ├── utils/
│   ├── App.tsx
│   └── main.tsx
├── tests/
│   ├── setup.ts
│   ├── mocks/
│   └── e2e/
├── .storybook/               # Component documentation
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

### Component Template

```typescript
// components/ui/Button/Button.tsx
import { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './Button.module.css';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', loading, className, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          styles.button,
          styles[variant],
          styles[size],
          loading && styles.loading,
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Spinner className={styles.spinner} />}
        <span className={clsx(loading && styles.hidden)}>{children}</span>
      </button>
    );
  }
);

Button.displayName = 'Button';
```

## Common Pitfalls to Avoid

1. **Not Handling Loading States**: Always show feedback
2. **Ignoring Error States**: Every API call can fail
3. **Poor Form UX**: Validation on blur, clear errors
4. **Layout Shift**: Reserve space for async content
5. **Over-fetching**: Use pagination, infinite scroll wisely
6. **Missing Keyboard Support**: Tab order, focus management
7. **Forgetting Mobile**: Touch targets, responsive design
8. **Giant Bundles**: Code split, lazy load routes
9. **No Optimistic Updates**: Update UI before server confirms
10. **Accessibility Afterthought**: Build accessible from start

## Performance Optimization

### Loading Strategies

```typescript
// Route-based code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

// Component-based code splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));

// Suspense for loading states
<Suspense fallback={<PageSkeleton />}>
  <Dashboard />
</Suspense>
```

### Image Optimization

```typescript
// Responsive images
<img
  src="/image.jpg"
  srcSet="/image-400.jpg 400w, /image-800.jpg 800w"
  sizes="(max-width: 600px) 400px, 800px"
  loading="lazy"
  alt="Description"
/>

// Modern formats with fallback
<picture>
  <source srcSet="/image.avif" type="image/avif" />
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Description" />
</picture>
```

### Caching Strategy

```typescript
// React Query caching
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
    },
  },
});
```
