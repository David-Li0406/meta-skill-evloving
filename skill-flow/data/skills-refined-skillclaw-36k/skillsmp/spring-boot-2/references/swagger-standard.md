# Swagger Documentation Standard

This document defines the mandatory standard for documenting all REST controllers in the CVIX
project.

## Standard based on

- `ContactController` - Best example of complete documentation
- `WaitlistController` - Second best example

## Mandatory Structure

### 1. Controller Class

```kotlin
/**
 * Controller for [feature description].
 *
 * [Detailed description of what this controller does, its purpose, and any special considerations]
 *
 * Uses header-based API versioning (API-Version: v1).
 *
 * ## Security Features: (if applicable)
 * - [Security feature 1]
 * - [Security feature 2]
 *
 * ## Special Notes: (if applicable)
 * - [Note 1]
 * - [Note 2]
 *
 * @property mediator The mediator for dispatching commands.
 * @property [otherProperty] Description of other injected properties.
 * @created [date] (optional, for historical tracking)
 */
@Validated  // If using Jakarta validation
@RestController
@RequestMapping(value = ["/api/[resource]"])
@Tag(
    name = "[Resource Name]",
    description = "[Resource] management endpoints"
)
class [Resource]Controller(
private val mediator: Mediator,
// other dependencies
) : ApiController(mediator) {
    // ...
}
```

### 2. Endpoint Method

```kotlin
/**
 * Endpoint for [operation description].
 *
 * [Detailed explanation of what this endpoint does, including:]
 * - Input validation rules
 * - Business logic flow
 * - Side effects
 * - Special considerations
 *
 * @param [param1] Description of parameter 1.
 * @param [param2] Description of parameter 2.
 * @return ResponseEntity with [success response type] or error response.
 */
@Operation(
    summary = "[Short action description]",
    description = "[Detailed description of what this operation does, including business logic and validation]",
)
@ApiResponses(
    value = [
        ApiResponse(
            responseCode = "200",  // or 201 for creation
            description = "[Success description]",
            content = [Content(schema = Schema(implementation = [SuccessResponse]::class))],
        ),
        ApiResponse(
            responseCode = "400",
            description = "[What causes a 400 error]",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "401",
            description = "Unauthorized - Authentication required",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "403",
            description = "Forbidden - Insufficient permissions",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "404",
            description = "Resource not found",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "409",
            description = "[What causes a conflict]",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "429",
            description = "Rate limit exceeded",
            headers = [Header(
                name = "Retry-After",
                description = "Seconds until rate limit resets"
            )],
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "500",
            description = "Internal server error",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
    ],
)
@SecurityRequirement(name = "bearerAuth")  // If endpoint requires authentication
@[HttpMethod]Mapping(
    produces = ["application/vnd.api.v1+json"],
    consumes = ["application/json"],  // If endpoint accepts body
)
suspend fun [operationName](
@Valid @RequestBody request: [Request],
// other params
): ResponseEntity<[Response]> {
    // implementation
}
```

### 3. Request DTOs

**ALL** request DTOs MUST have:

```kotlin
/**
 * Request body for [operation description].
 *
 * [Detailed description of the purpose and usage]
 *
 * @property [field1] Description including constraints and examples.
 * @property [field2] Description including constraints and examples.
 */
data class [Operation]Request(
@field:NotBlank(message = "[Field] is required")
@field:Size(min = X, max = Y, message = "[Field] must be between X and Y characters")
@field:Schema(
    description = "[Detailed field description]",
    example = "[realistic example value]",
    required = true,  // or false
    minLength = X,     // if applicable
    maxLength = Y,     // if applicable
)
val [field]: String,

@field:Email(message = "Email must be valid")
@field:NotBlank(message = "Email is required")
@field:Schema(
    description = "User's email address",
    example = "user@example.com",
    required = true,
    format = "email",
)
val email: String,

@field:Pattern(regexp = "^[regex]$", message = "[Constraint description]")
@field:Schema(
    description = "[Field description]",
    example = "[example]",
    allowableValues = ["value1", "value2"],  // if enum-like
    required = true,
)
val [enumField]: String,
)
```

### 4. Response DTOs

```kotlin
/**
 * Response for [operation description].
 *
 * [Detailed description of when this response is returned]
 *
 * @property success Whether the operation succeeded.
 * @property message Localized message describing the result.
 * @property data Optional data payload.
 */
@Schema(description = "[Operation] success response")
data class [Operation]Response(
@field:Schema(
    description = "Operation success indicator",
    example = "true",
)
val success: Boolean,

@field:Schema(
    description = "Localized message describing the result",
    example = "Operation completed successfully",
)
val message: String,

@field:Schema(
    description = "[Optional data description]",
    nullable = true,
)
val data: [DataType]? = null,
)
```

## Standard HTTP Codes

| Code | Usage                 | When to use                                          |
|------|-----------------------|------------------------------------------------------|
| 200  | OK                    | Successful GET/PATCH/DELETE                          |
| 201  | Created               | Successful POST/PUT that creates resources           |
| 400  | Bad Request           | Validation failed, invalid data                      |
| 401  | Unauthorized          | Missing or invalid token                             |
| 403  | Forbidden             | Valid token but insufficient permissions             |
| 404  | Not Found             | Resource does not exist                              |
| 409  | Conflict              | Duplicate email, invalid state, constraint violation |
| 429  | Too Many Requests     | Rate limit exceeded                                  |
| 500  | Internal Server Error | Unexpected server error                              |

## Standard Content Types

- **Produces**: `application/vnd.api.v1+json` (versioned API)
- **Consumes**: `application/json`

## Security Annotations

For endpoints that require authentication:

```kotlin
@Operation(
    summary = "...",
    security = [SecurityRequirement(name = "bearerAuth")],
)
```

## Validation Annotations

### String Fields

- `@NotBlank` - Not null, empty, or only whitespace
- `@Size(min, max)` - String length
- `@Email` - Valid email format
- `@Pattern(regexp)` - Custom regex

### Numeric Fields

- `@NotNull` - Not null
- `@Min(value)` - Minimum value
- `@Max(value)` - Maximum value
- `@Positive` / `@PositiveOrZero`

### Collections

- `@NotEmpty` - Not null and not empty
- `@Size(min, max)` - Collection size

## Best Practices

1. **KDoc first, Swagger second**: Document in KDoc, then in Swagger annotations
2. **Realistic examples**: Use examples that represent real data
3. **Complete descriptions**: Explain the "why", not just the "what"
4. **All HTTP codes**: Document ALL possible responses
5. **Localization**: Use `MessageSource` for localized messages
6. **Logging**: Log at INFO for successful operations, WARN for business errors, ERROR for technical
   failures
7. **Content Schema**: ALWAYS specify `Content(schema = Schema(implementation = ...))`
8. **ProblemDetail**: Use Spring's `ProblemDetail` for error responses
9. **Headers**: Document special headers (e.g., `Retry-After` for 429)

## Complete Example: ContactController

See `/server/engine/src/main/kotlin/com/cvix/contact/infrastructure/http/ContactController.kt`

This controller is the gold standard for Swagger documentation in the project.

## Verification

Before committing:

```bash
make verify-all  # Debe pasar sin errores
```

To view the generated documentation:

1. Run `./gradlew bootRun`
2. Open `http://localhost:8080/swagger-ui.html`

## Anti-Patterns to Avoid

❌ **BAD**:

```kotlin
@Operation(summary = "Login endpoint")
@ApiResponses(
    ApiResponse(responseCode = "200", description = "OK"),
    ApiResponse(responseCode = "400", description = "Bad request"),
)
```

✅ **GOOD**:

```kotlin
@Operation(
    summary = "Authenticate user",
    description = "Authenticates a user with email and password, returning access and refresh tokens. " +
            "Optionally extends session duration if rememberMe is true.",
)
@ApiResponses(
    value = [
        ApiResponse(
            responseCode = "200",
            description = "Authentication successful, tokens returned",
            content = [Content(schema = Schema(implementation = AccessToken::class))],
        ),
        ApiResponse(
            responseCode = "400",
            description = "Invalid email format or password does not meet security requirements",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "401",
            description = "Invalid credentials - email or password is incorrect",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "429",
            description = "Too many login attempts - rate limit exceeded",
            headers = [Header(
                name = "Retry-After",
                description = "Seconds until rate limit resets"
            )],
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
        ApiResponse(
            responseCode = "500",
            description = "Internal server error during authentication",
            content = [Content(schema = Schema(implementation = ProblemDetail::class))],
        ),
    ],
)
```

---

**This standard is MANDATORY** for all new controllers and must be progressively applied to existing
ones.
