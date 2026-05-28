---
title: Use NamedTuple for Immutable Lightweight Records
impact: HIGH
impactDescription: 3-10× less memory than dict, attribute access by name
tags: ds, namedtuple, immutable, records
---

## Use NamedTuple for Immutable Lightweight Records

Dictionaries storing fixed fields waste memory on hash tables and string keys. `NamedTuple` provides named access with tuple efficiency.

**Incorrect (dict overhead for structured data):**

```python
def fetch_coordinates() -> list[dict[str, float]]:
    return [
        {"latitude": 40.7128, "longitude": -74.0060, "altitude": 10.0},
        {"latitude": 34.0522, "longitude": -118.2437, "altitude": 71.0},
    ]
    # Each dict: ~240 bytes
```

**Correct (NamedTuple, minimal overhead):**

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    latitude: float
    longitude: float
    altitude: float

def fetch_coordinates() -> list[Coordinate]:
    return [
        Coordinate(40.7128, -74.0060, 10.0),
        Coordinate(34.0522, -118.2437, 71.0),
    ]
    # Each tuple: ~72 bytes
```

**Benefits:**
- Immutable by default (hashable, safe as dict keys)
- Named attribute access (`coord.latitude`)
- Unpacking support (`lat, lon, alt = coord`)
- Memory efficient (no per-instance dict)

Reference: [NamedTuple documentation](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
