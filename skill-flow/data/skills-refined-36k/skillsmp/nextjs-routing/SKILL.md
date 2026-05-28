---
name: nextjs-routing
description: "WHAT: Next.js Pages Router patterns with useRouter and query parameters. WHEN: client-side navigation, accessing URL params, programmatic routing. KEYWORDS: nextjs, router, useRouter, Link, query, navigate, route, URL, web, push."
---

# Next.js Routing - Web

Next.js routing patterns for the React web application using the Pages Router.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use Next.js routing for:
- Client-side navigation without full page reloads
- Accessing URL parameters and query strings
- Programmatic navigation (redirects, form submissions)
- Dynamic route handling
- Route-based data prefetching

**Note:** This codebase uses Next.js Pages Router, not App Router.

## Core Principles

### 1. useRouter Hook

**Import from custom router wrapper that extends Next.js router.**

✅ **Good:**
```typescript
// app/unified-spaces/registration-page/steps/utils/email.ts:2
import { useRouter } from '@/libs/router';

export const useGetPrefilledEmail = (): string | undefined => {
  const { query } = useRouter();

  if (typeof query.email === 'string') {
    if (isEmailValid(query.email)) {
      return query.email;
    }
  }

  return undefined;
};
```

**Why:** The custom wrapper (@/libs/router) extends next/router with additional query handling. Always use this, not direct next/router import.

### 2. Accessing Query Parameters

**Use router.query to access URL query parameters.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/hooks/useRedirectCustomerToFinishOrder.ts:28
import { useRouter } from '@/libs/router';
import omit from 'lodash/omit';

const useRedirectCustomerToFinishOrder = () => {
  const router = useRouter();

  return useCallback(
    (cartId: string) => {
      // Remove specific query params
      const queryParams = omit(router.query, ['c', 'step', 'mealsize']);

      return router.push(
        addQueryToUrl('/checkout', {
          ...queryParams,
          cartId,
        })
      );
    },
    [router]
  );
};
```

**Why:** router.query provides parsed query parameters as an object. Omit can remove unwanted params.

### 3. Programmatic Navigation with router.push

**Use router.push() for client-side navigation.**

✅ **Good:**
```typescript
// app/unified-spaces/referral-page/referral/components/manual-credit-issuance/RedeemedDialog.tsx:72
import { useRouter } from '@/libs/router';

export const RedeemedDialog: React.FC = () => {
  const router = useRouter();
  const { manualCreditIssuanceSecondaryBtnRoute } = useReferralConfig();

  const handleSecondaryBtnClick = () => {
    trackManualCreditIssuanceCheckCreditBalance('ManualRewardClaimed');

    router.push(manualCreditIssuanceSecondaryBtnRoute);
    clearDialogs();
  };

  return (
    <button onClick={handleSecondaryBtnClick}>
      Check Credit Balance
    </button>
  );
};
```

**Why:** router.push() triggers client-side navigation without a full page reload.

### 4. Navigation with Query Parameters

**Build URLs with query parameters for navigation.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/hooks/useRedirectCustomerToFinishOrder.ts:46
const useRedirectCustomerToFinishOrder = () => {
  const router = useRouter();
  const locale = useSelectedLocale();

  return useCallback(
    (cartId: string) => {
      // Add query params to URL
      return router.push(
        addQueryToUrl('/checkout-form/address', {
          locale,
          cartId,
          step: 'address',
        })
      );
    },
    [router, locale]
  );
};
```

**Helper function pattern:**
```typescript
// Utility for adding query params to URL
const addQueryToUrl = (url: string, params: Record<string, any>): string => {
  const queryString = new URLSearchParams(params).toString();
  return `${url}?${queryString}`;
};
```

**Why:** Query parameters maintain state across navigation and enable deep linking.

### 5. Link Component

**Use Next.js Link for declarative navigation.**

✅ **Good:**
```typescript
// app/unified-spaces/checkout-header/header/components/cart-button/index.tsx:2
import Link from 'next/link';

const CartButton = () => {
  return (
    <Link href="/cart">
      <a>
        <Icon icon={<CartOutline24 />} />
        View Cart
      </a>
    </Link>
  );
};
```

**With query parameters:**
```typescript
<Link href={{ pathname: '/checkout', query: { step: 'payment' } }}>
  <a>Continue to Payment</a>
</Link>
```

**Why:** Link enables client-side navigation and prefetches linked pages for better performance.

### 6. Conditional Navigation

**Navigate based on conditions (auth state, feature flags, etc.).**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/hooks/useRedirectCustomerToFinishOrder.ts:44
const useRedirectCustomerToFinishOrder = () => {
  const router = useRouter();
  const brand = useBrand();
  const isCustomerLoggedIn = useIsomorphicIsCustomerType();

  return useCallback(
    (cartId: string) => {
      // Conditional navigation based on auth and brand
      if (isCustomerLoggedIn) {
        if (brand === Brand.yourcompany) {
          return router.push(
            addQueryToUrl('/checkout', {
              locale,
              ...queryParams,
            })
          );
        } else {
          return router.push(
            addQueryToUrl('/checkout/delivery', {
              sku: productCtx.product?.handle,
              cartId,
            })
          );
        }
      }

      // Not logged in - redirect to register
      return router.push(
        addQueryToUrl('/register', {
          returnUrl: '/checkout',
          ...queryParams,
        })
      );
    },
    [router, brand, isCustomerLoggedIn]
  );
};
```

**Why:** Conditional navigation handles different user flows based on application state.

## Router API

### Router Properties

```typescript
import { useRouter } from '@/libs/router';

const router = useRouter();

// Current pathname
router.pathname // '/checkout/address'

// Query parameters as object
router.query // { step: 'address', locale: 'en-US' }

// Full path with query string
router.asPath // '/checkout/address?step=address&locale=en-US'

// Base path (for internationalization)
router.basePath // ''

// Current locale
router.locale // 'en-US'

// Whether route is ready
router.isReady // true

// Whether page was loaded via back/forward
router.isFallback // false
```

### Router Methods

```typescript
// Navigate to a page
router.push('/path')
router.push({ pathname: '/path', query: { id: '123' } })

// Replace current history entry
router.replace('/path')

// Go back in history
router.back()

// Reload current route
router.reload()

// Prefetch a page
router.prefetch('/path')

// Listen to route changes
router.events.on('routeChangeStart', (url) => {
  console.log('Navigating to:', url);
});
```

## Advanced Patterns

### Custom Navigation Hook

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';

export const useNavigateToCheckout = () => {
  const router = useRouter();
  const locale = useSelectedLocale();

  return useCallback(
    (params: { cartId: string; step?: string }) => {
      const { cartId, step = 'address' } = params;

      router.push({
        pathname: '/checkout',
        query: {
          locale,
          cartId,
          step,
        },
      });
    },
    [router, locale]
  );
};

// Usage
const navigateToCheckout = useNavigateToCheckout();
navigateToCheckout({ cartId: '123', step: 'payment' });
```

### Router Events

```typescript
import { useEffect } from 'react';
import { useRouter } from '@/libs/router';

function useRouteChangeTracking() {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      // Track page view
      analytics.track('Page View', { url });
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);
}
```

### Preserving Query Params

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';

export const useNavigateWithPreservedParams = () => {
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
};
```

## Link Patterns

### Basic Link

```typescript
import Link from 'next/link';

<Link href="/about">
  <a>About Us</a>
</Link>
```

### Link with Query Parameters

```typescript
<Link href={{ pathname: '/product', query: { id: '123' } }}>
  <a>View Product</a>
</Link>
```

### Conditional Link

```typescript
{isAuthenticated ? (
  <Link href="/dashboard">
    <a>Dashboard</a>
  </Link>
) : (
  <Link href="/login">
    <a>Login</a>
  </Link>
)}
```

### External Link

```typescript
// For external URLs, use regular <a> tag
<a href="https://external.com" target="_blank" rel="noopener noreferrer">
  External Site
</a>
```

## File Organization

```
hooks/
├── useRedirectCustomerToFinishOrder.ts  # Custom navigation logic
├── useNavigateToCheckout.ts             # Reusable navigation
└── useRouteChangeTracking.ts            # Router event handling

utils/
├── addQueryToUrl.ts                     # URL building utilities
└── parseQueryParams.ts                  # Query parsing helpers
```

## Common Mistakes

1. **Importing from next/router directly** - Use @/libs/router wrapper instead
2. **Not using Link for internal navigation** - Link enables prefetching
3. **Forgetting to memoize navigation callbacks** - Use useCallback with router as dependency
4. **Mutating router.query** - Query object is read-only, create new object
5. **Not handling router.isReady** - Query params may not be available immediately on first render
6. **Using router.push in useEffect without cleanup** - Can cause navigation after unmount

## Quick Reference

### Basic Navigation

```typescript
import { useRouter } from '@/libs/router';

const router = useRouter();

// Navigate
router.push('/path');
router.push({ pathname: '/path', query: { id: '123' } });

// Access query
const { id } = router.query;

// Go back
router.back();
```

### With Link

```typescript
import Link from 'next/link';

<Link href="/about">
  <a>About</a>
</Link>

<Link href={{ pathname: '/product', query: { id: '123' } }}>
  <a>Product</a>
</Link>
```

### Custom Hook Pattern

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';

export const useNavigate = () => {
  const router = useRouter();

  return useCallback(
    (path: string, params = {}) => {
      router.push({ pathname: path, query: params });
    },
    [router]
  );
};
```

### Router Events

```typescript
useEffect(() => {
  const handleChange = (url) => console.log('Navigated to:', url);
  router.events.on('routeChangeComplete', handleChange);
  return () => router.events.off('routeChangeComplete', handleChange);
}, [router]);
```
