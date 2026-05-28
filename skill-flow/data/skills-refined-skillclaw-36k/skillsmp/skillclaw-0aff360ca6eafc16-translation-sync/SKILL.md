---
name: translation-sync
description: Use this skill when managing Finnish/English content translations in the KR92 Bible Voice project, including syncing translations, validating completeness, and handling CSV imports/exports.
---

# Skill body

## Capabilities
- Sync topic translations between Finnish and English
- Manage term translation cache
- Validate translation completeness
- Export/import CSV for bulk updates
- Identify missing translations

## Translation Tables

### term_translations (bible_schema)
Caches Finnish ↔ English term translations for search:
```sql
term_fi TEXT
main_term_en TEXT
synonyms_en TEXT[]
ai_main_term_en TEXT
ai_synonyms_en TEXT[]
source TEXT -- 'topic', 'ai', 'manual'
```

### topical_topics (bible_schema)
Topic names in both languages:
```sql
slug TEXT -- English slug
name_en TEXT -- English name
name_fi TEXT -- Finnish name (can be null)
slug_fi TEXT -- Finnish slug (can be null)
is_core BOOLEAN
```

## Usage Examples

### Example 1: Find Missing Topic Translations
**User:** "Find all topics that don't have Finnish translations"

**Assistant:**
```sql
-- Find topics without Finnish translation
SELECT
  id,
  slug,
  name_en,
  name_fi,
  slug_fi,
  CASE
    WHEN name_fi IS NULL AND slug_fi IS NULL THEN 'Both missing'
    WHEN name_fi IS NULL THEN 'Name missing'
    WHEN slug_fi IS NULL THEN 'Slug missing'
  END AS missing_fields
FROM bible_schema.topical_topics
WHERE name_fi IS NULL OR slug_fi IS NULL
ORDER BY is_core DESC, name_en;

-- Count statistics
SELECT
  COUNT(*) as total_topics,
  COUNT(name_fi) as translated_topics,
  COUNT(*) - COUNT(name_fi) as missing_translations,
  ROUND(100.0 * COUNT(name_fi) / COUNT(*), 2) as percent_translated
FROM bible_schema.topical_topics;
```

### Example 2: Bulk Update Topics from CSV
**User:** "Import topic translations from CSV file"

**Assistant:**

First, create CSV format:
```csv
slug,name_fi,slug_fi
forgiveness,anteeksianto,anteeksianto
grace,armo,armo
salvation,pelastus,pelastus
faith,usko,usko
love,rakkaus,rakkaus
```

Then, SQL to import:
```sql
-- Create temporary table for import
CREATE TEMP TABLE topic_translations_import (
  slug TEXT,
  name_fi TEXT,
  slug_fi TEXT
);

-- Import CSV (via Supabase Dashboard or psql)
\copy topic_translations_import FROM 'translations.csv' CSV HEADER;

-- Update topics with translations
UPDATE bible_schema.topical_topics t
SET
  name_fi = i.name_fi,
  slug_fi = i.slug_fi
FROM topic_translations_import i
WHERE t.slug = i.slug;
```