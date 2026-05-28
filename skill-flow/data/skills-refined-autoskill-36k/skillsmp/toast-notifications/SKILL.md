---
name: toast-notifications
version: 1.0.0
lastUpdated: 2026-01-18
description: Cookie-based toast notification system for server-to-client messaging. Use with Server Actions to provide user feedback after redirects.
tags: [toast, notifications, server-actions, user-feedback, cookies]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to show a toast after form submission
  - Display error toast from server action
  - Toast with custom duration
  - Use toast with redirect
---

# Toast Notifications Skill

Cookie-based toast notification system for server-to-client messaging.

> **Reference Files:**
> - [architecture.md](./architecture.md) - How the system works
> - [patterns.md](./patterns.md) - Usage patterns
> - [examples.md](./examples.md) - Practical examples

## Project Configuration

The toast system is located in `lib/toast/`:

```
lib/toast/
├── constants.ts       # Cookie name and max age
├── types.ts           # ToastType, ToastMessage
├── server/
│   └── toast.cookie.ts  # Server-side cookie setter
└── components/
    └── toast-handler.tsx  # Client-side toast display
```

## Quick Start

### Show Toast After Server Action

```typescript
// features/budget/server/actions/create-budget.ts
"use server";

import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function createBudget(data: FormData): RedirectAction {
  const [error, budget] = await createBudgetInDb(data);

  if (error) {
    await setToastCookie("Failed to create budget", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Budget created successfully!", "success");
  return redirect(`/budgets/${budget.id}`);
}
```

### Toast Types

```typescript
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

// Success (green)
await setToastCookie("Operation completed!", "success");

// Error (red)
await setToastCookie("Something went wrong", "error");

// Warning (yellow)
await setToastCookie("Please review your input", "warning");

// Info (blue)
await setToastCookie("New features available", "info");
```

### Custom Duration

```typescript
// Default duration is ~5 seconds
await setToastCookie("Quick message", "info");

// Custom duration in milliseconds
await setToastCookie("This stays longer", "info", 10000);  // 10 seconds
```

## How It Works

1. **Server Action** calls `setToastCookie()` with message and type
2. **Cookie** is set with JSON payload: `{ type, message, duration }`
3. **Redirect** happens (or response returns)
4. **Client** renders new page with `ToastHandler` component
5. **ToastHandler** reads cookie on pathname change
6. **Toast** is displayed using design system's Toaster
7. **Cookie** is immediately removed

## Key Concepts

### Why Cookies?

Server Actions often redirect after completion. Since the response is a redirect, we can't pass data directly. Cookies persist across the redirect and can be read on the next page load.

### Toast Handler Placement

The `ToastHandler` is included in `components/providers.tsx`:

```typescript
// components/providers.tsx
import { Toaster } from "@szum-tech/design-system";
import { ToastHandler } from "~/lib/toast/components/toast-handler";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <Toaster />
      <ToastHandler />
    </>
  );
}
```

### Pathname-Based Triggering

ToastHandler watches `pathname` changes using `usePathname()`:

```typescript
const pathname = usePathname();

React.useEffect(() => {
  // Check and display toast on route change
}, [pathname]);
```

This ensures toasts appear after navigation.

## API Reference

### setToastCookie

```typescript
async function setToastCookie(
  message: string,
  type: ToastType = "success",
  duration?: number
): Promise<void>
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | string | required | Toast message text |
| `type` | ToastType | "success" | Toast variant |
| `duration` | number | undefined | Display duration in ms |

### ToastType

```typescript
type ToastType = "success" | "error" | "info" | "warning";
```

### ToastMessage

```typescript
interface ToastMessage {
  type: ToastType;
  message: string;
  duration?: number;
}
```

## File Locations

| Purpose | Location |
|---------|----------|
| Server cookie setter | `lib/toast/server/toast.cookie.ts` |
| Client handler | `lib/toast/components/toast-handler.tsx` |
| Types | `lib/toast/types.ts` |
| Constants | `lib/toast/constants.ts` |
| Providers | `components/providers.tsx` |

## Related Skills

- `server-actions` - Using toasts with server actions
- `clerk-auth-proxy` - Toast after auth operations
