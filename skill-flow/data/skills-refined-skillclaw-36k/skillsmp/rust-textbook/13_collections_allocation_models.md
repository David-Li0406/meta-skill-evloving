# 13 — Collections and Allocation Models (Address Stability and Size Discipline)

[INVARIANT: INV-1301] Moving Storage Invalidates References.
- `Vec`/`String` reallocation moves elements/bytes.
- REJECT IF: APIs return references into moving storage while also permitting mutation that can reallocate without lifetime coupling that forbids the mutation.
- ENFORCE BY: borrow tying (`&self` vs `&mut self`); indices/handles; chunked arenas; slabs with stable handles.
[PROVENANCE] std docs: `Vec` and `String` capacity growth implies reallocation and movement.

[HAZARD: RSK-1301] Use-After-Realloc via Stale Pointers/References.
- TRIGGER: storing raw pointers into `Vec`/`String` buffers across pushes/reserves; returning slices and later mutating the backing buffer.
- FAILURE MODE: stale pointer dereference (UB if unsafe); logic corruption in safe code.
- REJECT IF: any pointer/reference escapes without a proof it cannot be invalidated.
- ENFORCE BY: avoid raw pointers into moving buffers; make reallocation impossible for the borrow lifetime; use `Pin` only with explicit invariants.
[PROVENANCE] Rust Abstract Machine reference validity (INV-0004); std docs for `Vec`/`String`.
[VERIFICATION] Miri for unsafe pointer dereference; tests that force reallocation paths.

[CONTRACT: CTR-1301] Identity Strategy Must Match Invariants.
- Stable address required: use non-moving storage or indirection.
- Stable identity required: use handles; add generation counters when reuse is possible.
- Bulk free/reset required: bump arenas with explicit lifetime boundary.
- REJECT IF: identity assumptions are implicit (pointer address equality, index reuse without generation).
[PROVENANCE] Stable identity is not implied by Rust collections; it is a design contract.

[CONTRACT: CTR-1302] Query Result Limiting (Memory DoS Prevention).
- Apply limits BEFORE collecting iterators to prevent memory exhaustion from query results.
- REJECT IF: `.collect()` precedes `.take(limit)` in query paths.
- ENFORCE BY: `.take(limit).collect()`.
[PROVENANCE] APM2 Implementation Standard; RSK-1901 (Resource Exhaustion).
[VERIFICATION] Query with limit=N on M>>N items, verify O(limit) memory.

[HAZARD: RSK-1302] Size Math and Allocation Are Attacker-Controlled at Boundaries.
- TRIGGER: parsing lengths from inputs; `len * size_of::<T>()` computations; `reserve`/`with_capacity` from untrusted sizes.
- FAILURE MODE: integer overflow; oversized allocation; quadratic behavior due to repeated growth.
- REJECT IF: size computations are unchecked in boundary code.
- ENFORCE BY: `checked_*` arithmetic; explicit caps; amortization control (`reserve_exact` policy) where required.
[PROVENANCE] Rust Reference: overflow behavior differs by build; correctness requires explicit checked math where overflow is a risk.
[VERIFICATION] Property tests for size boundaries; fuzzers for parsers; overflow-focused tests.

[HAZARD: RSK-1303] Hash Iteration Order Is Nondeterministic.
- FAILURE MODE: flaky tests; unstable serialization/spec drift.
- REJECT IF: tests/specs rely on hash iteration order.
- ENFORCE BY: sort keys; use ordered maps/sets for deterministic output; define ordering in the format contract.
[PROVENANCE] std docs: hash maps do not guarantee iteration order.
[VERIFICATION] Deterministic snapshot tests that sort before asserting.

[HAZARD: RSK-1304] Ghost Key Prevention in TTL Queues.
- When using insertion-order queues (VecDeque) with TTL-based eviction, keys can be reused after expiration.
- REJECT IF: queue stores only keys without timestamps for TTL-based stores.
- ENFORCE BY: store timestamps alongside keys in the queue to detect and skip stale "ghost" entries.
[PROVENANCE] APM2 Implementation Standard.
[VERIFICATION] Test ghost key eviction: reuse key after TTL, verify new entry survives eviction.

[CONTRACT: CTR-1303] Bounded In-Memory Stores (Memory DoS Prevention).
- REJECT IF: in-memory collections (HashMaps, Vecs) tracking external events lack a hard upper bound.
- ENFORCE BY:
  - use a `max_entries` limit.
  - O(1) eviction: use `VecDeque` alongside `HashMap` to track insertion order for fast eviction.
[PROVENANCE] APM2 Implementation Standard; CTR-MEM001.

```rust
// Pattern: Bounded Store with O(1) Eviction
impl<K: Hash + Eq + Clone, V> BoundedStore<K, V> {
    pub fn insert(&mut self, key: K, value: V) {
        while self.entries.len() >= self.max_entries {
            if let Some(old_key) = self.insertion_order.pop_front() {
                self.entries.remove(&old_key);
            }
        }
        self.entries.insert(key.clone(), value);
        self.insertion_order.push_back(key);
    }
}
```

## References (Normative Anchors)

- std `Vec`: https://doc.rust-lang.org/std/vec/struct.Vec.html
- std `String`: https://doc.rust-lang.org/std/string/struct.String.html
- Rust Reference: Behavior considered undefined (invalid dereference): https://doc.rust-lang.org/reference/behavior-considered-undefined.html
