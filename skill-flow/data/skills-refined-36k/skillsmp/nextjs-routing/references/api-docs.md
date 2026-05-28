# Next.js Routing - API Reference

**Version**: Next.js 13.x (Pages Router)

**IMPORTANT**: This codebase uses the custom `@/libs/router` wrapper, NOT `next/router` directly.

## Official Documentation

- **Next.js Router**: https://nextjs.org/docs/pages/api-reference/functions/use-router
- **Next.js Link**: https://nextjs.org/docs/pages/api-reference/components/link
- **Next.js Routing**: https://nextjs.org/docs/pages/building-your-application/routing

## useRouter Hook

Access the router object in any function component.

```typescript
import { useRouter } from '@/libs/router'; // NOT from 'next/router'

function Component() {
  const router = useRouter();

  return <div>Current path: {router.pathname}</div>;
}
```

**Returns**: `NextRouter` object

## Router Properties

### pathname

```typescript
router.pathname: string
```

Current route path (without query string).

```typescript
// URL: /checkout/address?step=1
router.pathname // "/checkout/address"
```

### query

```typescript
router.query: ParsedUrlQuery
```

Query parameters as an object. Values can be `string | string[]`.

```typescript
// URL: /product?id=123&tags=sale&tags=new
router.query // { id: "123", tags: ["sale", "new"] }

// Type guard for single value
if (typeof router.query.id === 'string') {
  const productId = router.query.id;
}

// Handle array values
const tags = Array.isArray(router.query.tags)
  ? router.query.tags
  : [router.query.tags];
```

### asPath

```typescript
router.asPath: string
```

Full path including query string and hash.

```typescript
// URL: /checkout/address?step=1#payment
router.asPath // "/checkout/address?step=1#payment"
```

### basePath

```typescript
router.basePath: string
```

Active base path (for internationalization).

```typescript
router.basePath // "" (usually empty)
```

### locale

```typescript
router.locale: string | undefined
```

Currently active locale.

```typescript
router.locale // "en-US"
```

### locales

```typescript
router.locales: string[] | undefined
```

All configured locales.

```typescript
router.locales // ["en-US", "de-DE", "fr-FR"]
```

### defaultLocale

```typescript
router.defaultLocale: string | undefined
```

Default configured locale.

```typescript
router.defaultLocale // "en-US"
```

### isReady

```typescript
router.isReady: boolean
```

Whether the router fields are updated client-side and ready for use.

```typescript
useEffect(() => {
  if (router.isReady) {
    // router.query is now available
    const { id } = router.query;
  }
}, [router.isReady, router.query]);
```

**Important**: On initial render, `router.query` may be empty. Always check `router.isReady`.

### isPreview

```typescript
router.isPreview: boolean
```

Whether the application is in preview mode.

### isFallback

```typescript
router.isFallback: boolean
```

Whether the current page is in fallback mode (for ISR).

## Router Methods

### push

Navigate to a new route.

```typescript
router.push(url: string | UrlObject, as?: string, options?: TransitionOptions): Promise<boolean>
```

**Parameters**:
- `url: string | UrlObject` - URL to navigate to
- `as?: string` - Optional decorator for the URL shown in browser
- `options?: TransitionOptions` - Additional options

**Returns**: `Promise<boolean>` - Resolves to `true` if route change was successful

```typescript
// Simple string URL
router.push('/about');

// URL with query parameters
router.push('/product?id=123');

// URL object (recommended)
router.push({
  pathname: '/product',
  query: { id: '123', category: 'electronics' },
});

// With options
router.push('/profile', undefined, { scroll: false });
```

**Options**:
```typescript
interface TransitionOptions {
  shallow?: boolean;       // Update URL without re-running getStaticProps
  locale?: string;         // Change locale
  scroll?: boolean;        // Scroll to top after navigation (default: true)
}
```

### replace

Replace the current history entry instead of adding a new one.

```typescript
router.replace(url: string | UrlObject, as?: string, options?: TransitionOptions): Promise<boolean>
```

Same signature as `push()`, but replaces current history entry.

```typescript
// Replaces instead of pushing
router.replace('/login');

// With query params
router.replace({
  pathname: '/search',
  query: { q: 'nextjs' },
});
```

**When to use**:
- Login redirects (don't want back button to return to login)
- Error page redirects
- Replacing invalid/temporary states

### back

Navigate back to the previous page.

```typescript
router.back(): void
```

```typescript
<button onClick={() => router.back()}>
  Go Back
</button>
```

### reload

Reload the current page.

```typescript
router.reload(): void
```

```typescript
<button onClick={() => router.reload()}>
  Refresh Page
</button>
```

### prefetch

Prefetch a page for faster client-side transitions.

```typescript
router.prefetch(url: string, as?: string, options?: PrefetchOptions): Promise<void>
```

```typescript
useEffect(() => {
  // Prefetch checkout page
  router.prefetch('/checkout');
}, [router]);
```

**Note**: `<Link>` components automatically prefetch by default.

## Router Events

Subscribe to router events.

```typescript
router.events.on(event: string, handler: (...args: any[]) => void): void
router.events.off(event: string, handler: (...args: any[]) => void): void
```

### Available Events

```typescript
// Route change started
'routeChangeStart' - (url: string, { shallow: boolean }) => void

// Route change completed
'routeChangeComplete' - (url: string, { shallow: boolean }) => void

// Route change error
'routeChangeError' - (err: Error, url: string, { shallow: boolean }) => void

// Before history change
'beforeHistoryChange' - (url: string, { shallow: boolean }) => void

// Hash change started
'hashChangeStart' - (url: string, { shallow: boolean }) => void

// Hash change completed
'hashChangeComplete' - (url: string, { shallow: boolean }) => void
```

### Example Usage

```typescript
import { useEffect } from 'react';
import { useRouter } from '@/libs/router';

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      console.log('App is changing to:', url);
      // Track page view in analytics
    };

    const handleRouteError = (err: Error, url: string) => {
      console.error('Route change error:', err, url);
    };

    router.events.on('routeChangeComplete', handleRouteChange);
    router.events.on('routeChangeError', handleRouteError);

    // Cleanup
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
      router.events.off('routeChangeError', handleRouteError);
    };
  }, [router]);

  return <Component {...pageProps} />;
}
```

## Link Component

Declarative navigation with automatic prefetching.

```typescript
import Link from 'next/link';

<Link href="/about">
  <a>About Us</a>
</Link>
```

### Props

```typescript
interface LinkProps {
  href: string | UrlObject;
  as?: string;
  replace?: boolean;
  scroll?: boolean;
  shallow?: boolean;
  passHref?: boolean;
  prefetch?: boolean;
  locale?: string;
  legacyBehavior?: boolean;
}
```

### Basic Usage

```typescript
// Simple link
<Link href="/about">
  <a>About</a>
</Link>

// Link with query params
<Link href={{ pathname: '/product', query: { id: '123' } }}>
  <a>View Product</a>
</Link>

// Link with hash
<Link href="/docs#getting-started">
  <a>Getting Started</a>
</Link>
```

### Props Examples

```typescript
// Replace history instead of push
<Link href="/login" replace>
  <a>Login</a>
</Link>

// Don't scroll to top after navigation
<Link href="/profile" scroll={false}>
  <a>Profile</a>
</Link>

// Disable prefetching
<Link href="/heavy-page" prefetch={false}>
  <a>Heavy Page</a>
</Link>

// Shallow routing (update URL without re-running data fetching)
<Link href="/products?sort=price" shallow>
  <a>Sort by Price</a>
</Link>
```

### Dynamic Routes

```typescript
// Dynamic route: /product/[id]
<Link href={`/product/${productId}`}>
  <a>View Product</a>
</Link>

// With object syntax (recommended)
<Link href={{ pathname: '/product/[id]', query: { id: productId } }}>
  <a>View Product</a>
</Link>
```

### External Links

```typescript
// For external URLs, use regular <a> tag
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Site
</a>
```

## TypeScript Types

### NextRouter

```typescript
import type { NextRouter } from 'next/router';

const router: NextRouter = useRouter();
```

### ParsedUrlQuery

```typescript
import type { ParsedUrlQuery } from 'querystring';

interface ParsedUrlQuery {
  [key: string]: string | string[] | undefined;
}

// Usage
const query: ParsedUrlQuery = router.query;
```

### UrlObject

```typescript
interface UrlObject {
  pathname?: string;
  query?: ParsedUrlQuery;
  hash?: string;
  auth?: string | null;
  hostname?: string | null;
  port?: string | null;
  protocol?: string | null;
  search?: string | null;
  slashes?: boolean | null;
}

// Usage
const url: UrlObject = {
  pathname: '/product',
  query: { id: '123', category: 'electronics' },
  hash: '#reviews',
};

router.push(url);
```

## URL Building Utilities

### addQueryToUrl

```typescript
function addQueryToUrl(
  pathname: string,
  params: Record<string, string>
): string {
  const queryString = new URLSearchParams(params).toString();
  return `${pathname}?${queryString}`;
}

// Usage
const url = addQueryToUrl('/checkout', {
  cartId: '123',
  step: 'payment',
});
// → "/checkout?cartId=123&step=payment"
```

### URLSearchParams

```typescript
// Build query string
const params = new URLSearchParams({
  q: 'nextjs',
  category: 'docs',
});

params.toString(); // "q=nextjs&category=docs"

// Parse query string
const params = new URLSearchParams(window.location.search);
const query = params.get('q'); // "nextjs"
```

### Omit Query Parameters

```typescript
import omit from 'lodash/omit';

// Remove specific query params
const cleanedQuery = omit(router.query, ['step', 'temp']);

// Navigate with cleaned query
router.push({
  pathname: '/checkout',
  query: cleanedQuery,
});
```

## Common Patterns

### Type-Safe Query Access

```typescript
function useQueryParam(key: string): string | undefined {
  const router = useRouter();
  const value = router.query[key];

  return typeof value === 'string' ? value : undefined;
}

// Usage
const productId = useQueryParam('id');
```

### Wait for Router Ready

```typescript
function MyComponent() {
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (router.isReady) {
      setIsReady(true);
    }
  }, [router.isReady]);

  if (!isReady) {
    return <div>Loading...</div>;
  }

  const { id } = router.query;
  return <div>Product ID: {id}</div>;
}
```

### Preserve Query on Navigation

```typescript
function navigateWithQuery(router: NextRouter, pathname: string) {
  router.push({
    pathname,
    query: router.query, // Preserve current query
  });
}
```

## Key Considerations

- Always import from `@/libs/router`, not `next/router`
- Check `router.isReady` before accessing `router.query`
- Query values can be `string | string[]` - always type check
- Use `Link` for internal navigation (enables prefetching)
- Use `router.push` for programmatic navigation
- Clean up router event listeners in useEffect
- Use `useCallback` when passing router-dependent functions
- URL object syntax is preferred over string concatenation
- Use `router.replace` for redirects that shouldn't add history
