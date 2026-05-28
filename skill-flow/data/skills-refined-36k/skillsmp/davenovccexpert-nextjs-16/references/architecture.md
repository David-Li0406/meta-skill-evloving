<overview>
Next.js 16 project architecture with App Router, focusing on scalable structure for production applications.
</overview>

<project_structure>
<recommended_structure>
```
my-app/
├── src/
│   ├── app/                    # App Router directory
│   │   ├── (auth)/             # Route group - auth pages
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (marketing)/        # Route group - public pages
│   │   │   ├── about/
│   │   │   └── pricing/
│   │   ├── (dashboard)/        # Route group - protected pages
│   │   │   ├── layout.tsx      # Shared dashboard layout
│   │   │   ├── dashboard/
│   │   │   ├── settings/
│   │   │   └── profile/
│   │   ├── api/                # API routes
│   │   │   └── webhooks/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── loading.tsx         # Global loading state
│   │   ├── error.tsx           # Global error handler
│   │   ├── not-found.tsx       # 404 page
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # Reusable UI primitives
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── card.tsx
│   │   └── features/           # Feature-specific components
│   │       ├── auth/
│   │       └── dashboard/
│   ├── lib/
│   │   ├── dal.ts              # Data Access Layer
│   │   ├── actions/            # Server Actions
│   │   │   ├── auth.ts
│   │   │   └── products.ts
│   │   ├── db.ts               # Database client
│   │   └── utils.ts            # Utility functions
│   ├── hooks/                  # Custom React hooks
│   ├── types/                  # TypeScript types
│   └── styles/                 # Additional styles
├── public/                     # Static assets
├── proxy.ts                    # Proxy (replaces middleware)
├── next.config.ts
├── tsconfig.json
└── package.json
```
</recommended_structure>

<route_groups>
Route groups allow organizing routes without affecting URL structure.

**Syntax:** Wrap folder name in parentheses `(groupName)`

**Use cases:**
- Separate layouts for marketing vs app pages
- Group authenticated vs public routes
- Organize by feature without adding URL segments

```
app/
├── (marketing)/          # /about, /pricing (NOT /marketing/about)
│   ├── about/
│   └── pricing/
├── (dashboard)/          # /dashboard, /settings
│   ├── layout.tsx        # Shared layout for dashboard pages
│   ├── dashboard/
│   └── settings/
```
</route_groups>

<parallel_routes>
Render multiple pages in the same layout simultaneously.

**Syntax:** Prefix folder with `@` - `@slotName`

```
app/
├── @dashboard/
│   └── page.tsx
├── @sidebar/
│   └── page.tsx
└── layout.tsx            # Receives both as props
```

```tsx
// layout.tsx
export default function Layout({
  children,
  dashboard,
  sidebar,
}: {
  children: React.ReactNode
  dashboard: React.ReactNode
  sidebar: React.ReactNode
}) {
  return (
    <div className="flex">
      <aside>{sidebar}</aside>
      <main>
        {dashboard}
        {children}
      </main>
    </div>
  )
}
```
</parallel_routes>

<intercepting_routes>
Intercept navigation to show different content (e.g., modal).

**Syntax:**
- `(.)` - same level
- `(..)` - one level up
- `(..)(..)` - two levels up
- `(...)` - from root

**Example - Photo modal:**
```
app/
├── @modal/
│   └── (.)photos/[id]/   # Intercepts /photos/[id]
│       └── page.tsx      # Shows modal
├── photos/
│   └── [id]/
│       └── page.tsx      # Full page (direct navigation)
```
</intercepting_routes>
</project_structure>

<file_conventions>
<special_files>
| File | Purpose |
|------|---------|
| `page.tsx` | UI for a route segment |
| `layout.tsx` | Shared UI wrapper (persists across navigation) |
| `template.tsx` | Like layout but remounts on navigation |
| `loading.tsx` | Loading UI (wraps page in Suspense) |
| `error.tsx` | Error UI (wraps page in Error Boundary) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint |
| `proxy.ts` | Request proxy (formerly middleware) |
</special_files>

<dynamic_routes>
| Pattern | Example | Matches |
|---------|---------|---------|
| `[slug]` | `/blog/[slug]` | `/blog/hello` |
| `[...slug]` | `/blog/[...slug]` | `/blog/a/b/c` |
| `[[...slug]]` | `/blog/[[...slug]]` | `/blog` or `/blog/a/b` |
</dynamic_routes>
</file_conventions>

<colocation>
**Colocate related files within route folders:**

```
app/
└── dashboard/
    ├── page.tsx
    ├── loading.tsx
    ├── error.tsx
    ├── DashboardChart.tsx    # Component used only here
    ├── use-dashboard.ts      # Hook used only here
    └── dashboard.test.tsx    # Tests for this route
```

**Benefits:**
- Related code stays together
- Easy to understand scope
- Simplifies refactoring
</colocation>

<anti_patterns>
**Avoid:**

<anti_pattern name="flat-structure">
**Problem:** All pages at root level
```
app/
├── login.tsx
├── register.tsx
├── dashboard.tsx
├── settings.tsx
├── profile.tsx
```

**Better:** Group by feature/domain
```
app/
├── (auth)/
├── (dashboard)/
```
</anti_pattern>

<anti_pattern name="deep-nesting">
**Problem:** Excessive nesting
```
app/dashboard/settings/profile/edit/form/page.tsx
```

**Better:** Flatten where possible, use route groups for organization
</anti_pattern>

<anti_pattern name="components-in-app">
**Problem:** Mixing components with routes
```
app/
├── dashboard/
│   ├── page.tsx
│   └── Button.tsx    # Shared component shouldn't be here
```

**Better:** Put shared components in `src/components/`
</anti_pattern>
</anti_patterns>
