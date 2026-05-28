---
name: edge-function-generator
description: Use this skill when creating and maintaining Supabase Edge Functions, including setting up CORS, integrating shared modules, adding JWT validation, configuring environment variables, and auditing dependency versions.
---

# Edge Function Generator

## Capabilities
- Scaffold new Edge Functions with proper structure
- Set up CORS headers and error handling
- Integrate shared modules from `_shared/`
- Add JWT validation and logging
- Configure environment variables
- Audit and update dependency versions across functions

## Edge Function Structure

### Location
```
supabase/functions/
├── _shared/              # Shared modules (import with ../_shared/)
│   ├── deps.ts           # Centralized dependencies - import from here!
│   ├── ai-config.ts
│   ├── ai-prompt.ts
│   ├── ai-providers.ts
│   └── ai-quota.ts
├── function-name/
│   └── index.ts
```

### Deployment
- Lovable Cloud: Auto-deploy on save
- Manual: `supabase functions deploy function-name`

## Usage Examples

### Example 1: Create Basic Edge Function
**User:** "Create a new edge function to get verse of the day"

**Assistant:**
```typescript
import { serve } from "../_shared/deps.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
```

### Example 2: Edge Function with JWT Authentication
**User:** "Create edge function for user to save custom bookmark with note"

**Assistant:**
```typescript
import { serve } from "../_shared/deps.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      throw new Error('Missing authorization header');
    }

    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
```

### Example 3: Edge Function with AI Integration
**User:** "Create edge function for AI-powered verse explanation"

**Assistant:**
```typescript
import { serve } from "../_shared/deps.ts";
import { getFeatureConfig } from "../_shared/ai-config.ts";
import { getPrompt } from "../_shared/ai-prompt.ts";
import { callProvider } from "../_shared/ai-providers.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
```

## Common Patterns

### CORS Headers
Always include for client access:
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
```

### Error Handling
```typescript
try {
  // Logic
} catch (error) {
  console.error('Error:', error);
  return new Response(
    JSON.stringify({ success: false, error: error.message }),
    { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
  );
}
```

### Supabase Client
```typescript
const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const supabase = createClient(supabaseUrl, supabaseKey);
```

### Environment Variables
```typescript
const apiKey = Deno.env.get('EXTERNAL_API_KEY');
if (!apiKey) {
  throw new Error('Missing API key configuration');
}
```

## Version Audit Workflow
When auditing for stray direct imports:
```bash
grep -r "deno.land/std@" supabase/functions/ | grep -v deps.ts
grep -r "esm.sh/@supabase" supabase/functions/ | grep -v deps.ts
```

## Testing Edge Functions

### cURL Test
```bash
curl -X POST https://project.supabase.co/functions/v1/function-name \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### TypeScript Test
```typescript
const { data, error } = await supabase.functions.invoke('function-name', {
  body: { key: 'value' }
});
```

## Related Documentation
- See `Docs/02-DESIGN.md` for Edge Functions overview
- See `Docs/06-AI-ARCHITECTURE.md` for AI integration patterns