# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

## Code Output Patterns

### Minimal Example Pattern

Show the simplest possible working code:

```markdown
## Quick Start

```python
from mylib import Client

client = Client()
result = client.do_thing("input")
print(result)
```

For advanced options, see references/advanced.md
```

### Progressive Complexity Pattern

Start simple, add complexity only when needed:

```markdown
## Usage Levels

### Basic (most users)
```python
result = process(data)
```

### With Options
```python
result = process(data, format="json", validate=True)
```

### Full Control
```python
result = process(
    data,
    format="json",
    validate=True,
    hooks={
        "pre": my_preprocessor,
        "post": my_postprocessor
    },
    config=custom_config
)
```

## Validation Patterns

### Checklist Pattern

For outputs that must meet criteria:

```markdown
## Before Submitting

Verify your output against this checklist:

- [ ] All required fields present
- [ ] Dates in ISO 8601 format
- [ ] No PII in public fields
- [ ] Total under 10MB
- [ ] Valid JSON/YAML syntax
```

### Assertion Pattern

For programmatic validation:

```markdown
## Output Validation

Run the validator before using output:

```bash
scripts/validate_output.py output.json
```

Expected: "✅ Output valid"

Common errors:
- "Missing field: X" → Add required field X
- "Invalid date format" → Use YYYY-MM-DD
```

## Grounding Outputs with Context7

When skill outputs involve library-specific formats or patterns:

```markdown
## API Response Format

**First, verify current format with Context7:**
```
context7_get-library-docs /api/library --topic "response format"
```

**Then format output accordingly:**

Based on current documentation, responses should follow:
[Insert pattern from documentation]

**Note:** API response formats may change between versions.
Always verify against current documentation.
```

## Consistency Patterns

### Naming Convention Pattern

```markdown
## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Files | kebab-case | `user-profile.ts` |
| Classes | PascalCase | `UserProfile` |
| Functions | camelCase | `getUserProfile` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` |
| Database tables | snake_case | `user_profiles` |
```

### Style Guide Pattern

```markdown
## Code Style

- Indent: 2 spaces
- Line length: 80 characters max
- Quotes: Single quotes for strings
- Semicolons: Required
- Trailing commas: Always in multiline

Run formatter before committing:
```bash
npm run format
```
```
