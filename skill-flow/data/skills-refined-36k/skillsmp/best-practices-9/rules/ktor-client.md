# Ktor Client Rules

## ktor-client-config - Configure HttpClient properly

Create a properly configured HttpClient with all necessary plugins.

### Incorrect

```kotlin
val client = HttpClient()
```

### Correct

```kotlin
val client = HttpClient(CIO) {
    // JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
            coerceInputValues = true
        })
    }

    // Timeouts
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 10_000
        socketTimeoutMillis = 30_000
    }

    // Logging (debug builds only)
    install(Logging) {
        logger = Logger.DEFAULT
        level = LogLevel.HEADERS
        filter { request ->
            request.url.host.contains("api.example.com")
        }
    }

    // Default headers
    defaultRequest {
        header(HttpHeaders.ContentType, ContentType.Application.Json)
        header("X-App-Version", BuildConfig.VERSION_NAME)
    }

    // Response validation
    expectSuccess = true
    HttpResponseValidator {
        handleResponseExceptionWithRequest { exception, _ ->
            when (exception) {
                is ClientRequestException -> throw ApiException.Client(exception)
                is ServerResponseException -> throw ApiException.Server(exception)
                else -> throw exception
            }
        }
    }
}
```

---

## ktor-client-engine - Use platform-appropriate engine

Select the right HTTP engine for each platform.

### Correct

```kotlin
// commonMain
expect fun createHttpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient

// androidMain
actual fun createHttpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(OkHttp) {
        config()
        engine {
            config {
                connectTimeout(10, TimeUnit.SECONDS)
                readTimeout(30, TimeUnit.SECONDS)
            }
        }
    }
}

// iosMain
actual fun createHttpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(Darwin) {
        config()
        engine {
            configureRequest {
                setAllowsCellularAccess(true)
            }
        }
    }
}

// desktopMain (JVM)
actual fun createHttpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(CIO) {
        config()
    }
}
```

---

## ktor-client-singleton - Use single HttpClient instance

Reuse HttpClient across requests, don't create per-request.

### Incorrect

```kotlin
class UserApi {
    suspend fun getUser(id: String): User {
        // Wrong: Creates new client per request
        val client = HttpClient()
        return client.get("$BASE_URL/users/$id").body()
    }
}
```

### Correct

```kotlin
class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): User {
        return client.get("$BASE_URL/users/$id").body()
    }
}

// Koin module
val networkModule = module {
    single { createHttpClient() }
    single { UserApi(get()) }
}
```

---

## ktor-client-close - Close HttpClient properly

Close HttpClient when no longer needed to release resources.

### Correct

```kotlin
// Application-scoped client (closed on app termination)
class ApiClient(private val client: HttpClient) {
    fun close() {
        client.close()
    }
}

// Session-scoped client
class SessionManager {
    private var client: HttpClient? = null

    fun startSession() {
        client = createHttpClient()
    }

    fun endSession() {
        client?.close()
        client = null
    }
}

// One-off request with use
suspend fun quickFetch(url: String): String {
    return HttpClient().use { client ->
        client.get(url).bodyAsText()
    }
}
```

---

## ktor-client-interceptor - Use plugins for cross-cutting concerns

Add authentication, logging, and other concerns via plugins.

### Correct

```kotlin
val client = HttpClient {
    // Auth token injection
    install(Auth) {
        bearer {
            loadTokens {
                BearerTokens(tokenProvider.accessToken, tokenProvider.refreshToken)
            }
            refreshTokens {
                val newTokens = refreshTokens(oldTokens)
                BearerTokens(newTokens.access, newTokens.refresh)
            }
        }
    }

    // Request/response transformation
    install(HttpSend) {
        intercept { request ->
            // Add correlation ID to every request
            request.headers.append("X-Correlation-ID", UUID.randomUUID().toString())
            execute(request)
        }
    }

    // Retry on specific errors
    install(HttpRequestRetry) {
        retryOnServerErrors(maxRetries = 3)
        exponentialDelay()
    }
}
```
