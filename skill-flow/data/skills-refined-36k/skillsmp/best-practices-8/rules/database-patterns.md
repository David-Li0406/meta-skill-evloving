---
title: Database Patterns
impact: HIGH
impactDescription: Non-blocking database access, data consistency
tags: r2dbc, repository, transaction, connection-pool, database
---

# Database Patterns

R2DBC enables non-blocking database access. JDBC blocks the event loop and should be avoided.

## Rule 1: Use R2DBC Not JDBC

```kotlin
// ❌ INCORRECT - blocking JDBC
@Repository
class UserRepository(
    private val jdbcTemplate: JdbcTemplate
) {
    fun findById(id: Long): User? {
        return jdbcTemplate.queryForObject(...)  // BLOCKS!
    }
}

// ✅ CORRECT - R2DBC with coroutines
@Repository
interface UserRepository : CoroutineCrudRepository<User, Long> {
    suspend fun findByEmail(email: String): User?

    @Query("SELECT * FROM users WHERE status = :status")
    fun findByStatus(status: String): Flow<User>
}
```

## Rule 2: Use CoroutineCrudRepository

```kotlin
// ✅ CORRECT - CoroutineCrudRepository for suspend functions
@Repository
interface OrderRepository : CoroutineCrudRepository<Order, Long> {

    // Suspend function for single result
    suspend fun findByOrderNumber(orderNumber: String): Order?

    // Flow for multiple results
    fun findByUserId(userId: Long): Flow<Order>

    // Custom query with suspend
    @Query("SELECT * FROM orders WHERE status = :status LIMIT :limit")
    suspend fun findTopByStatus(status: String, limit: Int): List<Order>
}

// ✅ CORRECT - use in service
@Service
class OrderService(
    private val orderRepository: OrderRepository
) {
    suspend fun getOrder(id: Long): Order {
        return orderRepository.findById(id)
            ?: throw OrderNotFoundException(id)
    }

    fun getUserOrders(userId: Long): Flow<Order> {
        return orderRepository.findByUserId(userId)
    }
}
```

## Rule 3: Handle Transactions Correctly

```kotlin
// ❌ INCORRECT - no transaction for multiple operations
suspend fun transferMoney(from: Long, to: Long, amount: BigDecimal) {
    val fromAccount = accountRepository.findById(from)!!
    fromAccount.balance -= amount
    accountRepository.save(fromAccount)  // committed

    val toAccount = accountRepository.findById(to)!!  // if this fails, money lost!
    toAccount.balance += amount
    accountRepository.save(toAccount)
}

// ✅ CORRECT - programmatic transaction with coroutines
@Service
class TransferService(
    private val transactionalOperator: TransactionalOperator,
    private val accountRepository: AccountRepository
) {
    suspend fun transferMoney(from: Long, to: Long, amount: BigDecimal) {
        transactionalOperator.executeAndAwait {
            val fromAccount = accountRepository.findById(from)
                ?: throw AccountNotFoundException(from)
            val toAccount = accountRepository.findById(to)
                ?: throw AccountNotFoundException(to)

            if (fromAccount.balance < amount) {
                throw InsufficientFundsException()
            }

            accountRepository.save(fromAccount.copy(balance = fromAccount.balance - amount))
            accountRepository.save(toAccount.copy(balance = toAccount.balance + amount))
        }
    }
}

// ✅ CORRECT - @Transactional with suspend
@Service
class OrderService(
    private val orderRepository: OrderRepository,
    private val inventoryRepository: InventoryRepository
) {
    @Transactional
    suspend fun createOrder(order: Order): Order {
        val savedOrder = orderRepository.save(order)
        inventoryRepository.decrementStock(order.productId, order.quantity)
        return savedOrder
    }
}
```

## Rule 4: Configure Connection Pool

```kotlin
// ✅ CORRECT - R2DBC pool configuration
@Configuration
class R2dbcConfig {

    @Bean
    fun connectionFactory(): ConnectionFactory {
        val connectionFactory = ConnectionFactories.get(
            ConnectionFactoryOptions.builder()
                .option(DRIVER, "pool")
                .option(PROTOCOL, "postgresql")
                .option(HOST, "localhost")
                .option(DATABASE, "mydb")
                .option(USER, System.getenv("DB_USER"))
                .option(PASSWORD, System.getenv("DB_PASSWORD"))
                .build()
        )

        val poolConfig = ConnectionPoolConfiguration.builder(connectionFactory)
            .maxIdleTime(Duration.ofMinutes(10))
            .maxSize(20)
            .initialSize(5)
            .maxCreateConnectionTime(Duration.ofSeconds(5))
            .validationQuery("SELECT 1")
            .build()

        return ConnectionPool(poolConfig)
    }
}
```

## Rule 5: Avoid N+1 Queries

```kotlin
// ❌ INCORRECT - N+1 queries
suspend fun getUsersWithOrders(): List<UserWithOrders> {
    val users = userRepository.findAll().toList()
    return users.map { user ->
        val orders = orderRepository.findByUserId(user.id).toList()  // N queries!
        UserWithOrders(user, orders)
    }
}

// ✅ CORRECT - batch fetch
suspend fun getUsersWithOrders(): List<UserWithOrders> {
    val users = userRepository.findAll().toList()
    val userIds = users.map { it.id }

    // Single batch query for all orders
    val ordersByUser = orderRepository.findByUserIdIn(userIds)
        .toList()
        .groupBy { it.userId }

    return users.map { user ->
        UserWithOrders(user, ordersByUser[user.id] ?: emptyList())
    }
}
```

## Detection Checklist

Look for these database anti-patterns:

- [ ] `JdbcTemplate` or blocking database drivers
- [ ] `ReactiveCrudRepository` returning `Mono/Flux` instead of `CoroutineCrudRepository`
- [ ] Multiple `repository.save()` calls without `@Transactional` or `transactionalOperator`
- [ ] Iterating over entities and querying per item (N+1)
- [ ] Database credentials in source code instead of environment variables
