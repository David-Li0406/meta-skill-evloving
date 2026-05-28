# Dispatch Contract Specification

This document defines the complete contract for the Fulcrum dispatch system.

## Overview

The dispatch system sends structured events from agent execution to the Fulcrum API. These events appear as milestones in the ticket timeline, providing users visibility into agent progress.

## Design Principles

### Best-Effort Delivery

- All dispatch methods return `False` on any error (never raise exceptions)
- No retries are attempted
- Requests timeout after 1.5 seconds by default
- Agent execution continues regardless of dispatch success/failure

### Automatic Protections

- Sensitive keys (`api_key`, `token`, `password`, `secret`, etc.) are automatically redacted
- Payloads exceeding 64KB are truncated
- Summaries exceeding 512 characters are truncated

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `FULCRUM_DISPATCH_URL` | The dispatch API endpoint URL |
| `FULCRUM_DISPATCH_TOKEN` | Authentication token for the API |
| `FULCRUM_TICKET_UUID` | UUID of the ticket being processed |
| `FULCRUM_RUN_UUID` | UUID of the current execution run |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `FULCRUM_MESSAGE_UUID` | UUID of the current message (if applicable) | None |
| `FULCRUM_DISPATCH_DEBUG` | Set to "1" to enable debug logging | Disabled |
| `FULCRUM_DISPATCH_TIMEOUT_MS` | Request timeout in milliseconds | 1500 |
| `FULCRUM_DISPATCH_MAX_BYTES` | Maximum payload size in bytes | 65536 |

## Entry Schema

All dispatches follow this base schema:

```python
class DispatchEntry:
    # Required fields
    ticket_uuid: str           # UUID of the ticket
    run_uuid: str              # UUID of the run
    kind: str                  # Classification (max 64 chars)
    summary: str               # Human-readable summary (max 512 chars, single line)

    # Optional fields
    message_uuid: str | None   # Reference to a ticket message
    payload: dict | None       # Additional structured data (max 64KB)
    source: str                # Origin of dispatch (default: "sdk", max 32 chars)
    schema_version: int        # Schema version (default: 1)
    client_ts: str | None      # Client timestamp (ISO string)
```

### Constraints

| Field | Constraint |
|-------|------------|
| `kind` | Non-empty, max 64 characters |
| `summary` | Max 512 characters, single line (no newlines) |
| `payload` | Max 64KB when serialized to JSON |
| `source` | Max 32 characters |

## Dispatch Kinds

### text

General text milestones for phase transitions and status updates.

**Payload Schema:**
```python
class TextPayload:
    text: str | None  # Optional additional text content
```

**Example:**
```python
dispatch.dispatch_text("Processing complete")
dispatch.dispatch_text("Extracted data", text="Found 12 matching records")
```

### api_call

External API interactions where the action is the primary event.

**Payload Schema:**
```python
class ApiCallPayload:
    service: str      # Service/provider name (required)
    operation: str    # Operation performed (required)
    # Additional fields allowed
```

**Example:**
```python
dispatch.dispatch_api_call(
    "Called Claude for text extraction",
    service="anthropic",
    operation="messages.create",
    model="claude-sonnet-4-5-20250929"
)
```

### external_ref

References to external resources for later retrieval/display.

**Payload Schema:**
```python
class ExternalRefPayload:
    provider: str     # Provider name (required)
    ref_type: str     # Type of reference (required)
    ref_id: str       # External reference ID (required)
    url: str | None   # Optional URL to the resource
```

**Example:**
```python
dispatch.dispatch_external_ref(
    "Browser task created",
    provider="browser-use",
    ref_type="task",
    ref_id="task_abc123"
)
```

### db

Database operations with counts (not raw data).

**Payload Schema:**
```python
class DbPayload:
    table: str        # Table name (required)
    operation: str    # Operation type: insert, update, delete, select (required)
    count: int | None # Number of rows affected/returned
    query: str | None # Optional query string (will be redacted)
```

**Example:**
```python
dispatch.dispatch_db(
    "Inserted invoice records",
    operation="insert",
    table="invoices",
    rows=15
)
```

### model

Pydantic model display events. Shows actual model field values in the timeline.

**Payload Schema:**
```python
class ModelPayload:
    model_name: str          # Class name of the model (required)
    data: dict | None        # Actual model field values (auto-serialized)
    input_summary: str | None # Brief description of input
    output_summary: str | None # Brief description of output
```

**Example:**
```python
dispatch.dispatch_model(
    "Validated invoice data",
    model=invoice_instance,
    input_summary="12 line items, total $1,234.56"
)
# Timeline will display: model: Invoice, temperature: 10, unit: celsius, etc.
```

## Redaction

The following keys are automatically redacted from payloads:

- `api_key`
- `token`
- `password`
- `secret`
- `credential`
- `auth`
- `key` (when value looks like a key)

Redacted values are replaced with `"[REDACTED]"`.

To skip redaction for a specific dispatch (use with caution):

```python
dispatch.dispatch("custom", "Summary", payload, skip_redaction=True)
```

## Wire Protocol

### HTTP Request

```http
POST {FULCRUM_DISPATCH_URL}
Authorization: Bearer {FULCRUM_DISPATCH_TOKEN}
Content-Type: application/json

{
  "ticket_uuid": "...",
  "run_uuid": "...",
  "kind": "text",
  "summary": "Processing started",
  "source": "sdk",
  "schema_version": 1,
  "client_ts": "2025-01-15T10:30:00Z"
}
```

### Response

- `2xx`: Success
- `4xx`: Client error (not retried)
- `5xx`: Server error (not retried)

## Client API

### Initialization

```python
from fulcrum_sdk._internal.dispatch import get_dispatch_client

# From environment variables (recommended)
dispatch = get_dispatch_client()

# Manual configuration (advanced)
from fulcrum_sdk._internal.dispatch import DispatchClient
dispatch = DispatchClient(
    dispatch_url="https://api.fulcrum.ai/dispatch",
    dispatch_token="token",
    ticket_uuid="ticket-uuid",
    run_uuid="run-uuid",
    message_uuid="message-uuid",  # optional
    timeout_ms=1500,
    max_bytes=65536,
    debug=False,
)
```

### Methods

| Method | Description |
|--------|-------------|
| `dispatch(kind, summary, payload=None, ...)` | Core dispatch method |
| `dispatch_text(summary, text=None)` | Text milestone |
| `dispatch_api_call(summary, service, operation, **details)` | API call event |
| `dispatch_external_ref(summary, provider, ref_type, ref_id, url=None)` | External reference |
| `dispatch_db(summary, operation, table, rows=None, query=None)` | Database operation |
| `dispatch_model(summary, model, input_summary=None)` | Model validation |

### Properties

| Property | Description |
|----------|-------------|
| `enabled` | `True` if client is properly configured |

## Error Handling

All dispatch methods return `bool`:
- `True`: Dispatch sent successfully
- `False`: Dispatch failed (any reason)

Failures are logged to stderr if `FULCRUM_DISPATCH_DEBUG=1`.

Common failure reasons:
- Missing environment variables (client disabled)
- Network timeout
- API error response
- Payload too large (after truncation notice is added)
