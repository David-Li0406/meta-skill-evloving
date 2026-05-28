# Template Literal Types

> **When to use:** For creating type-safe string patterns, such as for event names, CSS values, route parameters, or i18n keys.

Use template literals for string pattern types:

```typescript
// DO: Type-safe event names
type EventName = `on${Capitalize<'click' | 'focus' | 'blur'>}`;
// Result: 'onClick' | 'onFocus' | 'onBlur'

// DO: Type-safe CSS properties
type CSSUnit = 'px' | 'rem' | 'em' | '%';
type CSSValue = `${number}${CSSUnit}`;
// '10px', '1.5rem', '100%' are valid

const width: CSSValue = '100px';  // OK
const bad: CSSValue = '100';      // Error: missing unit

// DO: Type-safe route parameters
type Route = '/users/:userId' | '/posts/:postId';
type ExtractParam<TRoute extends string> =
  TRoute extends `${string}:${infer TParam}`
    ? TParam
    : never;

type UserParam = ExtractParam<'/users/:userId'>;  // 'userId'

// DO: Type-safe i18n keys
type Locale = 'en' | 'ja' | 'zh';
type I18nKey = 'greeting' | 'farewell';
type LocalizedKey = `${Locale}.${I18nKey}`;
// 'en.greeting' | 'en.farewell' | 'ja.greeting' | ...
```

## Common Patterns

| Pattern | Description |
|---------|-------------|
| `Capitalize<T>` | First letter uppercase |
| `Uppercase<T>` | All uppercase |
| `Lowercase<T>` | All lowercase |
| `${infer X}` | Extract parts of strings |

## Use Cases

| Scenario | Example |
|----------|---------|
| Event systems | `on${Capitalize<EventType>}` |
| CSS-in-JS | `${number}${CSSUnit}` |
| Route parameters | `${string}:${infer Param}` |
| i18n keys | `${Locale}.${Key}` |
| API endpoints | `/api/v${number}/${Resource}` |
