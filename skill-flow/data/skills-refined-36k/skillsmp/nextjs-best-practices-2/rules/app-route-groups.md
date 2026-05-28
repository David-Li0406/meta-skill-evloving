---
title: Use Route Groups for Organization
impact: CRITICAL
impactDescription: Organize routes without affecting URL structure
tags: routing, organization, layouts, architecture
---

## Use Route Groups for Organization

Route groups (folders with parentheses) organize files and share layouts without affecting the URL path. Essential for clean architecture.

**Incorrect (layout duplication or messy URLs):**

```
app/
├── marketing-home/page.tsx      # URL: /marketing-home ❌
├── marketing-about/page.tsx     # URL: /marketing-about ❌
├── dashboard/page.tsx
├── dashboard/settings/page.tsx
└── layout.tsx                   # Same layout for everything ❌
```

**Correct (route groups for organization):**

```
app/
├── (marketing)/                 # Group - not in URL
│   ├── layout.tsx               # Marketing layout (navbar, footer)
│   ├── page.tsx                 # URL: /
│   ├── about/page.tsx           # URL: /about
│   └── pricing/page.tsx         # URL: /pricing
│
├── (dashboard)/                 # Group - not in URL
│   ├── layout.tsx               # Dashboard layout (sidebar)
│   ├── dashboard/page.tsx       # URL: /dashboard
│   └── settings/page.tsx        # URL: /settings
│
├── (auth)/                      # Group - not in URL
│   ├── layout.tsx               # Minimal auth layout
│   ├── login/page.tsx           # URL: /login
│   └── register/page.tsx        # URL: /register
│
└── layout.tsx                   # Root layout (html, body)
```

**Multiple layouts for same route:**

```typescript
// app/(shop)/products/page.tsx - Uses shop layout
// app/(admin)/products/page.tsx - Uses admin layout (different /products!)

// Be careful: same URL path can't exist in multiple groups
```

**Opting out of layouts:**

```typescript
// app/(with-sidebar)/dashboard/page.tsx - Has sidebar
// app/(no-sidebar)/dashboard/print/page.tsx - No sidebar for print view
```

**Parallel routes with groups:**

```
app/
├── @modal/                      # Parallel route slot
│   └── (.)photo/[id]/page.tsx   # Intercepted route
├── (gallery)/
│   ├── layout.tsx
│   └── page.tsx
└── layout.tsx
```

Route groups are purely organizational - they don't create URL segments.

Reference: [Route Groups](https://nextjs.org/docs/app/building-your-application/routing/route-groups)
