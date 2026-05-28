---
name: production-audit
description: Comprehensive production readiness audit for Next.js/NestJS applications. Covers security, performance, code quality, accessibility, SEO, error handling, and operational readiness.
version: 1.3.0
author: SphereOS
license: MIT
tags: [Audit, Security, Performance, Code Quality, Production, Next.js, NestJS]
dependencies: []
allowed-tools: Read, Glob, Grep, Bash, Task, WebFetch
github-repo: gautam-lulla/claude-skills
skill-path: production-audit
---

## FIRST: Check for Updates

**Before proceeding, check if a newer version is available:**

1. Read local version from `~/.claude/skills/production-audit/SKILL.md` frontmatter
2. Fetch remote version: `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/production-audit/SKILL.md`
3. Compare the `version:` field in both

**If remote version > local version**, use AskUserQuestion:
- Question: "A newer version of p-audit is available. Current: [local] → Latest: [remote]. What would you like to do?"
- Options:
  1. "Update and continue (Recommended)"
  2. "Continue with current version"
  3. "View changelog"

**If user selects "Update and continue":**
- Fetch SKILL.md, CHANGELOG.md, LEARNINGS.md from GitHub raw URL
- Save to `~/.claude/skills/production-audit/`
- Confirm: "Updated p-audit to version [X]. Proceeding..."

**If user selects "View changelog":**
- Fetch and display `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/production-audit/CHANGELOG.md`
- Then ask again

**If versions match**, proceed silently (no prompt).

---

# Production Readiness Audit

This skill performs a comprehensive audit of a Next.js/NestJS application to ensure it is ready for production deployment. The audit covers security, performance, code quality, **developer experience & code consistency** (recommended for early-stage projects), accessibility, SEO, error handling, and operational readiness.

---

## IMPORTANT: First Step - Select Project

**Before running any audit checks, you MUST ask the user which project to audit using AskUserQuestion:**

```
Use AskUserQuestion with:
- Question: "Which project should I run the production audit on?"
- Options:
  1. Current directory ([show actual pwd path])
  2. Enter a different path
```

If the user selects option 2 ("Enter a different path"), they will type the path. Use that path for all subsequent audit commands.

Store the selected project path and use it as the base path for ALL file searches, reads, and commands throughout the audit.

---

## How to Use This Skill

Invoke with `/production-audit` and Claude will:

1. **Ask which project to audit** (current directory or custom path)
2. Read the project structure and configuration files
3. Perform automated checks across all audit categories
4. Generate a detailed report with findings
5. Provide severity ratings (Critical, High, Medium, Low)
6. Suggest fixes for each issue found

---

## Audit Categories

1. [Software Architecture Audit](#1-software-architecture-audit)
2. [Security Audit](#2-security-audit)
3. [Performance Audit](#3-performance-audit)
4. [Code Quality Audit](#4-code-quality-audit)
5. [Developer Experience & Code Consistency Audit](#5-developer-experience--code-consistency-audit) ⭐ *Early-stage priority*
6. [Error Handling Audit](#6-error-handling-audit)
7. [Accessibility Audit](#7-accessibility-audit)
8. [SEO Audit](#8-seo-audit)
9. [Environment & Configuration Audit](#9-environment--configuration-audit)
10. [Dependencies Audit](#10-dependencies-audit)
11. [Build & Deployment Audit](#11-build--deployment-audit)
12. [Monitoring & Observability Audit](#12-monitoring--observability-audit)

---

## 1. Software Architecture Audit

### 1.1 Project Structure & Organization

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Directory structure | High | Inconsistent or flat structure, no clear separation |
| Feature organization | Medium | Related files scattered across directories |
| Barrel exports | Medium | Missing or inconsistent index.ts files |
| Colocation | Medium | Related files not colocated (component + styles + tests) |

**Expected Next.js App Router Structure:**
```
src/
├── app/                      # Routes and pages
│   ├── (marketing)/          # Route groups for layouts
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── api/                  # API routes
│   ├── layout.tsx            # Root layout
│   ├── error.tsx             # Error boundary
│   └── not-found.tsx         # 404 page
├── components/
│   ├── ui/                   # Primitive/atomic components
│   ├── blocks/               # Composite sections
│   └── layout/               # Layout components
├── lib/                      # Utilities and shared logic
│   ├── utils/                # Pure utility functions
│   ├── hooks/                # Custom React hooks
│   ├── context/              # React context providers
│   └── api/                  # API client/fetching layer
├── types/                    # TypeScript type definitions
├── config/                   # Configuration constants
└── styles/                   # Global styles
```

**Audit Checklist:**
- [ ] Clear separation between app routes and reusable code
- [ ] Components organized by type (ui/blocks/layout) or feature
- [ ] Shared utilities in `lib/` not scattered in components
- [ ] Types centralized or colocated with relevant code
- [ ] No business logic in page components (delegated to lib/)

### 1.2 Component Architecture

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Single Responsibility | High | Components doing too many things |
| Prop drilling | High | Props passed through 3+ levels |
| Component size | Medium | Components > 200-300 lines |
| Presentation vs Container | Medium | Mixed data fetching and UI rendering |
| Reusability | Medium | Duplicate component logic |

**Component Hierarchy Pattern:**
```
Pages (Route Components)
  └── Fetch data, handle routing
  └── Pass data to templates/blocks

Templates (Page-level layouts)
  └── Compose blocks into page structure
  └── No data fetching

Blocks (Section components)
  └── Self-contained sections (Hero, Features, etc.)
  └── Receive content as props

UI Components (Primitives)
  └── Button, Input, Card, etc.
  └── Purely presentational
  └── Design system atoms
```

**Anti-patterns to Flag:**
```typescript
// ❌ BAD: Component doing too much
export function UserDashboard() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState([]);
  const [notifications, setNotifications] = useState([]);
  // ... 300 lines of mixed concerns
}

// ✅ GOOD: Separated concerns
export function UserDashboard() {
  return (
    <DashboardLayout>
      <UserProfile />
      <UserPosts />
      <UserNotifications />
    </DashboardLayout>
  );
}
```

**Audit Commands:**
```bash
# Find large components (>200 lines)
find src/components -name "*.tsx" -exec wc -l {} \; | awk '$1 > 200 {print}'

# Check for prop drilling patterns
grep -r "props\." --include="*.tsx" src/components | wc -l
```

### 1.3 Data Flow & State Management

| Check | Severity | What to Look For |
|-------|----------|------------------|
| State location | High | Global state for local concerns |
| Server vs Client state | High | Duplicating server data in client state |
| Prop drilling depth | Medium | Data passed through many component layers |
| State updates | Medium | Unnecessary re-renders from state changes |
| Cache strategy | Medium | No caching or over-caching |

**State Categories:**
| Type | Where to Store | Example |
|------|----------------|---------|
| Server state | React Query / Apollo / Server Components | User data, CMS content |
| Global UI state | Context or Zustand | Theme, sidebar open |
| Local UI state | useState | Form inputs, modals |
| URL state | searchParams | Filters, pagination |
| Form state | React Hook Form / useFormState | Form values, validation |

**Data Flow Pattern (Next.js App Router):**
```
Server Component (page.tsx)
  └── Fetch data from CMS/API
  └── Pass as props to children

Client Components (interactive parts only)
  └── Local UI state (useState)
  └── Form state (useFormState)
  └── NO data fetching (receive as props)
```

**Anti-patterns to Flag:**
```typescript
// ❌ BAD: Fetching in client component
'use client';
export function ProductList() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch('/api/products').then(res => res.json()).then(setProducts);
  }, []);
  // ...
}

// ✅ GOOD: Server component fetches, client receives
// page.tsx (Server Component)
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// ProductList.tsx (Client Component for interactivity)
'use client';
export function ProductList({ products }: { products: Product[] }) {
  // Only UI state here
}
```

### 1.4 Separation of Concerns

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Business logic in components | High | Complex logic mixed with JSX |
| API calls in components | High | fetch/axios directly in components |
| Hardcoded values | Medium | Magic numbers/strings in components |
| Style logic in components | Low | Complex conditional styling inline |

**Layer Separation:**
```
┌─────────────────────────────────────────────┐
│  Presentation Layer (components/)           │
│  - React components                         │
│  - UI rendering only                        │
│  - Receives data as props                   │
└─────────────────────────────────────────────┘
                    ↑ props
┌─────────────────────────────────────────────┐
│  Application Layer (app/, lib/hooks/)       │
│  - Page components                          │
│  - Custom hooks                             │
│  - Orchestrates data flow                   │
└─────────────────────────────────────────────┘
                    ↑ data
┌─────────────────────────────────────────────┐
│  Data Layer (lib/api/, lib/content/)        │
│  - API clients                              │
│  - Data fetching functions                  │
│  - Data transformation                      │
└─────────────────────────────────────────────┘
                    ↑ raw data
┌─────────────────────────────────────────────┐
│  External Services (CMS, APIs, DB)          │
└─────────────────────────────────────────────┘
```

**Expected File Organization:**
```typescript
// lib/content/index.ts - Data fetching abstraction
export async function getPageContent(slug: string) { ... }
export async function getProducts() { ... }

// lib/utils/formatters.ts - Pure utility functions
export function formatPrice(amount: number) { ... }
export function formatDate(date: Date) { ... }

// lib/hooks/useCart.ts - Stateful logic
export function useCart() { ... }

// components/ui/Button.tsx - Presentational only
export function Button({ children, variant }) { ... }
```

### 1.5 API Design & Data Fetching

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Consistent fetching pattern | High | Mixed fetch methods across codebase |
| Error handling | High | Inconsistent or missing error handling |
| Loading states | Medium | No loading indicators |
| Caching strategy | Medium | No caching or improper cache invalidation |
| Type safety | Medium | Untyped API responses |

**Data Fetching Layer Pattern:**
```typescript
// lib/api/client.ts - Base API client
class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`);
    if (!response.ok) {
      throw new APIError(response.status, await response.text());
    }
    return response.json();
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    // ...
  }
}

// lib/api/products.ts - Domain-specific functions
export async function getProducts(): Promise<Product[]> {
  return apiClient.get<Product[]>('/products');
}

export async function getProduct(id: string): Promise<Product> {
  return apiClient.get<Product>(`/products/${id}`);
}
```

**GraphQL Pattern (Apollo/SphereOS CMS):**
```typescript
// lib/queries/index.ts - Query definitions
export const GET_PAGE_CONTENT = gql`...`;

// lib/content/index.ts - Content fetching abstraction
export async function getPageContent(slug: string) {
  const client = getServerClient();
  const { data } = await client.query({
    query: GET_PAGE_CONTENT,
    variables: { slug },
  });
  return data?.page ?? null;
}
```

### 1.6 Type System Architecture

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Type coverage | High | `any` types, missing types |
| Type organization | Medium | Types scattered or duplicated |
| API type safety | High | Untyped API responses |
| Component prop types | Medium | Missing or incomplete prop interfaces |
| Discriminated unions | Low | Not using for complex state |

**Type Organization Pattern:**
```typescript
// types/index.ts - Re-export all types
export * from './api';
export * from './content';
export * from './components';

// types/api.ts - API response types
export interface APIResponse<T> {
  data: T;
  meta: {
    total: number;
    page: number;
  };
}

export interface APIError {
  code: string;
  message: string;
}

// types/content.ts - CMS content types
export interface Page {
  id: string;
  slug: string;
  title: string;
  content: PageContent;
}

export interface PageContent {
  hero: HeroSection;
  sections: Section[];
}

// types/components.ts - Shared component types
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}
```

**Type Inference Best Practices:**
```typescript
// ✅ GOOD: Infer from schema/API
type Product = Awaited<ReturnType<typeof getProduct>>;

// ✅ GOOD: Discriminated unions for state
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// ✅ GOOD: Zod for runtime validation + type inference
const ProductSchema = z.object({
  id: z.string(),
  name: z.string(),
  price: z.number(),
});
type Product = z.infer<typeof ProductSchema>;
```

### 1.7 Dependency Injection & Testability

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Hard-coded dependencies | Medium | Direct imports of external services |
| Global singletons | Medium | Modules with side effects on import |
| Testability | Medium | Functions that can't be unit tested |
| Mocking difficulty | Low | Tight coupling making mocks complex |

**Dependency Injection Pattern:**
```typescript
// ❌ BAD: Hard-coded dependency
export async function getProducts() {
  const response = await fetch('https://api.example.com/products');
  return response.json();
}

// ✅ GOOD: Injectable dependency
export function createProductService(apiClient: APIClient) {
  return {
    async getProducts() {
      return apiClient.get<Product[]>('/products');
    },
    async getProduct(id: string) {
      return apiClient.get<Product>(`/products/${id}`);
    },
  };
}

// Usage
const productService = createProductService(apiClient);

// Testing
const mockClient = { get: jest.fn() };
const testService = createProductService(mockClient);
```

### 1.8 Scalability Patterns

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Code splitting | High | Large bundles, no dynamic imports |
| Lazy loading | Medium | All components loaded upfront |
| Route-based splitting | Medium | Not using Next.js automatic splitting |
| Feature flags | Low | No mechanism for gradual rollouts |

**Code Splitting Patterns:**
```typescript
// ✅ Dynamic import for heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // If client-only
});

// ✅ Route groups for different layouts
app/
├── (marketing)/     # Marketing pages layout
│   ├── layout.tsx
│   └── page.tsx
├── (app)/           # App dashboard layout
│   ├── layout.tsx
│   └── dashboard/
└── (auth)/          # Auth layout
    ├── layout.tsx
    └── login/

// ✅ Parallel routes for complex UIs
app/
├── @modal/          # Modal slot
├── @sidebar/        # Sidebar slot
└── layout.tsx       # Composes slots
```

### 1.9 Design Patterns & Conventions

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Consistent patterns | Medium | Different approaches for same problem |
| Named exports | Low | Default exports everywhere |
| File naming | Low | Inconsistent naming conventions |
| Import organization | Low | Messy, unordered imports |

**Recommended Patterns:**

**Compound Components (for complex UI):**
```typescript
// Usage
<Accordion>
  <Accordion.Item>
    <Accordion.Trigger>Title</Accordion.Trigger>
    <Accordion.Content>Content</Accordion.Content>
  </Accordion.Item>
</Accordion>
```

**Render Props / Children as Function:**
```typescript
<DataFetcher url="/api/users">
  {({ data, loading, error }) => (
    loading ? <Spinner /> : <UserList users={data} />
  )}
</DataFetcher>
```

**Custom Hooks for Logic Reuse:**
```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}
```

### 1.10 Architecture Checklist

**Project Structure:**
- [ ] Clear directory organization (app/, components/, lib/, types/)
- [ ] Consistent file naming convention
- [ ] Related files colocated
- [ ] Barrel exports (index.ts) for clean imports

**Component Architecture:**
- [ ] Single responsibility per component
- [ ] No prop drilling (use composition or context)
- [ ] Components < 200 lines
- [ ] Clear separation: UI components vs page components

**Data Flow:**
- [ ] Server Components for data fetching
- [ ] Client Components only for interactivity
- [ ] Centralized data fetching layer (lib/content/ or lib/api/)
- [ ] Proper state management (server state vs client state)

**Separation of Concerns:**
- [ ] No business logic in components
- [ ] No direct API calls in components
- [ ] Utilities extracted to lib/
- [ ] Types centralized in types/

**Type Safety:**
- [ ] No `any` types
- [ ] All API responses typed
- [ ] All component props typed
- [ ] Zod or similar for runtime validation

**Scalability:**
- [ ] Dynamic imports for heavy components
- [ ] Route-based code splitting
- [ ] Feature organization supports team scaling

---

## 2. Security Audit

### 1.1 Environment Variables

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Secrets in code | Critical | API keys, passwords, tokens hardcoded in source files |
| .env in git | Critical | `.env`, `.env.local`, `.env.production` not in `.gitignore` |
| NEXT_PUBLIC exposure | High | Sensitive values prefixed with `NEXT_PUBLIC_` (exposes to client) |
| Missing env validation | Medium | No runtime validation of required environment variables |

**Files to Check:**
```
.env*
.gitignore
src/**/*.ts
src/**/*.tsx
next.config.js
```

**Audit Commands:**
```bash
# Check for hardcoded secrets patterns
grep -r "sk_live\|sk_test\|api_key\|apikey\|secret\|password\|token" --include="*.ts" --include="*.tsx" --include="*.js" src/

# Check if .env files are gitignored
grep -E "^\.env" .gitignore

# List all NEXT_PUBLIC variables
grep -r "NEXT_PUBLIC_" --include="*.ts" --include="*.tsx" src/
```

**Required Fixes:**
- [ ] All secrets stored in environment variables only
- [ ] `.env*` files in `.gitignore`
- [ ] Only non-sensitive values use `NEXT_PUBLIC_` prefix
- [ ] Environment variables validated at startup

### 1.2 Authentication & Authorization

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Auth on protected routes | Critical | Routes accessible without authentication |
| Session handling | High | Insecure session storage, missing expiration |
| CSRF protection | High | Forms without CSRF tokens |
| Input validation | High | User input not validated/sanitized |

**Files to Check:**
```
src/app/**/page.tsx
src/middleware.ts
src/lib/auth/
```

**Checklist:**
- [ ] Protected routes have auth checks
- [ ] Middleware validates authentication tokens
- [ ] Sessions expire appropriately
- [ ] User input is validated before use

### 1.3 HTTP Security Headers

| Header | Severity | Recommended Value |
|--------|----------|-------------------|
| Strict-Transport-Security | High | `max-age=31536000; includeSubDomains` |
| X-Content-Type-Options | Medium | `nosniff` |
| X-Frame-Options | Medium | `DENY` or `SAMEORIGIN` |
| X-XSS-Protection | Low | `1; mode=block` |
| Content-Security-Policy | High | Project-specific CSP |
| Referrer-Policy | Medium | `strict-origin-when-cross-origin` |

**Files to Check:**
```
next.config.js
vercel.json
middleware.ts
```

**Example Configuration (next.config.js):**
```javascript
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-XSS-Protection', value: '1; mode=block' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
];

module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};
```

### 1.4 Data Exposure

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Over-fetching | High | GraphQL/API returning more data than needed |
| Console.log leaks | Medium | Sensitive data logged to console |
| Source maps in prod | Medium | Source maps exposing code structure |
| Error message exposure | Medium | Stack traces shown to users |

**Audit Commands:**
```bash
# Check for console.log statements
grep -r "console\." --include="*.ts" --include="*.tsx" src/

# Check source map configuration
grep -r "productionBrowserSourceMaps" next.config.js
```

---

## 3. Performance Audit

### 2.1 Bundle Size

| Check | Severity | Threshold |
|-------|----------|-----------|
| First Load JS | High | < 100KB per route |
| Total bundle size | Medium | < 250KB gzipped |
| Large dependencies | Medium | No single dep > 50KB |

**Audit Commands:**
```bash
# Analyze bundle
npm run build
npx @next/bundle-analyzer

# Check bundle size
ls -la .next/static/chunks/
```

**Common Issues:**
- Importing entire libraries (`import _ from 'lodash'` vs `import debounce from 'lodash/debounce'`)
- Large icon libraries
- Unused dependencies
- Missing code splitting

### 2.2 Image Optimization

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Next.js Image component | High | Using `<img>` instead of `<Image>` |
| Image sizing | Medium | Missing width/height or sizes prop |
| Format optimization | Medium | Not using WebP/AVIF |
| Lazy loading | Low | Above-fold images not prioritized |

**Files to Check:**
```
src/components/**/*.tsx
src/app/**/*.tsx
next.config.js (images.remotePatterns)
```

**Checklist:**
- [ ] All images use Next.js `<Image>` component
- [ ] Remote image domains configured
- [ ] Appropriate sizes prop for responsive images
- [ ] `priority` set for LCP images
- [ ] Images are appropriately compressed

### 2.3 Rendering Strategy

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Unnecessary client components | High | `'use client'` on components that don't need it |
| Missing static generation | Medium | Dynamic pages that could be static |
| N+1 queries | High | Multiple sequential data fetches |
| Missing caching | Medium | No revalidation strategy |

**Files to Check:**
```
src/app/**/page.tsx
src/lib/content/
src/lib/queries/
```

**Checklist:**
- [ ] Server Components used by default
- [ ] Client Components only where needed (interactivity, hooks)
- [ ] Parallel data fetching with `Promise.all()`
- [ ] Appropriate `revalidate` or `dynamic` settings
- [ ] Streaming/Suspense for slow data

### 2.4 Core Web Vitals

| Metric | Target | Severity if Failed |
|--------|--------|-------------------|
| LCP (Largest Contentful Paint) | < 2.5s | High |
| FID (First Input Delay) | < 100ms | High |
| CLS (Cumulative Layout Shift) | < 0.1 | Medium |
| TTFB (Time to First Byte) | < 800ms | Medium |

**Audit Commands:**
```bash
# Run Lighthouse
npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse-report.json

# Or use Chrome DevTools Lighthouse tab
```

**Common Fixes:**
- LCP: Optimize hero images, preload fonts
- FID: Reduce JavaScript, defer non-critical scripts
- CLS: Set explicit dimensions on images/embeds
- TTFB: Optimize server response, use CDN

---

## 4. Code Quality Audit

### 4.1 TypeScript Strict Mode

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Strict mode enabled | High | `"strict": true` in tsconfig.json |
| No `any` types | Medium | Explicit or implicit `any` usage |
| No ts-ignore | Medium | `@ts-ignore` or `@ts-nocheck` comments |
| Proper null handling | Medium | Missing null checks |

**Files to Check:**
```
tsconfig.json
src/**/*.ts
src/**/*.tsx
```

**Audit Commands:**
```bash
# Check for any types
grep -r ": any" --include="*.ts" --include="*.tsx" src/

# Check for ts-ignore
grep -r "@ts-ignore\|@ts-nocheck" --include="*.ts" --include="*.tsx" src/

# Run type check
npx tsc --noEmit
```

**Required tsconfig.json Settings:**
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### 4.2 Linting & Formatting

| Check | Severity | What to Look For |
|-------|----------|------------------|
| ESLint configured | Medium | Missing or incomplete ESLint config |
| No lint errors | Medium | `npm run lint` fails |
| Prettier configured | Low | Inconsistent formatting |
| Pre-commit hooks | Low | No husky/lint-staged |

**Audit Commands:**
```bash
# Run linting
npm run lint

# Check for ESLint config
cat .eslintrc.json || cat .eslintrc.js || cat eslint.config.js
```

### 4.3 Code Organization

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Component size | Medium | Components > 300 lines |
| File organization | Low | Inconsistent file structure |
| Naming conventions | Low | Inconsistent naming |
| Dead code | Low | Unused exports, functions, variables |

**Checklist:**
- [ ] Components are focused and single-purpose
- [ ] Consistent file naming (kebab-case or PascalCase)
- [ ] Logical folder structure
- [ ] No commented-out code blocks
- [ ] No unused imports

---

## 5. Developer Experience & Code Consistency Audit

> **Early-Stage Priority:** This section is critical for new projects. Establishing clean, consistent patterns early prevents technical debt and makes the codebase easier to maintain as the team grows.

### 5.1 Module Structure Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Consistent module layout | High | Modules organized differently (some flat, some nested) |
| Index/barrel exports | High | Some modules export via index.ts, others don't |
| File colocation | High | Related files scattered (entity separate from its DTOs) |
| Naming alignment | High | Module name doesn't match folder/file naming |

**Expected Module Structure (NestJS Example):**
```
src/modules/
├── user/
│   ├── index.ts                 # Barrel export
│   ├── user.module.ts           # Module definition
│   ├── entities/
│   │   └── user.entity.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   ├── services/
│   │   └── user.service.ts
│   ├── resolvers/               # or controllers/
│   │   └── user.resolver.ts
│   └── __tests__/               # or *.spec.ts colocated
│       └── user.service.spec.ts
├── auth/                        # Same structure
├── content/                     # Same structure
└── media/                       # Same structure
```

**Anti-patterns to Flag:**
```
❌ Inconsistent structure across modules:
modules/
├── user/
│   ├── user.service.ts          # Flat structure
│   ├── user.controller.ts
│   └── user.entity.ts
├── auth/
│   ├── services/                # Nested structure
│   │   └── auth.service.ts
│   ├── controllers/
│   │   └── auth.controller.ts
│   └── entities/
│       └── auth.entity.ts

❌ Missing index.ts in some modules but not others
❌ Some modules use singular names (user/) others plural (users/)
```

**Audit Commands:**
```bash
# Compare module structures
for dir in src/modules/*/; do echo "=== $dir ===" && ls -la "$dir"; done

# Find modules missing index.ts
find src/modules -maxdepth 2 -type d ! -exec test -e '{}/index.ts' \; -print

# Check for inconsistent nesting
find src/modules -type f -name "*.service.ts" | head -10
find src/modules -type f -name "*.entity.ts" | head -10
```

### 5.2 Naming Convention Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| File naming | High | Mixed kebab-case and PascalCase files |
| Class naming | High | Inconsistent suffixes (Service vs Svc, Controller vs Ctrl) |
| Variable naming | Medium | Mixed camelCase and snake_case |
| Database columns | Medium | Inconsistent column naming (camelCase vs snake_case) |
| GraphQL fields | Medium | Inconsistent field naming across types |

**Naming Conventions Matrix:**

| Element | Convention | Example |
|---------|------------|---------|
| Files | kebab-case | `user-profile.service.ts` |
| Classes | PascalCase + Suffix | `UserProfileService` |
| Interfaces | PascalCase (no I prefix) | `UserProfile` |
| Variables | camelCase | `userProfile` |
| Constants | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| Database tables | snake_case (plural) | `user_profiles` |
| Database columns | snake_case | `created_at` |
| GraphQL types | PascalCase | `UserProfile` |
| GraphQL fields | camelCase | `createdAt` |
| Enum values | PascalCase or SCREAMING_SNAKE | `Active` or `ACTIVE` |

**Anti-patterns to Flag:**
```typescript
// ❌ Inconsistent file naming
user-profile.service.ts    // kebab-case
UserProfile.entity.ts      // PascalCase
userProfile.dto.ts         // camelCase

// ❌ Inconsistent class suffixes
class UserService {}       // "Service"
class AuthSvc {}           // "Svc"
class ContentManager {}    // "Manager"

// ❌ Mixed conventions in same entity
@Entity('UserProfiles')    // PascalCase table
class UserProfile {
  @Column()
  firstName: string;       // camelCase property

  @Column({ name: 'last_name' })
  lastName: string;        // snake_case in DB, camelCase in code (OK)

  @Column()
  created_at: Date;        // snake_case property (inconsistent!)
}
```

**Audit Commands:**
```bash
# Check for mixed file naming patterns
find src -name "*.ts" | xargs -I {} basename {} | sort | uniq -c | sort -rn

# Find files not following kebab-case
find src -name "*.ts" | grep -E "[A-Z]" | grep -v node_modules

# Check for inconsistent class suffixes
grep -r "class.*Service\|class.*Svc\|class.*Manager" --include="*.ts" src/
```

### 5.3 Import/Export Pattern Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Import organization | Medium | Unordered, ungrouped imports |
| Barrel exports | High | Inconsistent use of index.ts re-exports |
| Circular dependencies | Critical | Modules importing each other |
| Relative vs absolute | Medium | Mixed import path styles |
| Named vs default exports | Medium | Inconsistent export style |

**Expected Import Order:**
```typescript
// 1. Node built-ins
import { readFile } from 'fs';

// 2. External packages (npm)
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';

// 3. Internal aliases (@/ paths)
import { DatabaseService } from '@/database';
import { BaseEntity } from '@/common';

// 4. Relative imports (parent first, then siblings)
import { UserEntity } from '../entities';
import { CreateUserDto } from './dto';
```

**Anti-patterns to Flag:**
```typescript
// ❌ Deep relative imports (use barrel exports or aliases)
import { UserEntity } from '../../../modules/user/entities/user.entity';

// ❌ Importing from index when you could import directly (in same module)
import { UserService } from './index';  // Should be './user.service'

// ❌ Inconsistent export style within project
// file1.ts: export default class Foo {}
// file2.ts: export class Bar {}

// ❌ Circular dependency
// user.service.ts imports auth.service.ts
// auth.service.ts imports user.service.ts
```

**Audit Commands:**
```bash
# Find potential circular dependencies
npx madge --circular src/

# Check for deep relative imports
grep -r "from '\.\./\.\./\.\." --include="*.ts" src/

# Find default exports (should use named exports for consistency)
grep -r "export default" --include="*.ts" src/
```

### 5.4 Error Handling Pattern Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Exception types | High | Mixed custom and generic exceptions |
| Error messages | High | Inconsistent error message format |
| Error codes | Medium | No standardized error codes |
| Try-catch patterns | High | Inconsistent error handling approaches |
| Logging on errors | Medium | Some errors logged, others not |

**Expected Error Pattern:**
```typescript
// Consistent custom exception hierarchy
// src/common/exceptions/
export class BaseException extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 500,
  ) {
    super(message);
  }
}

export class NotFoundException extends BaseException {
  constructor(resource: string, identifier: string) {
    super('NOT_FOUND', `${resource} with id '${identifier}' not found`, 404);
  }
}

export class ValidationException extends BaseException {
  constructor(message: string, public readonly errors: ValidationError[]) {
    super('VALIDATION_ERROR', message, 400);
  }
}

// Consistent usage across services
throw new NotFoundException('User', userId);
throw new ValidationException('Invalid input', errors);
```

**Anti-patterns to Flag:**
```typescript
// ❌ Inconsistent exception throwing
// Service A:
throw new Error('User not found');

// Service B:
throw new NotFoundException('User not found');

// Service C:
throw new HttpException('User not found', 404);

// ❌ Inconsistent error message formats
throw new Error('user not found');           // lowercase
throw new Error('User Not Found');           // Title Case
throw new Error('USER_NOT_FOUND');           // SCREAMING
throw new Error('User with ID 123 not found'); // with ID
throw new Error('Cannot find user');         // different phrasing
```

**Audit Commands:**
```bash
# Find all throw statements to check consistency
grep -r "throw new" --include="*.ts" src/ | head -30

# Check for generic Error usage (should use custom exceptions)
grep -r "throw new Error(" --include="*.ts" src/

# Find HttpException usage (check for consistency)
grep -r "HttpException\|NotFoundException\|BadRequestException" --include="*.ts" src/
```

### 5.5 Type Definition Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Type location | High | Types scattered vs centralized |
| Interface vs Type | Medium | Inconsistent use of interface vs type |
| Optional properties | Medium | Inconsistent use of ? vs undefined |
| Null handling | High | Mixed null and undefined usage |
| DTO validation | High | Some DTOs validated, others not |

**Expected Type Organization:**
```typescript
// Shared types in types/ or common/
// src/common/types/
export interface PaginationParams {
  page: number;
  limit: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  totalPages: number;
}

// Module-specific types colocated
// src/modules/user/types/
export interface UserFilters {
  status?: UserStatus;
  role?: UserRole;
}

// Consistent DTO pattern
export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsEmail()
  email: string;

  @IsOptional()
  @IsString()
  bio?: string;
}
```

**Anti-patterns to Flag:**
```typescript
// ❌ Inconsistent interface vs type usage
interface User { ... }    // Some use interface
type Product = { ... }    // Others use type alias

// ❌ Inconsistent optional handling
interface Config {
  apiKey?: string;        // Optional with ?
  timeout: number | undefined;  // Optional with | undefined
  retries: number | null;       // Nullable (different meaning!)
}

// ❌ DTOs without validation in some modules
// user.dto.ts - has validation decorators
// product.dto.ts - no validation decorators
```

**Audit Commands:**
```bash
# Check for interface vs type consistency
grep -r "^interface\|^export interface" --include="*.ts" src/ | wc -l
grep -r "^type\|^export type" --include="*.ts" src/ | wc -l

# Find DTOs without class-validator decorators
find src -name "*.dto.ts" -exec grep -L "@Is\|@Min\|@Max\|@Valid" {} \;

# Check for mixed null/undefined
grep -r "| null\|| undefined" --include="*.ts" src/ | head -20
```

### 5.6 Service Pattern Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Method naming | High | Inconsistent CRUD method names |
| Return types | High | Some return entities, others DTOs |
| Transaction handling | High | Inconsistent transaction patterns |
| Dependency injection | Medium | Some deps injected, others instantiated |
| Method signatures | Medium | Inconsistent parameter ordering |

**Expected Service Pattern:**
```typescript
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    private readonly eventEmitter: EventEmitter,  // Injected, not instantiated
  ) {}

  // Consistent CRUD naming
  async create(dto: CreateUserDto): Promise<User> { ... }
  async findAll(filters: UserFilters): Promise<User[]> { ... }
  async findOne(id: string): Promise<User> { ... }
  async findOneOrFail(id: string): Promise<User> { ... }  // Throws if not found
  async update(id: string, dto: UpdateUserDto): Promise<User> { ... }
  async remove(id: string): Promise<void> { ... }

  // Consistent parameter order: identifier first, then data
  async updateStatus(id: string, status: UserStatus): Promise<User> { ... }
}
```

**Anti-patterns to Flag:**
```typescript
// ❌ Inconsistent CRUD naming across services
// UserService:
async create() {}
async getAll() {}
async getById() {}

// ProductService:
async createProduct() {}
async findAll() {}
async findOne() {}

// OrderService:
async add() {}
async list() {}
async fetch() {}

// ❌ Inconsistent return types
async findUser(id): Promise<User> {}      // Returns entity
async findProduct(id): Promise<ProductDto> {}  // Returns DTO

// ❌ Instantiating dependencies instead of injection
class UserService {
  private logger = new Logger();  // ❌ Should be injected
}
```

**Audit Commands:**
```bash
# Compare method names across services
grep -r "async create\|async find\|async get\|async update\|async delete\|async remove" --include="*.service.ts" src/

# Check for new keyword in services (potential DI violation)
grep -r "new.*(" --include="*.service.ts" src/ | grep -v "new Date\|new Error\|new Map\|new Set"
```

### 5.7 Test Pattern Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Test file location | Medium | Mixed colocated and centralized tests |
| Test naming | Medium | Inconsistent describe/it descriptions |
| Mock patterns | High | Different mocking approaches per module |
| Setup/teardown | Medium | Inconsistent beforeEach/afterEach usage |
| Coverage gaps | High | Some modules tested, others not |

**Expected Test Pattern:**
```typescript
// Consistent test file naming: *.spec.ts (unit) or *.e2e-spec.ts (e2e)
// Colocated: user.service.spec.ts next to user.service.ts
// Or centralized: __tests__/user.service.spec.ts

describe('UserService', () => {
  let service: UserService;
  let repository: MockType<Repository<User>>;

  // Consistent setup
  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useFactory: repositoryMockFactory,
        },
      ],
    }).compile();

    service = module.get(UserService);
    repository = module.get(getRepositoryToken(User));
  });

  // Consistent describe structure
  describe('create', () => {
    it('should create a user with valid data', async () => { ... });
    it('should throw ValidationException for invalid email', async () => { ... });
  });

  describe('findOne', () => {
    it('should return user when found', async () => { ... });
    it('should throw NotFoundException when not found', async () => { ... });
  });
});
```

**Anti-patterns to Flag:**
```typescript
// ❌ Inconsistent test descriptions
it('creates user')           // No "should"
it('should create a user')   // With "should"
it('user creation works')    // Different style

// ❌ Inconsistent mocking
// Test A: Uses jest.mock()
// Test B: Uses manual mock objects
// Test C: Uses @nestjs/testing mock factories

// ❌ Missing tests for some modules
// user.service.spec.ts ✓
// product.service.spec.ts ✓
// order.service.spec.ts ✗ (missing!)
```

**Audit Commands:**
```bash
# Find modules missing tests
for service in $(find src -name "*.service.ts" | grep -v spec); do
  spec="${service%.ts}.spec.ts"
  [ ! -f "$spec" ] && echo "Missing: $spec"
done

# Check test description consistency
grep -r "it('" --include="*.spec.ts" src/ | head -20
```

### 5.8 Documentation & Comments Consistency

| Check | Severity | What to Look For |
|-------|----------|------------------|
| JSDoc on public APIs | Medium | Some services documented, others not |
| README per module | Low | Inconsistent module documentation |
| Inline comments | Low | Over-commented or under-commented |
| TODO/FIXME tracking | Medium | Stale TODOs, no tracking system |

**Expected Documentation Pattern:**
```typescript
/**
 * Service for managing user accounts and authentication.
 *
 * @remarks
 * All methods require the caller to have appropriate permissions.
 * User data is automatically scoped to the current tenant.
 */
@Injectable()
export class UserService {
  /**
   * Creates a new user account.
   *
   * @param dto - The user creation data
   * @returns The created user entity
   * @throws {ValidationException} When email is already taken
   * @throws {ForbiddenException} When caller lacks permission
   */
  async create(dto: CreateUserDto): Promise<User> { ... }
}
```

**Anti-patterns to Flag:**
```typescript
// ❌ Obvious comments that don't add value
// Increment the counter
counter++;

// ❌ Outdated comments
// TODO: Implement validation (but validation exists)
// Returns user by ID (but method returns Promise<User[]>)

// ❌ Stale TODOs with no tracking
// TODO: Fix this later
// FIXME: Temporary hack
// HACK: Need to refactor
```

**Audit Commands:**
```bash
# Find TODOs and FIXMEs
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" src/

# Check JSDoc coverage on services
grep -l "@Injectable" src/**/*.service.ts | while read f; do
  grep -q "/\*\*" "$f" && echo "✓ $f" || echo "✗ $f"
done
```

### 5.9 Code Duplication & DRY Violations

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Duplicate logic | High | Same code copy-pasted across modules |
| Similar DTOs | Medium | Nearly identical DTOs not shared |
| Repeated queries | Medium | Same database queries in multiple places |
| Utility sprawl | Medium | Similar helper functions scattered |

**Common Duplication Patterns:**
```typescript
// ❌ Pagination logic repeated
// user.service.ts
const skip = (page - 1) * limit;
const [items, total] = await this.repo.findAndCount({ skip, take: limit });
return { items, total, page, totalPages: Math.ceil(total / limit) };

// product.service.ts - same code!
const skip = (page - 1) * limit;
const [items, total] = await this.repo.findAndCount({ skip, take: limit });
return { items, total, page, totalPages: Math.ceil(total / limit) };

// ✅ Extract to shared utility
// common/utils/pagination.ts
export function paginate<T>(items: T[], total: number, page: number, limit: number) {
  return { items, total, page, totalPages: Math.ceil(total / limit) };
}
```

**Audit Commands:**
```bash
# Find similar code blocks (using jscpd)
npx jscpd src/ --min-lines 5 --min-tokens 50

# Find duplicate string patterns
grep -roh "throw new.*Exception" --include="*.ts" src/ | sort | uniq -c | sort -rn

# Find similar method signatures
grep -r "async find.*(" --include="*.service.ts" src/
```

### 5.10 Developer Experience Checklist

**Module Structure:**
- [ ] All modules follow identical directory structure
- [ ] Barrel exports (index.ts) in every module
- [ ] Related files colocated (entity + DTOs + tests)
- [ ] Consistent module naming (singular vs plural)

**Naming Conventions:**
- [ ] File naming follows single convention (kebab-case recommended)
- [ ] Class suffixes consistent (Service, Controller, Resolver, etc.)
- [ ] Database naming follows convention (snake_case recommended)
- [ ] No mixed camelCase/snake_case in same layer

**Code Patterns:**
- [ ] CRUD methods named consistently across all services
- [ ] Error handling uses same exception hierarchy
- [ ] All DTOs have validation decorators
- [ ] Transaction patterns consistent

**Imports & Exports:**
- [ ] Import order consistent (externals → internals → relatives)
- [ ] No circular dependencies
- [ ] No deep relative imports (use aliases or barrels)
- [ ] Consistent use of named exports

**Testing:**
- [ ] Every service has corresponding spec file
- [ ] Test descriptions follow consistent pattern
- [ ] Mock setup standardized across tests
- [ ] No test files with skipped tests (.skip)

**Documentation:**
- [ ] Public APIs have JSDoc comments
- [ ] No stale TODO/FIXME comments
- [ ] Module-level README if complex

**Code Reuse:**
- [ ] No copy-pasted logic between modules
- [ ] Common utilities extracted to shared location
- [ ] Similar DTOs consolidated or inherited

---

## 6. Error Handling Audit

### 6.1 Error Boundaries

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Global error boundary | High | Missing `app/error.tsx` |
| Not found handling | Medium | Missing `app/not-found.tsx` |
| Segment error boundaries | Low | Missing error.tsx in route segments |

**Required Files:**
```
src/app/error.tsx        # Global error boundary
src/app/not-found.tsx    # 404 page
src/app/global-error.tsx # Root layout errors
```

**Example error.tsx:**
```tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### 6.2 API Error Handling

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Try-catch blocks | High | Unhandled promise rejections |
| Error responses | Medium | Inconsistent error response format |
| Logging | Medium | Errors not logged |
| User feedback | Medium | Silent failures |

**Files to Check:**
```
src/app/api/**/route.ts
src/lib/content/
src/lib/queries/
```

**Checklist:**
- [ ] All async operations wrapped in try-catch
- [ ] Consistent error response format
- [ ] Errors logged with context
- [ ] User-friendly error messages displayed
- [ ] Retry logic for transient failures

### 6.3 Form Validation

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Client-side validation | Medium | Forms submit without validation |
| Server-side validation | High | API accepts invalid data |
| Error display | Medium | Validation errors not shown to user |

**Checklist:**
- [ ] Required fields validated
- [ ] Email/phone formats validated
- [ ] Server validates all input (never trust client)
- [ ] Clear error messages displayed
- [ ] Form state preserved on error

---

## 7. Accessibility Audit

### 7.1 Semantic HTML

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Heading hierarchy | High | Skipped heading levels (h1 → h3) |
| Landmark regions | Medium | Missing main, nav, footer elements |
| Button vs link | Medium | `<div onClick>` instead of button/link |
| Lists | Low | Items not in ul/ol |

**Audit Commands:**
```bash
# Check for div with onClick (should be button)
grep -r "div.*onClick\|span.*onClick" --include="*.tsx" src/

# Check heading usage
grep -r "<h[1-6]" --include="*.tsx" src/
```

### 7.2 ARIA & Labels

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Image alt text | High | Images without alt attribute |
| Form labels | High | Inputs without associated labels |
| ARIA labels | Medium | Interactive elements without accessible names |
| Focus management | Medium | Focus not managed in modals/dialogs |

**Audit Commands:**
```bash
# Check for images without alt
grep -r "<Image\|<img" --include="*.tsx" src/ | grep -v "alt="

# Check for inputs without labels
grep -r "<input\|<Input" --include="*.tsx" src/
```

### 7.3 Keyboard Navigation

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Tab order | High | Illogical tab order |
| Focus visible | High | Focus indicator removed |
| Keyboard traps | High | Can't escape modal with keyboard |
| Skip links | Medium | No skip to main content link |

**Checklist:**
- [ ] All interactive elements focusable
- [ ] Visible focus indicators
- [ ] Logical tab order
- [ ] Escape closes modals
- [ ] Skip link for main content

### 7.4 Color & Contrast

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Color contrast | High | Text contrast ratio < 4.5:1 |
| Color-only info | Medium | Information conveyed only by color |
| Focus contrast | Medium | Focus indicator not visible |

**Tools:**
- Chrome DevTools Accessibility panel
- axe DevTools extension
- Lighthouse accessibility audit

---

## 8. SEO Audit

### 8.1 Meta Tags

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Title tags | High | Missing or duplicate titles |
| Meta descriptions | Medium | Missing or too long (> 160 chars) |
| Open Graph | Medium | Missing OG tags for social sharing |
| Canonical URLs | Medium | Missing canonical for duplicate content |

**Files to Check:**
```
src/app/layout.tsx
src/app/**/page.tsx
src/app/**/layout.tsx
```

**Required Metadata:**
```tsx
// src/app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'Site Name',
    template: '%s | Site Name',
  },
  description: 'Site description',
  openGraph: {
    title: 'Site Name',
    description: 'Site description',
    url: 'https://example.com',
    siteName: 'Site Name',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
  },
};
```

### 8.2 Structured Data

| Check | Severity | What to Look For |
|-------|----------|------------------|
| JSON-LD | Medium | Missing structured data |
| Schema validity | Medium | Invalid schema markup |
| Relevant schemas | Low | Missing business-specific schemas |

**Common Schemas:**
- Organization
- LocalBusiness
- BreadcrumbList
- Article
- Product
- FAQ

### 8.3 Technical SEO

| Check | Severity | What to Look For |
|-------|----------|------------------|
| robots.txt | Medium | Missing or misconfigured |
| sitemap.xml | Medium | Missing sitemap |
| Mobile-friendly | High | Not responsive |
| Page speed | High | Slow loading |

**Required Files:**
```
public/robots.txt
app/sitemap.ts (or sitemap.xml)
```

---

## 9. Environment & Configuration Audit

### 9.1 Environment Files

| Check | Severity | What to Look For |
|-------|----------|------------------|
| .env.example | Medium | No example env file for onboarding |
| Env validation | Medium | No schema validation for env vars |
| Production values | High | Dev values in production config |

**Required Files:**
```
.env.example          # Template with placeholder values
.env.local           # Local development (gitignored)
.env.production      # Production overrides (if needed)
```

**Env Validation Example (using zod):**
```typescript
// src/lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_CMS_GRAPHQL_URL: z.string().url(),
  CMS_ORGANIZATION_ID: z.string().uuid(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

export const env = envSchema.parse(process.env);
```

### 9.2 Next.js Configuration

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Image domains | High | Remote images not configured |
| Redirects | Medium | Old URLs not redirecting |
| Headers | Medium | Security headers not set |
| Rewrites | Low | API proxying if needed |

**Files to Check:**
```
next.config.js
next.config.mjs
```

---

## 10. Dependencies Audit

### 10.1 Security Vulnerabilities

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Known vulnerabilities | Critical | `npm audit` findings |
| Outdated packages | Medium | Major versions behind |
| Deprecated packages | Medium | Using deprecated libraries |

**Audit Commands:**
```bash
# Check for vulnerabilities
npm audit

# Check for outdated packages
npm outdated

# Update to latest (be careful)
npm update
```

### 10.2 Dependency Hygiene

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Unused dependencies | Low | Packages in package.json not imported |
| Dev vs prod deps | Low | Dev dependencies in production |
| Lock file | Medium | Missing or outdated package-lock.json |

**Audit Commands:**
```bash
# Find unused dependencies
npx depcheck

# Verify lock file is in sync
npm ci
```

### 10.3 License Compliance

| Check | Severity | What to Look For |
|-------|----------|------------------|
| License compatibility | Medium | GPL dependencies in proprietary project |
| License documentation | Low | No license documentation |

**Audit Commands:**
```bash
# Check licenses
npx license-checker --summary
```

---

## 11. Build & Deployment Audit

### 11.1 Build Process

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Build succeeds | Critical | `npm run build` fails |
| No build warnings | Medium | TypeScript/ESLint warnings in build |
| Build time | Low | Excessively long builds |

**Audit Commands:**
```bash
# Run production build
npm run build

# Check build output
ls -la .next/
```

### 11.2 Deployment Configuration

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Vercel config | Medium | Missing vercel.json optimizations |
| Environment vars | Critical | Production env vars not set |
| Domain config | High | Custom domain not configured |
| SSL | Critical | HTTPS not enforced |

**Files to Check:**
```
vercel.json
.vercelignore
```

### 11.3 CI/CD Pipeline

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Automated tests | Medium | No tests run on PR |
| Lint checks | Medium | No linting in CI |
| Preview deployments | Low | No preview for PRs |
| Rollback plan | Medium | No rollback strategy |

---

## 12. Monitoring & Observability Audit

### 12.1 Error Tracking

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Error service | High | No Sentry/similar configured |
| Source maps | Medium | Errors not deobfuscated |
| Alert rules | Medium | No alerts for errors |

**Integration Check:**
```bash
# Check for Sentry
grep -r "sentry" package.json
grep -r "@sentry" src/
```

### 12.2 Analytics

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Analytics configured | Medium | No analytics tracking |
| Privacy compliance | High | No cookie consent |
| Performance monitoring | Medium | No RUM (Real User Monitoring) |

### 12.3 Logging

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Structured logging | Medium | No consistent log format |
| Log levels | Low | Everything at same level |
| PII in logs | High | Sensitive data logged |

---

## Audit Report Template

After completing the audit, generate a report using this template:

```markdown
# Production Readiness Audit Report

**Project:** [PROJECT_NAME]
**Date:** [DATE]
**Auditor:** Claude Code

## Summary

| Category | Critical | High | Medium | Low | Pass |
|----------|----------|------|--------|-----|------|
| Architecture | X | X | X | X | ✓/✗ |
| Security | X | X | X | X | ✓/✗ |
| Performance | X | X | X | X | ✓/✗ |
| Code Quality | X | X | X | X | ✓/✗ |
| **DX & Consistency** | X | X | X | X | ✓/✗ |
| Error Handling | X | X | X | X | ✓/✗ |
| Accessibility | X | X | X | X | ✓/✗ |
| SEO | X | X | X | X | ✓/✗ |
| Configuration | X | X | X | X | ✓/✗ |
| Dependencies | X | X | X | X | ✓/✗ |
| Build/Deploy | X | X | X | X | ✓/✗ |
| Monitoring | X | X | X | X | ✓/✗ |

**Overall Status:** [READY / NOT READY / CONDITIONAL]

## Critical Issues (Must Fix)

1. [Issue description]
   - **Location:** [file:line]
   - **Fix:** [recommended fix]

## High Priority Issues

1. [Issue description]
   - **Location:** [file:line]
   - **Fix:** [recommended fix]

## Medium Priority Issues

[List issues]

## Low Priority Issues

[List issues]

## Recommendations

[Additional recommendations for improvement]
```

---

## Quick Audit Checklist

For a rapid assessment, verify these critical items:

### Must Have (Critical)
- [ ] No secrets in code
- [ ] `.env*` files gitignored
- [ ] `npm run build` succeeds
- [ ] `npm audit` shows no critical vulnerabilities
- [ ] Error boundaries in place
- [ ] HTTPS enforced
- [ ] Production env vars configured

### Should Have (High)
- [ ] Security headers configured
- [ ] TypeScript strict mode
- [ ] All images use Next.js Image
- [ ] Core Web Vitals passing
- [ ] Form validation (client + server)
- [ ] Alt text on images
- [ ] Meta tags configured
- [ ] Error tracking configured

### Nice to Have (Medium/Low)
- [ ] Structured data
- [ ] Sitemap
- [ ] Analytics
- [ ] Pre-commit hooks
- [ ] CI/CD pipeline
- [ ] Documentation

---

## Version History

**v1.2** (January 2026)
- Added Developer Experience & Code Consistency Audit (Section 5)
- Covers module structure, naming conventions, import/export patterns, error handling consistency, type definitions, service patterns, test patterns, documentation, and code duplication
- Marked as "Early-stage priority" for new projects
- 12 audit categories total

**v1.1** (January 2026)
- Added comprehensive Software Architecture Audit (Section 1)
- 11 audit categories total

**v1.0** (January 2026)
- Initial production audit skill
- 10 audit categories
- Report template

---

*End of Production Readiness Audit Skill*
