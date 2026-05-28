# Phase 2: Project Initialization & CMS Integration Setup

## Step 1: CMS API Reference

The CMS GraphQL schema and all API operations are provided by the `sphereos-cms-api` skill (listed as a dependency). Reference that skill for:

- Authentication (`login` mutation)
- Content Types CRUD operations
- Content Entries CRUD operations
- Media uploads (`uploadMedia` mutation)
- Query operations (`contentEntryBySlug`, etc.)

No manual schema acquisition is needed.

## Step 2: Project Initialization

1. Initialize git repository

2. Create Next.js 14+ project with TypeScript, Tailwind, App Router

3. Set up directory structure:
```
src/
├── app/                    # Next.js App Router pages
├── components/
│   ├── ui/                 # Primitive UI components
│   ├── blocks/             # Section-level components
│   ├── layout/             # Layout components (header, footer)
│   └── shared/             # Shared utilities (Editable wrapper)
├── lib/
│   ├── content/            # Content read layer
│   ├── cms/                # CMS write operations (including media upload)
│   └── queries/            # GraphQL queries/mutations
├── types/                  # TypeScript interfaces
└── styles/                 # Global styles

docs/
├── figma-exports/          # PDF exports from Figma
└── cms-entries/            # CMS content documentation

project-config/
└── config.md               # Project configuration
```

4. Install dependencies:
```bash
npm install @apollo/client graphql
npm init playwright@latest
```

5. Create `.env.local` from the template in `/project-config/`:
```
NEXT_PUBLIC_CMS_GRAPHQL_URL=[CMS GraphQL URL]
CMS_ORGANIZATION_ID=[CMS Organization ID]
# Optional: CMS_PROPERTY_ID=[Property ID if multi-property setup]
```

**Note:** No CDN credentials needed — media uploads go through the CMS API (`uploadMedia` mutation).

## Step 3: CMS Integration Setup

### 3.1 Create Edit Mode Middleware

**CRITICAL:** Create middleware to handle edit mode cache bypass. This sets a cookie when `?edit=true` is in the URL, enabling the inline editor to show fresh content after saves.

Create `/src/middleware.ts`:

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Middleware to handle CMS edit mode cookie.
 * Sets a cookie when ?edit=true is in the URL so the server can bypass cache.
 * Removes the cookie when ?edit=false or edit param is not present.
 */
export function middleware(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const editParam = searchParams.get('edit');
  const response = NextResponse.next();

  if (editParam === 'true') {
    // Set cookie for edit mode (expires in 1 hour)
    response.cookies.set('cms-edit-mode', 'true', {
      httpOnly: false,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60, // 1 hour
    });
  } else if (editParam === 'false') {
    // Explicitly exiting edit mode - remove the cookie
    response.cookies.delete('cms-edit-mode');
  }
  // If no edit param, leave cookie as-is (allows navigating between pages in edit mode)

  return response;
}

export const config = {
  // Run middleware on all page routes (not API routes, static files, etc.)
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.).*)',
  ],
};
```

### 3.2 Create Apollo Client

Create `/src/lib/apollo-client.ts`:

```typescript
import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const CMS_GRAPHQL_URL = process.env.NEXT_PUBLIC_CMS_GRAPHQL_URL || 'http://localhost:3000/graphql';

/**
 * Check if we're in CMS edit mode by reading the cookie.
 * The cookie is set by middleware when ?edit=true is in the URL.
 *
 * This function safely handles both server and client contexts.
 */
function isEditMode(): boolean {
  // Server-side: try to read from next/headers cookies
  if (typeof window === 'undefined') {
    try {
      // Dynamic import to avoid bundling next/headers in client code
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { cookies } = require('next/headers');
      const cookieStore = cookies();
      return cookieStore.get('cms-edit-mode')?.value === 'true';
    } catch {
      // cookies() throws when not in a request context
      return false;
    }
  }

  // Client-side: read from document.cookie
  if (typeof document !== 'undefined') {
    return document.cookie.includes('cms-edit-mode=true');
  }

  return false;
}

/**
 * Create a fetch function that respects edit mode.
 * In edit mode, bypasses Next.js Data Cache to ensure fresh data.
 */
function createFetch(): typeof fetch {
  const editMode = isEditMode();

  if (editMode) {
    // Edit mode: bypass cache for fresh data
    return (input, init) => fetch(input, { ...init, cache: 'no-store' });
  }

  // Normal mode: use default caching
  return fetch;
}

/**
 * Create Apollo Client for server-side rendering.
 * Used in React Server Components with async/await.
 *
 * Automatically bypasses cache when in edit mode (detected via cookie).
 */
export function getServerClient(token?: string) {
  const httpLink = new HttpLink({
    uri: CMS_GRAPHQL_URL,
    fetch: createFetch(),
  });

  const authLink = setContext((_, { headers }) => ({
    headers: {
      ...headers,
      ...(token && { authorization: `Bearer ${token}` }),
    },
  }));

  return new ApolloClient({
    link: from([authLink, httpLink]),
    cache: new InMemoryCache(),
    defaultOptions: {
      query: {
        fetchPolicy: 'no-cache',
        errorPolicy: 'all',
      },
    },
  });
}

/**
 * Create a basic client for public queries (no auth).
 *
 * Automatically bypasses cache when in edit mode (detected via cookie).
 */
export function getPublicClient() {
  const httpLink = new HttpLink({
    uri: CMS_GRAPHQL_URL,
    fetch: createFetch(),
  });

  return new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
    defaultOptions: {
      query: {
        fetchPolicy: 'no-cache',
      },
    },
  });
}
```

### 3.3 Create GraphQL Queries

Create `/src/lib/queries/index.ts`:
   - **IMPORTANT:** Read schema first, match exact structure

### 3.4 Create Content Read Layer

Create `/src/lib/content/index.ts`:
   - `getPageContent(pageSlug: string)`
   - `getSiteSettings()`
   - `getNavigation()`
   - `getFooterContent()`

**CRITICAL:** Include `transformImageUrls()` function as documented in SKILL.md.

### 3.5 Create CMS Write Utilities

Create `/src/lib/cms/index.ts`:
   - Include media upload function using CMS `uploadMedia` mutation
   - Reference `sphereos-cms-api` skill for mutation details

### 3.6 Create Editable Helper

Create `/src/components/shared/Editable.tsx`:

```typescript
interface EditableProps {
  entry: string;
  field: string;
  type?: 'text' | 'richtext' | 'image' | 'array';
  as?: keyof JSX.IntrinsicElements;
  className?: string;
  children: React.ReactNode;
}

export function Editable({ entry, field, type, as: Tag = 'span', className, children }: EditableProps) {
  return (
    <Tag
      className={className}
      data-cms-entry={entry}
      data-cms-field={field}
      {...(type && { 'data-cms-type': type })}
    >
      {children}
    </Tag>
  );
}
```

## Edit Mode Caching Behavior

| Visitor Type | URL | Behavior |
|-------------|-----|----------|
| Regular visitor | `site.com/` | Cached responses (fast) |
| Editor | `site.com/?edit=true` | Fresh data on every request |
| Editor navigating | `site.com/about` (with cookie) | Fresh data persists |
| Exit edit mode | `site.com/?edit=false` | Cookie removed, back to cached |

This ensures:
- **Performance:** Regular visitors get fast cached responses
- **Editor experience:** Content editors see changes immediately after saving

## Git Commit

```bash
git commit -m "feat: project initialization with Next.js, Tailwind, Apollo Client, middleware, Editable component"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 2: Project initialized" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-3-TOKENS.md](PHASE-3-TOKENS.md)
