# TextMate Grammar Reference

## Grammar Structure

```json
{
  "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
  "name": "My Language",
  "scopeName": "source.mylang",
  "fileTypes": ["ml"],
  "patterns": [
    { "include": "#main" }
  ],
  "repository": {
    "main": {
      "patterns": [
        { "include": "#comments" },
        { "include": "#strings" },
        { "include": "#keywords" }
      ]
    }
  }
}
```

## Pattern Types

### Match Pattern (single line)

```json
{
  "match": "\\b(if|else|while)\\b",
  "name": "keyword.control.mylang"
}
```

### Begin/End Pattern (multiline)

```json
{
  "begin": "/\\*",
  "end": "\\*/",
  "name": "comment.block.mylang",
  "patterns": [
    { "include": "#nested-content" }
  ]
}
```

### Captures

```json
{
  "match": "(function)\\s+(\\w+)",
  "captures": {
    "1": { "name": "keyword.function.mylang" },
    "2": { "name": "entity.name.function.mylang" }
  }
}
```

### Begin/End Captures

```json
{
  "begin": "(class)\\s+(\\w+)",
  "beginCaptures": {
    "1": { "name": "keyword.class.mylang" },
    "2": { "name": "entity.name.class.mylang" }
  },
  "end": "\\}",
  "endCaptures": {
    "0": { "name": "punctuation.brace.close.mylang" }
  }
}
```

## Common Regex Patterns

```json
{
  "comment-line": "//.*$",
  "comment-block": "/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/",
  "string-double": "\"(?:[^\"\\\\]|\\\\.)*\"",
  "string-single": "'(?:[^'\\\\]|\\\\.)*'",
  "number-int": "\\b\\d+\\b",
  "number-float": "\\b\\d+\\.\\d+\\b",
  "number-hex": "\\b0x[0-9a-fA-F]+\\b",
  "identifier": "\\b[a-zA-Z_][a-zA-Z0-9_]*\\b",
  "word-boundary": "\\b(?:word1|word2)\\b"
}
```

## Scope Naming Convention

### Keywords
- `keyword.control` - if, else, for, while, return
- `keyword.operator` - new, typeof, instanceof
- `keyword.other` - import, export, as

### Entities
- `entity.name.function` - function names
- `entity.name.class` - class names
- `entity.name.type` - type names
- `entity.name.tag` - HTML/XML tags

### Variables
- `variable` - general variables
- `variable.parameter` - function parameters
- `variable.language` - this, self, super

### Constants
- `constant.numeric` - numbers
- `constant.language` - true, false, null
- `constant.character.escape` - \n, \t

### Strings
- `string.quoted.single`
- `string.quoted.double`
- `string.template`
- `string.regexp`

### Comments
- `comment.line`
- `comment.block`
- `comment.documentation`

### Storage
- `storage.type` - class, function, var, let
- `storage.modifier` - static, public, private

## Priority and Greedy

```json
{
  "name": "string.quoted.double",
  "match": "\"[^\"]*\"",
  "greedy": true
}
```

Greedy prevents other patterns from matching within this pattern.
