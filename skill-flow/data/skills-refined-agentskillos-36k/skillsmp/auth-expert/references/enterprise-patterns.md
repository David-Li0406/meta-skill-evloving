# 🏢 Enterprise Architecture & Scalable Auth

## Modern Infrastructure for Auth
Scaling authentication across a monorepo (Bun or pnpm) requires a modular approach to identity management.

## Monorepo Strategy (Bun/pnpm)
In a monorepo, auth logic should reside in a shared package (e.g., `@repo/auth`) that is consumed by various apps (web, api, mobile).

### Directory Structure
```
packages/
  auth/
    src/
      index.ts        # Exports handlers, session helpers
      config/         # auth.config.ts (Edge safe)
      providers/      # Custom SSO providers
      adapters/       # Shared Prisma/DB adapter logic
apps/
  web/                # Next.js App
  api/                # Bun-based API
```

## Repomix Context Packing
When working with AI-assisted development (like the Gemini CLI), use **Repomix** to pack your authentication context. This allows the model to understand the entire auth flow without reading hundreds of individual files.

### packing Strategy
Pack the following files for the best "Mental Map" for the AI:
- `auth.ts`
- `auth.config.ts`
- `middleware.ts`
- Any custom providers in `lib/auth/`.

## Large Codebase Indexing
For repositories with 1000+ files, standard `grep` is insufficient. Use optimized indexing tools.

### High-Speed Discovery
```bash
# Search for auth patterns using high-performance tools
grep --file=auth-patterns.txt --recursive ./src
git grep "useSession" -- "*.tsx"
```

## Advanced Security: Audit Logging
In enterprise environments, every auth event must be logged with high fidelity.

### Event Schema
| Timestamp | Event Type | User ID | IP Address | User Agent | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-01-22T15:20 | SIGN_IN | user_99 | 1.1.1.1 | Mozilla/5.0 | SUCCESS |

## Unified Caching (Redis/Bun)
Use Bun's high-speed sqlite or a shared Redis instance to store session metadata. This ensures that a user remains logged in even if a specific application instance restarts.

## Implementation Rules
1.  **Strict Typing**: Every auth callback must be fully typed.
2.  **Zero-Trust**: Never trust a user ID from a client-side request; always verify via `auth()`.
3.  **Environment Parity**: Use the same `AUTH_SECRET` strategy across all monorepo apps to allow cross-app session sharing.

*Updated: January 22, 2026 - 15:20*
