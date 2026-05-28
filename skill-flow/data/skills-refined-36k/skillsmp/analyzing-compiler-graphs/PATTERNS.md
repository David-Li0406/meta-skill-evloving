# Problem Patterns and Fixes

Common patterns found in compiler graphs and how to fix them.

## Problem 1: Indirect Calls (Critical!)

### Detection

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | contains("IndirectCall"))'
```

**Bad output**: `OptimizedIndirectCallNode` found

### Root Cause

No caching of CallTarget - dynamic lookup every time.

### Fix (Language Implementation)

```java
// ❌ BAD: Dynamic lookup every time
public Object execute(VirtualFrame frame) {
    CallTarget target = lookupFunction(name);
    return target.call(args);
}

// ✅ GOOD: Cache with @Cached
@Specialization(guards = "function == cachedFunction")
public Object executeCached(VirtualFrame frame,
        @Cached("function") Function cachedFunction,
        @Cached("cachedFunction.getCallTarget()") CallTarget callTarget) {
    return callTarget.call(args);
}
```

### Verification

Re-dump and check for `OptimizedDirectCallNode`.

---

## Problem 2: Failed Escape Analysis

### Detection

```bash
cat graphs.json | jq 'select(.name | contains("After PartialEscape")) |
  .nodes[] | select(.props.label | test("Alloc|New"))'
```

**Bad output**: `CommitAllocationNode` or `NewInstanceNode` found after PartialEscape

### Root Cause

Object escapes the compilation unit:
- Object stored in field visible to other threads
- Object passed to method that doesn't inline
- Object stored in escaping data structure
- Identity operations (synchronization, ==)

### Fix (Guest Language)

```lox
// ❌ BAD: Object escapes
var temp = Point(x, y);
this.lastPoint = temp;  // Escapes!

// ✅ GOOD: Object stays local
fun calculate(x, y) {
    var temp = Point(x, y);  // Local only
    var result = temp.distance();
    return result;  // Only result escapes
}
```

### Verification

After PartialEscape phase should show zero allocation nodes.

---

## Problem 3: Boxing/Unboxing

### Detection

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | test("Box|Unbox"))'
```

**Bad output**: `BoxNode` and `UnboxNode` found

### Root Cause

Missing primitive specializations.

### Fix (Language Implementation)

```java
// ❌ BAD: Generic Object parameters
@Specialization
Object add(Object left, Object right) { ... }

// ✅ GOOD: Primitive specializations
@Specialization
int add(int left, int right) { return left + right; }

@Specialization
long add(long left, long right) { return left + right; }

@Specialization
double add(double left, double right) { return left + right; }
```

### Verification

Box/Unbox nodes should disappear from graph.

---

## Problem 4: Deoptimization Nodes in Hot Paths

### Detection

```bash
cat truffle-tier.json | jq '.nodes[] | select(.props.label | test("Deoptimize|Unreached"))'
```

**Bad output**: Nodes found in hot function

### Root Cause

Unstable type assumptions.

### Fix

Add proper guards and type specializations. Use `detecting-deoptimizations` skill to find exact location.

---

## Problem 5: High InvokeNode Count

### Detection

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key == "InvokeNode")'
```

**Bad output**: High count of `InvokeNode`

### Root Cause

Unspecialized method calls - should be specialized arithmetic nodes.

### Fix

Add proper specializations for operations so they compile to direct arithmetic rather than method calls.

---

## Success Criteria

After optimization:
- ✅ Zero `OptimizedIndirectCallNode` (all direct)
- ✅ Zero allocation nodes after PartialEscape
- ✅ Zero `BoxNode`/`UnboxNode` (primitives stay unboxed)
- ✅ Low `InvokeNode` count (arithmetic specialized)
- ✅ Zero `DeoptimizeNode` in hot paths
- ✅ High `ConstantNode` count (good partial evaluation)
- ✅ Simple, linear graphs (few branches)

---

## Reference Documentation

- Seafoam: https://github.com/Shopify/seafoam
- BGV format: https://github.com/Shopify/seafoam/blob/main/docs/bgv.md
- GraalVM Debugging: https://github.com/oracle/graal/blob/master/compiler/docs/Debugging.md
- Use `fetching-truffle-documentation` skill for API reference
