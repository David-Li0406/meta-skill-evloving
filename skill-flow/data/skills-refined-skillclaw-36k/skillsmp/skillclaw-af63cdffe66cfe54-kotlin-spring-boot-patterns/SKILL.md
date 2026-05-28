---
name: kotlin-spring-boot-patterns
description: Use this skill when implementing backend services with Kotlin and Spring Boot, including patterns for services, repositories, and controllers.
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

    fun findById(id: UUID): EntityName? =
        repository.findById(id)

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

    override fun getById(id: UUID): ResponseEntity<EntityResponse> {
        val entity = service.findById(id)
            ?: throw ResourceNotFoundRestException("EntityName", id)
        return ResponseEntity.ok(entity.toResponse())
    }
}
```

## API Interface Pattern

```kotlin
@Tag(name = "Entity Name")
```