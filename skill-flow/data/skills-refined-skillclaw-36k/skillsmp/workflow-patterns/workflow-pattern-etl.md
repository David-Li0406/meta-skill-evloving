---
name: workflow-pattern-etl
description: "ETL pipeline patterns (Extract, Transform, Load). Use when asking 'ETL', 'data pipeline', 'extract transform load', 'data migration', or 'data integration'."
---

# ETL Pipeline Patterns

Comprehensive patterns for Extract, Transform, Load workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-pattern-data`](workflow-pattern-data.md), [`dataflow-specialist`](../../02-dataflow/dataflow-specialist.md)
> Related Subagents: `dataflow-specialist` (database ETL), `pattern-expert` (ETL workflows)

## Quick Reference

ETL patterns enable:
- **Data extraction** - CSV, JSON, databases, APIs
- **Transformation** - Clean, normalize, enrich, aggregate
- **Loading** - Write to databases, files, APIs
- **Error handling** - Validation, retries, dead letter queues

## Pattern 1: CSV to Database ETL

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. EXTRACT: Read CSV
workflow.add_node("CSVReaderNode", "extract", {
    "file_path": "data/customers.csv",
    "delimiter": ",",
    "encoding": "utf-8"
})

# 2. TRANSFORM: Validate data
workflow.add_node("DataValidationNode", "validate", {
    "input": "{{extract.data}}",
    "schema": {
        "email": "email",
        "age": "integer",
        "name": "string"
    },
    "on_error": "collect"  # Collect invalid rows
})

# 3. TRANSFORM: Clean data
workflow.add_node("TransformNode", "clean", {
    "input": "{{validate.valid_data}}",
    "transformations": [
        {"field": "email", "operation": "lowercase"},
        {"field": "name", "operation": "trim"},
        {"field": "phone", "operation": "normalize_phone"}
    ]
})

# 4. TRANSFORM: Enrich data
workflow.add_node("APICallNode", "enrich_location", {
    "url": "https://api.example.com/geocode",
    "method": "POST",
    "body": "{{clean.data}}"
})

# 5. LOAD: Insert to database
workflow.add_node("DatabaseExecuteNode", "load", {
    "query": """
        INSERT INTO customers (name, email, age, location)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (email) DO UPDATE SET
            name = EXCLUDED.name,
            age = EXCLUDED.age,
            location = EXCLUDED.location
    """,
    "parameters": "{{enrich_location.enriched_data}}"
})

# 6. Error handling: Log invalid rows
workflow.add_node("CSVWriterNode", "log_errors", {
    "file_path": "logs/invalid_rows.csv",
    "data": "{{validate.invalid_data}}",
    "headers": ["row", "error", "data"]
})

# Connect nodes
workflow.add_connection("extract", "validate")
workflow.add_connection("validate", "clean")
workflow.add_connection("clean", "enrich_location")
workflow.add_connection("enrich_location", "load")
workflow.add_connection("validate", "log_errors")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Pattern 2: API to Database ETL

```python
workflow = WorkflowBuilder()

# 1. EXTRACT: Paginated API
workflow.add_node("SetVariableNode", "init_page", {
    "page": 1,
    "has_more": True
})

workflow.add_node("APICallNode", "extract_api", {
    "url": "https://api.example.com/users?page={{init_page.page}}",
    "method": "GET",
    "headers": {"Authorization": "Bearer {{secrets.api_token}}"}
})

# 2. TRANSFORM: Normalize API response
workflow.add_node("TransformNode", "normalize", {
    "input": "{{extract_api.data}}",
    "mapping": {
        "user_id": "id",
        "full_name": "name",
        "email_address": "email",
        "created_at": "timestamp|iso8601"
    }
})

# 3. TRANSFORM: Filter records
workflow.add_node("FilterNode", "filter_active", {
    "input": "{{normalize.data}}",
    "condition": "status == 'active' AND created_at > '2024-01-01'"
})

# 4. LOAD: Batch insert
workflow.add_node("DatabaseExecuteNode", "load_batch", {
    "query": """
        INSERT INTO users (user_id, full_name, email_address, created_at)
        VALUES (?, ?, ?, ?)
    """,
    "batch": True,
    "batch_size": 100,
    "parameters": "{{filter_active.filtered_data}}"
})

# 5. Check for more pages
workflow.add_node("ConditionalNode", "check_more", {
    "condition": "{{extract_api.has_next_page}} == true",
    "true_branch": "next_page",
    "false_branch": "complete"
})

# 6. Increment page
workflow.add_node("TransformNode", "next_page", {
    "input": "{{init_page.page}}",
    "transformation": "value + 1"
})

# Loop for pagination
workflow.add_connection("init_page", "extract_api")
workflow.add_connection("extract_api", "normalize")
workflow.add_connection("normalize", "filter_active")
workflow.add_connection("filter_active", "load_batch")
workflow.add_connection("load_batch", "check_more")
workflow.add_connection("check_more", "next_page", "true")
workflow.add_connection("next_page", "extract_api")  # Loop!
```

## Pattern 3: Database to Database Migration

```python
workflow = WorkflowBuilder()

# 1. EXTRACT: Read from source DB
workflow.add_node("DatabaseQueryNode", "extract_source", {
    "connection": "source_db",
    "query": """
        SELECT id, name, email, created_at
        FROM legacy_users
        WHERE migrated = FALSE
        LIMIT 1000
    """
})

# 2. TRANSFORM: Data mapping
workflow.add_node("TransformNode", "transform_schema", {
    "input": "{{extract_source.results}}",
    "transformations": [
        {"source": "id", "target": "legacy_id", "type": "string"},
        {"source": "name", "target": "full_name", "type": "string"},
        {"source": "email", "target": "email_address", "type": "lowercase"},
        {"source": "created_at", "target": "registration_date", "type": "datetime"}
    ]
})

# 3. TRANSFORM: Validate business rules
workflow.add_node("DataValidationNode", "validate_rules", {
    "input": "{{transform_schema.data}}",
    "rules": [
        {"field": "email_address", "validation": "email_format"},
        {"field": "full_name", "validation": "not_empty"},
        {"field": "registration_date", "validation": "valid_date"}
    ]
})

# 4. LOAD: Insert to target DB
workflow.add_node("DatabaseExecuteNode", "load_target", {
    "connection": "target_db",
    "query": """
        INSERT INTO users (legacy_id, full_name, email_address, registration_date)
        VALUES (?, ?, ?, ?)
    """,
    "batch": True,
    "parameters": "{{validate_rules.valid_data}}"
})

# 5. Update source DB (mark as migrated)
workflow.add_node("DatabaseExecuteNode", "mark_migrated", {
    "connection": "source_db",
    "query": """
        UPDATE legacy_users
        SET migrated = TRUE, migrated_at = NOW()
        WHERE id IN ({{load_target.inserted_ids}})
    """
})

# 6. Handle failures
workflow.add_node("DatabaseExecuteNode", "log_failures", {
    "connection": "source_db",
    "query": """
        INSERT INTO migration_failures (legacy_id, error, data)
        VALUES (?, ?, ?)
    """,
    "parameters": "{{validate_rules.invalid_data}}"
})

workflow.add_connection("extract_source", "transform_schema")
workflow.add_connection("transform_schema", "validate_rules")
workflow.add_connection("validate_rules", "load_target")
workflow.add_connection("load_target", "mark_migrated")
workflow.add_connection("validate_rules", "log_failures")
```

## Pattern 4: Real-Time Streaming ETL

```python
workflow = WorkflowBuilder()

# 1. EXTRACT: Stream from message queue
workflow.add_node("MessageQueueConsumerNode", "extract_stream", {
    "queue_url": "kafka://localhost:9092/events",
    "topic": "user_events",
    "batch_size": 50
})

# 2. TRANSFORM: Parse events
workflow.add_node("TransformNode", "parse_events", {
    "input": "{{extract_stream.messages}}",
    "parsing": {
        "format": "json",
        "flatten": True,
        "extract_fields": ["user_id", "event_type", "timestamp", "data"]
    }
})

# 3. TRANSFORM: Aggregate metrics
workflow.add_node("AggregateNode", "calculate_metrics", {
    "input": "{{parse_events.events}}",
    "group_by": ["user_id", "event_type"],
    "aggregations": {
        "count": "COUNT(*)",
        "avg_duration": "AVG(data.duration)",
        "last_seen": "MAX(timestamp)"
    },
    "window": "5m"  # 5-minute window
})

# 4. LOAD: Write to time-series DB
workflow.add_node("DatabaseExecuteNode", "load_metrics", {
    "connection": "timescaledb",
    "query": """
        INSERT INTO user_metrics (user_id, event_type, count, avg_duration, last_seen, window_start)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    "parameters": "{{calculate_metrics.aggregated}}"
})

# 5. Acknowledge messages
workflow.add_node("MessageQueueAckNode", "ack_messages", {
    "message_ids": "{{extract_stream.message_ids}}"
})

workflow.add_connection("extract_stream", "parse_events")
workflow.add_connection("parse_events", "calculate_metrics")
workflow.add_connection("calculate_metrics", "load_metrics")
workflow.add_connection("load_metrics", "ack_messages")
```

## Best Practices

1. **Batch processing** - Process in chunks (100-1000 records)
2. **Idempotent operations** - Use UPSERT/ON CONFLICT
3. **Error isolation** - Collect invalid data separately
4. **Transaction boundaries** - Commit per batch
5. **Progress tracking** - Mark processed records
6. **Data validation** - Validate at each stage
7. **Logging** - Track successes, failures, timing

## Common Pitfalls

- **No error handling** - Lost data on failures
- **Memory overload** - Loading entire datasets
- **Missing validation** - Invalid data in target
- **No rollback strategy** - Can't recover from failures
- **Poor performance** - Not using batch operations

## Related Skills

- **DataFlow Framework**: [`dataflow-specialist`](../../02-dataflow/dataflow-specialist.md)
- **Data Patterns**: [`workflow-pattern-data`](workflow-pattern-data.md)
- **Database Nodes**: [`nodes-database-reference`](../nodes/nodes-database-reference.md)

## Documentation

- **ETL Patterns**: [`sdk-users/7-advanced-topics/workflows/etl-patterns.md`](../../../../sdk-users/7-advanced-topics/workflows/etl-patterns.md)
- **DataFlow Guide**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md)

<!-- Trigger Keywords: ETL, data pipeline, extract transform load, data migration, data integration, batch processing -->
