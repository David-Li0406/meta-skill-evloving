# Editor Integration Guide

## Monaco Editor Setup

The FableDSL editor uses Monaco Editor with custom language support.

### Language Configuration
```typescript
// packages/editor/src/languages/fabledsl.ts
export const fableDslLanguage: LanguageConfiguration = {
  comments: {
    lineComment: '//',
    blockComment: ['/*', '*/']
  },
  brackets: [
    ['{', '}'],
    ['[', ']'],
    ['(', ')']
  ],
  autoClosingPairs: [
    { open: '{', close: '}' },
    { open: '[', close: ']' },
    { open: '(', close: ')' },
    { open: '"', close: '"' }
  ],
  surroundingPairs: [
    { open: '{', close: '}' },
    { open: '[', close: ']' },
    { open: '(', close: ')' },
    { open: '"', close: '"' }
  ]
};
```

## Syntax Highlighting

### Token Definitions
```typescript
export const fableDslTokens: TokenTheme = {
  keywords: [
    'page', 'text', 'button', 'image', 'video',
    'if', 'then', 'else', 'end',
    'for', 'each', 'in', 'do',
    'at', 'size', 'scale', 'duration', 'repeat'
  ],
  operators: ['>', '<', '>=', '<=', '==', '!=', '&&', '||'],
  symbols: /[=><!~?:&|+\-*\/\^%]+/,
  escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,
  tokenizer: {
    root: [
      // Keywords
      [/\b(page|text|button|image|video|if|then|else|end|for|each|in|do|at|size|scale|duration|repeat)\b/, 'keyword'],

      // Numbers
      [/\d+/, 'number'],

      // Strings
      [/"([^"\\]|\\.)*$/, 'string.invalid'],
      [/"([^"\\]|\\.)*"/, 'string'],

      // Coordinates
      [/\[(\s*\d+\s*,?\s*)+\]/, 'type'],

      // Comments
      [/\/\/.*$/, 'comment'],
      [/\/\*/, 'comment', '@comment'],

      // Whitespace
      [/\s+/, 'white'],
    ],
    comment: [
      [/[^\/*]+/, 'comment'],
      [/\*\//, 'comment', '@pop'],
      [/[\/*]/, 'comment']
    ]
  }
};
```

## Autocompletion

### Completion Provider
```typescript
export const fableDslCompletionProvider: CompletionProvider = {
  provideCompletionItems: (model, position) => {
    const word = model.getWordUntilPosition(position);
    const range = {
      startLineNumber: position.lineNumber,
      endLineNumber: position.lineNumber,
      startColumn: word.startColumn,
      endColumn: word.endColumn
    };

    const suggestions: CompletionItem[] = [
      // Keywords
      {
        label: 'page',
        kind: CompletionItemKind.Keyword,
        insertText: 'page ${1:number} {\n\t${2}\n}',
        insertTextRules: CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: 'Define a new page'
      },
      {
        label: 'text',
        kind: CompletionItemKind.Keyword,
        insertText: 'text "${1:text}" at [${2:x}, ${3:y}]',
        insertTextRules: CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: 'Add text element'
      },
      // Add more suggestions...
    ];

    return { suggestions };
  }
};
```

## Validation

### Diagnostic Provider
```typescript
export const fableDslDiagnosticProvider: DiagnosticProvider = {
  provideDiagnostics: async (model) => {
    const diagnostics: Diagnostic[] = [];
    const content = model.getValue();

    try {
      // Parse the content
      const ast = parseDSL(content);

      // Additional validation logic...

    } catch (error) {
      if (error instanceof ParseError) {
        diagnostics.push({
          severity: DiagnosticSeverity.Error,
          range: {
            startLineNumber: error.line,
            endLineNumber: error.line,
            startColumn: error.column,
            endColumn: error.column
          },
          message: error.message
        });
      }
    }

    return diagnostics;
  }
};
```

## Hover Information

### Hover Provider
```typescript
export const fableDslHoverProvider: HoverProvider = {
  provideHover: (model, position) => {
    const word = model.getWordAtPosition(position);

    if (!word) return null;

    const hoverMap: Record<string, string> = {
      'page': 'Define a new page in the story',
      'text': 'Display text content at a specific position',
      'button': 'Create an interactive button',
      'if': 'Conditional execution based on variables or expressions',
      'for': 'Loop over a collection of items'
    };

    const info = hoverMap[word.word];
    if (info) {
      return {
        contents: [
          { value: `**${word.word}**\n\n${info}` }
        ]
      };
    }

    return null;
  }
};
```

## Keyboard Shortcuts

### Command Registration
```typescript
export const fableDslCommands = [
  {
    id: 'fable-dsl.format',
    handler: () => {
      // Format the current document
    }
  },
  {
    id: 'fable-dsl.run',
    handler: () => {
      // Execute the current story
    }
  }
];
```

## Theme Integration

### Color Theme
```typescript
export const fableDslTheme: EditorTheme = {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'keyword', foreground: '569CD6', fontStyle: 'bold' },
    { token: 'string', foreground: 'CE9178' },
    { token: 'number', foreground: 'B5CEA8' },
    { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
    { token: 'type', foreground: '4EC9B0' }
  ],
  colors: {
    'editor.background': '#0f0f0f',
    'editor.foreground': '#d4d4d4',
    'editor.lineHighlightBackground': '#2d2d30',
    'editorCursor.foreground': '#aeafad'
  }
};
```