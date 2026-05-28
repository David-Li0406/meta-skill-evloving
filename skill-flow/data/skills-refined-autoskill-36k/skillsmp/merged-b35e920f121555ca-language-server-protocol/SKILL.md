---
name: language-server-protocol
description: Use this skill when implementing Language Server Protocol features such as diagnostics, completions, hover, and navigation.
---

# Language Server Protocol (LSP)

## Quick Start

```typescript
import { createConnection, TextDocuments, ProposedFeatures } from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

connection.onInitialize(() => ({
  capabilities: {
    textDocumentSync: TextDocumentSyncKind.Incremental,
    completionProvider: { triggerCharacters: [".", "/"], resolveProvider: true },
    hoverProvider: true,
    definitionProvider: true,
  }
}));

documents.onDidChangeContent((change) => {
  validateDocument(change.document);
});

documents.listen(connection);
connection.listen();
```

## Core Concepts

- **Connection**: JSON-RPC communication channel between client and server.
- **TextDocuments**: Manages open document state with incremental sync.
- **Capabilities**: Server declares features in `onInitialize` response.
- **Diagnostics**: Errors/warnings pushed via `connection.sendDiagnostics()`.

## Common Providers

| Provider | Purpose | Key Method |
|----------|---------|------------|
| `completionProvider` | Autocomplete suggestions | `onCompletion` |
| `hoverProvider` | Tooltip on hover | `onHover` |
| `definitionProvider` | Go-to-definition | `onDefinition` |
| `referencesProvider` | Find all references | `onReferences` |
| `documentSymbolProvider` | Outline/symbols | `onDocumentSymbol` |
| `codeActionProvider` | Quick fixes | `onCodeAction` |

## Key Patterns

- Use `TextDocument.positionAt(offset)` and `offsetAt(position)` for conversions.
- Return `null` from handlers when no result is available.
- Diagnostics use `DiagnosticSeverity.Error | Warning | Information | Hint`.
- Use `Location` for definitions, `LocationLink` for richer go-to-definition.

## Implementation Examples

### Completions

```typescript
connection.onCompletion((params): CompletionItem[] => {
  const document = documents.get(params.textDocument.uri);
  const position = params.position;

  const line = document?.getText({
    start: { line: position.line, character: 0 },
    end: position
  });

  return [
    { label: "map", kind: CompletionItemKind.Function, detail: "(fn) -> List" },
    { label: "filter", kind: CompletionItemKind.Function, detail: "(fn) -> List" },
    { label: "reduce", kind: CompletionItemKind.Function, detail: "(init, fn) -> Value" },
  ];
});
```

### Hover Information

```typescript
connection.onHover((params): Hover | null => {
  const document = documents.get(params.textDocument.uri);
  const word = getWordAtPosition(document, params.position);

  const builtin = BUILTINS[word];
  if (builtin) {
    return {
      contents: {
        kind: "markdown",
        value: `**${word}**\n\n${builtin.description}\n\n\`\`\`lea\n${builtin.signature}\n\`\`\``
      }
    };
  }
  return null;
});
```

### Diagnostics

```typescript
documents.onDidChangeContent((change) => {
  const document = change.document;
  const diagnostics: Diagnostic[] = [];

  try {
    parse(document.getText());
  } catch (error) {
    if (error instanceof ParseError) {
      diagnostics.push({
        severity: DiagnosticSeverity.Error,
        range: error.range,
        message: error.message,
        source: "lea"
      });
    }
  }

  connection.sendDiagnostics({ uri: document.uri, diagnostics });
});
```

### Go to Definition

```typescript
connection.onDefinition((params): Definition | null => {
  const document = documents.get(params.textDocument.uri);
  const word = getWordAtPosition(document, params.position);

  const definition = findDefinition(document.getText(), word);
  if (definition) {
    return {
      uri: params.textDocument.uri,
      range: definition.range
    };
  }
  return null;
});
```

## Protocol Messages

- `textDocument/completion` - Code completions
- `textDocument/hover` - Hover information
- `textDocument/definition` - Go to definition
- `textDocument/references` - Find all references
- `textDocument/documentSymbol` - Document outline
- `textDocument/formatting` - Code formatting