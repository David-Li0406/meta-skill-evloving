# Code Quality and Maintainability

## Single Responsibility Functions

Each function should perform **one well-defined task**.

### Guidelines

- **Focus**: A function should do one thing and do it well
- **Naming**: If you struggle to name a function without using "and", it might do too much
- **Length**: Functions should typically be 20-50 lines; longer functions often need splitting

### Example

❌ **Multiple responsibilities**:
```cpp
void processUserRequest(const Request& req) {
    // Validate input
    if (!isValid(req)) throw InvalidRequest();

    // Authenticate user
    User user = authenticate(req.token);

    // Fetch data from database
    Data data = db.fetch(req.id);

    // Transform data
    Result result = transform(data);

    // Log activity
    logger.log("Request processed");

    // Send response
    sendResponse(result);
}
```

✅ **Single responsibilities**:
```cpp
void processUserRequest(const Request& req) {
    validateRequest(req);
    User user = authenticateUser(req.token);
    Data data = fetchData(req.id);
    Result result = transformData(data);
    logActivity("Request processed");
    sendResponse(result);
}
```

## Complexity Management

### Reduce Nesting

Deep nesting makes code hard to read and maintain.

❌ **Deep nesting**:
```cpp
if (user.isAuthenticated()) {
    if (user.hasPermission()) {
        if (data.isValid()) {
            if (!cache.has(key)) {
                // Process...
            }
        }
    }
}
```

✅ **Early returns**:
```cpp
if (!user.isAuthenticated()) return;
if (!user.hasPermission()) return;
if (!data.isValid()) return;
if (cache.has(key)) return;

// Process...
```

### Extract Helper Functions

Break complex functions into smaller, named pieces:

✅ **Clear intent**:
```cpp
bool canProcessRequest(const User& user, const Data& data) {
    return user.isAuthenticated()
        && user.hasPermission()
        && data.isValid();
}

void processRequest() {
    if (!canProcessRequest(user, data)) return;
    // Process...
}
```

## Avoid Magic Numbers

Replace hard-coded values with named constants.

❌ **Magic numbers**:
```cpp
if (retryCount > 3) return;
sleep(5000);
buffer.resize(1024);
```

✅ **Named constants**:
```cpp
const int MAX_RETRY_COUNT = 3;
const int RETRY_DELAY_MS = 5000;
const int BUFFER_SIZE_BYTES = 1024;

if (retryCount > MAX_RETRY_COUNT) return;
sleep(RETRY_DELAY_MS);
buffer.resize(BUFFER_SIZE_BYTES);
```

## Error Logging

When catching exceptions, include sufficient context for debugging.

❌ **Insufficient context**:
```cpp
catch (const Exception& e) {
    log("Error occurred");
}
```

✅ **Rich context**:
```cpp
catch (const Exception& e) {
    log("Failed to process user request",
        "user_id", user.id,
        "request_type", req.type,
        "error", e.what(),
        "retry_count", retryCount);
}
```

## Prefer Immutability

Use immutable data structures where practical to minimize side effects.

✅ **Immutability in C++**:
```cpp
const auto result = processData(input);  // const prevents modification
```

✅ **Immutability in Kotlin**:
```kotlin
val result = processData(input)  // val instead of var
```

✅ **Immutability in Python**:
```python
from typing import Final
RESULT: Final = process_data(input)  # Final for constants
```

## Regular Refactoring

### Refactoring Cadence

- **During development**: Refactor as you notice code smells
- **Before features**: Clean up related code before adding new features
- **Dedicated time**: Schedule regular refactoring sessions

### Refactoring Checklist

- [ ] Run full test suite before refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Commit working state frequently
- [ ] Document non-obvious refactorings

### Common Refactorings

- **Extract Method**: Pull complex code into separate functions
- **Rename**: Improve names for clarity
- **Consolidate Conditional**: Simplify complex if-statements
- **Replace Temp with Query**: Replace temporary variables with function calls
- **Remove Dead Code**: Delete unused code

## Code Review Focus Areas

When reviewing code, check for:

- [ ] Single responsibility adherence
- [ ] Appropriate function/class sizes
- [ ] Clear, descriptive naming
- [ ] No magic numbers
- [ ] Sufficient error context
- [ ] Test coverage for changes
- [ ] Documentation for public APIs
