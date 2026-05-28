---
name: fastedgesgeometry-architecture
description: Architecture and implementation details of FastEdgesGeometry. Use when modifying FastEdgesGeometry, understanding its optimization techniques, or debugging edge generation issues.
---

# FastEdgesGeometry Architecture

## Background

FastEdgesGeometry is a performance-optimized fork of Three.js EdgesGeometry. The original EdgesGeometry had performance issues with complex geometries, leading to the creation of this optimized version.

File: `src/FastEdgesGeometry.ts`

## Evolution History

### Stage 1: Three.js EdgesGeometry (Original)

Standard Three.js EdgesGeometry implementation:

| Aspect | Implementation |
|--------|----------------|
| Edge hash | String concatenation: `"x,y,z"` format (4 decimal precision) |
| Edge storage | `Object` with string keys: `"hash0_hash1"` |
| Normal calculation | `Triangle.getNormal()` method |
| Vertex accumulation | `Array.push()` |

**Problem**: String hash generation and object key lookup are slow

### Stage 2: FastEdgesGeometry (v0.7.3, 2024-11)

Replaced string hash with numeric hash:

| Aspect | Implementation |
|--------|----------------|
| Edge hash | Numeric hash via `hybridtaus()` (Tausworthe algorithm) |
| Edge storage | `Map<number, {index0, index1, normal}>` |
| Normal calculation | `Triangle.getNormal()` method (unchanged) |
| Vertex accumulation | `Array.push()` (unchanged) |

**Improvement**: Numeric hash speeds up edge lookup (~3-4x faster)
**Remaining issues**: Function call overhead, object allocation, dynamic arrays

### Stage 3: FastEdgesGeometry (v0.7.4+, 2026-01)

Applied further optimizations:

| Aspect | Implementation |
|--------|----------------|
| Edge hash | Inline `computeHash()` with pre-transformed seed |
| Edge storage | Parallel Typed Arrays (`Uint32Array`, `Float32Array`) |
| Normal calculation | Direct cross product calculation |
| Vertex accumulation | Pre-allocated `Float32Array` with index tracking |

**Improvement**: Function inlining, Typed Arrays, object allocation avoidance (~30% faster)

## Optimization Mapping

### Stage 2 → Stage 3 Optimization Details

| Stage 2 (v0.7.3) | Stage 3 (v0.7.4+) | Rationale |
|----------------|-------------------|-----------|
| `Triangle` class with `getNormal()` | Direct cross product calculation | Avoid method call overhead and object property access |
| `Map<hash, {index0, index1, normal}>` | Parallel Typed Arrays (`Uint32Array`, `Float32Array`) | Reduce object allocation and GC pressure |
| `vertices.push()` dynamic array | Pre-allocated `Float32Array` with final `slice()` | Avoid array resize operations |
| `hybridtaus()` function calls | Inline hash computation | Eliminate function call stack overhead |
| `options?.seed` access in loop | Pre-transformed seed constant | Avoid repeated optional chaining |
| `Triangle` object for vertex access | Direct `Vector3` variables (`_a`, `_b`, `_c`) | Eliminate object property lookup |

### Code Structure Mapping

| Operation | Three.js EdgesGeometry | FastEdges (v0.7.3) | FastEdges (v0.7.4+) |
|-----------|------------------------|--------------------|--------------------|
| Hash generation | `"x,y,z"` string | `hybridtaus(x,y,z)` | `computeHash(x,y,z)` inline |
| Normal calculation | `triangle.getNormal(normal)` | `triangle.getNormal(normal)` | direct cross product |
| Edge storage | `edgeData["hash"] = obj` | `edgeData.set(hash, obj)` | `typed arrays[slot]` |
| Vertex accumulation | `vertices.push(...)` | `vertices.push(...)` | `vertexBuffer[writeIndex++]` |

### Inline Hash Function

The `computeHash()` function (lines 94-100) is an inline expansion of `hybridtaus()`:

```typescript
// hybridtaus() static method (preserved for public API):
static hybridtaus(x, y, z, seed = 255) {
  x = FastEdgesGeometry.taus(x, 13, 19, 12, 0xfffffffe);
  y = FastEdgesGeometry.taus(y, 2, 25, 4, 0xfffffff8);
  z = FastEdgesGeometry.taus(z, 3, 11, 17, 0xfffffff0);
  seed = u32(seed * 1664525 + 1013904223);
  return u32(x ^ y ^ z ^ seed);
}

// Inlined as computeHash() with pre-transformed seed:
const transformedSeed = (seed * 1664525 + 1013904223) >>> 0;
const computeHash = (x, y, z) => {
  x = (((x & 0xfffffffe) << 13) ^ (((x << 19) ^ x) >>> 12)) >>> 0;
  y = (((y & 0xfffffff8) << 2) ^ (((y << 25) ^ y) >>> 4)) >>> 0;
  z = (((z & 0xfffffff0) << 3) ^ (((z << 11) ^ z) >>> 17)) >>> 0;
  return (x ^ y ^ z ^ transformedSeed) >>> 0;
};
```

The magic numbers (`0xfffffffe`, `0xfffffff8`, `0xfffffff0`) and bit shifts come from the Tausworthe random number generator algorithm (GPU Gems 3, Chapter 37).

## Performance Results

Benchmark comparison (Chrome, macOS):

| Geometry | Triangles | EdgesGeometry | FastEdges (old) | FastEdges (new) | Speedup |
|----------|-----------|---------------|-----------------|-----------------|---------|
| SphereGeometry(32,32) | 1,984 | 4.40ms | 1.20ms | 0.90ms | 4.9x vs original |
| TorusKnot(200,32) | 12,800 | 28.40ms | 6.50ms | 5.00ms | 5.7x vs original |
| TorusKnot(400,64) | 51,200 | 134.40ms | 28.70ms | 21.80ms | 6.2x vs original |

## Optimization Principles Applied

1. **Inline function calls** - Eliminate call stack overhead in hot loops
2. **Pre-allocate fixed arrays** - Replace dynamic `push()` with typed array indexing
3. **Avoid high-level abstractions** - Use primitives instead of objects/classes
4. **Pre-compute constants** - Move invariant calculations outside loops

## Trade-offs

- **Readability**: Code is more complex and harder to understand
- **Maintainability**: Changes require understanding the optimization mapping
- **Justification**: Edge geometry generation directly impacts user experience (frame drops during scene initialization)

## Future Optimization Considerations

If further optimization is needed:
- WebGPU Compute Shader (parallel processing on GPU)
- Web Workers (limited benefit due to data transfer overhead)
- Only practical for geometries with 100k+ triangles
