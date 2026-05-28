# Testing Patterns for DSL Extensions

## Test Structure

Organize tests by component and functionality:

```
packages/
├── parser/
│   └── tests/
│       ├── parser.test.ts
│       ├── grammar.test.ts
│       └── types.test.ts
├── runtime/
│   └── tests/
│       ├── components.test.tsx
│       ├── engine.test.ts
│       └── animations.test.ts
├── editor/
│   └── tests/
│       ├── syntax.test.ts
│       ├── completion.test.ts
│       └── validation.test.ts
└── e2e/
    └── tests/
        └── integration.test.ts
```

## Parser Tests

### Grammar Testing
```typescript
import { parseDSL } from '../src/parser';
import { expect } from 'vitest';

describe('DSL Grammar', () => {
  test('parses basic page structure', () => {
    const dsl = `
      page 1 {
        text "Hello World" at [100, 100]
      }
    `;

    const ast = parseDSL(dsl);

    expect(ast.pages).toHaveLength(1);
    expect(ast.pages[0].agents).toHaveLength(1);
    expect(ast.pages[0].agents[0]).toMatchObject({
      type: 'text',
      content: 'Hello World',
      position: [100, 100]
    });
  });

  test('validates syntax errors', () => {
    const invalidDsl = `
      page 1 {
        invalid_command "test"
      }
    `;

    expect(() => parseDSL(invalidDsl)).toThrow();
  });
});
```

### Type Validation
```typescript
import { BounceAnimation } from '../src/types';

describe('Type Validation', () => {
  test('validates bounce animation properties', () => {
    const validBounce: BounceAnimation = {
      type: 'bounce',
      duration: 1000,
      intensity: 'intense',
      repeat: 3
    };

    expect(validBounce.type).toBe('bounce');
    expect(validBounce.duration).toBe(1000);
  });

  test('rejects invalid intensity values', () => {
    // TypeScript should catch this at compile time
    // const invalidBounce: BounceAnimation = {
    //   type: 'bounce',
    //   intensity: 'invalid' // TypeScript error
    // };
  });
});
```

## Runtime Tests

### Component Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { FableButton } from '../src/components/FableButton';

describe('FableButton', () => {
  test('renders button with correct text', () => {
    render(
      <FableButton
        text="Click Me"
        position={[100, 100]}
        onClick={() => {}}
      />
    );

    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  test('calls onClick when clicked', () => {
    const mockOnClick = vi.fn();
    render(
      <FableButton
        text="Click Me"
        position={[100, 100]}
        onClick={mockOnClick}
      />
    );

    fireEvent.click(screen.getByText('Click Me'));
    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });
});
```

### Animation Testing
```typescript
import { AnimationEngine } from '../src/engine/AnimationEngine';

describe('AnimationEngine', () => {
  test('executes bounce animation', async () => {
    const element = document.createElement('div');
    document.body.appendChild(element);

    const animation = {
      type: 'bounce' as const,
      duration: 500,
      intensity: 'medium' as const,
      repeat: 2
    };

    await AnimationEngine.animate(element, animation);

    // Verify animation completed
    expect(element.style.transform).toBeDefined();
  });

  test('handles animation errors gracefully', async () => {
    const invalidElement = null as any;

    await expect(
      AnimationEngine.animate(invalidElement, { type: 'bounce' })
    ).rejects.toThrow();
  });
});
```

## Editor Tests

### Syntax Highlighting
```typescript
import { fableDslTokens } from '../src/languages/fabledsl';

describe('Syntax Highlighting', () => {
  test('highlights keywords correctly', () => {
    const input = 'page 1 { text "Hello" at [100, 100] }';
    const tokens = tokenize(input, fableDslTokens);

    expect(tokens).toContainEqual({
      type: 'keyword',
      value: 'page'
    });

    expect(tokens).toContainEqual({
      type: 'keyword',
      value: 'text'
    });
  });

  test('highlights strings correctly', () => {
    const input = 'text "Hello World" at [100, 100]';
    const tokens = tokenize(input, fableDslTokens);

    expect(tokens).toContainEqual({
      type: 'string',
      value: '"Hello World"'
    });
  });
});
```

### Autocompletion
```typescript
import { fableDslCompletionProvider } from '../src/languages/fabledsl';

describe('Autocompletion', () => {
  test('provides page completion', () => {
    const model = createMockModel('pa');
    const position = { lineNumber: 1, column: 3 };

    const completions = fableDslCompletionProvider.provideCompletionItems(model, position);

    expect(completions.suggestions).toContainEqual(
      expect.objectContaining({
        label: 'page',
        kind: CompletionItemKind.Keyword
      })
    );
  });

  test('provides animation completions', () => {
    const model = createMockModel('bounce dur');
    const position = { lineNumber: 1, column: 11 };

    const completions = fableDslCompletionProvider.provideCompletionItems(model, position);

    expect(completions.suggestions).toContainEqual(
      expect.objectContaining({
        label: 'duration'
      })
    );
  });
});
```

## Integration Tests

### End-to-End Testing
```typescript
import { FablePlayer } from '../src/components/FablePlayer';
import { parseDSL } from '@fable-js/parser';

describe('End-to-End', () => {
  test('executes complete story', async () => {
    const dsl = `
      page 1 {
        text "Welcome!" at [100, 100]
        button "Continue" at [100, 200] do goto page 2
      }

      page 2 {
        text "You made it!" at [100, 100]
      }
    `;

    const ast = parseDSL(dsl);

    const mockOnStateChange = vi.fn();
    render(
      <FablePlayer
        ast={ast}
        onStateChange={mockOnStateChange}
      />
    );

    // Simulate user interaction
    const button = screen.getByText('Continue');
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnStateChange).toHaveBeenCalledWith(
        expect.objectContaining({
          currentPage: 2
        })
      );
    });
  });
});
```

## Performance Testing

### Animation Performance
```typescript
import { AnimationEngine } from '../src/engine/AnimationEngine';

describe('Performance', () => {
  test('animation completes within time limit', async () => {
    const element = document.createElement('div');
    const startTime = performance.now();

    await AnimationEngine.animate(element, {
      type: 'bounce',
      duration: 1000
    });

    const endTime = performance.now();
    const duration = endTime - startTime;

    // Allow some tolerance for execution time
    expect(duration).toBeLessThan(1200);
  });

  test('handles multiple concurrent animations', async () => {
    const elements = Array.from({ length: 10 }, () =>
      document.createElement('div')
    );

    const animations = elements.map(element =>
      AnimationEngine.animate(element, {
        type: 'fade_in',
        duration: 500
      })
    );

    const startTime = performance.now();
    await Promise.all(animations);
    const endTime = performance.now();

    expect(endTime - startTime).toBeLessThan(800);
  });
});
```

## Test Utilities

### Mock Helpers
```typescript
export const createMockModel = (content: string) => ({
  getValue: () => content,
  getWordUntilPosition: (position: any) => ({
    word: content.slice(0, position.column - 1),
    startColumn: 1,
    endColumn: position.column
  }),
  getWordAtPosition: (position: any) => ({
    word: 'test',
    startColumn: 1,
    endColumn: 5
  })
});

export const createMockPosition = (line: number, column: number) => ({
  lineNumber: line,
  column: column
});
```

## Continuous Integration

### Test Configuration
```javascript
// vitest.config.js
export default {
  test: {
    environment: 'jsdom',
    setupFiles: ['./test-setup.ts'],
    coverage: {
      reporter: ['text', 'lcov', 'html'],
      exclude: ['node_modules/', 'dist/']
    }
  }
};
```

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test
      - run: npm run test:e2e
```