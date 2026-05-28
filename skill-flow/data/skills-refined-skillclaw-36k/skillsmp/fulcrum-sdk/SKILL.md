---
name: fulcrum-sdk
description: "Dispatch milestones to user-facing timeline. Use when completing significant steps: starting major phases, calling external APIs, creating external references, completing database operations, or validating Pydantic models. Never dispatch every tool call or internal logs. Environment variables FULCRUM_DISPATCH_URL, FULCRUM_DISPATCH_TOKEN, FULCRUM_TICKET_UUID, and FULCRUM_RUN_UUID must be set (injected by system)."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# Fulcrum SDK - Dispatch System

## Overview

The dispatch system provides a user-facing timeline of agent progress. Dispatches appear as milestones in the ticket UI, helping users understand what the agent is doing and track progress on their request.

**Key principle**: Dispatch **milestones**, not tool traces. Users care about meaningful progress, not internal implementation details.

## Quick Start

```python
from fulcrum_sdk._internal.dispatch import get_dispatch_client

dispatch = get_dispatch_client()  # Configured from FULCRUM_* env vars

# Simple text milestone
dispatch.dispatch_text("Starting invoice processing")

# API call with service context
dispatch.dispatch_api_call(
    "Called Phonic to confirm appointment",
    service="phonic",
    operation="outbound_call",
    phone="+1234567890"
)
```

Or use the validation script:

```bash
uv run skills/fulcrum-sdk/scripts/dispatch.py
```

## When to Dispatch

### DO Dispatch

| Situation | Example |
|-----------|---------|
| Starting a major phase | `dispatch_text("Starting data extraction")` |
| Calling external APIs | `dispatch_api_call("Geocoding address", service="mapbox", ...)` |
| Creating external references | `dispatch_external_ref("Browser task created", provider="browser-use", ...)` |
| Database operations (with counts) | `dispatch_db("Inserted invoices", operation="insert", table="invoices", rows=15)` |
| Pydantic model display | `dispatch_model("Validated invoice data", model=invoice)` |

### DO NOT Dispatch

| Situation | Why |
|-----------|-----|
| Every tool call | Users don't need internal trace |
| Internal logs | Use stdout/stderr instead |
| Large payloads | Keep summaries concise |
| Secrets/credentials | Never dispatch sensitive data |
| Debug output | Belongs in stdout events |

## Kind Selection Guide

Choose the dispatch kind based on what's most valuable to the user:

| Kind | Use When | Example |
|------|----------|---------|
| `text` | General milestones, phase transitions | "Processing complete" |
| `api_call` | External API interaction is the key event | "Called Claude for extraction" |
| `external_ref` | Creating a reference for later display | Browser task, generated file |
| `db` | Database operation (include counts, not rows) | "Inserted 15 records" |
| `model` | Pydantic model display (shows field values) | "Validated Invoice model" |

## API Reference

### Getting the Client

```python
from fulcrum_sdk._internal.dispatch import get_dispatch_client

dispatch = get_dispatch_client()

# Check if dispatch is enabled
if dispatch.enabled:
    dispatch.dispatch_text("Ready to process")
```

### dispatch_text(summary, text=None)

General text milestone. Simplest dispatch kind.

```python
dispatch.dispatch_text("Starting invoice processing")
dispatch.dispatch_text("Extracted 12 line items", text="Items included office supplies, software licenses")
```

### dispatch_api_call(summary, service, operation, **details)

External API call. Include service name and operation.

```python
dispatch.dispatch_api_call(
    "Geocoding delivery address",
    service="mapbox",
    operation="geocode",
    address="123 Main St"
)

dispatch.dispatch_api_call(
    "Generated summary with Claude",
    service="anthropic",
    operation="messages.create",
    model="claude-sonnet-4-5-20250929"
)
```

### dispatch_external_ref(summary, provider, ref_type, ref_id, url=None)

External reference for later retrieval/display.

```python
# Browser Use task
dispatch.dispatch_external_ref(
    "Browser task created",
    provider="browser-use",
    ref_type="task",
    ref_id=task.id
)

# Phonic conversation
dispatch.dispatch_external_ref(
    "Outbound call started",
    provider="phonic",
    ref_type="conversation",
    ref_id=result.conversation_id
)

# Note: dispatch_external_ref is ONLY for external services with hosted IDs
# (e.g., browser-use tasks, phonic conversations). Do NOT use it for local
# files in /output/ - those are automatically collected and uploaded after
# execution. Users access them through the ticket files panel.
```

### dispatch_db(summary, operation, table, rows=None, query=None)

Database operation. Include counts, not raw data.

```python
dispatch.dispatch_db(
    "Inserted invoice records",
    operation="insert",
    table="invoices",
    rows=15
)

dispatch.dispatch_db(
    "Updated order status",
    operation="update",
    table="orders",
    rows=1,
    query="UPDATE orders SET status = 'complete' WHERE id = ?"
)
```

### dispatch_model(summary, model, input_summary=None)

Display Pydantic model data as an intermediate step. The model's field values are automatically serialized and shown in the timeline.

```python
from models.invoice import Invoice

invoice = Invoice(**data)
dispatch.dispatch_model(
    "Validated invoice data",
    model=invoice,
    input_summary="12 line items, total $1,234.56"
)
# Timeline will show: model: Invoice, temperature: 10, unit: celsius, etc.
```

## Best Practices

### Write Good Summaries

Summaries should be:
- **Present tense**: "Processing invoices" not "Processed invoices"
- **User-focused**: What matters to them, not implementation details
- **Concise**: Single line, max 512 characters
- **Specific**: "Extracted 12 line items" not "Extracted data"

### Include Relevant Context

```python
# Good - includes context
dispatch.dispatch_api_call(
    "Confirming appointment for John Smith",
    service="phonic",
    operation="outbound_call",
    phone="+1234567890"
)

# Bad - missing context
dispatch.dispatch_api_call(
    "Made phone call",
    service="phonic",
    operation="outbound_call"
)
```

### Handle Optional Dispatch

The client returns `False` on any error and never raises exceptions:

```python
# Dispatch failures don't affect execution
result = dispatch.dispatch_text("Starting processing")
# result is False if dispatch failed, but code continues

# Or check explicitly
if not dispatch.dispatch_text("Starting"):
    print("Dispatch failed (non-critical)")
```

## Anti-Patterns

### Don't Dispatch Tool Traces

```python
# BAD - Too granular
dispatch.dispatch_text("Reading file config.json")
dispatch.dispatch_text("Parsing JSON content")
dispatch.dispatch_text("Validating schema")
dispatch.dispatch_text("Writing to output.json")

# GOOD - Meaningful milestone
dispatch.dispatch_text("Configuration processed successfully")
```

### Don't Dispatch Large Payloads

```python
# BAD - Raw data in dispatch
dispatch.dispatch_json("Extracted data", {"rows": [...100 rows...]})

# GOOD - Summary only
dispatch.dispatch_db("Extracted invoice data", operation="select", table="invoices", rows=100)
```

### Don't Dispatch Sensitive Data

```python
# BAD - Contains API key
dispatch.dispatch_api_call("Calling API", service="mapbox", api_key="sk-...")

# GOOD - Key is automatically redacted, but don't include it
dispatch.dispatch_api_call("Geocoding address", service="mapbox", operation="geocode")
```

## Scripts

### scripts/dispatch.py

Validation script that emits test dispatches:

```bash
# Run with mock environment
export FULCRUM_DISPATCH_URL="http://localhost:8000/dispatch"
export FULCRUM_DISPATCH_TOKEN="test-token"
export FULCRUM_TICKET_UUID="test-ticket-uuid"
export FULCRUM_RUN_UUID="test-run-uuid"

uv run skills/fulcrum-sdk/scripts/dispatch.py
```

## References

For the complete dispatch contract specification, see [references/dispatch-contract.md](references/dispatch-contract.md).
