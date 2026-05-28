---
name: render-template
description: Render templates with variable substitution using {{variable}} or ${variable} syntax. Use for generating formatted output, reports, commit messages, or any text requiring variable interpolation.
---

# Render Template

Render templates with variable substitution.

## Instructions

### Step 1: Receive Input

- `template`: String (template with placeholders)
- `variables`: Object (key-value pairs)
- `syntax`: mustache|shell|mixed (default: mustache)

### Step 2: Supported Syntax

- **Mustache**: `{{variable}}`, `{{object.property}}`
- **Shell**: `${variable}`, `${VARIABLE}`

### Step 3: Resolution Rules

- Direct match: `{{name}}` → `variables.name`
- Nested: `{{user.name}}` → `variables.user.name`
- Missing: Replace with empty string

### Step 4: Optional Filters

- `{{variable | uppercase}}`
- `{{variable | lowercase}}`
- `{{variable | capitalize}}`

## Example

**Input**:

```json
{
  "template": "{{type}}({{scope}}): {{description}}",
  "variables": { "type": "feat", "scope": "auth", "description": "add OAuth2" }
}
```

**Output**: `feat(auth): add OAuth2`

## Error Handling

- Missing Variables: Replace with empty string
- Invalid Syntax: Return error
- Type Mismatch: Convert to string
