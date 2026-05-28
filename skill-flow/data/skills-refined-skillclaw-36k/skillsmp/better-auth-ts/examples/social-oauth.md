# Social OAuth Authentication Examples

## Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    },
    apple: {
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!,
    },
  },
});
```

## Client Sign In

```typescript
// Google
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
});

// GitHub
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
});

// Discord
await authClient.signIn.social({
  provider: "discord",
  callbackURL: "/dashboard",
});
```

## React Social Buttons

```tsx
"use client";

import { authClient } from "@/lib/auth-client";

export function SocialButtons() {
  const handleSocialSignIn = async (provider: string) => {
    await authClient.signIn.social({
      provider: provider as "google" | "github" | "discord",
      callbackURL: "/dashboard",
    });
  };

  return (
    <div className="flex flex-col gap-2">
      <button onClick={() => handleSocialSignIn("google")}>
        Continue with Google
      </button>
      <button onClick={() => handleSocialSignIn("github")}>
        Continue with GitHub
      </button>
      <button onClick={() => handleSocialSignIn("discord")}>
        Continue with Discord
      </button>
    </div>
  );
}
```

## Link Additional Account

```typescript
// Link GitHub to existing account
await authClient.linkSocial({
  provider: "github",
  callbackURL: "/settings/accounts",
});
```

## List Linked Accounts

```typescript
const { data: accounts } = await authClient.listAccounts();

accounts?.forEach((account) => {
  console.log(`${account.provider}: ${account.providerId}`);
});
```

## Unlink Account

```typescript
await authClient.unlinkAccount({
  accountId: "acc_123456",
});
```

## Account Linking Settings Page

```tsx
"use client";

import { useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";

interface Account {
  id: string;
  provider: string;
  providerId: string;
}

export function LinkedAccounts() {
  const [accounts, setAccounts] = useState<Account[]>([]);

  useEffect(() => {
    authClient.listAccounts().then(({ data }) => {
      if (data) setAccounts(data);
    });
  }, []);

  const linkAccount = async (provider: string) => {
    await authClient.linkSocial({
      provider: provider as "google" | "github",
      callbackURL: window.location.href,
    });
  };

  const unlinkAccount = async (accountId: string) => {
    await authClient.unlinkAccount({ accountId });
    setAccounts(accounts.filter((a) => a.id !== accountId));
  };

  const hasProvider = (provider: string) =>
    accounts.some((a) => a.provider === provider);

  return (
    <div>
      <h2>Linked Accounts</h2>

      {/* Google */}
      <div>
        <span>Google</span>
        {hasProvider("google") ? (
          <button onClick={() => {
            const acc = accounts.find((a) => a.provider === "google");
            if (acc) unlinkAccount(acc.id);
          }}>
            Unlink
          </button>
        ) : (
          <button onClick={() => linkAccount("google")}>
            Link
          </button>
        )}
      </div>

      {/* GitHub */}
      <div>
        <span>GitHub</span>
        {hasProvider("github") ? (
          <button onClick={() => {
            const acc = accounts.find((a) => a.provider === "github");
            if (acc) unlinkAccount(acc.id);
          }}>
            Unlink
          </button>
        ) : (
          <button onClick={() => linkAccount("github")}>
            Link
          </button>
        )}
      </div>
    </div>
  );
}
```

## Custom Redirect URI

```typescript
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
      redirectURI: "https://myapp.com/api/auth/callback/github",
    },
  },
});
```

## Request Additional Scopes

```typescript
export const auth = betterAuth({
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      scope: ["email", "profile", "https://www.googleapis.com/auth/calendar.readonly"],
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
      scope: ["user:email", "read:user", "repo"],
    },
  },
});
```

## Access OAuth Tokens

```typescript
// Get stored tokens from account
import { db } from "@/db";

const account = await db.query.account.findFirst({
  where: (account, { and, eq }) =>
    and(eq(account.userId, userId), eq(account.providerId, "github")),
});

if (account?.accessToken) {
  // Use token to call provider API
  const response = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `Bearer ${account.accessToken}`,
    },
  });
}
```

## Auto Link Accounts

```typescript
export const auth = betterAuth({
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github"],
    },
  },
});
```

## Provider Setup Guides

### Google

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → APIs & Services → Credentials
3. Create OAuth 2.0 Client ID
4. Add authorized redirect URI: `https://yourapp.com/api/auth/callback/google`

### GitHub

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. New OAuth App
3. Authorization callback URL: `https://yourapp.com/api/auth/callback/github`

### Discord

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. New Application → OAuth2
3. Add redirect: `https://yourapp.com/api/auth/callback/discord`

## Environment Variables

```env
# Google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Discord
DISCORD_CLIENT_ID=your-discord-client-id
DISCORD_CLIENT_SECRET=your-discord-client-secret
```
