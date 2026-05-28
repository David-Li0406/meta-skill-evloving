---
name: bible-lookup-helper
description: Use this skill when you need to fetch Bible verses, validate references, or generate RPC function calls in the KR92 Bible Voice project.
---

# Skill body

## Context Files (Read First)

For schema and API details, read from `Docs/context/`:
- `Docs/context/db-schema-short.md` - Bible schema tables
- `Docs/context/supabase-map.md` - RPC functions list

## Capabilities
- Generate correct RPC function calls for Bible lookups
- Validate OSIS reference formats
- Suggest optimal lookup patterns (verse vs chapter vs range)
- Provide book name aliases and normalization
- Convert between different reference formats
- Retrieve verse study data including Strong's tags
- Perform text searches within the Bible

## Usage Examples

### Example 1: Generate RPC call for single verse
**User:** "How do I fetch John 3:16 in Finnish?"
**Assistant:**
```typescript
const { data } = await supabase.rpc('get_verse_by_ref', {
  p_ref_book: 'John',
  p_chapter: 3,
  p_verse: 16,
  p_version_code: 'finstlk201',
  p_language_code: 'fi'
});
```

### Example 2: Generate RPC call for chapter
**User:** "Get all verses from Genesis chapter 1"
**Assistant:**
```typescript
const { data: verses } = await supabase.rpc('get_chapter_by_ref', {
  p_ref_book: 'Genesis',
  p_chapter: 1,
  p_version_code: 'finstlk201',
  p_language_code: 'fi'
});
```

### Example 3: Validate reference format
**User:** "Is '1. Joh.4:8' a valid reference?"
**Assistant:** Yes, this is valid. It follows the Finnish format for numbered books:
- Book: 1. Johannes (1 John)
- Chapter: 4
- Verse: 8

Alternative valid formats:
- `1 Joh.4:8` (without period after number)
- `1.Joh.4:8` (no space)
- `1 John 4:8` (English)

### Example 4: Convert reference formats
**User:** "Convert 'Joh.3:16' to OSIS format"
**Assistant:** OSIS format: `John.3.16`

Finnish formats accepted:
- `Joh.3:16` (with colon)
- `Joh.3.16` (with period)
- `Johannes 3:16` (full name)

### Example 5: Retrieve verse study data
**User:** "What is the study data for John 3:16?"
**Assistant:**
```typescript
const studyData = await supabase.rpc('get_verse_study_data', {
  p_version_code: 'finstlk201',
  p_book_name: 'John',
  p_chapter: 3,
  p_verse: 16
});
```

### Example 6: Perform text search
**User:** "Search for the word 'love' in the Bible."
**Assistant:**
```typescript
const results = await supabase.rpc('search_text', {
  p_search_term: 'love'
});
```