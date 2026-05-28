# Exception Handling Example

This example demonstrates global exception handling with @ControllerAdvice and custom exceptions.

## Files

### GlobalExceptionHandler.java
```java
package com.example.demo.exception;

import com.example.demo.dto.ErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.NoHandlerFoundException;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(
        ResourceNotFoundException ex,
        HttpServletRequest request
    ) {
        logger.error("Resource not found: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateResource(
        DuplicateResourceException ex,
        HttpServletRequest request
    ) {
        logger.error("Duplicate resource: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.CONFLICT.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
        BusinessException ex,
        HttpServletRequest request
    ) {
        logger.warn("Business exception: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.UNPROCESSABLE_ENTITY.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.unprocessableEntity().body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
        MethodArgumentNotValidException ex,
        HttpServletRequest request
    ) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult().getFieldErrors().forEach(error -> {
            String fieldName = error.getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        logger.error("Validation failed: {}", errors);

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .validationErrors(errors)
            .build();

        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(NoHandlerFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
        NoHandlerFoundException ex,
        HttpServletRequest request
    ) {
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .message("Endpoint not found: " + ex.getRequestURL())
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
        Exception ex,
        HttpServletRequest request
    ) {
        logger.error("Unexpected error occurred", ex);

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .message("An unexpected error occurred")
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### Custom Exceptions

#### BaseException.java
```java
package com.example.demo.exception;

public abstract class BaseException extends RuntimeException {
    public BaseException(String message) {
        super(message);
    }

    public BaseException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

#### ResourceNotFoundException.java
```java
package com.example.demo.exception;

public class ResourceNotFoundException extends BaseException {

    public ResourceNotFoundException(String resource, Long id) {
        super(String.format("%s not found with id: %s", resource, id));
    }

    public ResourceNotFoundException(String resource, String field, String value) {
        super(String.format("%s not found with %s: %s", resource, field, value));
    }

    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

#### DuplicateResourceException.java
```java
package com.example.demo.exception;

public class DuplicateResourceException extends BaseException {

    public DuplicateResourceException(String resource, String field, String value) {
        super(String.format("%s already exists with %s: %s", resource, field, value));
    }

    public DuplicateResourceException(String message) {
        super(message);
    }
}
```

#### BusinessException.java
```java
package com.example.demo.exception;

public class BusinessException extends BaseException {

    public BusinessException(String message) {
        super(message);
    }

    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### ErrorResponse.java
```java
package com.example.demo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Map;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    private int status;
    private String message;
    private LocalDateTime timestamp;
    private String path;
    private Map<String, String> validationErrors;
}
```

## Usage Example

### In Service Layer

```java
@Service
public class UserService {

    private final UserRepository userRepository;

    public UserDTO findById(Long id) {
        return userRepository.findById(id)
            .map(UserMapper::toDTO)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    public UserDTO create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }

        // Additional business validation
        if (request.getAge() != null && request.getAge() < 18) {
            throw new BusinessException("User must be at least 18 years old");
        }

        // Create user...
    }
}
```

## Example Error Responses

### Resource Not Found (404)

**Request:**
```
GET /api/users/999
```

**Response:**
```json
{
  "status": 404,
  "message": "User not found with id: 999",
  "timestamp": "2025-01-15T10:30:00",
  "path": "/api/users/999"
}
```

### Validation Error (400)

**Request:**
```
POST /api/users
{
  "email": "invalid-email",
  "password": "123"
}
```

**Response:**
```json
{
  "status": 400,
  "message": "Validation failed",
  "timestamp": "2025-01-15T10:30:00",
  "path": "/api/users",
  "validationErrors": {
    "email": "Email must be valid",
    "password": "Password must be at least 8 characters",
    "firstName": "First name is required"
  }
}
```

### Duplicate Resource (409)

**Request:**
```
POST /api/users
{
  "email": "existing@example.com"
}
```

**Response:**
```json
{
  "status": 409,
  "message": "User already exists with email: existing@example.com",
  "timestamp": "2025-01-15T10:30:00",
  "path": "/api/users"
}
```

### Business Exception (422)

**Response:**
```json
{
  "status": 422,
  "message": "User must be at least 18 years old",
  "timestamp": "2025-01-15T10:30:00",
  "path": "/api/users"
}
```

### Internal Server Error (500)

**Response:**
```json
{
  "status": 500,
  "message": "An unexpected error occurred",
  "timestamp": "2025-01-15T10:30:00",
  "path": "/api/users"
}
```

## Testing Exception Handling

```java
@SpringBootTest
@AutoConfigureMockMvc
class ExceptionHandlingTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void whenUserNotFound_ShouldReturn404() throws Exception {
        mockMvc.perform(get("/api/users/999"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.status").value(404))
            .andExpect(jsonPath("$.message").value("User not found with id: 999"))
            .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    void whenValidationFails_ShouldReturn400() throws Exception {
        String invalidJson = "{\"email\":\"invalid\",\"password\":\"123\"}";

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidJson))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.message").value("Validation failed"))
            .andExpect(jsonPath("$.validationErrors").exists());
    }
}
```

## Key Points

1. **@ControllerAdvice** - Handles exceptions globally
2. **Custom exceptions** - Type-safe exception handling
3. **Consistent error format** - Standardized ErrorResponse
4. **Proper HTTP status codes** - 404, 400, 409, 422, 500
5. **Logging** - Log errors appropriately
6. **No stack traces to clients** - Security best practice
