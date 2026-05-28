# Edge Function Dependency Versions

## Canonical Versions (Updated: 2026-01)

Use these versions for all new Edge Functions and when updating existing ones:

```typescript
// Deno Standard Library
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import { crypto } from "https://deno.land/std@0.190.0/crypto/mod.ts";

// Supabase Client
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";

// XHR Polyfill (for AI SDKs)
import "https://deno.land/x/xhr@0.1.0/mod.ts";
```

## Version Selection Rationale

| Package | Version | Why |
|---------|---------|-----|
| `deno.land/std` | `0.190.0` | Latest stable with Supabase Edge Runtime compatibility |
| `@supabase/supabase-js` | `2.49.1` | Latest 2.x with full TypeScript types |
| `xhr` | `0.1.0` | Only version, required for OpenAI/Anthropic SDKs |

## Detecting Version Drift

Run this grep to audit current versions:

```bash
# Find all import versions in Edge Functions
grep -r "from \"https://" supabase/functions/ | grep -E "@[0-9]" | sort -u
```

## When to Update Versions

1. **New Edge Function**: Always use canonical versions above
2. **Modifying existing function**: Update imports if touching the file
3. **Quarterly audit**: Check for security updates in dependencies
4. **After Supabase CLI update**: Verify runtime compatibility

## Version Compatibility Matrix

| Supabase CLI | Edge Runtime | Deno std | supabase-js |
|--------------|--------------|----------|-------------|
| 2.0+ | Deno 2.x | 0.190.0+ | 2.49.x |
| 1.x | Deno 1.x | 0.168.0 | 2.39.x |

## Import Map Alternative (deno.json)

For functions with many dependencies, use `deno.json`:

```json
{
  "imports": {
    "@supabase/supabase-js": "https://esm.sh/@supabase/supabase-js@2.49.1",
    "std/http": "https://deno.land/std@0.190.0/http/server.ts"
  }
}
```

Then import as:
```typescript
import { serve } from "std/http";
import { createClient } from "@supabase/supabase-js";
```
