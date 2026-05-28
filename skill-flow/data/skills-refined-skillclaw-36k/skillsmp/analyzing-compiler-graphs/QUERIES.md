# Analysis Queries

jq and seafoam queries for analyzing compiler graphs.

## Seafoam Queries

### Describe Graph Characteristics

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '{
    node_count,
    loops,
    branches,
    deopts,
    calls,
    linear
  }'
```

**Interpretation**:
- `deopts: false` = Good (stable compilation)
- `deopts: true` = Bad (deoptimization instability)
- `linear: true` = Optimal (no branches, straight-line code)

### Count Node Types

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts' | \
  jq 'to_entries | sort_by(.value) | reverse | .[0:10]'
```

### Find Call Nodes

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | contains("Call"))'
```

### Find Allocation Nodes

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | test("Alloc|New"))'
```

### Find Boxing Nodes

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | test("Box|Unbox"))'
```

### Render to SVG

```bash
seafoam file.bgv.gz:2 render > graph.svg
```

## jq Queries (for bgv2json output)

### Find TruffleTier Graph

```bash
cat graphs.json | jq 'select(.name | contains("After TruffleTier"))' | head -1 > truffle-tier.json
```

### Count Node Types

```bash
cat graphs.json | jq '.nodes[] | .props.label' | sort | uniq -c | sort -rn
```

### Find Indirect Calls

```bash
cat graphs.json | jq '.nodes[] | select(.props.label | contains("Call")) | .props.label' | sort | uniq -c
```

### Find Failed Escape Analysis

```bash
cat graphs.json | jq 'select(.name | contains("After PartialEscape")) |
  .nodes[] | select(.props.label | test("Alloc|New")) | .props.label' | sort | uniq -c
```

### Find Boxing Operations

```bash
cat graphs.json | jq '.nodes[] | select(.props.label | test("Box|Unbox")) | .props.label' | sort | uniq -c
```

### Find InvokeNodes (Unspecialized)

```bash
cat truffle-tier.json | jq '.nodes[] | select(.props.label == "InvokeNode") | .props'
```

## JSON Structure Reference

### Top-Level Structure

```json
{
  "name": ["function_name", "phase_name"],
  "props": { /* graph metadata */ },
  "nodes": [ /* IR nodes */ ],
  "edges": [ /* data/control flow */ ],
  "blocks": [ /* basic blocks */ ]
}
```

### Node Structure

```json
{
  "id": 5,
  "props": {
    "label": "AddNode",
    "category": "arithmetic",
    "stamp": "i32",
    "nodeToBlock": "B0",
    "node_class": {
      "node_class": "jdk.graal.compiler.nodes.calc.AddNode"
    }
  }
}
```

### Edge Structure

```json
{
  "from": 5,
  "to": 1,
  "props": {
    "direct": true,
    "name": "x",
    "type": "Value",
    "index": 0
  }
}
```

## Common Node Types

### Arithmetic Operations
- `AddNode`, `SubNode`, `MulNode`, `DivNode`
- `IntegerLessThanNode`, `IntegerEqualsNode`

### Constants & Parameters
- `ConstantNode` - Compile-time constants
- `ParameterNode` - Method parameters

### Conversions (Performance Critical)
- `BoxNode` / `BoxNode$AllocatingBoxNode` - Boxing ⚠️
- `UnboxNode` - Unboxing ⚠️

### Memory Operations
- `LoadFieldNode`, `StoreFieldNode`
- `LoadIndexedNode`, `StoreIndexedNode`

### Allocations (Escape Analysis)
- `TruffleNew` - Object allocation ⚠️
- `CommitAllocationNode`, `NewInstanceNode` - Failed EA ⚠️

### Call Operations
- `OptimizedDirectCallNode` - Specialized ✅
- `OptimizedIndirectCallNode` - Dynamic ⚠️
- `InvokeNode`, `InvokeWithExceptionNode` - Unspecialized ⚠️

### Control Flow
- `IfNode`, `LoopBeginNode`, `LoopEndNode`
- `MergeNode`, `BeginNode`, `EndNode`, `ReturnNode`
