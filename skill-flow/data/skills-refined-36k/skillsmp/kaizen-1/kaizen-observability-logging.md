# Kaizen Structured Logging

**Quick reference for JSON logging with ELK Stack integration**

## Overview

Production-ready structured logging with JSON format for ELK Stack (Elasticsearch, Logstash, Kibana). Context propagation for trace correlation and centralized logger management.

## Quick Start

```python
from kaizen.core.base_agent import BaseAgent

# Enable structured logging (one line!)
agent = BaseAgent(config=config, signature=signature)
agent.enable_observability(
    service_name="my-agent",
    enable_logging=True
)

# All operations automatically logged
result = agent.run(question="test")
```

**Access Kibana**: `http://localhost:5601`

## LoggingManager

Centralized structured logging:

```python
from kaizen.core.autonomy.observability import LoggingManager

manager = LoggingManager(
    service_name="my-service",
    log_level="INFO",              # DEBUG, INFO, WARNING, ERROR, CRITICAL
    output_format="json",          # json, text
    output_file="/var/log/kaizen.log"  # Optional file output
)
```

**Methods**:
- `debug(message, context)`: Debug-level logging
- `info(message, context)`: Informational logging
- `warning(message, context)`: Warning logging
- `error(message, context)`: Error logging
- `critical(message, context)`: Critical error logging

## Structured Log Format

All logs are JSON-formatted:

```json
{
  "timestamp": "2025-10-26T10:53:45.123Z",
  "level": "INFO",
  "service": "my-agent",
  "agent_id": "qa-agent-001",
  "trace_id": "abc123def456",
  "event_type": "agent_execution",
  "message": "Agent loop completed successfully",
  "context": {
    "duration_ms": 234.5,
    "question": "What is AI?",
    "answer_length": 150
  },
  "metadata": {
    "environment": "production",
    "version": "0.5.0"
  }
}
```

## LoggingHook

Automatic logging via hooks:

```python
from kaizen.core.autonomy.hooks.builtin import LoggingHook

hook = LoggingHook(logging_manager=manager)
agent._hook_manager.register_hook(hook)
```

**Automatically logs**:
- Agent loop start/completion
- Tool executions
- LLM API calls
- Memory operations
- Errors and exceptions

## Context Propagation

Trace context automatically included:

```python
# Context from HookContext
context = {
    "agent_id": context.agent_id,
    "trace_id": context.trace_id,
    "event_type": context.event_type.value,
    "timestamp": context.timestamp,
    "data": context.data
}

# Logged with every message
manager.info("Operation completed", context=context)
```

## Log Levels

### DEBUG
Detailed diagnostic information:
```python
manager.debug("Entering tool execution", context={"tool": "calculator"})
```

### INFO
General informational messages:
```python
manager.info("Agent loop completed", context={"duration_ms": 234})
```

### WARNING
Warning messages (non-critical):
```python
manager.warning("Retry attempt", context={"attempt": 2, "max_retries": 3})
```

### ERROR
Error messages (operation failed):
```python
manager.error("Tool execution failed", context={"error": str(e)})
```

### CRITICAL
Critical errors (service degraded):
```python
manager.critical("Database connection lost", context={"db_host": "localhost"})
```

## ELK Stack Integration

### Elasticsearch Storage

Logs are sent to Elasticsearch for indexing:

```python
manager = LoggingManager(
    service_name="my-agent",
    elasticsearch_host="localhost",
    elasticsearch_port=9200,
    index_name="kaizen-logs"
)
```

### Kibana Queries

**Search by trace_id**:
```
trace_id: "abc123def456"
```

**Search by agent_id**:
```
agent_id: "qa-agent-001"
```

**Search errors in last 24h**:
```
level: ERROR AND @timestamp: [now-24h TO now]
```

**Search slow operations**:
```
context.duration_ms: >1000
```

## Common Patterns

### Operation Logging

```python
import time

# Log operation start
manager.info("Starting data processing", context={"records": 1000})

start_time = time.time()
try:
    # Process data
    result = process_data()

    # Log success
    duration_ms = (time.time() - start_time) * 1000
    manager.info("Data processing completed", context={
        "records": 1000,
        "duration_ms": duration_ms,
        "status": "success"
    })
except Exception as e:
    # Log error
    duration_ms = (time.time() - start_time) * 1000
    manager.error("Data processing failed", context={
        "records": 1000,
        "duration_ms": duration_ms,
        "error": str(e),
        "error_type": type(e).__name__
    })
```

### Multi-Agent Logging

```python
# Each agent logs with unique agent_id
for agent in agents:
    agent.enable_observability(
        service_name=f"multi-agent-{agent.agent_id}",
        enable_logging=True
    )

# Search in Kibana by agent_id or service
```

### Structured Context

```python
# Rich context for debugging
manager.info("LLM API call", context={
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "prompt_length": 150,
    "response_length": 234,
    "cost_usd": 0.003
})
```

## Production Deployment

### Docker Compose Stack

```bash
# Start ELK Stack
cd docs/observability
docker-compose up -d
```

**Included**:
- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`
- Log aggregation configured

### Production Configuration

```python
import os

manager = LoggingManager(
    service_name=os.getenv("SERVICE_NAME", "my-agent"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    elasticsearch_host=os.getenv("ES_HOST", "localhost"),
    elasticsearch_port=int(os.getenv("ES_PORT", "9200")),
    index_name=f"kaizen-logs-{os.getenv('ENVIRONMENT', 'dev')}"
)
```

### Log Rotation

```python
# File-based logging with rotation
manager = LoggingManager(
    service_name="my-agent",
    output_file="/var/log/kaizen.log",
    max_bytes=100_000_000,  # 100MB
    backup_count=10         # Keep 10 rotated files
)
```

## Testing

```python
import pytest
from io import StringIO

def test_structured_logging():
    # Capture logs
    stream = StringIO()
    manager = LoggingManager(
        service_name="test",
        output_stream=stream
    )

    # Log message
    manager.info("Test message", context={"key": "value"})

    # Verify JSON format
    import json
    log_line = stream.getvalue()
    log_entry = json.loads(log_line)

    assert log_entry["level"] == "INFO"
    assert log_entry["message"] == "Test message"
    assert log_entry["context"]["key"] == "value"
```

## Custom Log Fields

```python
# Add custom fields to all logs
manager = LoggingManager(
    service_name="my-agent",
    default_context={
        "environment": "production",
        "region": "us-west-2",
        "version": "0.5.0"
    }
)

# Custom fields included automatically
manager.info("Operation completed")
# Output includes: "environment": "production", "region": "us-west-2", etc.
```

## Log Aggregation

### Logstash Pipeline

```ruby
# logstash.conf
input {
  file {
    path => "/var/log/kaizen.log"
    codec => json
  }
}

filter {
  # Parse timestamp
  date {
    match => ["timestamp", "ISO8601"]
  }

  # Add geoip
  geoip {
    source => "client_ip"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "kaizen-logs-%{+YYYY.MM.dd}"
  }
}
```

## Compliance & Security

### PII Redaction

```python
# Redact sensitive data
def redact_pii(context):
    if "email" in context:
        context["email"] = "***@***.com"
    if "ssn" in context:
        context["ssn"] = "***-**-****"
    return context

# Log with redaction
manager.info("User action", context=redact_pii(user_data))
```

### Audit Logging

```python
# High-importance logs for compliance
manager.info("Data access", context={
    "user_id": "user123",
    "action": "read",
    "resource": "patient_record_456",
    "ip_address": "192.168.1.1",
    "timestamp": time.time()
})
```

## Resources

- **Implementation**: `src/kaizen/core/autonomy/observability/logging_manager.py`
- **Hook**: `src/kaizen/core/autonomy/hooks/builtin/logging_hook.py`
- **Tests**: `tests/unit/core/autonomy/observability/test_logging_manager.py`
- **ELK Stack**: https://www.elastic.co/elk-stack
- **JSON Logging**: https://github.com/madzak/python-json-logger
