---
name: workflow-pattern-data
description: "Data processing pipeline patterns (clean, transform, aggregate). Use when asking 'data pipeline', 'data processing', 'data transformation', or 'data cleaning'."
---

# Data Processing Pipeline Patterns

Patterns for data cleaning, transformation, and aggregation workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-pattern-etl`](workflow-pattern-etl.md), [`nodes-transform-reference`](../nodes/nodes-transform-reference.md)

## Pattern: Data Quality Pipeline

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Load data
workflow.add_node("CSVReaderNode", "load", {"file_path": "data.csv"})

# 2. Remove duplicates
workflow.add_node("DeduplicateNode", "dedupe", {
    "input": "{{load.data}}",
    "key_fields": ["email"]
})

# 3. Validate schema
workflow.add_node("DataValidationNode", "validate", {
    "input": "{{dedupe.data}}",
    "schema": {"email": "email", "age": "integer"}
})

# 4. Clean fields
workflow.add_node("TransformNode", "clean", {
    "input": "{{validate.valid_data}}",
    "transformations": [
        {"field": "email", "operation": "lowercase"},
        {"field": "name", "operation": "trim"}
    ]
})

# 5. Aggregate metrics
workflow.add_node("AggregateNode", "aggregate", {
    "input": "{{clean.data}}",
    "group_by": ["country"],
    "aggregations": {"count": "COUNT(*)", "avg_age": "AVG(age)"}
})

workflow.add_connection("load", "dedupe")
workflow.add_connection("dedupe", "validate")
workflow.add_connection("validate", "clean")
workflow.add_connection("clean", "aggregate")
```

## Documentation

- **Data Processing**: [`sdk-users/7-advanced-topics/workflows/data-processing.md`](../../../../sdk-users/7-advanced-topics/workflows/data-processing.md)

<!-- Trigger Keywords: data pipeline, data processing, data transformation, data cleaning, data quality -->
