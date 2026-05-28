# Exception and Error Handling

Apply these principles consistently, supplementing them with language-specific error handling patterns.

## General Principles

### Anticipate and Handle Errors

Use appropriate mechanisms to signal and handle errors:

- **Exceptions**: For exceptional, recoverable errors (C++, Java, Python, Kotlin)
- **Result types**: For expected error conditions (Rust, modern C++)
- **Error codes**: For performance-critical or C-compatible code
- **Null safety**: Language built-in null handling (Kotlin, TypeScript)

### Language-Specific Patterns

**C++**:
```cpp
// Use exceptions for exceptional cases
throw std::runtime_error("Database connection failed");

// Use std::optional for expected "no value" cases
std::optional<User> findUser(int id);

// Use std::expected (C++23) or similar for expected errors
std::expected<Data, Error> fetchData();
```

**Kotlin**:
```kotlin
// Use exceptions for exceptional cases
throw IllegalStateException("Invalid state transition")

// Use nullable types for expected "no value"
fun findUser(id: Int): User?

// Use Result for expected errors
fun fetchData(): Result<Data>
```

**Python**:
```python
# Use exceptions (Python's idiomatic approach)
raise ValueError("Invalid configuration")

# Use Optional for "no value" cases
from typing import Optional
def find_user(id: int) -> Optional[User]:
    ...
```

## Resource Management

### Ensure Cleanup

Resources (files, connections, memory) must be released when no longer needed.

**C++ (RAII)**:
```cpp
{
    std::ifstream file("data.txt");  // Automatically closed when scope exits
    // Use file...
}  // File closed here, even if exception thrown
```

**Python (Context Managers)**:
```python
with open("data.txt") as file:
    # Use file...
# File automatically closed here
```

**Kotlin (use function)**:
```kotlin
File("data.txt").inputStream().use { stream ->
    // Use stream...
}  // Stream automatically closed
```

### Custom Resource Management

Create RAII wrappers or context managers for custom resources:

```cpp
class DatabaseConnection {
public:
    DatabaseConnection() { connect(); }
    ~DatabaseConnection() { disconnect(); }

    // Disable copying, enable moving
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection(DatabaseConnection&&) = default;

private:
    void connect();
    void disconnect();
};
```

## Input Validation

### Validate Early

Validate all external input at the boundary of your system:

```cpp
User createUser(const UserData& data) {
    // Validate at entry point
    if (data.email.empty()) {
        throw std::invalid_argument("Email cannot be empty");
    }
    if (!isValidEmail(data.email)) {
        throw std::invalid_argument("Invalid email format");
    }
    if (data.age < 0 || data.age > 150) {
        throw std::invalid_argument("Age must be between 0 and 150");
    }

    // Now safe to process
    return User{data};
}
```

### Validation Checklist

- [ ] **Type checking**: Verify data types match expectations
- [ ] **Range checking**: Ensure numeric values are within valid ranges
- [ ] **Format validation**: Check strings match expected patterns (email, URL, etc.)
- [ ] **Size limits**: Enforce maximum sizes for collections and strings
- [ ] **Business rules**: Validate domain-specific constraints

### Security Implications

Proper input validation prevents:

- **Injection attacks**: SQL injection, command injection, XSS
- **Buffer overflows**: In languages like C/C++
- **Resource exhaustion**: Via excessively large inputs
- **Logic errors**: From unexpected data formats

## Error Handling Patterns

### Try-Catch Best Practices

```cpp
try {
    // Attempt operation
    performCriticalOperation();
}
catch (const SpecificException& e) {
    // Handle specific exception with appropriate recovery
    logger.error("Specific error", "details", e.what());
    notifyUser("Operation failed: " + std::string(e.what()));
}
catch (const std::exception& e) {
    // Handle general exceptions
    logger.error("Unexpected error", "type", typeid(e).name(), "message", e.what());
    notifyUser("An unexpected error occurred");
}
catch (...) {
    // Last resort: catch all
    logger.critical("Unknown error type");
    notifyUser("A critical error occurred");
}
```

### Don't Swallow Exceptions

❌ **Silent failure**:
```cpp
try {
    criticalOperation();
}
catch (...) {
    // Nothing - error completely hidden!
}
```

✅ **Proper handling**:
```cpp
try {
    criticalOperation();
}
catch (const std::exception& e) {
    logger.error("Critical operation failed", "error", e.what());
    // Take appropriate action: retry, fallback, or propagate
    throw;  // Re-throw if can't handle
}
```

### Error Context Propagation

Include sufficient context when propagating errors:

```cpp
void processFile(const std::string& filename) {
    try {
        auto data = readFile(filename);
        transform(data);
    }
    catch (const std::exception& e) {
        // Add context before re-throwing
        throw std::runtime_error(
            "Failed to process file '" + filename + "': " + e.what()
        );
    }
}
```

## Error Recovery Strategies

### Retry with Backoff

For transient errors:

```cpp
template<typename Func>
auto retryWithBackoff(Func operation, int maxRetries = 3) {
    int retryDelay = 100;  // Start with 100ms

    for (int attempt = 0; attempt < maxRetries; ++attempt) {
        try {
            return operation();
        }
        catch (const TransientError& e) {
            if (attempt == maxRetries - 1) throw;  // Last attempt, give up

            logger.warn("Operation failed, retrying",
                       "attempt", attempt + 1,
                       "delay_ms", retryDelay);

            std::this_thread::sleep_for(std::chrono::milliseconds(retryDelay));
            retryDelay *= 2;  // Exponential backoff
        }
    }
}
```

### Fallback Mechanisms

Provide alternative functionality when primary fails:

```cpp
Data fetchData(int id) {
    try {
        return primaryDataSource.fetch(id);
    }
    catch (const DataSourceError& e) {
        logger.warn("Primary source failed, using cache", "error", e.what());
        return cache.fetch(id);  // Fallback to cache
    }
}
```

### Circuit Breaker

Prevent cascading failures:

```cpp
class CircuitBreaker {
    int failureCount = 0;
    const int threshold = 5;
    bool isOpen = false;

public:
    template<typename Func>
    auto execute(Func operation) {
        if (isOpen) {
            throw CircuitOpenError("Circuit breaker is open");
        }

        try {
            auto result = operation();
            failureCount = 0;  // Reset on success
            return result;
        }
        catch (...) {
            if (++failureCount >= threshold) {
                isOpen = true;
                logger.error("Circuit breaker opened");
            }
            throw;
        }
    }
};
```
