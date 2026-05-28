# WebFlux and Coroutines

Patterns for reactive programming with Spring WebFlux and Kotlin coroutines.

## Core Rule: NEVER Block

```kotlin
// ❌ NEVER use block() in application code
val user = userRepository.findById(id).block()  // WRONG!

// ✅ Use coroutines with suspend
suspend fun getUser(id: UUID): User {
    return userRepository.findById(id).awaitSingleOrNull()
        ?: throw NotFoundException("User not found")
}

// ✅ Or stay in reactive
fun getUser(id: UUID): Mono<User> {
    return userRepository.findById(id)
        .switchIfEmpty(Mono.error(NotFoundException("User not found")))
}
```

## Choosing Your Model

| Scenario                      | Recommendation                                   |
|-------------------------------|--------------------------------------------------|
| Controllers, handlers         | Prefer `suspend fun` for coroutine-first design  |
| Library code, reactive chains | Use `Mono<T>`/`Flux<T>` for composability        |
| Repository methods            | `suspend fun` with `CoroutineCrudRepository`     |
| WebClient calls               | Convert at boundary, don't suspend inside chains |

## Suspend Functions in Controllers

Controllers use `suspend` functions for endpoints:

```kotlin
@RestController
class UserController(private val mediator: Mediator) : ApiController(mediator) {

    @GetMapping("/users/{id}")
    suspend fun getUser(@PathVariable id: UUID): ResponseEntity<UserResponse> {
        val query = GetUserQuery(id)
        val user = dispatch(query)  // suspend call
        return ResponseEntity.ok(user.toResponse())
    }

    @PostMapping("/users")
    suspend fun createUser(
        @Valid @RequestBody request: CreateUserRequest,
    ): ResponseEntity<UserIdResponse> {
        val command = CreateUserCommand(request.email)
        val userId = dispatch(command)  // suspend call
        return ResponseEntity.created(URI.create("/users/$userId")).body(UserIdResponse(userId))
    }
}
```

## Repository Layer with Coroutines

Use `CoroutineCrudRepository` for coroutine-native repositories:

```kotlin
// Spring Data interface
interface UserR2dbcRepository : CoroutineCrudRepository<UserEntity, UUID> {
    suspend fun findByEmail(email: String): UserEntity?
    suspend fun existsByEmail(email: String): Boolean
    fun findAllByIsActive(isActive: Boolean): Flow<UserEntity>
}

// Adapter using suspend functions
@Repository
class UserStoreR2dbcRepository(
    private val r2dbcRepository: UserR2dbcRepository,
    private val mapper: UserMapper,
) : UserRepository {

    override suspend fun findById(id: UserId): User? {
        return r2dbcRepository.findById(id.value)
            ?.let { with(mapper) { it.toDomain() } }
    }

    override suspend fun findAll(): List<User> {
        return r2dbcRepository.findAll()
            .map { with(mapper) { it.toDomain() } }
            .toList()
    }
}
```

## Converting Between Reactive and Coroutines

### Mono/Flux to Suspend

```kotlin
// Mono to suspend (single value)
suspend fun getUser(id: UUID): User? {
    return userReactiveRepository.findById(id).awaitSingleOrNull()
}

// Mono to suspend (required value)
suspend fun getRequiredUser(id: UUID): User {
    return userReactiveRepository.findById(id).awaitSingle()
}

// Flux to List
suspend fun getAllUsers(): List<User> {
    return userReactiveRepository.findAll().collectList().awaitSingle()
}

// Flux to Flow
fun getAllUsersFlow(): Flow<User> {
    return userReactiveRepository.findAll().asFlow()
}
```

### Suspend to Mono/Flux

```kotlin
// Suspend to Mono
fun getUserMono(id: UUID): Mono<User> = mono {
    getUserSuspend(id)
}

// Suspend to Flux (via Flow)
fun getUsersFlux(): Flux<User> = flux {
    getAllUsersSuspend().forEach { emit(it) }
}
```

## WebClient with Coroutines

```kotlin
@Component
class ExternalApiClient(
    private val webClient: WebClient,
) {
    suspend fun fetchData(id: String): ExternalData {
        return webClient.get()
            .uri("/data/{id}", id)
            .retrieve()
            .bodyToMono(ExternalData::class.java)
            .awaitSingle()
    }

    suspend fun fetchDataOrNull(id: String): ExternalData? {
        return webClient.get()
            .uri("/data/{id}", id)
            .retrieve()
            .bodyToMono(ExternalData::class.java)
            .awaitSingleOrNull()
    }

    // Handling errors
    suspend fun fetchDataWithErrorHandling(id: String): ExternalData {
        return webClient.get()
            .uri("/data/{id}", id)
            .retrieve()
            .onStatus({ it.is4xxClientError }) {
                Mono.error(NotFoundException("Data not found: $id"))
            }
            .onStatus({ it.is5xxServerError }) {
                Mono.error(ExternalServiceException("External service error"))
            }
            .bodyToMono(ExternalData::class.java)
            .awaitSingle()
    }
}
```

## Parallel Execution

```kotlin
suspend fun fetchUserWithOrganization(userId: UUID): UserWithOrg {
    // Sequential (one after another)
    val user = userRepository.findById(userId).awaitSingle()
    val org = orgRepository.findById(user.orgId).awaitSingle()
    return UserWithOrg(user, org)
}

suspend fun fetchUserWithOrganizationParallel(userId: UUID, orgId: UUID): UserWithOrg {
    // Parallel execution with coroutineScope
    return coroutineScope {
        val userDeferred = async { userRepository.findById(userId).awaitSingle() }
        val orgDeferred = async { orgRepository.findById(orgId).awaitSingle() }

        UserWithOrg(userDeferred.await(), orgDeferred.await())
    }
}
```

## Error Handling in Reactive Chains

```kotlin
// ✅ CORRECT: Handle errors at the end of the chain
fun findUser(id: UUID): Mono<User> {
    return userRepository.findById(id)
        .switchIfEmpty(Mono.error(NotFoundException("User not found: $id")))
        .onErrorMap { ex ->
            when (ex) {
                is DataAccessException -> RepositoryException("Database error", ex)
                else -> ex
            }
        }
}

// ✅ CORRECT: In suspend functions, use try-catch or Result
suspend fun findUserSafe(id: UUID): Result<User> = runCatching {
    userRepository.findById(id).awaitSingle()
}
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Mixing suspend inside reactive operators
fun findUserWithOrg(userId: UUID): Mono<UserWithOrg> {
    return userRepository.findById(userId)
        .flatMap { user ->
            runBlocking { orgService.findById(user.orgId) }  // NEVER!
        }
}

// ✅ CORRECT: Stay reactive
fun findUserWithOrg(userId: UUID): Mono<UserWithOrg> {
    return userRepository.findById(userId)
        .flatMap { user ->
            orgRepository.findById(user.orgId)
                .map { org -> UserWithOrg(user, org) }
        }
}

// ✅ CORRECT: Or use suspend throughout
suspend fun findUserWithOrg(userId: UUID): UserWithOrg {
    val user = userRepository.findById(userId).awaitSingle()
    val org = orgRepository.findById(user.orgId).awaitSingle()
    return UserWithOrg(user, org)
}

// ❌ WRONG: Using GlobalScope
GlobalScope.launch {
    emailService.sendNotification(user)  // Fire and forget - bad!
}

// ✅ CORRECT: Use structured concurrency
suspend fun createUserWithNotification(user: User) = coroutineScope {
    val savedUser = userRepository.save(user)
    launch {
        emailService.sendWelcome(savedUser)  // Structured, cancellable
    }
    savedUser
}
```

## Transactions with Suspend Functions

> **Important**: `@Transactional` does NOT work reliably with `suspend` functions.
> Use `TransactionalOperator.executeAndAwait` instead.
>
>
See: [Spring Framework 6.2 - Coroutines Transactions](https://docs.spring.io/spring-framework/reference/languages/kotlin/coroutines.html)

```kotlin
import org.springframework.transaction.reactive.TransactionalOperator
import org.springframework.transaction.reactive.executeAndAwait

@Repository
class UserStoreR2dbcRepository(
    private val r2dbcRepository: UserR2dbcRepository,
    private val roleRepository: RoleR2dbcRepository,
    private val txOperator: TransactionalOperator,
) : UserRepository {

    override suspend fun createWithRoles(user: User, roles: List<Role>) =
        txOperator.executeAndAwait {
            val savedUser = r2dbcRepository.save(user.toEntity())
            roles.forEach { role ->
                roleRepository.save(UserRole(savedUser.id, role.id))
            }
            savedUser
        }
}
```

For `Flow` operations, use the `transactional` extension:

```kotlin
fun updateAllUsers(): Flow<User> =
    findAllUsers()
        .map { updateUser(it) }
        .transactional(txOperator)
```

See [repositories.md - Transaction Management](./repositories.md#transaction-management) for
complete patterns.

## Related References

- [repositories.md](./repositories.md) - Repository patterns with coroutines
- [controllers.md](./controllers.md) - Suspend functions in controllers
