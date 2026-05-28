# Strong's Lexicon Validation Procedures

Detailed procedures for validating and fixing Strong's concordance data.

## Full Database Audit

### 1. Lexicon Entry Completeness

```sql
-- Find entries missing required fields
SELECT strongs_number, lemma, definition_short
FROM bible_schema.strongs_lexicon
WHERE lemma IS NULL OR lemma = ''
   OR definition_short IS NULL OR definition_short = '';

-- Count entries by language
SELECT
  CASE WHEN strongs_number LIKE 'H%' THEN 'Hebrew' ELSE 'Greek' END as language,
  COUNT(*) as count
FROM bible_schema.strongs_lexicon
GROUP BY 1;
```

Expected: ~8,674 Hebrew (H1-H8674), ~5,624 Greek (G1-G5624)

### 2. Cross-Reference Integrity

```sql
-- Find see_also references that don't exist
WITH all_refs AS (
  SELECT strongs_number, unnest(see_also) as ref
  FROM bible_schema.strongs_lexicon
  WHERE see_also IS NOT NULL AND array_length(see_also, 1) > 0
)
SELECT ar.strongs_number, ar.ref as missing_ref
FROM all_refs ar
LEFT JOIN bible_schema.strongs_lexicon sl ON sl.strongs_number = ar.ref
WHERE sl.strongs_number IS NULL;

-- Find compare references that don't exist
WITH all_refs AS (
  SELECT strongs_number, unnest(compare) as ref
  FROM bible_schema.strongs_lexicon
  WHERE compare IS NOT NULL AND array_length(compare, 1) > 0
)
SELECT ar.strongs_number, ar.ref as missing_ref
FROM all_refs ar
LEFT JOIN bible_schema.strongs_lexicon sl ON sl.strongs_number = ar.ref
WHERE sl.strongs_number IS NULL;
```

### 3. Derivation Field Parsing

```sql
-- Find derivation fields with unparseable references
SELECT strongs_number, derivation
FROM bible_schema.strongs_lexicon
WHERE derivation IS NOT NULL
  AND derivation ~ '[ghGH][0-9]+'
  AND NOT (derivation ~ '\[\[[GH][0-9]+\]\]' OR derivation ~ '\([gh][0-9]+\)');
```

### 4. KJV Word Mapping Integrity

```sql
-- Find verses with no Strong's mappings (should be 0 for complete KJV)
SELECT v.id, vk.osis
FROM bible_schema.verses v
JOIN bible_schema.verse_keys vk ON v.verse_key_id = vk.id
JOIN bible_schema.bible_versions bv ON v.version_id = bv.id
WHERE bv.code = 'KJV'
  AND NOT EXISTS (
    SELECT 1 FROM bible_schema.kjv_strongs_words ksw WHERE ksw.verse_id = v.id
  )
LIMIT 10;

-- Find orphaned kjv_strongs_words (verse_id doesn't exist)
SELECT ksw.verse_id, COUNT(*)
FROM bible_schema.kjv_strongs_words ksw
LEFT JOIN bible_schema.verses v ON ksw.verse_id = v.id
WHERE v.id IS NULL
GROUP BY ksw.verse_id;
```

## Data Quality Checks

### Strong's Number Format Validation

Valid formats:
- `H1` to `H8674` (Hebrew)
- `G1` to `G5624` (Greek)
- No leading zeros in database (normalized)

```sql
-- Find malformed Strong's numbers
SELECT strongs_number
FROM bible_schema.strongs_lexicon
WHERE strongs_number !~ '^[GH][1-9][0-9]*$';

-- Find numbers with leading zeros (should be 0)
SELECT strongs_number
FROM bible_schema.strongs_lexicon
WHERE strongs_number ~ '^[GH]0';
```

### Duplicate Detection

```sql
-- Find duplicate lemmas (potential data issues)
SELECT lemma, array_agg(strongs_number) as numbers, COUNT(*)
FROM bible_schema.strongs_lexicon
WHERE lemma IS NOT NULL
GROUP BY lemma
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 20;
```

## External Validation

### Compare with OpenScriptures Data

To validate against the authoritative source:

1. Download from https://github.com/openscriptures/strongs
2. Parse the Greek/Hebrew JSON/XML files
3. Compare field by field:
   - lemma
   - pronunciation
   - definition
   - derivation references

### Web API Validation

Use Bible SDK API to spot-check entries:

```
GET https://biblesdk.com/api/strongs/G26
```

Compare returned definition with database entry.

## Fix Procedures

### Normalize Strong's Numbers

```sql
-- Fix any with leading zeros (if found)
UPDATE bible_schema.strongs_lexicon
SET strongs_number = regexp_replace(strongs_number, '^([GH])0+', '\1')
WHERE strongs_number ~ '^[GH]0';
```

### Clean Corrupted KJV Entries

```sql
-- Remove punctuation-only entries with invalid Strong's
DELETE FROM bible_schema.kjv_strongs_words
WHERE word_text ~ '^[.,;:?!]$'
  AND strongs_number IS NOT NULL
  AND strongs_number NOT IN (SELECT strongs_number FROM bible_schema.strongs_lexicon);
```

### Fix Cross-Reference Arrays

```sql
-- Normalize cross-references in see_also (remove leading zeros)
UPDATE bible_schema.strongs_lexicon
SET see_also = (
  SELECT array_agg(regexp_replace(ref, '^([GH])0+', '\1'))
  FROM unnest(see_also) as ref
)
WHERE see_also IS NOT NULL
  AND EXISTS (SELECT 1 FROM unnest(see_also) as ref WHERE ref ~ '^[GH]0');
```

## Performance Optimization

### Required Indexes

```sql
-- Essential indexes for Strong's lookups
CREATE INDEX IF NOT EXISTS idx_kjv_strongs_words_strongs_number
ON bible_schema.kjv_strongs_words(strongs_number);

CREATE INDEX IF NOT EXISTS idx_kjv_strongs_words_verse_id
ON bible_schema.kjv_strongs_words(verse_id);

-- Composite for word-level lookups
CREATE INDEX IF NOT EXISTS idx_kjv_strongs_words_verse_word
ON bible_schema.kjv_strongs_words(verse_id, word_order);
```

### Query Optimization

For high-frequency Strong's numbers (G3588, G2532, etc.), consider:
- Pagination for search results
- Caching of common lookups
- Limiting initial result sets

## Monitoring Queries

### Daily Health Check

```sql
-- Quick health check query
SELECT
  (SELECT COUNT(*) FROM bible_schema.strongs_lexicon) as lexicon_count,
  (SELECT COUNT(*) FROM bible_schema.kjv_strongs_words) as kjv_words_count,
  (SELECT COUNT(*) FROM bible_schema.kjv_strongs_words WHERE strongs_number IS NULL) as null_strongs,
  (SELECT COUNT(DISTINCT strongs_number) FROM bible_schema.kjv_strongs_words WHERE strongs_number IS NOT NULL) as unique_strongs;
```

Expected values:
- lexicon_count: ~14,197
- kjv_words_count: ~939,793
- null_strongs: ~636,561 (punctuation and untranslated words)
- unique_strongs: ~8,000-10,000
