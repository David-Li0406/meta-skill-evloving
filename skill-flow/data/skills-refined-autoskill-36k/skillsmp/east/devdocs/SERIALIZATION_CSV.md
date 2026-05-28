# CSV Serialization Design Document

This document specifies the design for CSV serialization support in East as a **standard library builtin**, following the pattern established by BEAST and JSON serialization.

## Table of Contents

1. [Rationale](#rationale)
2. [Design Overview](#design-overview)
3. [Type System Integration](#type-system-integration)
4. [API Design](#api-design)
5. [Configuration](#configuration)
6. [Implementation Architecture](#implementation-architecture)
7. [Serialization Specification](#serialization-specification)
8. [Future Work](#future-work)

---

## Rationale

### Why CSV as a Builtin?

CSV should be implemented as an **expression standard library builtin** (like `decodeBeast`, `encodeJson`) rather than a platform function. Here's why:

#### 1. CSV is a Serialization Format

CSV is fundamentally a **data serialization format**, in the same category as JSON and BEAST:
- Converts typed East values to/from a byte representation
- Requires type information to correctly interpret data
- Benefits from compile-time type specialization

The existing pattern is clear:
- `blob.decodeBeast(type)` → Builtin AST node with `type_parameters`
- `blob.decodeJson(type)` → Builtin AST node with `type_parameters`
- `blob.decodeCsv(type, config)` → Should follow the same pattern

#### 2. Performance Requirements

The current platform function approach (`east-node-io`, `east-py-io`) has severe limitations:

**Platform Function Approach** (current):
```typescript
// Returns untyped Dict<String, Variant<Null|Boolean|Integer|Float|String|DateTime|Blob>>
csv_parse(blob, config) → Array<Dict<String, LiteralValueType>>
```

Problems:
- **Runtime type dispatch**: Every cell requires variant matching
- **Memory overhead**: Every value wrapped in a variant object
- **No compile-time specialization**: Same code path regardless of schema
- **Ergonomic burden**: User must manually extract and cast values

**Builtin Approach** (proposed):
```typescript
// Returns strongly-typed Array<MyRowStruct>
blob.decodeCsv(ArrayType(MyRowStruct), config) → Array<MyRowStruct>
```

Benefits:
- **Compile-time specialization**: Type-specific encoder/decoder generated at compile time
- **No boxing overhead**: Values decoded directly to target type
- **Type safety**: Schema mismatches caught at decode time with clear errors
- **Familiar pattern**: Consistent with BEAST/JSON which users already know

#### 3. Cross-Platform Consistency

As a builtin, CSV serialization will:
- Work identically across all East backends (JavaScript, Julia, Python)
- Be part of the language specification, not a platform-specific feature
- Have consistent semantics regardless of execution environment

#### 4. Domain Relevance

East's target users are business analysts, consultants, and data scientists. CSV is:
- The primary data interchange format in business contexts
- Exported by Excel, databases, ERPs, and analytics tools
- Often the first format users encounter when working with data

This isn't scope creep - it's serving the core use case.

### Why Not Keep It as a Platform Function?

The fundamental issue is that **platform functions cannot be generic over types**. Without generic platform functions (a significant language extension), we cannot have:

```typescript
// This is impossible with current platform function design
csv_parse<T>(blob: Blob, type: T, config: Config) → Array<T>
```

Adding generic platform functions would require:
- Changes to the IR format
- Changes to the compiler
- Changes to every platform implementation
- Complex type inference at platform boundaries

The builtin approach is simpler and follows established patterns.

---

## Design Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    User-Facing API (expr/blob.ts)               │
│  blob.decodeCsv(type, config)  │  array.encodeCsv(config)       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AST Builtins (builtins.ts)                   │
│  BlobDecodeCsv  │  ArrayEncodeCsv                               │
│  type_parameters: [elementType]                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Compiler (compile.ts)                              │
│  Generates specialized encoder/decoder at compile time          │
│  using serialization/csv.ts                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           Serialization Core (serialization/csv.ts)             │
│  encodeCsvFor(type, config) → (value) => Uint8Array             │
│  decodeCsvFor(type, config) → (blob) => value                   │
└─────────────────────────────────────────────────────────────────┘
```

### Integration with Existing Patterns

Following `serialization/json.ts` and `serialization/beast.ts`:

| Component | JSON | BEAST | CSV (proposed) |
|-----------|------|-------|----------------|
| Encode function | `encodeJSONFor(type)` | `encodeBeastFor(type)` | `encodeCsvFor(structType, config)` |
| Decode function | `decodeJSONFor(type)` | `decodeBeastFor(type)` | `decodeCsvFor(structType, config)` |
| Expr method (decode) | `blob.decodeJson(type)` | `blob.decodeBeast(type)` | `blob.decodeCsv(ArrayType(struct), config)` |
| Expr method (encode) | `East.Blob.encodeJson(value)` | `East.Blob.encodeBeast(value)` | `array.encodeCsv(config)` |
| Builtin name | `BlobDecodeJson` | `BlobDecodeBeast` | `BlobDecodeCsv`, `ArrayEncodeCsv` |

---

## Type System Integration

### Supported Types for CSV

CSV is a **tabular format**. We support encoding/decoding:

| Container Type | CSV Representation |
|----------------|-------------------|
| `Array<Struct>` | Rows of records |

This covers the primary use case. More complex mappings (Dict, Set) can be achieved by transforming data before/after CSV operations.

### Supported Field Types

CSV cells can decode to these East types:

| East Type | CSV Text Representation | Notes |
|-----------|------------------------|-------|
| `Null` | Empty string or configured `nullString` | |
| `Boolean` | `true`, `false` | Case-sensitive |
| `Integer` | Decimal string: `123`, `-456` | 64-bit signed range |
| `Float` | Decimal: `3.14`, `-1e6`, `NaN`, `Infinity`, `-Infinity` | |
| `String` | Raw text (quoted if contains delimiter/newline) | |
| `DateTime` | ISO 8601: `2024-01-15T10:30:00.000` | UTC timezone |
| `Blob` | Hex string: `0x48656c6c6f` | |
| `Option<T>` | Empty = `none`, non-empty = `some(T)` | |

### Type Constraints

- **Top-level type**: Must be `Array<Struct>`
- **Struct fields**: Must be primitive types or `Option<primitive>`
- **No nested collections**: Arrays/Sets/Dicts cannot be struct fields

---

## API Design

### Decoding API

```typescript
// On BlobExpr (src/expr/blob.ts)
class BlobExpr {
  /**
   * Decodes CSV data from the blob into a typed array of structs.
   *
   * @param type - The expected East type (Array<Struct>)
   * @param options - Optional CSV parsing configuration
   * @returns ArrayExpr of the specified struct type
   *
   * @throws East runtime error if CSV is malformed or doesn't match type
   */
  decodeCsv<T extends ArrayType<StructType>>(
    type: T,
    options?: CsvParseOptions
  ): ExprType<T>;
}
```

### Encoding API

```typescript
// On ArrayExpr (src/expr/array.ts) - only for Array<Struct>
class ArrayExpr<T extends StructType> {
  /**
   * Encodes the array of structs as CSV data.
   *
   * @param options - Optional CSV serialization configuration
   * @returns BlobExpr containing the CSV data
   */
  encodeCsv(options?: CsvSerializeOptions): BlobExpr;
}
```

### Standard Library Entry Point

```typescript
// On East.Csv (src/expr/libs/csv.ts)
export default {
  /**
   * Creates a CSV column schema from a struct type.
   * Useful for explicit column type configuration.
   */
  columnsFromType<T extends StructType>(type: T): Expr<DictType<StringType, CsvColumnType>>;
}
```

### Usage Examples

```typescript
// Define row type
const SalesRecord = StructType({
  date: DateTimeType,
  product: StringType,
  quantity: IntegerType,
  price: FloatType,
  notes: OptionType(StringType),  // Optional field - empty cells become none
});

// Decode CSV - minimal config (uses defaults)
const parseSales = East.function([BlobType], ArrayType(SalesRecord), ($, blob) => {
  $.return(blob.decodeCsv(ArrayType(SalesRecord)));
});

// Decode CSV - with options
const parseSalesCustom = East.function([BlobType], ArrayType(SalesRecord), ($, blob) => {
  $.return(blob.decodeCsv(ArrayType(SalesRecord), {
    delimiter: ';',                        // European CSV style
    nullStrings: ['', 'N/A', 'NULL', '-'], // Common null representations
    trimFields: true,                      // Remove whitespace
  }));
});

// Encode CSV - minimal config
const exportSales = East.function([ArrayType(SalesRecord)], BlobType, ($, sales) => {
  $.return(sales.encodeCsv());
});

// Encode CSV - with options
const exportSalesCustom = East.function([ArrayType(SalesRecord)], BlobType, ($, sales) => {
  $.return(sales.encodeCsv({
    delimiter: '\t',          // TSV format
    newline: '\n',            // Unix line endings
    alwaysQuote: true,        // Quote all fields
  }));
});
```

---

## Configuration

Following the pattern from `east-ui`, we provide two layers:

1. **TypeScript interface** with optional properties for ergonomic API use
2. **East StructType** with `OptionType` fields for the underlying East value

This allows users to write clean config objects while the conversion to East values is handled automatically.

### Parse Configuration

#### TypeScript Interface (User-Facing)

```typescript
/**
 * Configuration options for CSV parsing.
 * All properties are optional with sensible defaults.
 */
export type CsvParseOptions = {
  /** Column type hints - infers from target struct type if not provided */
  columns?: Map<string, CsvColumnTypeLiteral>;

  /** Field delimiter (default: ",") */
  delimiter?: string;
  /** Quote character (default: '"') */
  quoteChar?: string;
  /** Escape character (default: '"' for doubled quotes) */
  escapeChar?: string;
  /** Line ending - auto-detects if not provided */
  newline?: string;

  /** Whether first row is headers (default: true) */
  hasHeader?: boolean;
  /** String values to treat as null (default: [""]) */
  nullStrings?: string[];
  /** Skip rows that are entirely empty (default: true) */
  skipEmptyLines?: boolean;
  /** Trim whitespace from field values (default: false) */
  trimFields?: boolean;

  /** Map CSV headers to struct field names */
  columnMapping?: Map<string, string>;
  /** Error on schema mismatch (default: false) */
  strict?: boolean;
};

type CsvColumnTypeLiteral = 'Null' | 'Boolean' | 'Integer' | 'Float' | 'String' | 'DateTime' | 'Blob';
```

#### East Type (Internal)

```typescript
export const CsvColumnType = VariantType({
  Null: NullType,
  Boolean: NullType,
  Integer: NullType,
  Float: NullType,
  String: NullType,
  DateTime: NullType,
  Blob: NullType,
});

export const CsvParseConfigType = StructType({
  columns: OptionType(DictType(StringType, CsvColumnType)),
  delimiter: OptionType(StringType),
  quoteChar: OptionType(StringType),
  escapeChar: OptionType(StringType),
  newline: OptionType(StringType),
  hasHeader: OptionType(BooleanType),
  nullStrings: OptionType(ArrayType(StringType)),  // Multiple null representations
  skipEmptyLines: OptionType(BooleanType),
  trimFields: OptionType(BooleanType),
  columnMapping: OptionType(DictType(StringType, StringType)),
  strict: OptionType(BooleanType),
});
```

#### Conversion Function

```typescript
/**
 * Converts user-friendly options to East config value.
 */
export function csvParseConfig(options?: CsvParseOptions): Expr<CsvParseConfigType> {
  // Convert columns Map to SortedMap with variant values
  const columnsValue = options?.columns
    ? new SortedMap([...options.columns.entries()].map(([k, v]) => [k, variant(v, null)]))
    : undefined;

  // Convert columnMapping Map to SortedMap
  const columnMappingValue = options?.columnMapping
    ? new SortedMap([...options.columnMapping.entries()])
    : undefined;

  return East.value({
    columns: columnsValue ? variant("some", columnsValue) : variant("none", null),
    delimiter: options?.delimiter ? variant("some", options.delimiter) : variant("none", null),
    quoteChar: options?.quoteChar ? variant("some", options.quoteChar) : variant("none", null),
    escapeChar: options?.escapeChar ? variant("some", options.escapeChar) : variant("none", null),
    newline: options?.newline ? variant("some", options.newline) : variant("none", null),
    hasHeader: options?.hasHeader !== undefined ? variant("some", options.hasHeader) : variant("none", null),
    nullStrings: options?.nullStrings ? variant("some", options.nullStrings) : variant("none", null),
    skipEmptyLines: options?.skipEmptyLines !== undefined ? variant("some", options.skipEmptyLines) : variant("none", null),
    trimFields: options?.trimFields !== undefined ? variant("some", options.trimFields) : variant("none", null),
    columnMapping: columnMappingValue ? variant("some", columnMappingValue) : variant("none", null),
    strict: options?.strict !== undefined ? variant("some", options.strict) : variant("none", null),
  }, CsvParseConfigType);
}
```

### Serialize Configuration

#### TypeScript Interface (User-Facing)

```typescript
/**
 * Configuration options for CSV serialization.
 * All properties are optional with sensible defaults.
 */
export type CsvSerializeOptions = {
  /** Field delimiter (default: ",") */
  delimiter?: string;
  /** Quote character (default: '"') */
  quoteChar?: string;
  /** Escape character (default: '"') */
  escapeChar?: string;
  /** Line ending (default: "\r\n") */
  newline?: string;
  /** Include header row (default: true) */
  includeHeader?: boolean;
  /** String to output for null values (default: "") */
  nullString?: string;
  /** Always quote all fields (default: false) */
  alwaysQuote?: boolean;
};
```

#### East Type (Internal)

```typescript
export const CsvSerializeConfigType = StructType({
  delimiter: OptionType(StringType),
  quoteChar: OptionType(StringType),
  escapeChar: OptionType(StringType),
  newline: OptionType(StringType),
  includeHeader: OptionType(BooleanType),
  nullString: OptionType(StringType),
  alwaysQuote: OptionType(BooleanType),
});
```

#### Conversion Function

```typescript
/**
 * Converts user-friendly options to East config value.
 */
export function csvSerializeConfig(options?: CsvSerializeOptions): Expr<CsvSerializeConfigType> {
  return East.value({
    delimiter: options?.delimiter ? variant("some", options.delimiter) : variant("none", null),
    quoteChar: options?.quoteChar ? variant("some", options.quoteChar) : variant("none", null),
    escapeChar: options?.escapeChar ? variant("some", options.escapeChar) : variant("none", null),
    newline: options?.newline ? variant("some", options.newline) : variant("none", null),
    includeHeader: options?.includeHeader !== undefined ? variant("some", options.includeHeader) : variant("none", null),
    nullString: options?.nullString ? variant("some", options.nullString) : variant("none", null),
    alwaysQuote: options?.alwaysQuote !== undefined ? variant("some", options.alwaysQuote) : variant("none", null),
  }, CsvSerializeConfigType);
}
```

### Configuration Notes

- **Type inference**: When `columns` is not provided, column types are inferred from the target struct type
- **Newline auto-detection**: Checks for `\r\n`, `\n`, or `\r` in order
- **Quote escaping**: Supports both doubled-quote (`""`) and backslash (`\"`) styles
- **UTF-8 BOM**: Automatically skipped if present at start of file
- **Defaults applied at runtime**: Missing columns use defaults from config, then fall back to `none` for optional fields

---

## Implementation Architecture

### File Structure

```
src/
├── serialization/
│   ├── csv.ts              # Core encode/decode functions
│   └── csv.spec.ts         # Unit tests
├── expr/
│   ├── blob.ts             # Add decodeCsv method
│   ├── array.ts            # Add encodeCsv method
│   ├── set.ts              # Add encodeCsv method
│   ├── dict.ts             # Add encodeCsv method
│   └── libs/
│       └── csv.ts          # Standard library helpers
├── builtins.ts             # Add BlobDecodeCsv, ArrayEncodeCsv, etc.
└── compile.ts              # Compile builtins to use csv.ts
```

### Core Serialization Functions

Following the pattern from `json.ts`:

```typescript
// serialization/csv.ts

/**
 * Creates a type-specialized CSV encoder for Array<Struct>.
 */
export function encodeCsvFor<T extends StructType>(
  structType: T,
  config?: CsvSerializeConfig
): (value: ValueTypeOf<ArrayType<T>>) => Uint8Array;

/**
 * Creates a type-specialized CSV decoder for Array<Struct>.
 */
export function decodeCsvFor<T extends StructType>(
  structType: T,
  config?: CsvParseConfig,
  frozen?: boolean
): (blob: Uint8Array) => ValueTypeOf<ArrayType<T>>;
```

### Compile-Time Specialization

The compiler generates specialized code at compile time:

```typescript
// In compile.ts, handling BlobDecodeCsv builtin:

case "BlobDecodeCsv": {
  const elementType = ast.type_parameters[0];
  const config = compileExpr(ast.arguments[1]); // config expression

  // Generate specialized decoder at compile time
  const decoder = decodeCsvFor(elementType, /* config evaluated at compile-time if constant */);

  return (blob: Uint8Array) => decoder(blob);
}
```

For dynamic config (config is an expression, not a constant), we generate:

```typescript
return (blob: Uint8Array, config: CsvParseConfig) => {
  const decoder = decodeCsvFor(elementType, config);
  return decoder(blob);
};
```

### Error Handling

CSV decode errors use East's standard `EastError` with `Location` information injected. This allows errors to be traced back to the exact position in the CSV file.

#### Null Values in Non-Optional Fields

If a cell value matches `nullStrings` (default: `[""]`) and the target field is **not** an `OptionType`, parsing throws an error:

```typescript
// Struct with required field
const Record = StructType({
  id: StringType,        // Required - null throws error
  name: OptionType(StringType),  // Optional - null becomes none
});

// CSV:
// id,name
// 123,Alice    → { id: "123", name: some("Alice") }
// ,Bob        → ERROR: null value for required field 'id' at row 2, column 0
// 456,        → { id: "456", name: none }
```

#### Error Format

Errors include a `Location` with row and column information:

```typescript
// EastError with Location
{
  message: "null value for required field 'quantity'",
  location: {
    row: 5,           // 1-indexed row number (excluding header)
    column: 2,        // 0-indexed column index
    columnName: "quantity",  // Column header name if available
  }
}
```

#### Error Types

| Error | Cause | Location |
|-------|-------|----------|
| Null in required field | Cell matches `nullStrings` but field is not `OptionType` | row, column, columnName |
| Type parse error | Cell value cannot be parsed as target type | row, column, columnName |
| Missing column | Required column not in CSV headers | n/a (header-level error) |
| Unclosed quote | Quote not terminated before end of row/file | row, column |
| Too few fields | Row has fewer fields than header | row |
| Malformed CSV | General parse failure | row, column (if determinable) |

#### Example Error Messages

```
EastError: null value for required field 'quantity' at row 5, column 2 (quantity)
EastError: expected Integer but found 'abc' at row 3, column 1 (price)
EastError: missing required column 'email' in CSV header
EastError: unclosed quote at row 10, column 4
EastError: row 7 has 3 fields, expected 5
```

---

## Serialization Specification

### CSV Format

East CSV follows RFC 4180 with extensions:

1. **Character encoding**: UTF-8 (with optional BOM detection)
2. **Line endings**: `\r\n` (standard), `\n`, or `\r` accepted on input
3. **Quoting**: Fields containing delimiter, quote, or newline must be quoted
4. **Quote escaping**: Doubled quotes (`""`) by default, configurable
5. **Header row**: Optional, enabled by default

### Type-Specific Encoding

| East Type | CSV Encoding | Notes |
|-----------|--------------|-------|
| Null | Empty string | Or configured `nullString` |
| Boolean | `true` / `false` | Lowercase |
| Integer | Decimal digits | No leading zeros except for `0` |
| Float | Standard notation | `NaN`, `Infinity`, `-Infinity` supported |
| String | As-is (quoted if needed) | UTF-8 encoded |
| DateTime | `YYYY-MM-DDTHH:mm:ss.sss` | No timezone suffix |
| Blob | `0x` + hex digits | Lowercase hex |
| Option.none | Empty string | Treated as null |
| Option.some | Inner value | Encoded normally |

### Header Mapping

For `Array<Struct>`, headers map to struct field names:
- Header order matches struct field definition order
- Unknown headers are ignored (with warning)
- Missing headers for non-optional fields cause error

### Round-Trip Guarantees

For all supported types:
```
decodeCsvFor(type)(encodeCsvFor(type)(value)) ≡ value
```

Exceptions:
- Floating-point precision limits apply
- String values containing only the `nullString` become null

---

## Memory Efficiency

### Streaming Decode Architecture

CSV files in business contexts can be large (millions of rows). The decoder must be memory-efficient:

#### 1. Single-Pass Parsing

The decoder processes the blob in a single pass without loading the entire structure into intermediate representations:

```typescript
// BAD: Creates intermediate string array for each row
const rows = text.split('\n').map(row => row.split(','));

// GOOD: Stream through bytes, decode directly to target type
function decodeCsvFor<T>(type: T): (blob: Uint8Array) => ValueTypeOf<T> {
  return (blob) => {
    const result: any[] = [];
    let offset = 0;

    // Parse header once
    const { headers, newOffset } = parseHeaderRow(blob, offset, config);
    offset = newOffset;

    // Pre-compile field decoders (one per column)
    const fieldDecoders = headers.map((h, i) => createFieldDecoder(type.fields[h]));

    // Stream rows directly into result array
    while (offset < blob.length) {
      const row = parseRowDirect(blob, offset, fieldDecoders);
      result.push(row);
      offset = row.newOffset;
    }

    return result;
  };
}
```

#### 2. Pre-Compiled Field Decoders

Field decoders are created once per type, not per row or per cell:

```typescript
// Created once at decode function creation time
const fieldDecoders: FieldDecoder[] = structType.fields.map(field => {
  switch (field.type.type) {
    case 'Integer': return decodeInteger;  // Reused function reference
    case 'Float': return decodeFloat;
    case 'String': return decodeString;    // Just slice, no copy if possible
    // ...
  }
});

// Used for every row - no allocation per field
function parseRowDirect(blob: Uint8Array, offset: number, decoders: FieldDecoder[]): RowResult {
  const obj: any = {};
  for (let i = 0; i < decoders.length; i++) {
    const { value, newOffset } = decoders[i](blob, offset);
    obj[fieldNames[i]] = value;
    offset = newOffset;
  }
  return { value: obj, newOffset: offset };
}
```

#### 3. String Slice vs Copy

For string fields, avoid copying when possible:

```typescript
// For unquoted fields: slice the underlying buffer
function decodeStringUnquoted(blob: Uint8Array, start: number, end: number): string {
  // TextDecoder can decode a view without copying
  return textDecoder.decode(blob.subarray(start, end));
}

// For quoted fields with escapes: must build new string
function decodeStringQuoted(blob: Uint8Array, start: number, end: number): string {
  // Only allocate when escapes present
  // ...
}
```

#### 4. Reusable Buffers

For encoding, reuse buffers across rows:

```typescript
function encodeCsvFor<T>(type: T): (value: ValueTypeOf<T>) => Uint8Array {
  // Pre-allocate buffer, grow as needed
  let buffer = new Uint8Array(64 * 1024);  // 64KB initial
  let offset = 0;

  const ensureCapacity = (needed: number) => {
    if (offset + needed > buffer.length) {
      const newBuffer = new Uint8Array(buffer.length * 2);
      newBuffer.set(buffer);
      buffer = newBuffer;
    }
  };

  return (value) => {
    offset = 0;  // Reset for each encode call
    // ... encode rows ...
    return buffer.slice(0, offset);  // Return exact size
  };
}
```

### Memory Comparison

| Approach | Memory per 1M rows × 10 columns |
|----------|--------------------------------|
| Platform function (variant boxing) | ~800MB (80 bytes/cell for variant wrapper) |
| Builtin (direct decode) | ~200MB (20 bytes/cell average for actual data) |
| Streaming with buffer reuse | ~200MB + ~64KB buffer |

---

## Missing Field Handling

CSV data often has missing or inconsistent fields. East CSV handles this through type-driven behavior.

### Optional vs Required Fields

Use `OptionType` for fields that may be missing or null:

```typescript
const FlexibleRecord = StructType({
  id: StringType,                    // Required - error if null/missing
  name: StringType,                  // Required
  email: OptionType(StringType),     // Optional - null becomes none
  age: OptionType(IntegerType),      // Optional
});

// CSV with missing "age" column works fine
// id,name,email
// 1,Alice,alice@example.com   → { id: "1", name: "Alice", email: some("..."), age: none }
// 2,Bob,                      → { id: "2", name: "Bob", email: none, age: none }
```

### Strict Mode

For data validation, enable strict mode to error on schema mismatches:

```typescript
const config: CsvParseOptions = {
  strict: true,  // Error if CSV has extra columns or missing columns
};
```

### Column Mapping

Map CSV headers to struct fields when names don't match:

```typescript
const config: CsvParseOptions = {
  columnMapping: new Map([
    ['First Name', 'firstName'],    // CSV header → struct field
    ['Last Name', 'lastName'],
    ['E-mail', 'email'],
  ]),
};
```

### Missing Field Behavior Matrix

| Scenario | Non-Optional Field | Optional Field |
|----------|-------------------|----------------|
| Column missing from header | Error | `none` for all rows |
| Cell value in `nullStrings` | Error | `none` |
| Column in CSV but not in struct | Ignored (unless strict mode) | Ignored |

---

## Future Work

### Phase 1: Core Implementation
- [ ] `serialization/csv.ts` - encode/decode functions
- [ ] `expr/blob.ts` - `decodeCsv` method
- [ ] `expr/array.ts` - `encodeCsv` method
- [ ] `builtins.ts` - `BlobDecodeCsv`, `ArrayEncodeCsv`
- [ ] `compile.ts` - compile builtin to use csv.ts
- [ ] `expr/libs/csv.ts` - helper functions (e.g., `columnsFromType`)
- [ ] Unit tests and compliance tests

### Phase 2: Cross-Platform
- [ ] Port to Python (`east-py/serialization/csv.py`)
- [ ] Port to Julia (`East.jl/src/serialization/csv.jl`)
- [ ] Cross-platform compliance tests

### Phase 4: Deprecation
- [ ] Deprecate `east-node-io` CSV platform functions
- [ ] Deprecate `east-py-io` CSV platform functions
- [ ] Migration guide for existing users

---

## References

- [RFC 4180](https://tools.ietf.org/html/rfc4180) - Common Format and MIME Type for CSV Files
- `src/serialization/json.ts` - JSON serialization pattern
- `src/serialization/beast.ts` - BEAST serialization pattern
- `src/expr/blob.ts` - `decodeBeast` implementation pattern
- `east-node-io/src/format/csv.ts` - Existing platform function (config design)
- `ELARACore/javascript/libs/core/src/east/csv.ts` - Legacy implementation
