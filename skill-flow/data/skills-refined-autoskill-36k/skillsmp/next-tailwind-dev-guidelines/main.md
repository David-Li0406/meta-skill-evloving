# Next.js + Tailwind Development Guidelines

**Tech Stack**: Next.js 15, React 19, Tailwind CSS v4, Radix UI, TanStack Query, TypeScript 5

This skill provides development guidelines specifically for the Zap Pilot frontend codebase. It
follows a **progressive disclosure pattern** - start here for the overview, then consult specific
resource files as needed.

## Core Principles

1. **Service-First Architecture**: All API operations use service functions (no classes)
2. **Component Composition**: Reusable, well-typed components with clear interfaces
3. **Type Safety**: Comprehensive TypeScript with strict configuration
4. **Performance**: Lazy loading, memoization, and React Query caching
5. **Accessibility**: ARIA labels and keyboard navigation support

## Quick Reference

### When Working With...

- **Components**: See `@components.md` for patterns, props, and composition
- **Routing**: See `@routing.md` for Next.js App Router patterns
- **Data Fetching**: See `@data-fetching.md` for React Query patterns
- **State**: See `@state-management.md` for Context and hooks
- **Styling**: See `@styling.md` for Tailwind and design system
- **Performance**: See `@performance.md` for optimization strategies
- **Testing**: See `@testing.md` for Vitest and Playwright patterns
- **Web3**: See `@web3-integration.md` for wallet and chain management

## Project Structure

```
src/
├── app/              # Next.js App Router pages
│   ├── layout.tsx    # Root layout with providers
│   ├── page.tsx      # Home page
│   └── bundle/       # Bundle sharing feature
├── components/       # Feature-based component organization
│   ├── ui/           # Design system components
│   ├── PortfolioAllocation/  # Portfolio management
│   ├── SwapPage/     # Trading interface
│   ├── Web3/         # Wallet connectivity
│   └── shared/       # Cross-feature components
├── hooks/            # Custom hooks for business logic
│   ├── queries/      # React Query hooks
│   └── *.ts          # Domain-specific hooks
├── services/         # API integration (service functions)
│   ├── accountService.ts    # User & wallet management
│   ├── intentService.ts     # Transaction execution
│   └── analyticsService.ts  # Portfolio analytics
├── providers/        # React Context providers
├── lib/              # Utilities and helpers
├── types/            # TypeScript definitions
└── config/           # Configuration files
```

## Development Workflow

### Before Starting

```bash
# Type check
npm run type-check

# Run tests
npm run test:unit

# Lint
npm run lint
```

### Component Development

1. **Define types** in component file or `src/types/`
2. **Create service functions** in appropriate `src/services/` file
3. **Create custom hooks** for business logic in `src/hooks/`
4. **Build UI component** with proper TypeScript types
5. **Add tests** in `tests/unit/`
6. **Document** with JSDoc comments

### File Naming Conventions

- **Components**: PascalCase (e.g., `PortfolioCard.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `usePortfolioData.ts`)
- **Services**: camelCase with `Service` suffix (e.g., `analyticsService.ts`)
- **Utils**: camelCase (e.g., `formatCurrency.ts`)
- **Types**: PascalCase (e.g., `PortfolioData.ts`)

## Common Patterns

### Service Functions

```typescript
// src/services/analyticsService.ts
export async function getPortfolioAPR(userId: string): Promise<PortfolioAPRData> {
  const response = await fetch(`/api/portfolio/${userId}/apr`);
  if (!response.ok) {
    throw new Error(`Failed to fetch portfolio APR: ${response.statusText}`);
  }
  return response.json();
}
```

### Custom Hooks with React Query

```typescript
// src/hooks/queries/usePortfolioQuery.ts
export function usePortfolioQuery(userId: string) {
  return useSuspenseQuery({
    queryKey: ["portfolio", userId],
    queryFn: () => analyticsService.getPortfolioData(userId),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}
```

### Component Structure

```typescript
// src/components/PortfolioCard.tsx
interface PortfolioCardProps {
  userId: string;
  variant?: 'compact' | 'detailed';
  onAction?: (action: string) => void;
}

export function PortfolioCard({
  userId,
  variant = 'detailed',
  onAction
}: PortfolioCardProps) {
  const { data, isLoading } = usePortfolioQuery(userId);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="rounded-lg bg-gradient-to-br from-purple-900/20 to-blue-900/20 p-6">
      {/* Component implementation */}
    </div>
  );
}
```

## Error Handling

### API Errors

```typescript
// Service functions throw errors
export async function getPortfolioData(userId: string) {
  const response = await fetch(`/api/portfolio/${userId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch portfolio: ${response.statusText}`);
  }
  return response.json();
}

// React Query handles errors
const { data, error } = useQuery({
  queryKey: ['portfolio', userId],
  queryFn: () => portfolioService.getPortfolioData(userId),
});

if (error) {
  return <ErrorMessage message={error.message} />;
}
```

### Component Error Boundaries

```typescript
// Wrap components with error boundaries for safety
<ErrorBoundary fallback={<ErrorFallback />}>
  <PortfolioAllocation userId={userId} />
</ErrorBoundary>
```

## Testing Standards

- **Unit Tests**: All service functions and custom hooks
- **Component Tests**: User-facing behavior with React Testing Library
- **E2E Tests**: Critical user flows with Playwright
- **Coverage**: Minimum 80% threshold

## Performance Guidelines

- **Lazy Load**: Use `React.lazy()` for route-based code splitting
- **Memoization**: Use `React.memo()` for expensive components
- **Query Caching**: Configure React Query `staleTime` and `cacheTime`
- **Image Optimization**: Use Next.js Image component

## Security Best Practices

- **Input Validation**: Validate all user inputs with Zod schemas
- **Error Messages**: Don't leak sensitive information in errors
- **CSP**: Follow strict Content Security Policy headers
- **Wallet Security**: Never expose private keys or sensitive wallet data

## Progressive Disclosure

This main file provides an overview. For detailed guidance on specific topics:

- **Components**: `@components.md` - Radix UI patterns, composition, props
- **Routing**: `@routing.md` - Next.js App Router, navigation, dynamic routes
- **Data Fetching**: `@data-fetching.md` - React Query patterns, caching strategies
- **State Management**: `@state-management.md` - Context providers, custom hooks
- **Styling**: `@styling.md` - Tailwind utilities, design tokens, animations
- **Performance**: `@performance.md` - Optimization techniques, lazy loading
- **Testing**: `@testing.md` - Vitest, Playwright, testing patterns
- **Web3 Integration**: `@web3-integration.md` - ThirdWeb SDK, wallet connectivity

Use `@filename.md` to include the resource file in your context when needed.
