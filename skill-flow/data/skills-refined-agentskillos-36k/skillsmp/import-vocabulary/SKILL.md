---
name: import-vocabulary
description: Import vocabulary from Word documents (.docx) containing Arabic words. Use when the user wants to import, add, or extract vocabulary from a Word document, docx file, or Arabic learning materials. Extracts Arabic-English word pairs and creates/updates decks based on categories.
---

# Import Vocabulary from Word Documents

This skill extracts Arabic vocabulary from .docx files and imports them into the flashcard system.

## Workflow Overview

1. **Extract** → Parse .docx with pandoc
2. **Generate** → Create markdown file with extracted vocabulary
3. **Confirm** → Ask user which words to import
4. **Import** → Create cards via API
5. **Archive** → Move files to `processed/` folder

## Step 1: Extract Text from Document

Use pandoc to convert the Word document to markdown:

```bash
pandoc "path/to/document.docx" -t markdown
```

## Step 2: Parse and Generate Markdown

From the extracted content, identify vocabulary entries and create a markdown file in the same directory as the source document.

**Filename pattern:** `{original_name}.vocab.md`

Example: `صفات.docx` → `صفات.vocab.md`

**Markdown format:**

```markdown
# Vocabulary: صفات (Adjectives)

Source: صفات.docx
Extracted: 2024-01-15
Category: Adjectives

## Words

| # | Arabic | English | Notes | Import |
|---|--------|---------|-------|--------|
| 1 | جديد / جديدة | new | masc/fem | ✓ |
| 2 | قديم / قديمة | old | masc/fem | ✓ |
| 3 | ثقيل / ثقيلة | heavy | masc/fem | ✓ |
| 4 | خفيف / خفيفة | light | masc/fem | ✓ |

## Summary

- Total words found: 12
- Ready to import: 12
- Skipped: 0
```

**Parsing rules:**
- Strip `{dir="rtl"}` markers from Arabic text
- Ignore image references like `![...](media/...)`
- Skip exercise blanks (____), instructions, non-vocabulary content
- Handle masculine/feminine pairs: "جديد- جديدة" → "جديد / جديدة"
- Preserve Arabic diacritics (tashkeel)

## Step 3: Ask for Confirmation

Present the generated markdown to the user and ask:

```
I've extracted 12 vocabulary items from "صفات.docx"

Category detected: Adjectives (صفات)
Target deck: [New deck "Adjectives (صفات)" / Existing deck "..."]

Preview:
1. جديد / جديدة - new
2. قديم / قديمة - old
3. ثقيل / ثقيلة - heavy
...

Would you like to:
- Import all words
- Review the full list in صفات.vocab.md first
- Skip certain words (specify which)
```

## Step 4: Check/Create Deck

**Check existing decks:**
```bash
curl -s http://localhost:3001/api/decks
```

**Determine deck:**
1. Check filename for category hints:
   - "صفات" = Adjectives
   - "أسماء" = Nouns
   - "أفعال" = Verbs
   - "definite article" = Grammar
2. Match against existing deck names
3. If no match: create new deck or use "Import YYYY-MM-DD"

**Create new deck (if needed):**
```bash
curl -X POST "http://localhost:3000/api/decks" \
  -H "Content-Type: application/json" \
  -d '{"name": "Adjectives (صفات)", "description": "Imported from صفات.docx"}'
```

## Step 5: Import Cards via API

```bash
curl -X POST "http://localhost:3000/api/decks/{deck_id}/cards" \
  -H "Content-Type: application/json" \
  -d '[
    {"front": "جديد / جديدة", "back": "new", "notes": "masc/fem"},
    {"front": "قديم / قديمة", "back": "old", "notes": "masc/fem"}
  ]'
```

## Step 6: Archive to Processed Folder

After successful import, move both files to a `processed/` subfolder:

```bash
# Create processed folder if it doesn't exist
mkdir -p "path/to/processed"

# Move the original docx
mv "path/to/document.docx" "path/to/processed/"

# Move the generated vocab markdown
mv "path/to/document.vocab.md" "path/to/processed/"
```

**Folder structure after processing:**

```
example-arabic-docs/
├── processed/
│   ├── صفات.docx
│   ├── صفات.vocab.md
│   ├── الأسماء.docx
│   └── الأسماء.vocab.md
└── new-document.docx  (not yet processed)
```

## Step 7: Report Results

```
✓ Imported 12 cards to deck "Adjectives (صفات)" (ID: 5)

Files archived:
  → processed/صفات.docx
  → processed/صفات.vocab.md

View deck: http://localhost:3000/deck/5
```

## Error Handling

- If dev server isn't running: prompt user to run `npm run dev`
- If API call fails: keep files in original location, report error
- If no vocabulary found: create empty .vocab.md noting "No vocabulary extracted"

## Notes

- The .vocab.md files serve as a permanent record of what was extracted
- User can edit .vocab.md before confirming import if needed
- The processed/ folder makes it easy to see what's been imported
- WebSearch can be used to look up unclear translations
