# East API Reference

Complete function signatures, types, and arguments for the East language.

---

## Table of Contents

- [East Namespace](#east-namespace)
  - [Patch Operations](#patch-operations)
- [BlockBuilder Operations](#blockbuilder-operations)
- [Types](#types)
  - [Patch Types](#patch-types)
- [Boolean Expressions](#boolean-expressions)
- [Integer Expressions](#integer-expressions)
- [Float Expressions](#float-expressions)
- [String Expressions](#string-expressions)
- [DateTime Expressions](#datetime-expressions)
- [Blob Expressions](#blob-expressions)
- [Array Expressions](#array-expressions)
- [Set Expressions](#set-expressions)
- [Dict Expressions](#dict-expressions)
- [Struct Expressions](#struct-expressions)
- [Variant Expressions](#variant-expressions)
- [Ref Expressions](#ref-expressions)
- [Standard Library](#standard-library)

---

## East Namespace

Main entry point for building East programs.

### Expression Creation

| Signature | Description |
|-----------|-------------|
| `East.value<V>(val: ValueTypeOf<V>): Expr<V>` | Create expression from JavaScript value |
| `East.value<T extends EastType>(val: Expr<T> \| ValueTypeOf<T>, type: T): Expr<T>` | Create expression with explicit type |
| <code>East.str\`...\`: StringExpr</code> | String interpolation template |
| `East.print<T extends EastType>(expr: Expr<T>): StringExpr` | Convert any expression to string |

### Function Definition

| Signature | Description |
|-----------|-------------|
| `East.function<I extends EastType[], O extends EastType>(inputs: I, output: O, body: ($, ...args) => Expr \| value): FunctionExpr` | Define synchronous function |
| `East.asyncFunction<I extends EastType[], O extends EastType>(inputs: I, output: O, body: ($, ...args) => Expr \| value): FunctionExpr` | Define asynchronous function |
| `East.compile<I extends EastType[], O extends EastType>(fn: FunctionExpr<I, O>, platform: PlatformFunction[]): (...inputs) => ValueTypeOf<O>` | Compile to executable JavaScript |
| `East.compileAsync<I extends EastType[], O extends EastType>(fn: FunctionExpr<I, O>, platform: PlatformFunction[]): (...inputs) => Promise<ValueTypeOf<O>>` | Compile async function |
| `East.platform<I extends EastType[], O extends EastType>(name: string, inputs: I, output: O): PlatformHelper` | Create sync platform function helper |
| `East.asyncPlatform<I extends EastType[], O extends EastType>(name: string, inputs: I, output: O): PlatformHelper` | Create async platform function helper |

### Comparisons

All comparison functions have multiple aliases for convenience:

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `East.equal<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `equals`, `eq` | Deep equality |
| `East.notEqual<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `notEquals`, `ne` | Deep inequality |
| `East.less<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `lessThan`, `lt` | Less than (total ordering) |
| `East.lessEqual<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `lessThanOrEqual`, `lte`, `le` | Less than or equal |
| `East.greater<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `greaterThan`, `gt` | Greater than |
| `East.greaterEqual<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | `greaterThanOrEqual`, `gte`, `ge` | Greater than or equal |
| `East.is<T extends DataType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): BooleanExpr` | | Reference equality (mutable types) |

### Utilities

| Signature | Description |
|-----------|-------------|
| `East.min<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): Expr<T>` | Minimum (total ordering) |
| `East.max<T extends EastType>(a: Expr<T>, b: Expr<T> \| ValueTypeOf<T>): Expr<T>` | Maximum (total ordering) |
| `East.clamp<T extends EastType>(x: Expr<T>, min: Expr<T> \| ValueTypeOf<T>, max: Expr<T> \| ValueTypeOf<T>): Expr<T>` | Clamp between min and max |

### Patch Operations

| Signature | Description |
|-----------|-------------|
| `East.diff<T extends EastType>(before: Expr<T>, after: Expr<T>): Expr<PatchType<T>>` | Compute structural difference between two values |
| `East.applyPatch<T extends EastType>(value: Expr<T>, patch: Expr<PatchType<T>>): Expr<T>` | Apply a patch to a value |
| `East.composePatch<T extends EastType>(first: Expr<PatchType<T>>, second: Expr<PatchType<T>>, type: T): Expr<PatchType<T>>` | Combine two patches into one |
| `East.invertPatch<T extends EastType>(patch: Expr<PatchType<T>>, type: T): Expr<PatchType<T>>` | Invert a patch (for undo operations) |

---

## BlockBuilder Operations

The first argument (`$`) in function body provides scope operations.

### Variables

| Signature | Description |
|-----------|-------------|
| `$.const<V>(value: ValueTypeOf<V>): Expr<V>` | Declare immutable variable (infers type) |
| `$.const<T extends EastType>(value: Expr<T> \| ValueTypeOf<T>, type: T): Expr<T>` | Declare with explicit type |
| `$.let<V>(value: ValueTypeOf<V>): Expr<V>` | Declare mutable variable (infers type) |
| `$.let<T extends EastType>(value: Expr<T> \| ValueTypeOf<T>, type: T): Expr<T>` | Declare with explicit type |
| `$.assign<T extends EastType>(variable: Expr<T>, value: Expr<T> \| ValueTypeOf<T>): NullExpr` | Reassign mutable variable |

### Execution

| Signature | Description |
|-----------|-------------|
| `$<T extends EastType>(expr: Expr<T>): Expr<T>` | Execute expression (for side effects) |
| `$.return<Ret>(value: Expr<Ret> \| ValueTypeOf<Ret>): NeverExpr` | Early return |
| `$.error(message: StringExpr \| string, location?: Location): NeverExpr` | Throw error |

### Control Flow

| Signature | Description |
|-----------|-------------|
| `$.if(condition: BooleanExpr \| boolean, body: ($: BlockBuilder) => void \| Expr): IfBuilder` | If statement (chain `.elseIf()`, `.else()`) |
| `$.while(condition: BooleanExpr \| boolean, body: ($: BlockBuilder, label: Label) => void \| Expr): NullExpr` | While loop |
| `$.for<T>(array: ArrayExpr<T>, body: ($: BlockBuilder, value: ExprType<T>, index: IntegerExpr, label: Label) => void): NullExpr` | For loop over array |
| `$.for<K>(set: SetExpr<K>, body: ($: BlockBuilder, key: ExprType<K>, label: Label) => void): NullExpr` | For loop over set |
| `$.for<K, V>(dict: DictExpr<K, V>, body: ($: BlockBuilder, value: ExprType<V>, key: ExprType<K>, label: Label) => void): NullExpr` | For loop over dict |
| `$.break(label: Label): NeverExpr` | Break from loop |
| `$.continue(label: Label): NeverExpr` | Continue to next iteration |
| `$.match<Cases>(variant: VariantExpr<Cases>, cases: { [Tag in keyof Cases]: ($: BlockBuilder, data: ExprType<Cases[Tag]>) => void \| Expr }): NullExpr` | Pattern match (statement form) |

### Error Handling

| Signature | Description |
|-----------|-------------|
| `$.try(body: ($: BlockBuilder) => void \| Expr)` | Try block; chain `.catch()` and/or `.finally()` |
| `.catch(body: ($: BlockBuilder, message: StringExpr, stack: ArrayExpr<StackFrame>) => void \| Expr)` | Handle errors |
| `.finally(body: ($: BlockBuilder) => void \| Expr)` | Cleanup (always executes) |

---

## Types

### Primitive Types

```typescript
import { NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType } from "@elaraai/east";
```

### Collection Types

```typescript
import { ArrayType, SetType, DictType, RefType } from "@elaraai/east";

ArrayType(IntegerType)                    // Array of integers
SetType(StringType)                       // Set of strings
DictType(StringType, IntegerType)         // Dict with string keys, integer values
RefType(IntegerType)                      // Mutable reference to integer
```

### Compound Types

```typescript
import { StructType, VariantType, RecursiveType } from "@elaraai/east";

// Product type (record)
const PersonType = StructType({ name: StringType, age: IntegerType });

// Sum type (tagged union)
const OptionType = VariantType({ some: IntegerType, none: NullType });

// Recursive type (trees, DAGs)
const TreeType = RecursiveType((self) => StructType({ value: IntegerType, children: ArrayType(self) }));
```

### Function Types

```typescript
import { FunctionType, AsyncFunctionType } from "@elaraai/east";

FunctionType([IntegerType, IntegerType], IntegerType)  // (int, int) => int
AsyncFunctionType([StringType], BlobType)              // async (string) => blob
```

### Patch Types

```typescript
import { PatchType } from "@elaraai/east";

PatchType(IntegerType)     // Patch for Integer → VariantType<{ unchanged, replace }>
PatchType(ArrayType(T))    // Patch for Array → VariantType<{ unchanged, replace, patch }>
PatchType(StructType(...)) // Patch for Struct → VariantType<{ unchanged, replace, patch }>
```

Patch types are variant types with these cases:
- `unchanged`: No changes (value is `null`)
- `replace`: Complete replacement (value is `{ before: T, after: T }`)
- `patch`: Structural changes (only for compound types like Array, Dict, Set, Struct, Variant)

---

## Boolean Expressions

### Short-Circuiting Operations

| Signature | Description |
|-----------|-------------|
| `x.not(): BooleanExpr` | Logical NOT |
| `x.and(y: ($: BlockBuilder) => BooleanExpr \| boolean): BooleanExpr` | Logical AND (short-circuit) |
| `x.or(y: ($: BlockBuilder) => BooleanExpr \| boolean): BooleanExpr` | Logical OR (short-circuit) |
| `condition.ifElse<T>(thenFn: ($: BlockBuilder) => ExprType<T>, elseFn: ($: BlockBuilder) => ExprType<T>): ExprType<T>` | Conditional (ternary) |

### Non-Short-Circuiting Operations

| Signature | Description |
|-----------|-------------|
| `x.bitAnd(y: BooleanExpr \| boolean): BooleanExpr` | Bitwise AND |
| `x.bitOr(y: BooleanExpr \| boolean): BooleanExpr` | Bitwise OR |
| `x.bitXor(y: BooleanExpr \| boolean): BooleanExpr` | Bitwise XOR |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `x.equals(other: BooleanExpr \| boolean): BooleanExpr` | `equal`, `eq` | Check equality |
| `x.notEquals(other: BooleanExpr \| boolean): BooleanExpr` | `notEqual`, `ne` | Check inequality |

---

## Integer Expressions

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `x.negate(): IntegerExpr` | | Unary negation |
| `x.add(y: IntegerExpr \| bigint): IntegerExpr` | `plus` | Addition |
| `x.subtract(y: IntegerExpr \| bigint): IntegerExpr` | `sub`, `minus` | Subtraction |
| `x.multiply(y: IntegerExpr \| bigint): IntegerExpr` | `mul`, `times` | Multiplication |
| `x.divide(y: IntegerExpr \| bigint): IntegerExpr` | `div` | Integer division (floored), `0 / 0 = 0` |
| `x.remainder(y: IntegerExpr \| bigint): IntegerExpr` | `mod`, `rem`, `modulo` | Remainder (floored modulo) |
| `x.pow(y: IntegerExpr \| bigint): IntegerExpr` | | Exponentiation |
| `x.abs(): IntegerExpr` | | Absolute value |
| `x.sign(): IntegerExpr` | | Sign (-1, 0, or 1) |
| `x.log(base: IntegerExpr \| bigint): IntegerExpr` | | Logarithm (floored, custom base) |
| `x.toFloat(): FloatExpr` | | Convert to float (may be approximate) |
| `x.equals(other: IntegerExpr \| bigint): BooleanExpr` | `equal`, `eq` | Check equality |
| `x.notEquals(other: IntegerExpr \| bigint): BooleanExpr` | `notEqual`, `ne` | Check inequality |
| `x.greaterThan(other: IntegerExpr \| bigint): BooleanExpr` | `greater`, `gt` | Greater than |
| `x.lessThan(other: IntegerExpr \| bigint): BooleanExpr` | `less`, `lt` | Less than |
| `x.greaterThanOrEqual(other: IntegerExpr \| bigint): BooleanExpr` | `greaterEqual`, `gte`, `ge` | Greater than or equal |
| `x.lessThanOrEqual(other: IntegerExpr \| bigint): BooleanExpr` | `lessEqual`, `lte`, `le` | Less than or equal |

---

## Float Expressions

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `x.negate(): FloatExpr` | | Unary negation |
| `x.add(y: FloatExpr \| number): FloatExpr` | `plus` | Addition |
| `x.subtract(y: FloatExpr \| number): FloatExpr` | `sub`, `minus` | Subtraction |
| `x.multiply(y: FloatExpr \| number): FloatExpr` | `mul`, `times` | Multiplication |
| `x.divide(y: FloatExpr \| number): FloatExpr` | `div` | Division, `0.0 / 0.0 = NaN` |
| `x.remainder(y: FloatExpr \| number): FloatExpr` | `mod`, `rem`, `modulo` | Remainder (floored modulo) |
| `x.pow(y: FloatExpr \| number): FloatExpr` | | Exponentiation |
| `x.abs(): FloatExpr` | | Absolute value |
| `x.sign(): FloatExpr` | | Sign (-1, 0, or 1) |
| `x.sqrt(): FloatExpr` | | Square root |
| `x.exp(): FloatExpr` | | Exponential (e^x) |
| `x.log(): FloatExpr` | | Natural logarithm |
| `x.sin(): FloatExpr` | | Sine |
| `x.cos(): FloatExpr` | | Cosine |
| `x.tan(): FloatExpr` | | Tangent |
| `x.toInteger(): IntegerExpr` | | Convert to integer (throws if not exact) |
| `x.equals(other: FloatExpr \| number): BooleanExpr` | `equal`, `eq` | Check equality |
| `x.notEquals(other: FloatExpr \| number): BooleanExpr` | `notEqual`, `ne` | Check inequality |
| `x.greaterThan(other: FloatExpr \| number): BooleanExpr` | `greater`, `gt` | Greater than |
| `x.lessThan(other: FloatExpr \| number): BooleanExpr` | `less`, `lt` | Less than |
| `x.greaterThanOrEqual(other: FloatExpr \| number): BooleanExpr` | `greaterEqual`, `gte`, `ge` | Greater than or equal |
| `x.lessThanOrEqual(other: FloatExpr \| number): FloatExpr` | `lessEqual`, `lte`, `le` | Less than or equal |

---

## String Expressions

### Manipulation

| Signature | Description |
|-----------|-------------|
| `str.concat(other: StringExpr \| string): StringExpr` | Concatenate |
| `str.repeat(count: IntegerExpr \| bigint): StringExpr` | Repeat n times |
| `str.substring(from: IntegerExpr \| bigint, to: IntegerExpr \| bigint): StringExpr` | Extract substring |
| `str.upperCase(): StringExpr` | Convert to uppercase |
| `str.lowerCase(): StringExpr` | Convert to lowercase |
| `str.trim(): StringExpr` | Remove whitespace from both ends |
| `str.trimStart(): StringExpr` | Remove whitespace from start |
| `str.trimEnd(): StringExpr` | Remove whitespace from end |
| `str.split(separator: StringExpr \| string): ArrayExpr<StringType>` | Split into array |
| `str.replace(search: StringExpr \| string, replacement: StringExpr \| string): StringExpr` | Replace first occurrence |

### Query

| Signature | Description |
|-----------|-------------|
| `str.length(): IntegerExpr` | String length (UTF-16 code units) |
| `str.startsWith(prefix: StringExpr \| string): BooleanExpr` | Test if starts with prefix |
| `str.endsWith(suffix: StringExpr \| string): BooleanExpr` | Test if ends with suffix |
| `str.contains(substring: StringExpr \| string): BooleanExpr` | Test if contains substring |
| `str.contains(regex: RegExp): BooleanExpr` | Test if matches regex |
| `str.indexOf(substring: StringExpr \| string): IntegerExpr` | Find index (-1 if not found) |
| `str.indexOf(regex: RegExp): IntegerExpr` | Find regex match index |

### Encoding

| Signature | Description |
|-----------|-------------|
| `str.encodeUtf8(): BlobExpr` | Encode as UTF-8 bytes |
| `str.encodeUtf16(): BlobExpr` | Encode as UTF-16 bytes (little-endian with BOM) |

### Parsing

| Signature | Description |
|-----------|-------------|
| `str.parse<T extends DataType>(type: T): ExprType<T>` | Parse string to type (throws on error) |
| `str.parseJson<T extends DataType>(type: T): ExprType<T>` | Parse JSON to type (throws on error) |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `str.equals(other: StringExpr \| string): BooleanExpr` | `equal`, `eq` | Check equality |
| `str.notEquals(other: StringExpr \| string): BooleanExpr` | `notEqual`, `ne` | Check inequality |
| `str.greaterThan(other: StringExpr \| string): BooleanExpr` | `greater`, `gt` | Greater than (lexicographic) |
| `str.lessThan(other: StringExpr \| string): BooleanExpr` | `less`, `lt` | Less than (lexicographic) |
| `str.greaterThanOrEqual(other: StringExpr \| string): BooleanExpr` | `greaterEqual`, `gte`, `ge` | Greater than or equal |
| `str.lessThanOrEqual(other: StringExpr \| string): BooleanExpr` | `lessEqual`, `lte`, `le` | Less than or equal |

---

## DateTime Expressions

### Component Access

| Signature | Description |
|-----------|-------------|
| `date.getYear(): IntegerExpr` | Get year |
| `date.getMonth(): IntegerExpr` | Get month (1-12) |
| `date.getDayOfMonth(): IntegerExpr` | Get day of month (1-31) |
| `date.getDayOfWeek(): IntegerExpr` | Get day of week (0-6, Sunday=0) |
| `date.getHour(): IntegerExpr` | Get hour (0-23) |
| `date.getMinute(): IntegerExpr` | Get minute (0-59) |
| `date.getSecond(): IntegerExpr` | Get second (0-59) |
| `date.getMillisecond(): IntegerExpr` | Get millisecond (0-999) |

### Arithmetic

| Signature | Description |
|-----------|-------------|
| `date.addMilliseconds(ms: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add milliseconds |
| `date.subtractMilliseconds(ms: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract milliseconds |
| `date.addSeconds(s: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add seconds |
| `date.subtractSeconds(s: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract seconds |
| `date.addMinutes(m: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add minutes |
| `date.subtractMinutes(m: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract minutes |
| `date.addHours(h: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add hours |
| `date.subtractHours(h: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract hours |
| `date.addDays(d: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add days |
| `date.subtractDays(d: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract days |
| `date.addWeeks(w: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Add weeks |
| `date.subtractWeeks(w: IntegerExpr \| FloatExpr \| bigint \| number): DateTimeExpr` | Subtract weeks |

### Duration

| Signature | Description |
|-----------|-------------|
| `date.durationMilliseconds(other: DateTimeExpr \| Date): IntegerExpr` | Duration in ms (positive if other > this) |
| `date.durationSeconds(other: DateTimeExpr \| Date): FloatExpr` | Duration in seconds |
| `date.durationMinutes(other: DateTimeExpr \| Date): FloatExpr` | Duration in minutes |
| `date.durationHours(other: DateTimeExpr \| Date): FloatExpr` | Duration in hours |
| `date.durationDays(other: DateTimeExpr \| Date): FloatExpr` | Duration in days |
| `date.durationWeeks(other: DateTimeExpr \| Date): FloatExpr` | Duration in weeks |

### Conversion

| Signature | Description |
|-----------|-------------|
| `date.toEpochMilliseconds(): IntegerExpr` | Milliseconds since Unix epoch |
| `date.printFormatted(formatString: string): StringExpr` | Format to string using format specifiers |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `date.equals(other: DateTimeExpr \| Date): BooleanExpr` | `equal`, `eq` | Check equality |
| `date.notEquals(other: DateTimeExpr \| Date): BooleanExpr` | `notEqual`, `ne` | Check inequality |
| `date.greaterThan(other: DateTimeExpr \| Date): BooleanExpr` | `greater`, `gt` | Greater than (later) |
| `date.lessThan(other: DateTimeExpr \| Date): BooleanExpr` | `less`, `lt` | Less than (earlier) |
| `date.greaterThanOrEqual(other: DateTimeExpr \| Date): BooleanExpr` | `greaterEqual`, `gte`, `ge` | Greater than or equal |
| `date.lessThanOrEqual(other: DateTimeExpr \| Date): BooleanExpr` | `lessEqual`, `lte`, `le` | Less than or equal |

---

## Blob Expressions

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `blob.size(): IntegerExpr` | | Size in bytes |
| `blob.getUint8(offset: IntegerExpr \| bigint): IntegerExpr` | | Get byte at offset (0-255, throws if OOB) |
| `blob.decodeUtf8(): StringExpr` | | Decode as UTF-8 (throws on invalid) |
| `blob.decodeUtf16(): StringExpr` | | Decode as UTF-16 (throws on invalid) |
| `blob.decodeBeast<T extends EastType>(type: T, version: 'v1' \| 'v2' = 'v1'): ExprType<T>` | | Decode BEAST format |
| `blob.decodeCsv<T extends StructType>(structType: T, options?: CsvParseOptions): ArrayExpr<T>` | | Parse CSV to array of structs |
| `blob.equals(other: BlobExpr \| Uint8Array): BooleanExpr` | `equal`, `eq` | Check equality |
| `blob.notEquals(other: BlobExpr \| Uint8Array): BooleanExpr` | `notEqual`, `ne` | Check inequality |

---

## Array Expressions

For `ArrayExpr<T>` where `T` is the element type:

### Read Operations

| Signature | Description |
|-----------|-------------|
| `array.size(): IntegerExpr` | Array length |
| `array.length(): IntegerExpr` | Array length (alias) |
| `array.has(index: IntegerExpr \| bigint): BooleanExpr` | Check if index valid |
| `array.get(index: IntegerExpr \| bigint): ExprType<T>` | Get element (throws if OOB) |
| `array.get(index: IntegerExpr \| bigint, defaultFn: ($: BlockBuilder, i: IntegerExpr) => ExprType<T>): ExprType<T>` | Get or compute default |
| `array.at(index: IntegerExpr \| bigint, defaultFn?: ($: BlockBuilder, i: IntegerExpr) => ExprType<T>): ExprType<T>` | Alias for get |
| `array.tryGet(index: IntegerExpr \| bigint): OptionExpr<T>` | Safe get returning Option |
| `array.getKeys(keys: ArrayExpr<IntegerType>, onMissing?: ($: BlockBuilder, i: IntegerExpr) => ExprType<T>): ArrayExpr<T>` | Get multiple elements by indices |

### Mutation Operations

| Signature | Description |
|-----------|-------------|
| `array.update(index: IntegerExpr \| bigint, value: ExprType<T> \| ValueTypeOf<T>): NullExpr` | Replace element (throws if OOB) |
| `array.merge<T2>(index: IntegerExpr \| bigint, value: ExprType<T2> \| ValueTypeOf<T2>, updateFn: ($: BlockBuilder, old: ExprType<T>, new_: ExprType<T2>, i: IntegerExpr) => ExprType<T>): ExprType<T>` | Merge with function |
| `array.pushLast(value: ExprType<T> \| ValueTypeOf<T>): NullExpr` | Append to end |
| `array.popLast(): ExprType<T>` | Remove from end (throws if empty) |
| `array.pushFirst(value: ExprType<T> \| ValueTypeOf<T>): NullExpr` | Prepend to start |
| `array.popFirst(): ExprType<T>` | Remove from start (throws if empty) |
| `array.append(other: ArrayExpr<T> \| ValueTypeOf<T>[]): NullExpr` | Append all (mutating) |
| `array.prepend(other: ArrayExpr<T> \| ValueTypeOf<T>[]): NullExpr` | Prepend all (mutating) |
| `array.clear(): NullExpr` | Remove all elements |
| `array.sortInPlace(byFn?: ($: BlockBuilder, v: ExprType<T>) => Expr): NullExpr` | Sort in-place |
| `array.reverseInPlace(): NullExpr` | Reverse in-place |

### Functional Operations (Immutable)

| Signature | Description |
|-----------|-------------|
| `array.copy(): ArrayExpr<T>` | Shallow copy |
| `array.slice(start: IntegerExpr \| bigint, end: IntegerExpr \| bigint): ArrayExpr<T>` | Extract subarray |
| `array.concat(other: ArrayExpr<T> \| ValueTypeOf<T>[]): ArrayExpr<T>` | Concatenate into new array |
| `array.sort(byFn?: ($: BlockBuilder, v: ExprType<T>) => Expr): ArrayExpr<T>` | Sorted copy |
| `array.reverse(): ArrayExpr<T>` | Reversed copy |
| `array.isSorted(byFn?: ($: BlockBuilder, v: ExprType<T>) => Expr): BooleanExpr` | Check if sorted |
| `array.map<U>(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<U>): ArrayExpr<U>` | Transform each |
| `array.filter(predicate: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => BooleanExpr): ArrayExpr<T>` | Keep matching |
| `array.filterMap<U>(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => OptionExpr<U>): ArrayExpr<U>` | Filter and map with Option |
| `array.flatMap<U>(fn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ArrayExpr<U>): ArrayExpr<U>` | Flatten arrays |
| `array.flattenToSet<K>(fn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => SetExpr<K>): SetExpr<K>` | Flatten to set |
| `array.flattenToDict<K, U>(fn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => DictExpr<K, U>, onConflictFn?: ($: BlockBuilder, v1: ExprType<U>, v2: ExprType<U>, key: ExprType<K>) => ExprType<U>): DictExpr<K, U>` | Flatten to dict |
| `array.findFirst(value: ExprType<T> \| ValueTypeOf<T>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): OptionExpr<IntegerType>` | Find first index |
| `array.findAll(value: ExprType<T> \| ValueTypeOf<T>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): ArrayExpr<IntegerType>` | Find all indices |
| `array.firstMap<U>(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => OptionExpr<U>): OptionExpr<U>` | Find first matching and transform |
| `array.forEach(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => void): NullExpr` | Execute for each |

### Reduction Operations

| Signature | Description |
|-----------|-------------|
| `array.reduce<Acc>(combineFn: ($: BlockBuilder, acc: ExprType<Acc>, x: ExprType<T>, i: IntegerExpr) => ExprType<Acc>, init: ExprType<Acc> \| ValueTypeOf<Acc>): ExprType<Acc>` | Fold with initial |
| `array.reduce(combineFn: ($: BlockBuilder, acc: ExprType<T>, x: ExprType<T>, i: IntegerExpr) => ExprType<T>): ExprType<T>` | Fold without initial |
| `array.every(predicate?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => BooleanExpr): BooleanExpr` | All match |
| `array.some(predicate?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => BooleanExpr): BooleanExpr` | Any match |
| `array.sum(): IntegerExpr \| FloatExpr` | Sum (for numeric arrays) |
| `array.sum(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => IntegerExpr \| FloatExpr): IntegerExpr \| FloatExpr` | Sum with projection |
| `array.mean(): FloatExpr` | Mean (NaN if empty) |
| `array.mean(fn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => IntegerExpr \| FloatExpr): FloatExpr` | Mean with projection |
| `array.maximum(by?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): ExprType<T>` | Maximum value (throws if empty) |
| `array.minimum(by?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): ExprType<T>` | Minimum value (throws if empty) |
| `array.findMaximum(by?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): OptionExpr<IntegerType>` | Find index of maximum |
| `array.findMinimum(by?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): OptionExpr<IntegerType>` | Find index of minimum |

### Conversion Operations

| Signature | Description |
|-----------|-------------|
| `array.stringJoin(separator: StringExpr \| string): StringExpr` | Join string array |
| `array.toSet<K>(keyFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>): SetExpr<K>` | Convert to set |
| `array.toDict<K, V>(keyFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<V>): DictExpr<K, V>` | Convert to dict |
| `array.encodeCsv(options?: CsvSerializeOptions): BlobExpr` | Serialize to CSV |

### Grouping Operations

| Signature | Description |
|-----------|-------------|
| `array.groupReduce<K, Acc>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, initFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<Acc>, reduceFn: ($: BlockBuilder, acc: ExprType<Acc>, x: ExprType<T>, key: ExprType<K>) => ExprType<Acc>): DictExpr<K, Acc>` | Group and reduce |
| `array.groupSize<K>(keyFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>): DictExpr<K, IntegerType>` | Count per group |
| `array.groupSum<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => IntegerExpr \| FloatExpr): DictExpr<K, IntegerType \| FloatType>` | Sum per group |
| `array.groupMean<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => IntegerExpr \| FloatExpr): DictExpr<K, FloatType>` | Mean per group |
| `array.groupMinimum<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, T>` | Min value per group |
| `array.groupMaximum<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, T>` | Max value per group |
| `array.groupToArrays<K, V>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<V>): DictExpr<K, ArrayType<V>>` | Collect to arrays |
| `array.groupToSets<K, V>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<V>): DictExpr<K, SetType<V>>` | Collect to sets |
| `array.groupToDicts<K, K2, V>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, keyFn2: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K2>, valueFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<V>, combineFn?: ($: BlockBuilder, v1: ExprType<V>, v2: ExprType<V>) => ExprType<V>): DictExpr<K, DictType<K2, V>>` | Collect to nested dicts |
| `array.groupEvery<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, predFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => BooleanExpr): DictExpr<K, BooleanType>` | All match per group |
| `array.groupSome<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, predFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => BooleanExpr): DictExpr<K, BooleanType>` | Any match per group |
| `array.groupFindFirst<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, value: Expr, projFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, OptionType<IntegerType>>` | Find first index per group |
| `array.groupFindAll<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, value: Expr, projFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, ArrayType<IntegerType>>` | Find all indices per group |
| `array.groupFindMinimum<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, IntegerType>` | Find min index per group |
| `array.groupFindMaximum<K>(keyFn: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => ExprType<K>, byFn?: ($: BlockBuilder, x: ExprType<T>, i: IntegerExpr) => Expr): DictExpr<K, IntegerType>` | Find max index per group |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `array.equals(other: ArrayExpr<T> \| ValueTypeOf<T>[]): BooleanExpr` | `equal`, `eq` | Check deep equality |
| `array.notEquals(other: ArrayExpr<T> \| ValueTypeOf<T>[]): BooleanExpr` | `notEqual`, `ne` | Check deep inequality |

---

## Set Expressions

For `SetExpr<K>` where `K` is the key/element type:

### Read Operations

| Signature | Description |
|-----------|-------------|
| `set.size(): IntegerExpr` | Set size |
| `set.has(key: ExprType<K> \| ValueTypeOf<K>): BooleanExpr` | Check if key exists |

### Mutation Operations

| Signature | Description |
|-----------|-------------|
| `set.insert(key: ExprType<K> \| ValueTypeOf<K>): NullExpr` | Insert (throws if exists) |
| `set.tryInsert(key: ExprType<K> \| ValueTypeOf<K>): BooleanExpr` | Safe insert (returns success) |
| `set.delete(key: ExprType<K> \| ValueTypeOf<K>): NullExpr` | Delete (throws if missing) |
| `set.tryDelete(key: ExprType<K> \| ValueTypeOf<K>): BooleanExpr` | Safe delete (returns success) |
| `set.clear(): NullExpr` | Remove all |
| `set.unionInPlace(other: SetExpr<K> \| Set<ValueTypeOf<K>>): NullExpr` | Union in-place |

### Set Operations

| Signature | Description |
|-----------|-------------|
| `set.copy(): SetExpr<K>` | Shallow copy |
| `set.union(other: SetExpr<K> \| Set<ValueTypeOf<K>>): SetExpr<K>` | Union |
| `set.intersection(other: SetExpr<K> \| Set<ValueTypeOf<K>>): SetExpr<K>` | Intersection |
| `set.difference(other: SetExpr<K> \| Set<ValueTypeOf<K>>): SetExpr<K>` | Difference (in this, not other) |
| `set.symmetricDifference(other: SetExpr<K> \| Set<ValueTypeOf<K>>): SetExpr<K>` | Symmetric difference |
| `set.isSubsetOf(other: SetExpr<K> \| Set<ValueTypeOf<K>>): BooleanExpr` | Check subset |
| `set.isSupersetOf(other: SetExpr<K> \| Set<ValueTypeOf<K>>): BooleanExpr` | Check superset |
| `set.isDisjointFrom(other: SetExpr<K> \| Set<ValueTypeOf<K>>): BooleanExpr` | Check no common elements |

### Functional Operations

| Signature | Description |
|-----------|-------------|
| `set.filter(predicate: ($: BlockBuilder, key: ExprType<K>) => BooleanExpr): SetExpr<K>` | Keep matching |
| `set.filterMap<V>(fn: ($: BlockBuilder, key: ExprType<K>) => OptionExpr<V>): DictExpr<K, V>` | Filter and map with Option |
| `set.firstMap<U>(fn: ($: BlockBuilder, key: ExprType<K>) => OptionExpr<U>): OptionExpr<U>` | Find first matching and transform |
| `set.forEach(fn: ($: BlockBuilder, key: ExprType<K>) => void): NullExpr` | Execute for each |
| `set.map<V>(fn: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): DictExpr<K, V>` | Map to dict |
| `set.reduce<Acc>(fn: ($: BlockBuilder, acc: ExprType<Acc>, key: ExprType<K>) => ExprType<Acc>, init: ExprType<Acc> \| ValueTypeOf<Acc>): ExprType<Acc>` | Fold |
| `set.every(fn?: ($: BlockBuilder, key: ExprType<K>) => BooleanExpr): BooleanExpr` | All match |
| `set.some(fn?: ($: BlockBuilder, key: ExprType<K>) => BooleanExpr): BooleanExpr` | Any match |
| `set.sum(): IntegerExpr \| FloatExpr` | Sum (for numeric sets) |
| `set.sum(fn: ($: BlockBuilder, key: ExprType<K>) => IntegerExpr \| FloatExpr): IntegerExpr \| FloatExpr` | Sum with projection |
| `set.mean(): FloatExpr` | Mean (NaN if empty) |
| `set.mean(fn: ($: BlockBuilder, key: ExprType<K>) => IntegerExpr \| FloatExpr): FloatExpr` | Mean with projection |

### Conversion Operations

| Signature | Description |
|-----------|-------------|
| `set.toArray<V>(fn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): ArrayExpr<V>` | Convert to array |
| `set.toSet<U>(keyFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<U>): SetExpr<U>` | Convert to new set |
| `set.toDict<K2, V>(keyFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<K2>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>, onConflictFn?: ($: BlockBuilder, v1: ExprType<V>, v2: ExprType<V>, key: ExprType<K2>) => ExprType<V>): DictExpr<K2, V>` | Convert to dict |
| `set.flattenToArray<V>(fn: ($: BlockBuilder, key: ExprType<K>) => ArrayExpr<V>): ArrayExpr<V>` | Flatten to array |
| `set.flattenToSet<U>(fn: ($: BlockBuilder, key: ExprType<K>) => SetExpr<U>): SetExpr<U>` | Flatten to set |
| `set.flattenToDict<K2, V>(fn: ($: BlockBuilder, key: ExprType<K>) => DictExpr<K2, V>, onConflictFn?: ($: BlockBuilder, v1: ExprType<V>, v2: ExprType<V>, key: ExprType<K2>) => ExprType<V>): DictExpr<K2, V>` | Flatten to dict |

### Grouping Operations

| Signature | Description |
|-----------|-------------|
| `set.groupReduce<G, Acc>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, initFn: ($: BlockBuilder, g: ExprType<G>) => ExprType<Acc>, reduceFn: ($: BlockBuilder, acc: ExprType<Acc>, key: ExprType<K>, g: ExprType<G>) => ExprType<Acc>): DictExpr<G, Acc>` | Group and reduce |
| `set.groupSize<G>(keyFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>): DictExpr<G, IntegerType>` | Count per group |
| `set.groupSum<G>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => IntegerExpr \| FloatExpr): DictExpr<G, IntegerType \| FloatType>` | Sum per group |
| `set.groupMean<G>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => IntegerExpr \| FloatExpr): DictExpr<G, FloatType>` | Mean per group |
| `set.groupToArrays<G, V>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): DictExpr<G, ArrayType<V>>` | Collect to arrays |
| `set.groupToSets<G, V>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): DictExpr<G, SetType<V>>` | Collect to sets |
| `set.groupToDicts<G, K2, V>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, keyFn2: ($: BlockBuilder, key: ExprType<K>) => ExprType<K2>, valueFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>, combineFn?: ($: BlockBuilder, v1: ExprType<V>, v2: ExprType<V>) => ExprType<V>): DictExpr<G, DictType<K2, V>>` | Collect to nested dicts |
| `set.groupEvery<G>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, predFn: ($: BlockBuilder, key: ExprType<K>) => BooleanExpr): DictExpr<G, BooleanType>` | All match per group |
| `set.groupSome<G>(keyFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<G>, predFn: ($: BlockBuilder, key: ExprType<K>) => BooleanExpr): DictExpr<G, BooleanType>` | Any match per group |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `set.equals(other: SetExpr<K> \| Set<ValueTypeOf<K>>): BooleanExpr` | `equal`, `eq` | Check deep equality |
| `set.notEquals(other: SetExpr<K> \| Set<ValueTypeOf<K>>): BooleanExpr` | `notEqual`, `ne` | Check deep inequality |

---

## Dict Expressions

For `DictExpr<K, V>` where `K` is the key type and `V` is the value type:

### Read Operations

| Signature | Description |
|-----------|-------------|
| `dict.size(): IntegerExpr` | Dict size |
| `dict.has(key: ExprType<K> \| ValueTypeOf<K>): BooleanExpr` | Check if key exists |
| `dict.get(key: ExprType<K> \| ValueTypeOf<K>): ExprType<V>` | Get value (throws if missing) |
| `dict.get(key: ExprType<K> \| ValueTypeOf<K>, defaultFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): ExprType<V>` | Get or compute default |
| `dict.tryGet(key: ExprType<K> \| ValueTypeOf<K>): OptionExpr<V>` | Safe get returning Option |
| `dict.keys(): SetExpr<K>` | Get all keys |
| `dict.getKeys(keys: SetExpr<K> \| Set<ValueTypeOf<K>>, onMissing?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): DictExpr<K, V>` | Get multiple entries by keys |

### Mutation Operations

| Signature | Description |
|-----------|-------------|
| `dict.insert(key: ExprType<K> \| ValueTypeOf<K>, value: ExprType<V> \| ValueTypeOf<V>): NullExpr` | Insert (throws if exists) |
| `dict.insertOrUpdate(key: ExprType<K> \| ValueTypeOf<K>, value: ExprType<V> \| ValueTypeOf<V>): NullExpr` | Insert or update |
| `dict.update(key: ExprType<K> \| ValueTypeOf<K>, value: ExprType<V> \| ValueTypeOf<V>): NullExpr` | Update (throws if missing) |
| `dict.merge<T2>(key: ExprType<K> \| ValueTypeOf<K>, value: ExprType<T2> \| ValueTypeOf<T2>, updateFn: ($: BlockBuilder, old: ExprType<V>, new_: ExprType<T2>, key: ExprType<K>) => ExprType<V>, initialFn?: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): NullExpr` | Merge with function |
| `dict.getOrInsert(key: ExprType<K> \| ValueTypeOf<K>, defaultFn: ($: BlockBuilder, key: ExprType<K>) => ExprType<V>): ExprType<V>` | Get or insert default |
| `dict.delete(key: ExprType<K> \| ValueTypeOf<K>): NullExpr` | Delete (throws if missing) |
| `dict.tryDelete(key: ExprType<K> \| ValueTypeOf<K>): BooleanExpr` | Safe delete |
| `dict.pop(key: ExprType<K> \| ValueTypeOf<K>): ExprType<V>` | Remove and return |
| `dict.swap(key: ExprType<K> \| ValueTypeOf<K>, value: ExprType<V> \| ValueTypeOf<V>): ExprType<V>` | Replace and return old |
| `dict.clear(): NullExpr` | Remove all |
| `dict.unionInPlace(other: DictExpr<K, V> \| Map<ValueTypeOf<K>, ValueTypeOf<V>>, mergeFn?: ($: BlockBuilder, v1: ExprType<V>, v2: ExprType<V>, key: ExprType<K>) => ExprType<V>): NullExpr` | Union in-place |

### Functional Operations

| Signature | Description |
|-----------|-------------|
| `dict.copy(): DictExpr<K, V>` | Shallow copy |
| `dict.map<U>(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>): DictExpr<K, U>` | Transform values |
| `dict.filter(predicate: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => BooleanExpr): DictExpr<K, V>` | Keep matching |
| `dict.filterMap<U>(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => OptionExpr<U>): DictExpr<K, U>` | Filter and map with Option |
| `dict.firstMap<U>(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => OptionExpr<U>): OptionExpr<U>` | Find first matching and transform |
| `dict.forEach(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => void): NullExpr` | Execute for each |
| `dict.reduce<Acc>(fn: ($: BlockBuilder, acc: ExprType<Acc>, val: ExprType<V>, key: ExprType<K>) => ExprType<Acc>, init: ExprType<Acc> \| ValueTypeOf<Acc>): ExprType<Acc>` | Fold |
| `dict.every(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => BooleanExpr): BooleanExpr` | All match |
| `dict.some(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => BooleanExpr): BooleanExpr` | Any match |
| `dict.sum(): IntegerExpr \| FloatExpr` | Sum values |
| `dict.sum(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => IntegerExpr \| FloatExpr): IntegerExpr \| FloatExpr` | Sum with projection |
| `dict.mean(): FloatExpr` | Mean (NaN if empty) |
| `dict.mean(fn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => IntegerExpr \| FloatExpr): FloatExpr` | Mean with projection |

### Conversion Operations

| Signature | Description |
|-----------|-------------|
| `dict.toArray<U>(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>): ArrayExpr<U>` | Convert to array |
| `dict.toSet<U>(keyFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>): SetExpr<U>` | Convert to set |
| `dict.toDict<K2, V2>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<K2>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<V2>, onConflictFn?: ($: BlockBuilder, v1: ExprType<V2>, v2: ExprType<V2>, key: ExprType<K2>) => ExprType<V2>): DictExpr<K2, V2>` | Convert to new dict |
| `dict.flattenToArray<U>(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ArrayExpr<U>): ArrayExpr<U>` | Flatten to array |
| `dict.flattenToSet<U>(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => SetExpr<U>): SetExpr<U>` | Flatten to set |
| `dict.flattenToDict<K2, V2>(fn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => DictExpr<K2, V2>, onConflictFn?: ($: BlockBuilder, v1: ExprType<V2>, v2: ExprType<V2>, key: ExprType<K2>) => ExprType<V2>): DictExpr<K2, V2>` | Flatten to dict |

### Grouping Operations

| Signature | Description |
|-----------|-------------|
| `dict.groupReduce<G, Acc>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, initFn: ($: BlockBuilder, g: ExprType<G>) => ExprType<Acc>, reduceFn: ($: BlockBuilder, acc: ExprType<Acc>, val: ExprType<V>, key: ExprType<K>, g: ExprType<G>) => ExprType<Acc>): DictExpr<G, Acc>` | Group and reduce |
| `dict.groupSize<G>(keyFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>): DictExpr<G, IntegerType>` | Count per group |
| `dict.groupSum<G>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => IntegerExpr \| FloatExpr): DictExpr<G, IntegerType \| FloatType>` | Sum per group |
| `dict.groupMean<G>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => IntegerExpr \| FloatExpr): DictExpr<G, FloatType>` | Mean per group |
| `dict.groupToArrays<G, U>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>): DictExpr<G, ArrayType<U>>` | Collect to arrays |
| `dict.groupToSets<G, U>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>): DictExpr<G, SetType<U>>` | Collect to sets |
| `dict.groupToDicts<G, K2, U>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, keyFn2: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<K2>, valueFn?: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<U>, combineFn?: ($: BlockBuilder, v1: ExprType<U>, v2: ExprType<U>) => ExprType<U>): DictExpr<G, DictType<K2, U>>` | Collect to nested dicts |
| `dict.groupEvery<G>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, predFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => BooleanExpr): DictExpr<G, BooleanType>` | All match per group |
| `dict.groupSome<G>(keyFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => ExprType<G>, predFn: ($: BlockBuilder, val: ExprType<V>, key: ExprType<K>) => BooleanExpr): DictExpr<G, BooleanType>` | Any match per group |

### Comparison Operations

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `dict.equals(other: DictExpr<K, V> \| Map<ValueTypeOf<K>, ValueTypeOf<V>>): BooleanExpr` | `equal`, `eq` | Check deep equality |
| `dict.notEquals(other: DictExpr<K, V> \| Map<ValueTypeOf<K>, ValueTypeOf<V>>): BooleanExpr` | `notEqual`, `ne` | Check deep inequality |

---

## Struct Expressions

Struct fields are accessed directly as properties:

```typescript
const PersonType = StructType({ name: StringType, age: IntegerType });

// In function body:
person.name  // StringExpr
person.age   // IntegerExpr
```

---

## Variant Expressions

For `VariantExpr<Cases>` where `Cases` is a record of `{ tag: ValueType, ... }`:

| Signature | Aliases | Description |
|-----------|---------|-------------|
| `variant.match<R>(handlers: { [Tag in keyof Cases]: ($: BlockBuilder, data: ExprType<Cases[Tag]>) => ExprType<R> }): ExprType<R>` | | Full match |
| `variant.match<R>(handlers: { [Tag in keyof Cases]?: ($: BlockBuilder, data: ExprType<Cases[Tag]>) => ExprType<R> }, defaultFn: ($: BlockBuilder) => ExprType<R>): ExprType<R>` | | Partial match with default |
| `variant.unwrap<Tag extends keyof Cases>(tag?: Tag): ExprType<Cases[Tag]>` | | Extract value (throws if wrong tag) |
| `variant.unwrap<Tag extends keyof Cases>(tag: Tag, defaultFn: ($: BlockBuilder) => ExprType<Cases[Tag]>): ExprType<Cases[Tag]>` | | Extract or compute default |
| `variant.getTag(): StringExpr` | | Get tag as string |
| `variant.hasTag<Tag extends keyof Cases>(tag: Tag): BooleanExpr` | | Check if has tag |
| `variant.equals(other: VariantExpr<Cases> \| ValueTypeOf<Cases>): BooleanExpr` | `equal`, `eq` | Check equality |
| `variant.notEquals(other: VariantExpr<Cases> \| ValueTypeOf<Cases>): BooleanExpr` | `notEqual`, `ne` | Check inequality |

---

## Ref Expressions

For `RefExpr<T>` where `T` is the value type:

| Signature | Description |
|-----------|-------------|
| `refCell.get(): ExprType<T>` | Get current value |
| `refCell.update(value: ExprType<T> \| ValueTypeOf<T>): NullExpr` | Replace value |
| `refCell.merge<T2>(value: ExprType<T2> \| ValueTypeOf<T2>, updateFn: ($: BlockBuilder, current: ExprType<T>, delta: ExprType<T2>) => ExprType<T>): NullExpr` | Merge with function |

---

## Standard Library

### East.Integer

| Signature | Description |
|-----------|-------------|
| `East.Integer.printCommaSeperated(x: IntegerExpr \| bigint): StringExpr` | Format with commas: `"1,234,567"` |
| `East.Integer.printCompact(x: IntegerExpr \| bigint): StringExpr` | Business units: `"1.5M"`, `"21K"` |
| `East.Integer.printCompactSI(x: IntegerExpr \| bigint): StringExpr` | SI units: `"1.5M"`, `"21k"` |
| `East.Integer.printCompactComputing(x: IntegerExpr \| bigint): StringExpr` | Binary units (1024): `"1.5Mi"` |
| `East.Integer.printOrdinal(x: IntegerExpr \| bigint): StringExpr` | Ordinal: `"1st"`, `"2nd"`, `"3rd"` |
| `East.Integer.printPercentage(x: IntegerExpr \| bigint): StringExpr` | Format as percentage: `"45%"` |
| `East.Integer.printCurrency(x: IntegerExpr \| bigint): StringExpr` | Currency with $: `"$1,234"` |
| `East.Integer.digitCount(x: IntegerExpr \| bigint): IntegerExpr` | Count decimal digits |
| `East.Integer.roundNearest(x: IntegerExpr \| bigint, step: IntegerExpr \| bigint): IntegerExpr` | Round to nearest multiple |
| `East.Integer.roundUp(x: IntegerExpr \| bigint, step: IntegerExpr \| bigint): IntegerExpr` | Round up (ceiling) to multiple |
| `East.Integer.roundDown(x: IntegerExpr \| bigint, step: IntegerExpr \| bigint): IntegerExpr` | Round down (floor) to multiple |
| `East.Integer.roundTruncate(x: IntegerExpr \| bigint, step: IntegerExpr \| bigint): IntegerExpr` | Round towards zero to multiple |

### East.Float

| Signature | Description |
|-----------|-------------|
| `East.Float.roundFloor(x: FloatExpr \| number): IntegerExpr` | Round down to integer |
| `East.Float.roundCeil(x: FloatExpr \| number): IntegerExpr` | Round up to integer |
| `East.Float.roundHalf(x: FloatExpr \| number): IntegerExpr` | Round to nearest integer |
| `East.Float.roundTrunc(x: FloatExpr \| number): IntegerExpr` | Truncate towards zero |
| `East.Float.roundNearest(x: FloatExpr \| number, step: FloatExpr \| number): FloatExpr` | Round to nearest multiple |
| `East.Float.roundUp(x: FloatExpr \| number, step: FloatExpr \| number): FloatExpr` | Round up to multiple |
| `East.Float.roundDown(x: FloatExpr \| number, step: FloatExpr \| number): FloatExpr` | Round down to multiple |
| `East.Float.roundTruncate(x: FloatExpr \| number, step: FloatExpr \| number): FloatExpr` | Round towards zero to multiple |
| `East.Float.roundToDecimals(x: FloatExpr \| number, decimals: IntegerExpr \| bigint): FloatExpr` | Round to decimal places |
| `East.Float.approxEqual(x: FloatExpr \| number, y: FloatExpr \| number, epsilon: FloatExpr \| number): BooleanExpr` | Approximate equality |
| `East.Float.printCommaSeperated(x: FloatExpr \| number, decimals: IntegerExpr \| bigint): StringExpr` | Format with commas |
| `East.Float.printCurrency(x: FloatExpr \| number): StringExpr` | Currency with $ and 2 decimals |
| `East.Float.printFixed(x: FloatExpr \| number, decimals: IntegerExpr \| bigint): StringExpr` | Fixed decimal places |
| `East.Float.printCompact(x: FloatExpr \| number): StringExpr` | Business units: `"21.5K"` |
| `East.Float.printPercentage(x: FloatExpr \| number, decimals: IntegerExpr \| bigint): StringExpr` | Format as percentage |

### East.DateTime

| Signature | Description |
|-----------|-------------|
| `East.DateTime.fromEpochMilliseconds(ms: IntegerExpr \| bigint): DateTimeExpr` | Create from Unix epoch ms |
| `East.DateTime.fromComponents(y, m?, d?, h?, min?, s?, ms?): DateTimeExpr` | Create from components |
| `East.DateTime.parseFormatted(format: string, dateString: string): DateTimeExpr` | Parse from format (throws on error) |
| `East.DateTime.roundNearestMillisecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest ms |
| `East.DateTime.roundUpMillisecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to ms |
| `East.DateTime.roundDownMillisecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to ms |
| `East.DateTime.roundNearestSecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest second |
| `East.DateTime.roundUpSecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to second |
| `East.DateTime.roundDownSecond(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to second |
| `East.DateTime.roundNearestMinute(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest minute |
| `East.DateTime.roundUpMinute(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to minute |
| `East.DateTime.roundDownMinute(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to minute |
| `East.DateTime.roundNearestHour(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest hour |
| `East.DateTime.roundUpHour(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to hour |
| `East.DateTime.roundDownHour(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to hour |
| `East.DateTime.roundNearestDay(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest day |
| `East.DateTime.roundUpDay(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to day |
| `East.DateTime.roundDownDay(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to day |
| `East.DateTime.roundNearestWeek(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round to nearest Monday |
| `East.DateTime.roundUpWeek(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round up to Monday |
| `East.DateTime.roundDownWeek(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to Monday |
| `East.DateTime.roundDownMonth(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to month start |
| `East.DateTime.roundDownYear(date: DateTimeExpr, step: IntegerExpr \| bigint): DateTimeExpr` | Round down to year start |

### East.Array

| Signature | Description |
|-----------|-------------|
| `East.Array.range(start: IntegerExpr \| bigint, end: IntegerExpr \| bigint, step?: IntegerExpr \| bigint): ArrayExpr<IntegerType>` | Generate integer range [start, end) |
| `East.Array.linspace(start: FloatExpr \| number, stop: FloatExpr \| number, size: IntegerExpr \| bigint): ArrayExpr<FloatType>` | Generate equally-spaced floats [start, stop] |
| `East.Array.generate<T>(size: IntegerExpr \| bigint, valueType: T, valueFn: ($: BlockBuilder, i: IntegerExpr) => ExprType<T>): ArrayExpr<T>` | Generate using function |

### East.Set

| Signature | Description |
|-----------|-------------|
| `East.Set.generate<K>(size: IntegerExpr \| bigint, keyType: K, keyFn: ($: BlockBuilder, i: IntegerExpr) => ExprType<K>): SetExpr<K>` | Generate using function |

### East.Dict

| Signature | Description |
|-----------|-------------|
| `East.Dict.generate<K, V>(size: IntegerExpr \| bigint, keyType: K, valueType: V, keyFn: ($: BlockBuilder, i: IntegerExpr) => ExprType<K>, valueFn: ($: BlockBuilder, i: IntegerExpr) => ExprType<V>): DictExpr<K, V>` | Generate using functions |

### East.Blob

| Signature | Description |
|-----------|-------------|
| `East.Blob.encodeBeast(value: Expr, version: 'v1' \| 'v2' = 'v1'): BlobExpr` | Encode to BEAST binary format |

### East.String

| Signature | Description |
|-----------|-------------|
| `East.String.printError(message: StringExpr \| string, stack: ArrayExpr<StackFrame>): StringExpr` | Pretty-print error with stack trace |
| `East.String.printJson(value: Expr): StringExpr` | Serialize value to JSON string |
