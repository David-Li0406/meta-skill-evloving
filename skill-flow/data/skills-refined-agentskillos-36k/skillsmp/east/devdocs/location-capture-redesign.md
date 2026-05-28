# Location Capture Redesign

## Problem Statement

When errors occur during East program execution (in east-py), the error messages show incorrect source locations - typically pointing to internal library code or Node.js ESM loader internals instead of the user's source file.

### Current Behavior

```
Error: node:internal/modules/esm/loader:665:26: list index out of range
```

### Desired Behavior

```
Error: list index out of range
  at file:///tmp/failtest/node_modules/@elaraai/east/dist/src/location.js:28:17
  at file:///tmp/failtest/node_modules/@elaraai/east/dist/src/expr/array.js:164:27
  at file:///tmp/failtest/dist/index.js:8:18
  at file:///tmp/failtest/node_modules/@elaraai/east/dist/src/expr/block.js:299:15
  at file:///tmp/failtest/dist/index.js:4:51
```

Show the full stack - both user code and library code. No filtering, no guessing.

## Root Cause Analysis

### 1. Fragile Skip-Count Based Location Capture

The current `get_location(skip)` function uses a fixed skip count:

```typescript
export function get_location(skip: number = 1): Location {
  const err = new Error();
  const lines = err.stack.split('\n').slice(skip + 1);
  // Returns first matching frame...
}
```

**Problems:**
- Skip count assumes fixed call depth, but this varies
- Call sites use `get_location(2)` (399 occurrences) or `get_location(3)` (10 occurrences)
- User code appears at varying frame indices (2, 3, 4, 5...) depending on call depth

### 2. Regex-Based Stack Parsing

The current regex doesn't handle all stack trace formats:

```typescript
const match = line.match(/at\s[<>a-zA-Z0-9_$]*\s+(?:(?:\w+\.)*\w+\s+)?\(?(.*?):(\d+):(\d+)\)?$/);
```

**Problems:**
- Doesn't match `at file:///path:line:col` format (no function name)
- Doesn't match `at Obj.method (path:line:col)` (dots in function name)

### 3. Single Location Storage

Each IR node stores only ONE location. This loses the full call stack context.

## Proposed Solution

### Capture Full Stack, No Filtering

Instead of trying to pick "the right" frame, capture and store the entire stack:

```typescript
function parseStackLine(line: string): Location | null {
  // Simple regex that matches file:line:col at end of line
  const match = line.match(/\(?([^()\s]+):(\d+):(\d+)\)?$/);
  if (match) {
    return {
      filename: match[1],
      line: BigInt(match[2]),
      column: BigInt(match[3]),
    };
  }
  return null;
}

export function get_location(): Location[] {
  const err = new Error();
  const stack = err.stack;
  if (!stack) return [];

  const lines = stack.split('\n').slice(1); // Skip "Error" line
  const frames: Location[] = [];

  for (const line of lines) {
    const parsed = parseStackLine(line);
    if (parsed) {
      frames.push(parsed);
    }
  }

  return frames;
}
```

**Benefits:**
- No skip parameter - removes fragile guessing
- No filtering - shows full context
- Simple regex that handles common formats
- Works in any JS runtime (not V8-specific)

### IR Type Changes

Keep `LocationType` as a single location struct. Change IR nodes to use an array:

```typescript
// LocationType stays the same - represents ONE location
export const LocationType = StructType({
  filename: StringType,
  line: IntegerType,
  column: IntegerType,
});

// In IRType, change from:
location: LocationType
// to:
location: ArrayType(LocationType)
```

**TypeScript types:**

```typescript
// LocationValue stays as single location
export type LocationValue = {
  filename: string,
  line: bigint,
  column: bigint,
};

// IR nodes change from:
location: LocationValue
// to:
location: LocationValue[]
```

### Python Changes

The Python `EastError` already supports multiple locations via `ir_stack`:

```python
class EastError(Exception):
    def __init__(self, message: str, location: dict[str, Any]):
        self.message = message
        self.location = location
        self.ir_stack: list[dict[str, Any]] = [location]
```

Change to read location array from IR directly instead of building `ir_stack` manually.

## Implementation Plan

### Step 1: Update `get_location()` in `src/location.ts`

1. Change return type from `Location` to `Location[]`
2. Remove `skip` parameter
3. Use simpler, more permissive regex
4. Return all parsed frames

### Step 2: Update IR Types in `src/ir.ts`

1. Change `LocationValue` usage in all IR node types to `LocationValue[]`
2. Change `location: LocationType` to `location: ArrayType(LocationType)` in `IRType`

### Step 3: Update Call Sites

Files: `src/expr/*.ts` (all ~409 call sites)

1. Change `get_location(2)` to `get_location()`
2. Change `get_location(3)` to `get_location()`
3. Update code that consumes the location to handle array

### Step 4: Update AST to IR Conversion

File: `src/ast_to_ir.ts`

Update any code that converts Location to LocationValue.

### Step 5: Update Python Runtime

File: `east-py/packages/east-py/east/runtime/compiler.py`

1. Read location as array from IR
2. Update error formatting to display stack

### Step 6: Update `printLocationValue()`

Change to format array of locations as stack trace.

## Testing Strategy

1. Create e3 package with intentional error (e.g., array index out of bounds)
2. Run via east-py
3. Verify error shows full stack trace with both user and library frames

## Breaking Changes

This is a breaking change:
- IR schema change (location becomes array)
- Python runtime update required
- Any code consuming IR location field needs update

Requires major version bump and CHANGELOG documentation.
