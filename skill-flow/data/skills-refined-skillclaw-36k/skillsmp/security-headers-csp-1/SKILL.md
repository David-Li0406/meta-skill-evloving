---
name: security-headers-csp
description: Guide for CSP, security headers, and external scripts. Use fetchWithHmac for APIs, safeFetch for external services.
---

# Security Headers & CSP Skill

## Purpose

Guide for managing Content Security Policy (CSP), security headers, and safe external script loading.

## CSP Policy Overview

This project uses a **relaxed CSP policy with host allowlisting**:

- Allows `'unsafe-inline'` for inline scripts and JSON-LD
- Enables ISR/PPR caching (strict CSP would break this)
- Security maintained through explicit host allowlisting
- **No nonce required** for scripts

## Allowlisted Domains

The following domains are trusted in `script-src` and `script-src-elem`:

| Domain                              | Purpose               |
| ----------------------------------- | --------------------- |
| `googletagmanager.com`              | Google Tag Manager    |
| `google-analytics.com`              | Google Analytics      |
| `googlesyndication.com`             | Google Ads            |
| `googleadservices.com`              | Google Ads conversion |
| `fundingchoicesmessages.google.com` | Google consent        |
| `www.gstatic.com`                   | Google static assets  |
| `tpc.googlesyndication.com`         | Ad personalization    |

## Adding External Scripts

### Using Next.js Script Component

```tsx
import Script from "next/script";

// ✅ CORRECT - afterInteractive for most scripts
<Script
  src="https://example.com/script.js"
  strategy="afterInteractive"
/>

// ✅ CORRECT - lazyOnload for non-critical analytics
<Script
  src="https://www.googletagmanager.com/gtag/js?id=GA_ID"
  strategy="lazyOnload"
/>
```

### Strategy Selection

| Strategy            | When to Use                                   |
| ------------------- | --------------------------------------------- |
| `afterInteractive`  | Default for most scripts                      |
| `lazyOnload`        | Non-critical analytics, helps Core Web Vitals |
| `beforeInteractive` | Critical scripts (rarely needed)              |

### No Nonce Required

Due to relaxed CSP, scripts work without nonce props:

```tsx
// ✅ CORRECT - No nonce needed
<Script src="https://trusted.com/script.js" strategy="afterInteractive" />

// ❌ UNNECESSARY - Don't add nonce
<Script src="https://trusted.com/script.js" nonce={nonce} />
```

## JSON-LD Implementation

JSON-LD is rendered server-side via `JsonLdServer` component:

```tsx
import { JsonLdServer } from "@components/partials/JsonLdServer";

// ✅ CORRECT - Server-rendered, no nonce needed
<JsonLdServer data={structuredData} />;
```

The component:

- Escapes `</script>` and `<` to prevent XSS
- Data comes from server-side API responses
- No nonce required due to relaxed CSP

## Security Headers (proxy.ts)

The proxy middleware (`proxy.ts`) injects these headers:

```typescript
// Key security headers
"X-Content-Type-Options": "nosniff"
"X-Frame-Options": "DENY"
"X-XSS-Protection": "1; mode=block"  // Deprecated but harmless - see note below
"Referrer-Policy": "strict-origin-when-cross-origin"
"Permissions-Policy": "camera=(), microphone=(), geolocation=(self)"
```

> **Note**: `X-XSS-Protection` is deprecated. Chrome removed XSS Auditor in 2019, and modern browsers ignore this header. It's kept for legacy browser compatibility but provides no security benefit in current browsers. The real XSS protection comes from CSP and proper output escaping.

## Adding New External Domains

If you need to add a new external service:

1. **Evaluate necessity** - Is it really needed?

2. **Add to CSP in proxy.ts**:

   ```typescript
   // Find the CSP construction in proxy.ts
   const csp = [
     // ... existing directives
     `script-src 'self' 'unsafe-inline' https://newdomain.com`,
   ].join("; ");
   ```

3. **Document the purpose** in this skill file

4. **Test in development** before deploying

## HMAC Security for APIs

All internal API calls use HMAC signing:

```typescript
import { fetchWithHmac } from "@lib/api/fetch-wrapper";

// ✅ CORRECT - Uses HMAC signing with timeout
const data = await fetchWithHmac("/api/events");

// ❌ WRONG - Raw fetch without security
const data = await fetch("/api/events");
```

The `fetchWithHmac` function:

- Signs requests with HMAC
- Has built-in 10s timeout
- Validates responses

## Safe Fetch Patterns

For external webhooks/services, use safe fetch utilities:

```typescript
import { safeFetch, fireAndForgetFetch } from "@utils/safe-fetch";

// ✅ For external services with response handling
const result = await safeFetch("https://webhook.example.com/notify", {
  method: "POST",
  body: JSON.stringify(data),
});

// ✅ For fire-and-forget notifications
await fireAndForgetFetch("https://webhook.example.com/ping");
```

Features:

- 5s default timeout
- Response validation
- Sentry error logging
- Never hangs in serverless

## Rationale for Relaxed CSP

For a cultural events site with:

- HMAC-protected backend
- No user-generated content in scripts
- Need for ISR/PPR caching

Relaxed CSP enables better performance while maintaining security through host allowlisting.

## Checklist for Security Changes

- [ ] Adding new external script? → Add domain to CSP
- [ ] Using Script component? → Choose correct strategy
- [ ] Making API calls? → Use `fetchWithHmac`
- [ ] External webhooks? → Use `safeFetch` or `fireAndForgetFetch`
- [ ] JSON-LD data? → Use `JsonLdServer` component
- [ ] New security header? → Add to `proxy.ts`

## Files to Reference

- [proxy.ts](../../../proxy.ts) - CSP and security headers
- [lib/api/fetch-wrapper.ts](../../../lib/api/fetch-wrapper.ts) - `fetchWithHmac`
- [utils/safe-fetch.ts](../../../utils/safe-fetch.ts) - Safe fetch utilities
- [components/partials/JsonLdServer.tsx](../../../components/partials/JsonLdServer.tsx) - JSON-LD component
- [app/GoogleScripts.tsx](../../../app/GoogleScripts.tsx) - Analytics script loading
