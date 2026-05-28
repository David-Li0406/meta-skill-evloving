---
name: i18n-validation
description: Validate translation keys exist in both Polish and English locale files before committing. Use when adding new user-facing text or translation keys.
---

# i18n Key Validation Skill

Validates that translation keys exist in both Polish and English locale files before committing
changes.

## Purpose

USE this skill when:

- Adding new user-facing text to Vue components
- Using `$t('translation.key')` in templates or composables
- Creating new translation keys in locale files
- Before committing changes that introduce new i18n keys

DO NOT use this skill for:

- Reading existing translations
- Translating text manually
- Modifying translation values (non-key changes)

## Critical Rules

⚠️ **Polish is PRIMARY** - All user-facing text must be in Polish via $t() ⚠️ **Both locales
REQUIRED** - Keys must exist in BOTH `i18n/locales/pl.json` AND `i18n/locales/en.json` ⚠️ **No
hardcoded Polish** - Never put Polish text directly in templates

## Workflow Steps

### Step 1: Detect New Translation Keys

**Goal**: Identify new `$t()` calls in Vue components or composables.

**Actions**:

1. Scan modified/new files for `$t('...')` or `t('...')` calls
2. Extract translation keys from:
   - Template usage: `{{ $t('common.submit') }}`
   - Script usage: `const title = t('pages.meetings.title')`
   - Computed properties: `computed(() => $t('navigation.home'))`
3. Build list of all translation keys used
4. If no new keys found, skip workflow

**Output**: List of translation keys to validate.

---

### Step 2: Validate Key in pl.json

**Goal**: Ensure translation key exists in Polish locale file.

**Actions**:

1. Read `i18n/locales/pl.json`
2. For each translation key, verify it exists:
   - Parse hierarchical key: `pages.meetings.title` → `pages` → `meetings` → `title`
   - Navigate JSON structure to find key
   - Check if value is a non-empty string
3. Identify MISSING keys (keys used in code but not in pl.json)
4. Identify EMPTY keys (keys with empty string values)

**Output**: List of missing/empty keys in pl.json (if any).

---

### Step 3: Validate Key in en.json

**Goal**: Ensure translation key exists in English locale file (fallback).

**Actions**:

1. Read `i18n/locales/en.json`
2. For each translation key, verify it exists:
   - Same hierarchical parsing as Step 2
   - Navigate JSON structure
   - Check for non-empty string value
3. Identify MISSING keys (keys in pl.json but not in en.json)
4. Identify EMPTY keys (keys with empty string values)

**Output**: List of missing/empty keys in en.json (if any).

---

### Step 4: Verify Key Path Consistency

**Goal**: Ensure key paths match exactly in both files.

**Actions**:

1. Compare hierarchical structure of keys between pl.json and en.json:
   - Same nesting depth
   - Same parent keys
   - Same key names (case-sensitive)
2. Identify MISMATCHED paths:
   - Key exists in pl.json as `pages.meeting.title`
   - Key exists in en.json as `pages.meetings.title`
   - These are DIFFERENT keys!
3. Check for typos in key names across files

**Output**: List of mismatched key paths (if any).

---

### Step 5: Browser Console Check (Manual)

**Goal**: Test for missing translation warnings in development mode.

**Actions**:

1. Prompt user to run application:

```
🔍 Translation keys validated in files.

Please test in browser:

1. Run dev server: pnpm dev
2. Navigate to pages using new translation keys
3. Open browser console (F12 → Console tab)
4. Look for warnings like:
   [i18n] Missing translation: pages.meetings.title (locale: pl)

If you see warnings:
- Check key spelling in component
- Verify key exists in i18n/locales/*.json
- Ensure JSON syntax is valid (no trailing commas)
```

2. Wait for user confirmation
3. If warnings found, return to Step 2/3 to fix issues

**Output**: No missing translation warnings in browser console.

---

### Step 6: Polish Character Verification

**Goal**: Verify Polish characters render correctly.

**Actions**:

1. Check that Polish translations contain proper Polish characters:
   - ą, ć, ę, ł, ń, ó, ś, ź, ż
2. Ensure locale files are UTF-8 encoded
3. Prompt user to visually verify in browser:

```
✅ Translation keys validated.

Please verify Polish characters render correctly:

1. Navigate to pages with new translations
2. Check for garbled characters (Ä, Ã, etc.)
3. Common characters to check: ą ć ę ł ń ó ś ź ż

If characters are garbled:
- File encoding issue - ensure UTF-8
- Font issue - check font-family in CSS
```

**Output**: Polish characters confirmed rendering correctly.

---

### Step 7: Pre-Commit Checklist

**Goal**: Final validation before commit.

**Actions**:

1. Display pre-commit checklist for user:

```
✅ i18n Key Validation Pre-Commit Checklist

Translation key: [example: pages.meetings.create.title]

□ Key exists in i18n/locales/pl.json
□ Key exists in i18n/locales/en.json
□ Key paths are identical in both files
□ No missing translation warnings in browser console
□ Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż) render correctly
□ No hardcoded Polish text in component
□ Used $t() for all user-facing text
□ JSON files have valid syntax (no trailing commas)

All checkboxes must be checked before committing.
```

2. Confirm all items checked
3. If any items unchecked, return to corresponding workflow step

**Output**: All validation checks passed, ready to commit.

## References

- i18n patterns: `.agents/i18n-patterns.md`
- Polish locale: `i18n/locales/pl.json`
- English locale: `i18n/locales/en.json`
- Vue i18n documentation: Official docs (Context7)
