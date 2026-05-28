---
title: Use orjson for High-Performance JSON
impact: MEDIUM
impactDescription: 3-10× faster than stdlib json
tags: serial, json, orjson, performance
---

## Use orjson for High-Performance JSON

The `orjson` library is significantly faster than the standard library `json` module and handles common Python types natively.

**Incorrect (stdlib json, slow):**

```python
import json

def serialize_response(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")

def parse_request(body: bytes) -> dict:
    return json.loads(body.decode("utf-8"))
```

**Correct (orjson, 3-10× faster):**

```python
import orjson

def serialize_response(data: dict) -> bytes:
    return orjson.dumps(data)  # Returns bytes directly

def parse_request(body: bytes) -> dict:
    return orjson.loads(body)  # Accepts bytes directly
```

**orjson handles common types:**

```python
import orjson
from datetime import datetime
from uuid import UUID

data = {
    "timestamp": datetime.now(),  # Auto-serialized to ISO format
    "user_id": UUID("12345678-1234-5678-1234-567812345678"),
    "scores": [1.5, 2.7, 3.9],
}

# No need for custom encoder
result = orjson.dumps(data)
```

Reference: [orjson documentation](https://github.com/ijl/orjson)
