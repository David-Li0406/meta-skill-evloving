---
name: Frontend Architecture Expert
description: Expert knowledge of Next.js 14 App Router, dual-brand implementation, dashboard variants, and state management patterns.
---

# Frontend Architecture Skill - SocioPulse V2

## Overview

The frontend is built with **Next.js 14 (App Router)** and implements a sophisticated dual-brand system with polymorphic UI components.

---

## 1. Route Groups Architecture

### Structure

```
app/
├── (auth)/          # Login, register pages (no nav/footer)
│   ├── login/
│   └── register/
├── (platform)/      # Main app (requires authentication)
│   ├── dashboard/   # Dashboards (4 variants)
│   ├── wall/        # Fil Pro feed
│   ├── sos/         # SOS Renfort missions
│   └── catalogue/   # Services marketplace
└── (admin)/         # Admin panel (ADMIN role only)
    └── users/
```

### Route Group Purpose

- **(auth)**: No navigation, centered layout, public access
- **(platform)**: Full navigation, requires auth, role-based access
- **(admin)**: Admin-specific layout, requires ADMIN role

---

## 2. Middleware (`middleware.ts`)

### Responsibilities

1. **JWT Authentication**: Verify token from cookies
2. **Role-Based Routing**: Redirect based on UserRole
3. **Subdomain Handling**: `dash.sociopulse.com` → `/admin`
4. **Security Headers**: Inject CSP, X-Frame-Options

### Flow

```typescript
// Simplified logic
export async function middleware(request) {
  const token = request.cookies.get('accessToken');
  
  if (!token && isProtectedPath(pathname)) {
    return redirect('/auth/login');
  }
  
  const { role } = await verifyJWT(token);
  
  // Redirect to appropriate dashboard
  if (pathname === '/dashboard') {
    if (role === 'CLIENT') return redirect('/dashboard/client');
    if (role === 'TALENT') return redirect('/dashboard/talent');
    if (role === 'ADMIN') return redirect('/admin');
  }
}
```

---

## 3. Dual-Brand Implementation

### Brand Detection

```typescript
// lib/brand.ts
const APP_MODE = process.env.NEXT_PUBLIC_APP_MODE as 'SOCIAL' | 'MEDICAL';
export const currentBrand = APP_MODE === 'MEDICAL' ? MEDICAL_CONFIG : SOCIAL_CONFIG;

// Usage in components
import { currentBrand, isMedical } from '@/lib/brand';

<h1>{currentBrand.heroTitle}</h1>
{isMedical() && <CriticalUrgencyBadge />}
```

### HTML Attribute (for CSS)

```tsx
// app/layout.tsx
<html data-brand={currentBrand.mode}>
  {/* CSS variables automatically switch */}
</html>
```

---

## 4. Dashboard Variants

### 4 Dashboard Types

**Client Dashboards:**

1. **shift-planner** (Medical): Calendar-dense view for managing shifts
2. **project-hub** (Social): Card grid for supervising projects

**Talent Dashboards:**
3. **job-ticker** (Medical): Fast list of urgent vacations
4. **portfolio-feed** (Social): Skills showcase + mission feed

### Dynamic Resolution

```tsx
// components/dashboard/DashboardResolver.tsx
import { getDashboardLayout } from '@/lib/domain-config';

export function DashboardResolver({ role }: { role: 'CLIENT' | 'TALENT' }) {
  const layout = getDashboardLayout(role === 'CLIENT' ? 'client' : 'talent');
  
  switch (layout) {
    case 'shift-planner':
      return <ShiftPlannerDashboard />;
    case 'project-hub':
      return <ProjectHubDashboard />;
    case 'job-ticker':
      return <JobTickerDashboard />;
    case 'portfolio-feed':
      return <PortfolioFeedDashboard />;
  }
}
```

---

## 5. State Management

### Server Components (Default)

```tsx
// app/(platform)/sos/page.tsx
export default async function SOSPage() {
  const missions = await fetchMissions(); // Direct API call
  return <MissionList missions={missions} />;
}
```

### Server Actions (Mutations)

```typescript
// app/actions/missions.ts
'use server';

export async function createMission(data: FormData) {
  const response = await fetch(`${API_URL}/relief-missions`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
  revalidatePath('/sos');
  return response.json();
}

// Usage in client component
import { createMission } from '@/app/actions/missions';

<form action={createMission}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

### Client State (Custom Hooks)

```typescript
// lib/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    fetch(`${API_URL}/auth/me`, { credentials: 'include' })
      .then(res => res.json())
      .then(setUser)
      .finally(() => setIsLoading(false));
  }, []);
  
  return { user, isLoading, isAuthenticated: !!user };
}
```

---

## 6. Polymorphic Components

### Terminology-Aware Components

```tsx
// components/mission/MissionCard.tsx
import { getTerm } from '@/lib/domain-config';

export function MissionCard({ mission }) {
  return (
    <div>
      <h3>{getTerm('mission')}</h3>  {/* "Mission" or "Vacation" */}
      <p>{getTerm('urgentAction')}</p> {/* "Mission SOS" or "Vacation urgente" */}
    </div>
  );
}
```

### Feature-Gated Components

```tsx
import { isFeatureEnabled } from '@/lib/domain-config';

{isFeatureEnabled('enableWorkshops') && (
  <CatalogueSection />
)}

{isFeatureEnabled('enableCriticalUrgency') && (
  <UrgencyLevel level="CRITICAL" />
)}
```

---

## 7. Real-Time Updates

### Socket.IO Client

```typescript
// lib/useSocket.ts
import { io } from 'socket.io-client';

export function useSocket() {
  const socket = useMemo(() => 
    io(API_URL, { withCredentials: true }), 
    []
  );
  
  useEffect(() => {
    socket.on('mission:new', (mission) => {
      toast.info('Nouvelle mission disponible!');
    });
    
    return () => socket.disconnect();
  }, [socket]);
  
  return socket;
}
```

### Custom Events (Optimistic UI)

```typescript
// components/create/CreateActionModal.tsx
window.dispatchEvent(
  new CustomEvent('sociopulse:wall:feed-item', {
    detail: { status: 'optimistic', item: optimisticItem }
  })
);

// components/wall/useWallFeed.ts
useEffect(() => {
  const handler = (e: CustomEvent) => {
    if (e.detail.status === 'optimistic') {
      setItems(prev => [e.detail.item, ...prev]);
    }
  };
  window.addEventListener('sociopulse:wall:feed-item', handler);
  return () => window.removeEventListener('sociopulse:wall:feed-item', handler);
}, []);
```

---

## 8. SEO & Metadata

### Dynamic Metadata

```tsx
// app/(platform)/sos/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'SOS Renfort | SocioPulse',
  description: 'Trouvez des intervenants sociaux en urgence',
};
```

### Schema.org Markup

```tsx
// components/mission/MissionCard.tsx
<script type="application/ld+json">
  {JSON.stringify({
    "@context": "https://schema.org",
    "@type": "JobPosting",
    "title": mission.title,
    "hiringOrganization": mission.client.name,
    "datePosted": mission.createdAt,
  })}
</script>
```

---

## 9. Performance Optimizations

### Code Splitting

```tsx
import dynamic from 'next/dynamic';

const HeavyModal = dynamic(() => import('./HeavyModal'), {
  loading: () => <Spinner />,
  ssr: false,
});
```

### Image Optimization

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // For above-the-fold images
/>
```

---

## 10. Best Practices

### DO

✅ Use Server Components by default  
✅ Use Server Actions for mutations  
✅ Leverage polymorphic helpers (`getTerm()`, `isFeatureEnabled()`)  
✅ Use `'use client'` only when needed (interactivity)  
✅ Implement optimistic UI for better UX

### DON'T

❌ Hardcode brand-specific logic (use helpers)  
❌ Over-use Client Components (hurts performance)  
❌ Forget to revalidate after mutations  
❌ Skip SEO metadata on public pages

---

*This frontend architecture enables dual-brand functionality with clean separation of concerns and optimal performance.*
