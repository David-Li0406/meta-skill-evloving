# Type Inventory - Raamattu Nyt

Complete inventory of TypeScript type sources for Supabase integration.

## Auto-Generated (DO NOT EDIT)

### `apps/raamattu-nyt/src/integrations/supabase/types.ts`

**Source:** `npx supabase gen types typescript --project-id iryqgmjauybluwnqhxbg`

**Contains:**
- `Database` type with `public` schema only
- Tables: app_config, app_settings, audio_assets, audio_cues, bookmarks, highlights, profiles, search_history, summaries, summary_groups, etc.
- Functions: ~40 RPCs in `public` schema (many are wrappers for bible_schema)
- Enums from `public` schema

**Key typed RPCs (use directly, no `as any` needed):**
- `get_chapter_by_ref`, `get_verse_by_ref`, `get_verses_by_ref`
- `get_verse_study_data`, `get_chapter_bundle`
- `get_user_highlights`, `get_user_bookmarks`
- `get_verses_with_tags_and_topics`
- `search_text`, `search_text_extended`
- `get_kjv_verse_with_strongs`

**Regenerate when:**
- New migration applied to database
- New RPC function added to public schema
- Table columns changed

## Manual Types (SAFE TO EDIT)

### `apps/raamattu-nyt/src/integrations/supabase/custom-types.ts`

**Purpose:** Types for entities not in auto-generated types

**Current contents:**
- Admin schema: `TokenImportance`, `ApiToken`, `ApiTokenUpdate`
- Bible schema RPCs: `AIUsageSummary`, `CanUseAIParams`, `CanUseAIResult`, `EffectivePlan`, `TokenBalance`
- Bible schema tables: `AIFeature`, `AIFeatureBinding`, `AIPricing`, `BibleVersion`

**Add here:**
- Types for bible_schema entities
- Types for admin schema entities
- Custom RPC return types
- Extended query result types

### `apps/raamattu-nyt/src/lib/bibleSchemaClient.ts`

**Purpose:** Typed client for bible_schema operations

**Provides:**
- `bibleSchemaRpc<T>()` - Generic typed RPC caller
- `bibleSchemaTable()` - Table query builder
- Pre-typed functions: `getAIUsageSummary()`, `canUseAI()`, `getEffectivePlan()`, `getUserTokenBalance()`, `getAIFeatures()`, `getBibleVersions()`

## Usage Patterns

### Public schema RPCs (typed in types.ts)

```typescript
// ✅ CORRECT - Use directly, it's already typed!
const { data, error } = await supabase.rpc('get_user_highlights', {
  p_user_id: userId
});

// ❌ WRONG - Unnecessary `as any`
const { data, error } = await (supabase as any).rpc('get_user_highlights', {...});
```

### Bible schema RPCs (typed in custom-types.ts)

```typescript
// ✅ CORRECT - Use bibleSchemaClient
import { getAIUsageSummary, bibleSchemaRpc } from '@/lib/bibleSchemaClient';

// Pre-typed function
const { data } = await getAIUsageSummary();

// Or generic with type parameter
const { data } = await bibleSchemaRpc<CustomType>('custom_function', params);
```

### Bible schema tables

```typescript
// ✅ CORRECT - Use bibleSchemaTable
import { bibleSchemaTable } from '@/lib/bibleSchemaClient';

const { data } = await bibleSchemaTable('ai_features')
  .select('*')
  .eq('is_active', true);
```

## Schema-Specific Access

| Schema | In types.ts? | Access Method |
|--------|--------------|---------------|
| `public` | YES | `supabase.from()`, `supabase.rpc()` |
| `bible_schema` | NO | `bibleSchemaClient` functions |
| `notifications` | NO | `bibleSchemaRpc()` or REST with header |
| `admin` | NO | Service role only |
| `feedback` | NO | RPC wrappers in public |

## Import Paths

```typescript
// Auto-generated types
import type { Database } from '@/integrations/supabase/types';

// Custom types
import type {
  ApiToken,
  AIUsageSummary,
  AIFeature
} from '@/integrations/supabase/custom-types';

// Bible schema client
import {
  bibleSchemaRpc,
  bibleSchemaTable,
  getAIUsageSummary
} from '@/lib/bibleSchemaClient';

// Supabase client (typed with Database)
import { supabase } from '@/integrations/supabase/client';
```

## Type Helpers

### Extract table types

```typescript
import type { Database } from '@/integrations/supabase/types';

type Tables = Database['public']['Tables'];
type Highlights = Tables['highlights']['Row'];
type HighlightInsert = Tables['highlights']['Insert'];
```

### Extract function types

```typescript
type Functions = Database['public']['Functions'];
type GetUserHighlightsReturn = Functions['get_user_highlights']['Returns'];
```
