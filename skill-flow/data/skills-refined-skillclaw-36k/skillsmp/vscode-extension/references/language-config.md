# VS Code Language Configuration

## File: language-configuration.json

```json
{
  "comments": {
    "lineComment": "//",
    "blockComment": ["/*", "*/"]
  },
  "brackets": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"]
  ],
  "autoClosingPairs": [
    { "open": "{", "close": "}" },
    { "open": "[", "close": "]" },
    { "open": "(", "close": ")" },
    { "open": "\"", "close": "\"", "notIn": ["string"] },
    { "open": "'", "close": "'", "notIn": ["string", "comment"] }
  ],
  "surroundingPairs": [
    { "open": "{", "close": "}" },
    { "open": "[", "close": "]" },
    { "open": "(", "close": ")" },
    { "open": "\"", "close": "\"" },
    { "open": "'", "close": "'" }
  ],
  "folding": {
    "markers": {
      "start": "^\\s*//\\s*#?region\\b",
      "end": "^\\s*//\\s*#?endregion\\b"
    }
  },
  "wordPattern": "(-?\\d*\\.\\d\\w*)|([^\\`\\~\\!\\@\\#\\%\\^\\&\\*\\(\\)\\-\\=\\+\\[\\{\\]\\}\\\\\\|\\;\\:\\'\\\"\\,\\.\\<\\>\\/\\?\\s]+)",
  "indentationRules": {
    "increaseIndentPattern": "^.*\\{[^}]*$",
    "decreaseIndentPattern": "^\\s*\\}"
  }
}
```

## Comments

Enables toggle comment commands (Ctrl+/).

```json
{
  "comments": {
    "lineComment": "//",
    "blockComment": ["/*", "*/"]
  }
}
```

## Brackets

Defines matching brackets for highlighting and navigation.

```json
{
  "brackets": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"],
    ["<", ">"]  // for generics
  ]
}
```

## Auto-Closing Pairs

Automatically insert closing character when opening is typed.

```json
{
  "autoClosingPairs": [
    { "open": "{", "close": "}" },
    { "open": "\"", "close": "\"", "notIn": ["string", "comment"] }
  ]
}
```

`notIn` options: `string`, `comment`, `regex`

## Surrounding Pairs

Characters that surround selections.

## Folding

### Indentation-based (default)
No configuration needed.

### Marker-based

```json
{
  "folding": {
    "markers": {
      "start": "^\\s*//\\s*region\\b",
      "end": "^\\s*//\\s*endregion\\b"
    }
  }
}
```

### Off-side rule (Python-style)

```json
{
  "folding": {
    "offSide": true
  }
}
```

## Indentation Rules

```json
{
  "indentationRules": {
    "increaseIndentPattern": "^.*\\{[^}]*$|^.*\\([^)]*$",
    "decreaseIndentPattern": "^\\s*[\\}\\)]",
    "indentNextLinePattern": "^.*:$",
    "unIndentedLinePattern": "^\\s*#.*$"
  }
}
```

## Word Pattern

Defines what constitutes a "word" for double-click selection.

```json
{
  "wordPattern": "[a-zA-Z_][a-zA-Z0-9_]*"
}
```

## On Enter Rules

Actions when Enter is pressed.

```json
{
  "onEnterRules": [
    {
      "beforeText": "^\\s*/\\*\\*(?!/)([^\\*]|\\*(?!/))*$",
      "afterText": "^\\s*\\*/$",
      "action": { "indent": "indentOutdent", "appendText": " * " }
    }
  ]
}
```
