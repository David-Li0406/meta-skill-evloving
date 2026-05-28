---
name: Frontend Architecture (Next.js)
description: Next.js 14 App Router, client/server components, middleware routing, and state management.
---

# Frontend Architecture (Next.js)

## Context

- **Framework**: Next.js 14 (App Router)
- **Location**: `apps/web/`
- **Port**: 3000 (dev), 3000 (prod)
- **Styling**: Tailwind CSS + Framer Motion

---

## Directory Structure

```
apps/web/
├── app/
│   ├── (marketing)/       # Public pages (landing, about)
│   ├── (platform)/        # Authenticated area
│   │   ├── dashboard/
│   │   ├── wall/
│   │   └── profile/
│   ├── api/               # API routes (minimal)
│   ├── layout.tsx         # Root layout with providers
│   └── middleware.ts      # Subdomain routing
├── components/
│   ├── ui/                # Dumb, reusable (Button, Input)
│   ├── features/          # Smart, domain-specific
│   └── layout/            # Navbar, Footer, Sidebar
├── lib/
│   ├── api.ts             # Axios instance
│   ├── brand.config.ts    # Dual-brand configuration
│   └── utils.ts           # Helpers
├── hooks/                 # Custom React hooks
└── public/                # Static assets
```

---

## Core Principles

1. **Server Components by Default**: Only use `'use client'` when needed.
2. **Middleware Routing**: Subdomains handled in `middleware.ts`.
3. **Colocation**: Keep related files together (component + styles + hooks).

---

## Client vs Server Components

### Server Component (default)

```tsx
// app/(platform)/dashboard/page.tsx
export default async function DashboardPage() {
  const user = await getCurrentUser(); // Direct DB/API call
  return <DashboardClient user={user} />;
}
```

### Client Component

```tsx
// components/features/MissionCard.tsx
'use client';

import { useState } from 'react';

export function MissionCard({ mission }) {
  const [isExpanded, setIsExpanded] = useState(false);
  // Event handlers, hooks, interactivity
}
```

---

## Middleware Routing

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  
  if (hostname.includes('sociopulse')) {
    // SocioPulse theme
    request.headers.set('x-brand', 'sociopulse');
  } else if (hostname.includes('medicopulse')) {
    // MedicoPulse theme
    request.headers.set('x-brand', 'medicopulse');
  }
  
  return NextResponse.next();
}
```

---

## API Client

```typescript
// lib/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

// Interceptor for auth token
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

---

## Forms with Zod + React Hook Form

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { missionSchema } from '@/lib/schemas';

export function CreateMissionForm() {
  const form = useForm({
    resolver: zodResolver(missionSchema),
    defaultValues: { title: '', type: 'TEMPORARY' },
  });

  const onSubmit = async (data) => {
    await api.post('/missions', data);
  };

  return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>;
}
```

---

## Layouts

### Root Layout

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>
          <BrandProvider>
            {children}
          </BrandProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
```

### Platform Layout

```tsx
// app/(platform)/layout.tsx
export default function PlatformLayout({ children }) {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>{children}</main>
      <Footer />
    </div>
  );
}
```

---

## Do's and Don'ts

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use `zod` for validation | Put heavy logic in `page.tsx` |
| Fetch data in Server Components | Expose secrets in Client Components |
| Use `@packages/ui` components | Create duplicate UI components |
| Implement loading states | Ignore error boundaries |
