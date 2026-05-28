# Magic Link Authentication Examples

## Server Setup

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { magicLink } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    magicLink({
      sendMagicLink: async ({ email, token, url }, request) => {
        // Send email with magic link
        await sendEmail({
          to: email,
          subject: "Sign in to My App",
          html: `
            <h1>Sign in to My App</h1>
            <p>Click the link below to sign in:</p>
            <a href="${url}">Sign In</a>
            <p>This link expires in 5 minutes.</p>
            <p>If you didn't request this, you can ignore this email.</p>
          `,
        });
      },
      expiresIn: 60 * 5, // 5 minutes (default)
      disableSignUp: false, // Allow new users to sign up via magic link
    }),
  ],
});
```

## Client Setup

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/client";
import { magicLinkClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [magicLinkClient()],
});
```

## Request Magic Link

```typescript
const { error } = await authClient.signIn.magicLink({
  email: "user@example.com",
  callbackURL: "/dashboard",
});

if (error) {
  console.error("Failed to send magic link:", error.message);
}
```

## React Magic Link Form

```tsx
"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";

export function MagicLinkForm() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const { error } = await authClient.signIn.magicLink({
      email,
      callbackURL: "/dashboard",
    });

    setLoading(false);

    if (error) {
      setError(error.message);
      return;
    }

    setSent(true);
  };

  if (sent) {
    return (
      <div>
        <h2>Check your email</h2>
        <p>We sent a magic link to <strong>{email}</strong></p>
        <p>Click the link in the email to sign in.</p>
        <button onClick={() => setSent(false)}>
          Use a different email
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign in with Magic Link</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Sending..." : "Send Magic Link"}
      </button>
    </form>
  );
}
```

## With New User Callback

```typescript
await authClient.signIn.magicLink({
  email: "new@example.com",
  callbackURL: "/dashboard",
  newUserCallbackURL: "/welcome", // Redirect new users here
});
```

## With Name for New Users

```typescript
await authClient.signIn.magicLink({
  email: "new@example.com",
  name: "John Doe", // Used if user doesn't exist
  callbackURL: "/dashboard",
});
```

## Disable Sign Up

Only allow existing users:

```typescript
// Server
magicLink({
  sendMagicLink: async ({ email, url }) => {
    await sendEmail({ to: email, subject: "Sign in", html: `<a href="${url}">Sign in</a>` });
  },
  disableSignUp: true, // Only existing users can use magic link
})
```

## Custom Email Templates

### With React Email

```typescript
import { MagicLinkEmail } from "@/emails/magic-link";
import { render } from "@react-email/render";
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

magicLink({
  sendMagicLink: async ({ email, url }) => {
    await resend.emails.send({
      from: "noreply@myapp.com",
      to: email,
      subject: "Sign in to My App",
      html: render(MagicLinkEmail({ url })),
    });
  },
})
```

### Email Template Component

```tsx
// emails/magic-link.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Html,
  Preview,
  Text,
} from "@react-email/components";

interface MagicLinkEmailProps {
  url: string;
}

export function MagicLinkEmail({ url }: MagicLinkEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Sign in to My App</Preview>
      <Body style={{ fontFamily: "sans-serif" }}>
        <Container>
          <Text>Click the button below to sign in:</Text>
          <Button
            href={url}
            style={{
              background: "#000",
              color: "#fff",
              padding: "12px 20px",
              borderRadius: "5px",
            }}
          >
            Sign In
          </Button>
          <Text style={{ color: "#666", fontSize: "14px" }}>
            This link expires in 5 minutes.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

## With Nodemailer

```typescript
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT),
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

magicLink({
  sendMagicLink: async ({ email, url }) => {
    await transporter.sendMail({
      from: '"My App" <noreply@myapp.com>',
      to: email,
      subject: "Sign in to My App",
      html: `<a href="${url}">Sign in</a>`,
    });
  },
})
```

## With SendGrid

```typescript
import sgMail from "@sendgrid/mail";

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

magicLink({
  sendMagicLink: async ({ email, url }) => {
    await sgMail.send({
      to: email,
      from: "noreply@myapp.com",
      subject: "Sign in to My App",
      html: `<a href="${url}">Sign in</a>`,
    });
  },
})
```

## Error Handling

```typescript
await authClient.signIn.magicLink({
  email,
  callbackURL: "/dashboard",
  fetchOptions: {
    onError(ctx) {
      if (ctx.error.status === 404) {
        setError("No account found with this email");
      } else if (ctx.error.status === 429) {
        setError("Too many requests. Please wait a moment.");
      } else {
        setError("Failed to send magic link");
      }
    },
  },
});
```

## Combine with Password Auth

```tsx
// Allow both magic link and password
export function SignInForm() {
  const [mode, setMode] = useState<"password" | "magic-link">("password");

  return (
    <div>
      <div>
        <button onClick={() => setMode("password")}>Password</button>
        <button onClick={() => setMode("magic-link")}>Magic Link</button>
      </div>

      {mode === "password" ? (
        <PasswordSignInForm />
      ) : (
        <MagicLinkForm />
      )}
    </div>
  );
}
```

## Verification Page (Optional)

If you want a custom verification page:

```tsx
// app/auth/verify/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export default function VerifyPage() {
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      return;
    }

    authClient.signIn
      .magicLink({ token })
      .then(({ error }) => {
        if (error) {
          setStatus("error");
        } else {
          setStatus("success");
          router.push("/dashboard");
        }
      });
  }, [token, router]);

  if (status === "loading") {
    return <p>Verifying...</p>;
  }

  if (status === "error") {
    return (
      <div>
        <h2>Invalid or expired link</h2>
        <p>Please request a new magic link.</p>
        <a href="/sign-in">Back to sign in</a>
      </div>
    );
  }

  return <p>Redirecting...</p>;
}
```
