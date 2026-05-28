# Memory Management

## Prevent Memory Leaks

### Automatic Memory Management (Preferred)

Use language features that automatically manage memory:

**C++ Smart Pointers**:
```cpp
#include <memory>

// Unique ownership
std::unique_ptr<Resource> resource = std::make_unique<Resource>();

// Shared ownership
std::shared_ptr<Resource> shared = std::make_shared<Resource>();

// Weak reference (doesn't prevent deletion)
std::weak_ptr<Resource> weak = shared;
```

**Kotlin/Java Automatic GC**:
```kotlin
// Memory automatically managed by garbage collector
val resource = Resource()
// No manual cleanup needed
```

**Python Automatic GC**:
```python
# Memory automatically managed
resource = Resource()
# No manual cleanup needed
```

### Manual Memory Management (When Required)

If you must use manual memory management:

```cpp
class ResourceManager {
    Resource* resource_;

public:
    ResourceManager() : resource_(new Resource()) {}

    ~ResourceManager() {
        delete resource_;  // Always clean up in destructor
        resource_ = nullptr;
    }

    // Rule of Five: Define or delete all special members
    ResourceManager(const ResourceManager&) = delete;
    ResourceManager& operator=(const ResourceManager&) = delete;

    ResourceManager(ResourceManager&& other) noexcept
        : resource_(other.resource_) {
        other.resource_ = nullptr;
    }

    ResourceManager& operator=(ResourceManager&& other) noexcept {
        if (this != &other) {
            delete resource_;
            resource_ = other.resource_;
            other.resource_ = nullptr;
        }
        return *this;
    }
};
```

### Common Leak Sources

❌ **Early returns without cleanup**:
```cpp
void processData() {
    Resource* res = new Resource();

    if (someCondition) {
        return;  // LEAK! Resource not deleted
    }

    delete res;
}
```

✅ **RAII prevents leaks**:
```cpp
void processData() {
    auto res = std::make_unique<Resource>();

    if (someCondition) {
        return;  // OK! unique_ptr cleans up automatically
    }

    // res cleaned up automatically here too
}
```

❌ **Exception throwing without cleanup**:
```cpp
void processData() {
    Resource* res = new Resource();

    // If this throws, resource leaks
    riskyOperation();

    delete res;
}
```

✅ **RAII handles exceptions**:
```cpp
void processData() {
    auto res = std::make_unique<Resource>();

    // If this throws, unique_ptr still cleans up
    riskyOperation();
}
```

## Clarify Object Lifetimes

### Ownership Semantics

Make ownership explicit in your code:

**Single Owner (C++)**:
```cpp
class ResourceOwner {
    std::unique_ptr<Resource> ownedResource_;  // Clear ownership

public:
    // Transfer ownership to caller
    std::unique_ptr<Resource> releaseResource() {
        return std::move(ownedResource_);
    }

    // Borrow resource (no ownership transfer)
    Resource* borrowResource() {
        return ownedResource_.get();
    }
};
```

**Shared Ownership (C++)**:
```cpp
class SharedResourceManager {
    std::shared_ptr<Resource> sharedResource_;

public:
    // Share ownership with caller
    std::shared_ptr<Resource> getResource() {
        return sharedResource_;  // Reference count increases
    }
};
```

### Lifetime Guidelines

1. **Prefer stack allocation** over heap when possible
2. **Use smart pointers** instead of raw pointers for ownership
3. **Document lifetime** in function comments when non-obvious
4. **Avoid dangling references** by ensuring objects outlive references to them

### Example: Dangling Reference Prevention

❌ **Dangling reference**:
```cpp
const std::string& getDatabaseName() {
    std::string name = "MyDatabase";
    return name;  // WRONG! Returning reference to local variable
}
```

✅ **Proper lifetime**:
```cpp
// Option 1: Return by value
std::string getDatabaseName() {
    return "MyDatabase";  // OK! Value returned
}

// Option 2: Return reference to long-lived object
class Database {
    std::string name_ = "MyDatabase";

public:
    const std::string& getName() const {
        return name_;  // OK! name_ lives as long as Database object
    }
};
```

## Avoid Holding Unnecessary References

### Reference Lifetime Issues

**C++**:
```cpp
class UserManager {
    std::vector<std::weak_ptr<User>> activeUsers_;  // Use weak_ptr to avoid keeping objects alive

public:
    void registerUser(std::shared_ptr<User> user) {
        activeUsers_.push_back(user);  // weak_ptr doesn't extend lifetime
    }

    void cleanup() {
        // Remove expired weak_ptrs
        activeUsers_.erase(
            std::remove_if(activeUsers_.begin(), activeUsers_.end(),
                [](const auto& weak) { return weak.expired(); }),
            activeUsers_.end()
        );
    }
};
```

**Kotlin**:
```kotlin
class EventManager {
    // WeakReference doesn't prevent garbage collection
    private val listeners = mutableListOf<WeakReference<EventListener>>()

    fun registerListener(listener: EventListener) {
        listeners.add(WeakReference(listener))
    }

    fun cleanup() {
        listeners.removeAll { it.get() == null }
    }
}
```

**Python**:
```python
import weakref

class EventManager:
    def __init__(self):
        self._listeners = []  # List of weak references

    def register_listener(self, listener):
        self._listeners.append(weakref.ref(listener))

    def cleanup(self):
        # Remove dead references
        self._listeners = [ref for ref in self._listeners if ref() is not None]
```

## Memory Efficiency

### Pool Allocations

For frequent allocations/deallocations:

```cpp
template<typename T, size_t PoolSize = 1024>
class ObjectPool {
    std::array<T, PoolSize> pool_;
    std::vector<T*> available_;

public:
    ObjectPool() {
        for (auto& obj : pool_) {
            available_.push_back(&obj);
        }
    }

    T* acquire() {
        if (available_.empty()) {
            throw std::runtime_error("Pool exhausted");
        }

        T* obj = available_.back();
        available_.pop_back();
        return obj;
    }

    void release(T* obj) {
        available_.push_back(obj);
    }
};
```

### Reduce Allocations

```cpp
// Bad: Allocates on every call
std::string formatMessage(const std::string& name, int value) {
    return "User " + name + " has value " + std::to_string(value);
}

// Better: Single allocation
std::string formatMessage(const std::string& name, int value) {
    std::ostringstream oss;
    oss << "User " << name << " has value " << value;
    return oss.str();
}

// Best: Pre-allocated buffer for repeated calls
class MessageFormatter {
    std::ostringstream buffer_;

public:
    std::string formatMessage(const std::string& name, int value) {
        buffer_.str("");  // Clear buffer
        buffer_ << "User " << name << " has value " << value;
        return buffer_.str();
    }
};
```

## Memory Safety Tools

### Detection Tools

**C++ Sanitizers**:
```bash
# Address Sanitizer (detects leaks, use-after-free, buffer overflows)
g++ -fsanitize=address -g program.cpp

# Memory Sanitizer (detects uninitialized reads)
clang++ -fsanitize=memory -g program.cpp

# Leak Sanitizer (detects memory leaks)
g++ -fsanitize=leak -g program.cpp
```

**Valgrind**:
```bash
# Comprehensive memory error detection
valgrind --leak-check=full --show-leak-kinds=all ./program

# Detailed leak information
valgrind --leak-check=full --track-origins=yes ./program
```

### Static Analysis

```bash
# Clang Static Analyzer
clang++ --analyze program.cpp

# Cppcheck
cppcheck --enable=all program.cpp
```
