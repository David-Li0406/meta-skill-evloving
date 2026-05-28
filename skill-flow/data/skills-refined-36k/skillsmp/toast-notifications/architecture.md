# Toast System Architecture

## Overview

The toast notification system uses cookies to communicate from server to client. This is necessary because Server Actions often redirect, and redirect responses cannot carry additional data.

## Flow Diagram

```
┌─────────────────┐
│  Server Action  │
│                 │
│ setToastCookie()│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Set Cookie    │
│  "app-toast"    │
│ {type, message} │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    redirect()   │
│  or return      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Client Render  │
│  ToastHandler   │
│  useEffect      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Read Cookie    │
│  Display Toast  │
│  Remove Cookie  │
└─────────────────┘
```

## Components

### Server Side: toast.cookie.ts

```typescript
"use server";

import { cookies } from "next/headers";
import { TOAST_COOKIE_NAME } from "~/lib/toast/constants";
import type { ToastMessage, ToastType } from "~/lib/toast/types";

const cookieConfig = {
  maxAge: 5000,        // 5 seconds
  path: "/",           // Available on all routes
  httpOnly: false,     // Must be readable by client JS
  sameSite: "lax",     // Sent with same-site navigations
  secure: process.env.NODE_ENV === "production"
};

export async function setToastCookie(
  message: string,
  type: ToastType = "success",
  duration?: number
) {
  const cookieStore = await cookies();

  const toastData: ToastMessage = {
    type,
    message,
    duration
  };

  cookieStore.set(TOAST_COOKIE_NAME, JSON.stringify(toastData), cookieConfig);
}
```

### Client Side: toast-handler.tsx

```typescript
"use client";

import * as React from "react";
import Cookies from "js-cookie";
import { toast } from "@szum-tech/design-system";
import { usePathname } from "next/navigation";
import { TOAST_COOKIE_NAME } from "~/lib/toast/constants";
import type { ToastMessage } from "~/lib/toast/types";

export function ToastHandler() {
  const pathname = usePathname();

  React.useEffect(() => {
    const toastCookie = Cookies.get(TOAST_COOKIE_NAME);
    if (!toastCookie) return;

    try {
      const toastData = JSON.parse(toastCookie) as ToastMessage;

      switch (toastData.type) {
        case "success":
          toast.success(toastData.message, { duration: toastData.duration });
          break;
        case "error":
          toast.error(toastData.message, { duration: toastData.duration });
          break;
        case "warning":
          toast.warning(toastData.message, { duration: toastData.duration });
          break;
        case "info":
          toast.info(toastData.message, { duration: toastData.duration });
          break;
        default:
          toast(toastData.message, { duration: toastData.duration });
      }
    } catch (error) {
      console.error("Failed to parse toast cookie");
    } finally {
      Cookies.remove(TOAST_COOKIE_NAME, { path: "/" });
    }
  }, [pathname]);

  return null;
}
```

### Provider Setup

```typescript
// components/providers.tsx
import { Toaster } from "@szum-tech/design-system";
import { ToastHandler } from "~/lib/toast/components/toast-handler";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <Toaster />        {/* Renders toast container */}
      <ToastHandler />   {/* Reads cookies, triggers toasts */}
    </>
  );
}

// app/layout.tsx
import { Providers } from "~/components/providers";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Cookie Configuration

### TOAST_COOKIE_NAME

```typescript
export const TOAST_COOKIE_NAME = "app-toast";
```

Unique name to avoid conflicts with other cookies.

### TOAST_COOKIE_MAX_AGE

```typescript
export const TOAST_COOKIE_MAX_AGE = 5_000; // 5 seconds
```

Short max-age ensures stale toasts don't appear unexpectedly.

### Cookie Options

| Option | Value | Reason |
|--------|-------|--------|
| `maxAge` | 5000 | Auto-expires if not consumed |
| `path` | "/" | Available on all routes |
| `httpOnly` | false | Must be readable by client JS |
| `sameSite` | "lax" | Sent with same-site navigation |
| `secure` | prod only | HTTPS in production |

## Why This Approach?

### Alternative: Session Storage

**Pros:** Simpler, no cookies
**Cons:** Requires client-side JS, doesn't work with redirects

### Alternative: URL Parameters

**Pros:** Simple, works everywhere
**Cons:** Exposes message in URL, bookmarkable errors

### Alternative: Server State

**Pros:** No cookies needed
**Cons:** Complex state management, doesn't survive redirect

### Cookie Approach (Chosen)

**Pros:**
- Works with redirect()
- No URL pollution
- Auto-cleanup with maxAge
- Design system integration

**Cons:**
- Requires httpOnly: false
- Cookie size limit (~4KB)
- Slight complexity

## Security Considerations

### httpOnly: false

The cookie must be readable by client JavaScript, so `httpOnly: false` is required. This is acceptable because:

1. The cookie contains only UI messages, no sensitive data
2. The cookie is removed immediately after reading
3. Short maxAge limits exposure window

### Message Content

Never put sensitive information in toast messages:

```typescript
// ❌ Bad - exposes internal details
await setToastCookie(`User ${userId} created with role ${role}`, "success");

// ✅ Good - generic message
await setToastCookie("User created successfully", "success");
```

### XSS Prevention

The message is rendered by the design system's Toaster, which handles escaping. However, avoid including user input directly:

```typescript
// ❌ Potentially unsafe
await setToastCookie(`Welcome, ${userInput}!`, "success");

// ✅ Safer
await setToastCookie("Welcome!", "success");
```

## Error Handling

### Cookie Parse Failure

```typescript
try {
  const toastData = JSON.parse(toastCookie);
  // Display toast
} catch (error) {
  logger.error({ error }, "Failed to parse toast cookie");
} finally {
  // Always remove cookie to prevent infinite loop
  Cookies.remove(TOAST_COOKIE_NAME, { path: "/" });
}
```

### Missing Cookie

```typescript
const toastCookie = Cookies.get(TOAST_COOKIE_NAME);
if (!toastCookie) {
  return; // No toast to show, exit early
}
```

## Debugging

### Check Cookie in DevTools

1. Open DevTools → Application → Cookies
2. Look for `app-toast` cookie
3. Check value is valid JSON

### Add Logging

```typescript
React.useEffect(() => {
  const toastCookie = Cookies.get(TOAST_COOKIE_NAME);
  console.log("Toast cookie:", toastCookie);

  if (!toastCookie) {
    console.log("No toast cookie found");
    return;
  }
  // ...
}, [pathname]);
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Toast not showing | Cookie not set | Check server action runs |
| Toast on wrong page | No pathname dep | Add pathname to useEffect |
| Toast shows twice | Multiple handlers | Ensure single ToastHandler |
| Stale toast | Cookie not removed | Check finally block |
