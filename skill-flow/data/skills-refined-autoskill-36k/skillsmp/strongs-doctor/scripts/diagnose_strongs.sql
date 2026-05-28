-- Strong's Concordance Diagnostic Script
-- Run these queries to diagnose issues with Strong's data

-- ============================================================
-- SECTION 1: LEXICON HEALTH CHECK
-- ============================================================

-- 1.1 Count entries by language
SELECT
  CASE WHEN strongs_number LIKE 'H%' THEN 'Hebrew' ELSE 'Greek' END as language,
  COUNT(*) as count
FROM bible_schema.strongs_lexicon
GROUP BY 1;

-- 1.2 Find entries missing required fields
SELECT strongs_number,
  CASE WHEN lemma IS NULL OR lemma = '' THEN 'missing lemma' END as issue
FROM bible_schema.strongs_lexicon
WHERE lemma IS NULL OR lemma = ''
LIMIT 20;

-- 1.3 Find malformed Strong's numbers
SELECT strongs_number
FROM bible_schema.strongs_lexicon
WHERE strongs_number !~ '^[GH][1-9][0-9]*$'
LIMIT 20;

-- ============================================================
-- SECTION 2: KJV WORDS INTEGRITY
-- ============================================================

-- 2.1 Summary statistics
SELECT
  COUNT(*) as total_entries,
  COUNT(DISTINCT verse_id) as unique_verses,
  COUNT(DISTINCT strongs_number) as unique_strongs,
  COUNT(*) FILTER (WHERE strongs_number IS NULL) as null_strongs,
  COUNT(*) FILTER (WHERE word_text = '') as empty_words
FROM bible_schema.kjv_strongs_words;

-- 2.2 Check for corruption pattern (punctuation with Strong's numbers)
SELECT word_text, strongs_number, COUNT(*) as count
FROM bible_schema.kjv_strongs_words
WHERE word_text IN ('.', ',', ';', ':', '?', '!', '')
  AND strongs_number IS NOT NULL
GROUP BY word_text, strongs_number
ORDER BY count DESC
LIMIT 20;

-- 2.3 Most common Strong's numbers (should be articles/particles at top)
SELECT strongs_number, COUNT(*) as occurrences
FROM bible_schema.kjv_strongs_words
WHERE strongs_number IS NOT NULL
GROUP BY strongs_number
ORDER BY occurrences DESC
LIMIT 15;

-- ============================================================
-- SECTION 3: CROSS-REFERENCE VALIDATION
-- ============================================================

-- 3.1 Find broken see_also references
WITH refs AS (
  SELECT strongs_number, unnest(see_also) as ref
  FROM bible_schema.strongs_lexicon
  WHERE see_also IS NOT NULL AND array_length(see_also, 1) > 0
)
SELECT r.strongs_number, r.ref as missing_ref
FROM refs r
LEFT JOIN bible_schema.strongs_lexicon sl ON sl.strongs_number = r.ref
WHERE sl.strongs_number IS NULL
LIMIT 20;

-- 3.2 Find entries with unparseable derivation references
SELECT strongs_number, derivation
FROM bible_schema.strongs_lexicon
WHERE derivation ~ 'from [gh][0-9]+'
  AND derivation !~ '\[\[[GH][0-9]+\]\]'
LIMIT 10;

-- ============================================================
-- SECTION 4: INDEX CHECK
-- ============================================================

-- 4.1 List indexes on kjv_strongs_words
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'kjv_strongs_words'
  AND schemaname = 'bible_schema';

-- ============================================================
-- SECTION 5: SAMPLE DATA VERIFICATION
-- ============================================================

-- 5.1 Verify G26 (agape/love) - should match expected definition
SELECT strongs_number, lemma, definition_short
FROM bible_schema.strongs_lexicon
WHERE strongs_number = 'G26';

-- 5.2 Sample KJV words for G26
SELECT ksw.word_text, v.text as verse_text, vk.osis
FROM bible_schema.kjv_strongs_words ksw
JOIN bible_schema.verses v ON ksw.verse_id = v.id
JOIN bible_schema.verse_keys vk ON v.verse_key_id = vk.id
WHERE ksw.strongs_number = 'G26'
LIMIT 5;

-- 5.3 Verify H3068 (YHWH/LORD) - most common Hebrew word
SELECT strongs_number, lemma, definition_short
FROM bible_schema.strongs_lexicon
WHERE strongs_number = 'H3068';
