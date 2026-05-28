# Naming Conventions (Official Anthropic Guidelines)

## Skill Name Requirements

The `name` field in YAML frontmatter must follow these rules:

| Rule | Requirement |
|------|-------------|
| Max length | 64 characters |
| Characters | Lowercase letters, numbers, hyphens only |
| No XML tags | Cannot contain `<` or `>` |
| Reserved words | Cannot contain "anthropic" or "claude" |

## Recommended Naming Style: Gerund Form

Use **gerund form** (verb + -ing) for skill names as this clearly describes the activity.

### Good Examples (Gerund Form)
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`
- `deploying-apps`

### Acceptable Alternatives
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

### Avoid
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`
- Inconsistent patterns within your skill collection
- CamelCase: `myAwesomeSkill`
- Underscores: `my_awesome_skill`

## Description Requirements

The `description` field must follow these rules:

| Rule | Requirement |
|------|-------------|
| Non-empty | Must have content |
| Max length | 1024 characters |
| No XML tags | Cannot contain `<` or `>` |
| Point of view | **Third person only** |

### Third Person Requirement

The description is injected into the system prompt. Inconsistent point-of-view causes discovery problems.

| Status | Example |
|--------|---------|
| **Good** | "Processes Excel files and generates reports" |
| **Avoid** | "I can help you process Excel files" |
| **Avoid** | "You can use this to process Excel files" |

### Description Template

```
[Action verb] [what it does]. Use when [specific triggers/contexts].
```

### Good Description Examples

**PDF Processing:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel Analysis:**
```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git Commit Helper:**
```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

### Avoid Vague Descriptions

```yaml
# BAD - Too vague
description: Helps with documents
description: Processes data
description: Does stuff with files

# GOOD - Specific with triggers
description: Converts Word documents to PDF with formatting preservation. Use when user needs .docx to .pdf conversion or mentions Word/PDF conversion.
```

## Validation Checklist

Before finalizing a skill name and description:

- [ ] Name is ≤ 64 characters
- [ ] Name uses only lowercase, numbers, hyphens
- [ ] Name doesn't contain "anthropic" or "claude"
- [ ] Description is non-empty and ≤ 1024 characters
- [ ] Description uses third person
- [ ] Description includes what it does AND when to use it
- [ ] No XML tags in either field
