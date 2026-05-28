---
title: WebFlux Patterns
impact: MEDIUM
impactDescription: Non-blocking endpoints, reactive HTTP
tags: WebFlux, coRouter, WebClient, filter, controller
---

# WebFlux Patterns

Spring WebFlux enables non-blocking HTTP with native coroutine support.

## Rule 1: Use Suspend in Controllers

```kotlin
// ✅ CORRECT - suspend function in controller
@RestController
@RequestMapping("/api/users")
class UserController(
    private val userService: UserService
) {
    @GetMapping("/{id}")
    suspend fun getUser(@PathVariable id: Long): User {
        return userService.findById(id)
            ?: throw ResponseStatusException(HttpStatus.NOT_FOUND)
    }

    @GetMapping
    fun getAllUsers(): Flow<User> {  // Flow for streaming
        return userService.findAll()
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun createUser(@RequestBody user: User): User {
        return userService.save(user)
    }
}
```

## Rule 2: Use coRouter DSL

```kotlin
// ✅ CORRECT - coRouter for functional endpoints
@Configuration
class RouterConfig(
    private val userHandler: UserHandler
) {
    @Bean
    fun userRoutes() = coRouter {
        "/api/users".nest {
            GET("", userHandler::getAllUsers)
            GET("/{id}", userHandler::getUser)
            POST("", userHandler::createUser)
            PUT("/{id}", userHandler::updateUser)
        }

        filter { request, next ->
            val start = System.currentTimeMillis()
            val response = next(request)
            logger.info("${request.method()} ${request.path()} - ${System.currentTimeMillis() - start}ms")
            response
        }
    }
}
```

## Rule 3: Use WebClient with awaitBody

```kotlin
// ✅ CORRECT - WebClient with coroutine extensions
@Service
class ExternalApiService(
    private val webClient: WebClient
) {
    suspend fun fetchUser(userId: String): ExternalUser {
        return webClient.get()
            .uri("/users/{id}", userId)
            .retrieve()
            .awaitBody()
    }

    fun fetchUsers(): Flow<ExternalUser> {
        return webClient.get()
            .uri("/users")
            .retrieve()
            .bodyToFlow()
    }
}
```

## Rule 4: Use CoWebFilter

```kotlin
// ✅ CORRECT - CoWebFilter for coroutine-based filtering
@Component
class LoggingFilter : CoWebFilter() {

    override suspend fun filter(exchange: ServerWebExchange, chain: CoWebFilterChain) {
        val request = exchange.request
        val start = System.currentTimeMillis()

        try {
            chain.filter(exchange)
        } finally {
            logger.info("${request.method} ${request.path} - ${System.currentTimeMillis() - start}ms")
        }
    }
}
```

## Detection Checklist

- [ ] `RestTemplate` instead of `WebClient`
- [ ] Missing `suspend` on controller methods
- [ ] `router {}` instead of `coRouter {}`
- [ ] `WebFilter` instead of `CoWebFilter`
