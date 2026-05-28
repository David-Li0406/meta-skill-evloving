# Monorepo Architecture Details

## Table of Contents
- [Shell Frontend](#shell-frontend)
- [Apps Structure](#apps-structure)
- [Packages Architecture](#packages-architecture)
- [Supabase Backend](#supabase-backend)
- [Path Alias Configuration](#path-alias-configuration)
- [Security Model](#security-model)

## Shell Frontend

The root `src/` directory contains a minimal shell frontend required for Lovable Cloud deployment.

```
src/
├── App.tsx           # Thin wrapper delegating to apps/raamattu-nyt
├── main.tsx          # Entry point
├── index.css         # Root styles
└── integrations/     # Supabase client configuration
    └── supabase/
        ├── client.ts
        └── types.ts
```

**Key Points:**
- Lovable Cloud requires root-level entry point
- Shell delegates to main app immediately
- Supabase client configured here, shared by apps
- Minimal code - avoid putting logic here

## Apps Structure

### raamattu-nyt (Main App)
```
apps/raamattu-nyt/
├── src/
│   ├── components/     # UI components
│   ├── hooks/          # App-specific hooks
│   ├── pages/          # Route pages
│   ├── integrations/   # External service clients
│   └── lib/            # Utilities
├── vite.config.ts      # Build config with aliases
├── tsconfig.json       # TypeScript paths
├── tailwind.config.ts  # Tailwind config
└── package.json        # Dependencies
```

### idea-machina (Secondary App)
Smaller AI prompt management tool. Same structure pattern.

## Packages Architecture

### Package Naming Convention
- NPM scope: `@raamattu-nyt/`
- Directory: `packages/<name>/`
- Import alias: `@<name>/` or `@shared-<name>/`

### Standard Package Structure
```
packages/my-package/
├── src/
│   ├── index.ts        # Main exports
│   ├── hooks/          # React hooks
│   ├── components/     # React components (if any)
│   ├── utils/          # Utilities
│   └── types.ts        # TypeScript types
└── package.json
```

### Package.json Template
```json
{
  "name": "@raamattu-nyt/package-name",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./*": "./src/*"
  }
}
```

### Current Packages

| Package | Alias | Purpose |
|---------|-------|---------|
| `@raamattu-nyt/ai` | `@ai` | AI integration, prompts, usage logging |
| `@raamattu-nyt/shared-auth` | `@shared-auth` | Authentication hooks, user management |
| `@raamattu-nyt/shared-content` | `@shared-content` | Bible content, RPCs, search |
| `@raamattu-nyt/shared-history` | `@shared-history` | Reading history, bookmarks |
| `@raamattu-nyt/shared-voice` | `@shared-voice` | Audio Bible, TTS |
| `@raamattu-nyt/ui` | `@ui` | Shared shadcn/ui components |

## Supabase Backend

Single Supabase project backing all apps.

```
supabase/
├── functions/          # Edge Functions
│   ├── _shared/       # Shared modules
│   ├── ai-orchestrator/
│   └── translate-search-term/
├── migrations/         # Database schema
└── config.toml         # Local config
```

### Database Schemas
- `public` - User data, app settings, auth extensions
- `bible_schema` - Bible text, AI features, topics
- `feedback` - User feedback system

### Edge Functions
All AI calls route through Edge Functions for:
- Cost tracking
- Rate limiting
- Provider abstraction
- Logging

## Path Alias Configuration

### Vite Config (apps/raamattu-nyt/vite.config.ts)
```typescript
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@shared-auth": path.resolve(__dirname, "../../packages/shared-auth/src"),
      "@shared-content": path.resolve(__dirname, "../../packages/shared-content/src"),
      "@shared-history": path.resolve(__dirname, "../../packages/shared-history/src"),
      "@shared-voice": path.resolve(__dirname, "../../packages/shared-voice/src"),
      "@ai": path.resolve(__dirname, "../../packages/ai/src"),
      "@ui": path.resolve(__dirname, "../../packages/ui/src"),
    },
  },
});
```

### TypeScript Config (apps/raamattu-nyt/tsconfig.json)
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@shared-auth/*": ["../../packages/shared-auth/src/*"],
      "@shared-content/*": ["../../packages/shared-content/src/*"],
      "@ui/*": ["../../packages/ui/src/*"]
    }
  }
}
```

## Security Model

### Row Level Security (RLS)
All tables have RLS enabled. Common patterns:

```sql
-- User can only access own data
CREATE POLICY "Users can view own data"
ON table_name FOR SELECT
USING (user_id = auth.uid());

-- Public read, authenticated write
CREATE POLICY "Public read"
ON table_name FOR SELECT
USING (true);

CREATE POLICY "Authenticated insert"
ON table_name FOR INSERT
WITH CHECK (auth.uid() IS NOT NULL);
```

### API Security
- Never expose service role key in frontend
- Use RPC functions instead of direct table access
- Edge Functions validate JWT before operations
- AI usage tracked in `ai_usage_logs`

### Environment Variables
```
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
# Never commit service role key
```
