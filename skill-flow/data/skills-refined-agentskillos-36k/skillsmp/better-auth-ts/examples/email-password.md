# Email/Password Authentication Examples

## Basic Sign Up

```typescript
// Client-side
const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",
});

if (error) {
  console.error("Sign up failed:", error.message);
  return;
}

console.log("User created:", data.user);
```

## Sign In

```typescript
// Client-side
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
});

if (error) {
  console.error("Sign in failed:", error.message);
  return;
}

// Redirect to dashboard
window.location.href = "/dashboard";
```

## Sign In with Callback

```typescript
await authClient.signIn.email({
  email: "user@example.com",
  password: "password",
  callbackURL: "/dashboard", // Redirect after success
});
```

## Sign Out

```typescript
await authClient.signOut();
// Or with redirect
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => {
      window.location.href = "/";
    },
  },
});
```

## React Hook Example

```tsx
// hooks/useAuth.ts
import { authClient } from "@/lib/auth-client";
import { useState } from "react";

export function useSignIn() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    setError(null);

    const { error } = await authClient.signIn.email({
      email,
      password,
    });

    setLoading(false);

    if (error) {
      setError(error.message);
      return false;
    }

    return true;
  };

  return { signIn, loading, error };
}
```

## React Form Component

```tsx
"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const { error } = await authClient.signIn.email({
      email,
      password,
    });

    setLoading(false);

    if (error) {
      setError(error.message);
      return;
    }

    router.push("/dashboard");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
```

## Server Action (Next.js)

```typescript
// app/actions/auth.ts
"use server";

import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export async function signIn(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  try {
    await auth.api.signInEmail({
      body: { email, password },
    });
    redirect("/dashboard");
  } catch (error) {
    return { error: "Invalid credentials" };
  }
}

export async function signUp(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  const name = formData.get("name") as string;

  try {
    await auth.api.signUpEmail({
      body: { email, password, name },
    });
    redirect("/dashboard");
  } catch (error) {
    return { error: "Sign up failed" };
  }
}
```

## Password Reset Flow

### Request Reset

```typescript
// Client
await authClient.forgetPassword({
  email: "user@example.com",
  redirectTo: "/reset-password", // URL with token
});
```

### Server Config

```typescript
// lib/auth.ts
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `<a href="${url}">Reset Password</a>`,
      });
    },
  },
});
```

### Reset Password

```typescript
// Client - on /reset-password page
const token = new URLSearchParams(window.location.search).get("token");

await authClient.resetPassword({
  newPassword: "newSecurePassword123",
  token,
});
```

## Email Verification

### Server Config

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Verify Email</a>`,
      });
    },
  },
});
```

### Resend Verification

```typescript
await authClient.sendVerificationEmail({
  email: "user@example.com",
  callbackURL: "/dashboard",
});
```

## Password Requirements

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },
});
```

## Error Handling

```typescript
const { error } = await authClient.signIn.email({
  email,
  password,
});

if (error) {
  switch (error.status) {
    case 401:
      setError("Invalid email or password");
      break;
    case 403:
      setError("Please verify your email first");
      break;
    case 429:
      setError("Too many attempts. Please try again later.");
      break;
    default:
      setError("Something went wrong");
  }
}
```
