# Next.js Routing - Production Examples

Real-world examples of Next.js routing patterns from the web codebase demonstrating useRouter hook, query parameters, programmatic navigation, and Link component.

**Important**: This codebase uses Next.js Pages Router (NOT App Router) and the custom `@/libs/router` wrapper.

## Example 1: Accessing Query Parameters with useRouter

**File**: `app/unified-spaces/registration-page/steps/utils/email.ts:2`

```typescript
import { useRouter } from '@/libs/router';
import { isEmailValid } from '@/utils/validation';

export const useGetPrefilledEmail = (): string | undefined => {
  const { query } = useRouter();

  // Type guard: ensure query.email is a string
  if (typeof query.email === 'string') {
    if (isEmailValid(query.email)) {
      return query.email;
    }
  }

  return undefined;
};

// Usage in component
function RegistrationForm() {
  const prefilledEmail = useGetPrefilledEmail();
  const [email, setEmail] = useState(prefilledEmail || '');

  return (
    <input
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      placeholder={prefilledEmail ? undefined : 'Enter your email'}
    />
  );
}
```

**Key patterns:**
- Import from `@/libs/router` (custom wrapper), NOT `next/router`
- Access query params with `router.query`
- Type guard: `typeof query.email === 'string'` (query values can be `string | string[]`)
- Returns `undefined` for invalid or missing email
- Custom hook pattern with "use" prefix

**URL example**: `/register?email=user@example.com`

**Why this pattern:**
- Type-safe query param access
- Validation before using query values
- Reusable logic extracted into custom hook
- Handles missing/invalid query params gracefully

## Example 2: Programmatic Navigation with router.push

**File**: `app/unified-spaces/referral-page/referral/components/manual-credit-issuance/RedeemedDialog.tsx:72`

```typescript
import { useRouter } from '@/libs/router';
import { useReferralConfig } from '@/hooks/useReferralConfig';
import { trackManualCreditIssuanceCheckCreditBalance } from '@/analytics';

export const RedeemedDialog: React.FC = () => {
  const router = useRouter();
  const { manualCreditIssuanceSecondaryBtnRoute } = useReferralConfig();

  const handleSecondaryBtnClick = () => {
    // Track analytics event
    trackManualCreditIssuanceCheckCreditBalance('ManualRewardClaimed');

    // Programmatic navigation
    router.push(manualCreditIssuanceSecondaryBtnRoute);

    // Clean up dialog state
    clearDialogs();
  };

  return (
    <Dialog open={true}>
      <h2>Credit Redeemed!</h2>
      <p>Your credit has been successfully applied to your account.</p>

      <button onClick={handleSecondaryBtnClick}>
        Check Credit Balance
      </button>
    </Dialog>
  );
};
```

**Key patterns:**
- `router.push()` for programmatic navigation
- Navigation triggered by button click
- Analytics tracking before navigation
- Route path from config/feature flags
- State cleanup after navigation

**Why this pattern:**
- Client-side navigation without full page reload
- Track user actions before navigation
- Flexible routing based on configuration
- Clean separation of navigation and UI logic

## Example 3: Navigation with Query Parameters

**File**: `app/unified-spaces/plans-sections/single-question-flow/hooks/useRedirectCustomerToFinishOrder.ts:28`

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';
import omit from 'lodash/omit';
import { addQueryToUrl } from '@/utils/url';

const useRedirectCustomerToFinishOrder = () => {
  const router = useRouter();

  return useCallback(
    (cartId: string) => {
      // Remove specific query params from current URL
      const queryParams = omit(router.query, ['c', 'step', 'mealsize']);

      // Add new query params and navigate
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

// Usage
function ProductSelectionFlow() {
  const redirectToCheckout = useRedirectCustomerToFinishOrder();
  const { cartId } = useCart();

  const handleContinue = () => {
    redirectToCheckout(cartId);
  };

  return (
    <button onClick={handleContinue}>
      Continue to Checkout
    </button>
  );
}
```

**URL transformation**:
```
Before: /plans?c=123&step=2&mealsize=4&locale=en-US&utm_source=email
After:  /checkout?locale=en-US&utm_source=email&cartId=abc123

// Removed: c, step, mealsize
// Preserved: locale, utm_source
// Added: cartId
```

**Key patterns:**
- `omit()` removes unwanted query params
- `addQueryToUrl()` utility builds URL with query string
- Preserves some existing query params (locale, utm_source)
- Custom hook returns memoized callback
- `useCallback` with `[router]` dependency

**Why this pattern:**
- Clean query param manipulation
- Preserve important params (tracking, locale) across navigation
- Remove flow-specific params (step, mealsize)
- Reusable navigation logic

## Example 4: Conditional Navigation Based on State

**File**: `app/unified-spaces/plans-sections/single-question-flow/hooks/useRedirectCustomerToFinishOrder.ts:44`

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';
import { useBrand, Brand } from '@/hooks/useBrand';
import { useIsomorphicIsCustomerType } from '@/hooks/useAuth';
import { addQueryToUrl } from '@/utils/url';

const useRedirectCustomerToFinishOrder = () => {
  const router = useRouter();
  const brand = useBrand();
  const isCustomerLoggedIn = useIsomorphicIsCustomerType();
  const locale = useSelectedLocale();

  return useCallback(
    (cartId: string, productHandle?: string) => {
      const queryParams = omit(router.query, ['c', 'step']);

      // Logged-in customer - brand-specific flow
      if (isCustomerLoggedIn) {
        if (brand === Brand.yourcompany) {
          // YourCompany: direct to checkout
          return router.push(
            addQueryToUrl('/checkout', {
              locale,
              ...queryParams,
              cartId,
            })
          );
        } else {
          // Other brands: go to delivery selection
          return router.push(
            addQueryToUrl('/checkout/delivery', {
              sku: productHandle,
              cartId,
            })
          );
        }
      }

      // Not logged in - redirect to registration with return URL
      return router.push(
        addQueryToUrl('/register', {
          returnUrl: '/checkout',
          ...queryParams,
          cartId,
        })
      );
    },
    [router, brand, isCustomerLoggedIn, locale]
  );
};
```

**Navigation flow**:
```
User clicks "Finish Order"
├── Logged in?
│   ├── Yes - Brand = YourCompany? → /checkout?cartId=123
│   └── Yes - Brand = Other → /checkout/delivery?sku=abc&cartId=123
└── No → /register?returnUrl=/checkout&cartId=123
```

**Key patterns:**
- Multi-conditional navigation based on auth + brand
- Different checkout flows per brand
- Return URL for post-login redirect
- Dependencies: `[router, brand, isCustomerLoggedIn, locale]`

**Why this pattern:**
- Handles complex business logic in one place
- Supports multiple brands with different flows
- Preserves state across auth flow with returnUrl
- Reusable across components

## Example 5: Using Next.js Link Component

**File**: `app/unified-spaces/checkout-header/header/components/cart-button/index.tsx:2`

```typescript
import Link from 'next/link';
import { Icon } from '@/components/Icon';
import { CartOutline24 } from '@/icons';

const CartButton: React.FC = () => {
  const { itemCount } = useCart();

  return (
    <Link href="/cart">
      <a className="cart-button">
        <Icon icon={<CartOutline24 />} />
        <span>View Cart</span>
        {itemCount > 0 && (
          <span className="cart-badge">{itemCount}</span>
        )}
      </a>
    </Link>
  );
};

// Link with query parameters
const CheckoutLink: React.FC<{ cartId: string }> = ({ cartId }) => {
  return (
    <Link
      href={{
        pathname: '/checkout',
        query: { cartId, step: 'address' },
      }}
    >
      <a>Continue to Checkout</a>
    </Link>
  );
};

// Conditional Link
const NavLink: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? (
    <Link href="/dashboard">
      <a>Dashboard</a>
    </Link>
  ) : (
    <Link href="/login">
      <a>Login</a>
    </Link>
  );
};
```

**Key patterns:**
- `<Link>` component wraps `<a>` tag (Pages Router requirement)
- `href="/cart"` for simple routes
- `href={{ pathname, query }}` for routes with query params
- Conditional rendering based on auth state
- Link prefetches linked page on hover

**Why use Link:**
- Client-side navigation (no full page reload)
- Automatic prefetching for better performance
- Preserves scroll position
- Works with browser back/forward buttons

## Example 6: Custom Navigation Hook with addQueryToUrl

**File**: `app/unified-spaces/plans-sections/single-question-flow/hooks/useNavigateToCheckout.ts`

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';
import { useSelectedLocale } from '@/hooks/useLocale';

interface NavigateToCheckoutParams {
  cartId: string;
  step?: 'address' | 'payment' | 'review';
  returnUrl?: string;
}

export const useNavigateToCheckout = () => {
  const router = useRouter();
  const locale = useSelectedLocale();

  return useCallback(
    (params: NavigateToCheckoutParams) => {
      const { cartId, step = 'address', returnUrl } = params;

      const queryParams: Record<string, string> = {
        locale,
        cartId,
        step,
      };

      if (returnUrl) {
        queryParams.returnUrl = returnUrl;
      }

      const url = addQueryToUrl('/checkout', queryParams);
      return router.push(url);
    },
    [router, locale]
  );
};

// Utility function
function addQueryToUrl(
  pathname: string,
  params: Record<string, string>
): string {
  const queryString = new URLSearchParams(params).toString();
  return `${pathname}?${queryString}`;
}

// Usage in multiple components
function ProductFlow() {
  const navigateToCheckout = useNavigateToCheckout();
  const { cartId } = useCart();

  return (
    <button
      onClick={() =>
        navigateToCheckout({
          cartId,
          step: 'payment',
        })
      }
    >
      Skip to Payment
    </button>
  );
}

function LoginFlow() {
  const navigateToCheckout = useNavigateToCheckout();

  return (
    <button
      onClick={() =>
        navigateToCheckout({
          cartId: 'temp',
          returnUrl: '/plans',
        })
      }
    >
      Create Account
    </button>
  );
}
```

**Key patterns:**
- Custom hook encapsulates navigation logic
- Type-safe parameters with TypeScript interface
- `addQueryToUrl` utility builds URL strings
- Optional parameters with defaults (`step = 'address'`)
- Conditional query params (`if (returnUrl)`)
- Reusable across multiple components

**URL examples**:
```typescript
navigateToCheckout({ cartId: '123' })
// → /checkout?locale=en-US&cartId=123&step=address

navigateToCheckout({ cartId: '123', step: 'payment' })
// → /checkout?locale=en-US&cartId=123&step=payment

navigateToCheckout({ cartId: '123', returnUrl: '/plans' })
// → /checkout?locale=en-US&cartId=123&step=address&returnUrl=/plans
```

**Why this pattern:**
- Single source of truth for checkout navigation
- Type-safe navigation parameters
- Consistent query param handling
- Easy to test independently

## Example 7: Router Events for Analytics

**File**: `app/hooks/useRouteChangeTracking.ts`

```typescript
import { useEffect } from 'react';
import { useRouter } from '@/libs/router';
import { trackPageView } from '@/analytics';

export function useRouteChangeTracking() {
  const router = useRouter();

  useEffect(() => {
    // Track initial page load
    trackPageView({
      url: router.asPath,
      pathname: router.pathname,
      query: router.query,
    });

    // Track subsequent route changes
    const handleRouteChange = (url: string) => {
      trackPageView({
        url,
        pathname: router.pathname,
        query: router.query,
      });
    };

    // Listen to route change events
    router.events.on('routeChangeComplete', handleRouteChange);

    // Cleanup listener
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);
}

// Usage in _app.tsx
function MyApp({ Component, pageProps }) {
  useRouteChangeTracking(); // Track all route changes

  return <Component {...pageProps} />;
}
```

**Router events**:
- `routeChangeStart` - Route change started
- `routeChangeComplete` - Route change finished
- `routeChangeError` - Route change error
- `beforeHistoryChange` - Before history changes
- `hashChangeStart` - Hash change started
- `hashChangeComplete` - Hash change finished

**Key patterns:**
- `router.events.on()` subscribes to route changes
- `router.events.off()` in cleanup function
- Track both initial load and subsequent navigations
- `router.asPath` includes full URL with query
- `router.pathname` is the route path only

**Why this pattern:**
- Centralized analytics tracking
- Automatic tracking for all route changes
- Cleanup prevents memory leaks
- Access to full route information

## Example 8: Preserving Query Parameters Across Navigation

**File**: `app/hooks/useNavigateWithPreservedParams.ts`

```typescript
import { useRouter } from '@/libs/router';
import { useCallback } from 'react';

export const useNavigateWithPreservedParams = () => {
  const router = useRouter();

  return useCallback(
    (pathname: string, additionalParams: Record<string, string> = {}) => {
      // Merge existing query with new params
      const query = {
        ...router.query,
        ...additionalParams,
      };

      return router.push({
        pathname,
        query,
      });
    },
    [router]
  );
};

// Usage
function MultiStepFlow() {
  const navigate = useNavigateWithPreservedParams();

  const goToNextStep = () => {
    // Preserves: locale, utm_source, utm_campaign
    // Adds: step=2
    navigate('/checkout', { step: '2' });
  };

  return <button onClick={goToNextStep}>Next Step</button>;
}
```

**Navigation flow**:
```
Current URL: /plans?locale=en-US&utm_source=email&utm_campaign=summer

After navigate('/checkout', { step: '2' }):
→ /checkout?locale=en-US&utm_source=email&utm_campaign=summer&step=2

// All existing params preserved, new param added
```

**Key patterns:**
- Spread `router.query` to preserve all existing params
- Merge with `additionalParams` (new params override existing)
- Useful for tracking params (utm_*, locale)
- Reusable navigation helper

**Why this pattern:**
- Preserves marketing attribution params
- Maintains locale across navigation
- Consistent query param handling
- Single function for all navigations

## Summary

These production examples demonstrate:

1. **Query Parameter Access**: Type-safe reading with `router.query` and type guards
2. **Programmatic Navigation**: `router.push()` for event-driven navigation
3. **Query Manipulation**: Remove/preserve/add params with `omit()` and spread
4. **Conditional Navigation**: Multi-branch navigation based on auth/brand/state
5. **Link Component**: Declarative navigation with prefetching
6. **Custom Navigation Hooks**: Reusable navigation logic with TypeScript types
7. **Router Events**: Analytics tracking on route changes
8. **Query Preservation**: Maintain tracking params across navigations

**Common patterns across examples:**
- Always import from `@/libs/router` (NOT `next/router`)
- Use `useCallback` for navigation functions with `[router]` dependency
- Type guard query params: `typeof query.param === 'string'`
- Use `addQueryToUrl()` utility for building URLs with query strings
- Custom hooks for reusable navigation logic
- Preserve tracking params (locale, utm_*) across navigation
- Clean up router event listeners in useEffect
- Link component for declarative navigation with prefetching

**Anti-patterns to avoid:**
- Importing from `next/router` directly (use `@/libs/router`)
- Not type-checking query params (can be `string | string[]`)
- Mutating `router.query` object (create new object with spread)
- Forgetting `useCallback` for navigation functions
- Not cleaning up router event listeners
- Using `router.push` without checking `router.isReady`
- Creating navigation logic directly in components (extract to custom hooks)
