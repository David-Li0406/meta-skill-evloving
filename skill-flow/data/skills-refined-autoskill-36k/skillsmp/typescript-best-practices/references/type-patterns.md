# Type Design Patterns

## Type Declarations: interface vs type

| Use | When |
|-----|------|
| `interface` | Object structures, class contracts, extensible APIs |
| `type` | Union types, mapped types, conditional types, tuples |

```typescript
// DO: interface for objects
interface User { id: string }

// DO: type for unions
type Status = 'active' | 'inactive';

// DO: type for mapped types
type NullableProps<TObj> = { [TProp in keyof TObj]: TObj[TProp] | null };
```

## Array Type Syntax

| DO | DON'T |
|----|-------|
| `Array<TItem>` | `TItem[]` |
| `ReadonlyArray<TItem>` | `readonly TItem[]` |

```typescript
// DO: Generic syntax is more explicit
type Users = Array<User>;
type ReadonlyUsers = ReadonlyArray<User>;
type Matrix = Array<Array<number>>;

// DON'T: Bracket syntax is less visible
type Users = User[];
type Matrix = number[][];
```

**Why prefer `Array<T>`:**
- More explicit and visible than `[]` suffix
- Consistent with other generic types (`Map<K, V>`, `Set<T>`, `Promise<T>`)
- Nested arrays are more readable: `Array<Array<T>>` vs `T[][]`

## Object Type Syntax

Avoid `{}` as it accepts almost anything. Use explicit types:

| Use Case | DO | DON'T |
|----------|-----|-------|
| Empty object | `Record<string, never>` | `{}` |
| Any object (extends) | `Record<string, any>` | `Record<string, unknown>` |
| Any object (annotation) | `Record<string, unknown>` | `Record<string, any>` |
| Non-primitive | `object` | `{}` |

```typescript
// DO: Empty object type
type EmptyObject = Record<string, never>;

// DO: Generic constraint (use any for extends)
function merge<TObj extends Record<string, any>>(target: TObj, source: TObj): TObj;

// DO: Type annotation (use unknown)
const config: Record<string, unknown> = {};

// DON'T: {} accepts almost anything
type BadEmpty = {};
const bad: BadEmpty = { unexpected: 'property' };  // No error!
```

## any Usage

| DO | DON'T |
|----|-------|
| `<TFunc extends (...args: Array<any>) => any>` | `const data: any = response` |
| Use `unknown` for truly unknown types | Use `any` to silence errors |
| Parse with zod/arktype, then use inferred type | Cast with `as any` |

```typescript
// DO: Use any only in generic constraints
function debounce<TFunc extends (...args: Array<any>) => any>(
  func: TFunc,
  wait: number
): TFunc;

// DO: Runtime validation for unknown data
import { z } from 'zod';
const UserSchema = z.object({ id: z.string(), name: z.string() });
const user = UserSchema.parse(response); // typed as User

// DON'T: Use any to bypass type checking
const data: any = await fetch('/api/user').then(r => r.json());
```

## Avoid `as` and `!` Assertions

`as` and `!` bypass type checking and create "type lies."

| DO | DON'T |
|----|-------|
| Zod/arktype for runtime validation | `response as User` |
| `satisfies` for compile-time checks | `value as unknown as Type` |
| Type guards (`if ('prop' in obj)`) | `as any` to silence errors |
| Explicit null checks | `x!` non-null assertion |

```typescript
// DO: Runtime validation
const user = UserSchema.parse(response);

// DO: satisfies for compile-time checking
const config = { port: 3000 } satisfies ServerConfig;

// DO: Type guard
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value;
}

// DO: Explicit null check
const element = document.getElementById('app');
if (element === null) throw new Error('Element not found');
element.textContent = 'Hello';

// DON'T: Assertions without validation
const unsafeUser = response as User;
const unsafeElement = document.getElementById('app')!;
```

**When `as` is acceptable:**

| Context | Example | Why OK |
|---------|---------|--------|
| `as const` | `{ key: 'value' } as const` | Narrows to literal, not a type lie |
| Type test files | `anyObj as Result satisfies Expected` | Testing type behavior |
| After exhaustive narrowing | `as never` in default case | Proves unreachable |

## Function Declarations

| DO | DON'T |
|----|-------|
| `const fn: MyType = (arg) => { }` | `const fn = (arg: ArgType): RetType => { }` |
| `const fn = ((arg) => { }) satisfies MyType` | `function fn(arg: ArgType): RetType { }` |

```typescript
// DO: Type on the const, implementation infers params
const myFunction: myFunction.Type = (options) => {
  // options is typed from myFunction.Type
};

// DO: satisfies when namespace doesn't exist
const onClick = ((event) => {
  // implementation
}) satisfies React.ComponentProps<'button'>['onClick'];

// DON'T: Redundant inline type annotations
const bad = (options: myFunction.Options): myFunction.Ret => {};
```

## Type Extraction

| DO | DON'T |
|----|-------|
| `React.ComponentProps<'button'>['onClick']` | `(e: React.MouseEvent<HTMLButtonElement>) => void` |
| `NonNullable<typeof config['timeout']>` | Manually redefine the type |
| `Parameters<typeof fn>[0]` | Copy parameter types manually |

```typescript
// DO: Extract from existing definitions
type OnClick = React.ComponentProps<'button'>['onClick'];
type ItemIds = Array<Item['id']>;
type TimeoutType = NonNullable<typeof config['timeout']>;

// DON'T: Redefine types that already exist
type BadItemIds = Array<number>; // Won't update if Item.id changes
```

## Generic Constants

| DO | DON'T |
|----|-------|
| `defineConfig<const TConfig>(config: TConfig)` | Lose literal types with regular generics |
| `as const satisfies BaseConfig` | `as BaseConfig` (loses specificity) |

```typescript
// DO: const generic for strict inference
function defineConfig<const TConfig extends BaseConfig>(config: TConfig): TConfig {
  return config;
}

const strictConfig = defineConfig({
  routes: ['/home', '/about'], // readonly ['/home', '/about']
  debug: true,
});

// DO: as const satisfies for one-off definitions
const literalConfig = {
  routes: ['/home', '/about'],
} as const satisfies BaseConfig;

// DON'T: Lose literal types
const looseConfig: BaseConfig = {
  routes: ['/home', '/about'], // widened to Array<string>
};
```

## Namespace Pattern for Type Organization

Group related types with function using namespace. Put documentation on the namespace.

```typescript
/**
 * Creates a debounced function that delays invoking `func` until after
 * `wait` milliseconds have elapsed since the last invocation.
 */
namespace debounce {
  export interface Options {
    wait: number;
    immediate: boolean;
  }
  export type Ret = () => void;
  export type Type = (func: (...args: unknown[]) => void, options: Options) => Ret;
}

const debounce: debounce.Type = (func, options) => {
  // implementation
};

export { debounce };
```

| DO | DON'T |
|----|-------|
| `namespace myFunc { export interface Options {} }` | `namespace Utils { export function helper() {} }` |
| Group types with their function | Use namespace for runtime code |
| Types only in namespaces | Mix types and implementation |

## Multiple Call Signatures

When a function has overloads, define separate interfaces and extend.

```typescript
// DO: Extend separate interfaces
namespace myFunction {
  export interface TypeBasic {
    (options: Options): Ret;
  }
  export interface TypeWithExtra {
    (options: Options, extra: boolean): RetWithExtra;
  }
  export interface Type extends TypeBasic, TypeWithExtra {}
}

// DON'T: Define all signatures in one interface
namespace myFunction {
  export interface Type {
    (options: Options): Ret;
    (options: Options, extra: boolean): RetWithExtra;
  }
}
```

**Why separate interfaces?**
- Each signature can be reused independently
- Simplifies runtime implementation
- Better type inference for polymorphic components

## Function with Additional Properties

For functions with properties (like `myFunc.defaultOptions`):

```typescript
namespace myFunction {
  export interface Options { wait: number; immediate: boolean; }
  export type Ret = () => void;
  export type TypeImpl = (options: Options) => Ret;
  export interface AllInOneProps { defaultOptions: Options; }
  export type Type = TypeImpl & AllInOneProps;
}

const myFunctionImpl: myFunction.TypeImpl = (options) => {};
const myFunction: myFunction.Type = Object.assign(myFunctionImpl, {
  defaultOptions: { wait: 300, immediate: false },
});
```

### Tree-Shaking Considerations

| Pattern | When to Use |
|---------|-------------|
| All-in-one props | Features frequently used together (`Select.Option`) |
| Separate exports | Independent features (`AutoComplete` - adds bundle size) |

## Generic Defaults for Better DX

### Default Type for Narrowing

```typescript
function logError<TError = Error>(error: TError) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

### StringOrLiteral Pattern

Allow both known literal values (with autocomplete) and arbitrary strings:

```typescript
type StringOrLiteral<TLiteral extends string> = TLiteral | (string & {});

function on<TEvent extends string = 'click' | 'focus' | 'blur'>(
  event: StringOrLiteral<TEvent>,
  handler: () => void,
) {}

on('click', () => {});   // Autocomplete suggests known values
on('custom', () => {});  // Also accepts arbitrary strings
```
