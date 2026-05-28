# Repositories - R2DBC Adapters

Repository adapters implement **domain repository ports** using Spring Data R2DBC.
They live in the infrastructure layer and translate between domain models and database entities.

## Architecture Pattern

```markdown
Domain Layer (Port)              Infrastructure Layer (Adapter)
┌─────────────────────┐          ┌─────────────────────────────────────┐
│ WaitlistRepository  │◄─────────│ WaitlistStoreR2dbcRepository        │
│ (interface)         │          │ (implements domain interface)       │
│                     │          │                                     │
│ + save(entry)       │          │ - WaitlistR2dbcRepository (Spring)  │
│ + findByEmail()     │          │ - WaitlistEntryMapper               │
└─────────────────────┘          └─────────────────────────────────────┘
```

## Domain Repository Port

The domain layer defines the contract. **NO Spring annotations**:

```kotlin
// domain/WaitlistRepository.kt
interface WaitlistRepository {
    suspend fun save(entry: WaitlistEntry): WaitlistEntry
    suspend fun findByEmail(email: Email): WaitlistEntry?
    suspend fun existsByEmail(email: Email): Boolean
    suspend fun count(): Long
}
```

## Spring Data R2DBC Repository

The raw Spring Data interface for database operations:

```kotlin
// infrastructure/persistence/repository/WaitlistR2dbcRepository.kt
@Repository
interface WaitlistR2dbcRepository : CoroutineCrudRepository<WaitlistEntryEntity, UUID> {

    suspend fun findByEmail(email: String): WaitlistEntryEntity?

    suspend fun existsByEmail(email: String): Boolean

    fun findBySourceRaw(sourceRaw: String): Flow<WaitlistEntryEntity>

    fun findBySourceNormalized(sourceNormalized: String): Flow<WaitlistEntryEntity>

    @Query("SELECT COUNT(*) FROM waitlist WHERE source_raw = :sourceRaw")
    suspend fun countBySourceRaw(sourceRaw: String): Long

    @Query("SELECT COUNT(*) FROM waitlist WHERE source_normalized = :sourceNormalized")
    suspend fun countBySourceNormalized(sourceNormalized: String): Long
}
```

### Repository Interface Options

| Interface                        | Operations        | Return Types            |
|----------------------------------|-------------------|-------------------------|
| `CoroutineCrudRepository<T, ID>` | Coroutine-based   | `suspend`, `Flow`       |
| `ReactiveCrudRepository<T, ID>`  | Reactive-based    | `Mono`, `Flux`          |
| `R2dbcRepository<T, ID>`         | Extended reactive | `Mono`, `Flux` + paging |

**Prefer `CoroutineCrudRepository`** for Kotlin projects with coroutines.

## Repository Adapter (Store)

The adapter implements the domain port, using the Spring repository and mapper:

```kotlin
// infrastructure/persistence/WaitlistStoreR2dbcRepository.kt
@Repository
class WaitlistStoreR2dbcRepository(
    private val waitlistR2dbcRepository: WaitlistR2dbcRepository,
    private val waitlistEntryMapper: WaitlistEntryMapper,
) : WaitlistRepository {

    override suspend fun save(entry: WaitlistEntry): WaitlistEntry {
        logger.debug("Saving waitlist entry with ID: {}", entry.id.id)
        return try {
            val entity = with(waitlistEntryMapper) { entry.toEntity() }
            val savedEntity = waitlistR2dbcRepository.save(entity)
            logger.info("Successfully saved waitlist entry with ID: {}", entry.id.id)
            with(waitlistEntryMapper) { savedEntity.toDomain() }
        } catch (error: Exception) {
            logger.error("Failed to save waitlist entry with ID: {}", entry.id.id, error)
            throw error
        }
    }

    override suspend fun findByEmail(email: Email): WaitlistEntry? {
        logger.debug("Finding waitlist entry by email")
        val entity = waitlistR2dbcRepository.findByEmail(email.value)
        return entity?.let { with(waitlistEntryMapper) { it.toDomain() } }
    }

    override suspend fun existsByEmail(email: Email): Boolean {
        logger.debug("Checking if email exists in waitlist")
        return waitlistR2dbcRepository.existsByEmail(email.value)
    }

    override suspend fun count(): Long {
        logger.debug("Counting total waitlist entries")
        return waitlistR2dbcRepository.count()
    }

    companion object {
        private val logger = LoggerFactory.getLogger(WaitlistStoreR2dbcRepository::class.java)
    }
}
```

## Naming Convention

| Component             | Naming Pattern                  | Example                        |
|-----------------------|---------------------------------|--------------------------------|
| Domain port           | `{Feature}Repository`           | `WaitlistRepository`           |
| Spring Data interface | `{Feature}R2dbcRepository`      | `WaitlistR2dbcRepository`      |
| Adapter class         | `{Feature}StoreR2dbcRepository` | `WaitlistStoreR2dbcRepository` |
| Entity                | `{Feature}Entity`               | `WaitlistEntryEntity`          |
| Mapper                | `{Feature}Mapper`               | `WaitlistEntryMapper`          |

## Folder Structure

```markdown
feature/
├── domain/
│ └── {Feature}Repository.kt # Port interface (NO Spring)
└── infrastructure/
└── persistence/
├── entity/
│ └── {Feature}Entity.kt # @Table entity
├── mapper/
│ └── {Feature}Mapper.kt # Domain ↔ Entity mapping
├── repository/
│ └── {Feature}R2dbcRepository.kt # Spring Data interface
└── {Feature}StoreR2dbcRepository.kt # Adapter implementing port
```

## Custom Queries

Use `@Query` for complex operations:

```kotlin
@Repository
interface WaitlistR2dbcRepository : CoroutineCrudRepository<WaitlistEntryEntity, UUID> {

    // Simple derived query
    suspend fun findByEmail(email: String): WaitlistEntryEntity?

    // Custom query with parameters
    @Query("SELECT COUNT(*) FROM waitlist WHERE source_raw = :sourceRaw")
    suspend fun countBySourceRaw(sourceRaw: String): Long

    // Query returning Flow for streaming
    @Query("SELECT * FROM waitlist WHERE created_at > :since ORDER BY created_at DESC")
    fun findRecentEntries(since: Instant): Flow<WaitlistEntryEntity>

    // Update query (returns affected row count)
    @Modifying
    @Query("UPDATE waitlist SET is_active = :isActive WHERE id = :id")
    suspend fun updateActiveStatus(id: UUID, isActive: Boolean): Int
}
```

## Transaction Management

> **Important**: In reactive Spring (R2DBC), `@Transactional` works with reactive types
> (`Mono`, `Flux`, `Flow`), but **NOT reliably with `suspend` functions**.
> For coroutines, use `TransactionalOperator.executeAndAwait`.
>
>
See: [Spring Framework 6.2 - Coroutines Transactions](https://docs.spring.io/spring-framework/reference/languages/kotlin/coroutines.html)

### For `suspend` Functions - Use TransactionalOperator

```kotlin
import org.springframework.transaction.reactive.TransactionalOperator
import org.springframework.transaction.reactive.executeAndAwait

@Repository
class WorkspaceStoreR2dbcRepository(
    private val r2dbcRepository: WorkspaceR2dbcRepository,
    private val memberRepository: MemberR2dbcRepository,
    private val txOperator: TransactionalOperator,
) : WorkspaceRepository {

    override suspend fun createWithMembers(
        workspace: Workspace,
        members: List<WorkspaceMember>,
    ) = txOperator.executeAndAwait {
        r2dbcRepository.save(workspace.toEntity())
        members.forEach { memberRepository.save(it.toEntity()) }
        // All operations in single transaction
    }
}
```

### For `Flow` - Use transactional Extension

```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import org.springframework.transaction.reactive.transactional

class PersonRepository(private val txOperator: TransactionalOperator) {

    fun updateAllPeople(): Flow<Person> =
        findPeople()
            .map { updatePerson(it) }
            .transactional(txOperator)  // Wraps Flow in transaction

    private fun findPeople(): Flow<Person> { /* ... */
    }
    private suspend fun updatePerson(person: Person): Person { /* ... */
    }
}
```

### For Reactive Types (`Mono`/`Flux`) - @Transactional Works

```kotlin
// ✅ @Transactional works with Mono/Flux return types
@Transactional
class ReactivePersonService : PersonService {

    override fun createAndFind(name: String): Mono<Person> {
        return repository.save(Person(name))
            .flatMap { saved -> repository.findById(saved.id) }
    }

    override fun findAll(): Flow<Person> {
        return repository.findAll()  // Flow also works with @Transactional
    }
}
```

### TransactionalOperator Configuration

```kotlin
@Configuration
class TransactionConfig {

    @Bean
    fun transactionalOperator(
        transactionManager: ReactiveTransactionManager,
    ): TransactionalOperator = TransactionalOperator.create(transactionManager)
}
```

### Summary: When to Use What

| Return Type   | Transaction Approach                        |
|---------------|---------------------------------------------|
| `suspend fun` | `TransactionalOperator.executeAndAwait`     |
| `Flow<T>`     | `.transactional(operator)` extension        |
| `Mono<T>`     | `@Transactional` or `TransactionalOperator` |
| `Flux<T>`     | `@Transactional` or `TransactionalOperator` |

## Anti-Patterns

```kotlin
// ❌ WRONG: Domain port extending Spring interface
interface UserRepository : ReactiveCrudRepository<UserEntity, UUID> {
    // Domain port must NOT extend Spring interfaces!
}

// ✅ CORRECT: Pure Kotlin interface for domain port
interface UserRepository {
    suspend fun save(user: User): User
    suspend fun findById(id: UserId): User?
}

// ❌ WRONG: Exposing entities from adapter
@Repository
class UserStoreR2dbcRepository(...) : UserRepository {
    override suspend fun findById(id: UserId): UserEntity? {  // WRONG return type!
        return userR2dbcRepository.findById(id.value)
    }
}

// ✅ CORRECT: Return domain objects
@Repository
class UserStoreR2dbcRepository(...) : UserRepository {
    override suspend fun findById(id: UserId): User? {
        return userR2dbcRepository.findById(id.value)
            ?.let { with(mapper) { it.toDomain() } }
    }
}

// ❌ WRONG: Using block() in adapter
override suspend fun findById(id: UserId): User? {
    return userR2dbcRepository.findById(id.value).block()  // NEVER block!
}

// ✅ CORRECT: Use await extensions
override suspend fun findById(id: UserId): User? {
    return userR2dbcRepository.findById(id.value).awaitSingleOrNull()
}
```

## Related References

- [entities-mappers.md](./entities-mappers.md) - Entity definitions and mappers
- [webflux-coroutines.md](./webflux-coroutines.md) - Reactive/coroutine patterns
- [configuration.md](./configuration.md) - R2DBC connection configuration
