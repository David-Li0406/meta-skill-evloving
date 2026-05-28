# Hooks Patterns - Production Examples

Real-world examples of React hooks patterns from the web codebase demonstrating useState, useEffect, custom hooks, and web-specific hooks.

## Example 1: Custom Hook with Explicit Types

**File**: `app/state/cart/cartSku/useCartSkuState.ts:5`

```typescript
import { useAtom, SetStateAction } from 'jotai';
import { CartSku, cartSkuState } from './cartSkuState';

const useCartSkuState = (): [
  CartSku,
  (update: SetStateAction<CartSku>) => void
] => useAtom(cartSkuState);

export default useCartSkuState;
```

**Key patterns:**
- Custom hook name starts with "use" prefix
- Explicit return type as tuple: `[CartSku, (update: SetStateAction<CartSku>) => void]`
- Re-exports Jotai's `useAtom` with specific type
- Type-safe state access and updates

**Usage:**
```typescript
function CartComponent() {
  const [cartSku, setCartSku] = useCartSkuState();

  const updateQuantity = (newQuantity: number) => {
    setCartSku((prev) => ({ ...prev, quantity: newQuantity }));
  };

  return <div>Items: {cartSku.quantity}</div>;
}
```

**Why this pattern:**
- Encapsulates state management logic
- Type-safe consumer code
- Single source of truth for cart SKU state
- Easy to test independently

## Example 2: Custom Hook for Translation Data

**File**: `app/unified-spaces/registration-page/testimonials/useReviews.ts:6`

```typescript
import { useT9n } from '@/libs/translation';

const APPLANGA_GROUP = 'registration.testimonials';

interface Review {
  displayName: string;
  text: string;
}

export const useReviews = (
  numberOfReviews: number
): Review[] => {
  const { translateRaw } = useT9n(APPLANGA_GROUP);

  const reviews: Review[] = [];

  for (let i = 1; i <= numberOfReviews; i++) {
    const displayName = translateRaw(`review-${i}.displayName`);
    const text = translateRaw(`review-${i}.text`);

    if (text) {
      reviews.push({ displayName, text });
    }
  }

  return reviews;
};

// Usage
function TestimonialsSection() {
  const reviews = useReviews(5);

  return (
    <div>
      {reviews.map((review, index) => (
        <div key={index}>
          <p>{review.text}</p>
          <span>- {review.displayName}</span>
        </div>
      ))}
    </div>
  );
}
```

**Key patterns:**
- Custom hook composes other hooks (`useT9n`)
- Loop inside hook to build data structure
- Filters out empty translations with conditional push
- Returns typed array of reviews
- No state - pure data transformation

**Why this pattern:**
- Centralizes translation logic
- Reusable across components
- Type-safe review data
- Easy to modify number of reviews

## Example 3: useEffect with Data Fetching and Cleanup

**File**: Production pattern for API data fetching

```typescript
import { useEffect, useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;
    let controller = new AbortController();

    async function fetchUser() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user');
        }

        const data = await response.json();

        if (isMounted) {
          setUser(data);
        }
      } catch (err) {
        if (isMounted && err.name !== 'AbortError') {
          setError(err as Error);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchUser();

    // Cleanup function
    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [userId]); // Re-run when userId changes

  return { user, loading, error };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { user, loading, error } = useUser(userId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return null;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

**Key patterns:**
- Three-state pattern: `data`, `loading`, `error`
- `isMounted` flag prevents state updates after unmount
- AbortController cancels pending fetch on unmount
- Cleanup function in useEffect return
- Error handling with try/catch/finally
- Dependency array `[userId]` triggers refetch when ID changes

**Why this pattern:**
- Prevents memory leaks with `isMounted` check
- Cancels fetch requests on unmount (AbortController)
- Complete loading/error states for UX
- Reusable across components

## Example 4: useCallback for Memoized Event Handlers

**File**: Production pattern for form handlers

```typescript
import { useState, useCallback } from 'react';

interface FormData {
  email: string;
  password: string;
}

function LoginForm() {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Memoized field change handler
  const handleFieldChange = useCallback(
    (field: keyof FormData) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormData((prev) => ({
        ...prev,
        [field]: e.target.value,
      }));
    },
    []
  );

  // Memoized submit handler
  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      setIsSubmitting(true);
      try {
        await fetch('/api/login', {
          method: 'POST',
          body: JSON.stringify(formData),
        });
      } catch (error) {
        console.error(error);
      } finally {
        setIsSubmitting(false);
      }
    },
    [formData]
  );

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={formData.email}
        onChange={handleFieldChange('email')}
      />
      <input
        type="password"
        value={formData.password}
        onChange={handleFieldChange('password')}
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

**Key patterns:**
- `useCallback` with empty deps `[]` for field handler (stable reference)
- `useCallback` with `[formData]` deps for submit handler
- Higher-order function pattern: `handleFieldChange('email')` returns handler
- Function updater: `setFormData((prev) => ...)` for immutable updates
- Loading state prevents double-submit

**Why this pattern:**
- Stable function references prevent child re-renders
- Type-safe field updates with `keyof FormData`
- Reusable field change handler
- Proper async handling with try/catch/finally

## Example 5: useMemo for Expensive Computations

**File**: Production pattern for filtered/sorted lists

```typescript
import { useMemo, useState } from 'react';

interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
  rating: number;
}

interface ProductListProps {
  products: Product[];
}

function ProductList({ products }: ProductListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'price' | 'rating'>('rating');

  // Expensive filtering and sorting - memoized
  const filteredProducts = useMemo(() => {
    console.log('Computing filtered products...');

    return products
      .filter((p) => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || p.category === selectedCategory;
        return p.inStock && matchesSearch && matchesCategory;
      })
      .sort((a, b) => {
        if (sortBy === 'price') {
          return a.price - b.price;
        }
        return b.rating - a.rating;
      });
  }, [products, searchQuery, selectedCategory, sortBy]);

  // Simple computation - NOT memoized
  const totalProducts = filteredProducts.length;

  return (
    <div>
      <input
        type="text"
        placeholder="Search products..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
      >
        <option value="all">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>

      <p>Found {totalProducts} products</p>

      <ul>
        {filteredProducts.map((product) => (
          <li key={product.id}>
            {product.name} - ${product.price}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Key patterns:**
- `useMemo` for expensive filter + sort operations
- Complete dependency array: `[products, searchQuery, selectedCategory, sortBy]`
- Simple computation (`totalProducts`) NOT memoized
- Console.log shows when recomputation happens

**Why this pattern:**
- Prevents expensive filtering/sorting on every render
- Only recomputes when dependencies change
- Simple operations stay unmemoized (avoid over-optimization)
- Improves performance for large lists

## Example 6: Custom Hook with Window Events (Web-Specific)

**File**: Production pattern for window resize handling

```typescript
import { useState, useEffect } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

export function useWindowSize(): WindowSize {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // SSR guard
    if (typeof window === 'undefined') {
      return;
    }

    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup function
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty deps - run once on mount

  return windowSize;
}

// Usage
function ResponsiveComponent() {
  const { width, height } = useWindowSize();
  const isMobile = width < 768;

  return (
    <div>
      <p>Window size: {width} x {height}</p>
      {isMobile ? <MobileNav /> : <DesktopNav />}
    </div>
  );
}
```

**Key patterns:**
- SSR-safe: `typeof window !== 'undefined'` check
- Initial state from current window size
- Window event listener in useEffect
- **Cleanup function removes event listener**
- Empty dependency array `[]` - effect runs once
- Returns simple object with width/height

**Why this pattern:**
- Works with Next.js SSR (no window reference errors)
- Automatically updates on resize
- Cleans up event listener on unmount
- Reusable across components

## Example 7: useRouter from Next.js (Web-Specific)

**File**: Production pattern for Next.js navigation

```typescript
import { useRouter } from 'next/router';
import { useCallback } from 'react';

function ProductDetail() {
  const router = useRouter();

  // Get query params
  const { id, category } = router.query;

  const handleBackClick = useCallback(() => {
    // Navigate back
    router.back();
  }, [router]);

  const handleNavigateToCategory = useCallback(() => {
    // Navigate to specific route
    router.push(`/products/category/${category}`);
  }, [router, category]);

  const handleAddToCart = useCallback(async () => {
    // Programmatic navigation after action
    await addProductToCart(id as string);

    // Navigate with query params
    router.push({
      pathname: '/cart',
      query: { from: 'product-detail' },
    });
  }, [router, id]);

  // Show loading state during route change
  useEffect(() => {
    const handleRouteChange = () => {
      console.log('Route is changing...');
    };

    router.events.on('routeChangeStart', handleRouteChange);

    return () => {
      router.events.off('routeChangeStart', handleRouteChange);
    };
  }, [router]);

  return (
    <div>
      <h1>Product {id}</h1>
      <p>Category: {category}</p>

      <button onClick={handleBackClick}>Back</button>
      <button onClick={handleNavigateToCategory}>
        View Category
      </button>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  );
}
```

**Key patterns:**
- `useRouter()` hook from Next.js
- Access query params: `router.query`
- Navigation methods: `router.push()`, `router.back()`
- Programmatic navigation with query params
- Router events for loading states
- Memoized handlers with `useCallback`

**Why this pattern:**
- Type-safe routing with Next.js
- Clean programmatic navigation
- Access to route params and query strings
- Route change event handling

## Example 8: Combining Multiple Hooks

**File**: Production pattern for complex hook composition

```typescript
import { useFetch } from '@/libs/fetch';
import { useAuth } from '@/hooks/useAuth';
import { useQueryClient, useQuery } from 'react-query';
import { RequestIds } from '@/constants/RequestIds';

interface SubscriptionData {
  id: string;
  status: 'active' | 'cancelled' | 'expired';
  expiresAt: string;
}

function useCurrentSubscription() {
  const { fetch } = useFetch(); // OpenTelemetry traced fetch
  const { isAuthenticated, customerId } = useAuth(); // Auth state
  const queryClient = useQueryClient();

  // React Query with useFetch integration
  const query = useQuery(
    [RequestIds['subscription.current'], { customerId }],
    () => getCurrentSubscription({ customerId }, queryKey, fetch),
    {
      enabled: isAuthenticated && !!customerId,
      retry: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  // Refetch subscription
  const refetchSubscription = useCallback(() => {
    queryClient.invalidateQueries([RequestIds['subscription.current']]);
  }, [queryClient]);

  return {
    ...query,
    refetchSubscription,
  };
}

// Usage
function SubscriptionStatus() {
  const { data: subscription, isLoading, error, refetchSubscription } = useCurrentSubscription();

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  if (!subscription) return null;

  return (
    <div>
      <p>Status: {subscription.status}</p>
      <button onClick={refetchSubscription}>Refresh</button>
    </div>
  );
}
```

**Key patterns:**
- Combines three hooks: `useFetch`, `useAuth`, `useQuery`
- Conditional query execution with `enabled`
- Custom refetch function using `useQueryClient`
- Returns enhanced query object with additional methods
- Type-safe subscription data

**Why this pattern:**
- Encapsulates complex data fetching logic
- Reusable authentication + data fetching
- Clean component API
- Centralized subscription logic

## Summary

These production examples demonstrate:

1. **Custom Hook with Types**: Explicit return types for type-safe consumers
2. **Custom Hook for Data**: Composing hooks to build data structures
3. **useEffect with Cleanup**: Data fetching with abort controller and mounted check
4. **useCallback for Handlers**: Memoized event handlers with proper dependencies
5. **useMemo for Expensive Ops**: Filtering/sorting large lists
6. **Window Events Hook**: SSR-safe window resize handling with cleanup
7. **Next.js useRouter**: Programmatic navigation and query params
8. **Combining Hooks**: Composing multiple hooks for complex logic

**Common patterns across examples:**
- Always use "use" prefix for custom hooks
- Explicit TypeScript types on return values and parameters
- Cleanup functions in useEffect for event listeners and subscriptions
- Empty dependency arrays `[]` for mount-only effects
- Complete dependency arrays for reactive effects
- `isMounted` flag prevents state updates after unmount
- AbortController cancels pending fetch requests
- `useCallback` for functions passed to children
- `useMemo` only for expensive operations
- SSR-safe checks (`typeof window !== 'undefined'`)

**Anti-patterns to avoid:**
- Forgetting "use" prefix on custom hooks
- Missing dependencies in useEffect/useMemo/useCallback
- Not cleaning up event listeners or subscriptions
- Calling hooks conditionally or in loops
- Over-using useMemo/useCallback for simple operations
- Not handling unmounted component state updates
- Missing TypeScript types on custom hooks
