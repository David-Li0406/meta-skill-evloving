# CQRS Handlers - Command and Query Handlers

Command and Query handlers implement the CQRS (Command Query Responsibility Segregation) pattern.
They receive commands/queries from controllers via the Mediator and orchestrate the use case logic.

> **Important**: Handlers live in the **application layer** but use the `@Service` annotation
> from `com.cvix.common.domain.Service` (NOT Spring's `@Service`). This allows them to be
> discovered by the Mediator while keeping them framework-agnostic in their logic.

## Handler Types

| Type                       | Interface                                      | Returns           | Purpose                      |
|----------------------------|------------------------------------------------|-------------------|------------------------------|
| `CommandHandler<C>`        | `CommandHandler<JoinWaitlistCommand>`          | `Unit` (void)     | Write operations, no result  |
| `CommandWithResultHandler` | `CommandWithResultHandler<C, R>`               | `R` (result type) | Write operations with result |
| `QueryHandler<Q, R>`       | `QueryHandler<GetResumeQuery, ResumeResponse>` | `R` (result type) | Read operations              |

## Command Handler (No Result)

For commands that don't need to return data to the caller:

```kotlin
// application/create/JoinWaitlistCommand.kt
data class JoinWaitlistCommand(
    val id: UUID,
    val email: String,
    val source: String,
    val language: String,
    val ipAddress: String? = null,
    val metadata: Map<String, Any>? = null,
) : Command

// application/create/JoinWaitlistCommandHandler.kt
@Service
class JoinWaitlistCommandHandler(
    private val waitlistJoiner: WaitlistJoiner,  // Application service
) : CommandHandler<JoinWaitlistCommand> {

    override suspend fun handle(command: JoinWaitlistCommand) {
        logger.info("Handling JoinWaitlistCommand for source: {}", command.source)

        // Parse and validate (application concern)
        val email = Email.of(command.email)
            ?: throw IllegalArgumentException("Invalid email format")
        val source = WaitlistSource.fromString(command.source)
        val language = Language.fromString(command.language)
        val entryId = WaitlistEntryId(command.id)

        // Delegate to service (business logic)
        waitlistJoiner.join(
            id = entryId,
            email = email,
            sourceRaw = command.source,
            sourceNormalized = source,
            language = language,
            ipAddress = command.ipAddress,
            metadata = command.metadata,
        )

        logger.info("Successfully processed JoinWaitlistCommand")
    }

    companion object {
        private val logger = LoggerFactory.getLogger(JoinWaitlistCommandHandler::class.java)
    }
}
```

## Command Handler With Result

For commands that need to return data (e.g., created entity ID or full response):

```kotlin
// application/create/CreateResumeCommand.kt
data class CreateResumeCommand(
    val id: UUID,
    val userId: UUID,
    val workspaceId: UUID,
    val title: String?,
    val content: Resume,
    val createdBy: String,
) : Command

// application/create/CreateResumeCommandHandler.kt
@Service
class CreateResumeCommandHandler(
    private val resumeCreator: ResumeCreator,
) : CommandWithResultHandler<CreateResumeCommand, ResumeDocumentResponse> {

    override suspend fun handle(command: CreateResumeCommand): ResumeDocumentResponse {
        log.info(
            "Creating resume - userId={}, workspaceId={}",
            command.userId,
            command.workspaceId,
        )

        val savedDocument = resumeCreator.create(
            id = command.id,
            userId = command.userId,
            workspaceId = command.workspaceId,
            title = command.title ?: command.content.basics.name.value,
            content = command.content,
            createdBy = command.createdBy,
        )

        return ResumeDocumentResponse.from(savedDocument)
    }

    companion object {
        private val log = LoggerFactory.getLogger(CreateResumeCommandHandler::class.java)
    }
}
```

## Application Services

Handlers delegate to **application services** that contain the actual business logic.
Services are **NOT** annotated with Spring annotations - they're wired via `@Configuration`:

```kotlin
// application/create/WaitlistJoiner.kt
@Service  // com.cvix.common.domain.Service - NOT org.springframework.stereotype.Service
class WaitlistJoiner(
    private val repository: WaitlistRepository,           // Domain port
    eventPublisher: EventPublisher<WaitlistEntryCreatedEvent>,
    private val metrics: WaitlistMetrics,                 // Domain port
    private val securityConfig: WaitlistSecurityConfig,   // Domain port
) {
    private val eventBroadcaster = EventBroadcaster<WaitlistEntryCreatedEvent>()

    init {
        this.eventBroadcaster.use(eventPublisher)
    }

    suspend fun join(
        id: WaitlistEntryId,
        email: Email,
        sourceRaw: String,
        sourceNormalized: WaitlistSource,
        language: Language,
        ipAddress: String? = null,
        metadata: Map<String, Any>? = null,
    ): WaitlistEntry {
        logger.info("Attempting to add email to waitlist")

        // Business rule: check uniqueness
        if (repository.existsByEmail(email)) {
            throw EmailAlreadyExistsException(email.value)
        }

        // Business logic: hash IP for privacy
        val ipHash = ipAddress?.let { hashIpAddress(it) }

        // Create domain entity
        val entry = WaitlistEntry.create(
            id = id,
            email = email,
            sourceRaw = sourceRaw,
            sourceNormalized = sourceNormalized,
            language = language,
            ipHash = ipHash,
            metadata = metadata,
        )

        // Persist via repository port
        val savedEntry = repository.save(entry)

        // Publish domain events
        savedEntry.pullDomainEvents().forEach { event ->
            eventBroadcaster.publish(event as WaitlistEntryCreatedEvent)
        }

        return savedEntry
    }
}
```

## Folder Structure

Organize by use case within the `application/` layer:

```markdown
feature/
└── application/
├── create/
│ ├── CreateFeatureCommand.kt
│ ├── CreateFeatureCommandHandler.kt
│ └── FeatureCreator.kt # Service with business logic
├── get/
│ ├── GetFeatureQuery.kt
│ ├── GetFeatureQueryHandler.kt
│ └── FeatureRetrieval.kt # Service for read logic
├── list/
│ ├── ListFeaturesQuery.kt
│ ├── ListFeaturesQueryHandler.kt
│ └── FeatureCatalog.kt # Service for listing
├── update/
│ ├── UpdateFeatureCommand.kt
│ └── UpdateFeatureCommandHandler.kt
└── delete/
├── DeleteFeatureCommand.kt
└── DeleteFeatureCommandHandler.kt
```

## Handler Responsibilities

| Do                                    | Don't                                     |
|---------------------------------------|-------------------------------------------|
| Parse/validate command data           | Access HTTP request/response              |
| Transform primitives to value objects | Import Spring web annotations             |
| Call application services             | Call repositories directly (use services) |
| Map service results to response types | Implement complex business logic          |
| Log at INFO level for operations      | Catch exceptions (let them propagate)     |

## The @Service Annotation

We use a **custom** `@Service` annotation, NOT Spring's:

```kotlin
package com.cvix.common.domain

/**
 * Custom service annotation for application layer services.
 * Discovered by component scanning but keeps domain/application layer
 * framework-agnostic in its logic.
 */
@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
annotation class Service
```

This allows the Mediator to discover handlers while keeping them portable.

## Anti-Patterns

```kotlin
// ❌ WRONG: Business logic in handler
@Service
class CreateUserCommandHandler(
    private val repository: UserRepository,  // Direct repository access
) : CommandHandler<CreateUserCommand> {
    override suspend fun handle(command: CreateUserCommand) {
        // Business logic should be in service!
        if (repository.existsByEmail(command.email)) {
            throw ConflictException("Email exists")
        }
        val user = User(email = command.email)
        repository.save(user)
        emailService.sendWelcome(user)  // Side effect in handler!
    }
}

// ✅ CORRECT: Handler delegates to service
@Service
class CreateUserCommandHandler(
    private val userCreator: UserCreator,  // Application service
) : CommandHandler<CreateUserCommand> {
    override suspend fun handle(command: CreateUserCommand) {
        val email = Email.of(command.email) ?: throw IllegalArgumentException("Invalid email")
        userCreator.create(email)  // All logic in service
    }
}
```

## Related References

- [controllers.md](./controllers.md) - How controllers dispatch to handlers
- [configuration.md](./configuration.md) - How services are wired as beans
- [../hexagonal-architecture/SKILL.md](../hexagonal-architecture/SKILL.md) - Application layer
  patterns
