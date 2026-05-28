# Next.js Routing Implementation Patterns

Implementation patterns and anti-patterns for Next.js routing with the Pages Router.

**IMPORTANT**: This codebase uses `@/libs/router` wrapper, NOT `next/router` directly.

## Pattern: Import from Custom Router Wrapper

Always import from the custom router wrapper.

✅ **Good:**
```typescript
import { useRouter } from '@/libs/router';

function Component() {
  const router = useRouter();
  return <div>{router.pathname}</div>;
}
```

❌ **Bad:**
```typescript
// Don't import directly from next/router
import { useRouter } from 'next/router';

function Component() {
  const router = useRouter();
  return <div>{router.pathname}</div>;
}
```

**Why:** The `@/libs/router` wrapper:
- Extends Next.js router with custom query handling
- Adds application-specific functionality
- Maintains consistency across codebase
- May include analytics or error handling

## Pattern: Type-Safe Query Parameter Access

Always type-check query parameters before use.

✅ **Good:**
```typescript
function ProductPage() {
  const router = useRouter();
  const { id, category } = router.query;

  // Type guard for single value
  if (typeof id === 'string') {
    return <Product id={id} />;
  }

  return <div>Invalid product ID</div>;
}

// Custom hook pattern
export function useQueryParam(key: string): string | undefined {
  const router = useRouter();
  const value = router.query[key];

  return typeof value === 'string' ? value : undefined;
}

// Usage
const productId = useQueryParam('id');
```

❌ **Bad:**
```typescript
function ProductPage() {
  const router = useRouter();

  // No type check - can be string | string[] | undefined
  const id = router.query.id;

  // Crashes if id is array or undefined
  return <Product id={id.toUpperCase()} />;
}
```

**Why:** Query values can be:
- `string` - Single value (`?id=123`)
- `string[]` - Multiple values (`?tags=a&tags=b`)
- `undefined` - Missing param
Type guards prevent runtime errors.

## Pattern: Check router.isReady Before Using Query

Wait for router to be ready on client-side.

✅ **Good:**
```typescript
function ProductPage() {
  const router = useRouter();
  const [productId, setProductId] = useState<string | null>(null);

  useEffect(() => {
    if (router.isReady) {
      const { id } = router.query;
      if (typeof id === 'string') {
        setProductId(id);
      }
    }
  }, [router.isReady, router.query]);

  if (!productId) {
    return <div>Loading...</div>;
  }

  return <Product id={productId} />;
}
```

❌ **Bad:**
```typescript
function ProductPage() {
  const router = useRouter();
  const { id } = router.query; // May be empty on first render!

  return <Product id={id as string} />; // Crashes if id is undefined
}
```

**Why:** On initial client-side render:
- `router.query` may be empty object `{}`
- Query params populate after hydration
- `router.isReady` signals when query is available
- Server-side rendering has query immediately

## Pattern: Use Link for Internal Navigation

Use `<Link>` for internal navigation to enable prefetching.

✅ **Good:**
```typescript
import Link from 'next/link';

function Navigation() {
  return (
    <nav>
      <Link href="/about">
        <a>About</a>
      </Link>

      <Link href={{ pathname: '/product', query: { id: '123' } }}>
        <a>Product</a>
      </Link>
    </nav>
  );
}
```

❌ **Bad:**
```typescript
// Regular anchor tag - full page reload
function Navigation() {
  return (
    <nav>
      <a href="/about">About</a>
      <a href="/product?id=123">Product</a>
    </nav>
  );
}

// Button with router.push for simple links
function Navigation() {
  const router = useRouter();

  return (
    <button onClick={() => router.push('/about')}>About</button>
  );
}
```

**Why:** `<Link>` component:
- Client-side navigation (no full reload)
- Automatic prefetching on hover
- Better performance
- Preserves scroll position
Use `router.push` only for programmatic navigation (form submit, button click with logic).

## Pattern: Use router.push for Programmatic Navigation

Use `router.push()` for navigation triggered by logic.

✅ **Good:**
```typescript
function LoginForm() {
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const success = await loginUser(credentials);

    if (success) {
      // Programmatic navigation after logic
      router.push('/dashboard');
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

❌ **Bad:**
```typescript
// Using Link when you need conditional logic
function LoginForm() {
  return (
    <form>
      <input ... />
      <Link href="/dashboard">
        <a>
          <button type="submit">Login</button>
        </a>
      </Link>
    </form>
  );
}
```

**Why:** Use `router.push` when:
- Navigation depends on logic (validation, API call)
- Need to perform actions before navigation
- Conditional navigation based on response
Use `<Link>` for simple, declarative navigation.

## Pattern: Preserve Query Parameters

Preserve important query params across navigation.

✅ **Good:**
```typescript
function useNavigateWithPreservedParams() {
  const router = useRouter();

  return useCallback(
    (pathname: string, additionalParams = {}) => {
      // Preserve existing query params
      router.push({
        pathname,
        query: {
          ...router.query,
          ...additionalParams,
        },
      });
    },
    [router]
  );
}

// Usage
const navigate = useNavigateWithPreservedParams();

navigate('/checkout', { step: '2' });
// Preserves: locale, utm_source, etc.
// Adds: step=2
```

❌ **Bad:**
```typescript
// Loses query params on navigation
function Component() {
  const router = useRouter();

  const handleNext = () => {
    router.push('/checkout'); // Lost: locale, utm_source!
  };

  return <button onClick={handleNext}>Next</button>;
}
```

**Why:** Preserving query params:
- Maintains tracking info (utm_*, ref, etc.)
- Preserves locale/language settings
- Keeps feature flags across pages
- Better analytics attribution

## Pattern: Remove Specific Query Parameters

Selectively remove query params when navigating.

✅ **Good:**
```typescript
import omit from 'lodash/omit';

function useNavigateToCheckout() {
  const router = useRouter();

  return useCallback(
    (cartId: string) => {
      // Remove flow-specific params
      const cleanedQuery = omit(router.query, ['step', 'temp', 'mealsize']);

      router.push({
        pathname: '/checkout',
        query: {
          ...cleanedQuery,
          cartId,
        },
      });
    },
    [router]
  );
}
```

❌ **Bad:**
```typescript
// Manually filtering params - error-prone
function useNavigateToCheckout() {
  const router = useRouter();

  return useCallback(
    (cartId: string) => {
      const { step, temp, mealsize, ...rest } = router.query;

      router.push({
        pathname: '/checkout',
        query: {
          ...rest,
          cartId,
        },
      });
    },
    [router]
  );
}
```

**Why:** Using `omit()`:
- Declarative param removal
- Less error-prone than manual destructuring
- Clear intent
- Easy to add/remove params from exclusion list

## Pattern: Memoize Navigation Callbacks

Use `useCallback` for navigation functions.

✅ **Good:**
```typescript
function Component() {
  const router = useRouter();

  const handleNavigate = useCallback(() => {
    router.push('/checkout');
  }, [router]);

  const handleNavigateWithParam = useCallback((id: string) => {
    router.push(`/product/${id}`);
  }, [router]);

  return (
    <>
      <button onClick={handleNavigate}>Checkout</button>
      <ExpensiveChild onNavigate={handleNavigate} />
    </>
  );
}
```

❌ **Bad:**
```typescript
function Component() {
  const router = useRouter();

  // New function every render - causes child re-render
  const handleNavigate = () => {
    router.push('/checkout');
  };

  return <ExpensiveChild onNavigate={handleNavigate} />;
}
```

**Why:** `useCallback` with `[router]`:
- Stable function reference
- Prevents unnecessary child re-renders
- Better performance with React.memo
- Standard pattern for callbacks

## Pattern: addQueryToUrl Utility

Use utility function for building URLs with query strings.

✅ **Good:**
```typescript
function addQueryToUrl(
  pathname: string,
  params: Record<string, string>
): string {
  const queryString = new URLSearchParams(params).toString();
  return `${pathname}?${queryString}`;
}

// Usage
router.push(
  addQueryToUrl('/checkout', {
    cartId: '123',
    step: 'payment',
  })
);
// → "/checkout?cartId=123&step=payment"
```

❌ **Bad:**
```typescript
// Manual string concatenation
router.push(`/checkout?cartId=${cartId}&step=${step}`);

// No URL encoding - breaks with special characters
router.push(`/checkout?name=${name}&email=${email}`);
```

**Why:** `addQueryToUrl` utility:
- Automatic URL encoding
- Handles special characters
- Consistent format
- Type-safe with TypeScript

## Pattern: Custom Navigation Hooks

Extract navigation logic into reusable hooks.

✅ **Good:**
```typescript
interface NavigateToCheckoutParams {
  cartId: string;
  step?: 'address' | 'payment';
}

export function useNavigateToCheckout() {
  const router = useRouter();
  const locale = useSelectedLocale();

  return useCallback(
    (params: NavigateToCheckoutParams) => {
      const { cartId, step = 'address' } = params;

      router.push({
        pathname: '/checkout',
        query: { locale, cartId, step },
      });
    },
    [router, locale]
  );
}

// Usage in multiple components
function Component1() {
  const navigateToCheckout = useNavigateToCheckout();
  navigateToCheckout({ cartId: '123' });
}

function Component2() {
  const navigateToCheckout = useNavigateToCheckout();
  navigateToCheckout({ cartId: '456', step: 'payment' });
}
```

❌ **Bad:**
```typescript
// Duplicated navigation logic in each component
function Component1() {
  const router = useRouter();
  const locale = useSelectedLocale();

  const handleCheckout = () => {
    router.push({
      pathname: '/checkout',
      query: { locale, cartId: '123', step: 'address' },
    });
  };
}

function Component2() {
  const router = useRouter();
  const locale = useSelectedLocale();

  const handleCheckout = () => {
    router.push({
      pathname: '/checkout',
      query: { locale, cartId: '456', step: 'payment' },
    });
  };
}
```

**Why:** Custom navigation hooks:
- Centralize navigation logic
- Reusable across components
- Type-safe parameters
- Single source of truth
- Easy to test

## Pattern: Clean Up Router Event Listeners

Always clean up router event listeners.

✅ **Good:**
```typescript
function useRouteChangeTracking() {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      trackPageView(url);
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    // Cleanup function
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);
}
```

❌ **Bad:**
```typescript
// No cleanup - memory leak!
function useRouteChangeTracking() {
  const router = useRouter();

  useEffect(() => {
    router.events.on('routeChangeComplete', (url) => {
      trackPageView(url);
    });
    // Missing cleanup!
  }, [router]);
}
```

**Why:** Cleanup prevents:
- Memory leaks
- Multiple event listeners
- Handlers running after unmount
- Performance degradation

## Anti-Pattern: Mutating router.query

Never mutate the `router.query` object.

❌ **Bad:**
```typescript
function Component() {
  const router = useRouter();

  const handleUpdate = () => {
    router.query.step = '2'; // Mutation!
    router.push({ pathname: '/checkout', query: router.query });
  };
}
```

✅ **Good:**
```typescript
function Component() {
  const router = useRouter();

  const handleUpdate = () => {
    // Create new object
    const newQuery = {
      ...router.query,
      step: '2',
    };

    router.push({ pathname: '/checkout', query: newQuery });
  };
}
```

**Why:** `router.query` is read-only:
- Mutations don't trigger updates
- Breaks React's immutability
- Can cause bugs
- Always create new objects

## Anti-Pattern: Using String Concatenation for URLs

Don't manually build URLs with string concatenation.

❌ **Bad:**
```typescript
// No URL encoding - breaks with special characters
router.push(`/search?q=${searchQuery}&category=${category}`);

// Special characters not encoded
router.push(`/product?name=${name}&description=${description}`);
```

✅ **Good:**
```typescript
// Use URL object
router.push({
  pathname: '/search',
  query: {
    q: searchQuery,
    category: category,
  },
});

// Or addQueryToUrl utility
router.push(
  addQueryToUrl('/product', {
    name: name,
    description: description,
  })
);
```

**Why:** URL object/utility:
- Automatic URL encoding
- Handles special characters
- Type-safe with TypeScript
- Prevents injection vulnerabilities

## Summary

**Key Patterns:**
- Import from `@/libs/router` (NOT `next/router`)
- Type-check query params with `typeof value === 'string'`
- Check `router.isReady` before using `router.query`
- Use `<Link>` for declarative navigation
- Use `router.push()` for programmatic navigation
- Preserve important query params across navigation
- Remove specific params with `omit()`
- Memoize navigation callbacks with `useCallback`
- Use `addQueryToUrl` utility for URL building
- Extract navigation logic into custom hooks
- Clean up router event listeners

**Anti-Patterns to Avoid:**
- Importing from `next/router` directly
- Not type-checking query parameters
- Not checking `router.isReady`
- Using `<a>` tags for internal links
- Mutating `router.query` object
- String concatenation for URLs
- Not cleaning up event listeners
- Duplicating navigation logic across components
- Forgetting to memoize navigation callbacks
