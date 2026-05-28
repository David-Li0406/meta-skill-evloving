# Clerk Auth - Sharp Edges

## CVE-2025-29927 Middleware Bypass Vulnerability

### **Id**
middleware-bypass-cve
### **Severity**
critical
### **Description**
  A critical vulnerability in Next.js (CVSS 9.1) allows attackers to
  bypass middleware authentication by sending a specific HTTP header.
  Affects self-hosted Next.js apps using middleware for auth.
  
  Update immediately: Next.js 15.2.3+, 14.2.25+, 13.5.9+, or 12.3.5+
  
### **Wrong Way**
  // Relying solely on middleware for auth
  // middleware.ts
  export default clerkMiddleware((auth, req) => {
    if (isProtectedRoute(req)) {
      await auth.protect();  // Can be bypassed!
    }
  });
  
  // No additional checks in route handler
  export async function GET() {
    // Assumes middleware already verified auth
    return Response.json(sensitiveData);
  }
  
### **Right Way**
  // 1. Update Next.js immediately
  npm install next@latest
  
  // 2. Defense in depth - verify in route handler too
  export async function GET() {
    const { userId } = await auth();
  
    if (!userId) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }
  
    // Now safe to return data
    return Response.json(sensitiveData);
  }
  
  // 3. Data Access Layer pattern (recommended)
  // Always verify auth at the data access point
  async function getProjects(userId: string) {
    const { userId: authUserId } = await auth();
  
    if (!authUserId || authUserId !== userId) {
      throw new Error('Unauthorized');
    }
  
    return prisma.project.findMany({
      where: { userId },
    });
  }
  
### **Detection Patterns**
  - next.*14\.[0-2]\.(?!25)
  - next.*15\.[0-2]\.(?!3)
### **References**
  - https://clerk.com/articles/complete-authentication-guide-for-nextjs-app-router

## Multiple Middleware Files Cause Conflicts

### **Id**
multiple-middleware-files
### **Severity**
high
### **Description**
  Having separate middleware files for different routes causes conflicts
  and redirect loops. Next.js only supports one middleware.ts file.
  
### **Wrong Way**
  // middleware.ts - handles /api
  // middleware/auth.ts - handles /dashboard
  // middleware/admin.ts - handles /admin
  
  // This causes:
  // - Unpredictable behavior
  // - Redirect loops
  // - Some routes unprotected
  
### **Right Way**
  // Single middleware.ts at project root
  import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
  
  const isProtectedRoute = createRouteMatcher([
    '/dashboard(.*)',
    '/api/private(.*)',
  ]);
  
  const isAdminRoute = createRouteMatcher([
    '/admin(.*)',
  ]);
  
  export default clerkMiddleware(async (auth, req) => {
    if (isAdminRoute(req)) {
      await auth.protect({ role: 'org:admin' });
      return;
    }
  
    if (isProtectedRoute(req)) {
      await auth.protect();
    }
  });
  
  export const config = {
    matcher: ['/((?!_next|.*\\..*).*)'],
  };
  
### **Detection Patterns**
  - middleware.*\.ts.*middleware.*\.ts
### **References**
  - https://clerk.com/docs/reference/nextjs/clerk-middleware

## 4KB Session Token Cookie Limit

### **Id**
cookie-size-limit
### **Severity**
high
### **Description**
  Browsers limit cookies to 4KB. Clerk stores session tokens in cookies.
  Adding large custom claims to the session token can exceed this limit,
  causing authentication to silently fail.
  
### **Wrong Way**
  // Adding large custom claims to session token
  // Clerk Dashboard > Sessions > Customize session token
  
  {
    "metadata": "{{user.public_metadata}}",  // Could be large!
    "permissions": "{{org.permissions}}",
    "full_profile": "{{user.unsafe_metadata}}",
    "audit_log": "{{user.public_metadata.audit_log}}"  // Very large!
  }
  
  // Cookie exceeds 4KB, auth breaks silently
  
### **Right Way**
  // Keep session token minimal
  // Clerk Dashboard > Sessions > Customize session token
  
  {
    "userId": "{{user.id}}",
    "role": "{{org.role}}"
  }
  
  // Fetch large data via API when needed
  export async function GET() {
    const { userId } = await auth();
  
    // Fetch permissions from database
    const permissions = await prisma.userPermission.findMany({
      where: { userId },
    });
  
    // Fetch from Clerk Backend API if needed
    const user = await clerkClient.users.getUser(userId);
    const metadata = user.publicMetadata;
  
    return Response.json({ permissions, metadata });
  }
  
### **Detection Patterns**
  - session.*token.*metadata
  - public_metadata.*session
### **References**
  - https://clerk.com/docs/guides/sessions/session-tokens

## auth() Requires clerkMiddleware Configuration

### **Id**
auth-without-middleware
### **Severity**
high
### **Description**
  The auth() function only works when clerkMiddleware is properly
  configured. Without it, auth() returns empty objects and
  authentication fails silently.
  
### **Wrong Way**
  // No middleware.ts file
  // Or middleware without clerkMiddleware
  
  // middleware.ts
  export function middleware(req) {
    // Custom middleware, no clerkMiddleware
    return NextResponse.next();
  }
  
  // app/dashboard/page.tsx
  const { userId } = await auth();
  // userId is always undefined!
  
### **Right Way**
  // middleware.ts - must use clerkMiddleware
  import { clerkMiddleware } from '@clerk/nextjs/server';
  
  export default clerkMiddleware();
  
  export const config = {
    matcher: [
      '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
      '/(api|trpc)(.*)',
    ],
  };
  
  // Now auth() works
  // app/dashboard/page.tsx
  import { auth } from '@clerk/nextjs/server';
  
  export default async function Dashboard() {
    const { userId } = await auth();
    // userId is now populated correctly
  }
  
### **Detection Patterns**
  - auth\(\).*(?!clerkMiddleware)
### **References**
  - https://clerk.com/docs/references/nextjs/auth

## Webhook Race Conditions

### **Id**
webhook-race-conditions
### **Severity**
medium
### **Description**
  Webhooks are eventually consistent. Events can arrive out of order
  (user.updated before user.created) or during the same request that
  triggered them. This causes race conditions and missing data.
  
### **Wrong Way**
  // Webhook handler assumes order
  if (eventType === 'user.created') {
    await prisma.user.create({
      data: { clerkId: id, email },
    });
  }
  
  if (eventType === 'user.updated') {
    await prisma.user.update({
      where: { clerkId: id },  // Fails if user.created not processed!
      data: { email },
    });
  }
  
### **Right Way**
  // Use upsert for all events
  if (eventType === 'user.created' || eventType === 'user.updated') {
    await prisma.user.upsert({
      where: { clerkId: id },
      create: {
        clerkId: id,
        email: email_addresses[0]?.email_address,
        firstName: first_name,
        lastName: last_name,
      },
      update: {
        email: email_addresses[0]?.email_address,
        firstName: first_name,
        lastName: last_name,
      },
    });
  }
  
  // Handle delete gracefully
  if (eventType === 'user.deleted') {
    await prisma.user.deleteMany({
      where: { clerkId: id },
    });
    // deleteMany doesn't throw if record doesn't exist
  }
  
  // Alternative: JIT sync during request
  async function syncUser(clerkId: string) {
    const clerkUser = await clerkClient.users.getUser(clerkId);
  
    return prisma.user.upsert({
      where: { clerkId },
      create: {
        clerkId,
        email: clerkUser.emailAddresses[0]?.emailAddress,
        // ...
      },
      update: {
        email: clerkUser.emailAddresses[0]?.emailAddress,
        // ...
      },
    });
  }
  
### **Detection Patterns**
  - user\.created.*prisma\..*\.create
  - user\.updated.*prisma\..*\.update(?!Many)
### **References**
  - https://clerk.com/articles/how-to-sync-clerk-user-data-to-your-database

## auth() is Async in App Router

### **Id**
async-auth-app-router
### **Severity**
medium
### **Description**
  In Next.js App Router, auth() is an async function and must be awaited.
  In Pages Router, getAuth() was synchronous. Forgetting await causes
  undefined values.
  
### **Wrong Way**
  // Missing await - common mistake
  export default async function Dashboard() {
    const { userId } = auth();  // Missing await!
    // userId is undefined or a Promise
  
    if (!userId) {
      redirect('/sign-in');  // Always redirects!
    }
  }
  
### **Right Way**
  // Correct: await auth()
  export default async function Dashboard() {
    const { userId } = await auth();
  
    if (!userId) {
      redirect('/sign-in');
    }
  
    // userId is now correctly populated
  }
  
  // In Server Actions
  'use server';
  export async function createPost(formData: FormData) {
    const { userId } = await auth();  // Must await
  
    if (!userId) {
      throw new Error('Unauthorized');
    }
  }
  
### **Detection Patterns**
  - const.*=.*auth\(\)(?!.*await)
  - auth\(\)\.userId
### **References**
  - https://clerk.com/docs/references/nextjs/auth

## Middleware Blocks Webhook Endpoints

### **Id**
webhook-blocking-middleware
### **Severity**
medium
### **Description**
  Webhook requests come from Clerk servers, not authenticated users.
  If middleware protects all routes, webhook endpoints return 401.
  
### **Wrong Way**
  // middleware.ts - protects everything
  export default clerkMiddleware(async (auth, req) => {
    await auth.protect();  // Blocks webhooks!
  });
  
  // Webhook handler never reached
  // app/api/webhooks/clerk/route.ts
  
### **Right Way**
  // Exclude webhook routes from protection
  import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
  
  const isPublicRoute = createRouteMatcher([
    '/',
    '/sign-in(.*)',
    '/sign-up(.*)',
    '/api/webhooks(.*)',  // Webhooks are public
  ]);
  
  export default clerkMiddleware(async (auth, req) => {
    if (!isPublicRoute(req)) {
      await auth.protect();
    }
  });
  
  // Webhook handler verifies with svix instead
  export async function POST(req: Request) {
    // Verify with svix signature
    const wh = new Webhook(WEBHOOK_SECRET);
    const evt = wh.verify(body, headers);
    // ...
  }
  
### **Detection Patterns**
  - auth\.protect\(\)(?!.*webhook)
### **References**
  - https://clerk.com/docs/webhooks/sync-data

## Accessing Auth State Before isLoaded

### **Id**
not-checking-isLoaded
### **Severity**
medium
### **Description**
  Client-side auth state is undefined during initial load/hydration.
  Accessing user or userId before isLoaded is true causes errors or
  incorrect behavior.
  
### **Wrong Way**
  'use client';
  import { useUser } from '@clerk/nextjs';
  
  export function Profile() {
    const { user } = useUser();
  
    // user is undefined during load!
    return <h1>Hello {user.firstName}</h1>;  // Error!
  }
  
### **Right Way**
  'use client';
  import { useUser } from '@clerk/nextjs';
  
  export function Profile() {
    const { user, isLoaded, isSignedIn } = useUser();
  
    // Check loading state
    if (!isLoaded) {
      return <div>Loading...</div>;
    }
  
    // Check auth state
    if (!isSignedIn) {
      return <div>Please sign in</div>;
    }
  
    // Now safe to access user
    return <h1>Hello {user.firstName}</h1>;
  }
  
  // Or use Suspense boundary
  import { ClerkLoaded, ClerkLoading } from '@clerk/nextjs';
  
  export function App() {
    return (
      <>
        <ClerkLoading>
          <div>Loading...</div>
        </ClerkLoading>
        <ClerkLoaded>
          <Profile />
        </ClerkLoaded>
      </>
    );
  }
  
### **Detection Patterns**
  - useUser\(\).*user\.(?!isLoaded)
  - useAuth\(\).*userId(?!.*isLoaded)
### **References**
  - https://clerk.com/docs/references/react/use-user

## Manual Redirects Cause Double Redirects

### **Id**
double-redirects
### **Severity**
medium
### **Description**
  Manually redirecting unauthenticated users in components when
  middleware already handles it causes double redirects. Centralize
  redirect logic in middleware.
  
### **Wrong Way**
  // middleware.ts
  export default clerkMiddleware(async (auth, req) => {
    if (isProtectedRoute(req)) {
      await auth.protect();  // Redirects to sign-in
    }
  });
  
  // app/dashboard/page.tsx
  export default async function Dashboard() {
    const { userId } = await auth();
  
    if (!userId) {
      redirect('/sign-in');  // Double redirect!
    }
  }
  
### **Right Way**
  // Option 1: Let middleware handle all redirects
  // middleware.ts
  export default clerkMiddleware(async (auth, req) => {
    if (isProtectedRoute(req)) {
      await auth.protect();  // Handles redirect
    }
  });
  
  // app/dashboard/page.tsx - no redirect needed
  export default async function Dashboard() {
    const { userId } = await auth();
    // userId guaranteed by middleware
  }
  
  // Option 2: Don't protect in middleware, redirect in component
  // middleware.ts
  export default clerkMiddleware();  // No protection
  
  // app/dashboard/page.tsx
  export default async function Dashboard() {
    const { userId } = await auth();
  
    if (!userId) {
      redirect('/sign-in');  // Single redirect
    }
  }
  
### **Detection Patterns**
  - auth\.protect.*redirect.*sign-in
### **References**
  - https://clerk.com/articles/complete-authentication-guide-for-nextjs-app-router

## Organization Data Not Scoped by orgId

### **Id**
org-data-leakage
### **Severity**
high
### **Description**
  In multi-tenant apps, failing to filter data by orgId allows users
  to access other organizations' data by manipulating the active org
  or crafting requests.
  
### **Wrong Way**
  // Fetching without org scope
  export async function GET() {
    const { userId } = await auth();
  
    // Returns ALL projects, not just current org!
    const projects = await prisma.project.findMany({
      where: { userId },
    });
  
    return Response.json(projects);
  }
  
### **Right Way**
  // Always scope by orgId
  export async function GET() {
    const { userId, orgId } = await auth();
  
    if (!userId) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }
  
    // Scope to current organization
    const projects = await prisma.project.findMany({
      where: {
        organizationId: orgId ?? null,  // null for personal
        ...(orgId ? {} : { userId }),   // Personal = userId filter
      },
    });
  
    return Response.json(projects);
  }
  
  // In data access layer
  async function getProjects() {
    const { userId, orgId } = await auth();
  
    if (!userId) throw new Error('Unauthorized');
  
    // Multi-tenant aware query
    return prisma.project.findMany({
      where: orgId
        ? { organizationId: orgId }
        : { userId, organizationId: null },
    });
  }
  
### **Detection Patterns**
  - prisma\..*\.findMany(?!.*orgId)
  - where.*userId(?!.*orgId)
### **References**
  - https://clerk.com/articles/multi-tenancy-in-react-applications-guide