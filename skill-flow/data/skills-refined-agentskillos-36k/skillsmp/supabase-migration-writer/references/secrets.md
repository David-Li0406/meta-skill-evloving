# Supabase Secrets Reference

## Current Secrets

| Secret Name | Purpose | Used By |
|------------|---------|---------|
| `ANTHROPIC_API_KEY` | Claude AI API access | ai-orchestrator, translate-search-term |
| `ANTHROPIC_MODEL` | Default Anthropic model | ai-orchestrator |
| `ELEVENLABS_API_KEY` | Text-to-speech audio generation | generate-audio, get-elevenlabs-usage |
| `LOVABLE_API_KEY` | Lovable Cloud deployment | Build system |
| `OPENAI_API_KEY` | OpenAI embeddings and fallback | embed, ai-orchestrator |
| `OPENAI_MODEL` | Default OpenAI model | embed |
| `OPENROUTER_API_KEY` | OpenRouter multi-model access | ai-orchestrator |
| `RESEND_API_KEY` | Email delivery service | send-notifications |
| `SUPABASE_ANON_KEY` | Public API access | Client apps |
| `SUPABASE_DB_URL` | Direct database connection | Edge Functions |
| `SUPABASE_SERVICE_ROLE_KEY` | Admin API access | Edge Functions (server-side) |
| `SUPABASE_URL` | Supabase project URL | All services |

## Accessing Secrets in Edge Functions

```typescript
// In Edge Function
const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
const supabaseUrl = Deno.env.get("SUPABASE_URL");
```

## Managing Secrets

### List secrets (CLI)
```bash
npx supabase secrets list --project-ref iryqgmjauybluwnqhxbg
```

### Set a secret (CLI)
```bash
npx supabase secrets set SECRET_NAME=value --project-ref iryqgmjauybluwnqhxbg
```

### Via Dashboard
1. Go to Supabase Dashboard > Project Settings > Edge Functions
2. Click "Manage secrets"
3. Add or update secrets

## Security Notes

- Never commit secrets to version control
- Use `SUPABASE_SERVICE_ROLE_KEY` only in Edge Functions (server-side)
- `SUPABASE_ANON_KEY` is safe for client-side use
- Rotate API keys periodically (check api_tokens table for deadlines)
