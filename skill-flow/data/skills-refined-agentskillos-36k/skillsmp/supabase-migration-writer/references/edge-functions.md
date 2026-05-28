# Edge Functions Reference

## Active Edge Functions

| Function | JWT Required | Purpose |
|----------|-------------|---------|
| `ai-orchestrator` | Yes | Central AI feature dispatcher |
| `embed` | No | Generate OpenAI embeddings |
| `generate-audio` | Yes | ElevenLabs TTS generation |
| `get-elevenlabs-usage` | No | ElevenLabs usage stats |
| `manage-notification-types` | No | Notification type CRUD |
| `regenerate-audio-cues` | No | Rebuild audio cue timing |
| `send-notifications` | No | Send emails via Resend |
| `topic-translations` | Yes | AI topic translation |
| `translate-search-term` | No | Finnish-English term translation |

## Directory Structure

```
supabase/functions/
├── _shared/              # Shared modules
│   ├── ai-quota.ts       # Quota checking helpers
│   ├── cors.ts           # CORS headers
│   └── supabase.ts       # Client initialization
├── ai-orchestrator/
│   └── index.ts
├── embed/
│   └── index.ts
├── generate-audio/
│   └── index.ts
└── ...
```

## Configuration

Edge Function settings are in `supabase/config.toml`:

```toml
[functions.embed]
verify_jwt = false

[functions.generate-audio]
verify_jwt = true
```

## Creating New Edge Functions

1. Create directory: `supabase/functions/<function-name>/`
2. Add `index.ts` with Deno.serve handler
3. Configure JWT in `config.toml`
4. Deploy via Lovable Cloud (auto) or `npx supabase functions deploy`

## Edge Function Template

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { corsHeaders } from "../_shared/cors.ts";

Deno.serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { param } = await req.json();

    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
```

## Shared Modules

Import from `_shared/`:
```typescript
import { corsHeaders } from "../_shared/cors.ts";
import { createClient } from "../_shared/supabase.ts";
import { checkQuota, consumeQuota } from "../_shared/ai-quota.ts";
```
