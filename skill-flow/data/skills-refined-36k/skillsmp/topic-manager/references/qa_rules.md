# Topic QA Rules

## QA Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `unchecked` | Default for imports, not yet reviewed | Review needed |
| `ok` | Verified correct | No action |
| `needs_review` | Flagged for human review | Priority review |

## Validation Rules

### Finnish Translation Quality

1. **Spelling Check** - Use Voikko/Omorfi to verify word validity
2. **No English Left** - Ensure name_fi is actual Finnish, not English copy
3. **Proper Diacritics** - ä and ö must be correctly used
4. **Appropriate Capitalization** - Only proper nouns capitalized in Finnish
5. **Compound Words** - Check if should be written together (yhdyssanat)

### Translation Accuracy

1. **Biblical Terms** - Use established Finnish Bible terminology
2. **Theological Accuracy** - Maintain theological meaning
3. **Common Usage** - Prefer commonly understood Finnish terms

### Structural Quality

1. **Slug Format** - slug_fi should be lowercase, hyphenated, URL-safe
2. **Length** - Keep reasonable length for UI display
3. **Consistency** - Similar topics should have similar translation patterns

## Common Finnish Biblical Terms

| English | Finnish | Notes |
|---------|---------|-------|
| Grace | Armo | Not "armahdus" |
| Faith | Usko | |
| Salvation | Pelastus | |
| Redemption | Lunastus | |
| Forgiveness | Anteeksianto | |
| Righteousness | Vanhurskaus | |
| Sin | Synti | |
| Covenant | Liitto | |
| Prophet | Profeetta | |
| Apostle | Apostoli | |
| Disciple | Opetuslapsi | |
| Worship | Ylistys / Palvonta | Context-dependent |
| Prayer | Rukous | |
| Blessing | Siunaus | |
| Gospel | Evankeliumi | |
| Kingdom | Valtakunta | |
| Heaven | Taivas | |
| Hell | Helvetti | |
| Angel | Enkeli | |
| Demon | Demoni / Paha henki | |
| Holy Spirit | Pyhä Henki | |
| Trinity | Kolminaisuus | |
| Baptism | Kaste | |
| Communion | Ehtoollinen | |
| Resurrection | Ylösnousemus | |

## Issue Detection Queries

### Find Potential English Names
```sql
SELECT id, name_en, name_fi
FROM bible_schema.topical_topics
WHERE name_fi ~ '^[a-zA-Z]+$'  -- Only ASCII letters
AND LENGTH(name_fi) > 3;
```

### Find Missing Diacritics
```sql
SELECT id, name_en, name_fi
FROM bible_schema.topical_topics
WHERE name_fi LIKE '%ae%' OR name_fi LIKE '%oe%'
-- Could be missing ä or ö
```

### Find Duplicate Translations
```sql
SELECT name_fi, COUNT(*) as cnt, array_agg(name_en) as english_names
FROM bible_schema.topical_topics
WHERE name_fi IS NOT NULL
GROUP BY name_fi
HAVING COUNT(*) > 1;
```

### Find Short/Suspicious Translations
```sql
SELECT id, name_en, name_fi
FROM bible_schema.topical_topics
WHERE name_fi IS NOT NULL
AND LENGTH(name_fi) < 3;
```

## Topic Suggestion Tables

### topic_suggestions
User-submitted new topic suggestions.

| Column | Type | Description |
|--------|------|-------------|
| suggested_term | TEXT | Finnish term suggested |
| suggested_name_en | TEXT | English equivalent if provided |
| status | TEXT | 'pending', 'approved', 'rejected' |
| admin_notes | TEXT | Admin review notes |
| created_topic_id | UUID | ID if approved and created |

### topic_content_suggestions
Suggestions for topic field updates.

| Column | Type | Description |
|--------|------|-------------|
| topic_id | UUID | Target topic |
| field_name | TEXT | Which field to update |
| language | TEXT | 'fi' or 'en' |
| suggested_content | TEXT | Proposed content |
| status | TEXT | Review status |

### topic_comprehensive_suggestions
AI-generated comprehensive topic improvements.

| Column | Type | Description |
|--------|------|-------------|
| topic_id | UUID | Target topic |
| semantic_field_fi/en | TEXT | Suggested semantic fields |
| usage_context_fi/en | TEXT | Suggested usage context |
| nuance_fi/en | TEXT | Suggested nuance text |
| suggested_verses | JSONB | Suggested Bible references |
| suggested_relations | JSONB | Suggested topic relations |
| suggest_deletion | BOOLEAN | Flag topic for deletion |
| deletion_reason | TEXT | Why to delete |

## Review Workflow

1. **Daily Review** - Check `qa_status = 'unchecked'` topics
2. **Priority** - Start with `is_core = true` topics
3. **Validation** - Run through Finnish spell checker
4. **Theological Review** - Verify translation accuracy
5. **Mark Complete** - Set `qa_status = 'ok'`
