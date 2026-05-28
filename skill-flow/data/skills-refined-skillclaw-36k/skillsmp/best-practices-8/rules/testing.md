---
title: Testing
impact: MEDIUM
impactDescription: Reliable coroutine tests, proper mocking
tags: runTest, MockK, coEvery, coVerify, Turbine, TestDispatcher
---

# Testing

Testing coroutines requires special utilities for virtual time control and suspend function mocking.

## Rule 1: Use runTest for Coroutine Tests

```kotlin
// ❌ INCORRECT - using runBlocking
@Test
fun `test with runBlocking`() = runBlocking {
    val result = suspendFunction()  // No virtual time control
    assertEquals(expected, result)
}

// ✅ CORRECT - use runTest
@Test
fun `test with runTest`() = runTest {
    val result = suspendFunction()  // Virtual time, instant delays
    assertEquals(expected, result)
}

// ✅ CORRECT - with virtual time control
@Test
fun `test delay completes instantly`() = runTest {
    coEvery { repository.findById(any()) } coAnswers {
        delay(1000)  // Completes instantly in runTest
        User(1L, "test@example.com")
    }

    val result = userService.getUser(1L)

    assertNotNull(result)
    // Test completes instantly despite delay
}
```

## Rule 2: Use MockK coEvery/coVerify

```kotlin
// ✅ CORRECT - MockK for coroutine mocking
class OrderServiceTest {

    private val orderRepository = mockk<OrderRepository>()
    private val paymentService = mockk<PaymentService>()
    private val orderService = OrderService(orderRepository, paymentService)

    @Test
    fun `should create order with payment`() = runTest {
        // Given
        val order = Order(productId = 1L, quantity = 2)
        val savedOrder = order.copy(id = 1L)

        coEvery { orderRepository.save(any()) } returns savedOrder
        coEvery { paymentService.processPayment(any()) } returns PaymentResult.SUCCESS

        // When
        val result = orderService.createOrder(order)

        // Then
        assertEquals(1L, result.id)

        coVerify(exactly = 1) { orderRepository.save(order) }
        coVerify(exactly = 1) { paymentService.processPayment(savedOrder) }
    }

    @Test
    fun `should handle payment failure`() = runTest {
        coEvery { orderRepository.save(any()) } returns Order(id = 1L)
        coEvery { paymentService.processPayment(any()) } throws PaymentException("Failed")

        assertThrows<PaymentException> {
            orderService.createOrder(Order())
        }
    }
}
```

## Rule 3: Use Turbine for Flow Testing

```kotlin
// build.gradle.kts
// testImplementation("app.cash.turbine:turbine:1.0.0")

// ✅ CORRECT - Turbine for Flow testing
class EventServiceTest {

    private val eventService = EventService()

    @Test
    fun `should emit events in order`() = runTest {
        eventService.events.test {
            // Trigger events
            eventService.emit(Event("first"))
            eventService.emit(Event("second"))

            // Assert emissions
            assertEquals(Event("first"), awaitItem())
            assertEquals(Event("second"), awaitItem())

            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `should handle flow errors`() = runTest {
        val errorFlow = flow {
            emit(1)
            throw RuntimeException("Error")
        }

        errorFlow.test {
            assertEquals(1, awaitItem())
            val error = awaitError()
            assertEquals("Error", error.message)
        }
    }
}
```

## Rule 4: Use TestDispatcher for Controlled Execution

```kotlin
// ✅ CORRECT - TestDispatcher for controlled execution
class TimerServiceTest {

    @Test
    fun `should emit at intervals`() = runTest {
        val testDispatcher = StandardTestDispatcher(testScheduler)
        val timerService = TimerService(testDispatcher)

        val emissions = mutableListOf<Long>()
        val job = launch {
            timerService.ticker(1000).take(3).collect { emissions.add(it) }
        }

        advanceTimeBy(3000)
        runCurrent()

        assertEquals(3, emissions.size)
        job.cancel()
    }
}

// ✅ CORRECT - inject dispatcher for testability
class DataRefresher(
    private val dispatcher: CoroutineDispatcher = Dispatchers.Default
) {
    suspend fun refresh() = withContext(dispatcher) {
        // ...
    }
}

@Test
fun `test data refresh`() = runTest {
    val refresher = DataRefresher(StandardTestDispatcher(testScheduler))
    refresher.refresh()
    advanceUntilIdle()
    // assertions
}
```

## Rule 5: Test with WebTestClient

```kotlin
// ✅ CORRECT - WebTestClient for integration tests
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserControllerIntegrationTest {

    @Autowired
    lateinit var webTestClient: WebTestClient

    @Test
    fun `should get user by id`() {
        webTestClient.get()
            .uri("/api/users/1")
            .exchange()
            .expectStatus().isOk
            .expectBody<User>()
            .consumeWith { result ->
                val user = result.responseBody!!
                assertEquals(1L, user.id)
            }
    }

    @Test
    fun `should stream users`() {
        webTestClient.get()
            .uri("/api/users/stream")
            .accept(MediaType.APPLICATION_NDJSON)
            .exchange()
            .expectStatus().isOk
            .returnResult<User>()
            .responseBody
            .test()
            .expectNextCount(10)
            .verifyComplete()
    }
}
```

## Rule 6: Use Testcontainers for Database

```kotlin
// ✅ CORRECT - Testcontainers with R2DBC
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    companion object {
        @Container
        val postgres = PostgreSQLContainer("postgres:15-alpine")

        @JvmStatic
        @DynamicPropertySource
        fun properties(registry: DynamicPropertyRegistry) {
            registry.add("spring.r2dbc.url") {
                "r2dbc:postgresql://${postgres.host}:${postgres.getMappedPort(5432)}/${postgres.databaseName}"
            }
            registry.add("spring.r2dbc.username") { postgres.username }
            registry.add("spring.r2dbc.password") { postgres.password }
        }
    }

    @Autowired
    lateinit var userRepository: UserRepository

    @Test
    fun `should save and retrieve user`() = runTest {
        val user = User(email = "test@example.com", name = "Test")
        val saved = userRepository.save(user)
        val retrieved = userRepository.findById(saved.id!!)

        assertNotNull(retrieved)
        assertEquals("test@example.com", retrieved?.email)
    }
}
```

## Detection Checklist

Look for these testing anti-patterns:

- [ ] `runBlocking` instead of `runTest` for coroutine tests
- [ ] `every` instead of `coEvery` for suspend functions
- [ ] `verify` instead of `coVerify` for suspend functions
- [ ] Flow tested without Turbine's `.test {}` extension
- [ ] Integration tests without `@Testcontainers` for database
- [ ] Hardcoded dispatchers instead of injected ones
