---
name: nodes-transform-reference
description: "Transformation nodes reference (DataTransformer, Filter, Map, Sort). Use when asking 'transform node', 'DataTransformer', 'data transform', 'filter data', or 'map node'."
---

# Transformation Nodes Reference

Complete reference for data transformation and processing nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-data-reference`](nodes-data-reference.md), [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (transformation workflows)

## Quick Reference

```python
from kailash.nodes.transform import (
    FilterNode,
    DataTransformer,
    AggregationNode,
    TextSplitterNode
)
```

## Filter Node

### FilterNode
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("FilterNode", "filter", {
    "condition": "age > 18 and status == 'active'",
    "data": []  # From previous node
})
```

## Data Transformer

### DataTransformer
```python
workflow.add_node("DataTransformer", "transform", {
    "transformations": [
        {"field": "price", "operation": "multiply", "value": 1.1},
        {"field": "name", "operation": "upper"}
    ],
    "data": []  # From previous node
})
```

## Aggregation

### AggregationNode
```python
workflow.add_node("AggregationNode", "aggregate", {
    "group_by": ["category"],
    "aggregations": [
        {"field": "price", "operation": "sum"},
        {"field": "quantity", "operation": "avg"}
    ],
    "data": []  # From previous node
})
```

## Text Processing

### TextSplitterNode
```python
workflow.add_node("TextSplitterNode", "splitter", {
    "chunk_size": 1000,
    "chunk_overlap": 100,
    "separator": "\n\n"
})
```

## Related Skills

- **Data Nodes**: [`nodes-data-reference`](nodes-data-reference.md)
- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Transform Nodes**: [`sdk-users/2-core-concepts/nodes/06-transform-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/06-transform-nodes.md)

<!-- Trigger Keywords: transform node, DataTransformer, data transform, filter data, map node, FilterNode, AggregationNode -->
