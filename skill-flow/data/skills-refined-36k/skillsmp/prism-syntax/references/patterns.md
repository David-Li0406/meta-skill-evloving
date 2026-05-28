# Advanced Prism Pattern Techniques

## Pattern Object Properties

```javascript
{
  'token-name': {
    pattern: /regex/,
    lookbehind: true,
    greedy: true,
    alias: 'other-token',
    inside: { /* nested grammar */ }
  }
}
```

## Lookbehind

Exclude part of match from token:

```javascript
{
  // Match "foo" in "function foo"
  'function-name': {
    pattern: /(\bfunction\s+)\w+/,
    lookbehind: true  // Excludes "function " from token
  }
}
```

## Greedy Matching

Prevents other patterns from matching within:

```javascript
{
  'string': {
    pattern: /"(?:[^"\\]|\\.)*"/,
    greedy: true  // Keywords inside won't be highlighted
  }
}
```

## Nested Grammars (inside)

```javascript
{
  'template-string': {
    pattern: /`(?:\\[\s\S]|\$\{[^}]+\}|(?!\$\{)[^`\\])*`/,
    greedy: true,
    inside: {
      'interpolation': {
        pattern: /\$\{[^}]+\}/,
        inside: {
          'punctuation': /^\$\{|\}$/,
          'expression': {
            pattern: /[\s\S]+/,
            inside: Prism.languages.javascript
          }
        }
      },
      'string': /[\s\S]+/
    }
  }
}
```

## Including Other Patterns

```javascript
Prism.languages.mylang = {
  'expression': {
    pattern: /\{[^}]+\}/,
    inside: {
      // Include all patterns from another grammar
      ...Prism.languages.javascript
    }
  }
};
```

## Rest Pattern

Match everything else:

```javascript
{
  'block': {
    pattern: /\{[^}]+\}/,
    inside: {
      'keyword': /\bif\b/,
      'rest': {
        pattern: /[\s\S]+/,
        inside: Prism.languages.mylang  // Recurse
      }
    }
  }
}
```

## Token Arrays (Multiple Patterns)

```javascript
{
  'string': [
    /"(?:\\.|[^"\\])*"/,  // Double quotes
    /'(?:\\.|[^'\\])*'/,  // Single quotes
    {
      pattern: /`(?:\\.|[^`\\])*`/,
      alias: 'template'
    }
  ]
}
```

## Extending Languages

```javascript
Prism.languages.myext = Prism.languages.extend('javascript', {
  'keyword': /\b(?:if|else|myKeyword)\b/
});

// Insert before/after
Prism.languages.insertBefore('myext', 'keyword', {
  'my-token': /pattern/
});
```

## Complex Pattern: Attributes

```javascript
{
  'attr': {
    pattern: /(\[\s*)[\w-]+(?:\s*[~|^$*]?=\s*(?:"[^"]*"|'[^']*'|[^\s\]]+))?/,
    lookbehind: true,
    inside: {
      'attr-name': /^[\w-]+/,
      'operator': /[~|^$*]?=/,
      'attr-value': {
        pattern: /"[^"]*"|'[^']*'|[^\s\]]+/,
        inside: {
          'punctuation': /^["']|["']$/
        }
      }
    }
  }
}
```

## Complex Pattern: Function Calls

```javascript
{
  'function-call': {
    pattern: /\b([a-z_]\w*)\s*\(/i,
    inside: {
      'function': /^[a-z_]\w*/i,
      'punctuation': /\($/
    }
  }
}
```

## Handling Edge Cases

### Escape sequences in strings

```javascript
{
  'string': {
    pattern: /"(?:[^"\\]|\\.)*"/,
    greedy: true,
    inside: {
      'escape': /\\(?:[nrt\\"]|u[\da-fA-F]{4}|x[\da-fA-F]{2})/
    }
  }
}
```

### Multi-line comments

```javascript
{
  'comment': {
    pattern: /\/\*[\s\S]*?\*\//,  // [\s\S] matches any char including newlines
    greedy: true
  }
}
```

### Heredocs

```javascript
{
  'heredoc': {
    pattern: /<<<(['"]?)(\w+)\1\r?\n[\s\S]*?\r?\n\2;?/,
    greedy: true,
    inside: {
      'punctuation': /^<<<['"]?\w+['"]?|^\w+;?$/m
    }
  }
}
```

## Debugging Patterns

```javascript
// Test in browser console
Prism.tokenize('your code here', Prism.languages.mylang);
```
