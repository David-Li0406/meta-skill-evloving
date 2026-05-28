---
name: hexagonal-architecture
description: >
  Hexagonal Architecture (Ports and Adapters) with CQRS for clean, testable code.
  Trigger: When creating features, domain models, use cases, or organizing backend code.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
metadata:
  author: cvix
  version: "1.0"
---

# Hexagonal Architecture Skill

Patterns for implementing Hexagonal Architecture (Ports and Adapters) with CQRS in Kotlin/Spring
Boot.

## When to Use

- Creating new features or bounded contexts
- Designing domain models and value objects
- Implementing use cases (commands/queries)
- Organizing code within a feature
- Deciding where code belongs (domain vs application vs infrastructure)

## Critical Concepts

| Concept            | Description                                                 |
|--------------------|-------------------------------------------------------------|
| **Domain**         | Pure business logic, NO framework or library dependencies   |
| **Application**    | Use cases orchestrating domain operations                   |
| **Infrastructure** | Framework integration (Spring, R2DBC, HTTP)                 |
| **Ports**          | Interfaces defined by domain, implemented by infrastructure |
| **Adapters**       | Infrastructure implementations of ports                     |

## Feature Structure

**EVERY feature follows this structure**:

```markdown
📁 {feature}/
├── 📁 domain/           # Pure Kotlin, NO Spring annotations
├── 📁 application/      # Use cases, CQRS handlers
└── 📁 infrastructure/   # Spring Boot, R2DBC, HTTP
```

### Dependency Flow (CRITICAL)

```markdown
domain ← application ← infrastructure
   ↑          ↑              ↑
 NOTHING    domain      domain + application
```

| Layer              | Can Depend On        | NEVER Depends On                    |
|--------------------|----------------------|-------------------------------------|
| **Domain**         | Nothing (pure)       | Application, Infrastructure, Spring |
| **Application**    | Domain only          | Infrastructure, Spring              |
| **Infrastructure** | Domain + Application | -                                   |

---

## 1. Domain Layer (`domain/`)

**Pure Kotlin. NO framework dependencies. NO Spring annotations.**

### What Belongs Here

| Element                   | Purpose                             | Example                         |
|---------------------------|-------------------------------------|---------------------------------|
| **Entities**              | Core business objects with identity | `Workspace.kt`                  |
| **Value Objects**         | Immutable domain concepts           | `WorkspaceId.kt`, `Email.kt`    |
| **Repository Interfaces** | Contracts for persistence (PORTS)   | `WorkspaceRepository.kt`        |
| **Domain Events**         | Facts that happened in the domain   | `WorkspaceCreatedEvent.kt`      |
| **Domain Exceptions**     | Business rule violations            | `WorkspaceNotFoundException.kt` |

### Entity Example

```kotlin
// domain/Workspace.kt
data class Workspace(
    val id: WorkspaceId,
    val name: WorkspaceName,
    val ownerId: UserId,
    val members: List<WorkspaceMember> = emptyList(),
    val createdAt: Instant = Instant.now(),
) {
    // Business logic INSIDE the entity
    fun addMember(userId: UserId, role: WorkspaceRole): Workspace {
        require(!hasMember(userId)) { "User is already a member" }
        return copy(
            members = members + WorkspaceMember(userId, role),
        )
    }

    fun hasMember(userId: UserId): Boolean =
        members.any { it.userId == userId }

    fun isOwner(userId: UserId): Boolean = ownerId == userId
}
```

### Value Object Example

```kotlin
// domain/WorkspaceId.kt
@JvmInline
value class WorkspaceId(val value: UUID) {
    companion object {
        fun generate(): WorkspaceId = WorkspaceId(UUID.randomUUID())
    }
}

// domain/WorkspaceName.kt
@JvmInline
value class WorkspaceName(val value: String) {
    init {
        require(value.isNotBlank()) { "Workspace name cannot be blank" }
        require(value.length <= 100) { "Workspace name too long" }
    }
}

// domain/Email.kt
@JvmInline
value class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email format" }
    }

    fun domain(): String = value.substringAfter("@")
}
```

### Repository Interface (PORT)

```kotlin
// domain/WorkspaceRepository.kt
interface WorkspaceRepository {
    suspend fun save(workspace: Workspace): Workspace
    suspend fun findById(id: WorkspaceId): Workspace?
    suspend fun delete(id: WorkspaceId)
}

// domain/WorkspaceFinderRepository.kt (read-only queries)
interface WorkspaceFinderRepository {
    suspend fun findByOwnerId(ownerId: UserId): List<Workspace>
    suspend fun findByMemberId(memberId: UserId): List<Workspace>
    suspend fun existsByName(name: WorkspaceName): Boolean
}
```

### Domain Exception

```kotlin
// domain/WorkspaceException.kt
sealed class WorkspaceException(message: String) : RuntimeException(message)

class WorkspaceNotFoundException(id: WorkspaceId) :
    WorkspaceException("Workspace not found: ${id.value}")

class WorkspaceAlreadyExistsException(name: WorkspaceName) :
    WorkspaceException("Workspace already exists: ${name.value}")

class WorkspaceMemberAlreadyExistsException(userId: UserId) :
    WorkspaceException("User is already a member: ${userId.value}")
```

### Domain Event

```kotlin
// domain/event/WorkspaceCreatedEvent.kt
data class WorkspaceCreatedEvent(
    val workspaceId: WorkspaceId,
    val ownerId: UserId,
    val name: WorkspaceName,
    val occurredAt: Instant = Instant.now(),
) : DomainEvent
```

### Domain Structure

```markdown
📁 domain/
├── Workspace.kt                    # Entity
├── WorkspaceMember.kt              # Entity
├── WorkspaceId.kt                  # Value Object
├── WorkspaceName.kt                # Value Object
├── WorkspaceRole.kt                # Value Object (enum)
├── WorkspaceRepository.kt          # Repository interface (write)
├── WorkspaceFinderRepository.kt    # Repository interface (read)
├── WorkspaceException.kt           # Domain exceptions
└── 📁 event/
    └── WorkspaceCreatedEvent.kt    # Domain event
```

---

## 2. Application Layer (`application/`)

**Use cases organized by CQRS. Framework-agnostic.**

### CQRS Organization

```markdown
📁 application/
├── 📁 create/           # Command: Create workspace
│   ├── CreateWorkspaceCommand.kt
│   ├── CreateWorkspaceCommandHandler.kt
│   └── WorkspaceCreator.kt
├── 📁 find/             # Query: Find workspaces
│   ├── FindWorkspaceQuery.kt
│   ├── FindWorkspaceQueryHandler.kt
│   └── WorkspaceFinder.kt
├── 📁 update/           # Command: Update workspace
└── 📁 delete/           # Command: Delete workspace
```

### Command Pattern (Writes)

```kotlin
// application/create/CreateWorkspaceCommand.kt
data class CreateWorkspaceCommand(
    val name: String,
    val ownerId: UUID,
)

// application/create/CreateWorkspaceCommandHandler.kt
class CreateWorkspaceCommandHandler(
    private val creator: WorkspaceCreator,
) {
    suspend fun handle(command: CreateWorkspaceCommand): WorkspaceId {
        return creator.create(
            name = WorkspaceName(command.name),
            ownerId = UserId(command.ownerId),
        )
    }
}

// application/create/WorkspaceCreator.kt
class WorkspaceCreator(
    private val repository: WorkspaceRepository,
    private val finderRepository: WorkspaceFinderRepository,
    private val eventPublisher: DomainEventPublisher,
    private val auditLogger: WorkspaceAuditPort, // infrastructure adapter implements this
) {
    suspend fun create(name: WorkspaceName, ownerId: UserId): WorkspaceId {
        auditLogger.creating(name, ownerId)

        // Business rule: unique name
        if (finderRepository.existsByName(name)) {
            throw WorkspaceAlreadyExistsException(name)
        }

        val workspace = Workspace(
            id = WorkspaceId.generate(),
            name = name,
            ownerId = ownerId,
        )

        repository.save(workspace)

        eventPublisher.publish(
            WorkspaceCreatedEvent(
                workspaceId = workspace.id,
                ownerId = ownerId,
                name = name,
            ),
        )

        auditLogger.created(workspace.id)
        return workspace.id
    }
}
```

### Query Pattern (Reads)

```kotlin
// application/find/FindWorkspaceQuery.kt
data class FindWorkspaceQuery(
    val workspaceId: UUID,
)

// application/find/FindWorkspaceQueryHandler.kt
class FindWorkspaceQueryHandler(
    private val finder: WorkspaceFinder,
) {
    suspend fun handle(query: FindWorkspaceQuery): Workspace {
        return finder.findById(WorkspaceId(query.workspaceId))
    }
}

// application/find/WorkspaceFinder.kt
class WorkspaceFinder(
    private val repository: WorkspaceFinderRepository,
) {
    suspend fun findById(id: WorkspaceId): Workspace {
        return repository.findById(id)
            ?: throw WorkspaceNotFoundException(id)
    }

    suspend fun findByMember(memberId: UserId): List<Workspace> {
        return repository.findByMemberId(memberId)
    }
}
```

### Key Principles

- **Handlers are thin**: Receive command/query → delegate to service → return
- **Services contain logic**: Validation, orchestration, event publishing
- **NO Spring annotations**: Application layer is framework-agnostic
- **Return domain objects**: Not DTOs (mapping happens in infrastructure)

---

## 3. Infrastructure Layer (`infrastructure/`)

**Spring Boot integration. Implements domain ports.**

### Structure

```markdown
📁 infrastructure/
├── 📁 http/                              # REST controllers
│   ├── CreateWorkspaceController.kt
│   ├── FindWorkspaceController.kt
│   └── 📁 request/
│       └── CreateWorkspaceRequest.kt
│   └── 📁 response/
│       └── WorkspaceResponse.kt
├── 📁 persistence/                       # Database (R2DBC)
│   ├── WorkspaceStoreR2DbcRepository.kt  # Implements WorkspaceRepository
│   ├── 📁 entity/
│   │   └── WorkspaceEntity.kt
│   ├── 📁 mapper/
│   │   └── WorkspaceMapper.kt
│   └── 📁 repository/
│       └── WorkspaceR2DbcRepository.kt   # Spring Data interface
├── 📁 event/
│   └── WorkspaceEventPublisher.kt
└── 📁 configuration/
    └── WorkspaceConfiguration.kt         # Bean definitions
```

### Controller (HTTP Adapter)

```kotlin
// infrastructure/http/CreateWorkspaceController.kt
@RestController
@RequestMapping("/api/workspaces")
class CreateWorkspaceController(
    private val commandHandler: CreateWorkspaceCommandHandler,
) {
    @PostMapping
    suspend fun create(
        @Valid @RequestBody request: CreateWorkspaceRequest,
    ): ResponseEntity<WorkspaceIdResponse> {
        val command = CreateWorkspaceCommand(
            name = request.name,
            ownerId = request.ownerId,
        )

        val workspaceId = commandHandler.handle(command)

        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(WorkspaceIdResponse(workspaceId.value))
    }
}

// infrastructure/http/request/CreateWorkspaceRequest.kt
data class CreateWorkspaceRequest(
    @field:NotBlank
    val name: String,
    @field:NotNull
    val ownerId: UUID,
)

// infrastructure/http/response/WorkspaceResponse.kt
data class WorkspaceResponse(
    val id: UUID,
    val name: String,
    val ownerId: UUID,
    val memberCount: Int,
    val createdAt: Instant,
)

fun Workspace.toResponse() = WorkspaceResponse(
    id = id.value,
    name = name.value,
    ownerId = ownerId.value,
    memberCount = members.size,
    createdAt = createdAt,
)
```

### Persistence (Repository Adapter)

```kotlin
// infrastructure/persistence/WorkspaceStoreR2DbcRepository.kt
@Repository
class WorkspaceStoreR2DbcRepository(
    private val r2dbcRepository: WorkspaceR2DbcRepository,
    private val mapper: WorkspaceMapper,
) : WorkspaceRepository {

    override suspend fun save(workspace: Workspace): Workspace {
        val entity = mapper.toEntity(workspace)
        val saved = r2dbcRepository.save(entity).awaitSingle()
        return mapper.toDomain(saved)
    }

    override suspend fun findById(id: WorkspaceId): Workspace? {
        return r2dbcRepository.findById(id.value).awaitSingleOrNull()
            ?.let { mapper.toDomain(it) }
    }

    override suspend fun delete(id: WorkspaceId) {
        r2dbcRepository.deleteById(id.value).awaitSingleOrNull()
    }
}

// infrastructure/persistence/repository/WorkspaceR2DbcRepository.kt
interface WorkspaceR2DbcRepository : ReactiveCrudRepository<WorkspaceEntity, UUID> {
    fun findByOwnerId(ownerId: UUID): Flux<WorkspaceEntity>
}

// infrastructure/persistence/entity/WorkspaceEntity.kt
@Table("workspaces")
data class WorkspaceEntity(
    @Id val id: UUID? = null,
    val name: String,
    val ownerId: UUID,
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant = Instant.now(),
)

// infrastructure/persistence/mapper/WorkspaceMapper.kt
@Component
class WorkspaceMapper {
    fun toDomain(entity: WorkspaceEntity): Workspace = Workspace(
        id = WorkspaceId(requireNotNull(entity.id)),
        name = WorkspaceName(entity.name),
        ownerId = UserId(entity.ownerId),
        createdAt = entity.createdAt,
    )

    fun toEntity(domain: Workspace): WorkspaceEntity = WorkspaceEntity(
        id = domain.id.value,
        name = domain.name.value,
        ownerId = domain.ownerId.value,
        createdAt = domain.createdAt,
    )
}
```

### Configuration (Wire Everything)

```kotlin
// infrastructure/configuration/WorkspaceConfiguration.kt
@Configuration
class WorkspaceConfiguration {

    @Bean
    fun workspaceCreator(
        repository: WorkspaceRepository,
        finderRepository: WorkspaceFinderRepository,
        eventPublisher: DomainEventPublisher,
    ) = WorkspaceCreator(repository, finderRepository, eventPublisher)

    @Bean
    fun createWorkspaceCommandHandler(
        creator: WorkspaceCreator,
    ) = CreateWorkspaceCommandHandler(creator)

    @Bean
    fun workspaceFinder(
        repository: WorkspaceFinderRepository,
    ) = WorkspaceFinder(repository)

    @Bean
    fun findWorkspaceQueryHandler(
        finder: WorkspaceFinder,
    ) = FindWorkspaceQueryHandler(finder)
}
```

---

## Decision Tree: Where Does This Code Belong?

```markdown
Is it business logic with NO framework dependencies?
├── YES → DOMAIN
│   ├── Has identity? → Entity
│   ├── Immutable concept? → Value Object
│   ├── Data access contract? → Repository Interface
│   └── Business event? → Domain Event
│
└── NO → Does it orchestrate domain operations?
    ├── YES → APPLICATION
    │   ├── Writes data? → Command + Handler + Service
    │   └── Reads data? → Query + Handler + Service
    │
    └── NO → INFRASTRUCTURE
        ├── HTTP? → Controller + Request/Response DTOs
        ├── Database? → Repository Implementation + Entity + Mapper
        └── External service? → Adapter
```

## Anti-Patterns

❌ **Spring annotations in Domain** - Domain must be pure Kotlin
❌ **Business logic in Controllers** - Controllers only handle HTTP
❌ **Business logic in Repository implementations** - Logic belongs in Domain/Application
❌ **Exposing database entities** - Always map to domain, then to DTOs
❌ **Application depending on Infrastructure** - Only Infrastructure depends down
❌ **Fat handlers** - Handlers should be thin, delegate to services
❌ **Anemic domain models** - Put behavior IN the entities

## Error Handling Across Layers

Error propagation follows the hexagonal boundaries:

| Layer              | Error Type               | Responsibility                                            |
|--------------------|--------------------------|-----------------------------------------------------------|
| **Domain**         | Domain exceptions        | Pure business errors (e.g., `InsufficientFundsException`) |
| **Application**    | Application-level errors | Translate infrastructure errors, orchestrate domain       |
| **Infrastructure** | HTTP-friendly responses  | Map exceptions to status codes and `ProblemDetail`        |

**Rules:**

1. **Domain errors bubble as domain exceptions** – Keep domain exceptions pure Kotlin, no framework
   dependencies
2. **Infrastructure exceptions are mapped at the application boundary** – Catch and translate in
   application services or handlers before reaching controllers
3. **Controllers never catch domain exceptions directly** – Use `@ControllerAdvice` to map
   domain/application errors to HTTP responses

```kotlin
// Domain layer - pure business exception
class UserAlreadyExistsException(val email: Email) : DomainException("User with email ${email.value} already exists")

// Application layer - catches and translates
class CreateUserHandler(private val userRepository: UserRepository) {
    suspend fun handle(command: CreateUserCommand): Result<UserId> = runCatching {
        // Domain exception bubbles up
        userRepository.findByEmail(command.email)?.let {
            throw UserAlreadyExistsException(command.email)
        }
        // ...
    }
}

// Infrastructure layer - maps to HTTP
@RestControllerAdvice
class DomainExceptionHandler {
    @ExceptionHandler(UserAlreadyExistsException::class)
    fun handleConflict(ex: UserAlreadyExistsException) =
        ResponseEntity.status(HttpStatus.CONFLICT)
            .body(ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.message))
}
```

## Testing Strategy by Layer

Each layer has specific testing requirements (see
also: [Decision Tree](#decision-tree-where-does-this-code-belong)
and [Architecture Tests](#architecture-tests-archunit)):

| Layer              | Test Type                     | Strategy                                                                                     |
|--------------------|-------------------------------|----------------------------------------------------------------------------------------------|
| **Domain**         | Unit tests                    | Pure logic, no mocks needed, fast execution                                                  |
| **Application**    | Integration / Component tests | Mock Repository/Port interfaces, verify orchestration (component/unit-level, not full-stack) |
| **Infrastructure** | E2E tests                     | Real DB (Testcontainers), real HTTP calls, full stack                                        |

```kotlin
// Domain - pure unit test (no mocking)
@UnitTest
class EmailTest {
    @Test
    fun `should reject invalid email format`() {
        shouldThrow<IllegalArgumentException> {
            Email("invalid")
        }
    }
}

// Application - integration with mocked ports
@UnitTest
class CreateUserHandlerTest {
    private val userRepository = mockk<UserRepository>()
    private val handler = CreateUserHandler(userRepository)

    @Test
    fun `should create user when email is unique`() = runTest {
        coEvery { userRepository.findByEmail(any()) } returns null
        coEvery { userRepository.save(any()) } returns testUser

        val result = handler.handle(CreateUserCommand(email, name))

        result.isSuccess shouldBe true
    }
}

// Infrastructure - E2E with Testcontainers
@IntegrationTest
class UserControllerIntegrationTest {
    @Test
    fun `POST users should create user and return 201`() {
        webTestClient.post().uri("/api/users")
            .bodyValue(CreateUserRequest(email, name))
            .exchange()
            .expectStatus().isCreated
            .expectBody<UserIdResponse>()
    }
}
```

## Commands

```bash
# Create new feature structure
mkdir -p server/engine/src/main/kotlin/com/cvix/{feature}/{domain,application,infrastructure}

# Verify architecture (check imports)
rg "import org.springframework" server/engine/src/main/kotlin/com/cvix/*/domain/

# Should return NOTHING - domain must be pure
```

## Architecture Tests (ArchUnit)

To keep boundaries enforced automatically, every new feature/bounded context must be added to the
ArchUnit test so rules run for it.

- File: server/engine/src/test/kotlin/com/cvix/ArchTest.kt
- Update the `boundedContexts` list to include the new feature folder name (matches
  `com.cvix.{feature}`):

```kotlin
private val boundedContexts = listOf(
    "users",
    "authentication",
    "workspace",
    "ratelimit",
    "resume",
    "waitlist",
    "subscription",
    "contact",
    // ➕ add your new feature here, e.g. "billing"
)
```

Run tests to verify rules apply to your feature:

```bash
./gradlew test --tests com.cvix.ArchTest
```

## Resources

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [spring-boot skill](../spring-boot/SKILL.md) - Framework patterns for Infrastructure
  layer
- [kotlin skill](../kotlin/SKILL.md) - Kotlin conventions for all layers
