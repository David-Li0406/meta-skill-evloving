# Database Schema Reference

## Schemas

| Schema | Purpose | Tables |
|--------|---------|--------|
| `public` | User data, application tables | profiles, highlights, bookmarks, summaries, etc. |
| `bible_schema` | Bible text, AI system, topics | verses, books, chapters, ai_*, topical_*, etc. |
| `feedback` | User feedback system | targets, user_feedbacks, aggregates |
| `auth` | Supabase auth (managed) | users, sessions, etc. |
| `storage` | Supabase storage (managed) | buckets, objects |

## Core Tables by Schema

### public

| Table | Purpose | RLS |
|-------|---------|-----|
| `profiles` | User profiles, preferences | Yes |
| `highlights` | Verse highlights | Yes |
| `bookmarks` | Verse/chapter bookmarks | Yes |
| `summaries` | User study summaries | Yes |
| `user_reading_history` | Reading progress | Yes |
| `search_history` | Search queries | Yes |
| `audio_assets` | Audio file metadata | Yes |
| `audio_cues` | Verse timing in audio | Yes |
| `user_roles` | Admin/moderator roles | Yes |
| `app_settings` | Application config | Yes |

### bible_schema

| Table | Purpose | RLS |
|-------|---------|-----|
| `bible_versions` | Bible translations (KR92, KJV, etc.) | Yes |
| `books` | Bible books | Yes |
| `chapters` | Chapters per book | Yes |
| `verses` | Verse text with FTS | Yes |
| `verse_keys` | OSIS reference mapping | Yes |
| `topical_topics` | Topical Bible topics | Yes |
| `topical_references` | Topic-verse links | Yes |
| `ai_usage_logs` | AI call tracking | Yes |
| `ai_plan_quotas` | Quota per plan/feature | Yes |
| `ai_features` | Available AI features | Yes |
| `ai_feature_bindings` | Feature-model mapping | Yes |
| `ai_prompt_templates` | AI prompt management | Yes |
| `api_tokens` | API token metadata | Yes |

### feedback

| Table | Purpose | RLS |
|-------|---------|-----|
| `targets` | Feedback target entities | Yes |
| `user_feedbacks` | Individual feedback | Yes |
| `aggregates` | Aggregated scores | Yes |

## Common Data Types

```sql
-- IDs
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id UUID REFERENCES auth.users(id)

-- Timestamps
created_at TIMESTAMPTZ DEFAULT now()
updated_at TIMESTAMPTZ DEFAULT now()

-- Enums (defined as CHECK constraints)
status TEXT CHECK (status IN ('draft', 'published', 'archived'))

-- Arrays
tags TEXT[] DEFAULT '{}'

-- JSON
metadata JSONB DEFAULT '{}'
```

## Key Foreign Key Relationships

```
auth.users.id
  ├── public.profiles.user_id
  ├── public.highlights.user_id
  ├── public.bookmarks.user_id
  ├── public.summaries.user_id
  └── public.user_roles.user_id

bible_schema.bible_versions.id
  ├── bible_schema.books.version_id
  ├── bible_schema.chapters.version_id
  └── bible_schema.verses.version_id

bible_schema.books.id
  └── bible_schema.chapters.book_id

bible_schema.chapters.id
  └── bible_schema.verses.chapter_id

bible_schema.verses.id
  ├── public.highlights.verse_id
  ├── public.bookmarks.verse_id
  └── public.audio_cues.verse_id
```

## Useful RPC Functions

```sql
-- Get user's plan for quota checking
get_user_plan(p_user_id UUID) RETURNS TEXT

-- Check quota availability
check_ai_quota(p_user_id UUID, p_feature TEXT) RETURNS JSON

-- Consume quota tokens
consume_ai_quota(p_user_id UUID, p_feature TEXT, p_tokens INT) RETURNS VOID

-- Get verse by OSIS reference
get_verse_by_osis(p_osis TEXT, p_version_code TEXT) RETURNS SETOF verses
```
