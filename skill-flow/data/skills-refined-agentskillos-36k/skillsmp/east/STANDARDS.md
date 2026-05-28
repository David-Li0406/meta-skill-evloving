# East Development Standards

**This document is MANDATORY and MUST be followed for all East development.**

All contributors MUST follow these standards for documentation and testing. These standards ensure consistency, correctness, and maintainability across the East codebase.

---

## Table of Contents

- [TypeDoc Documentation Standards](#typedoc-documentation-standards)
- [USAGE.md Documentation Standards](#usagemd-documentation-standards)
- [Testing Standards](#testing-standards)

---

## TypeDoc Documentation Standards

All public APIs MUST include TypeDoc comments following these precise rules.

### Classes

**Requirements:**
- Include a summary describing the class purpose
- Document key invariants or design decisions
- Use `@example` for non-trivial usage patterns
  - For **expression classes** (in `/src/expr/` or `/src/expr/libs/`): see [Examples for Expression Classes](#examples-for-expression-classes)
  - For **regular classes**: see [Examples for Regular Classes](#examples-for-regular-classes)
- Mark internal classes with `@internal`

**Example (Expression Class):**

```typescript
/**
 * Expression representing binary blob values and operations.
 *
 * BlobExpr provides methods for working with binary data including size queries,
 * byte access, text encoding/decoding (UTF-8, UTF-16), and BEAST binary format operations.
 * Blobs are immutable sequences of bytes.
 *
 * @example
 * ```ts
 * // Encoding and decoding text
 * const encodeText = East.function([StringType], BlobType, ($, text) => {
 *   $.return(text.encodeUtf8());
 * });
 *
 * const decodeText = East.function([BlobType], StringType, ($, blob) => {
 *   $.return(blob.decodeUtf8());
 * });
 *
 * // Working with blob bytes
 * const getByte = East.function([BlobType, IntegerType], IntegerType, ($, blob, offset) => {
 *   $.return(blob.getUint8(offset));
 * });
 * ```
 */
export class BlobExpr extends Expr<BlobType> {
  // ...
}
```

**Example (Regular Class):**

```typescript
/**
 * Represents a type-checked East expression with guaranteed type safety.
 *
 * This class wraps the IR representation and ensures all type constraints
 * are validated before serialization.
 *
 * @example
 * ```ts
 * const expr = new TypedExpr(IntegerType, {
 *   kind: 'Literal',
 *   value: 42n
 * });
 * const ir = expr.toIR();
 * ```
 */
export class TypedExpr { ... }
```

### Methods

**Requirements:**
- Document purpose relative to the class context
- Use `@param name - description` for all parameters (omit types, TypeScript infers them)
- Use `@returns description` for return value (omit type, TypeScript infers it)
- Use `@throws` for error conditions:
  - For **expression classes**: `@throws East runtime error if <condition>`
  - For **regular classes**: `@throws {ErrorType} <description>`
- Use `@remarks` for important usage notes or constraints
- Include `@example` for non-trivial methods
  - For **expression classes**: must use `East.function()` → `East.compile()` pattern
  - For **regular classes**: show typical usage
- Mark deprecated methods with `@deprecated` and alternatives

**Example (Expression Class Method):**

```typescript
/**
 * Gets the byte value at the specified offset.
 *
 * @param offset - The zero-based byte offset to read from
 * @returns An IntegerExpr representing the unsigned 8-bit integer (0-255) at that offset
 *
 * @throws East runtime error if the offset is out of bounds (< 0 or >= blob size)
 *
 * @example
 * ```ts
 * const getByte = East.function([BlobType, IntegerType], IntegerType, ($, blob, offset) => {
 *   $.return(blob.getUint8(offset));
 * });
 * const compiled = East.compile(getByte.toIR(), []);
 * const blob = new Uint8Array([72, 101, 108, 108, 111]); // "Hello"
 * compiled(blob, 0n);  // 72n (ASCII 'H')
 * compiled(blob, 1n);  // 101n (ASCII 'e')
 * // compiled(blob, 10n) would throw error (out of bounds)
 * ```
 */
getUint8(offset: IntegerExpr | bigint): IntegerExpr {
  // ...
}
```

### Types and Interfaces

**Requirements:**
- Provide a concise summary of what the type represents
- Document type parameters with `@typeParam Name - description` for generics
- Document each field/property with inline comments
- Use `@remarks` for important usage notes or constraints

**Example:**

```typescript
/**
 * Configuration for the East compiler backend.
 *
 * @remarks
 * Platform functions must be provided for the compiled code to execute.
 */
export interface CompilerOptions {
  /** Whether to freeze input data to prevent mutation */
  freezeInputs: boolean;
  /** Maximum recursion depth for function calls */
  maxDepth: number;
}

/**
 * A result type that can be either success or failure.
 *
 * @typeParam T - The type of the success value
 * @typeParam E - The type of the error value
 */
export type Result<T, E> =
  | { success: true, value: T }
  | { success: false, error: E };
```

### Functions

**Requirements:**
- Start with a verb describing what the function does
- Document type parameters with `@typeParam Name - description` for generics
- Document all parameters with `@param name - description` (omit types, TypeScript infers them)
- Document return value with `@returns description` (omit type, TypeScript infers it)
- Use `@throws {ErrorType}` for documented error conditions
- Include `@example` for complex functions

**Example:**

```typescript
/**
 * Compiles an East IR expression to executable JavaScript.
 *
 * @param expr - The type-checked IR expression to compile
 * @param platform - Platform-specific function implementations
 * @returns An executable JavaScript function
 * @throws {CompileError} When the IR contains unsupported constructs
 *
 * @example
 * ```ts
 * const fn = compile(expr, { log: console.log });
 * const result = fn({ x: 5, y: 10 });
 * ```
 */
export function compile(expr: IR, platform: Platform): Function { ... }

/**
 * Maps each element of an array using a transform function.
 *
 * @typeParam T - The type of elements in the input array
 * @typeParam U - The type of elements in the output array
 * @param array - The array to map over
 * @param fn - The transform function to apply to each element
 * @returns A new array with transformed elements
 */
export function map<T, U>(array: T[], fn: (item: T) => U): U[] { ... }
```

### General Rules

**MUST follow:**
- Write in present tense ("Returns the type" not "Will return the type")
- Be concise but complete - avoid redundant information
- Use proper markdown formatting for code references: \`Type\`, \`null\`, etc.
- Use `{@link SymbolName}` to create links to other documented types, functions, or classes
- Include `@internal` for implementation details not part of public API
- Group related overloads with a single comment on the first signature

**Linking Example:**

```typescript
/**
 * Represents the Never type in East's type system.
 *
 * @remarks
 * This is a {@link variant} with the "Never" tag, representing the bottom type.
 * See {@link option} for the standard nullable type pattern.
 */
export type NeverType = variant<"Never", null>;

/**
 * Attempts to get an element from an array.
 *
 * @param array - The array to index into
 * @param index - The zero-based index
 * @returns An {@link option} containing the element if found, or {@link none} if out of bounds
 */
export function tryGet<T>(array: T[], index: number): option<T> { ... }
```

### Examples for Expression Classes

**This section applies ONLY to expression classes and standard library classes in `/src/expr/` and `/src/expr/libs/`.**

**CRITICAL REQUIREMENT:** All TypeDoc `@example` blocks in expression classes MUST:
1. Use the complete `East.function()` → `East.compile()` → execution flow pattern
2. Be validated using the `mcp__east-mcp__east_compile` tool during development

**Pattern for Expression Methods:**

All examples for East expression methods (classes in `/src/expr/` and `/src/expr/libs/`) MUST use the complete `East.function()` → `East.compile()` → execution flow:

```typescript
/**
 * Returns the size of the blob in bytes.
 *
 * @returns An IntegerExpr representing the number of bytes
 *
 * @example
 * ```ts
 * const getSize = East.function([BlobType], IntegerType, ($, blob) => {
 *   $.return(blob.size());
 * });
 * const compiled = East.compile(getSize.toIR(), []);
 * const text = "hello";
 * const blob = new TextEncoder().encode(text);
 * compiled(blob);  // 5n (5 bytes for "hello")
 * ```
 */
```

**Example Rules:**

* **MUST show complete executable code**: Include function definition with `East.function()`, compilation with `East.compile()`, and execution
* **MUST use separate `@example` blocks for different use cases**: Don't combine multiple examples in a single block with `compiled2`, `compiled3`, etc.
* **MUST use consistent naming**: Always use `const compiled =` for the compiled function (never `compiled2` or other variants)
* **MUST include inline comments for results**: Show expected output in comments after function calls
* **MUST use descriptive function names**: Name the East function descriptively (e.g., `makeRange`, `filterEvens`, `sumArray`)
* **SHOULD add context comments**: Use comments like `// With custom step` to clarify what the example demonstrates
* **SHOULD show both simple and complex cases**: First example shows basic usage, subsequent examples show variations or advanced features
* **MUST use proper East literals**: Remember `1n` for integers, `1.0` for floats, proper type constructors like `ArrayType(IntegerType)`

**Common Patterns:**

```typescript
// Instance method example
/**
 * @example
 * ```ts
 * const doubleNumbers = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
 *   $.return(arr.map(($, x, i) => x.multiply(2n)));
 * });
 * const compiled = East.compile(doubleNumbers.toIR(), []);
 * compiled([1n, 2n, 3n]);  // [2n, 4n, 6n]
 * ```
 */

// Static/library function example
/**
 * @example
 * ```ts
 * const makeLinspace = East.function([], ArrayType(FloatType), ($) => {
 *   $.return(East.Array.linspace(0.0, 1.0, 5n));
 * });
 * const compiled = East.compile(makeLinspace.toIR(), []);
 * compiled();  // [0.0, 0.25, 0.5, 0.75, 1.0]
 * ```
 */

// Mutation example
/**
 * @example
 * ```ts
 * const appendValue = East.function([ArrayType(IntegerType), IntegerType], ArrayType(IntegerType), ($, arr, value) => {
 *   $(arr.pushLast(value));  // Mutate the array
 *   $.return(arr);
 * });
 * const compiled = East.compile(appendValue.toIR(), []);
 * const myArray = [1n, 2n, 3n];
 * compiled(myArray, 4n);  // [1n, 2n, 3n, 4n]
 * ```
 */
```

**Validation Process for Expression Classes:**

When adding or modifying examples in `/src/expr/` or `/src/expr/libs/`:
1. Extract the East code from the example block
2. Use `mcp__east-mcp__east_compile` tool to validate it compiles without errors
3. If compilation fails, fix the example code
4. Only commit examples that successfully compile

### Examples for Regular Classes

**This section applies to all other classes (NOT in `/src/expr/` or `/src/expr/libs/`).**

For regular classes (compiler, IR, types, etc.), examples MUST:
- Show typical usage patterns
- Use realistic code that would actually run
- Be concise and focused on the API being documented
- NOT use the `East.function()` → `East.compile()` pattern
- NOT be validated with `mcp__east-mcp__east_compile` (not applicable)

**Example for regular class:**

```typescript
/**
 * Compiles an East IR expression to executable JavaScript.
 *
 * @param expr - The type-checked IR expression to compile
 * @param platform - Platform-specific function implementations
 * @returns An executable JavaScript function
 * @throws {CompileError} When the IR contains unsupported constructs
 *
 * @example
 * ```ts
 * const ir = myEastFunction.toIR();
 * const compiled = East.compile(ir, [log.implement(console.log)]);
 * const result = compiled({ x: 5, y: 10 });
 * console.log(result);  // Expected output
 * ```
 */
export function compile(expr: IR, platform: Platform): Function { ... }
```

---

## USAGE.md Documentation Standards

`USAGE.md` is the **end-user facing documentation** for the East language. It MUST follow these precise formatting and organization standards.

### Type Section Structure

Each type MUST have a section following this exact structure:

```markdown
### TypeName

Brief description of what the type represents and key characteristics.

**Example:**
```typescript
// Complete working example showing typical usage
import { East, TypeName, ... } from "@elaraai/east";

const exampleFunction = East.function([...], ..., ($, ...) => {
    // Create values with $.let() and East.value() (type inference)
    const value1 = $.let(East.value(...));

    // Alternative: Create values with $.let() and East.value() with explicit type
    const value2 = $.let(East.value(..., TypeName));

    // Show typical operations
    const result = ...;

    $.return(result);
});

const compiled = East.compile(exampleFunction, []);
console.log(compiled(...));  // Expected output
```

**Operations:**
| Signature | Description | Example |
|-----------|-------------|---------|
| **Category Name** |
| `methodName(param: Type): ReturnType` | Description | `instance.methodName(arg)` |
| `methodName(param: Type): ReturnType` **❗** | Description (can throw) | `instance.methodName(arg)` |

**Standard Library:** See [STDLIB.md](./STDLIB.md#typename) for additional utilities.

---
```

### Operations Table Rules

**MUST follow:**
- Three columns: `Signature | Description | Example`
- Group operations by category using bold headers: `| **Category Name** |`
- Use `**❗**` after return type for operations that can throw errors
- Show complete type signatures including parameter types
- Provide concise, actionable descriptions
- Give simple, inline usage examples

**Common Categories:**
- `**Base Operations**` - Core functionality
- `**Read Operations**` - Query operations (no mutation)
- `**Mutation Operations**` - In-place modifications
- `**Functional Operations**` or `**Functional Operations (Immutable)**` - Return new values
- `**Conversion Operations**` - Type conversions
- `**Comparison Operations**` - Equality/ordering
- `**Reduction Operations**` - Aggregations
- `**Grouping Operations**` - Group-by operations
- `**Short-Circuiting Operations**` / `**Non-Short-Circuiting Operations**` - For boolean logic

**Example:**

```markdown
| Signature | Description | Example |
|-----------|-------------|---------|
| **Read Operations** |
| `size(): IntegerExpr` | Get array length | `array.size()` |
| `has(index: IntegerExpr \| bigint): BooleanExpr` | Check if index is valid (0 ≤ index < size) | `array.has(5n)` |
| `get<V extends EastType>(index: IntegerExpr \| bigint): ExprType<V>` **❗** | Get element (errors if out of bounds) | `array.get(0n)` |
| **Mutation Operations** |
| `pushLast<V extends EastType>(value: ExprType<V> \| ValueTypeOf<V>): NullExpr` | Append to end | `array.pushLast(42n)` |
| `clear(): NullExpr` | Remove all elements | `array.clear()` |
```

### Example Block Rules

**Top-level examples** (in type sections) MUST:
- Show complete, executable code
- Import necessary types from `@elaraai/east`
- Demonstrate the most common use case for the type
- Show BOTH ways to create values:
  - Type inference: `const x = $.let(East.value(...))`
  - Explicit type: `const x = $.let(East.value(..., TypeName))`
- Include expected output in comments
- Use realistic variable names and scenarios

**Method examples** (in operations tables) MUST:
- Be concise one-liners showing usage
- Not include imports or full function definitions
- Focus on the method call syntax

### Formatting Rules

**MUST follow:**
- Use **three backticks** for code blocks: \`\`\`typescript
- Use **single backticks** for inline code: \`TypeName\`
- Use **bold** for emphasis: **mutable**, **immutable**
- Use **❗** emoji for error-throwing operations
- Use `|` for union types: `IntegerExpr | bigint`
- Escape `|` in table cells: `IntegerExpr \| bigint`
- Use arrow syntax for callbacks: `($, x) => ...`
- Show types in signatures but NOT in parameter descriptions

**Notes sections:**
- Add a `**Notes:**` or `**Important notes:**` section after operations for critical information
- Use bullet points for multiple notes
- Keep notes concise and actionable

---

## Testing Standards

All East functionality MUST be thoroughly tested using the self-hosted test platform in `/test`.

### Test File Structure

**Requirements:**
- One test file per type/feature: `test/typename.spec.ts`
- Import test infrastructure from `platforms.spec.js`:
  ```typescript
  import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";
  ```
- Use `describe` for the top-level test suite
- Use `test` method for individual test cases
- Each test MUST be a complete East function

**Example:**

```typescript
import {
  East,
  ArrayType, IntegerType, BooleanType,
} from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

describe("Array", (test) => {
    test("Array ops", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).size(), 0n))
        $(assert.equal(East.value([1n, 2n, 3n]).size(), 3n))

        $(assert.equal(East.value([10n, 20n, 30n]).has(0n), true))
        $(assert.equal(East.value([10n, 20n, 30n]).has(3n), false))

        $(assert.throws(East.value([10n, 20n, 30n]).get(-1n)))
        $(assert.equal(East.value([10n, 20n, 30n]).get(0n), 10n))
    });

    test("Mutation", $ => {
        const a = $.let([], ArrayType(IntegerType))
        $(assert.equal(a, []))

        $(a.pushLast(1n))
        $(assert.equal(a, [1n]))

        $(a.pushLast(2n))
        $(assert.equal(a, [1n, 2n]))
    });
});
```

### Test Coverage Requirements

**MUST test:**
- **Basic operations**: Core functionality with typical inputs
- **Edge cases**: Empty collections, zero values, boundary conditions
- **Error conditions**: Operations that should throw (use `assert.throws`)
- **Mutation**: Both the mutation operation AND the resulting state
- **Type variations**: Different type parameters where applicable

**Example coverage for a method:**

```typescript
// Basic operation
$(assert.equal(East.value([1n, 2n, 3n]).get(0n), 10n))

// Edge cases
$(assert.throws(East.value([10n, 20n, 30n]).get(-1n)))  // Negative index
$(assert.throws(East.value([10n, 20n, 30n]).get(3n)))   // Out of bounds

// With default function
$(assert.equal(East.value([10n, 20n, 30n]).get(3n, _ => 40n), 40n))

// With tryGet (option variant)
$(assert.equal(East.value([10n, 20n, 30n]).tryGet(2n), some(30n)))
$(assert.equal(East.value([10n, 20n, 30n]).tryGet(3n), none))
```

### Test Naming and Organization

**Test names MUST:**
- Be concise and descriptive
- Use lowercase with spaces: `"Array ops"`, `"Mutation"`, `"UTF-8 decoding/encoding"`
- Group related functionality: `"Beast v1 - Null type"`, `"Beast v1 - Boolean type"`

**Test organization:**
- Group tests by functionality, not by alphabetical order
- Start with basic operations, then move to advanced features
- Put error condition tests at the end of each group

### Assertion Patterns

**Available assertions:**
```typescript
$(assert.equal(actual, expected))         // Deep equality
$(assert.notEqual(actual, expected))      // Deep inequality
$(assert.throws(expression))              // Expects error
```

**Best practices:**
- Use `$.let()` for complex values that are reused
- Use direct `East.value()` for simple, single-use values
- Always show the expected behavior in comments when not obvious
- Test round-trip operations (encode → decode, serialize → deserialize)

---

## Compliance

**These standards are MANDATORY.**

- All pull requests MUST comply with these standards
- Code review MUST verify compliance
- No exceptions without explicit approval from the project maintainer

**Before committing:**
1. ✅ All public APIs have TypeDoc comments following these standards
2. ✅ All TypeDoc examples in **expression classes** (`/src/expr/` and `/src/expr/libs/`) compile successfully (validated with `mcp__east-mcp__east_compile`)
3. ✅ USAGE.md documentation follows the formatting and organization standards
4. ✅ All new functionality has comprehensive test coverage
5. ✅ All tests pass: `npm run test`
6. ✅ Linting passes: `npm run lint`

**When in doubt, refer to:**
- `/src/expr/blob.ts` for TypeDoc examples
- `/USAGE.md` sections for Array, Dict, Set for USAGE.md examples
- `/test/blob.spec.ts` and `/test/array.spec.ts` for testing examples
