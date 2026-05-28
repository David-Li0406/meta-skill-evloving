<preload_query_pattern>
Use `preloadQuery` + `usePreloadedQuery` for server-rendered pages with real-time reactivity.

<server_component>
```tsx
// page.tsx (Server Component)
import { preloadQuery } from "convex/nextjs";
import { api } from "@/convex/_generated/api";
import { Dashboard } from "./Dashboard";

export default async function DashboardPage() {
  const preloadedData = await preloadQuery(api.dashboard.getData);
  return <Dashboard preloadedData={preloadedData} />;
}
```
</server_component>

<client_component>
```tsx
// Dashboard.tsx (Client Component)
"use client";
import { usePreloadedQuery } from "convex/react";
import { Preloaded } from "convex/react";
import { api } from "@/convex/_generated/api";

export function Dashboard({
  preloadedData
}: {
  preloadedData: Preloaded<typeof api.dashboard.getData>
}) {
  const data = usePreloadedQuery(preloadedData);
  // data is now reactive - updates in real-time!
  return <div>{data.name}</div>;
}
```
</client_component>

<benefits>
- No loading spinner on initial page load
- Page is fully rendered server-side
- Real-time updates after hydration
</benefits>
</preload_query_pattern>

<auth_routing>
Use `proxy.ts` (NOT middleware.ts) for authentication routing with Convex Auth. Do NOT use `<AuthGuard>` components.

```typescript
// proxy.ts
import {
  convexAuthNextjsMiddleware,
  createRouteMatcher,
  nextjsMiddlewareRedirect,
} from "@convex-dev/auth/nextjs";

const isPublicRoute = createRouteMatcher(["/", "/login", "/signup"]);

export default convexAuthNextjsMiddleware(async (request, { convexAuth }) => {
  const isAuthenticated = await convexAuth.isAuthenticated();

  if (!isPublicRoute(request) && !isAuthenticated) {
    return nextjsMiddlewareRedirect(request, "/login");
  }

  if (isPublicRoute(request) && isAuthenticated && request.nextUrl.pathname !== "/") {
    return nextjsMiddlewareRedirect(request, "/dashboard");
  }
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

<critical>
File MUST be named `proxy.ts`, not `middleware.ts` - this is the required pattern for Convex Auth.
</critical>
</auth_routing>

<auth_provider_setup>
Set up ConvexAuthNextjsProvider in your layout:

<server_layout>
```tsx
// app/layout.tsx
import { ConvexAuthNextjsServerProvider } from "@convex-dev/auth/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ConvexAuthNextjsServerProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ConvexAuthNextjsServerProvider>
  );
}
```
</server_layout>

<client_provider>
```tsx
// app/ConvexClientProvider.tsx
"use client";
import { ConvexAuthNextjsProvider } from "@convex-dev/auth/nextjs";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: React.ReactNode }) {
  return (
    <ConvexAuthNextjsProvider client={convex}>
      {children}
    </ConvexAuthNextjsProvider>
  );
}
```
</client_provider>
</auth_provider_setup>
