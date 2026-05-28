---
title: Avoid Pickle for Untrusted Data
impact: MEDIUM
impactDescription: prevents arbitrary code execution vulnerabilities
tags: serial, pickle, security, deserialization
---

## Avoid Pickle for Untrusted Data

Pickle can execute arbitrary code during deserialization. Never unpickle data from untrusted sources. Use safe alternatives like JSON or MessagePack.

**Incorrect (arbitrary code execution risk):**

```python
import pickle

def load_user_data(data: bytes) -> UserData:
    return pickle.loads(data)  # Can execute arbitrary code!
```

**Correct (safe JSON deserialization):**

```python
import orjson
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    email: str

def load_user_data(data: bytes) -> UserData:
    return UserData.model_validate(orjson.loads(data))
```

**When pickle is acceptable:**
- Internal caching (e.g., ML model checkpoints)
- IPC between trusted processes
- Data you serialized yourself

**Safer pickle alternative (restricted):**

```python
import pickle

# Restrict unpickling to specific classes
class RestrictedUnpickler(pickle.Unpickler):
    SAFE_CLASSES = {"UserData", "OrderData"}

    def find_class(self, module, name):
        if name in self.SAFE_CLASSES:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Forbidden class: {name}")
```

Reference: [pickle security warning](https://docs.python.org/3/library/pickle.html#module-pickle)
