# Ktor Error Handling Rules

## ktor-error-comprehensive - Implement comprehensive error handling

Handle all types of network errors with specific error types.

### Incorrect

```kotlin
class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): User {
        return client.get("$BASE_URL/users/$id").body()
    }
}
```

### Correct

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val exception: ApiException) : ApiResult<Nothing>()
}

sealed class ApiException(message: String, cause: Throwable? = null) : Exception(message, cause) {
    class Network(cause: Throwable) : ApiException("Network error", cause)
    class Timeout(cause: Throwable) : ApiException("Request timed out", cause)
    class Client(val code: Int, message: String) : ApiException("Client error: $code - $message")
    class Server(val code: Int, message: String) : ApiException("Server error: $code - $message")
    class Parse(cause: Throwable) : ApiException("Failed to parse response", cause)
    class Unknown(cause: Throwable) : ApiException("Unknown error", cause)
}

class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): ApiResult<User> = safeApiCall {
        client.get("$BASE_URL/users/$id").body()
    }

    private suspend fun <T> safeApiCall(block: suspend () -> T): ApiResult<T> {
        return try {
            ApiResult.Success(block())
        } catch (e: CancellationException) {
            throw e // Don't catch cancellation
        } catch (e: HttpRequestTimeoutException) {
            ApiResult.Error(ApiException.Timeout(e))
        } catch (e: ClientRequestException) {
            val body = e.response.bodyAsText()
            ApiResult.Error(ApiException.Client(e.response.status.value, body))
        } catch (e: ServerResponseException) {
            val body = e.response.bodyAsText()
            ApiResult.Error(ApiException.Server(e.response.status.value, body))
        } catch (e: SerializationException) {
            ApiResult.Error(ApiException.Parse(e))
        } catch (e: IOException) {
            ApiResult.Error(ApiException.Network(e))
        } catch (e: Exception) {
            ApiResult.Error(ApiException.Unknown(e))
        }
    }
}
```

---

## ktor-error-status - Handle HTTP status codes properly

Map HTTP status codes to appropriate error types.

### Correct

```kotlin
sealed class HttpError(val code: Int, message: String) : Exception(message) {
    // 4xx Client errors
    class BadRequest(message: String) : HttpError(400, message)
    class Unauthorized(message: String) : HttpError(401, message)
    class Forbidden(message: String) : HttpError(403, message)
    class NotFound(message: String) : HttpError(404, message)
    class Conflict(message: String) : HttpError(409, message)
    class UnprocessableEntity(val errors: Map<String, List<String>>) : HttpError(422, "Validation failed")

    // 5xx Server errors
    class InternalServer(message: String) : HttpError(500, message)
    class ServiceUnavailable(message: String) : HttpError(503, message)
    class GatewayTimeout(message: String) : HttpError(504, message)

    // Unknown
    class Unknown(code: Int, message: String) : HttpError(code, message)
}

fun HttpResponse.toError(): HttpError {
    val body = runBlocking { bodyAsText() }
    return when (status.value) {
        400 -> HttpError.BadRequest(body)
        401 -> HttpError.Unauthorized(body)
        403 -> HttpError.Forbidden(body)
        404 -> HttpError.NotFound(body)
        409 -> HttpError.Conflict(body)
        422 -> {
            val errors = Json.decodeFromString<ValidationErrors>(body)
            HttpError.UnprocessableEntity(errors.errors)
        }
        500 -> HttpError.InternalServer(body)
        503 -> HttpError.ServiceUnavailable(body)
        504 -> HttpError.GatewayTimeout(body)
        else -> HttpError.Unknown(status.value, body)
    }
}
```

---

## ktor-error-retry - Implement retry logic for transient failures

Add retry logic with exponential backoff.

### Correct

```kotlin
suspend fun <T> retryWithBackoff(
    times: Int = 3,
    initialDelayMs: Long = 100,
    maxDelayMs: Long = 10000,
    factor: Double = 2.0,
    shouldRetry: (Exception) -> Boolean = { it.isRetryable() },
    block: suspend () -> T
): T {
    var currentDelay = initialDelayMs
    repeat(times - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            if (!shouldRetry(e)) throw e

            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelayMs)
        }
    }
    return block() // Last attempt
}

private fun Exception.isRetryable(): Boolean = when (this) {
    is CancellationException -> false
    is HttpRequestTimeoutException -> true
    is ConnectException -> true
    is ServerResponseException -> response.status.value in 500..599
    else -> false
}

// Or use Ktor's built-in retry
val client = HttpClient {
    install(HttpRequestRetry) {
        retryOnServerErrors(maxRetries = 3)
        retryOnException(maxRetries = 3, retryOnTimeout = true)
        exponentialDelay()
    }
}
```

---

## ktor-error-propagate - Propagate errors to UI appropriately

Transform API errors to user-friendly messages.

### Correct

```kotlin
class UserViewModel(private val api: UserApi) : ViewModel() {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    fun loadUser(userId: String) {
        viewModelScope.launch {
            _state.value = UiState.Loading

            when (val result = api.getUser(userId)) {
                is ApiResult.Success -> {
                    _state.value = UiState.Success(result.data)
                }
                is ApiResult.Error -> {
                    _state.value = UiState.Error(result.exception.toUserMessage())
                }
            }
        }
    }
}

private fun ApiException.toUserMessage(): String = when (this) {
    is ApiException.Network -> "No internet connection. Please check your network."
    is ApiException.Timeout -> "Request timed out. Please try again."
    is ApiException.Client -> when (code) {
        401 -> "Session expired. Please login again."
        403 -> "You don't have permission to perform this action."
        404 -> "The requested resource was not found."
        else -> "Invalid request. Please try again."
    }
    is ApiException.Server -> "Server error. Please try again later."
    is ApiException.Parse -> "Unexpected response format."
    is ApiException.Unknown -> "Something went wrong. Please try again."
}
```

---

## ktor-error-logging - Log errors for debugging

Log errors with appropriate context for debugging.

### Correct

```kotlin
class ApiClient(
    private val client: HttpClient,
    private val logger: Logger
) {
    suspend fun <T> request(
        path: String,
        method: HttpMethod = HttpMethod.Get,
        block: suspend () -> T
    ): ApiResult<T> {
        val requestId = UUID.randomUUID().toString().take(8)

        logger.d("API", "[$requestId] $method $path")

        return try {
            val result = block()
            logger.d("API", "[$requestId] Success")
            ApiResult.Success(result)
        } catch (e: ClientRequestException) {
            logger.w("API", "[$requestId] Client error: ${e.response.status}", e)
            ApiResult.Error(e.toApiException())
        } catch (e: ServerResponseException) {
            logger.e("API", "[$requestId] Server error: ${e.response.status}", e)
            ApiResult.Error(e.toApiException())
        } catch (e: Exception) {
            if (e is CancellationException) throw e
            logger.e("API", "[$requestId] Failed: ${e.message}", e)
            ApiResult.Error(e.toApiException())
        }
    }
}
```
