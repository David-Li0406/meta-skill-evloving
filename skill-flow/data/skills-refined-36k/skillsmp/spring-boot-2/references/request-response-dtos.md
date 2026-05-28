# Request and Response DTOs

DTOs (Data Transfer Objects) are infrastructure layer objects for HTTP request/response
serialization.
They use Jakarta validation and Swagger annotations.

## Request DTOs

Request DTOs define the expected HTTP request body with validation:

```kotlin
// infrastructure/http/request/JoinWaitlistRequest.kt
data class JoinWaitlistRequest(
    @field:Email(message = "Email must be valid")
    @field:NotBlank(message = "Email is required")
    @field:Size(max = 320, message = "Email must not exceed 320 characters")
    @field:Schema(
        description = "User's email address",
        example = "user@example.com",
        required = true,
    )
    val email: String,

    @field:NotBlank(message = "Source is required")
    @field:Size(min = 1, max = 50, message = "Source must be between 1 and 50 characters")
    @field:Pattern(
        regexp = "^[a-z0-9-]+$",
        message = "Source must contain only lowercase letters, numbers, and hyphens",
    )
    @field:Schema(
        description = "Source from where the user is joining (e.g., landing-hero, landing-cta)",
        example = "landing-hero",
        required = true,
    )
    val source: String,

    @field:NotBlank(message = "Language is required")
    @field:Pattern(regexp = "^(en|es)$", message = "Language must be 'en' or 'es'")
    @field:Schema(
        description = "User's preferred language",
        example = "en",
        allowableValues = ["en", "es"],
        required = true,
    )
    val language: String,
)
```

## Validation Annotations

### String Fields

| Annotation         | Purpose                        | Example                             |
|--------------------|--------------------------------|-------------------------------------|
| `@NotBlank`        | Not null, empty, or whitespace | Required strings                    |
| `@Size(min, max)`  | Length constraints             | `@Size(min = 1, max = 100)`         |
| `@Email`           | Valid email format             | `@Email(message = "Invalid email")` |
| `@Pattern(regexp)` | Custom regex                   | `@Pattern(regexp = "^[a-z]+$")`     |

### Numeric Fields

| Annotation        | Purpose       | Example            |
|-------------------|---------------|--------------------|
| `@NotNull`        | Not null      | Required numbers   |
| `@Min(value)`     | Minimum value | `@Min(0)`          |
| `@Max(value)`     | Maximum value | `@Max(100)`        |
| `@Positive`       | > 0           | Prices, quantities |
| `@PositiveOrZero` | >= 0          | Counts             |

### Collections

| Annotation        | Purpose                | Example                    |
|-------------------|------------------------|----------------------------|
| `@NotEmpty`       | Not null and not empty | Required lists             |
| `@Size(min, max)` | Collection size        | `@Size(min = 1, max = 10)` |

## Schema Annotations

Always include `@Schema` for Swagger documentation:

```kotlin
@field:Schema(
    description = "User's email address for notifications",
    example = "user@example.com",
    required = true,
    format = "email",           // OpenAPI format hint
    minLength = 5,              // For string fields
    maxLength = 320,            // For string fields
    minimum = "0",              // For numeric fields
    maximum = "100",            // For numeric fields
    allowableValues = ["a", "b"], // For enum-like fields
    nullable = false,           // Explicit nullability
)
```

## Response DTOs

Response DTOs define the HTTP response body:

```kotlin
// infrastructure/http/response/JoinWaitlistResponse.kt
@Schema(description = "Waitlist join success response")
data class JoinWaitlistResponse(
    @field:Schema(
        description = "Whether the operation succeeded",
        example = "true",
    )
    val success: Boolean,

    @field:Schema(
        description = "Localized message describing the result",
        example = "Successfully added to waitlist!",
    )
    val message: String,
)

// For responses with data
@Schema(description = "User response with full details")
data class UserResponse(
    @field:Schema(description = "User's unique identifier")
    val id: UUID,

    @field:Schema(description = "User's email address")
    val email: String,

    @field:Schema(description = "User's display name")
    val name: String,

    @field:Schema(description = "Whether the user is active")
    val isActive: Boolean,

    @field:Schema(description = "When the user was created")
    val createdAt: Instant,
)
```

## Mapping Domain to Response

Create extension functions for clean mapping:

```kotlin
// In response file or separate mapper
fun User.toResponse() = UserResponse(
    id = id.value,
    email = email.value,
    name = name,
    isActive = isActive,
    createdAt = createdAt,
)

// Usage in controller
@GetMapping("/{id}")
suspend fun getUser(@PathVariable id: UUID): ResponseEntity<UserResponse> {
    val user = dispatch(GetUserQuery(id))
    return ResponseEntity.ok(user.toResponse())
}
```

## Nested DTOs

For complex requests with nested objects:

```kotlin
// infrastructure/http/request/CreateResumeRequest.kt
data class CreateResumeRequest(
    @field:NotBlank
    @field:Size(max = 200)
    @field:Schema(description = "Resume title", example = "Software Engineer Resume")
    val title: String,

    @field:Valid  // Validates nested object
    @field:NotNull
    @field:Schema(description = "Resume content")
    val content: ResumeContentRequest,
)

// Nested DTO
data class ResumeContentRequest(
    @field:Valid
    @field:NotNull
    val basics: BasicsDto,

    @field:Valid
    val workExperience: List<WorkExperienceDto> = emptyList(),

    @field:Valid
    val education: List<EducationDto> = emptyList(),
)

// Deeply nested
data class BasicsDto(
    @field:NotBlank
    @field:Size(max = 100)
    @field:Schema(description = "Full name", example = "John Doe")
    val name: String,

    @field:Email
    @field:Schema(description = "Email address", example = "john@example.com")
    val email: String?,

    @field:Valid
    val location: LocationDto?,
)
```

## Request Mapping

Create a mapper to transform request DTOs to domain objects:

```kotlin
// infrastructure/http/mapper/ResumeRequestMapper.kt
object ResumeRequestMapper {

    fun toDomain(request: ResumeContentRequest): Resume {
        return Resume(
            basics = toDomain(request.basics),
            workExperience = request.workExperience.map { toDomain(it) },
            education = request.education.map { toDomain(it) },
        )
    }

    private fun toDomain(dto: BasicsDto): Basics {
        return Basics(
            name = Name(dto.name),
            email = dto.email?.let { Email(it) },
            location = dto.location?.let { toDomain(it) },
        )
    }
}
```

## Folder Structure

```markdown
feature/
└── infrastructure/
└── http/
├── request/
│ ├── CreateFeatureRequest.kt
│ ├── UpdateFeatureRequest.kt
│ └── dto/ # Nested DTOs
│ ├── NestedDto1.kt
│ └── NestedDto2.kt
├── response/
│ ├── FeatureResponse.kt
│ └── FeatureListResponse.kt
└── mapper/
└── FeatureRequestMapper.kt
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Using domain objects as DTOs
@PostMapping
suspend fun create(@RequestBody user: User): ResponseEntity<User> {
    // Exposes domain internals!
}

// ✅ CORRECT: Use DTOs
@PostMapping
suspend fun create(@RequestBody request: CreateUserRequest): ResponseEntity<UserResponse> {
    val user = userCreator.create(request.toCommand())
    return ResponseEntity.ok(user.toResponse())
}

// ❌ WRONG: Validation in controller
@PostMapping
suspend fun create(@RequestBody request: CreateUserRequest): ResponseEntity<*> {
    if (request.email.isBlank()) {
        return ResponseEntity.badRequest().body("Email required")
    }
    // ...
}

// ✅ CORRECT: Use @Valid and validation annotations
@PostMapping
suspend fun create(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserResponse> {
    // Validation happens automatically, exceptions handled by @ControllerAdvice
}

// ❌ WRONG: Missing @field: prefix
data class Request(
    @NotBlank  // Won't work! Applies to property, not field
    val name: String,
)

// ✅ CORRECT: Use @field: prefix
data class Request(
    @field:NotBlank  // Applies to backing field for Jackson
    val name: String,
)
```

## Related References

- [controllers.md](./controllers.md) - Using DTOs in controllers
- [swagger-standard.md](./swagger-standard.md) - Complete Swagger documentation
- [error-handling.md](./error-handling.md) - Validation error responses
