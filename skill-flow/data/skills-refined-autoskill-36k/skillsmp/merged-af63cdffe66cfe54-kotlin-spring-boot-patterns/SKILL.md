---
name: kotlin-spring-boot-patterns
description: Use this skill when implementing backend services with Kotlin and Spring Boot, including REST APIs, services, repositories, and controllers.
---

# Kotlin Spring Boot Patterns

## Project Configuration

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.2.21"
    kotlin("plugin.spring") version "2.2.21"
    id("org.springframework.boot") version "3.5.7"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
}
```

## Entity Pattern

```kotlin
data class EntityName(
    val id: UUID,
    val name: String,
    val createdAt: Instant,
    val updatedAt: Instant?
)

enum class EnvironmentStatus {
    PENDING, RUNNING, STOPPED, FAILED
}
```

## Service Pattern

```kotlin
@Service
class EntityNameService(
    private val repository: EntityNameRepository,
    private val relatedService: RelatedService
) {
    @Transactional(propagation = Propagation.NEVER)
    fun create(request: CreateRequest): Pair<EntityResponse, Boolean> {
        // Check for existing (idempotency)
        repository.findByName(request.name)?.let {
            return Pair(it.toResponse(), false) // existing
        }

        // Create new
        val entity = EntityName(
            id = UUID.randomUUID(),
            name = request.name,
            createdAt = Instant.now(),
            updatedAt = null
        )

        val saved = repository.save(entity)
        return Pair(saved.toResponse(), true) // created
    }

    fun findById(id: UUID): EntityName =
        repository.findById(id)
            ?: throw ResourceNotFoundRestException("EntityName", id)

    fun findAll(): List<EntityName> =
        repository.findAll()
}
```

## Repository Pattern

```kotlin
@Repository
class EntityNameRepository(
    private val dsl: DSLContext
) {
    fun findById(id: UUID): EntityName? =
        dsl.selectFrom(ENTITY_NAME)
            .where(ENTITY_NAME.ID.eq(id))
            .fetchOne()
            ?.toEntity()

    fun findAll(): List<EntityName> =
        dsl.selectFrom(ENTITY_NAME)
            .fetch()
            .map { it.toEntity() }

    fun save(entity: EntityName): EntityName =
        dsl.insertInto(ENTITY_NAME)
            .set(ENTITY_NAME.ID, entity.id)
            .set(ENTITY_NAME.NAME, entity.name)
            .set(ENTITY_NAME.CREATED_AT, entity.createdAt)
            .returning()
            .fetchOne()!!
            .toEntity()

    private fun EntityNameRecord.toEntity() = EntityName(
        id = id,
        name = name,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}
```

## Controller Pattern

```kotlin
@RestController
class EntityNameController(
    private val service: EntityNameService
) : EntityNameApi {

    override fun create(request: CreateRequest): ResponseEntity<EntityResponse> {
        val (result, isNew) = service.create(request)
        return if (isNew) ResponseEntity.status(HttpStatus.CREATED).body(result)
        else ResponseEntity.ok(result)
    }

    override fun getById(id: UUID): ResponseEntity<EntityResponse> =
        ResponseEntity.ok(service.findById(id).toResponse())

    override fun list(): ResponseEntity<List<EntityResponse>> =
        ResponseEntity.ok(service.findAll().map { it.toResponse() })
}
```

## API Interface Pattern

```kotlin
@Tag(name = "Entity Name")
interface EntityNameApi {

    @Operation(summary = "Create entity")
    @PostMapping("/api/v1/entities")
    fun create(@RequestBody @Valid request: CreateRequest): ResponseEntity<EntityResponse>

    @Operation(summary = "Get entity by ID")
    @GetMapping("/api/v1/entities/{id}")
    fun getById(@PathVariable id: UUID): ResponseEntity<EntityResponse>

    @Operation(summary = "List all entities")
    @GetMapping("/api/v1/entities")
    fun list(): ResponseEntity<List<EntityResponse>>
}
```

## DTO Pattern

```kotlin
data class CreateRequest(
    @field:NotBlank(message = "Name is required")
    @field:Size(max = 100, message = "Name must be <= 100 chars")
    val name: String,

    @field:Size(max = 500)
    val description: String? = null
)

data class EntityResponse(
    val id: UUID,
    val name: String,
    val description: String?,
    val createdAt: Instant
)

// Extension function for mapping
fun EntityName.toResponse() = EntityResponse(
    id = id,
    name = name,
    description = description,
    createdAt = createdAt
)
```

## Exception Handling

```kotlin
// Typed exceptions
throw ResourceNotFoundRestException("EntityName", id)
throw ValidationRestException("Name cannot be empty")
throw ConflictRestException("Entity already exists")

// Global handler
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundRestException::class)
    fun handleNotFound(ex: ResourceNotFoundRestException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(ex.message ?: "Not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.map { "${it.field}: ${it.defaultMessage}" }
        return ResponseEntity.badRequest()
            .body(ErrorResponse("Validation failed", errors))
    }
}
```

## Null Safety Guidelines

- Use `?.let{}` for optional operations
- Use `when` for exhaustive matching
- Instead of not-null assertion, use `.single()` or `.firstOrNull()`
- Return `Pair<Result, Boolean>` for idempotent operations