# Test Patterns - API Reference

**Versions**:
- Jest v30.2.0
- @testing-library/react v13.4.0
- @testing-library/user-event v14.x
- @testing-library/jest-dom (matchers)

## Official Documentation

- **Testing Library**: https://testing-library.com/docs/react-testing-library/intro
- **Jest**: https://jestjs.io/docs/getting-started
- **User Event**: https://testing-library.com/docs/user-event/intro
- **Jest DOM**: https://github.com/testing-library/jest-dom

## Import Statements

```typescript
import { render, screen, waitFor, act } from '@testing-library/react';
import { renderHook } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { fireEvent } from '@testing-library/react';
```

## render()

Render a React component for testing.

```typescript
function render(
  ui: React.ReactElement,
  options?: RenderOptions
): RenderResult;

interface RenderOptions {
  wrapper?: React.ComponentType;
  container?: HTMLElement;
  baseElement?: HTMLElement;
  hydrate?: boolean;
}

interface RenderResult {
  container: HTMLElement;
  baseElement: HTMLElement;
  debug: (element?: HTMLElement) => void;
  rerender: (ui: React.ReactElement) => void;
  unmount: () => void;
  asFragment: () => DocumentFragment;
}
```

**Usage:**
```typescript
// Basic render
render(<Component />);

// With wrapper (providers)
render(<Component />, {
  wrapper: ({ children }) => (
    <QueryClientProvider client={new QueryClient()}>
      {children}
    </QueryClientProvider>
  ),
});

// Destructure for utilities
const { container, rerender, unmount } = render(<Component />);
```

## screen

Global object for querying rendered elements. Preferred over destructuring render.

```typescript
// Query methods (throw error if not found)
screen.getByTestId(id: string): HTMLElement;
screen.getByRole(role: string, options?: ByRoleOptions): HTMLElement;
screen.getByText(text: string | RegExp, options?: TextMatchOptions): HTMLElement;
screen.getByLabelText(text: string | RegExp): HTMLElement;
screen.getByPlaceholderText(text: string | RegExp): HTMLElement;
screen.getByAltText(text: string | RegExp): HTMLElement;
screen.getByTitle(title: string | RegExp): HTMLElement;
screen.getByDisplayValue(value: string | RegExp): HTMLElement;

// Query all methods (return array)
screen.getAllByTestId(id: string): HTMLElement[];
screen.getAllByRole(role: string): HTMLElement[];
screen.getAllByText(text: string | RegExp): HTMLElement[];
// ... etc

// queryBy methods (return null if not found, no error)
screen.queryByTestId(id: string): HTMLElement | null;
screen.queryByRole(role: string): HTMLElement | null;
screen.queryByText(text: string | RegExp): HTMLElement | null;
// ... etc

// queryAllBy methods (return empty array if not found)
screen.queryAllByTestId(id: string): HTMLElement[];
screen.queryAllByRole(role: string): HTMLElement[];
// ... etc

// findBy methods (async, wait for element)
screen.findByTestId(id: string, options?: WaitForOptions): Promise<HTMLElement>;
screen.findByRole(role: string, options?: WaitForOptions): Promise<HTMLElement>;
screen.findByText(text: string | RegExp, options?: WaitForOptions): Promise<HTMLElement>;
// ... etc

// findAllBy methods (async, wait for elements)
screen.findAllByTestId(id: string, options?: WaitForOptions): Promise<HTMLElement[]>;
screen.findAllByRole(role: string, options?: WaitForOptions): Promise<HTMLElement[]>;
// ... etc
```

### ByRoleOptions

```typescript
interface ByRoleOptions {
  name?: string | RegExp;       // Accessible name
  checked?: boolean;             // For checkboxes
  pressed?: boolean;             // For buttons
  selected?: boolean;            // For options
  expanded?: boolean;            // For disclosure widgets
  level?: number;                // For headings (1-6)
  hidden?: boolean;              // Include hidden elements
}
```

**Usage:**
```typescript
// Find by role with options
screen.getByRole('button', { name: 'Submit' });
screen.getByRole('checkbox', { checked: true });
screen.getByRole('heading', { level: 1 });
```

### TextMatchOptions

```typescript
interface TextMatchOptions {
  exact?: boolean;               // Exact match (default: true)
  normalizer?: (text: string) => string;  // Normalize whitespace
}
```

**Usage:**
```typescript
// Exact match (default)
screen.getByText('Hello World');

// Case-insensitive with regex
screen.getByText(/hello world/i);

// Partial match
screen.getByText('Hello', { exact: false });
```

### WaitForOptions

```typescript
interface WaitForOptions {
  timeout?: number;              // Default: 1000ms
  interval?: number;             // Check interval (default: 50ms)
}
```

**Usage:**
```typescript
// Custom timeout
const element = await screen.findByTestId('slow-element', {}, { timeout: 5000 });
```

## Query Method Selection

| Method | No Match | Multiple Matches | Await |
|--------|----------|------------------|-------|
| getBy* | Throw error | Return first | No |
| getAllBy* | Throw error | Return array | No |
| queryBy* | Return null | Return first | No |
| queryAllBy* | Return [] | Return array | No |
| findBy* | Throw error | Return first | Yes |
| findAllBy* | Throw error | Return array | Yes |

**When to use:**
- `getBy*`: Element must be present immediately
- `queryBy*`: Check element absence (`expect(...).not.toBeInTheDocument()`)
- `findBy*`: Element appears asynchronously

## waitFor()

Wait for assertion to pass.

```typescript
function waitFor<T>(
  callback: () => T | Promise<T>,
  options?: WaitForOptions
): Promise<T>;
```

**Usage:**
```typescript
await waitFor(() => {
  expect(screen.getByTestId('element')).toBeInTheDocument();
});

await waitFor(
  () => {
    expect(mockFn).toHaveBeenCalled();
  },
  { timeout: 3000 }
);
```

## act()

Wrap state updates to avoid warnings.

```typescript
function act(callback: () => void | Promise<void>): Promise<void>;
```

**Usage:**
```typescript
await act(() => {
  render(<Component />);
});

act(() => {
  result.current.setValue('new value');
});
```

**Note:** `userEvent` methods automatically wrap in `act()`.

## userEvent

Simulate realistic user interactions.

```typescript
import userEvent from '@testing-library/user-event';

// Click
userEvent.click(element: Element): Promise<void>;
userEvent.dblClick(element: Element): Promise<void>;

// Type
userEvent.type(element: Element, text: string, options?: TypeOptions): Promise<void>;
userEvent.clear(element: Element): Promise<void>;

// Keyboard
userEvent.keyboard(text: string): Promise<void>;
userEvent.tab(options?: TabOptions): Promise<void>;

// Select
userEvent.selectOptions(element: Element, values: string | string[]): Promise<void>;
userEvent.deselectOptions(element: Element, values: string | string[]): Promise<void>;

// Upload
userEvent.upload(element: Element, file: File | File[]): Promise<void>;

// Hover
userEvent.hover(element: Element): Promise<void>;
userEvent.unhover(element: Element): Promise<void>;

// Paste
userEvent.paste(text: string): Promise<void>;
```

### TypeOptions

```typescript
interface TypeOptions {
  delay?: number;                // Delay between keystrokes (ms)
  skipClick?: boolean;           // Skip initial click (default: false)
  skipAutoClose?: boolean;       // Skip auto-closing characters
}
```

**Usage:**
```typescript
// Click
await userEvent.click(button);
await userEvent.dblClick(button);

// Type
await userEvent.type(input, 'Hello World');
await userEvent.type(input, 'Slow typing', { delay: 100 });
await userEvent.clear(input);

// Keyboard
await userEvent.keyboard('{Enter}');
await userEvent.keyboard('{Shift>}A{/Shift}'); // Shift+A
await userEvent.tab();

// Select
await userEvent.selectOptions(select, 'option1');
await userEvent.selectOptions(select, ['option1', 'option2']);

// Upload
const file = new File(['content'], 'test.png', { type: 'image/png' });
await userEvent.upload(fileInput, file);

// Hover
await userEvent.hover(element);
await userEvent.unhover(element);

// Paste
await userEvent.paste('Pasted text');
```

### Keyboard Special Keys

```
{Enter}
{Escape}
{Backspace}
{Delete}
{Tab}
{Shift}
{Control}
{Alt}
{Meta}
{ArrowUp}
{ArrowDown}
{ArrowLeft}
{ArrowRight}
{Home}
{End}
{PageUp}
{PageDown}
```

## fireEvent (lower-level alternative)

Dispatch DOM events (less realistic than userEvent).

```typescript
fireEvent.click(element: Element): boolean;
fireEvent.change(element: Element, options: { target: { value: any } }): boolean;
fireEvent.submit(element: Element): boolean;
fireEvent.focus(element: Element): boolean;
fireEvent.blur(element: Element): boolean;
fireEvent.keyDown(element: Element, options: { key: string }): boolean;
fireEvent.keyUp(element: Element, options: { key: string }): boolean;
```

**Usage:**
```typescript
fireEvent.click(button);
fireEvent.change(input, { target: { value: 'text' } });
fireEvent.submit(form);
```

**Prefer:** `userEvent` over `fireEvent` for more realistic testing.

## renderHook()

Test custom hooks in isolation.

```typescript
function renderHook<Result, Props>(
  render: (props: Props) => Result,
  options?: RenderHookOptions<Props>
): RenderHookResult<Result, Props>;

interface RenderHookOptions<Props> {
  initialProps?: Props;
  wrapper?: React.ComponentType;
}

interface RenderHookResult<Result, Props> {
  result: { current: Result };
  rerender: (props?: Props) => void;
  unmount: () => void;
}
```

**Usage:**
```typescript
const { result } = renderHook(() => useCustomHook());

expect(result.current.value).toBe('initial');

act(() => {
  result.current.setValue('updated');
});

expect(result.current.value).toBe('updated');
```

## Jest API

### Test Structure

```typescript
describe(name: string, fn: () => void): void;
it(name: string, fn: () => void | Promise<void>): void;
test(name: string, fn: () => void | Promise<void>): void; // Alias for it

// Lifecycle
beforeAll(fn: () => void | Promise<void>): void;
beforeEach(fn: () => void | Promise<void>): void;
afterEach(fn: () => void | Promise<void>): void;
afterAll(fn: () => void | Promise<void>): void;
```

### Mock Functions

```typescript
// Create mock
jest.fn(): jest.Mock;
jest.fn(implementation: (...args: any[]) => any): jest.Mock;

// Mock methods
mockFn.mockReset(): void;                    // Clear calls and results
mockFn.mockClear(): void;                    // Clear calls only
mockFn.mockReturnValue(value: any): void;    // Return value
mockFn.mockReturnValueOnce(value: any): void;  // Return value once
mockFn.mockResolvedValue(value: any): void;  // Resolve promise
mockFn.mockRejectedValue(error: any): void;  // Reject promise
mockFn.mockImplementation(fn: Function): void;  // Custom implementation

// Clear all mocks
jest.clearAllMocks(): void;
jest.resetAllMocks(): void;
```

**Usage:**
```typescript
const mockFn = jest.fn();
mockFn.mockReturnValue('value');
mockFn.mockResolvedValue({ data: 'async' });

expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
```

### Module Mocking

```typescript
jest.mock(moduleName: string, factory?: () => any): void;
jest.unmock(moduleName: string): void;
jest.spyOn(object: any, methodName: string): jest.SpyInstance;
```

**Usage:**
```typescript
// Mock module
jest.mock('@/libs/router', () => ({
  useRouter: jest.fn(() => ({
    pathname: '/test',
    query: {},
  })),
}));

// Spy on method
const spy = jest.spyOn(console, 'error').mockImplementation(() => {});
```

## Jest DOM Matchers

Custom matchers from @testing-library/jest-dom.

```typescript
// Presence
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeEmptyDOMElement();

// Attributes
expect(element).toHaveAttribute('data-testid', 'value');
expect(element).toHaveClass('class-name');
expect(element).toHaveStyle({ color: 'red' });

// Text content
expect(element).toHaveTextContent('text');
expect(element).toContainHTML('<span>text</span>');

// Form elements
expect(input).toHaveValue('value');
expect(input).toHaveDisplayValue('display');
expect(checkbox).toBeChecked();
expect(input).toBeDisabled();
expect(input).toBeEnabled();
expect(input).toBeRequired();
expect(input).toBeInvalid();
expect(input).toBeValid();

// Focus
expect(element).toHaveFocus();

// Selection
expect(option).toBeSelected();
```

## Common Roles

ARIA roles for `getByRole()` queries:

- `button` - `<button>`, `<input type="button">`
- `checkbox` - `<input type="checkbox">`
- `radio` - `<input type="radio">`
- `textbox` - `<input type="text">`, `<textarea>`
- `link` - `<a href="...">`
- `heading` - `<h1>`, `<h2>`, etc.
- `img` - `<img>`
- `list` - `<ul>`, `<ol>`
- `listitem` - `<li>`
- `combobox` - `<select>`
- `option` - `<option>`
- `form` - `<form>`
- `table` - `<table>`
- `row` - `<tr>`
- `cell` - `<td>`, `<th>`
- `dialog` - `<dialog>`, `role="dialog"`
- `navigation` - `<nav>`
- `main` - `<main>`
- `banner` - `<header>`
- `contentinfo` - `<footer>`

## Best Practices

1. **Prefer accessible queries:**
   - `getByRole()` > `getByLabelText()` > `getByPlaceholderText()` > `getByTestId()`

2. **Use screen:**
   - Use `screen.*` instead of destructuring `render()`

3. **Use userEvent:**
   - Use `userEvent` over `fireEvent` for more realistic interactions

4. **Use findBy for async:**
   - Use `findBy*` for elements that appear asynchronously
   - Use `waitFor()` for complex async conditions

5. **Reset mocks:**
   - Reset mocks in `beforeEach` to prevent test interdependence

6. **Provide wrappers:**
   - Wrap components with providers for realistic testing

7. **Check accessibility:**
   - Use `getByRole()` to ensure proper ARIA attributes
