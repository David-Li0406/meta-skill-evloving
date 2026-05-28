---
name: textmate-grammar
description: Use this skill when creating or editing TextMate grammar files for syntax highlighting, covering patterns, scopes, and language tokenization.
---

# TextMate Grammar Authoring

## Quick Start

```json
{
  "scopeName": "source.your_language",
  "patterns": [
    { "include": "#comments" },
    { "include": "#keywords" },
    { "include": "#strings" }
  ],
  "repository": {
    "comments": {
      "name": "comment.line.double-dash.your_language",
      "match": "--.*$"
    },
    "keywords": {
      "match": "\\b(if|else|while|return|match)\\b",
      "name": "keyword.control.your_language"
    },
    "strings": {
      "begin": "\"",
      "end": "\"",
      "name": "string.quoted.double.your_language",
      "patterns": [{ "include": "#escapes" }]
    }
  }
}
```

## Core Concepts

- **scopeName**: Unique identifier like `source.js`, `text.html`.
- **patterns**: Array of rules applied in order.
- **repository**: Named rule groups for reuse via `#name`.
- **match**: Single-line regex pattern.
- **begin/end**: Multi-line patterns with nested content.

## Scope Naming Conventions

| Prefix | Usage |
|--------|-------|
| `keyword.control` | if, else, for, return, match |
| `keyword.operator` | +, -, =, && |
| `storage.type` | let, class, function, var |
| `entity.name.function` | function names |
| `entity.name.type` | type/class names |
| `variable.parameter` | function parameters |
| `string.quoted` | quoted strings |
| `comment.line` | single-line comments |
| `constant.numeric` | numbers |
| `punctuation.definition` | brackets, braces |

## Key Patterns

- Use `captures` to assign scopes to regex groups: `"captures": { "1": { "name": "..." } }`.
- Use `contentName` for scope of content between begin/end.
- Escape backslashes in JSON: `\\b` for word boundary.
- Order matters: first matching pattern wins.

## Testing

Use VSCode's "Developer: Inspect Editor Tokens and Scopes" command to verify tokenization.