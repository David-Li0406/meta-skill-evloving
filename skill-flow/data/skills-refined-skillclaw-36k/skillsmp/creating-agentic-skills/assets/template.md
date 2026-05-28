# SKILL.md Template

Copy this template to create a new skill. Replace all `{placeholders}` with actual values.

---

```markdown
---
name: {skill-name}
description: {What this skill does}. Use when {trigger contexts} or when user mentions {keywords}.
---

# {Skill Title}

{Brief overview: 2-3 sentences describing what this skill enables.}

## File Location
```

{path/to/files}

````

## Structure

```{language}
{Core code pattern or structure}
````

## Core Conventions

- {Convention 1}
- {Convention 2}
- {Convention 3}

## Workflow

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Example

```{language}
{Working example}
```

## References

- [references/{file1}.md](references/{file1}.md) - {When to read this}
- [references/{file2}.md](references/{file2}.md) - {When to read this}

````

---

## Template Variations

### Minimal Skill (no references)

```markdown
---
name: {skill-name}
description: {What + when + keywords}.
---

# {Title}

{Brief overview.}

## Structure

```{language}
{Pattern}
````

## Conventions

- {Key rules}

## Example

```{language}
{Working code}
```

````

### Skill with Scripts

```markdown
---
name: {skill-name}
description: {What + when + keywords}.
---

# {Title}

{Brief overview.}

## Quick Start

Run the script:
```bash
python scripts/{script}.py {args}
````

## Manual Approach

```{language}
{Code if not using script}
```

## References

- [references/{detail}.md](references/{detail}.md) - {When needed}

````

### Domain-Specific Skill

```markdown
---
name: {skill-name}
description: {What + when + keywords}.
---

# {Title}

{Brief overview.}

## Available Domains

**{Domain1}** - {Description}
See [references/{domain1}.md](references/{domain1}.md)

**{Domain2}** - {Description}
See [references/{domain2}.md](references/{domain2}.md)

## Common Pattern

```{language}
{Shared code pattern}
````

## Find Specific Content

```bash
grep -i "{term}" references/{domain}.md
```

````

---

## Frontmatter Examples

### Good Descriptions

```yaml
# Action + triggers + keywords
description: Create Laravel migration files for database schema changes. Use when creating migrations, modifying database schema, adding tables, or when user mentions migrations, database schema, schema changes, or database structure.

# Multiple capabilities
description: Extract text from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

# Quality/workflow skill
description: Run Laravel quality checks including Rector, Pint, PHPStan, tests, and coverage. Use when ensuring code quality, before committing, or when user mentions quality, checks, or composer checks.
````

### Name Conventions

```yaml
# Correct: lowercase, hyphens, action-oriented
name: creating-actions
name: managing-models
name: writing-feature-tests

# Incorrect
name: CreateActions      # No uppercase
name: creating_actions   # No underscores
name: actions            # Too vague
name: -creating-actions  # No leading hyphen
```
