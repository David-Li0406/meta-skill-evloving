# Controllers - Thin HTTP Adapters

Controllers are **infrastructure adapters** that handle HTTP concerns and delegate to application
layer handlers.
They have NO business logic - they transform HTTP requests into commands/queries and dispatch them.

## Core Principles

1. **Thin adapters**: Controllers only handle HTTP mapping, validation delegation, and response
   building
2. **Delegate to handlers**: All business logic lives in `CommandHandler` or `QueryHandler` classes
3. **Use Mediator pattern**: Dispatch commands/queries through `Mediator` instead of direct handler
   injection
4. **Swagger documentation**: All endpoints must follow
   the [swagger-standard](./swagger-standard.md)

## Standard Structure

```kotlin
// infrastructure/http/[Feature]Controller.kt
@Validated
@RestController
@RequestMapping(value = ["/api/[resource]"])
@Tag(name = "[Resource]", description = "[Resource] management endpoints")
class [Feature]Controller(
private val mediator: Mediator,
private val messageSource: MessageSource,  // For localized messages
) : ApiController(mediator) {
    // endpoints
}
```

## Real Example: WaitlistController

From `server/engine/src/main/kotlin/com/cvix/waitlist/infrastructure/http/WaitlistController.kt`:

```kotlin
@Validated
@RestController
@RequestMapping(value = ["/api/waitlist"])
@Tag(name = "Waitlist", description = "Waitlist management endpoints")
class WaitlistController(
    private val mediator: Mediator,
    private val messageSource: MessageSource,
) : ApiController(mediator) {

    @Operation(
        summary = "Join the waitlist",
        description = "Add a user's email to the waitlist for early access notifications",
    )
    @ApiResponses(
        value = [
            ApiResponse(
                responseCode = "201",
                description = "Successfully added to waitlist",
                content = [Content(schema = Schema(implementation = JoinWaitlistResponse::class))],
            ),
            ApiResponse(
                responseCode = "400",
                description = "Invalid request data",
                content = [Content(schema = Schema(implementation = ProblemDetail::class))],
            ),
            ApiResponse(
                responseCode = "409",
                description = "Email already exists in waitlist",
                content = [Content(schema = Schema(implementation = ProblemDetail::class))],
            ),
            // ... more responses
        ],
    )
    @PostMapping(
        produces = ["application/vnd.api.v1+json"],
        consumes = ["application/json"],
    )
    suspend fun join(
        @Valid @RequestBody request: JoinWaitlistRequest,
        serverRequest: ServerHttpRequest
    ): ResponseEntity<JoinWaitlistApiResponse> {
        logger.info("Join waitlist request from source: {}", request.source)

        // Extract metadata (HTTP concern)
        val metadata = mapOf(
            "userAgent" to (serverRequest.headers.getFirst("User-Agent") ?: "unknown"),
            "referer" to (serverRequest.headers.getFirst("Referer") ?: "direct"),
        )

        // Build command (transformation)
        val command = JoinWaitlistCommand(
            id = UUID.randomUUID(),
            email = request.email,
            source = request.source,
            language = request.language,
            ipAddress = ClientIpExtractor.extract(serverRequest),
            metadata = metadata,
        )

        // Dispatch to handler (delegation)
        dispatch(command)

        // Build response (HTTP concern)
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(JoinWaitlistResponse(success = true, message = getLocalizedMessage("success")))
    }
}
```

## Controller Per Operation Pattern

For complex features with multiple CQRS operations, use **one controller per operation**:

```markdown
infrastructure/http/
├── CreateResumeController.kt    # PUT /api/resume/{id}
├── GetResumeController.kt       # GET /api/resume/{id}
├── ListResumeController.kt      # GET /api/resume
├── UpdateResumeController.kt    # PATCH /api/resume/{id}
└── DeleteResumeController.kt    # DELETE /api/resume/{id}
```

From `server/engine/src/main/kotlin/com/cvix/resume/infrastructure/http/CreateResumeController.kt`:

```kotlin
@Validated
@RestController
@RequestMapping(value = ["/api"], produces = ["application/vnd.api.v1+json"])
@Tag(name = "Resume", description = "Resume/CV document management endpoints")
class CreateResumeController(
    mediator: Mediator,
) : ApiController(mediator) {

    @Operation(
        summary = "Create a new resume/CV document",
        description = "Creates a new resume within a workspace context.",
        security = [SecurityRequirement(name = "bearerAuth")],
    )
    @PutMapping("/resume/{id}", consumes = ["application/json"])
    suspend fun createResume(
        @PathVariable id: UUID,
        @Valid @RequestBody request: CreateResumeRequest,
    ): ResponseEntity<ResumeDocumentResponse> {
        val userId = userIdFromToken()
        val workspaceId = workspaceIdFromContext()

        val command = CreateResumeCommand(
            id = id,
            userId = userId,
            workspaceId = workspaceId,
            title = request.title,
            content = ResumeRequestMapper.toDomain(request.content),
            createdBy = userId.toString(),
        )

        val response = dispatch(command)

        return ResponseEntity
            .created(URI.create("/api/resume/$id"))
            .body(response)
    }
}
```

## Controller Responsibilities

| Do                                          | Don't                                    |
|---------------------------------------------|------------------------------------------|
| Extract data from HTTP request              | Implement business logic                 |
| Validate request via `@Valid`               | Call repositories directly               |
| Build commands/queries from requests        | Transform domain objects (use mappers)   |
| Dispatch via mediator                       | Catch exceptions (use @ControllerAdvice) |
| Build HTTP response with correct status     | Log sensitive data (use LogMasker)       |
| Extract context (user, workspace, IP, etc.) | Access domain layer directly             |

## HTTP Content Types

All endpoints use versioned content types:

```kotlin
@PostMapping(
    produces = ["application/vnd.api.v1+json"],  // ALWAYS use versioned
    consumes = ["application/json"],
)
```

## Utility Methods from ApiController

The base `ApiController` provides:

```kotlin
// Dispatch command (void)
dispatch(command)

// Dispatch command with result
val result = dispatch(commandWithResult)

// Get user ID from JWT token
val userId = userIdFromToken()

// Get workspace ID from X-Workspace-Id header
val workspaceId = workspaceIdFromContext()

// Sanitize path variables for URI building
val safeId = sanitizePathVariable(id.toString())
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Business logic in controller
@PostMapping
suspend fun createUser(@RequestBody request: CreateUserRequest): ResponseEntity<User> {
    // Don't do validation/business logic here!
    if (userRepository.existsByEmail(request.email)) {
        throw ConflictException("Email exists")
    }
    val user = userRepository.save(User(email = request.email))
    emailService.sendWelcome(user)  // Side effect in controller!
    return ResponseEntity.ok(user)
}

// ✅ CORRECT: Delegate to handler
@PostMapping
suspend fun createUser(@RequestBody request: CreateUserRequest): ResponseEntity<UserResponse> {
    val command = CreateUserCommand(email = request.email)
    val userId = dispatch(command)
    return ResponseEntity.created(URI.create("/api/users/$userId")).body(UserIdResponse(userId))
}
```

## Related References

- [swagger-standard.md](./swagger-standard.md) - API documentation standard
- [cqrs-handlers.md](./cqrs-handlers.md) - Command/Query handlers
- [request-response-dtos.md](./request-response-dtos.md) - Request/Response DTOs
- [error-handling.md](./error-handling.md) - Exception handling
