# East Serialization Specification

This document specifies how East types and values are represented, compared, and serialized across different formats. It serves as the canonical reference for implementing East in other languages (Julia, Python, etc.).

## Table of Contents

1. [Type System Overview](#type-system-overview)
2. [Value Semantics and Comparison](#value-semantics-and-comparison)
3. [Serialization Formats](#serialization-formats)
4. [Type-Specific Edge Cases](#type-specific-edge-cases)
5. [Implementation Reference](#implementation-reference)

---

## Type System Overview

East supports 13 types defined in `src/types.ts`:

### Primitive Types
- **Never**: Bottom type (uninhabited)
- **Null**: Unit type (single value: `null`)
- **Boolean**: Two values: `true`, `false`
- **Integer**: 64-bit signed integers (`-2^63` to `2^63-1`), represented as `bigint` in TypeScript
- **Float**: IEEE 754 double-precision (64-bit) floating-point
- **String**: UTF-8 text
- **DateTime**: Timestamp with millisecond precision (JavaScript `Date`)
- **Blob**: Immutable binary data (`Uint8Array`)

### Compound Types
- **Array**: Mutable, ordered collection of values
- **Set**: Mutable, sorted collection of unique keys (uses total ordering)
- **Dict**: Mutable, sorted collection of key-value pairs (uses total ordering on keys)
- **Struct**: Immutable product type (named fields, order matters for structural typing)
- **Variant**: Immutable sum type (tagged union, cases sorted alphabetically)

### Function Type
- **Function**: First-class functions (can be serialized as IR, not as data)

### Type Constraints
- **Immutable types** (can be Dict keys or Set elements): All types except Array, Set, Dict, Function
- **Data types** (can be fully serialized): All types except Function

---

## Value Semantics and Comparison

East defines a **total ordering** on all types (implemented in `src/comparison.ts`). This enables sorted collections and deterministic serialization.

### Comparison Functions

For each type `T`, East provides:
- `equalFor(T): (a, b) => boolean` - Equality check
- `compareFor(T): (a, b) => -1 | 0 | 1` - Three-way comparison for total ordering
- `lessFor(T)`, `lessEqualFor(T)`, `greaterFor(T)`, `greaterEqualFor(T)` - Derived comparisons

### Key Semantic Rules

1. **IEEE 754 Signed Zeros**: `-0.0` and `+0.0` are **distinct** values
   - `equalFor(FloatType)(-0.0, 0.0)` returns `false`
   - `compareFor(FloatType)(-0.0, 0.0)` returns `-1` (i.e., `-0.0 < 0.0`)
   - Rationale: Mathematical correctness (`1/-0.0 === -Infinity` vs `1/0.0 === Infinity`)

2. **NaN Handling**: `NaN` is ordered (unlike JavaScript)
   - Total ordering: `-Infinity < finite values < Infinity < NaN`
   - `equalFor(FloatType)(NaN, NaN)` returns `true`

3. **Collection Ordering**: Lexicographic comparison
   - Arrays, Sets, Dicts: Element-by-element comparison
   - Shorter collections are less than longer collections with same prefix

4. **Struct Ordering**: Field-by-field lexicographic comparison
   - Field order is significant
   - `{a: 1, b: 2}` ≠ `{b: 2, a: 1}` (different field order)

5. **Variant Ordering**: Case name first, then value
   - Cases are alphabetically sorted by name
   - `variant("a", 2)` < `variant("b", 1)`

---

## Serialization Formats

East provides multiple serialization formats for different use cases:

| Format | Use Case | Preserves Types | Binary/Text | Sortable | Interoperable |
|--------|----------|-----------------|-------------|----------|---------------|
| **East Text** | Human-readable, debugging | Yes (explicit types) | Text | No | East-specific |
| **JSON** | Internal interchange, APIs | Yes (with schema) | Text | No | Limited† |
| **BEAST v1** | Database indexes, sorting | Yes | Binary | Yes‡ | East-specific |
| **BEAST v2/Avro** | External systems, Apache Arrow | Yes | Binary | No | High |

† JSON has limited interoperability for special Float values and 64-bit Integers
‡ BEAST v1 binary encoding is lexicographically sortable (memcmp-compatible)

---

## Type-Specific Edge Cases

This section documents critical edge cases for each type across all serialization formats.

### Never Type

**Semantics**: Bottom type, cannot be instantiated

| Aspect | Behavior |
|--------|----------|
| Comparison | Throws error (no values exist) |
| East Text | Cannot encode/decode |
| JSON | Cannot encode/decode |
| BEAST v1 | Cannot encode/decode |
| BEAST v2 | Cannot encode/decode |
| Compiled JS | Never executed (type-level only) |

**Implementation notes**: Used for type-level operations (union/intersection). No runtime values.

---

### Null Type

**Semantics**: Unit type with single value `null`

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `null` |
| Comparison | All nulls are equal |
| East Text | `null` |
| JSON | `null` (JSON null) |
| BEAST v1 | 1 byte: `0x00` |
| BEAST v2 | 0 bytes (no data) |
| Compiled JS | `null` |

---

### Boolean Type

**Semantics**: Two values: `false` < `true`

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `true`, `false` |
| Comparison | `false` < `true` |
| East Text | `true`, `false` |
| JSON | `true`, `false` (JSON booleans) |
| BEAST v1 | 1 byte: `0x00` (false), `0x01` (true) |
| BEAST v2 | 1 byte: `0x00` (false), `0x01` (true) |
| Compiled JS | `true`, `false` |

---

### Integer Type

**Semantics**: 64-bit signed integers (`-2^63` to `2^63-1`)

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `bigint` |
| Range | `-9223372036854775808n` to `9223372036854775807n` |
| Comparison | Numeric ordering |
| East Text | Decimal string: `"123"`, `"-456"` |
| JSON | **String** encoding: `"123"`, `"-456"` † |
| BEAST v1 | Zigzag varint (1-10 bytes) |
| BEAST v2 | Zigzag varint (1-10 bytes) |
| Compiled JS | `bigint` arithmetic |

† **JSON Limitation**: JSON numbers are IEEE 754 doubles and cannot represent all 64-bit integers. East encodes integers as strings to preserve precision. External APIs must handle this.

**Edge cases**:
- `MIN_INT64`: `-9223372036854775808n` (special case: `-2^63`)
- `MAX_INT64`: `9223372036854775807n` (`2^63-1`)
- Powers of 2 near boundaries

---

### Float Type

**Semantics**: IEEE 754 double-precision (64-bit), with total ordering including signed zeros

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `number` |
| Comparison (normal) | Numeric ordering |
| Comparison (`-0.0` vs `0.0`) | `-0.0 < 0.0` (uses `Object.is()`) |
| Comparison (NaN) | `NaN` is greatest value, all NaNs are equal |
| Total ordering | `-Infinity < -finite < -0.0 < 0.0 < +finite < Infinity < NaN` |

#### Serialization of Special Values

| Value | East Text | JSON | BEAST v1 | BEAST v2 | Compiled JS |
|-------|-----------|------|----------|----------|-------------|
| **Normal floats** | `"3.14"`, `"-2.5"` | `3.14`, `-2.5` (JSON number) | 8 bytes (bit-twiddled) | 8 bytes (IEEE 754 LE) | `3.14`, `-2.5` |
| **`0.0` (positive zero)** | `"0.0"` | `0` (JSON number) | `0x8000_0000_0000_0000` | `0x0000_0000_0000_0000` | `0` |
| **`-0.0` (negative zero)** | `"-0.0"` | `"-0.0"` **(string)** † | `0x7FFF_FFFF_FFFF_FFFF` | `0x8000_0000_0000_0000` | `-0` |
| **`NaN`** | `"NaN"` | `"NaN"` **(string)** † | Canonical NaN | Canonical NaN `0x7FF8_0000_0000_0000` | `NaN` |
| **`Infinity`** | `"Infinity"` | `"Infinity"` **(string)** † | `0xFF..FF` | `0x7FF0_0000_0000_0000` | `Infinity` |
| **`-Infinity`** | `"-Infinity"` | `"-Infinity"` **(string)** † | `0x00..00` | `0xFFF0_0000_0000_0000` | `-Infinity` |

† **JSON Limitation**: JSON spec (ECMA-404, RFC 8259) does not support `NaN`, `Infinity`, or signed zeros. East encodes these as **strings** for lossless round-tripping. This requires **type-driven decoding** (the decoder knows from the East type schema whether a string is an Integer or Float special value). External APIs without East schemas cannot decode these reliably.

**Interoperability Options**:
1. Use BEAST v2/Avro format (native IEEE 754 support, interoperable with Apache Arrow, Protobuf)
2. Accept data loss in JSON (serialize `-0.0` as `0`, `NaN`/`Infinity` as `null`)
3. Use tagged union in JSON (e.g., `{"type": "NaN"}`)

#### Bit-Level Encoding Details

**BEAST v1** (memcmp-sortable):
- Positive floats (including `+0.0`): XOR sign bit → ensures `0.0 > -0.0` in byte comparison
- Negative floats (including `-0.0`): Flip all bits → reverses byte ordering for negatives
- Example: `-0.0` = `0x7FFF_FFFF_FFFF_FFFF`, `+0.0` = `0x8000_0000_0000_0000` (lexicographic order matches numeric)

**BEAST v2** (IEEE 754 little-endian):
- Standard `DataView.setFloat64(offset, value, true)`
- `-0.0`: Sign bit set, all other bits zero
- `+0.0`: All bits zero
- NaN normalization: All NaN bit patterns encoded as canonical quiet NaN for determinism

**Compiled JavaScript**:
- Native `number` arithmetic, inherently supports signed zeros
- Equality uses `Object.is()` when type is Float (matches East semantics)

---

### String Type

**Semantics**: UTF-8 text, lexicographic ordering

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `string` |
| Encoding | UTF-8 |
| Comparison | Lexicographic (code point order) |
| East Text | Quoted, escapes: `\`, backtick |
| JSON | JSON string (standard escaping) |
| BEAST v1 | Null-terminated UTF-8 bytes |
| BEAST v2 | Varint length + UTF-8 bytes |
| Compiled JS | `string` |

**Edge cases**:
- Empty string: `""`
- Unicode: CJK characters, emoji (multi-byte UTF-8)
- Special characters: Newlines, quotes, control characters (must be escaped in text formats)

---

### DateTime Type

**Semantics**: Timestamp with millisecond precision

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `Date` |
| Precision | Milliseconds |
| Comparison | Numeric timestamp ordering |
| East Text | RFC 3339 with timezone: `"2024-01-15T10:30:00.123+00:00"` |
| JSON | RFC 3339 with timezone: `"2024-01-15T10:30:00.123Z"` † |
| BEAST v1 | 8 bytes: signed 64-bit ms since epoch |
| BEAST v2 | 8 bytes: signed 64-bit ms since epoch |
| Compiled JS | `Date` object |

† **JSON Format**: Always uses UTC timezone (`Z` or `+00:00`) per RFC 3339 Section 5.6. "Unqualified local time" is forbidden (RFC 3339 Section 4.3).

**Edge cases**:
- Unix epoch: `1970-01-01T00:00:00.000Z`
- Negative timestamps (before 1970)
- Far future/past dates (within JavaScript Date range: ±100,000,000 days from epoch)

---

### Blob Type

**Semantics**: Immutable binary data

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `Uint8Array` |
| Comparison | Lexicographic byte comparison |
| East Text | Hex string: `"0x48656c6c6f"` |
| JSON | Hex string: `"0x48656c6c6f"` |
| BEAST v1 | Varint length + raw bytes |
| BEAST v2 | Varint length + raw bytes |
| Compiled JS | `Uint8Array` |

**Edge cases**:
- Empty blob: `0x` (0 bytes)
- Large blobs (megabytes)
- All byte values `0x00` to `0xFF`

---

### Array Type

**Semantics**: Mutable, ordered collection

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `Array` |
| Comparison | Lexicographic element comparison |
| East Text | `[elem1, elem2, ...]` |
| JSON | JSON array: `[elem1, elem2, ...]` |
| BEAST v1 | Continuation-byte encoding (elements terminated by sentinel) |
| BEAST v2 | Varint length + elements |
| Compiled JS | `Array` |

**Edge cases**:
- Empty array: `[]`
- Nested arrays: `[[1, 2], [3, 4]]`
- Large arrays (thousands of elements)
- Arrays with mutable elements (allowed, but elements cannot be Dict keys)

---

### Set Type

**Semantics**: Mutable, sorted collection of unique keys

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `SortedSet` (custom class) or native `Set` |
| Invariant | Keys are sorted by `compareFor(keyType)` |
| Comparison | Lexicographic key comparison |
| East Text | `{elem1, elem2, ...}` |
| JSON | Array of keys: `[key1, key2, ...]` † |
| BEAST v1 | Same as Array encoding |
| BEAST v2 | Array encoding + metadata tag (distinguishes from Array) |
| Compiled JS | `SortedSet` |

† **JSON Format**: Encodes as array. Metadata in East type schema distinguishes Set from Array. External systems without schemas will see a plain JSON array.

**Edge cases**:
- Empty set: `{}`
- Sets with Float keys (including `-0.0` vs `0.0`)
- Large sets

---

### Dict Type

**Semantics**: Mutable, sorted collection of key-value pairs

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `SortedMap` (custom class) or native `Map` |
| Invariant | Keys are sorted by `compareFor(keyType)` |
| Comparison | Lexicographic comparison (keys first, then values) |
| East Text | `{key1: value1, key2: value2, ...}` |
| JSON | Array of objects: `[{"key": k1, "value": v1}, ...]` † |
| BEAST v1 | Array of key-value pairs |
| BEAST v2 | Array of key-value pairs + metadata tag |
| Compiled JS | `SortedMap` |

† **JSON Format**: Encodes as array of `{"key": ..., "value": ...}` objects. External systems without East schemas will see a plain JSON array.

**Edge cases**:
- Empty dict: `{}`
- Non-string keys (e.g., Integer, Float)
- Dicts with complex keys (Struct, Variant)

---

### Struct Type

**Semantics**: Immutable product type (named fields)

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | Plain object `{}` |
| Field order | Significant for structural typing |
| Comparison | Field-by-field lexicographic comparison |
| East Text | `(field1=value1, field2=value2, ...)` |
| JSON | JSON object: `{"field1": value1, "field2": value2, ...}` |
| BEAST v1 | Field values in order (no field names) |
| BEAST v2 | Field values in order + schema metadata |
| Compiled JS | Plain object `{}` |

**Edge cases**:
- Empty struct: `()`
- Nested structs
- Field names requiring quoting (non-identifier characters)
- Field order mismatch (different types)

---

### Variant Type

**Semantics**: Immutable sum type (tagged union)

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | `{type: "caseName", value: ..., [variant_symbol]: null}` |
| Case order | Alphabetically sorted by case name |
| Comparison | Case name first (lexicographic), then value |
| East Text | `.caseName value` or `.caseName null` |
| JSON | `{"type": "caseName", "value": ...}` |
| BEAST v1 | Varint case index + value |
| BEAST v2 | Varint case index + value |
| Compiled JS | `variant("caseName", value)` |

**Edge cases**:
- Nullary variants (no data): `.none null`
- Nested variants
- Case name ordering (`a` < `b` in all formats)

---

### Function Type

**Semantics**: First-class functions (not serializable as data)

| Aspect | Behavior |
|--------|----------|
| JavaScript representation | Function |
| Comparison | Throws error (functions not comparable) |
| East Text | Prints as `λ` (cannot parse) |
| JSON | Cannot encode/decode |
| BEAST v1 | Cannot encode/decode |
| BEAST v2 | Type schema only (no data) |
| Compiled JS | JavaScript function |

**Notes**: Functions can be serialized as **IR** (intermediate representation) but not as **data**. Used for expression compilation, not data interchange.

---

## Implementation Reference

### TypeScript Implementation

- **Types**: `src/types.ts` - Type definitions, constructors, type operations
- **Comparison**: `src/comparison.ts` - `equalFor`, `compareFor`, `lessFor`, etc.
- **Compilation**: `src/compile.ts` - Compiles East IR to executable JavaScript
- **Serialization**:
  - East text: `src/serialization/east.ts`
  - JSON: `src/serialization/json.ts`
  - BEAST v1: `src/serialization/beast.ts`, `src/serialization/binary-utils.ts`
  - BEAST v2/Avro: `src/serialization/beast2.ts`, `src/serialization/avro-schema.ts`

### Key Implementation Patterns

#### Signed Zero Detection

```typescript
// Use Object.is() to distinguish -0.0 from 0.0
if (Object.is(value, -0)) {
  // Handle negative zero
} else if (value === 0) {
  // Handle positive zero
}
```

#### NaN Normalization

```typescript
// Canonical quiet NaN: 0x7FF8_0000_0000_0000
if (isNaN(value)) {
  return 0x7FF8_0000_0000_0000n; // Canonical representation
}
```

#### Type-Driven Decoding

All decoders take an `EastType` parameter to determine how to interpret values:

```typescript
function decodeJSONFor<T extends EastType>(type: T): (value: unknown) => ValueTypeOf<T>
```

This enables the same JSON value (e.g., string `"-0.0"`) to be decoded differently based on context:
- If `type = IntegerType`: Error (integers don't have signed zeros)
- If `type = FloatType`: Decoded as `-0.0`

#### Frozen Data

All decoders support a `frozen` parameter to produce immutable data:

```typescript
const decoder = decodeJSONFor(myType, frozen = true);
```

This recursively freezes decoded objects/arrays/collections (useful for security, preventing script mutation of platform data).

---

## Testing and Validation

### Fuzz Testing

The East test suite includes fuzz tests (`src/fuzz.ts`) that:
- Generate random types
- Generate random values conforming to those types
- Verify round-trip serialization preserves semantics
- Explicitly test edge cases (e.g., `-0.0` has 25% probability when generating Floats)

### Compliance Tests

When implementing East in a new language, verify:
1. **Comparison**: Total ordering matches TypeScript implementation
2. **Serialization round-trips**: `decode(encode(value)) == value` for all formats
3. **Cross-language interop**: Binary formats (BEAST v2) are byte-compatible
4. **Edge cases**: All special values in this document serialize/deserialize correctly

### Reference Test Suite

The `test/` directory contains compliance tests that execute on the self-hosted platform and other backends. These tests are format-agnostic and verify semantic correctness across implementations.

---

## Design Rationale

### Why Distinguish `-0.0` and `0.0`?

IEEE 754 signed zeros have mathematical significance:
- `1 / -0.0 === -Infinity`
- `1 / 0.0 === Infinity`
- Preserving the sign enables correct analysis (e.g., approaching a limit from below vs above)

Total ordering enables using Floats as Dict keys and Set elements.

### Why String Encoding for Special Floats in JSON?

JSON does not support `NaN`, `Infinity`, or signed zeros per spec (ECMA-404, RFC 8259). Options:
1. **String encoding** (current approach): Lossless, but requires East type schemas
2. **Data loss**: Serialize as `null` or `0` - simpler for external APIs, loses information
3. **Binary formats**: Use BEAST v2/Avro for full IEEE 754 support

East prioritizes **internal correctness** with type-driven decoding. For external APIs, use BEAST v2 or accept data loss.

### Why Sorted Collections?

Deterministic ordering:
- Enables binary search and efficient lookups
- Ensures consistent serialization (same set always serializes identically)
- Simplifies comparison (element-by-element lexicographic order)
- Critical for database indexes (BEAST v1 memcmp-sortable format)

---
