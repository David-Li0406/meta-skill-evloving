---
name: edge-function-generator
description: Use this skill when creating and maintaining Supabase Edge Functions, including setting up CORS, integrating shared modules, adding JWT validation, and configuring environment variables.
---

# Edge Function Generator

## Capabilities
- Scaffold new Edge Functions with proper structure
- Set up CORS headers and error handling
- Integrate shared modules from `_shared/`
- Add JWT validation and logging
- Configure environment variables
- Audit or update dependency versions across functions

## Edge Function Structure

### Location
```
supabase/functions/
├── _shared/              # Shared modules
│   ├── deps.ts           # Centralized dependencies
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
// supabase/functions/verse-of-the-day/index.ts

import { serve } from "../_shared/deps.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" }, status: 500 }
    );
  }
});
```

### Example 2: Edge Function with JWT Authentication
```typescript
// Get user from JWT
const authHeader = req.headers.get("Authorization");
if (!authHeader) {
  return new Response('Unauthorized', { status: 401 });
}

// Your logic for authenticated requests
```