# Modern API Authentication (2026 Standards)

Comprehensive guide to securing API integrations using OIDC, Passkeys, and PKCE.

## 1. OpenID Connect (OIDC) with PKCE

For web applications in 2026, the **Authorization Code Flow with Proof Key for Code Exchange (PKCE)** is the gold standard, even for server-side apps, as it mitigates authorization code injection attacks.

### Standard Implementation (Next.js 16 + Auth.js v5/NextAuth)

```typescript
// auth.config.ts
import type { NextAuthConfig } from 'next-auth';
import Google from 'next-auth/providers/google';

export const authConfig: NextAuthConfig = {
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code",
        },
      },
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
        token.refreshToken = account.refresh_token;
        token.expiresAt = Math.floor(Date.now() / 1000 + (account.expires_in || 0));
      }
      
      // Handle Token Rotation
      if (Date.now() < (token.expiresAt as number) * 1000) {
        return token;
      }
      
      return refreshAccessToken(token);
    },
  },
};
```

## 2. Passkeys (WebAuthn) Integration

Passkeys provide phishing-resistant authentication. When integrating an API that supports Passkeys, use the `navigator.credentials` API.

### Registration Flow Example
```typescript
async function registerPasskey() {
  const options = await api.getRegistrationOptions(); // Server provides challenge
  
  const credential = await navigator.credentials.create({
    publicKey: options
  }) as PublicKeyCredential;

  // Send the credential to your API for verification
  await api.verifyRegistration(credential);
}
```

## 3. Cross-Device Sessions & OIDC
In 2026, many APIs support "Device Flow" or OIDC "Back-Channel Logout" to sync sessions across TV, Mobile, and Web.

### Key Considerations:
- **Token Storage**: Use HTTP-only, Secure, SameSite=Lax/Strict cookies for web.
- **Refresh Token Rotation**: Ensure your OIDC provider rotates refresh tokens on every use to detect theft.
- **OIDC Discovery**: Always use the `.well-known/openid-configuration` endpoint to dynamically load provider metadata.

## 4. API Key Scoping
For machine-to-machine (M2M) communication, prefer short-lived JWTs over long-lived static API keys. If using static keys, implement **Granular Scoping**.

**Bad:** `ADMIN_API_KEY=...` (full access)
**Good:** `READ_ONLY_ANALYTICS_KEY=...` (limited to GET /analytics/*)

## Common Pitfalls
- **Storing Tokens in LocalStorage**: XSS can steal tokens. Use Secure Cookies.
- **Hardcoding Client Secrets**: Always use environment variables and ensure they are NOT prefixed with `NEXT_PUBLIC_` if they are for server-side use.
- **Ignoring PKCE**: Even for server-side flows, PKCE adds a layer of defense-in-depth.

*Updated: January 22, 2026 - 15:18
