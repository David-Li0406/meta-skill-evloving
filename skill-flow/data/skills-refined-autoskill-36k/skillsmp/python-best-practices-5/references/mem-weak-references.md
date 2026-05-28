---
title: Use Weak References for Caches and Observers
impact: HIGH
impactDescription: prevents memory leaks, allows automatic cleanup
tags: mem, weakref, cache, observer-pattern
---

## Use Weak References for Caches and Observers

Strong references in caches and observer patterns prevent garbage collection, causing memory leaks. Use `weakref` to allow objects to be collected when no longer needed.

**Incorrect (strong references prevent GC):**

```python
class EventEmitter:
    def __init__(self):
        self.listeners: list[Callable] = []

    def subscribe(self, callback: Callable):
        self.listeners.append(callback)  # Strong reference
        # Callback owner cannot be GC'd even when out of scope
```

**Correct (weak references allow GC):**

```python
import weakref

class EventEmitter:
    def __init__(self):
        self.listeners: list[weakref.ref] = []

    def subscribe(self, callback: Callable):
        self.listeners.append(weakref.ref(callback))

    def emit(self, event: Event):
        # Clean up dead references and call live ones
        self.listeners = [ref for ref in self.listeners if ref() is not None]
        for ref in self.listeners:
            if callback := ref():
                callback(event)
```

**Alternative (WeakValueDictionary for caches):**

```python
from weakref import WeakValueDictionary

# Cached objects can be GC'd when no other references exist
_user_cache: WeakValueDictionary[int, User] = WeakValueDictionary()

def get_user(user_id: int) -> User:
    if user_id not in _user_cache:
        _user_cache[user_id] = fetch_user_from_db(user_id)
    return _user_cache[user_id]
```

Reference: [weakref documentation](https://docs.python.org/3/library/weakref.html)
