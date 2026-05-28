# RPC Type Map

Manual type definitions for RPC functions not in auto-generated types.

## Public Schema RPCs (in types.ts)

These are already typed in the generated types.ts:

| Function | Returns |
|----------|---------|
| `get_user_highlights(uuid)` | highlights with verse info |
| `get_user_unique_tags(uuid)` | tag, usage_count |
| `save_bookmark(...)` | void |
| `get_user_bookmarks(uuid, int)` | bookmarks |
| `search_text(text, text, int)` | verses |
| `get_verses_with_tags_and_topics(...)` | verses with tags, topics, notes |

## Bible Schema RPCs (need manual types)

### get_verse_study_data

```typescript
interface GetVerseStudyDataParams {
  p_osis: string;
  p_version_code?: string;
}

interface VerseStudyData {
  verse_id: string;
  text_content: string;
  book_name: string;
  chapter_number: number;
  verse_number: number;
  strongs_data?: StrongsWord[];
}
```

### get_chapter_bundle

```typescript
interface GetChapterBundleParams {
  p_book: string;
  p_chapter: number;
  p_version_code?: string;
}

interface ChapterBundle {
  verses: BundleVerse[];
  audio?: AudioAsset;
  highlights?: HighlightData[];
}
```

### get_kjv_verses_tagged

```typescript
interface GetKjvVersesTaggedParams {
  p_osis_refs: string[];
}

interface KjvTaggedVerse {
  osis: string;
  plain_text: string;
  tagged_text: string;
}
```

## Subscription RPCs (bible_schema)

### get_effective_plan

```typescript
interface GetEffectivePlanReturn {
  plan_id: string;
  plan_name: string;
  token_quota: number;
  window_hours: number;
}
```

### can_use_ai

```typescript
interface CanUseAiParams {
  p_user_id: string;
  p_operation: string;
  p_tokens: number;
}

// Returns boolean
```

### get_user_token_balance

```typescript
// Returns number (remaining tokens)
```

## Usage Pattern

```typescript
// In your hook or service file:
import { supabase } from '@/integrations/supabase/client';
import type { VerseStudyData } from '@/integrations/supabase/custom-types';

async function getVerseStudy(osis: string): Promise<VerseStudyData | null> {
  const { data, error } = await (supabase.rpc as any)('get_verse_study_data', {
    p_osis: osis,
  }) as { data: VerseStudyData | null; error: Error | null };

  if (error) throw error;
  return data;
}
```

## Adding New RPC Types

When a new RPC is added:

1. Check if it's in `public` schema → regenerate types.ts
2. If in other schema → add to custom-types.ts:

```typescript
// custom-types.ts

export interface NewRpcParams {
  p_param1: string;
  p_param2?: number;
}

export interface NewRpcReturn {
  field1: string;
  field2: number;
}
```
