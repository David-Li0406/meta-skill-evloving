# Common Tech Stacks

Detection patterns for common web technology stacks.

## Framework Detection

| Framework | Detection Method | Confidence |
|-----------|------------------|------------|
| **Next.js** | `/_next/` in paths, `__NEXT_DATA__` global | high |
| **Nuxt** | `/_nuxt/` in paths, `__NUXT__` global | high |
| **Remix** | `/__remix` paths, data attributes | high |
| **Astro** | `astro` in script names | medium |
| **SvelteKit** | `_app` patterns, svelte attributes | medium |
| **Gatsby** | `/static/` patterns, gatsby globals | medium |

### Next.js Version Detection

```javascript
// Check __NEXT_DATA__ for version hints
typeof __NEXT_DATA__ !== 'undefined' && __NEXT_DATA__.buildId

// Turbopack indicator (Next.js 13+)
document.querySelector('script[src*="turbopack"]')

// App Router vs Pages Router
// App Router: RSC, streaming
// Pages Router: _next/data patterns
```

## Styling Detection

| System | Detection Method |
|--------|------------------|
| **Tailwind** | utility classes (`flex`, `pt-4`, `text-sm`) |
| **SASS/SCSS** | `.scss` in source maps, BEM-like classes |
| **CSS Modules** | hashed class names (`_component_abc123`) |
| **styled-components** | `sc-` prefixed classes |
| **Emotion** | `css-` prefixed classes |
| **CSS-in-JS** | inline style attributes, emotion/styled markers |

### Tailwind Version Hints

- v3: JIT mode, arbitrary values `[color:red]`
- v4: CSS-first config, `@theme` directive

## Hosting Detection

| Platform | Detection Method |
|----------|------------------|
| **Vercel** | `vercel` in headers, `.vercel.app` domain |
| **Netlify** | `netlify` in headers, `.netlify.app` domain |
| **Cloudflare** | `cf-` headers, `.pages.dev` domain |
| **AWS** | `x-amz-` headers, CloudFront patterns |
| **Railway** | `.up.railway.app` domain |
| **Render** | `.onrender.com` domain |

## CMS Detection

| CMS | Detection Method |
|-----|------------------|
| **Contentful** | `contentful` in API calls, `ctf` markers |
| **Sanity** | `sanity.io` API calls, GROQ queries |
| **Strapi** | `/api/` patterns, strapi markers |
| **WordPress** | `/wp-` paths, REST API |
| **Ghost** | `/ghost/` paths, ghost API |
| **Notion** | notion API calls |

## Auth Detection

| Provider | Detection Method |
|----------|------------------|
| **Clerk** | `clerk` in scripts, `__clerk` globals |
| **Auth0** | `auth0` in scripts |
| **NextAuth** | `/api/auth/` endpoints |
| **Supabase** | `supabase` in scripts |
| **Firebase** | `firebase` patterns |

## Database/Backend Hints

| Service | Detection Method |
|---------|------------------|
| **Convex** | `convex.cloud` API calls |
| **Supabase** | `supabase.co` API calls |
| **PlanetScale** | indirect (MySQL patterns) |
| **Prisma** | indirect (API patterns) |

## Analytics Detection

| Service | Detection Method |
|---------|------------------|
| **Vercel Analytics** | `_vercel` scripts |
| **Google Analytics** | `gtag`, `ga`, `analytics.js` |
| **Plausible** | `plausible.io` scripts |
| **Fathom** | `usefathom.com` scripts |
| **PostHog** | `posthog` scripts |
| **Amplitude** | `amplitude` scripts |

## Font Detection

```javascript
// Get computed fonts
getComputedStyle(document.body).fontFamily

// Check for web font loading
document.fonts.ready.then(() => {
  console.log([...document.fonts].map(f => f.family))
})

// Common font services
// - Google Fonts: fonts.googleapis.com
// - Adobe Fonts: use.typekit.net
// - Custom: direct .woff2 loading
```

## Quick Detection Script

```javascript
// Run in browser console or via agent-browser eval
const detect = {
  nextjs: typeof __NEXT_DATA__ !== 'undefined',
  nuxt: typeof __NUXT__ !== 'undefined',
  react: !!document.querySelector('[data-reactroot]') || typeof React !== 'undefined',
  vue: !!document.querySelector('[data-v-]'),
  tailwind: !!document.querySelector('[class*="flex"]'),
  vercel: document.cookie.includes('__vercel'),
}
console.log(detect)
```
