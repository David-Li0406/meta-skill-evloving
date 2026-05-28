---
name: testing
description: Guide for creating and running tests in the Markco VS Code extension
---
# Test Creation and Running Skill

This skill provides guidance for creating and running tests in the Markco VS Code extension.

## Project Test Structure

```
src/test/
├── runTest.ts           # Test runner entry point
└── suite/
    ├── index.ts         # Mocha test suite loader
    ├── CommentService.test.ts    # CommentService unit tests
    ├── CommentDecorator.test.ts  # CommentDecorator unit tests
    └── extension.test.ts         # Integration tests
```

## Running Tests

### From Command Line
```bash
# Run all tests
npm run test

# Compile and run tests
npm run test:watch

# Just compile (prerequisite for tests)
npm run compile
```

### From VS Code
1. **Task Runner**: Press `Ctrl+Shift+P` → "Tasks: Run Task" → Select "Run Tests"
2. **Debug Tests**: Press `F5` → Select "Run Extension Tests"
3. **Quick Test**: `Ctrl+Shift+B` to compile, then `Ctrl+Shift+P` → "Tasks: Run Test Task"

## Writing New Tests

### Test File Template
```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';
import * as Mocha from 'mocha';

const suite = Mocha.suite;
const test = Mocha.test;
const setup = Mocha.setup;
const teardown = Mocha.teardown;

suite('YourComponent Test Suite', () => {
  let sandbox: sinon.SinonSandbox;

  setup(() => {
    sandbox = sinon.createSandbox();
  });

  teardown(() => {
    sandbox.restore();
  });

  suite('Feature Group', () => {
    test('should do something', () => {
      // Arrange
      const expected = 'value';
      
      // Act
      const actual = 'value';
      
      // Assert
      assert.strictEqual(actual, expected);
    });
  });
});
```

### Mock Document Helper
Mock documents require the `encoding` property:
```typescript
function createMockDocument(text: string): vscode.TextDocument {
  const lines = text.split('\n');
  return {
    uri: vscode.Uri.parse('file:///test/mock.md'),
    languageId: 'markdown',
    lineCount: lines.length,
    encoding: 'utf-8',  // Required!
    getText: (range?: vscode.Range) => range ? /* extract range */ : text,
    // ... other required properties
  } as vscode.TextDocument;
}
```

### Mock Editor for Integration Tests
```typescript
async function createMockEditor(text: string): Promise<vscode.TextEditor> {
  const document = await vscode.workspace.openTextDocument({
    language: 'markdown',
    content: text
  });
  return await vscode.window.showTextDocument(document);
}
```

## Test Categories

### Unit Tests
- Test individual functions in isolation
- Mock VS Code APIs
- Focus on business logic
- Located in: `CommentService.test.ts`, `CommentDecorator.test.ts`

### Integration Tests
- Test component interactions
- Use real VS Code APIs when possible
- Test command execution
- Located in: `extension.test.ts`

## Key Test Scenarios to Cover

### CommentService
- Parse comments from markdown
- Handle malformed JSON
- Ignore comment blocks in code fences
- CRUD operations on comments
- Reply management
- Anchor reconciliation
- Text sanitization (-->)

### CommentDecorator
- Apply/clear decorations
- Find comment at position
- Focus management
- Navigate to comment

### Extension
- Command registration
- Activation events
- Configuration handling
- Webview communication

## Mocking Tips

### Stub VS Code APIs
```typescript
sandbox.stub(vscode.window, 'showInformationMessage').resolves();
sandbox.stub(vscode.workspace, 'applyEdit').resolves(true);
```

### Stub Git Commands
```typescript
sandbox.stub(child_process, 'exec').yields(null, { stdout: 'testuser\n' });
```

## Common Issues

1. **Tests hang**: Ensure all async operations complete
2. **Extension not active**: Tests run in separate VS Code instance
3. **File not found**: Use absolute paths or mock documents
4. **Mocha functions undefined**: Must import from Mocha explicitly (see template above)

## Adding New Test File
1. Create `src/test/suite/NewComponent.test.ts`
2. Follow the test template above (with Mocha imports!)
3. Run `npm run compile`
4. Run `npm test`
