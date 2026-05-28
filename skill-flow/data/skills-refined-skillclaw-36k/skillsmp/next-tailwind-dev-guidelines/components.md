# Component Development Patterns

## Component Architecture

### File Organization

Components are organized by feature, not by type:

```
src/components/
├── ui/                      # Design system primitives
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── LoadingSpinner.tsx
│   └── ErrorMessage.tsx
├── PortfolioAllocation/     # Feature-specific
│   ├── components/          # Sub-components
│   ├── hooks/              # Feature hooks
│   ├── types.ts            # Domain types
│   └── index.ts            # Public API
└── shared/                  # Cross-feature components
    ├── Header.tsx
    └── Footer.tsx
```

### Component Types

**1. UI Components (Design System)**

Reusable, styled primitives with no business logic:

```typescript
// src/components/ui/GradientButton.tsx
interface GradientButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
}

export function GradientButton({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  onClick,
  children,
  className = '',
}: GradientButtonProps) {
  const baseStyles = 'relative rounded-lg font-semibold transition-all duration-200';

  const variantStyles = {
    primary: 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white',
    secondary: 'bg-gray-800 hover:bg-gray-700 text-white',
    outline: 'border-2 border-purple-500 hover:bg-purple-500/10 text-purple-400',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? <LoadingSpinner size="sm" /> : children}
    </button>
  );
}
```

**2. Feature Components**

Domain-specific components with business logic:

```typescript
// src/components/PortfolioAllocation/PortfolioCard.tsx
interface PortfolioCardProps {
  userId: string;
  showActions?: boolean;
}

export function PortfolioCard({ userId, showActions = true }: PortfolioCardProps) {
  const { data: portfolio } = usePortfolioQuery(userId);
  const { data: apr } = usePortfolioAPRQuery(userId);

  return (
    <Card className="p-6">
      <h3 className="text-xl font-bold mb-4">Portfolio Overview</h3>
      <PortfolioMetrics portfolio={portfolio} apr={apr} />
      {showActions && <PortfolioActions userId={userId} />}
    </Card>
  );
}
```

**3. Container Components**

Page-level components that orchestrate features:

```typescript
// src/app/bundle/BundlePageClient.tsx
'use client';

export function BundlePageClient({ userId }: { userId: string }) {
  const { account } = useWalletProvider();
  const isOwner = account?.address === userId;

  return (
    <div className="container mx-auto px-4 py-8">
      {!isOwner && account && <SwitchPromptBanner targetUserId={userId} />}
      <PortfolioAllocation userId={userId} readOnly={!isOwner} />
    </div>
  );
}
```

## Radix UI Integration

### Using Radix UI Primitives

Radix UI provides headless, accessible components. Style them with Tailwind:

```typescript
import * as Dialog from '@radix-ui/react-dialog';

export function WalletModal({ open, onOpenChange }: ModalProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gray-900 rounded-lg p-6 w-full max-w-md z-50">
          <Dialog.Title className="text-xl font-bold mb-4">
            Connect Wallet
          </Dialog.Title>
          <Dialog.Description className="text-gray-400 mb-6">
            Choose your wallet provider to connect
          </Dialog.Description>
          {/* Modal content */}
          <Dialog.Close asChild>
            <button className="absolute top-4 right-4 text-gray-400 hover:text-white">
              ✕
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Common Radix UI Components

```typescript
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import * as Tooltip from '@radix-ui/react-tooltip';
import * as Switch from '@radix-ui/react-switch';

// Dropdown Menu
<DropdownMenu.Root>
  <DropdownMenu.Trigger>Options</DropdownMenu.Trigger>
  <DropdownMenu.Content className="bg-gray-900 rounded-lg p-2">
    <DropdownMenu.Item className="px-3 py-2 hover:bg-gray-800 rounded">
      Edit
    </DropdownMenu.Item>
  </DropdownMenu.Content>
</DropdownMenu.Root>

// Tooltip
<Tooltip.Provider>
  <Tooltip.Root>
    <Tooltip.Trigger>Hover me</Tooltip.Trigger>
    <Tooltip.Content className="bg-gray-800 px-3 py-2 rounded text-sm">
      Helpful tooltip text
    </Tooltip.Content>
  </Tooltip.Root>
</Tooltip.Provider>
```

## Component Props Best Practices

### Prop Interface Definition

```typescript
// ✅ Good: Clear, specific prop types
interface PortfolioMetricsProps {
  totalValue: number;
  apr: number;
  change24h: number;
  currency?: "USD" | "ETH";
  showTrend?: boolean;
}

// ❌ Bad: Vague, any types
interface PortfolioMetricsProps {
  data: any;
  config?: object;
}
```

### Default Props

```typescript
// Use destructuring with defaults
export function MetricsCard({
  currency = "USD",
  showTrend = true,
  precision = 2,
}: MetricsCardProps) {
  // Implementation
}
```

### Children Prop

```typescript
// For layout components
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

// For compound components
interface TabsProps {
  children: React.ReactElement<TabProps> | React.ReactElement<TabProps>[];
  defaultTab?: string;
}
```

## Loading & Error States

### Suspense Boundaries

```typescript
import { Suspense } from 'react';

export function PortfolioPage() {
  return (
    <Suspense fallback={<PortfolioSkeleton />}>
      <PortfolioContent />
    </Suspense>
  );
}

function PortfolioContent() {
  // useSuspenseQuery suspends until data is ready
  const { data } = useSuspenseQuery({
    queryKey: ['portfolio'],
    queryFn: portfolioService.getPortfolio,
  });

  return <PortfolioDisplay data={data} />;
}
```

### Manual Loading States

```typescript
export function PoolAnalytics({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['pools', userId],
    queryFn: () => analyticsService.getPoolPerformance(userId),
  });

  if (isLoading) {
    return <LoadingSpinner message="Loading pool data..." />;
  }

  if (error) {
    return <ErrorMessage message="Failed to load pool data" retry={() => refetch()} />;
  }

  return <PoolList pools={data} />;
}
```

### Skeleton Screens

```typescript
export function PortfolioSkeleton() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-gray-800 rounded w-1/3" />
      <div className="h-32 bg-gray-800 rounded" />
      <div className="grid grid-cols-3 gap-4">
        <div className="h-24 bg-gray-800 rounded" />
        <div className="h-24 bg-gray-800 rounded" />
        <div className="h-24 bg-gray-800 rounded" />
      </div>
    </div>
  );
}
```

## Performance Optimization

### React.memo for Expensive Components

```typescript
import { memo } from 'react';

interface ChartProps {
  data: DataPoint[];
  config: ChartConfig;
}

export const Chart = memo(function Chart({ data, config }: ChartProps) {
  // Expensive rendering logic
  return <canvas />;
}, (prevProps, nextProps) => {
  // Custom comparison: only re-render if data length changes
  return prevProps.data.length === nextProps.data.length;
});
```

### useMemo for Computed Values

```typescript
export function PortfolioMetrics({ positions }: { positions: Position[] }) {
  const totalValue = useMemo(() => {
    return positions.reduce((sum, pos) => sum + pos.value, 0);
  }, [positions]);

  const topHolding = useMemo(() => {
    return positions.reduce((top, pos) =>
      pos.value > top.value ? pos : top
    );
  }, [positions]);

  return (
    <div>
      <div>Total: {formatCurrency(totalValue)}</div>
      <div>Top: {topHolding.name}</div>
    </div>
  );
}
```

### useCallback for Event Handlers

```typescript
export function TransactionForm() {
  const { mutate } = useMutation({ mutationFn: executeTransaction });

  const handleSubmit = useCallback((values: FormValues) => {
    mutate(values);
  }, [mutate]);

  return <Form onSubmit={handleSubmit} />;
}
```

## Animation with Framer Motion

### Basic Animations

```typescript
import { motion } from 'framer-motion';

export function FadeInCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="card"
    >
      {children}
    </motion.div>
  );
}
```

### Stagger Animations

```typescript
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export function PoolList({ pools }: { pools: Pool[] }) {
  return (
    <motion.div variants={container} initial="hidden" animate="show">
      {pools.map(pool => (
        <motion.div key={pool.id} variants={item}>
          <PoolCard pool={pool} />
        </motion.div>
      ))}
    </motion.div>
  );
}
```

## Accessibility

### ARIA Labels

```typescript
<button
  aria-label="Connect wallet"
  aria-describedby="wallet-description"
>
  Connect
</button>
<span id="wallet-description" className="sr-only">
  Connect your Ethereum wallet to view your portfolio
</span>
```

### Keyboard Navigation

```typescript
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
  onClick={handleClick}
>
  Interactive element
</div>
```

### Screen Reader Support

```typescript
// Use semantic HTML
<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// Announce dynamic changes
<div aria-live="polite" aria-atomic="true">
  {transactionStatus}
</div>
```

## Testing Components

```typescript
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function renderWithProviders(component: ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });

  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
}

describe('PortfolioCard', () => {
  it('renders portfolio data', async () => {
    renderWithProviders(<PortfolioCard userId="0x123" />);

    expect(await screen.findByText(/Total Value/i)).toBeInTheDocument();
  });
});
```
