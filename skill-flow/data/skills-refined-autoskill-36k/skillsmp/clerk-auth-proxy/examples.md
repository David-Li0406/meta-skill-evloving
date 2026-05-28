# Clerk Authentication Examples

## Server Actions with Authentication

### Basic Protected Action

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import type { ActionResponse } from "~/lib/action-types";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-actions" });

export async function updateProfile(
  data: ProfileFormData
): ActionResponse<Profile> {
  // 1. Authentication check
  const { userId, isAuthenticated } = await auth();

  if (!isAuthenticated || !userId) {
    logger.warn("Unauthenticated user attempted to update profile");
    return { success: false, error: "Authentication required" };
  }

  // 2. Validation
  const parsed = profileSchema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 3. Database operation
  const [error, profile] = await updateProfileInDb(userId, parsed.data);
  if (error) {
    logger.error({ userId, errorCode: error.code }, "Failed to update profile");
    return { success: false, error: "Failed to update profile" };
  }

  // 4. Success
  logger.info({ userId }, "Profile updated successfully");
  return { success: true, data: profile };
}
```

### Role-Based Action

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import type { ActionResponse } from "~/lib/action-types";

export async function adminDeleteUser(
  targetUserId: string
): ActionResponse<void> {
  const { userId, sessionClaims } = await auth();

  // Check authentication
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // Check admin role
  if (sessionClaims?.metadata?.role !== "admin") {
    return { success: false, error: "Admin access required" };
  }

  // Prevent self-deletion
  if (userId === targetUserId) {
    return { success: false, error: "Cannot delete own account" };
  }

  const [error] = await deleteUser(targetUserId);
  if (error) {
    return { success: false, error: "Failed to delete user" };
  }

  return { success: true, data: undefined };
}
```

### Action with Redirect

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import type { RedirectAction } from "~/lib/action-types";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function createBudget(
  data: BudgetFormData
): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  const [error, budget] = await createBudgetInDb(userId, data);
  if (error) {
    return { success: false, error: "Failed to create budget" };
  }

  await setToastCookie("Budget created successfully!", "success");
  return redirect(`/budgets/${budget.id}`);
}
```

## Page Loaders with Authentication

### Basic Protected Page

```typescript
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

async function loadData() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  const [error, data] = await getUserDashboard(userId);

  if (error) {
    if (error.isNotFound) {
      redirect("/onboarding");
    }
    throw error; // Let error.tsx handle
  }

  return data;
}

export default async function DashboardPage() {
  const data = await loadData();

  return <Dashboard data={data} />;
}
```

### Page with Session Claims Check

```typescript
// app/admin/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect, notFound } from "next/navigation";

async function loadData() {
  const { userId, sessionClaims } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  // Check admin role
  if (sessionClaims?.metadata?.role !== "admin") {
    notFound(); // Or redirect to unauthorized page
  }

  return await getAdminDashboard();
}

export default async function AdminPage() {
  const data = await loadData();

  return <AdminDashboard data={data} />;
}
```

### Dynamic Route with Ownership Check

```typescript
// app/budgets/[id]/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect, notFound } from "next/navigation";

interface Props {
  params: Promise<{ id: string }>;
}

async function loadData(budgetId: string) {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  const [error, budget] = await getBudgetById(budgetId);

  if (error) {
    if (error.isNotFound) {
      notFound();
    }
    throw error;
  }

  // Ownership check
  if (budget.userId !== userId) {
    notFound(); // Don't reveal existence
  }

  return budget;
}

export default async function BudgetPage({ params }: Props) {
  const { id } = await params;
  const budget = await loadData(id);

  return <BudgetDetail budget={budget} />;
}
```

## Route Handlers

### Protected API Route

```typescript
// app/api/budgets/route.ts
import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  const [error, budgets] = await getBudgetsByUser(userId);

  if (error) {
    return NextResponse.json(
      { error: "Failed to fetch budgets" },
      { status: 500 }
    );
  }

  return NextResponse.json({ data: budgets });
}

export async function POST(request: Request) {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const body = await request.json();
    const parsed = budgetSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: "Validation failed", details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    const [error, budget] = await createBudget(userId, parsed.data);

    if (error) {
      return NextResponse.json(
        { error: "Failed to create budget" },
        { status: 500 }
      );
    }

    return NextResponse.json({ data: budget }, { status: 201 });
  } catch {
    return NextResponse.json(
      { error: "Invalid request body" },
      { status: 400 }
    );
  }
}
```

### Webhook Handler (No Auth)

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from "svix";
import { headers } from "next/headers";
import type { WebhookEvent } from "@clerk/nextjs/server";

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    throw new Error("Missing CLERK_WEBHOOK_SECRET");
  }

  const headerPayload = await headers();
  const svix_id = headerPayload.get("svix-id");
  const svix_timestamp = headerPayload.get("svix-timestamp");
  const svix_signature = headerPayload.get("svix-signature");

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response("Missing svix headers", { status: 400 });
  }

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      "svix-id": svix_id,
      "svix-timestamp": svix_timestamp,
      "svix-signature": svix_signature
    }) as WebhookEvent;
  } catch {
    return new Response("Invalid signature", { status: 400 });
  }

  // Handle events
  switch (evt.type) {
    case "user.created":
      await handleUserCreated(evt.data);
      break;
    case "user.deleted":
      await handleUserDeleted(evt.data);
      break;
  }

  return new Response("OK", { status: 200 });
}
```

## Client Components

### Using useUser Hook

```typescript
"use client";

import { useUser } from "@clerk/nextjs";
import { Skeleton } from "@szum-tech/design-system";

export function UserGreeting() {
  const { user, isLoaded, isSignedIn } = useUser();

  if (!isLoaded) {
    return <Skeleton className="h-8 w-32" />;
  }

  if (!isSignedIn) {
    return <span>Welcome, Guest</span>;
  }

  return <span>Welcome, {user.firstName}</span>;
}
```

### Using useAuth Hook

```typescript
"use client";

import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";

export function ProtectedButton() {
  const { isSignedIn } = useAuth();
  const router = useRouter();

  const handleClick = () => {
    if (!isSignedIn) {
      router.push("/sign-in");
      return;
    }

    // Perform action
  };

  return (
    <button onClick={handleClick}>
      {isSignedIn ? "Do Action" : "Sign In Required"}
    </button>
  );
}
```

### Checking Public Metadata on Client

```typescript
"use client";

import { useUser } from "@clerk/nextjs";

export function PlanBadge() {
  const { user } = useUser();

  const plan = user?.publicMetadata?.plan ?? "free";

  return (
    <span className="badge">
      {plan === "pro" ? "Pro Plan" : "Free Plan"}
    </span>
  );
}
```

## Providers Setup

```typescript
// components/providers.tsx
"use client";

import type { ReactNode } from "react";
import { ClerkProvider } from "@clerk/nextjs";
import { plPL } from "@clerk/localizations";
import { ToastHandler } from "~/lib/toast/components/toast-handler";
import { Toaster } from "@szum-tech/design-system";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ClerkProvider localization={plPL}>
      {children}
      <Toaster />
      <ToastHandler />
    </ClerkProvider>
  );
}
```

## Error Handling Patterns

### Graceful Auth Failure

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";

export async function safeAction(): ActionResponse<Data> {
  try {
    const { userId } = await auth();

    if (!userId) {
      return { success: false, error: "Please sign in to continue" };
    }

    // ... action logic
  } catch (error) {
    // Handle Clerk errors gracefully
    if (error instanceof Error && error.message.includes("CLERK")) {
      return { success: false, error: "Authentication service unavailable" };
    }
    throw error;
  }
}
```

### Logging Auth Events

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "secure-actions" });

export async function sensitiveAction(): ActionResponse {
  const { userId, sessionClaims } = await auth();

  if (!userId) {
    logger.warn({ action: "sensitiveAction" }, "Unauthenticated access attempt");
    return { success: false, error: "Authentication required" };
  }

  logger.info({
    userId,
    role: sessionClaims?.metadata?.role,
    action: "sensitiveAction"
  }, "Sensitive action accessed");

  // ... action logic
}
```
