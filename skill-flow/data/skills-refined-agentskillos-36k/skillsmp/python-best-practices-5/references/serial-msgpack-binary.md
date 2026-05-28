---
title: Use MessagePack for Compact Binary Serialization
impact: MEDIUM
impactDescription: 30-50% smaller than JSON, faster parsing
tags: serial, msgpack, binary, compression
---

## Use MessagePack for Compact Binary Serialization

MessagePack produces smaller payloads than JSON and parses faster, making it ideal for high-volume internal APIs and caching.

**Incorrect (verbose JSON for internal API):**

```python
import json

def cache_set(key: str, value: dict) -> None:
    redis.set(key, json.dumps(value))  # Verbose text format

def cache_get(key: str) -> dict | None:
    if data := redis.get(key):
        return json.loads(data)
    return None
```

**Correct (compact MessagePack):**

```python
import msgpack

def cache_set(key: str, value: dict) -> None:
    redis.set(key, msgpack.packb(value))  # 30-50% smaller

def cache_get(key: str) -> dict | None:
    if data := redis.get(key):
        return msgpack.unpackb(data)
    return None
```

**With custom types:**

```python
import msgpack
from datetime import datetime

def encode_datetime(obj):
    if isinstance(obj, datetime):
        return {"__datetime__": obj.isoformat()}
    return obj

def decode_datetime(obj):
    if "__datetime__" in obj:
        return datetime.fromisoformat(obj["__datetime__"])
    return obj

packed = msgpack.packb(data, default=encode_datetime)
unpacked = msgpack.unpackb(packed, object_hook=decode_datetime)
```

Reference: [msgpack-python documentation](https://github.com/msgpack/msgpack-python)
