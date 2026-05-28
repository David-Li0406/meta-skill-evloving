# Prism Token Types Reference

## Standard Tokens

### Comments

```javascript
{
  'comment': [
    { pattern: /\/\/.*/, alias: 'line' },
    { pattern: /\/\*[\s\S]*?\*\//, alias: 'block' },
    { pattern: /#.*/, alias: 'hash' }
  ]
}
```

CSS classes: `.token.comment`, `.token.comment.line`, `.token.comment.block`

### Strings

```javascript
{
  'string': [
    { pattern: /"(?:\\.|[^"\\])*"/, greedy: true },
    { pattern: /'(?:\\.|[^'\\])*'/, greedy: true },
    { pattern: /`(?:\\.|[^`\\])*`/, greedy: true, alias: 'template' }
  ]
}
```

### Keywords

```javascript
{
  'keyword': /\b(?:if|else|for|while|return|function|class|const|let|var)\b/
}
```

Subtypes:
- `keyword.control` - if, else, for, while, return
- `keyword.operator` - new, delete, typeof
- `keyword.declaration` - function, class, const

### Operators

```javascript
{
  'operator': /[+\-*/%=<>!&|^~?:]+|\.{3}/
}
```

### Punctuation

```javascript
{
  'punctuation': /[{}[\]();,.:]/
}
```

### Numbers

```javascript
{
  'number': [
    /\b0x[\da-f]+\b/i,           // Hex
    /\b0o[0-7]+\b/i,             // Octal
    /\b0b[01]+\b/i,              // Binary
    /\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i  // Decimal/float
  ]
}
```

### Booleans and Constants

```javascript
{
  'boolean': /\b(?:true|false)\b/,
  'constant': /\b(?:null|undefined|NaN|Infinity)\b/
}
```

## Entity Tokens

### Functions

```javascript
{
  'function': {
    pattern: /(\bfunction\s+)\w+/,
    lookbehind: true
  },
  'function-call': {
    pattern: /\b\w+(?=\()/,
    alias: 'function'
  }
}
```

### Classes

```javascript
{
  'class-name': [
    { pattern: /(\bclass\s+)\w+/, lookbehind: true },
    { pattern: /(\bextends\s+)\w+/, lookbehind: true },
    { pattern: /\b[A-Z][a-zA-Z0-9]*\b/ }  // PascalCase
  ]
}
```

### Properties

```javascript
{
  'property': {
    pattern: /(\.\s*)\w+/,
    lookbehind: true
  }
}
```

### Variables

```javascript
{
  'variable': /\b\w+\b/,
  'parameter': {
    pattern: /(\(\s*)\w+/,
    lookbehind: true
  }
}
```

## Special Tokens

### Regex

```javascript
{
  'regex': {
    pattern: /\/(?:[^\/\\\r\n]|\\.)+\/[gimsuy]*/,
    greedy: true,
    inside: {
      'regex-delimiter': /^\/|\/$/,
      'regex-flags': /[gimsuy]+$/
    }
  }
}
```

### Attributes (HTML/JSX)

```javascript
{
  'attr-name': /\b[\w-]+(?=\s*=)/,
  'attr-value': {
    pattern: /=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)/,
    inside: {
      'punctuation': /^=/,
      'string': /["'][^"']*["']/
    }
  }
}
```

### Tags (HTML/XML)

```javascript
{
  'tag': {
    pattern: /<\/?[\w:-]+[^>]*>/,
    inside: {
      'tag-name': /^<\/?[\w:-]+/,
      'attr-name': /[\w:-]+(?=\s*=)/,
      'punctuation': /[<>\/]/
    }
  }
}
```

## Token Aliases

```javascript
{
  'my-token': {
    pattern: /pattern/,
    alias: 'keyword'  // Applies keyword styling
  },
  'multi-alias': {
    pattern: /pattern/,
    alias: ['keyword', 'important']
  }
}
```

## Standard CSS Classes

| Token | CSS Class |
|-------|-----------|
| `comment` | `.token.comment` |
| `string` | `.token.string` |
| `keyword` | `.token.keyword` |
| `number` | `.token.number` |
| `operator` | `.token.operator` |
| `punctuation` | `.token.punctuation` |
| `function` | `.token.function` |
| `class-name` | `.token.class-name` |
| `boolean` | `.token.boolean` |
| `property` | `.token.property` |
| `builtin` | `.token.builtin` |
| `important` | `.token.important` |
| `regex` | `.token.regex` |
| `variable` | `.token.variable` |
