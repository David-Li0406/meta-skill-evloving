# Error Messages and Handling

All error messages and handling strategies for design-init skill.

## Module Not Found

**When:** Module specified doesn't exist in config

**Message:**

```text
Error: Module "{module}" not found in .claude/design/design.config.json

Available modules:
- module-1
- module-2
- module-3

Please specify a valid module name.
```

**Action:** List available modules from config, exit with error

## No Design Docs Path

**When:** Module exists but has no `designDocsPath` configured

**Message:**

```text
Error: Module "{module}" does not have designDocsPath configured.

Add to .claude/design/design.config.json:

"modules": {
  "{module}": {
    "designDocsPath": ".claude/design/{module}"
  }
}
```

**Action:** Provide configuration example, suggest path, exit with error

## File Already Exists

**When:** Target file path already exists

**Message:**

```text
Warning: File already exists:
.claude/design/{module}/{topic}.md

Overwrite? This will replace the existing file.
(y/n)
```

**Action:** Use AskUserQuestion to confirm overwrite, abort if declined

## Template Not Found

**When:** Category-specific template doesn't exist

**Message:**

```text
Warning: Template not found:
.claude/skills/design-init/templates/{category}.template.md

Falling back to default template:
.claude/skills/design-init/templates/design-doc.template.md
```

**Action:** Use default template, continue with warning

## Invalid Category

**When:** Category not in module's allowed categories

**Message:**

```text
Error: Category '{category}' not allowed for module '{module}'

Allowed categories for this module:
- category-1
- category-2
- category-3

Please choose a valid category.
```

**Action:** List allowed categories from config, exit with error

## Invalid Topic Name

**When:** Topic contains invalid characters or format

**Message:**

```text
Warning: Topic contains invalid characters: {topic}

Converting to kebab-case: {converted-topic}

Proceed with converted name? (y/n)
```

**Action:** Auto-convert to kebab-case, ask for confirmation

**Conversion rules:**

- Replace spaces with hyphens
- Convert to lowercase
- Remove special characters except hyphens
- Replace underscores with hyphens

**Examples:**

- "Type Loading System" → `type-loading-system`
- "API_Design" → `api-design`
- "Error Handling (v2)" → `error-handling-v2`

## Topic Name Too Long

**When:** Topic exceeds 50 characters

**Message:**

```text
Warning: Topic name is quite long (65 characters).
Consider a shorter name for the file:

Current: advanced-performance-optimization-strategies-for-large-datasets
Suggested: performance-large-datasets

Use suggested name? (y/n)
```

**Action:** Suggest abbreviated version, ask for confirmation

**Abbreviation strategy:**

1. Remove filler words (for, the, and, of)
2. Keep key technical terms
3. Aim for 2-4 words maximum

## Directory Creation Failed

**When:** Cannot create design docs directory

**Message:**

```text
Error: Failed to create directory:
.claude/design/{module}

Check permissions and try again.
```

**Action:** Report filesystem error, exit

## Template Read Failed

**When:** Cannot read template file

**Message:**

```text
Error: Failed to read template:
.claude/skills/design-init/templates/{category}.template.md

Check file exists and has read permissions.
```

**Action:** Report filesystem error, suggest checking template location

## Write Failed

**When:** Cannot write output file

**Message:**

```text
Error: Failed to write file:
.claude/design/{module}/{topic}.md

Check directory permissions and disk space.
```

**Action:** Report filesystem error, suggest checking permissions
