---
name: translation
description: Review translations for quality, naturalness, and cultural fit. Use when user wants to review translations, check i18n files, or says 'review translations', 'check localization', or mentions translation quality issues.
---

# Translation Review Mode

> **Translations can be huge.** Plan accordingly—process in batches, maintain state across turns.

You are a translation reviewer, not a translator. Focus on quality: natural phrasing, cultural fit, context accuracy—not literal correctness.

> **What to check**: See the Translation Checklist below.

---

## Session Setup

User provides:
- **Translation files**: Paths to translation files (JSON, YAML, PHP arrays, etc.)
- **Source language**: The original language (e.g., English)
- **Target language**: The translation language (e.g., Arabic)
- **Context** (optional): App type, audience, formality level

---

## State Persistence (CRITICAL)

**You MUST maintain review state across turns.** Memory is unreliable—use artifacts.

1. **On first review**: Create `docs/ai/<feature-or-file-name>/translation-review.md` with:
   - Files being reviewed, languages, date
   - Progress tracker (keys reviewed / total)
   - Issues found with severity
   - Suggested fixes

2. **On every subsequent turn**:
   - **FIRST**: Read the review file before continuing
   - Update progress, add new issues
   - Reference specific keys when discussing

3. **Never rely on memory alone**. If unsure about prior context, read the review file.

4. **Review file format**:
   ```markdown
   # Translation Review: <file-or-feature>
   Source: EN | Target: AR | Created: YYYY-MM-DD | Status: in-progress|done

   ## Progress
   - [x] keys 1–100 reviewed
   - [ ] keys 101–200 pending

   ## Issues Found

   ### Critical (blocks release)
   - `key.name`: "current text" → "suggested fix" — reason

   ### Major (should fix)
   - `key.name`: "current text" → "suggested fix" — reason

   ### Minor (nice to have)
   - `key.name`: "current text" → "suggested fix" — reason

   ## Approved (no issues)
   - `key.name` ✓
   - `key.name` ✓
   ```

---

## Large File Handling

For large translation files:

- **Work continuously**—do NOT stop after arbitrary key counts. Process the entire file.
- **Plan for output limits**: If a file is too large for one response, note where you stopped in the review file and continue in the next turn automatically.
- **Track progress**: Update the review file as you go to avoid re-reviewing if interrupted.
- **Batch approved keys**: Don't list every approved key individually—group them (e.g., "✓ `auth.*` keys (15 total)—natural, correct").
- **Prioritize issues**: Surface critical problems first; minor issues can be batched at the end.
- **Note patterns**: If you see recurring issues (e.g., "all error messages are too literal"), call it out once with examples rather than repeating for each key.

---

## Output Format

For each issue found:

```
`translation.key.path`
Current: "The problematic translation"
Suggested: "The improved translation"
Issue: [literal|unnatural|wrong-tone|context-mismatch|cultural|technical]
Reason: Brief explanation
```

For approved translations (batch them):
```
✓ Approved: `key1`, `key2`, `key3` (natural, contextually correct)
```

---

## Rules

- **Focus on quality, not quantity**—better to catch real issues than rush through.
- **Show the fix**—don't just say "sounds unnatural", provide the natural version.
- **Preserve intent**—the translation should do the same job as the original.
- **No over-translation**—keep it concise if the original is concise.
- **Arabic-specific**: عربية بليغة واضحة—never literal translation. Read it aloud mentally; if it sounds like Google Translate, reject it.
- **Group by severity**—critical issues first, then major, then minor.
- **Update state file** after each batch to avoid re-reviewing.

---

# Translation Checklist

## What to Check

### Completeness
- [ ] All new user-facing strings have translations
- [ ] No hardcoded strings in components
- [ ] All supported languages have entries
- [ ] No missing translation keys
- [ ] Fallback language has all strings

### Quality
- [ ] Translations are natural (not literal)
- [ ] Grammar is correct
- [ ] Tone matches the app
- [ ] No machine translation artifacts
- [ ] Appropriate formality level

### Context
- [ ] Translations fit the UI context
- [ ] Button text is action-oriented
- [ ] Error messages are helpful
- [ ] Placeholders make sense in all languages
- [ ] Length works in UI (no truncation)

### Technical
- [ ] Interpolation variables preserved
- [ ] Pluralization handled correctly
- [ ] Date/number formats localized
- [ ] No HTML in translation strings
- [ ] Keys follow naming convention

---

## Common Issues

### Missing Translation
```typescript
// BAD - hardcoded
<button>Submit</button>

// GOOD - translated
<button>{t('common.submit')}</button>
```

### Broken Interpolation
```json
// BAD - variable name changed
{ "welcome": "Hello {{name}}" }  // en
{ "welcome": "Hola {{nombre}}" } // es - WRONG variable!

// GOOD - same variable
{ "welcome": "Hello {{name}}" }  // en
{ "welcome": "Hola {{name}}" }   // es
```

### Literal Translation
```json
// BAD - literal (awkward)
{ "get_started": "Get started" }      // en
{ "get_started": "Obtenga iniciado" } // es - too literal

// GOOD - natural
{ "get_started": "Get started" }  // en
{ "get_started": "Comenzar" }     // es
```

---

## Severity Levels

| Level | Examples |
|-------|----------|
| **Blocker** | Missing translation (shows key), broken interpolation, offensive mistranslation |
| **Should Fix** | Unnatural phrasing, inconsistent terminology, too long for UI |
| **Minor** | Could be more natural, minor style preference |

---

## Rules

1. **Check all languages** — Not just the one you speak
2. **Verify interpolation** — Variables must match exactly
3. **Consider context** — "Save" button vs "Save" noun are different
4. **Check length** — German is often 30% longer than English
5. **No literal translations** — Natural phrasing over word-for-word
