# Error Handling - @ControllerAdvice and ProblemDetail

Centralized error handling using Spring's `@ControllerAdvice` with RFC 7807 `ProblemDetail`
responses.

## Global Exception Handler

Create a `@RestControllerAdvice` to handle exceptions globally:

```kotlin
// infrastructure/http/ResumeExceptionHandler.kt
@RestControllerAdvice("com.cvix.resume")  // Scope to package
class ResumeExceptionHandler(
    private val messageSource: MessageSource,
) {
    private val logger = LoggerFactory.getLogger(ResumeExceptionHandler::class.java)

    /**
     * Handle validation errors from @Valid
     */
    @ExceptionHandler(WebExchangeBindException::class)
    fun handleValidationException(
        ex: WebExchangeBindException,
        exchange: ServerWebExchange,
    ): ProblemDetail {
        val fieldErrors = ex.fieldErrors.map { error ->
            mapOf(
                "field" to error.field,
                "message" to (error.defaultMessage ?: "Invalid value"),
            )
        }

        val problemDetail = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST,
            "Request validation failed. Please check field errors.",
        )
        problemDetail.title = "Validation Error"
        problemDetail.type = URI.create("https://example.com/errors/validation")
        problemDetail.setProperty("errorCategory", "VALIDATION")
        problemDetail.setProperty("timestamp", Instant.now())
        problemDetail.setProperty("fieldErrors", fieldErrors)
        problemDetail.setProperty("traceId", exchange.request.id)

        logger.warn("Validation error: {} fields failed", fieldErrors.size)
        return problemDetail
    }

    /**
     * Handle domain-specific exceptions
     */
    @ExceptionHandler(InvalidResumeDataException::class)
    fun handleInvalidResumeDataException(
        ex: InvalidResumeDataException,
        exchange: ServerWebExchange,
    ): ProblemDetail {
        val localizedMessage = getLocalizedMessage(exchange, "resume.error.invalid_data")

        val problemDetail = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST,
            ex.message ?: "Resume data validation failed",
        )
        problemDetail.title = "Invalid Resume Data"
        problemDetail.type = URI.create("https://example.com/errors/resume/invalid-data")
        problemDetail.setProperty("errorCategory", "INVALID_RESUME_DATA")
        problemDetail.setProperty("timestamp", Instant.now())
        problemDetail.setProperty("localizedMessage", localizedMessage)
        problemDetail.setProperty("traceId", exchange.request.id)

        logger.warn("Invalid resume data: {}", ex.message)
        return problemDetail
    }

    /**
     * Catch-all for unexpected errors
     */
    @ExceptionHandler(Exception::class)
    fun handleGenericException(
        ex: Exception,
        exchange: ServerWebExchange,
    ): ProblemDetail {
        val problemDetail = ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again later.",
        )
        problemDetail.title = "Internal Server Error"
        problemDetail.type = URI.create("https://example.com/errors/internal")
        problemDetail.setProperty("errorCategory", "INTERNAL_ERROR")
        problemDetail.setProperty("timestamp", Instant.now())
        problemDetail.setProperty("traceId", exchange.request.id)

        logger.error("Unexpected error: {}", ex.message, ex)
        return problemDetail
    }

    private fun getLocalizedMessage(exchange: ServerWebExchange, key: String): String {
        val locale = exchange.localeContext.locale ?: Locale.getDefault()
        return messageSource.getMessage(key, null, locale)
    }
}
```

## ProblemDetail Structure

RFC 7807 standard fields:

| Field      | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `type`     | URI    | Yes      | URI reference identifying error type |
| `title`    | String | Yes      | Short summary of the problem         |
| `status`   | Int    | Yes      | HTTP status code                     |
| `detail`   | String | No       | Human-readable explanation           |
| `instance` | URI    | No       | URI reference to specific occurrence |

Custom properties via `setProperty()`:

```kotlin
problemDetail.setProperty("errorCategory", "VALIDATION")
problemDetail.setProperty("timestamp", Instant.now())
problemDetail.setProperty("traceId", exchange.request.id)
problemDetail.setProperty("fieldErrors", listOf(...))
problemDetail.setProperty("localizedMessage", "...")
```

## Exception to HTTP Status Mapping

| Exception Type             | HTTP Status               | Use Case                     |
|----------------------------|---------------------------|------------------------------|
| `NotFoundException`        | 404 Not Found             | Resource doesn't exist       |
| `ConflictException`        | 409 Conflict              | Duplicate, state conflict    |
| `ValidationException`      | 400 Bad Request           | Invalid input data           |
| `WebExchangeBindException` | 400 Bad Request           | @Valid failures              |
| `UnauthorizedException`    | 401 Unauthorized          | Missing/invalid auth         |
| `ForbiddenException`       | 403 Forbidden             | Insufficient permissions     |
| `UnprocessableException`   | 422 Unprocessable Entity  | Valid syntax, semantic error |
| `TimeoutException`         | 504 Gateway Timeout       | Downstream service timeout   |
| `Exception` (generic)      | 500 Internal Server Error | Unexpected errors            |

## Scoped Exception Handlers

Scope handlers to specific packages or controllers:

```kotlin
// Global handler for all controllers
@RestControllerAdvice
class GlobalExceptionHandler { ... }

// Scoped to resume package only
@RestControllerAdvice("com.cvix.resume")
class ResumeExceptionHandler { ... }

// Scoped to specific controllers
@RestControllerAdvice(assignableTypes = [UserController::class, AdminController::class])
class UserExceptionHandler { ... }
```

## Logging Best Practices

```kotlin
@ExceptionHandler(NotFoundException::class)
fun handleNotFound(ex: NotFoundException): ProblemDetail {
    // DEBUG for expected client errors (no stack trace)
    logger.debug("Resource not found: {}", ex.message)
    return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.message ?: "Not found")
}

@ExceptionHandler(ConflictException::class)
fun handleConflict(ex: ConflictException): ProblemDetail {
    // WARN for business rule violations
    logger.warn("Conflict: {}", ex.message)
    return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.message ?: "Conflict")
}

@ExceptionHandler(Exception::class)
fun handleGeneric(ex: Exception): ProblemDetail {
    // ERROR with stack trace for unexpected errors
    logger.error("Unexpected error: {}", ex.message, ex)
    return ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR)
}
```

## Localized Error Messages

Use `MessageSource` for i18n:

```kotlin
// messages.properties
resume.error.invalid_data = Resume data is invalid
        resume.error.not_found = Resume not found

// messages_es.properties
resume.error.invalid_data = Los datos del currículum son inválidos
        resume.error.not_found = Currículum no encontrado
```

```kotlin
private fun getLocalizedMessage(exchange: ServerWebExchange, key: String): String {
    val locale = exchange.localeContext.locale ?: Locale.getDefault()
    return messageSource.getMessage(key, null, locale)
}
```

## Domain Exceptions

Define domain exceptions in the domain layer (no Spring imports):

```kotlin
// domain/exception/ResumeException.kt
sealed class ResumeException(message: String) : RuntimeException(message)

class ResumeNotFoundException(id: String) : ResumeException("Resume not found: $id")
class InvalidResumeDataException(message: String) : ResumeException(message)
class ResumeGenerationException(message: String) : ResumeException(message)
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Catching exceptions in controller
@PostMapping
suspend fun create(@RequestBody request: CreateRequest): ResponseEntity<*> {
    return try {
        val result = service.create(request)
        ResponseEntity.ok(result)
    } catch (e: ConflictException) {
        ResponseEntity.status(HttpStatus.CONFLICT).body(mapOf("error" to e.message))
    }
}

// ✅ CORRECT: Let @ControllerAdvice handle it
@PostMapping
suspend fun create(@RequestBody request: CreateRequest): ResponseEntity<Response> {
    val result = service.create(request)  // Throws ConflictException
    return ResponseEntity.ok(result)
}

// ❌ WRONG: Returning raw exception message
@ExceptionHandler(Exception::class)
fun handleException(ex: Exception): ProblemDetail {
    return ProblemDetail.forStatusAndDetail(
        HttpStatus.INTERNAL_SERVER_ERROR,
        ex.message ?: "Error"  // May leak internal details!
    )
}

// ✅ CORRECT: Use generic message for unexpected errors
@ExceptionHandler(Exception::class)
fun handleException(ex: Exception): ProblemDetail {
    logger.error("Unexpected error", ex)  // Log full details
    return ProblemDetail.forStatusAndDetail(
        HttpStatus.INTERNAL_SERVER_ERROR,
        "An unexpected error occurred"  // Generic message
    )
}
```

## Related References

- [controllers.md](./controllers.md) - Controllers that delegate error handling
- [swagger-standard.md](./swagger-standard.md) - Documenting error responses
