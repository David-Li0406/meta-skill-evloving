---
name: textmate-grammar
description: Use this skill when creating or editing TextMate grammar files for syntax highlighting, covering scopes, patterns, and language tokenization.
---

# TextMate Grammar

## Quick Start

```json
{
  "scopeName": "source.<language>",
  "patterns": [
    { "include": "#comments" },
    { "include": "#keywords" },
    { "include": "#strings" }
  ],
  "repository": {
    "comments": {
      "name": "comment.line.<language>",
      "match": "--.*$"
    },
    "keywords": {
      "match": "\\b(if|else|while|return|match)\\b",
      "name": "keyword.control.<language>"
    },
    "strings": {
      "begin": "\"",
      "end": "\"",
      "name": "string.quoted.double.<language>",
      "patterns": [{ "include": "#escapes" }]
    }
  }
}
```

## Core Concepts

- **scopeName**: Unique identifier like `source.js`, `text.html`
- **patterns**: Array of rules applied in order
- **repository**: Named rule groups for reuse via `#name`
- **match**: Single-line regex pattern
- **begin/end**: Multi-line patterns with nested content
- **captures**: Assign scopes to regex groups: `"captures": { "1": { "name": "..." } }`
- **contentName**: Scope of content between begin/end
- **Order matters**: First matching pattern wins

## Scope Naming Conventions

| Prefix | Usage |
|--------|-------|
| `keyword.control` | if, else, for, return, match |
| `keyword.operator` | +, -, =, &&, /, > |
| `storage.type` | class, function, var, let, maybe |
| `entity.name.function` | function names |
| `entity.name.type` | type/class names |
| `variable.parameter` | function parameters |
| `string.quoted` | quoted strings |
| `comment.line` | single-line comments |
| `constant.numeric` | numbers |
| `punctuation.definition` | brackets, braces |

## Key Patterns

### Match Pattern

```json
{
  "name": "keyword.control.<language>",
  "match": "\\b(if|else|while|return|match)\\b"
}
```

### Begin/End Pattern

```json
{
  "name": "string.quoted.double.<language>",
  "begin": "\"",
  "end": "\"",
  "patterns": [
    {
      "name": "constant.character.escape.<language>",
      "match": "\\\\."
    }
  ]
}
```

### Lea-Specific Patterns

- **Pipe Operators**: 
```json
{
  "name": "keyword.operator.pipe.<language>",
  "match": "/>|/>>>|\\\\>|</"
}
```

- **Decorators**: 
```json
{
  "name": "entity.name.decorator.<language>",
  "match": "#[a-zA-Z_][a-zA-Z0-9_]*"
}
```

- **Type Annotations**: 
```json
{
  "match": "(::)\\s*([A-Z][a-zA-Z0-9]*)\\s*(:>)\\s*([A-Z][a-zA-Z0-9]*)",
  "captures": {
    "1": { "name": "keyword.operator.type.<language>" },
    "2": { "name": "entity.name.type.<language>" },
    "3": { "name": "keyword.operator.return-type.<language>" },
    "4": { "name": "entity.name.type.<language>" }
  }
}
```

- **Functions**: 
```json
{
  "begin": "\\(",
  "end": "\\)\\s*(->)",
  "endCaptures": {
    "1": { "name": "storage.type.function.arrow.<language>" }
  },
  "patterns": [
    { "include": "#parameters" }
  ]
}
```

## Testing

Use VSCode's "Developer: Inspect Editor Tokens and Scopes" command to verify tokenization.

## Reference Files

- [references/scopes.md](references/scopes.md) - Complete scope naming guide
- [references/regex.md](references/regex.md) - Oniguruma regex reference