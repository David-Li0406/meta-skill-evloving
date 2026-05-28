# Vector and Matrix Types Design

This document proposes adding `VectorType` and `MatrixType` to East as first-class numeric array types optimized for data science workloads.

## Motivation

### The Problem

East programs that combine general-purpose code with data science operations suffer from significant overhead when converting between East's `ArrayType` (backed by lists) and NumPy arrays required by ML libraries.

A typical data science East program:

```typescript
const mpf_train_samples = $.let(mpf_samples.filter(($, s) => train_batch_set.has(s.batch_id)));
const X_mpf_train = $.let(build_mpf_feature_matrix(mpf_train_samples));  // Returns ArrayType(ArrayType(FloatType))
const model = $.let(MAPIE.trainConformalClassifier(X_mpf_train, y_mpf_train, ...));  // Needs NumPy!
const pred_result = $.let(MAPIE.predictSet(model, X_mpf_test));  // Needs NumPy again!
```

The flow is:
1. **Structured data** (`ArrayType(StructType({...}))`) - needs East operations (filter, map, toDict)
2. **Numeric matrices** (`ArrayType(ArrayType(FloatType))`) - needs NumPy for ML
3. **Results back** as East arrays - more conversions

Every ML function call requires O(n) conversion:
```python
# Current conversion in east-py-datascience
def east_matrix_to_numpy(arr: EastArray) -> np.ndarray:
    return np.array([[float(x) for x in row] for row in arr], dtype=np.float32)
```

### The Solution

Add dedicated `VectorType` and `MatrixType` that are:
- Backed by contiguous numeric buffers (TypedArray in JS, NumPy in Python)
- Statically typed for rank (Vector = 1D, Matrix = 2D)
- Zero-copy passable to ML platform functions
- Interoperable with existing East operations

## Design Goals

1. **Zero-copy ML interop** - Pass to NumPy/sklearn without conversion
2. **Compile-time rank checking** - Vector vs Matrix distinguished in type system
3. **Shared storage** - Both use same underlying buffer format
4. **Minimal builtins** - Basic operations only; advanced math via platform functions
5. **Practical scope** - Float and Integer element types (covers 99% of ML use cases)

## Type Definitions

### VectorType

```typescript
export type VectorType<T = any> = { type: "Vector", element: T };

export function VectorType<const T extends FloatType | IntegerType | BooleanType>(element: T): VectorType<T> {
  if (element.type !== "Float" && element.type !== "Integer" && element.type !== "Boolean") {
    throw new Error(`Vector element type must be Float, Integer, or Boolean, got ${printType(element)}`);
  }
  return { type: "Vector", element };
}
```

### MatrixType

```typescript
export type MatrixType<T = any> = { type: "Matrix", element: T };

export function MatrixType<const T extends FloatType | IntegerType | BooleanType>(element: T): MatrixType<T> {
  if (element.type !== "Float" && element.type !== "Integer" && element.type !== "Boolean") {
    throw new Error(`Matrix element type must be Float, Integer, or Boolean, got ${printType(element)}`);
  }
  return { type: "Matrix", element };
}
```

### Element Type Constraints

Supported element types:

| Element Type | JS Runtime | Python Runtime |
|--------------|------------|----------------|
| `FloatType` | `Float64Array` | `np.ndarray` (float64) |
| `IntegerType` | `BigInt64Array` | `np.ndarray` (int64) |
| `BooleanType` | `Uint8Array` | `np.ndarray` (bool) |

Rationale:
- Float: features, predictions, probabilities
- Integer: labels, indices, counts
- Boolean: masks, prediction sets (common in conformal prediction)

### Type System Integration

```typescript
// Updated EastType union
export type EastType =
  | NeverType
  | NullType
  | BooleanType
  | IntegerType
  | FloatType
  | DateTimeType
  | StringType
  | BlobType
  | RefType
  | ArrayType
  | SetType
  | DictType
  | StructType
  | VariantType
  | RecursiveType
  | FunctionType
  | AsyncFunctionType
  | VectorType   // NEW
  | MatrixType;  // NEW

// Vectors and Matrices are MUTABLE (like Array)
// They cannot be Set keys or Dict keys
export type ImmutableType = /* unchanged - excludes Vector/Matrix */
```

## Internal Representation

### Shared Storage Model

Both Vector and Matrix use a contiguous buffer with shape metadata:

```typescript
// TypeScript runtime
interface VectorValue {
  data: Float64Array | BigInt64Array;
  length: number;
}

interface MatrixValue {
  data: Float64Array | BigInt64Array;  // Row-major order
  rows: number;
  cols: number;
}
```

```python
# Python runtime
class EastVector:
    data: np.ndarray  # 1D array

class EastMatrix:
    data: np.ndarray  # 2D array, row-major (C order)
```

### Memory Layout

Matrix uses **row-major** (C-style) layout:
```
Matrix [[a, b, c],      Storage: [a, b, c, d, e, f]
        [d, e, f]]      Index: data[row * cols + col]
```

This matches NumPy's default and allows zero-copy interop.

### Reshape: Vector ↔ Matrix

Since both share the same underlying buffer format, reshape is O(1):

```typescript
// Vector to Matrix (just add shape)
vector_to_matrix(v: Vector<Float>, rows: int, cols: int): Matrix<Float>
// Requires: rows * cols == vector_length(v)

// Matrix to Vector (flatten)
matrix_to_vector(m: Matrix<Float>): Vector<Float>
// Result length: rows * cols
```

## Builtins

### Vector Builtins

| Builtin | Signature | Description |
|---------|-----------|-------------|
| `VectorLength` | `Vector<T> → Integer` | Number of elements |
| `VectorGet` | `Vector<T>, Integer → T` | Get element at index |
| `VectorSet` | `Vector<T>, Integer, T → Null` | Set element at index (mutates) |
| `VectorSlice` | `Vector<T>, Integer, Integer → Vector<T>` | Slice [start, end) - returns copy |
| `VectorConcat` | `Vector<T>, Vector<T> → Vector<T>` | Concatenate vectors |
| `VectorFromArray` | `Array<T> → Vector<T>` | Convert from Array (copies) |
| `VectorToArray` | `Vector<T> → Array<T>` | Convert to Array (copies) |
| `VectorToMatrix` | `Vector<T>, Integer, Integer → Matrix<T>` | Reshape to matrix |
| `VectorZeros` | `Integer → Vector<Float>` | Create zero-filled vector |
| `VectorOnes` | `Integer → Vector<Float>` | Create one-filled vector |
| `VectorFill` | `Integer, T → Vector<T>` | Create vector filled with value |

### Matrix Builtins

| Builtin | Signature | Description |
|---------|-----------|-------------|
| `MatrixRows` | `Matrix<T> → Integer` | Number of rows |
| `MatrixCols` | `Matrix<T> → Integer` | Number of columns |
| `MatrixGet` | `Matrix<T>, Integer, Integer → T` | Get element at (row, col) |
| `MatrixSet` | `Matrix<T>, Integer, Integer, T → Null` | Set element (mutates) |
| `MatrixGetRow` | `Matrix<T>, Integer → Vector<T>` | Get row as vector (copy) |
| `MatrixGetCol` | `Matrix<T>, Integer → Vector<T>` | Get column as vector (copy) |
| `MatrixToVector` | `Matrix<T> → Vector<T>` | Flatten to vector (row-major) |
| `MatrixFromArray` | `Array<Array<T>> → Matrix<T>` | Convert from nested Array |
| `MatrixToArray` | `Matrix<T> → Array<Array<T>>` | Convert to nested Array |
| `MatrixTranspose` | `Matrix<T> → Matrix<T>` | Transpose (returns copy) |
| `MatrixZeros` | `Integer, Integer → Matrix<Float>` | Create zero-filled matrix |
| `MatrixOnes` | `Integer, Integer → Matrix<Float>` | Create one-filled matrix |
| `MatrixFill` | `Integer, Integer, T → Matrix<T>` | Create matrix filled with value |

### Iteration Builtins (Optional)

For compatibility with East's functional patterns:

| Builtin | Signature | Description |
|---------|-----------|-------------|
| `VectorMap` | `Vector<T>, (T, Integer) → U → Vector<U>` | Map over elements |
| `VectorFold` | `Vector<T>, U, (U, T, Integer) → U → U` | Fold/reduce |
| `MatrixMapElements` | `Matrix<T>, (T, Integer, Integer) → U → Matrix<U>` | Map over all elements |
| `MatrixMapRows` | `Matrix<T>, (Vector<T>, Integer) → Vector<U> → Matrix<U>` | Map over rows |

**Note:** These return new vectors/matrices (immutable semantics for map operations).

## Expression API

### VectorExpr (instance methods)

```typescript
class VectorExpr<T extends FloatType | IntegerType | BooleanType> extends Expr<VectorType<T>> {
  // Properties
  length(): IntegerExpr;

  // Element access
  get(index: IntegerExpr): ExprType<T>;
  set(index: IntegerExpr, value: ExprType<T>): NullExpr;  // Mutates

  // Slicing
  slice(start: IntegerExpr, end: IntegerExpr): VectorExpr<T>;

  // Conversion
  toArray(): ArrayExpr<T>;
  toMatrix(rows: IntegerExpr, cols: IntegerExpr): MatrixExpr<T>;

  // Higher-order (optional)
  map<U>(fn: (elem: ExprType<T>, idx: IntegerExpr) => ExprType<U>): VectorExpr<U>;
  fold<U>(initial: ExprType<U>, fn: (acc: ExprType<U>, elem: ExprType<T>, idx: IntegerExpr) => ExprType<U>): ExprType<U>;
}
```

### MatrixExpr (instance methods)

```typescript
class MatrixExpr<T extends FloatType | IntegerType | BooleanType> extends Expr<MatrixType<T>> {
  // Properties
  rows(): IntegerExpr;
  cols(): IntegerExpr;

  // Element access
  get(row: IntegerExpr, col: IntegerExpr): ExprType<T>;
  set(row: IntegerExpr, col: IntegerExpr, value: ExprType<T>): NullExpr;  // Mutates

  // Row/column access (returns copies)
  getRow(row: IntegerExpr): VectorExpr<T>;
  getCol(col: IntegerExpr): VectorExpr<T>;

  // Transformation
  transpose(): MatrixExpr<T>;

  // Conversion
  toVector(): VectorExpr<T>;  // Flatten row-major
  toArray(): ArrayExpr<ArrayType<T>>;
}
```

### Standard Library Functions

Located in `/src/expr/libs/vector.ts` and `/src/expr/libs/matrix.ts`.

#### East.Vector

```typescript
// /src/expr/libs/vector.ts
export default {
  /** Create a zero-filled float vector */
  zeros(length: IntegerExpr | bigint): VectorExpr<FloatType>;

  /** Create a one-filled float vector */
  ones(length: IntegerExpr | bigint): VectorExpr<FloatType>;

  /** Create a vector filled with a value */
  fill<T>(length: IntegerExpr | bigint, value: ExprType<T>): VectorExpr<T>;

  /** Convert an array to a vector */
  fromArray<T>(arr: ArrayExpr<T>): VectorExpr<T>;

  /** Generate a vector programmatically */
  generate<T>(length: IntegerExpr | bigint, elementType: T,
              fn: (idx: IntegerExpr) => ExprType<T>): VectorExpr<T>;
}
```

#### East.Matrix

```typescript
// /src/expr/libs/matrix.ts
export default {
  /** Create a zero-filled float matrix */
  zeros(rows: IntegerExpr | bigint, cols: IntegerExpr | bigint): MatrixExpr<FloatType>;

  /** Create a one-filled float matrix */
  ones(rows: IntegerExpr | bigint, cols: IntegerExpr | bigint): MatrixExpr<FloatType>;

  /** Create a matrix filled with a value */
  fill<T>(rows: IntegerExpr | bigint, cols: IntegerExpr | bigint,
          value: ExprType<T>): MatrixExpr<T>;

  /** Convert a nested array to a matrix */
  fromArray<T>(arr: ArrayExpr<ArrayType<T>>): MatrixExpr<T>;

  /** Create a matrix from an array of row vectors */
  fromRows<T>(rows: ArrayExpr<VectorType<T>>): MatrixExpr<T>;

  /** Create an identity matrix */
  identity(size: IntegerExpr | bigint): MatrixExpr<FloatType>;

  /** Generate a matrix programmatically */
  generate<T>(rows: IntegerExpr | bigint, cols: IntegerExpr | bigint, elementType: T,
              fn: (row: IntegerExpr, col: IntegerExpr) => ExprType<T>): MatrixExpr<T>;
}
```

### Usage Examples

```typescript
// Building a feature matrix from structured data
const samples = $.let(allSamples.filter(($, s) => trainSet.has(s.id)));
const X_train = $.let(
  East.Matrix.fromArray(
    samples.map(($, s) => [s.feature1, s.feature2, s.feature3])
  )
);
const y_train = $.let(
  East.Vector.fromArray(samples.map(($, s) => s.label))
);

// Pass directly to ML (zero-copy in Python runtime)
const model = $.let(Sklearn.fit(X_train, y_train, config));
const predictions = $.let(Sklearn.predict(model, X_test));

// Access results
$.for(East.Array.range(0n, predictions.length()), ($, i) => {
  $(Console.log(East.str`Prediction ${i}: ${predictions.get(i)}`));
});

// Reshape operations
const flattened = $.let(X_train.toVector());
const reshaped = $.let(flattened.toMatrix(100n, 3n));

// Create vectors/matrices directly
const zeros = $.let(East.Vector.zeros(100n));
const identity = $.let(East.Matrix.identity(3n));
const custom = $.let(East.Matrix.generate(3n, 3n, FloatType, ($, i, j) =>
  i.equals(j).ifElse(() => 1.0, () => 0.0)
));
```

## Serialization

### EastTypeType Extension

```typescript
export const EastTypeType = RecursiveType(type => VariantType({
  // ... existing types ...
  "Vector": type,  // element type
  "Matrix": type,  // element type
}));
```

### JSON Serialization

Type context provides the element type, so values are just JSON arrays:

```json
// Vector<Float> with values [1.0, 2.0, 3.0]
[1.0, 2.0, 3.0]

// Matrix<Float> 2x3 - nested arrays (row-major)
[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
```

The deserializer knows from type context whether it's parsing a `VectorType` or `MatrixType`, so no wrapper is needed. Matrix shape is implicit from the nested array structure.

### BEAST/BEAST2 Serialization

Element type is known from the type context (like other parameterized types).

Format:
```
Vector: [length: varint] [data: length * sizeof(element)]
Matrix: [rows: varint] [cols: varint] [data: rows*cols * sizeof(element)]
```

Binary data is stored directly (no per-element encoding), making serialization/deserialization O(1) with memcpy.

**Note:** The type tag (Vector vs Matrix) and element type are encoded separately in the type representation, not in the value.

## IR Representation

### NewVectorIR

```typescript
export type NewVectorIR = variant<"NewVector", {
  type: EastTypeValue;      // VectorType
  location: LocationValue[];
  length: IR;               // Integer expression
  values?: IR[];            // Optional initial values
}>;
```

### NewMatrixIR

```typescript
export type NewMatrixIR = variant<"NewMatrix", {
  type: EastTypeValue;      // MatrixType
  location: LocationValue[];
  rows: IR;                 // Integer expression
  cols: IR;                 // Integer expression
  values?: IR[];            // Optional initial values (row-major)
}>;
```

## Implementation Plan

**Reference:** All implementations MUST comply with [STANDARDS.md](/STANDARDS.md).

### Phase 1: Core Type System (East)

1. **types.ts** - Add `VectorType` and `MatrixType` type definitions
2. **type_of_type.ts** - Add serialization for Vector/Matrix types
3. **comparison.ts** - Add equality/comparison for Vector/Matrix values
4. **ir.ts** - Add `NewVectorIR` and `NewMatrixIR` nodes

**Estimated: ~300 lines**

### Phase 2: Builtins (East)

1. **builtins.ts** - Add Vector and Matrix builtin definitions
2. **analyze.ts** - Add type checking for new builtins
3. **compile.ts** - Add code generation for new builtins

**Estimated: ~500 lines**

### Phase 3: Serialization (East)

1. **serialization/json.ts** - JSON encoding/decoding
2. **serialization/beast.ts** - Binary encoding (v1)
3. **serialization/beast2.ts** - Binary encoding (v2)
4. **serialization/east.ts** - Text format

**Estimated: ~600 lines**

### Phase 4: Expression API (East)

1. **expr/vector.ts** - New `VectorExpr` class with TypeDoc (see [TypeDoc Standards](#typedoc-requirements))
2. **expr/matrix.ts** - New `MatrixExpr` class with TypeDoc
3. **expr/libs/vector.ts** - Standard library functions
4. **expr/libs/matrix.ts** - Standard library functions
5. **expr/types.ts** - Update type mappings
6. **expr/index.ts** - Export new classes

**Estimated: ~800 lines**

### Phase 5: Documentation (East)

1. **USAGE.md** - Add Vector and Matrix sections following USAGE.md standards
2. **STDLIB.md** - Document `East.Vector` and `East.Matrix` functions

### Phase 6: Testing (East)

1. **test/vector.spec.ts** - Comprehensive vector tests
2. **test/matrix.spec.ts** - Comprehensive matrix tests

Test coverage requirements:
- Basic operations (get, set, length, rows, cols)
- Edge cases (empty vectors/matrices, single element)
- Error conditions (out of bounds access)
- Mutation operations
- Conversion operations (toArray, fromArray, toMatrix, toVector)
- Serialization round-trips (JSON, BEAST)

### Phase 7: Python Runtime (east-py)

1. **types/types.py** - Add VectorType, MatrixType
2. **types/values.py** - Add EastVector, EastMatrix classes (numpy-backed)
3. **builtins/vector.py** - Vector builtin implementations
4. **builtins/matrix.py** - Matrix builtin implementations
5. **serialization/json.py** - JSON support
6. **serialization/beast.py** - Binary support

**Estimated: ~1000 lines**

### Phase 8: Integration (east-py-datascience)

1. Update ML platform functions to accept Vector/Matrix directly
2. Remove conversion helpers (or deprecate)
3. Update type annotations

**Estimated: ~200 lines**

## TypeDoc Requirements

Per [STANDARDS.md](/STANDARDS.md), all expression classes and methods MUST include TypeDoc with `@example` blocks using the `East.function()` → `East.compile()` → execution pattern.

**Example for VectorExpr.get():**

```typescript
/**
 * Gets the element at the specified index.
 *
 * @param index - The zero-based index to access
 * @returns An expression of the element type
 *
 * @throws East runtime error if the index is out of bounds
 *
 * @example
 * ```ts
 * const getElement = East.function([VectorType(FloatType), IntegerType], FloatType, ($, vec, idx) => {
 *   $.return(vec.get(idx));
 * });
 * const compiled = East.compile(getElement.toIR(), []);
 * const v = new Float64Array([1.0, 2.0, 3.0]);
 * compiled(v, 0n);  // 1.0
 * compiled(v, 2n);  // 3.0
 * // compiled(v, 5n) would throw error (out of bounds)
 * ```
 */
get(index: IntegerExpr | bigint): ExprType<T> { ... }
```

**Example for East.Vector.zeros():**

```typescript
/**
 * Creates a zero-filled float vector of the specified length.
 *
 * @param length - The number of elements in the vector
 * @returns A VectorExpr containing all zeros
 *
 * @example
 * ```ts
 * const makeZeros = East.function([IntegerType], VectorType(FloatType), ($, n) => {
 *   $.return(East.Vector.zeros(n));
 * });
 * const compiled = East.compile(makeZeros.toIR(), []);
 * compiled(5n);  // Float64Array([0.0, 0.0, 0.0, 0.0, 0.0])
 * ```
 */
zeros(length: IntegerExpr | bigint): VectorExpr<FloatType> { ... }
```

## Testing Requirements

Per [STANDARDS.md](/STANDARDS.md), tests use the self-hosted test platform.

**Example test file structure:**

```typescript
// test/vector.spec.ts
import {
  East,
  VectorType, MatrixType, FloatType, IntegerType, BooleanType,
} from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

describe("Vector", (test) => {
    test("Vector creation and access", $ => {
        const v = $.let(East.Vector.zeros(3n));
        $(assert.equal(v.length(), 3n));
        $(assert.equal(v.get(0n), 0.0));

        $(v.set(1n, 42.0));
        $(assert.equal(v.get(1n), 42.0));
    });

    test("Vector from array", $ => {
        const arr = $.let([1.0, 2.0, 3.0]);
        const v = $.let(East.Vector.fromArray(arr));
        $(assert.equal(v.length(), 3n));
        $(assert.equal(v.get(0n), 1.0));
    });

    test("Vector bounds checking", $ => {
        const v = $.let(East.Vector.zeros(3n));
        $(assert.throws(v.get(-1n)));
        $(assert.throws(v.get(3n)));
    });

    test("Vector to matrix reshape", $ => {
        const v = $.let(East.Vector.fromArray([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]));
        const m = $.let(v.toMatrix(2n, 3n));
        $(assert.equal(m.rows(), 2n));
        $(assert.equal(m.cols(), 3n));
        $(assert.equal(m.get(0n, 0n), 1.0));
        $(assert.equal(m.get(1n, 2n), 6.0));
    });
});

describe("Matrix", (test) => {
    test("Matrix creation and access", $ => {
        const m = $.let(East.Matrix.zeros(2n, 3n));
        $(assert.equal(m.rows(), 2n));
        $(assert.equal(m.cols(), 3n));
        $(assert.equal(m.get(0n, 0n), 0.0));
    });

    test("Matrix from nested array", $ => {
        const arr = $.let([[1.0, 2.0], [3.0, 4.0]]);
        const m = $.let(East.Matrix.fromArray(arr));
        $(assert.equal(m.rows(), 2n));
        $(assert.equal(m.cols(), 2n));
        $(assert.equal(m.get(1n, 0n), 3.0));
    });

    test("Matrix row/col access", $ => {
        const m = $.let(East.Matrix.fromArray([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]));
        const row = $.let(m.getRow(0n));
        $(assert.equal(row.length(), 3n));
        $(assert.equal(row.get(0n), 1.0));

        const col = $.let(m.getCol(1n));
        $(assert.equal(col.length(), 2n));
        $(assert.equal(col.get(0n), 2.0));
    });

    test("Matrix transpose", $ => {
        const m = $.let(East.Matrix.fromArray([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]));
        const t = $.let(m.transpose());
        $(assert.equal(t.rows(), 3n));
        $(assert.equal(t.cols(), 2n));
        $(assert.equal(t.get(0n, 1n), 4.0));
    });
});
```

## Comparison with Alternatives

| Approach | Type Safety | Performance | Complexity |
|----------|-------------|-------------|------------|
| **VectorType + MatrixType** | Compile-time rank | Zero-copy | Medium |
| TensorType(N, T) | Compile-time rank | Zero-copy | High (type-level integers) |
| TensorType(T) runtime shape | Runtime only | Zero-copy | Low |
| NumPy-backed EastArray | None | Zero-copy for floats | Medium (dual mode) |
| Optimized conversions | None | O(n) but faster | Low |

The VectorType + MatrixType approach provides the best balance of type safety and performance for data science workloads, which are dominated by 1D and 2D arrays.

## Design Decisions

1. **Boolean element support:** Yes - useful for masks (common in ML)

2. **Math operations as builtins:** No - keep math in platform functions; builtins are for structure only. Can revisit later if needed.

3. **`getRow`/`getCol` semantics:** Return copies, not views. Simpler and avoids shared mutation complexity. Views can be added later if performance requires.

4. **Element types:** Support both Float and Integer. Integer is essential for classification labels (`y_train`), indices, and counts.

5. **Naming convention:** Match Array pattern - use `VectorSet`, `MatrixSet` for mutation. Document that these mutate in place.

## Future Extensions

- **Tensor3Type** - If 3D+ tensors become needed (deep learning)
- **Sparse vectors/matrices** - For high-dimensional sparse data
- **GPU tensors** - For CUDA/WebGPU acceleration
- **SIMD operations** - For vectorized math in JS runtime

These can be added incrementally without breaking the Vector/Matrix design.

## Conclusion

Adding `VectorType` and `MatrixType` provides East with efficient, type-safe numeric array types optimized for data science workloads. The design:

- Eliminates O(n) conversion overhead at ML function boundaries
- Provides compile-time rank checking (1D vs 2D)
- Uses shared storage allowing O(1) reshape
- Keeps scope minimal (structure, not math)
- Integrates cleanly with existing East type system

This is a foundational addition that enables East to be a practical language for ML/data science applications.
