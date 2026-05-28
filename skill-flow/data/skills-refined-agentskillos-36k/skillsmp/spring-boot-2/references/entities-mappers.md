# Entities and Mappers

R2DBC entities represent database table rows. Mappers translate between domain models and entities.

## Entity Definition

Entities use Spring Data R2DBC annotations:

```kotlin
// infrastructure/persistence/entity/WaitlistEntryEntity.kt
@Table("waitlist")
data class WaitlistEntryEntity(
    @Id
    @JvmField
    val id: UUID,

    @Column("email")
    @get:Size(max = 320)
    val email: String,

    @Column("source_raw")
    @get:Size(max = 50)
    val sourceRaw: String,

    @Column("source_normalized")
    @get:Size(max = 50)
    val sourceNormalized: String,

    @Column("language")
    @get:Size(max = 10)
    val language: String,

    @Column("ip_hash")
    @get:Size(max = 64)
    val ipHash: String?,

    @Column("metadata")
    val metadata: Json?,  // JSONB column

    // Audit fields
    @CreatedBy
    @Column("created_by")
    @get:Size(max = 50)
    override val createdBy: String = "system",

    @CreatedDate
    @Column("created_at")
    override val createdAt: Instant,

    @LastModifiedBy
    @Column("updated_by")
    @get:Size(max = 50)
    override var updatedBy: String? = null,

    @LastModifiedDate
    @Column("updated_at")
    override var updatedAt: Instant? = null,
) : Serializable, Persistable<UUID>, AuditableEntityFields {

    override fun getId(): UUID = id

    /**
     * Determines if the entity is new (for INSERT vs UPDATE).
     */
    override fun isNew(): Boolean = isNewEntity()

    companion object {
        private const val serialVersionUID: Long = 1L
    }
}
```

## Key Annotations

| Annotation          | Purpose                                        |
|---------------------|------------------------------------------------|
| `@Table("name")`    | Maps class to database table                   |
| `@Id`               | Marks primary key field                        |
| `@Column("name")`   | Maps field to column (optional if names match) |
| `@CreatedDate`      | Auto-populates with creation timestamp         |
| `@LastModifiedDate` | Auto-updates with modification timestamp       |
| `@CreatedBy`        | Auto-populates with current user               |
| `@LastModifiedBy`   | Auto-updates with current user                 |

## Persistable Interface

For entities with client-generated IDs, implement `Persistable<ID>`:

```kotlin
data class MyEntity(
    @Id val id: UUID,
    // fields...
) : Persistable<UUID> {

    override fun getId(): UUID = id

    /**
     * R2DBC uses this to determine INSERT vs UPDATE.
     * Return true for new entities (INSERT), false for existing (UPDATE).
     */
    override fun isNew(): Boolean = updatedAt == null || createdAt == updatedAt
}
```

## JSONB Columns

For PostgreSQL JSONB columns, use `io.r2dbc.postgresql.codec.Json`:

```kotlin
@Column("metadata")
val metadata: Json?  // Stored as JSONB

// In mapper, serialize/deserialize:
val metadataJson = domain.metadata?.let {
    Json.of(jsonMapper.writeValueAsString(it))
}
```

## Mapper Component

Mappers translate between domain and entity. Use extension functions for clean syntax:

```kotlin
// infrastructure/persistence/mapper/WaitlistEntryMapper.kt
@Component
class WaitlistEntryMapper(
    private val jsonMapper: JsonMapper,  // Jackson 3.x
) {
    private val logger = LoggerFactory.getLogger(WaitlistEntryMapper::class.java)

    /**
     * Converts domain model to entity for persistence.
     */
    fun WaitlistEntry.toEntity(): WaitlistEntryEntity {
        val metadataJson = this.metadata?.let {
            try {
                Json.of(jsonMapper.writeValueAsString(it))
            } catch (e: JacksonException) {
                logger.error("Failed to serialize metadata for entry {}", this.id, e)
                null
            }
        }

        return WaitlistEntryEntity(
            id = this.id.id,
            email = this.email.value,
            sourceRaw = this.sourceRaw,
            sourceNormalized = this.sourceNormalized.value,
            language = this.language.code,
            ipHash = this.ipHash,
            metadata = metadataJson,
            createdBy = this.createdBy,
            createdAt = this.createdAt,
            updatedBy = this.updatedBy,
            updatedAt = this.updatedAt,
        )
    }

    /**
     * Converts entity to domain model.
     * Throws DomainMappingException if entity data is invalid.
     */
    fun WaitlistEntryEntity.toDomain(): WaitlistEntry {
        val metadata: Map<String, Any>? = this.metadata?.let { json ->
            try {
                @Suppress("UNCHECKED_CAST")
                jsonMapper.readValue(json.asString(), Map::class.java) as Map<String, Any>
            } catch (e: JacksonException) {
                logger.error("Failed to parse metadata JSON for entry {}", this.id, e)
                null
            }
        }

        val email = try {
            Email(this.email)
        } catch (e: IllegalArgumentException) {
            logger.error("Invalid email '{}' for entry {}", this.email, this.id)
            throw DomainMappingException("Invalid email for entry ${this.id}", e)
        }

        val language = try {
            Language.fromString(this.language)
        } catch (e: IllegalArgumentException) {
            logger.error("Invalid language '{}' for entry {}", this.language, this.id)
            throw DomainMappingException("Invalid language for entry ${this.id}", e)
        }

        return WaitlistEntry(
            id = WaitlistEntryId(this.id),
            email = email,
            sourceRaw = this.sourceRaw,
            sourceNormalized = WaitlistSource.fromString(this.sourceNormalized),
            language = language,
            ipHash = this.ipHash,
            metadata = metadata,
            createdBy = this.createdBy,
            createdAt = this.createdAt,
            updatedBy = this.updatedBy,
            updatedAt = this.updatedAt,
        )
    }
}
```

## Using Mappers in Repositories

Use `with(mapper) { ... }` for clean invocation:

```kotlin
@Repository
class WaitlistStoreR2dbcRepository(
    private val waitlistR2dbcRepository: WaitlistR2dbcRepository,
    private val waitlistEntryMapper: WaitlistEntryMapper,
) : WaitlistRepository {

    override suspend fun save(entry: WaitlistEntry): WaitlistEntry {
        val entity = with(waitlistEntryMapper) { entry.toEntity() }
        val savedEntity = waitlistR2dbcRepository.save(entity)
        return with(waitlistEntryMapper) { savedEntity.toDomain() }
    }

    override suspend fun findByEmail(email: Email): WaitlistEntry? {
        val entity = waitlistR2dbcRepository.findByEmail(email.value)
        return entity?.let { with(waitlistEntryMapper) { it.toDomain() } }
    }
}
```

## Auditing Configuration

Enable auditing for `@CreatedDate`, `@LastModifiedDate`, etc.:

```kotlin
@Configuration
@EnableR2dbcAuditing
class R2dbcConfig {
    @Bean
    fun auditorAware(): ReactiveAuditorAware<String> {
        return ReactiveAuditorAware {
            // Get current user from security context
            ReactiveSecurityContextHolder.getContext()
                .map { it.authentication?.name ?: "system" }
                .defaultIfEmpty("system")
        }
    }
}
```

## Folder Structure

```markdown
feature/
└── infrastructure/
└── persistence/
├── entity/
│ └── {Feature}Entity.kt # @Table data class
├── mapper/
│ └── {Feature}Mapper.kt # @Component with extension functions
├── repository/
│ └── {Feature}R2dbcRepository.kt
└── {Feature}StoreR2dbcRepository.kt
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Exposing entity to domain
class WaitlistEntry(
    val entity: WaitlistEntryEntity,  // Never store entity in domain!
)

// ✅ CORRECT: Domain has its own properties
class WaitlistEntry(
    val id: WaitlistEntryId,
    val email: Email,
    val source: WaitlistSource,
    // ... domain properties
)

// ❌ WRONG: Mapper without error handling
fun WaitlistEntryEntity.toDomain(): WaitlistEntry = WaitlistEntry(
    email = Email(this.email),  // May throw!
)

// ✅ CORRECT: Handle invalid data gracefully
fun WaitlistEntryEntity.toDomain(): WaitlistEntry {
    val email = try {
        Email(this.email)
    } catch (e: IllegalArgumentException) {
        throw DomainMappingException("Invalid email in entity ${this.id}", e)
    }
    // ...
}

// ❌ WRONG: Entity with business logic
@Table("users")
data class UserEntity(...) {
    fun isAdmin(): Boolean = roles.contains("ADMIN")  // Logic in entity!
}

// ✅ CORRECT: Entity is pure data
@Table("users")
data class UserEntity(
    @Id val id: UUID,
    val email: String,
    val roles: String,  // Stored as comma-separated or JSONB
    // ... no methods
)
```

## Related References

- [repositories.md](./repositories.md) - How entities are used in repositories
- [configuration.md](./configuration.md) - R2DBC and auditing configuration
