# Java Error Handling Patterns

## Table of Contents

1. [Exception Basics](#exception-basics)
2. [Checked vs Unchecked Exceptions](#checked-vs-unchecked-exceptions)
3. [Custom Exception Classes](#custom-exception-classes)
4. [Try-Catch-Finally](#try-catch-finally)
5. [Try-with-Resources](#try-with-resources)
6. [Multi-Catch](#multi-catch)
7. [Exception Chaining](#exception-chaining)
8. [Spring Boot Error Handling](#spring-boot-error-handling)

## Exception Basics

### Exception Hierarchy

```
Throwable
├── Error (unchecked - JVM errors, don't catch)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── ...
└── Exception
    ├── RuntimeException (unchecked)
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   ├── IndexOutOfBoundsException
    │   └── ...
    └── Checked Exceptions
        ├── IOException
        ├── SQLException
        ├── ClassNotFoundException
        └── ...
```

### Basic Try-Catch

```java
public String readFile(String path) {
    try {
        return Files.readString(Paths.get(path));
    } catch (IOException e) {
        logger.error("Failed to read file: " + path, e);
        throw new RuntimeException("Unable to read file", e);
    }
}
```

## Checked vs Unchecked Exceptions

### Checked Exceptions

Checked exceptions must be either caught or declared in the method signature.

```java
// Must declare throws
public String readFile(String path) throws IOException {
    return Files.readString(Paths.get(path));
}

// Or catch it
public String readFile(String path) {
    try {
        return Files.readString(Paths.get(path));
    } catch (IOException e) {
        logger.error("Failed to read file", e);
        return "";
    }
}

// Caller must handle
public void processFile() {
    try {
        String content = readFile("data.txt");
    } catch (IOException e) {
        // Handle error
    }
}
```

### Unchecked Exceptions (Runtime Exceptions)

Unchecked exceptions don't need to be declared or caught.

```java
public void validateAge(int age) {
    if (age < 0) {
        // No need to declare this
        throw new IllegalArgumentException("Age cannot be negative");
    }
    if (age < 18) {
        throw new BusinessRuleException("Must be at least 18");
    }
}

// Caller can optionally catch
public void registerUser(User user) {
    try {
        validateAge(user.getAge());
    } catch (IllegalArgumentException e) {
        logger.warn("Invalid age: " + user.getAge());
        // Handle gracefully
    }
}
```

### When to Use Which

**Use Checked Exceptions:**
- Recoverable conditions
- Expected errors (file not found, network timeout)
- Caller should be forced to handle
- External I/O operations

**Use Unchecked Exceptions:**
- Programming errors (null pointer, illegal state)
- Unrecoverable conditions
- Caller shouldn't be forced to handle
- Business rule violations

```java
// Checked: Caller should handle file not existing
public Config readConfig(String path) throws FileNotFoundException {
    File file = new File(path);
    if (!file.exists()) {
        throw new FileNotFoundException("Config file not found: " + path);
    }
    // Read and return config
}

// Unchecked: Programming error
public User getUserById(Long id) {
    if (id == null) {
        throw new IllegalArgumentException("User ID cannot be null");
    }
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}
```

## Custom Exception Classes

### Basic Custom Exception

```java
public class ApplicationException extends RuntimeException {
    private final String code;
    private final int statusCode;

    public ApplicationException(String message, String code, int statusCode) {
        super(message);
        this.code = code;
        this.statusCode = statusCode;
    }

    public ApplicationException(String message, String code, int statusCode, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.statusCode = statusCode;
    }

    public String getCode() {
        return code;
    }

    public int getStatusCode() {
        return statusCode;
    }
}
```

### Exception Hierarchy

```java
// Base exception
public class ApplicationException extends RuntimeException {
    private final String code;
    private final int statusCode;

    public ApplicationException(String message, String code, int statusCode) {
        super(message);
        this.code = code;
        this.statusCode = statusCode;
    }

    public ApplicationException(String message, String code, int statusCode, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.statusCode = statusCode;
    }

    public String getCode() {
        return code;
    }

    public int getStatusCode() {
        return statusCode;
    }
}

// Validation exception
public class ValidationException extends ApplicationException {
    private final Map<String, String> fieldErrors;

    public ValidationException(String message, Map<String, String> fieldErrors) {
        super(message, "VALIDATION_ERROR", 400);
        this.fieldErrors = fieldErrors;
    }

    public Map<String, String> getFieldErrors() {
        return fieldErrors;
    }
}

// Not found exception
public class NotFoundException extends ApplicationException {
    public NotFoundException(String resource, String identifier) {
        super(
            String.format("%s not found: %s", resource, identifier),
            "NOT_FOUND",
            404
        );
    }
}

// Authentication exception
public class AuthenticationException extends ApplicationException {
    public AuthenticationException(String message) {
        super(message, "AUTHENTICATION_ERROR", 401);
    }
}

// Business rule exception
public class BusinessRuleException extends ApplicationException {
    public BusinessRuleException(String message, String code) {
        super(message, code, 422);
    }
}

// Database exception
public class DatabaseException extends ApplicationException {
    public DatabaseException(String operation, Throwable cause) {
        super(
            "Database operation failed: " + operation,
            "DATABASE_ERROR",
            503,
            cause
        );
    }
}

// Usage
throw new ValidationException("Invalid input", Map.of(
    "email", "Invalid email format",
    "age", "Must be at least 18"
));

throw new NotFoundException("User", userId);

throw new AuthenticationException("Invalid credentials");

throw new BusinessRuleException(
    "Cannot delete order with pending shipment",
    "ORDER_HAS_PENDING_SHIPMENT"
);
```

## Try-Catch-Finally

### Basic Structure

```java
public void processFile(String path) {
    FileInputStream fis = null;
    try {
        fis = new FileInputStream(path);
        // Process file
        byte[] data = new byte[fis.available()];
        fis.read(data);
        process(data);
    } catch (FileNotFoundException e) {
        logger.error("File not found: " + path, e);
        throw new NotFoundException("File", path);
    } catch (IOException e) {
        logger.error("Failed to read file: " + path, e);
        throw new ApplicationException("File read failed", "IO_ERROR", 500, e);
    } finally {
        // Always executes
        if (fis != null) {
            try {
                fis.close();
            } catch (IOException e) {
                logger.error("Failed to close file", e);
            }
        }
    }
}
```

### Return in Finally

```java
public int calculate() {
    try {
        return riskyCalculation();
    } catch (Exception e) {
        logger.error("Calculation failed", e);
        return -1;
    } finally {
        // This runs after return value is determined
        cleanup();
    }
}

// ⚠️ Warning: Finally can override return value
public int badExample() {
    try {
        return 1;
    } finally {
        return 2;  // ❌ This overrides the return value - confusing!
    }
}
```

## Try-with-Resources

### Basic Usage

```java
// Automatically closes resources that implement AutoCloseable
public String readFile(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.lines().collect(Collectors.joining("\n"));
    }
    // reader is automatically closed here, even if exception occurs
}
```

### Multiple Resources

```java
public void copyFile(String source, String destination) throws IOException {
    try (
        InputStream in = new FileInputStream(source);
        OutputStream out = new FileOutputStream(destination)
    ) {
        byte[] buffer = new byte[1024];
        int length;
        while ((length = in.read(buffer)) > 0) {
            out.write(buffer, 0, length);
        }
    }
    // Both streams automatically closed in reverse order
}
```

### Try-with-Resources and Catch

```java
public String readFileWithDefault(String path) {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.lines().collect(Collectors.joining("\n"));
    } catch (IOException e) {
        logger.warn("Failed to read file, using default", e);
        return "default content";
    }
}
```

### Custom AutoCloseable

```java
public class DatabaseTransaction implements AutoCloseable {
    private final Connection connection;
    private boolean committed = false;

    public DatabaseTransaction(Connection connection) throws SQLException {
        this.connection = connection;
        this.connection.setAutoCommit(false);
    }

    public void commit() throws SQLException {
        connection.commit();
        committed = true;
    }

    @Override
    public void close() throws SQLException {
        if (!committed) {
            connection.rollback();
        }
        connection.setAutoCommit(true);
    }
}

// Usage
try (DatabaseTransaction tx = new DatabaseTransaction(connection)) {
    // Perform database operations
    performOperations();
    tx.commit();
}
// Automatically rolls back if commit wasn't called
```

## Multi-Catch

### Catching Multiple Exception Types

```java
public void processData(String data) {
    try {
        validate(data);
        parse(data);
        save(data);
    } catch (ValidationException | ParseException e) {
        // Handle both types the same way
        logger.error("Failed to process data", e);
        throw new ApplicationException("Data processing failed", "PROCESSING_ERROR", 400, e);
    } catch (DatabaseException e) {
        // Handle database errors differently
        logger.error("Database error", e);
        throw new ApplicationException("Database error", "DATABASE_ERROR", 503, e);
    }
}
```

### Catching Exception Hierarchy

```java
public void processUser(User user) {
    try {
        validateUser(user);
        saveUser(user);
        sendNotification(user);
    } catch (ValidationException e) {
        // Specific validation handling
        logger.warn("Validation failed: " + e.getFieldErrors());
        throw e;
    } catch (ApplicationException e) {
        // Other application exceptions
        logger.error("Application error", e);
        throw e;
    } catch (Exception e) {
        // Unexpected exceptions
        logger.error("Unexpected error", e);
        throw new ApplicationException("Unexpected error", "INTERNAL_ERROR", 500, e);
    }
}
```

## Exception Chaining

### Basic Chaining

```java
public User fetchUser(Long id) {
    try {
        return userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("User", id.toString()));
    } catch (DatabaseException e) {
        // Chain exceptions to preserve original cause
        throw new ApplicationException(
            "Failed to fetch user " + id,
            "USER_FETCH_ERROR",
            503,
            e  // Original exception as cause
        );
    }
}

// Access the cause
try {
    fetchUser(123L);
} catch (ApplicationException e) {
    logger.error("Error: " + e.getMessage());
    Throwable cause = e.getCause();
    if (cause != null) {
        logger.error("Caused by: " + cause.getMessage());
    }
}
```

### Suppressed Exceptions

```java
public void processWithMultipleResources() {
    try (
        Resource1 r1 = new Resource1();
        Resource2 r2 = new Resource2()
    ) {
        r1.use();
        r2.use();
    } catch (Exception e) {
        // If both r1.close() and r2.close() throw exceptions,
        // one becomes the main exception, others are suppressed
        logger.error("Main exception: " + e.getMessage());

        for (Throwable suppressed : e.getSuppressed()) {
            logger.error("Suppressed: " + suppressed.getMessage());
        }

        throw e;
    }
}
```

## Spring Boot Error Handling

### Global Exception Handler

```java
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFoundException(
        NotFoundException ex,
        WebRequest request
    ) {
        logger.error("Resource not found", ex);

        ErrorResponse error = new ErrorResponse(
            ex.getCode(),
            ex.getMessage(),
            HttpStatus.NOT_FOUND.value()
        );

        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
        ValidationException ex,
        WebRequest request
    ) {
        logger.warn("Validation failed", ex);

        ErrorResponse error = new ErrorResponse(
            ex.getCode(),
            ex.getMessage(),
            HttpStatus.BAD_REQUEST.value(),
            ex.getFieldErrors()
        );

        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ErrorResponse> handleApplicationException(
        ApplicationException ex,
        WebRequest request
    ) {
        logger.error("Application error", ex);

        ErrorResponse error = new ErrorResponse(
            ex.getCode(),
            ex.getMessage(),
            ex.getStatusCode()
        );

        return new ResponseEntity<>(error, HttpStatus.valueOf(ex.getStatusCode()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
        Exception ex,
        WebRequest request
    ) {
        logger.error("Unexpected error", ex);

        ErrorResponse error = new ErrorResponse(
            "INTERNAL_ERROR",
            "An unexpected error occurred",
            HttpStatus.INTERNAL_SERVER_ERROR.value()
        );

        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}

// Error response DTO
public class ErrorResponse {
    private String code;
    private String message;
    private int statusCode;
    private Map<String, String> fieldErrors;
    private String timestamp;

    public ErrorResponse(String code, String message, int statusCode) {
        this.code = code;
        this.message = message;
        this.statusCode = statusCode;
        this.timestamp = Instant.now().toString();
    }

    public ErrorResponse(String code, String message, int statusCode, Map<String, String> fieldErrors) {
        this(code, message, statusCode);
        this.fieldErrors = fieldErrors;
    }

    // Getters and setters
}
```

### Method-Level Exception Handling

```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.getUser(id);
        return ResponseEntity.ok(user);
    }

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException ex) {
        // This overrides global handler for this controller
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getCode(), ex.getMessage(), 404));
    }
}
```

### Bean Validation with Exception Handling

```java
import javax.validation.Valid;
import org.springframework.validation.BindingResult;

@RestController
@RequestMapping("/users")
public class UserController {

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest request) {
        // @Valid automatically validates and throws MethodArgumentNotValidException
        User user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}

// Global handler for validation
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
        MethodArgumentNotValidException ex
    ) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult().getFieldErrors().forEach(error -> {
            errors.put(error.getField(), error.getDefaultMessage());
        });

        ErrorResponse response = new ErrorResponse(
            "VALIDATION_ERROR",
            "Validation failed",
            400,
            errors
        );

        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }
}
```

### Async Exception Handling

```java
@Service
public class UserService {

    @Async
    public CompletableFuture<User> fetchUserAsync(Long id) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return userRepository.findById(id)
                    .orElseThrow(() -> new NotFoundException("User", id.toString()));
            } catch (Exception e) {
                logger.error("Async fetch failed", e);
                throw new CompletionException(e);
            }
        });
    }
}

// Usage
userService.fetchUserAsync(123L)
    .thenAccept(user -> logger.info("Found user: " + user))
    .exceptionally(ex -> {
        logger.error("Failed to fetch user", ex);
        return null;
    });
```

## Best Practices

### 1. Catch Specific Exceptions

```java
// ✅ Good: Catch specific exceptions
try {
    processData();
} catch (ValidationException e) {
    handleValidation(e);
} catch (DatabaseException e) {
    handleDatabase(e);
}

// ❌ Bad: Catching Exception hides specific errors
try {
    processData();
} catch (Exception e) {
    // Which error? Can't tell
    handleError(e);
}
```

### 2. Don't Swallow Exceptions

```java
// ❌ Bad: Silent failure
try {
    riskyOperation();
} catch (Exception e) {
    // Error is lost
}

// ✅ Good: Log or re-throw
try {
    riskyOperation();
} catch (Exception e) {
    logger.error("Operation failed", e);
    throw new ApplicationException("Operation failed", "OP_ERROR", 500, e);
}
```

### 3. Close Resources Properly

```java
// ❌ Bad: Manual closing
FileInputStream fis = null;
try {
    fis = new FileInputStream("file.txt");
    // use fis
} finally {
    if (fis != null) {
        fis.close();
    }
}

// ✅ Good: Try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // use fis
}
```

### 4. Provide Context

```java
// ❌ Bad: Generic message
throw new RuntimeException("Error");

// ✅ Good: Descriptive message with context
throw new ApplicationException(
    String.format("Failed to process user %s: invalid email format", userId),
    "INVALID_EMAIL",
    400
);
```

### 5. Don't Use Exceptions for Control Flow

```java
// ❌ Bad: Using exceptions for control flow
try {
    User user = findUserOrThrow(id);
    // process user
} catch (NotFoundException e) {
    // Create new user
    user = createUser(id);
}

// ✅ Good: Use Optional or boolean checks
Optional<User> userOpt = findUser(id);
User user = userOpt.orElseGet(() -> createUser(id));
```

### 6. Log Before Re-throwing

```java
public void processUser(Long id) {
    try {
        User user = fetchUser(id);
        validate(user);
        save(user);
    } catch (ValidationException e) {
        // Log with context before re-throwing
        logger.error("User validation failed for id: " + id, e);
        throw e;
    }
}
```

### 7. Use Custom Exceptions for Domain Logic

```java
// ✅ Good: Domain-specific exception
public class InsufficientFundsException extends BusinessRuleException {
    public InsufficientFundsException(BigDecimal balance, BigDecimal required) {
        super(
            String.format("Insufficient funds: balance %.2f, required %.2f", balance, required),
            "INSUFFICIENT_FUNDS"
        );
    }
}

// Makes code more readable
if (account.getBalance().compareTo(amount) < 0) {
    throw new InsufficientFundsException(account.getBalance(), amount);
}
```

## Summary

1. **Use checked exceptions** for recoverable conditions
2. **Use unchecked exceptions** for programming errors
3. **Always close resources** with try-with-resources
4. **Catch specific exceptions** instead of generic Exception
5. **Chain exceptions** to preserve error context
6. **Never swallow exceptions** without logging
7. **Provide context** in error messages
8. **Use @ControllerAdvice** for global error handling in Spring
9. **Log at appropriate levels** (error, warn, info, debug)
10. **Test error paths** thoroughly
