# Serialization Reference and Aliasing Design

This document describes how East serialization formats handle circular references and shared mutable data.

## Summary

East's serialization formats support references using unified `$.path` syntax for:
1. **Circular references** - Structural cycles in RecursiveType values
2. **Mutable aliases** - Object identity preservation for shared Array/Set/Dict instances

References use absolute paths from the root value (e.g., `$.field.subfield[0]`) to identify both circular references and shared mutable data. This provides a simple, consistent mechanism for both use cases.

This is **not** general-purpose compression or dictionary encoding. References are created automatically only when necessary to preserve semantics. Immutable values (structs, variants, primitives) are always duplicated, even if identical.

## Goals

1. **Circular references**: Support recursive types with cycles (e.g., `A -> B -> A`)
2. **Shared references**: Preserve object identity for mutable data (Array/Set/Dict)
3. **Single-pass streaming**: Encode and decode in one pass without building reference tables upfront
4. **Independence**: Multiple values in a stream are independent (contexts reset between values)
5. **Semantic preservation**: No lossy transformations, maintain exact structure semantics

## Aliasable Types

References are created automatically for:
- **Circular references**: Within RecursiveType structures (parent, grandparent, etc.)
- **Shared mutable collections**: When the same Array/Set/Dict instance appears multiple times

**Rationale:** This preserves the semantic meaning of the data structure (cycles and object identity) without implementing general compression or dictionary encoding.

Immutable types (Struct, Variant, primitives, Blob) are always duplicated. Even if the same immutable value appears multiple times, it will be serialized repeatedly rather than using references.

**Important constraints:**
- **Set/Dict keys are immutable**: Keys cannot contain mutable data (Array/Set/Dict). This ensures b-tree ordering and uniqueness-under-deep-value-equality are preserved.
- **Set/Dict keys are never referenced**: References only apply to the Set/Dict container itself or to Dict values. Individual keys are always inlined.
- **Array elements**: Can be any type, including mutable collections that may be referenced.
- **Dict values**: Can be any type, including mutable collections that may be referenced.

**Future extensions:** A `RefType` (mutable reference cell) may be added later to enable explicit sharing of arbitrary values. General aliasing for compression could also be added, using the same reference syntax.

## JSON Format

### Reference Syntax

References use the special object `{ "$ref": "#/path" }` where path is a JSON Pointer (RFC 6901).

**Example (shared mutable array):**
```json
{
  "list": [1, 2, 3],
  "ref1": { "$ref": "#/list" },
  "ref2": { "$ref": "#/list" }
}
```

After deserialization, `ref1` and `ref2` point to the same mutable array instance as `list`.

**Example (circular reference):**
```json
{
  "value": 42,
  "self": { "$ref": "#" }
}
```

The `self` field references the root object, creating a cycle.

### Path Format

JSON Pointer paths using `/` separator (RFC 6901):
- `/field` - struct field (escaping as per JSON Pointer spec)
- `/tag` - variant case name (accessing the case value)
- `/tag/field` - field within variant case value
- `/0` - array element at index 0
- `/0` - set element at index 0 (sorted order)
- `/0` - dict entry at index 0 (sorted key order)
- `/0/key` - key of dict entry at index 0 (rarely needed, keys are immutable)
- `/0/value` - value of dict entry at index 0

**Note on Dict access:** JSON format uses **ordinal indices** for dict entries because JSON Pointer (RFC 6901) uses `/` as separator, making it difficult to embed arbitrary East values (like struct keys) in the path. Dict entries are indexed in sorted key order for deterministic serialization.

### Collision Avoidance

The `{ "$ref": "..." }` syntax cannot collide with user data because:
1. Arrays/Sets/Dicts serialize as JSON arrays (no object form)
2. `RecursiveType` constructor validates that the inner type actually contains recursion
3. This prevents `RecursiveType(_ => StructType({ "$ref": StringType }))` which would be the only way to create a collision

### Encoding Algorithm

```typescript
interface JsonEncoderContext {
  refs: Map<any, string>;  // object -> JSON Pointer path
  currentPath: string[];   // Current position in JSON structure
}

function toJSON(value: any, type: EastType, ctx: JsonEncoderContext): any {
  if (isAliasable(type)) {
    if (ctx.refs.has(value)) {
      // Reference previously seen object
      return { "$ref": "#" + ctx.refs.get(value) };
    }

    // First encounter - add to refs and serialize
    ctx.refs.set(value, "/" + ctx.currentPath.join("/"));
    // ... continue with normal serialization ...
  }

  // ... handle non-aliasable types ...
}
```

### Decoding Algorithm

```typescript
interface JsonDecoderContext {
  refs: Map<string, any>;  // path -> deserialized object
  currentPath: string[];   // Current position during traversal
}

function fromJSON(json: any, type: EastType, ctx: JsonDecoderContext): any {
  // Check for reference
  if (json && typeof json === 'object' && "$ref" in json) {
    const path = json["$ref"].substring(1); // Remove '#' prefix
    return ctx.refs.get(path);
  }

  if (isAliasable(type)) {
    const path = "/" + ctx.currentPath.join("/");
    // Create object placeholder before descending (for circular refs)
    const obj = createPlaceholder(type);
    ctx.refs.set(path, obj);
    // ... populate object ...
    return obj;
  }

  // ... handle non-aliasable types ...
}
```

## East Text Format

### Reference Syntax

East text format has **two distinct reference syntaxes** for different purposes:

#### 1. Circular References: `@N` (Depth Markers)

**Syntax:**
```
circular_ref := '@' integer path_segment*
```

**Semantics:**
- `@N` refers to the value **N levels up** in the nesting hierarchy
- `@0` is the current value itself (self-reference)
- `@1` is the parent, `@2` is grandparent, etc.
- Optional path segments allow navigation: `@1.field[3]`
- Used for structural cycles in RecursiveType values
- Matches depth counter mechanism in `equalFor`/`compareFor`

#### 2. Mutable Aliases: `$.path` (Absolute Keypaths)

**Syntax:**
```
alias_ref := '$' path_segment*

path_segment :=
  | '.' identifier          -- struct field or variant case
  | '.' '`' escaped_id '`'  -- quoted field name (backticks)
  | '[' integer ']'         -- array element by index
  | '[' integer ']'         -- set element by index (sorted order)
  | '[' value ']'           -- dict value by key
```

Where `value` is any East value literal matching the dict's key type.

**Semantics:**
- `$` refers to the **root of the current literal** being encoded/decoded
- Paths reference **backward** in depth-first traversal order (streaming constraint)
- Used when the same mutable collection (Array/Set/Dict) appears multiple times
- Preserves object identity for mutation semantics
- Type context is always known, eliminating ambiguity
- Backtick escaping follows existing East identifier rules

**Dict access uses keys**, not ordinal indices (unlike JSON format).

#### Reserved: `&value` for Future RefType

The `&` prefix is reserved for a future `RefType` feature (mutable reference cell):
```
&(x: 1, y: 2)     // Create RefType wrapper (enables sharing immutable values)
myref.*           // Dereference in keypaths
```

This will enable explicit sharing of arbitrary immutable values when needed.

### Path Segment Types

#### For Circular References (`@N`)

| Syntax | Example | Meaning |
|--------|---------|---------|
| `@0` | `@0` | Self-reference (current value) |
| `@N` | `@2` | Value N levels up (e.g., grandparent) |
| `@N.field` | `@1.next` | Navigate from ancestor |
| `@N[index]` | `@2[0]` | Index into ancestor |

#### For Mutable Aliases (`$.path`)

| Segment | Context | Example | Meaning |
|---------|---------|---------|---------|
| `.field` | Struct | `$.user.name` | Access struct field `name` in struct field `user` |
| `` .`field name` `` | Struct | `` $.`user info`.age `` | Access field with spaces/special chars |
| `.tag` | Variant | `$.result.success` | Access variant case `success` (the variant value itself) |
| `.tag.field` | Variant value | `$.result.ok.value` | Access field `value` within variant case `ok` |
| `[N]` | Array | `$.items[3]` | Access array element at index 3 |
| `[N]` | Set | `$.tags[0]` | Access set element at index 0 (sorted order) |
| `["key"]` | Dict (string key) | `$.map["status"]` | Access dict value with string key `"status"` |
| `[42]` | Dict (int key) | `$.counts[42]` | Access dict value with integer key `42` |
| `[(x: 1, y: 2)]` | Dict (struct key) | `$.coords[(x: 1, y: 2)]` | Access dict value with struct key |

**Dict key syntax:** Dict values are accessed by **key**, not ordinal index. The key must be a complete East value literal matching the dict's key type. Set elements use ordinal indices (sorted order).

### Examples

**Mutable aliasing (shared array):**
```
(
  data: [1, 2, 3],
  copy1: $.data,
  copy2: $.data
)
```
After decoding, `copy1` and `copy2` refer to the same mutable array instance as `data`.

**Circular linked list:**
```
(
  value: 1,
  next: (
    value: 2,
    next: @2
  )
)
```
The inner `next` field uses `@2` to reference 2 levels up (the root struct), creating a cycle.

**Self-reference:**
```
(
  value: 42,
  self: @0
)
```
The `self` field uses `@0` to reference the current struct itself.

**Shared array in RecursiveType:**
```
(
  shared: [1, 2, 3],
  ref1: $.shared,
  ref2: $.shared
)
```
Both `ref1` and `ref2` point to the same mutable array instance. After decoding, mutations to `ref1` will be visible through `ref2`.

**Note on graphs:** A graph with shared nodes (where multiple edges point to the same node struct) would require a `RefType` wrapper to create references to immutable structs. Without `RefType`, each node would be duplicated rather than shared.

**Variant traversal:**
```
(
  result: .ok (value: [1, 2, 3], code: 200),
  backup: $.result.value
)
```
The path `$.result.ok.value` traverses into variant case `ok` and accesses its `value` field.

**Complex field names:**
```
(
  `field/with/slashes`: 42,
  `field~with~tildes`: [1, 2],
  reference: $`field/with/slashes`,
  ref_array: $`field~with~tildes`
)
```
Backtick quoting works in paths the same as in struct definitions.

**Dict with shared value:**
```
(
  cache: {
    "key1": (data: [10, 20], meta: "info"),
    "key2": (data: $.cache["key1"].data, meta: "shared")
  }
)
```
Entry "key2" shares the array from entry "key1". The syntax `$.cache["key1"]` accesses the dict value by its string key.

### When References Are Created

The encoder automatically creates references in these scenarios:

**1. Circular references (using `@N`):**
```
(value: 1, next: @0)                    // Self-reference
(value: 1, next: (value: 2, next: @2))  // Parent reference
```

**2. Shared mutable collections (using `$.path`):**
```
(
  data: [1, 2, 3],
  ref: $.data                           // Same array instance appears twice
)
```

**What does NOT create references:**

Immutable values are always duplicated, even if identical:
```
(
  user1: (name: "Alice", age: 30),
  user2: (name: "Alice", age: 30)       // Duplicated, not referenced
)
```

Both `user1` and `user2` are separate struct instances. Structs are immutable, so object identity doesn't matter.

### Design Decisions

**1. Depth markers vs absolute paths:**

Two reference mechanisms serve different purposes:
- **`@N` (circular refs)**: Can reference any ancestor (structural cycles)
- **`$.path` (mutable aliases)**: Can only reference backward in depth-first order

For mutable aliases, references must point to values already serialized. This enables:
- Single-pass streaming encoding/decoding
- Simple implementation (no forward reference resolution)
- Consistent with JSON Pointer approach

Example of what's **not allowed** (forward mutable alias):
```
(
  ref: $.data,        // ERROR: $.data doesn't exist yet
  data: [1, 2, 3]
)
```

Correct version:
```
(
  data: [1, 2, 3],
  ref: $.data         // OK: $.data was serialized first
)
```

Circular refs using `@N` don't have this restriction - they reference ancestors by depth count.

**2. Root-relative paths only:**

The `$` always refers to the root of the **current top-level value** being encoded/decoded. Each value in a stream is independent with a fresh context.

For a `.east` file containing a single value with circular reference:
```
(value: 1, next: (value: 2, next: @2))
```
The `@2` refers 2 levels up to the root struct (creating a cycle).

For multiple values in a stream, each has its own `$`:
```
[1, 2, 3]    // Value 1: $ is this array
[4, 5, 6]    // Value 2: $ is this array (independent context)
```

Values cannot reference across stream boundaries. To share data between "values", wrap them in a container:
```
(
  value1: [1, 2, 3],
  value2: $.value1    // OK: both in same root struct
)
```

**3. Type context eliminates ambiguity:**

The decoder always knows the expected type at each position. This means:
- `[3]` is unambiguous (array index vs struct field "3" vs dict entry index)
- No special escaping needed to distinguish numeric field names from indices
- References are validated against the type structure

**4. Collision avoidance:**

Like JSON format, references cannot collide with user data because:
- `$` is a reserved token that starts reference syntax
- `$` is not valid as the start of any other East value syntax
- Arrays/Sets/Dicts use `[...]` or `{...}` syntax (never start with `$`)
- Structs use `(...)` syntax
- Variants use `.tag` syntax
- Primitives use literal syntax

### Encoding Algorithm

```typescript
type PathSegment =
  | { type: 'field', name: string }           // struct field or variant case
  | { type: 'index', index: number }          // array/set element
  | { type: 'dict_key', key: any };           // dict value by key

interface EastEncoderContext {
  // For mutable aliases ($.path)
  refs: Map<any, PathSegment[]>;  // object -> path segments from root
  currentPath: PathSegment[];     // Current position in structure

  // For circular refs (@N)
  depthStack: any[];              // Stack of values in current nesting path
}

function printValue(value: any, type: EastType, ctx?: EastEncoderContext): string {
  if (!ctx) {
    // No context - plain serialization
    return serializeValue(value, type);
  }

  // Check for circular reference (ancestor in depth stack)
  const depthIndex = ctx.depthStack.indexOf(value);
  if (depthIndex !== -1) {
    const depth = ctx.depthStack.length - depthIndex - 1;
    return '@' + depth;  // Circular ref: @0, @1, @2, etc.
  }

  // Check for mutable alias (previously serialized mutable collection)
  if (isAliasable(type, value) && ctx.refs.has(value)) {
    const path = ctx.refs.get(value)!;
    return buildPathString(path);  // e.g., "$.field["key"].name"
  }

  // First encounter of aliasable value - record it
  if (isAliasable(type, value)) {
    ctx.refs.set(value, [...ctx.currentPath]);
  }

  // Add to depth stack before descending
  ctx.depthStack.push(value);
  const result = serializeValue(value, type, ctx);
  ctx.depthStack.pop();

  return result;
}

function buildPathString(segments: PathSegment[]): string {
  let result = '$';
  for (const segment of segments) {
    if (segment.type === 'index') {
      result += '[' + segment.index + ']';
    } else if (segment.type === 'dict_key') {
      result += '[' + printValue(segment.key) + ']';
    } else if (needsBacktickQuoting(segment.name)) {
      result += '.' + '`' + escapeBackticks(segment.name) + '`';
    } else {
      result += '.' + segment.name;
    }
  }
  return result;
}
```

**Key insights:**
- **Depth stack** tracks current nesting path for `@N` circular refs
- **Refs map** tracks already-serialized mutable collections for `$.path` aliases
- Circular refs checked first (immediate ancestors)
- Mutable aliases checked second (previously serialized values)

### Decoding Algorithm

```typescript
interface EastDecoderContext {
  // For mutable aliases ($.path)
  refs: Map<string, any>;       // path key -> deserialized object
  currentPath: PathSegment[];   // Current position during traversal

  // For circular refs (@N)
  depthStack: any[];            // Stack of values being deserialized
}

function parseValue(input: string, type: EastType, ctx?: EastDecoderContext): any {
  if (!ctx) {
    // No context - plain parsing
    return deserializeValue(input, type);
  }

  // Check for circular reference (@N)
  if (input.trimStart().startsWith('@')) {
    const depth = parseDepth(input);  // "@2" → 2
    if (depth >= ctx.depthStack.length) {
      throw new Error(`Invalid depth @${depth} (only ${ctx.depthStack.length} levels deep)`);
    }
    const targetIndex = ctx.depthStack.length - depth - 1;
    return ctx.depthStack[targetIndex];
  }

  // Check for mutable alias ($.path)
  if (input.trimStart().startsWith('$')) {
    const pathSegments = parsePath(input);  // "$.a.b["key"]" → segments
    const pathKey = pathKeyFromSegments(pathSegments);

    if (!ctx.refs.has(pathKey)) {
      throw new Error(`Undefined reference: ${input}`);
    }
    return ctx.refs.get(pathKey);
  }

  // Create placeholder for aliasable values (for backward mutable refs)
  if (isAliasable(type)) {
    const pathKey = pathKeyFromSegments(ctx.currentPath);
    const obj = createPlaceholder(type);
    ctx.refs.set(pathKey, obj);

    // Add to depth stack before descending
    ctx.depthStack.push(obj);
    populateObject(obj, input, type, ctx);
    ctx.depthStack.pop();

    return obj;
  }

  // Regular value - add to depth stack during deserialization
  ctx.depthStack.push(null);  // Placeholder for non-aliasable
  const result = deserializeValue(input, type, ctx);
  ctx.depthStack.pop();

  return result;
}

function parseDepth(ref: string): number {
  // Parse "@2" or "@0.field[3]" → extract depth number
}

function parsePath(ref: string): PathSegment[] {
  // Parse "$.field.`quoted`.tag["key"][(x: 1, y: 2)]" into PathSegment array
}

function pathKeyFromSegments(segments: PathSegment[]): string {
  // Convert PathSegment[] to unique string key for refs map
}
```

**Key insights:**
- **Depth stack** enables `@N` resolution (index from end of stack)
- **Refs map** enables `$.path` resolution (already-deserialized mutable objects)
- Check `@N` first, then `$.path`, then deserialize normally
- Add objects to both depth stack and refs map before descending (enables circular refs)

### Edge Cases and Restrictions

**Self-reference:**
```
(self: @0)
```
Valid. `@0` refers to the current value itself (depth 0).

**Root reference (mutable alias):**
```
(self: $)
```
Valid for mutable alias. `$` with no segments refers to the root itself.

**Dict value paths:**

Dict values are accessed by their **key**, not ordinal position:
```
(
  mydict: {
    "zebra": [1, 2, 3],
    "apple": [4, 5, 6],
    "mango": [7, 8, 9]
  },
  ref: $.mydict["apple"]
)
```
The path `$.mydict["apple"]` references the array `[4, 5, 6]` associated with key `"apple"`.

**Compound dict keys:**
```
(
  coords: {
    (x: 0, y: 0): "origin",
    (x: 1, y: 0): "east",
    (x: 0, y: 1): "north"
  },
  ref: $.coords[(x: 0, y: 0)]
)
```
The path `$.coords[(x: 0, y: 0)]` references the value `"origin"` with struct key `(x: 0, y: 0)`.

**Dict keys:** Keys can use `@N` for circular references within the key itself (each key has its own depth context starting from depth 0 = the key). Keys cannot use `$.path` to reference values outside the key. Dict values can be referenced normally with `$.path`.

**Set element indexing:**

Sets are serialized in sorted order. Elements are accessed by ordinal index:
```
(
  myset: {"zebra", "apple", "mango"}
)
```
Sorted order: `["apple", "mango", "zebra"]`
- `$.myset[0]` refers to `"apple"` (first in sorted order)
- `$.myset[2]` refers to `"zebra"` (third in sorted order)

**Set elements are immutable and never referenced:** Only the set container itself can be referenced. Individual set elements are always immutable and inlined.

**Variant case paths:**

Variants use `.tag` syntax like field access. The variant case name is **always included** in the path:
```
.success (value: [1, 2, 3])
```
- `.success` accesses the variant case value (the entire struct)
- `.success.value` accesses the `value` field within the `success` case

**Type lookup:** Given a root `EastType` and a keypath like `$.result.ok.value`, you can deterministically compute the type of the referenced value by traversing the type structure. This is essential for type-safe keypath operations in future language features.

**Invalid references:**

These will throw parse errors:
- Forward mutable aliases: `$.notYetDefined` (hasn't been serialized yet)
- Undefined paths: `$.nonexistent`
- Type mismatches: `$.stringField[3]` when `stringField` is not indexable
- Malformed syntax: `$..field`, `$[]`, `$[3.14]`
- Invalid depth: `@5` when only 2 levels deep
- Negative depth: `@-1`

### Relationship to Future Language Features

This keypath syntax is designed to potentially become a first-class language feature:

```
// Hypothetical future East code:
const path = $.user.profile.name;        // keypath as value
const getter = (obj) => obj at path;     // keypath application
const lenses = map(keypaths, makeLens);  // higher-order keypath usage
```

Similar to Swift's keypaths or TypeScript's mapped types, this would enable powerful generic programming patterns while maintaining type safety.

### Summary: East vs JSON Reference Formats

**East text format:**
- **Two reference types:**
  - `@N` for circular references (depth markers)
  - `$.path` for mutable aliases (absolute keypaths)
- Dict access by **key**: `$.mydict["key"]` or `$.coords[(x: 1, y: 2)]`
- More expressive and user-friendly
- Direct semantic mapping
- Better for future keypath language features

**JSON format:**
- **Single reference type:** `{ "$ref": "#/path" }` (handles both circular and mutable)
- Dict access by **ordinal index**: `#/mydict/0/value`
- Constrained by JSON Pointer RFC 6901
- Path separator `/` makes embedding compound keys difficult
- Still deterministic (sorted key order)

Both formats preserve identical semantics. The difference is syntactic expressiveness and convenience.

## Binary Format (BEAST)

### Format Overview

Uses tag bytes to distinguish definitions from references:
- `[0]` - Definition tag (followed by object data)
- `[1]` - Reference tag (followed by varint backwards offset)

**Example:**
```
[0][array data...]    // Definition at byte offset 0
[1][varint: 10]       // Reference: go back 10 bytes
[1][varint: 10]       // Reference: go back 10 bytes (same array)
```

### Offset Encoding

References use **backwards relative offsets** (bytes to go back from current position):
- Encoded as varint for compactness
- Relative to the current byte position
- Points to the **start** of the target object's definition tag

### Context Management

```typescript
interface BinaryEncoderContext {
  refs: Map<any, number>;  // object -> byte offset from root
  position: number;        // Current byte position from root
}

function encodeBinary(value: any, type: EastType, ctx: BinaryEncoderContext): void {
  if (isAliasable(type)) {
    if (ctx.refs.has(value)) {
      // Write reference
      const targetOffset = ctx.refs.get(value);
      const relativeOffset = ctx.position - targetOffset;
      writeByte(1);  // Reference tag
      writeVarint(relativeOffset);
      return;
    }

    // Write definition
    writeByte(0);  // Definition tag
    ctx.refs.set(value, ctx.position);  // Record position of definition tag
    // ... write object data, updating ctx.position ...
  }

  // ... handle non-aliasable types ...
}
```

### Circular Reference Handling

**Key insight:** Add object to refs map **before** descending into its contents.

**Example:**
```typescript
const a = { next: null };
const b = { next: a };
a.next = b;  // Circular reference

// Encoding:
// Byte 0: [0] - definition tag for 'a'
// Record: refs.set(a, 0)
// ... encode 'a.next' which is 'b'
// Byte 10: [0] - definition tag for 'b'
// Record: refs.set(b, 10)
// ... encode 'b.next' which is 'a'
// 'a' is in refs at byte 0
// Byte 20: [1][varint(20 - 0)] = [1][20]
```

### Multi-Value Streaming

Each top-level call to `encodeBinary(value, type)` (sans context) creates a fresh context:
- `refs` map is empty
- `position` starts at 0
- Values in the stream are independent

This is like JSONL or Avro streams - each line/value stands alone.

**Example:**
```
// Stream of two values:
[Type data][Value1 data][Type data][Value2 data]
     ↑            ↑            ↑            ↑
  fresh ctx   fresh ctx   fresh ctx   fresh ctx
```

If you want values to reference each other, wrap them in a single container (Array/Struct).

## Implementation Strategy

All three formats will follow similar patterns to `equalFor` / `compareFor`:

1. **Type-level context**: Track recursion boundaries (like `RecursiveTypeContext`)
2. **Value-level context**: Track seen objects and their paths/offsets (like `RecursiveValueContext`)
3. **Entry point**: Top-level function creates fresh context and delegates to inner function
4. **Late binding**: Use closures to break circular dependencies
5. **Pre-registration**: Add aliasable objects to context **before** descending into contents

## Validation

To prevent `{ "$ref": "..." }` collisions, add to `RecursiveType` constructor:

```typescript
export function RecursiveType(builder: (self: EastType) => EastType): RecursiveType {
  // Create placeholder for self-reference
  const placeholder: EastType = { type: "Recursive", value: null! };
  const innerType = builder(placeholder);

  // Validate that innerType actually contains recursion
  if (!containsRecursionTo(innerType, placeholder)) {
    throw new Error(
      "RecursiveType builder must return a type that references the self parameter. " +
      "Non-recursive types should not use RecursiveType."
    );
  }

  placeholder.value = innerType;
  return placeholder as RecursiveType;
}

function containsRecursionTo(type: EastType, target: EastType): boolean {
  if (type === target) return true;

  switch (type.type) {
    case "Array": return containsRecursionTo(type.value, target);
    case "Set": return containsRecursionTo(type.value, target);
    case "Dict":
      return containsRecursionTo(type.value.key, target) ||
             containsRecursionTo(type.value.value, target);
    case "Struct":
      return Object.values(type.value).some(t => containsRecursionTo(t, target));
    case "Variant":
      return Object.values(type.value).some(t => containsRecursionTo(t, target));
    case "Recursive":
      return containsRecursionTo(type.value, target);
    default:
      return false;
  }
}
```
