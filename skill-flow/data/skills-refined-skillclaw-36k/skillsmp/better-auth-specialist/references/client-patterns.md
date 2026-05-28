# Client Patterns for Better Auth

Frontend authentication patterns for Next.js 15+ and React 18+ applications.

## Table of Contents
- Setup and Configuration
- Authentication Forms
- Protected Routes
- Session Hooks
- User Context
- OAuth Integration

## Setup and Configuration

### Create Auth Client

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

// Export hooks and methods
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  useUser,
} = authClient;
```

### Session Provider (App Router)

```typescript
// app/layout.tsx
import { SessionProvider } from "@/lib/auth-client";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
```

### Session Provider (Pages Router)

```typescript
// pages/_app.tsx
import type { AppProps } from "next/app";
import { SessionProvider } from "@/lib/auth-client";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <SessionProvider>
      <Component {...pageProps} />
    </SessionProvider>
  );
}
```

## Authentication Forms

### Signup Form

```typescript
// components/auth/signup-form.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";

export function SignUpForm() {
  const router = useRouter();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signUp.email({
        email: formData.email,
        password: formData.password,
        name: formData.name,
      });

      toast({
        title: "Account created",
        description: "You have successfully signed up!",
      });

      router.push("/dashboard");
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to sign up",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          type="text"
          placeholder="John Doe"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
      </div>
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? "Creating account..." : "Sign Up"}
      </Button>
    </form>
  );
}
```

### Signin Form

```typescript
// components/auth/signin-form.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/components/ui/use-toast";

export function SignInForm() {
  const router = useRouter();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signIn.email({
        email: formData.email,
        password: formData.password,
        rememberMe: formData.rememberMe,
      });

      toast({
        title: "Welcome back!",
        description: "You have successfully signed in.",
      });

      router.push("/dashboard");
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Invalid email or password",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="remember"
          checked={formData.rememberMe}
          onCheckedChange={(checked) =>
            setFormData({ ...formData, rememberMe: checked as boolean })
          }
        />
        <Label htmlFor="remember" className="text-sm">
          Remember me
        </Label>
      </div>
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </Button>
    </form>
  );
}
```

### Combined Auth Page

```typescript
// app/auth/page.tsx
"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SignInForm } from "@/components/auth/signin-form";
import { SignUpForm } from "@/components/auth/signup-form";

export default function AuthPage() {
  return (
    <div className="container flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome</CardTitle>
          <CardDescription>Sign in to your account or create a new one</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="signin">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="signin">Sign In</TabsTrigger>
              <TabsTrigger value="signup">Sign Up</TabsTrigger>
            </TabsList>
            <TabsContent value="signin">
              <SignInForm />
            </TabsContent>
            <TabsContent value="signup">
              <SignUpForm />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Protected Routes

### Protected Page Component (App Router)

```typescript
// app/dashboard/page.tsx
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/auth");
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Protected Route Middleware

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "@/lib/auth";

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  // Protected routes
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    if (!session) {
      return NextResponse.redirect(new URL("/auth", request.url));
    }
  }

  // Auth routes (redirect to dashboard if already logged in)
  if (request.nextUrl.pathname.startsWith("/auth")) {
    if (session) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"],
};
```

### Client-Side Protected Component

```typescript
// components/protected-content.tsx
"use client";

import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loader2 } from "lucide-react";

export function ProtectedContent({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/auth");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return <>{children}</>;
}
```

## Session Hooks

### useSession Hook

```typescript
"use client";

import { useSession } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session, isPending, error } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error loading session</div>;
  }

  if (!session) {
    return <div>Not authenticated</div>;
  }

  return (
    <div>
      <p>Name: {session.user.name}</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### useUser Hook

```typescript
"use client";

import { useUser } from "@/lib/auth-client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function UserAvatar() {
  const { data: user, isPending } = useUser();

  if (isPending || !user) {
    return <Avatar><AvatarFallback>?</AvatarFallback></Avatar>;
  }

  return (
    <Avatar>
      <AvatarImage src={user.image} alt={user.name} />
      <AvatarFallback>{user.name?.[0] || "U"}</AvatarFallback>
    </Avatar>
  );
}
```

## User Menu Component

```typescript
// components/user-menu.tsx
"use client";

import { useSession, signOut } from "@/lib/auth-client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useRouter } from "next/navigation";
import { LogOut, Settings, User } from "lucide-react";

export function UserMenu() {
  const { data: session } = useSession();
  const router = useRouter();

  if (!session) return null;

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-10 w-10 rounded-full">
          <Avatar>
            <AvatarImage src={session.user.image} alt={session.user.name} />
            <AvatarFallback>{session.user.name?.[0] || "U"}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium">{session.user.name}</p>
            <p className="text-xs text-muted-foreground">{session.user.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => router.push("/profile")}>
          <User className="mr-2 h-4 w-4" />
          Profile
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => router.push("/settings")}>
          <Settings className="mr-2 h-4 w-4" />
          Settings
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleSignOut}>
          <LogOut className="mr-2 h-4 w-4" />
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

## OAuth Integration

### OAuth Sign In Buttons

```typescript
// components/auth/oauth-buttons.tsx
"use client";

import { signIn } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";

export function OAuthButtons() {
  const { toast } = useToast();

  const handleOAuthSignIn = async (provider: "google" | "github") => {
    try {
      await signIn.social({
        provider,
        callbackURL: "/dashboard",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: `Failed to sign in with ${provider}`,
      });
    }
  };

  return (
    <div className="grid gap-2">
      <Button
        variant="outline"
        onClick={() => handleOAuthSignIn("google")}
      >
        <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
          <path
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            fill="#4285F4"
          />
          <path
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            fill="#34A853"
          />
          <path
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            fill="#FBBC05"
          />
          <path
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            fill="#EA4335"
          />
        </svg>
        Continue with Google
      </Button>
      <Button
        variant="outline"
        onClick={() => handleOAuthSignIn("github")}
      >
        <svg className="mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
        </svg>
        Continue with GitHub
      </Button>
    </div>
  );
}
```

## Role-Based UI

### Role Check Hook

```typescript
// hooks/use-role.ts
"use client";

import { useSession } from "@/lib/auth-client";

export function useRole() {
  const { data: session } = useSession();

  const hasRole = (role: string) => {
    return session?.user?.roles?.some((r: any) => r.name === role) || false;
  };

  const hasAnyRole = (roles: string[]) => {
    return roles.some((role) => hasRole(role));
  };

  return { hasRole, hasAnyRole };
}
```

### Role-Based Component

```typescript
// components/role-guard.tsx
"use client";

import { useRole } from "@/hooks/use-role";

interface RoleGuardProps {
  roles: string[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function RoleGuard({ roles, children, fallback = null }: RoleGuardProps) {
  const { hasAnyRole } = useRole();

  if (!hasAnyRole(roles)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

// Usage
<RoleGuard roles={["admin", "moderator"]}>
  <AdminPanel />
</RoleGuard>
```

## Loading States

```typescript
// components/auth-loading.tsx
import { Skeleton } from "@/components/ui/skeleton";

export function AuthLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-12 w-full" />
      <Skeleton className="h-12 w-full" />
      <Skeleton className="h-10 w-full" />
    </div>
  );
}
```

## Error Handling

```typescript
// components/auth-error.tsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

interface AuthErrorProps {
  error: Error | null;
}

export function AuthError({ error }: AuthErrorProps) {
  if (!error) return null;

  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>Authentication Error</AlertTitle>
      <AlertDescription>{error.message}</AlertDescription>
    </Alert>
  );
}
```
