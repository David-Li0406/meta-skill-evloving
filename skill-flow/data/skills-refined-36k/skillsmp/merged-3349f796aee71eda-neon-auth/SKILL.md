---
name: neon-auth
description: Use this skill when adding authentication to Next.js, React SPA, or Node.js applications, including setup for Neon Auth in Next.js App Router applications.
---

# Neon Auth Integration

Add authentication to your application.

## When to Use This Skill

- Adding authentication to a new or existing project
- Implementing sign-in, sign-up, and session management
- Configuring social authentication (Google, GitHub)
- Setting up Neon Auth specifically in Next.js App Router applications (auth-only, no database needed)

**Package**: `@neondatabase/auth` (auth only, smaller bundle)

**Need database queries too?** Use the `neon-js` skill instead for `@neondatabase/neon-js` with unified auth + data API.

## Code Generation Rules

When generating TypeScript/JavaScript code, follow these rules:

**Complete reference:** See [Code Generation Rules](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/code-generation-rules.md) for:
- Import path handling (path aliases vs relative imports)
- Neon package imports (subpath exports, adapter patterns)
- CSS import strategy (Tailwind detection, single import method)
- File structure patterns

**Key points:**
- Check `tsconfig.json` for path aliases before generating imports
- Use relative imports if unsure or no aliases exist
- `BetterAuthReactAdapter` MUST be imported from `auth/react/adapters` subpath
- Adapters are factory functions - call them with `()`
- Choose ONE CSS import method (Tailwind or CSS, not both)

## Available Guides

Each guide is a complete, self-contained walkthrough with numbered phases:

- **`guides/nextjs-setup.md`** - Complete Next.js App Router setup guide
- **`guides/react-spa-setup.md`** - Detailed React SPA guide with react-router-dom integration

I'll automatically detect your context (package manager, framework, existing setup) and select the appropriate guide based on your request.

For troubleshooting, see the [Troubleshooting Guide](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-troubleshooting.md) in references.

## Quick Examples

Tell me what you're building - I'll handle the rest:

- "Add authentication to my Next.js app" -> Loads setup guide, sets up auth routes
- "Set up sign-in with Google" -> Configures social auth provider
- "Debug my auth session not persisting" -> Loads troubleshooting guide

## Reference Documentation

**Primary Resource:** See [neon-auth.mdc](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/neon-auth.mdc) for comprehensive guidelines including:
- All authentication methods (email/password, social, magic link)
- Session data structure
- UI components reference
- Error handling

**Framework-Specific Setup (choose your framework):**
- [Setup - Next.js](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-setup-nextjs.md)
- [Setup - React SPA](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-setup-react-spa.md)
- [Setup - Node.js](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-setup-nodejs.md)

**Framework-Specific UI (choose your framework):**
- [UI - Next.js](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-ui-nextjs.md)
- [UI - React SPA](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-ui-react-spa.md)

**Shared References:**
- [Common Mistakes](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-common-mistakes.md) - Import paths, adapter patterns, CSS
- [Troubleshooting Guide](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth-troubleshooting.md) - Error solutions
- [Code Generation Rules](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/code-generation-rules.md) - Import and CSS strategies
- [Auth Adapters Guide](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-js-adapters.md) - Adapter comparison
- [Import Reference](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-js-imports.md) - Complete import paths

## Templates

- `templates/nextjs-api-route.ts` - API route handler for Next.js
- `templates/auth-client.ts` - Client-side auth configuration

## Workflow

I will:
1. Detect your project context automatically (Next.js, React SPA, Node.js)
2. Select and load the appropriate guide
3. Follow the guide's phases sequentially
4. Track progress using the guide's workflow checklist
5. Load reference files only when needed
6. Offer to add Neon best practices to your project docs

Ready to get started? Just describe what you're building!

## Setup for Next.js

### 1. Install
```bash
npm install @neondatabase/auth
```

### 2. Environment (`.env.local`)
```
NEON_AUTH_BASE_URL=https://your-auth.neon.tech
```

### 3. API Route (`app/api/auth/[...path]/route.ts`)
```typescript
import { authApiHandler } from '@neondatabase/auth/next/server';

export const { GET, POST } = authApiHandler();
```

### 4. Middleware (`middleware.ts`)
```typescript
import { neonAuthMiddleware } from '@neondatabase/auth/next/server';

export default neonAuthMiddleware({
  loginUrl: '/auth/sign-in',
});

export const config = {
  matcher: ['/dashboard/:path*', '/account/:path*'],
};
```

### 5. Client (`lib/auth-client.ts`)
```typescript
'use client';
import { createAuthClient } from '@neondatabase/auth/next';

export const authClient = createAuthClient();
```

### 6. Provider (`app/providers.tsx`)
```typescript
'use client';
import { NeonAuthUIProvider } from '@neondatabase/auth/react/ui';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export function Providers({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <NeonAuthUIProvider
      authClient={authClient}
      navigate={router.push}
      replace={router.replace}
      onSessionChange={() => router.refresh()}
      redirectTo="/dashboard"
      Link={({href, children}) => <Link to={href}>{children}</Link>}
    >
      {children}
    </NeonAuthUIProvider>
  );
}
```

### 7. Layout (`app/layout.tsx`)
```typescript
import { Providers } from './providers';
import '@neondatabase/auth/ui/css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 8. Auth Pages (`app/auth/[path]/page.tsx`)
```typescript
import { AuthView } from '@neondatabase/auth/react/ui';
import { authViewPaths } from '@neondatabase/auth/react/ui/server';

export function generateStaticParams() {
  return Object.values(authViewPaths).map((path) => ({ path }));
}

export default async function AuthPage({ params }: { params: Promise<{ path: string }> }) {
  const { path } = await params;
  return <AuthView pathname={path} />;
}
```

## CSS & Styling

### Import Options

**Without Tailwind** (pre-built CSS bundle ~47KB):
```typescript
// app/layout.tsx
import '@neondatabase/auth/ui/css';
```

**With Tailwind CSS v4** (`app/globals.css`):
```css
@import 'tailwindcss';
@import '@neondatabase/auth/ui/tailwind';
```

**IMPORTANT**: Never import both - causes duplicate styles.

### Dark Mode

The provider includes `next-themes`. Control via `defaultTheme` prop:

```typescript
<NeonAuthUIProvider
  defaultTheme="system" // 'light' | 'dark' | 'system'
  // ...
>
```

### Custom Theming

Override CSS variables in `globals.css`:
```css
:root {
  --primary: hsl(221.2 83.2% 53.3%);
  --primary-foreground: hsl(210 40% 98%);
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --card: hsl(0 0% 100%);
  --card-foreground: hsl(222.2 84% 4.9%);
  --border: hsl(214.3 31.8% 91.4%);
  --input: hsl(214.3 31.8% 91.4%);
  --ring: hsl(221.2 83.2% 53.3%);
  --radius: 0.5rem;
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  /* ... dark mode overrides */
}
```

## NeonAuthUIProvider Props

Full configuration options:

```typescript
<NeonAuthUIProvider
  // Required
  authClient={authClient}

  // Navigation (Next.js specific)
  navigate={router.push}        // router.push for navigation
  replace={router.replace}      // router.replace for redirects
  onSessionChange={() => router.refresh()} // Refresh Server Components!
  redirectTo="/dashboard"       // Where to redirect after auth
  Link={({href, children}) => <Link to={href}>{children}</Link>}                   // Next.js Link component

  // Social/OAuth Providers
  social={{
    providers: ['google'],
  }}

  // Feature Flags
  emailOTP={true}               // Enable email OTP sign-in
  emailVerification={true}      // Require email verification
  magicLink={false}             // Magic link (disabled by default)
  multiSession={false}          // Multiple sessions (disabled)

  // Credentials Configuration
  credentials={{
    forgotPassword: true,       // Show forgot password link
  }}

  // Sign Up Fields
  signUp={{
    fields: ['name'],           // Additional fields: 'name', 'username', etc.
  }}

  // Account Settings Fields
  account={{
    fields: ['image', 'name', 'company', 'age', 'newsletter'],
  }}

  // Organization Features
  organization={{}}             // Enable org features

  // Dark Mode
  defaultTheme="system"         // 'light' | 'dark' | 'system'

  // Custom Labels
  localization={{
    SIGN_IN: 'Welcome Back',
    SIGN_UP: 'Create Account',
    FORGOT_PASSWORD: 'Forgot Password?',
    OR_CONTINUE_WITH: 'or continue with',
  }}
>
  {children}
</NeonAuthUIProvider>
```

## Server Components (RSC)

### Get Session in Server Component

```typescript
// NO 'use client' - this is a Server Component
import { neonAuth } from '@neondatabase/auth/next/server';

export async function Profile() {
  const { session, user } = await neonAuth();

  if (!user) return <div>Not signed in</div>;

  return (
    <div>
      <p>Hello, {user.name}</p>
      <p>Email: {user.email}</p>
    </div>
  );
}
```

### Route Handler with Auth

```typescript
// app/api/user/route.ts
import { neonAuth } from '@neondatabase/auth/next/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { user } = await neonAuth();

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return NextResponse.json({ user });
}
```

## Server Actions

### Setup Server Auth (`lib/auth/server.ts`)

```typescript
import { createAuthServer } from '@neondatabase/auth/next/server';

export const authServer = createAuthServer();
```

### Sign In Action

```typescript
// app/actions/auth.ts
'use server';
import { authServer } from '@/lib/auth/server';
import { redirect } from 'next/navigation';

export async function signIn(formData: FormData) {
  const { error } = await authServer.signIn.email({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  });

  if (error) {
    return { error: error.message };
  }

  redirect('/dashboard');
}

export async function signUp(formData: FormData) {
  const { error } = await authServer.signUp.email({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
    name: formData.get('name') as string,
  });

  if (error) {
    return { error: error.message };
  }

  redirect('/dashboard');
}

export async function signOut() {
  await authServer.signOut();
  redirect('/');
}
```

### Available Server Methods

```typescript
// Authentication
authServer.signIn.email({ email, password })
authServer.signUp.email({ email, password, name })
authServer.signOut()
authServer.getSession()

// User Management
authServer.updateUser({ name, image })

// Organizations
authServer.organization.create({ name, slug })
authServer.organization.list()

// Admin (if enabled)
authServer.admin.listUsers()
authServer.admin.banUser({ userId })
```

## Client Components

### Session Hook

```typescript
'use client';
import { authClient } from '@/lib/auth-client';

export function Dashboard() {
  const { data: session, isPending, error } = authClient.useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!session) return <div>Not signed in</div>;

  return <div>Hello, {session.user.name}</div>;
}
```

### Client-Side Auth Methods

```typescript
'use client';
import { authClient } from '@/lib/auth-client';

// Sign in
await authClient.signIn.email({ email, password });

// Sign up
await authClient.signUp.email({ email, password, name });

// OAuth
await authClient.signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
});

// Sign out
await authClient.signOut();

// Get session
const session = await authClient.getSession();
```

### UI Components

### AuthView - Main Auth Interface

```typescript
import { AuthView } from '@neondatabase/auth/react/ui';

// Handles: sign-in, sign-up, forgot-password, reset-password, callback, sign-out
<AuthView pathname={path} />
```

### Conditional Rendering

```typescript
import {
  SignedIn,
  SignedOut,
  AuthLoading,
  RedirectToSignIn,
} from '@neondatabase/auth/react/ui';

function MyPage() {
  return (
    <>
      <AuthLoading>
        <LoadingSpinner />
      </AuthLoading>

      <SignedIn>
        <Dashboard />
      </SignedIn>

      <SignedOut>
        <LandingPage />
      </SignedOut>

      {/* Auto-redirect if not signed in */}
      <RedirectToSignIn />
    </>
  );
}
```

### UserButton

```typescript
import { UserButton } from '@neondatabase/auth/react/ui';

function Header() {
  return (
    <header>
      <nav>...</nav>
      <UserButton />
    </header>
  );
}
```

### Account Management

```typescript
import {
  AccountSettingsCards,
  SecuritySettingsCards,
  SessionsCard,
  ChangePasswordCard,
  ChangeEmailCard,
  DeleteAccountCard,
  ProvidersCard,
} from '@neondatabase/auth/react/ui';
```

### Organization Components

```typescript
import {
  OrganizationSwitcher,
  OrganizationSettings