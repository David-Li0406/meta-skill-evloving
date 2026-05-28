# East Binary Serialization Format

## Purpose

Network-optimized binary encoding for East values and types. Used for transmitting data between Elara SDK (TypeScript/JavaScript) and backend (Julia), between server and client, and for efficient storage/caching.

**Encoding is Avro-compatible** where possible, allowing interop with Avro tooling while supporting East's richer type system through metadata.

## Design Requirements

- **Network efficiency**: Hundreds of MB datasets, millions of small strings, minimal overhead for small messages
- **Avro compatibility**: Binary encoding matches Apache Avro for interoperability with Julia `Avro.jl` and other tools
- **64-bit safe**: Julia runtime uses full 64-bit address space; must support up to `Number.MAX_SAFE_INTEGER` (2^53-1) for sizes/lengths
- **Security hardened**: No data smuggling via NaN payloads (banking/compliance requirement)
- **Flexible headers**: Support multiple modes - self-describing, Avro container, or header-free for known schemas
- **Simple and fast**: Closure-compiler pattern, minimal allocations
- **Version compatible**: Magic bytes + version for format evolution

## Format Specification

### Encoding Primitives

**Varint (unsigned LEB128)**
- Variable-length encoding for non-negative integers
- 7 bits per byte, MSB = continuation bit
- Range: 0 to 2^63-1 (sufficient for JavaScript safe integers)
- Examples:
  - `0` → `0x00` (1 byte)
  - `127` → `0x7F` (1 byte)
  - `128` → `0x80 0x01` (2 bytes)
  - `16383` → `0xFF 0x7F` (2 bytes)

**Zigzag varint (signed)**
- Maps signed integers to unsigned: `(n << 1) ^ (n >> 63)`
- Then encoded as varint
- Examples:
  - `0` → `0` → `0x00`
  - `-1` → `1` → `0x01`
  - `1` → `2` → `0x02`
  - `-2` → `3` → `0x03`

**UTF-8 String**
- Varint length (byte count)
- UTF-8 encoded bytes
- Uses custom encoder (faster for small strings than TextEncoder as of 2021)
- Decoder can use `buffer.subarray()` to avoid copies

**Float64 (IEEE 754)**
- 8 bytes, **little-endian** (Avro-compatible)
- **NaN normalization**: All NaN values written as canonical quiet NaN `0x000000000000F87F` (little-endian)
- **NaN validation on read**: Reject any non-canonical NaN patterns (security hardening)

### Value Encoding

**Binary encoding is Avro-compatible** - identical to Apache Avro binary format for interoperability.

All lengths/counts use **varint unsigned** encoding (LEB128).

| Type | Encoding | Avro Equivalent |
|------|----------|-----------------|
| **Null** | *(empty - no bytes)* | `null` |
| **Boolean** | 1 byte: `0x00` (false) or `0x01` (true) | `boolean` |
| **Integer** | Zigzag varint (1-10 bytes for int64 range) | `long` |
| **Float** | 8 bytes IEEE 754 double, **little-endian**, canonical NaN | `double` |
| **String** | Varint length + UTF-8 bytes | `string` |
| **DateTime** | Zigzag varint (milliseconds since Unix epoch) | `long` with `logicalType: "timestamp-millis"` |
| **Blob** | Varint length + raw bytes | `bytes` |
| **Array** | Varint length + N values (each encoded per element type) | `array` |
| **Set** | Varint length + N keys (sorted order) | `array` with `"east": "set"` metadata |
| **Dict** | Varint length + N × (key, value) pairs (sorted by key) | `array` of records with `"east": "dict"` metadata |
| **Ref** | Contained value | |
| **Struct** | Fields in declaration order *(no length - known from type)* | `record` |
| **Variant** | Varint tag index + value (encoded per case type) | Avro union of records |
| **Function** | *(not serializable - error)* | *(not supported)* |
| **AsyncFunction** | *(not serializable - error)* | *(not supported)* |

### Type Encoding

Used for encoding `EastType` itself (schema transmission).

**Type tags** (varint encoded):
```
00 - Array
01 - Blob
02 - Boolean
03 - DateTime
04 - Dict
05 - Float
06 - Function
07 - Integer
08 - Never
09 - Node (not yet implemented)
10 - Null
11 - Set
12 - String
13 - Struct
14 - Tree (not yet implemented)
15 - Variant
```

These are sorted alphabetically because that's how variant tags are _always_ serialized.
The future Tree/Node recursive type will allow us to refer to types as East values, and this encoding should be binary compatible (tree nodes themselves will be "transparent" in the encoding).

**Compound type encoding**:
- `Array<T>`: tag(0) + encode(T)
- `Set<T>`: tag(11) + encode(T)
- `Dict<K,V>`: tag(4) + encode(K) + encode(V)
- `Struct{f1:T1, f2:T2, ...}`: tag(13) + varint(fieldCount) + [(string(name) + encode(T))]
- `Variant{c1:T1, c2:T2, ...}`: tag(15) + varint(caseCount) + [(string(name) + encode(T))]

Note: Struct/Variant fields/cases are encoded in iteration order (already sorted for Variant).

### Avro Schema Mapping

East types can be represented as Avro schemas for file storage and interoperability. Custom properties are used to preserve East semantics.

**Type Mapping:**

All East types include `"east": "<TypeName>"` metadata for type identification when reading back, except for Avro unions (which represent the variant wrapper itself).

| East Type | Avro Schema | Notes |
|-----------|-------------|-------|
| `NullType` | `{"type": "null", "east": "Null"}` | With East metadata |
| `BooleanType` | `{"type": "boolean", "east": "Boolean"}` | With East metadata |
| `IntegerType` | `{"type": "long", "east": "Integer"}` | 64-bit signed integer |
| `FloatType` | `{"type": "double", "east": "Float"}` | 64-bit float |
| `StringType` | `{"type": "string", "east": "String"}` | UTF-8 encoded |
| `DateTimeType` | `{"type": "long", "logicalType": "timestamp-millis", "east": "DateTime"}` | Standard Avro logical type |
| `BlobType` | `{"type": "bytes", "east": "Blob"}` | With East metadata |
| `ArrayType<T>` | `{"type": "array", "items": <T>, "east": "Array"}` | With East metadata |
| `SetType<T>` | `{"type": "array", "items": <T>, "east": "Set"}` | Sorted array (Set vs Array distinguished by metadata) |
| `DictType<K,V>` | `{"type": "array", "items": {"type": "record", ...}, "east": "Dict"}` | Array of `{key, value}` records |
| `StructType{...}` | `{"type": "record", "name": "_<n>", "east": "Struct", "fields": [...]}` | Ordinal name + metadata |
| `VariantType{...}` | `[{"type": "record", "name": "_<n>", "east": "<caseName>", "fields": [{"name": "value", ...}]}, ...]` | Union of records with ordinal names; case name in metadata |

**Name Generation:**
- Structs: `_0`, `_1`, ... (ordinal from depth-first type tree traversal)
- Variant case records: `_0`, `_1`, ... (same ordinal namespace as structs)
- All generated names use leading underscore to avoid collisions
- Single namespace per Avro file - ordinals are unique within the type tree

**Set/Dict Encoding:**
- Sets encoded as sorted arrays with `"east": "Set"` metadata (distinguishes from Array)
- Dicts encoded as sorted arrays of `{key: K, value: V}` records with `"east": "Dict"` metadata
- Deduplication on read if needed for Sets

### Message Format Modes

East supports **three message modes** for different use cases:

**Mode 1: East Self-Describing (minimal overhead)**
```
[8-byte East header]
[Type encoding (binary)]
[Value data]
```
- Use for: Self-describing messages, single-value files, debugging
- Overhead: ~8 bytes header + type encoding (typically 10-50 bytes)
- Magic bytes: `0x89 0x45 0x61 0x73 0x74 0x0D 0x0A <version>`

**Mode 2: Header-Free (zero overhead)**
```
[Value data only]
```
- Use for: High-frequency messages where schema is known by both parties (e.g., API endpoint)
- Overhead: 0 bytes
- Schema must be agreed upon out-of-band

**Mode 3: Avro Container File (maximum compatibility)**
```
[Avro magic bytes: 0x4F 0x62 0x6A 0x01]
[Avro metadata map with JSON schema]
[Data blocks with sync markers]
```
- Use for: File storage, sharing with non-East tools, schema evolution
- Overhead: ~100+ bytes (full JSON schema in header)
- Compatible with `avro-tools`, `Avro.jl`, etc.

**Choosing a mode:**
- **Real-time UI updates**: Mode 2 (header-free) - schema known, zero overhead
- **File storage**: Mode 3 (Avro container) - maximum compatibility
- **One-off messages**: Mode 1 (East minimal) - self-describing, low overhead
- **Debugging/inspection**: Mode 1 or Mode 3

### East Minimal Header Format (Mode 1)

```
Header (8 bytes):
  0x89          - Invalid UTF-8 marker (like PNG)
  0x45 0x61 0x73 0x74 - "East" (human-readable in hex dumps)
  0x0D 0x0A     - CRLF (detects line-ending corruption)
  0x01          - Version byte (currently 1)

Type schema:    encoded EastType
Value data:     encoded value
```

Total header: 8 bytes + type encoding

The header uses PNG-style magic bytes to ensure file is recognized as binary:
- `0x89` is invalid UTF-8, preventing text interpretation
- CRLF detects text-mode transmission corruption
- Version byte allows format evolution

## Implementation Architecture

### Closure-Compiler Pattern

```typescript
// Factory functions return specialized closers
export function encodeFor(type: EastType): (value: any, writer: BufferWriter) => void
export function decodeFor(type: EastType): (reader: BufferReader) => any
```

Similar to existing `printFor()`, `equalFor()`, `parseFor()` pattern.

### Buffer Management

**BufferWriter** (managed Uint8Array with auto-growth):
```typescript
class BufferWriter {
  private buffer: Uint8Array
  private offset: number = 0
  private view: DataView  // for numeric writes

  constructor(initialCapacity = 16384)  // 16KB default

  // Auto-resize: exponential growth (2x), max +1GB per resize
  private ensureCapacity(needed: number): void

  // Primitive writes
  writeUint8(value: number): void
  writeVarint(value: number): void           // unsigned LEB128, for sizes/lengths/tags
  writeZigzag(value: bigint): void           // signed zigzag varint for IntegerType
  writeFloat64(value: number): void          // with NaN normalization
  writeBytes(bytes: Uint8Array): void        // raw copy
  writeStringUtf8(str: string): void         // varint length + custom UTF-8

  // Export
  toUint8Array(): Uint8Array                 // returns subarray (no copy)
}
```

**Stateless read functions** (use native DataView/Uint8Array):
```typescript
// Varint decoding - returns [value, newOffset]
function readVarint(buffer: Uint8Array, offset: number): [number, number]
  // Unsigned varint → number for sizes/lengths/tags
  // Throws if value > Number.MAX_SAFE_INTEGER

function readZigzag(buffer: Uint8Array, offset: number): [bigint, number]
  // Zigzag varint → bigint for signed IntegerType values

// Numeric reads using DataView
function readFloat64(view: DataView, offset: number): number
  // With NaN validation (throws on non-canonical)

// UTF-8 string (uses TextDecoder or custom)
function readStringUtf8(buffer: Uint8Array, offset: number): [string, number]
  // Reads varint length, then decodes string
```

**Rationale**: BufferWriter provides real value (auto-resize is tedious to manage). A BufferReader would just be ceremony - stateless functions with explicit offset tracking are simpler and avoid unnecessary object allocation.

### UTF-8 Encoding/Decoding

Adapt from old implementation (`../ELARACore/javascript/libs/core/src/east/binary.ts`):
- `utf8EncodeInto(str: string, buffer: Uint8Array, offset: number): number` - returns new offset
- `utf8Decode(bytes: Uint8Array, offset: number, length: number): string`

Changes from old code:
- Decoder takes explicit `length` parameter (no null-termination scan)
- Can pass `bytes.subarray(offset, offset + length)` to avoid copies

### NaN Security Hardening

**On encode** (`writeFloat64`):
```typescript
if (Number.isNaN(value)) {
  view.setBigUint64(offset, 0x000000000000F87Fn, true);  // canonical quiet NaN (little-endian)
} else {
  view.setFloat64(offset, value, true); // little-endian (Avro-compatible)
}
```

**On decode** (`readFloat64`):
```typescript
function readFloat64(view: DataView, offset: number): number {
  const bits = view.getBigUint64(offset, true); // little-endian
  // Check for NaN (exponent = all 1s, mantissa != 0)
  if ((bits & 0x7FF0000000000000n) === 0x7FF0000000000000n &&
      (bits & 0x000FFFFFFFFFFFFFn) !== 0n) {
    // It's a NaN - must be canonical quiet NaN
    if (bits !== 0x000000000000F87Fn && bits !== 0x000000000000F8FFn) {
      throw new Error(`Non-canonical NaN at offset ${offset}: 0x${bits.toString(16)}`);
    }
  }
  return view.getFloat64(offset, true); // little-endian
}
```

Rejects signaling NaNs, NaN payloads, etc. Only allows canonical quiet NaN (positive or negative).
**Note:** Little-endian encoding matches Apache Avro for cross-platform compatibility.

## API Surface

```typescript
// Mode 2: Header-free encoding (zero overhead, schema must be known)
export function encode(type: EastType, value: any): Uint8Array
export function decode(type: EastType, data: Uint8Array): any

// Mode 1: East minimal header (self-describing, low overhead)
export function encodeWithHeader(type: EastType, value: any): Uint8Array
export function decodeWithHeader(data: Uint8Array): { type: EastType, value: any }

// Mode 3: Avro container file (maximum compatibility)
export function encodeAvro(type: EastType, value: any): Uint8Array
export function decodeAvro(data: Uint8Array): { type: EastType, value: any }

// Type schema encoding/decoding (used internally by Mode 1)
export function encodeType(type: EastType): Uint8Array
export function decodeType(data: Uint8Array): EastType

// Avro schema generation (used internally by Mode 3)
export function toAvroSchema(type: EastType): object  // Returns Avro JSON schema
export function fromAvroSchema(schema: object): EastType  // Parse Avro schema to East type

// Low-level primitives (for advanced use)
export class BufferWriter { ... }
export function readVarint(buffer: Uint8Array, offset: number): [number, number]
export function readZigzag(buffer: Uint8Array, offset: number): [bigint, number]
export function readFloat64(view: DataView, offset: number): number
export function readStringUtf8(buffer: Uint8Array, offset: number): [string, number]
export function encodeFor(type: EastType): (value: any, writer: BufferWriter) => void
export function decodeFor(type: EastType): (buffer: Uint8Array, offset: number) => [any, number]
```

## Implementation TODO

### Phase 1: Buffer Infrastructure
- [x] Implement `BufferWriter` class with varint/zigzag/float64 methods
- [x] Implement stateless read functions: `readVarint`, `readZigzag`, `readFloat64` (with NaN validation)
- [x] Port UTF-8 encoder/decoder from old codebase (adapt for length-prefix)
- [x] Unit tests for buffer primitives (varints, zigzag, UTF-8, NaN handling)

### Phase 2: Value Encoding/Decoding (Avro-compatible)
- [x] Update `BufferWriter.writeFloat64()` to use little-endian (Avro-compatible)
- [x] Update `readFloat64()` to use little-endian with updated NaN validation
- [x] Implement `encodeFor()` factory for primitive types (Null, Boolean, Integer, Float, String, DateTime, Blob)
- [x] Implement `decodeFor()` factory for primitive types
- [x] Implement `encodeFor()` for compound types (Array, Set, Dict, Struct, Variant)
- [x] Implement `decodeFor()` for compound types
- [x] Error handling for Function type (not serializable)
- [x] NeverType errors at runtime, not when the factory is called (for empty arrays, etc)
- [x] Implement `encode()` and `decode()` high-level API (Mode 2: header-free)

### Phase 3: Type Schema Encoding (East Binary Format)
- [x] Implement `encodeTypeToBuffer(type: EastType, writer: BufferWriter)`
- [x] Implement `decodeTypeFromBuffer(buffer: Uint8Array, offset: number): [EastType, number]`
- [x] `encodeType()` and `decodeType()` wrapper functions
- [x] Unit tests for type encoding/decoding (28 tests passing)

### Phase 4: Avro Schema Mapping
- [x] Implement `toAvroSchema(type: EastType): object` - generate Avro JSON schema
- [x] Implement ordinal name generation for records (structs and variant cases)
  - Single namespace: `_0`, `_1`, `_2`, ... for all records in depth-first traversal
  - Track ordinal counter during recursive schema generation
- [x] Add `"east"` metadata to ALL types (primitives, compounds, records)
  - Primitives: `"east": "Integer"`, `"east": "String"`, etc.
  - Arrays/Sets/Dicts: `"east": "Array"`, `"east": "Set"`, `"east": "Dict"`
  - Structs: `"east": "Struct"` on the record
  - Variant cases: `"east": "<caseName>"` on each union member record (preserves original case name)
  - Exception: Avro unions themselves (the variant wrapper) get no metadata
- [x] Implement `fromAvroSchema(schema: object): EastType` - parse Avro schema
- [x] Handle `"east"` metadata to reconstruct correct East types
  - Distinguish Set from Array using metadata
  - Distinguish Dict from other array-of-records using metadata
  - Reconstruct variant case names from record metadata
  - Validate that all types have expected metadata
- [x] Unit tests for Avro schema mapping (33 tests passing)

### Phase 5: High-Level API (Three Modes)
- [x] Implement `encode()` and `decode()` functions (Mode 2: header-free)
- [x] Magic bytes constant: `MAGIC_BYTES = [0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01]`
- [x] Implement `encodeBeast()` and `decodeBeast()` (Mode 1: East minimal)
- [x] Unit tests for Beast format (36 tests passing)
- [x] Implement `encodeAvro()` and `decodeAvro()` (Mode 3: Avro container file)
- [x] Unit tests for Avro container format (32 tests passing)

### Phase 6: Testing
- [ ] Update float64 tests to expect little-endian encoding
- [ ] Port tests from `../ELARACore/javascript/libs/core/src/east/binary.spec.ts`
- [ ] Add security tests: NaN smuggling attempts (various bit patterns)
- [ ] Add size tests: large blobs (100MB+), deep nesting, millions of strings
- [ ] Add edge cases: empty collections, MAX_SAFE_INTEGER, extreme dates
- [ ] Fuzz testing for malformed inputs (truncated data, invalid varints, etc.)
- [ ] Test all three message modes (header-free, East minimal, Avro container)
- [ ] Cross-check Avro mode with `avro-tools` or `Avro.jl`

### Phase 7: Optimization (if needed)
- [ ] Benchmark against old implementation
- [ ] Profile hot paths (likely: varint encode/decode, UTF-8)
- [ ] Consider `TextEncoder.encodeInto()` if modern runtimes improved (Node 22, Chrome/Edge 2024+)
- [ ] Measure compression: compare size reduction vs old null-terminated format
- [ ] Test header overhead in practice (Mode 1 vs Mode 2 vs Mode 3)

## Size Estimates

Typical savings vs old format (null-terminated, fixed 4-byte lengths):

- Small integers (0-1000): 1-2 bytes vs 8 bytes → **75-87% savings**
- Recent dates: ~6 bytes vs 8 bytes → **25% savings**
- Small strings ("hello"): 6 bytes vs 13 bytes (or 6 bytes with null termination) → **0-54% savings**
- Array lengths: 1-2 bytes vs 8 bytes → **75-87% savings**
- Variant tags: 1 byte vs 1 byte → **same**

**Overall dataset compression: ~30-50% size reduction** for typical Elara data (mix of integers, dates, strings, small arrays).

For 100MB dataset → ~50-70MB after binary encoding (before any additional compression like gzip).

## Design Decisions Summary

**Avro Compatibility:**
- Binary encoding matches Apache Avro for maximum interoperability
- Little-endian float encoding (Avro standard, not network byte order)
- Custom `"east"` metadata properties preserve East-specific type information
- Compatible with `Avro.jl` (Julia), `avro-tools`, and other Avro implementations

**Type System Mapping:**
- **All types**: Include `"east": "<TypeName>"` metadata for type identification
- **Set**: Encoded as sorted array with `"east": "Set"` metadata (distinguishes from Array)
- **Dict**: Encoded as sorted array of `{key, value}` records with `"east": "Dict"` metadata
- **Variant**: Encoded as Avro union of records, each with:
  - Single `"value"` field containing the case payload
  - Ordinal name (`_0`, `_1`, ...) shared namespace with structs
  - `"east": "<caseName>"` metadata preserving original case name
- **Struct**: Anonymous structs get ordinal names (`_0`, `_1`, ...) with `"east": "Struct"` metadata
- **DateTime**: Uses standard Avro `logicalType: "timestamp-millis"` plus `"east": "DateTime"`

**Message Modes:**
1. **Header-free** (Mode 2): Zero overhead for known schemas (real-time UI updates)
2. **East minimal** (Mode 1): 8-byte header + binary type schema (self-describing)
3. **Avro container** (Mode 3): Full Avro file format (file storage, max compatibility)

**Security:**
- Canonical NaN enforcement prevents data smuggling
- All decode functions validate input and throw on malformed data
- Bounds checking on all reads

**Performance:**
- Custom UTF-8 encoder/decoder for small strings (faster than TextEncoder as of 2021)
- Varint encoding with safe integer validation
- Auto-resizing buffer writer with exponential growth
- Zero-copy operations where possible (subarray, views)
