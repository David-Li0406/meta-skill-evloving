---
name: metro-di-mobile
description: Use this skill when you need to implement compile-time dependency injection in Kotlin Multiplatform projects.
---

# Metro DI for Kotlin Multiplatform

Metro DI is a compile-time dependency injection framework for Kotlin Multiplatform (KMP), proven in production at Cash App.

## Setup

### build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.metro)
}

// Apply Metro plugin to modules that need DI
```

### libs.versions.toml

```toml
[versions]
metro = "0.1.1"

[plugins]
metro = { id = "dev.zacsweers.metro", version.ref = "metro" }
```

## Core Concepts

### @DependencyGraph

The root container for dependencies, typically one per application entry point.

```kotlin
// composeApp/src/commonMain/kotlin/di/AppGraph.kt
@DependencyGraph
interface AppGraph {
    // Expose dependencies
    val authRepository: AuthRepository
    val homeComponent: HomeComponent

    // Factory methods for runtime parameters
    fun createHomeComponent(context: ComponentContext): HomeComponent
}

// Create instance
val graph = createGraph<AppGraph>()
val authRepo = graph.authRepository
```

### @Provides

Define how to create instances of your dependencies.

```kotlin
@DependencyGraph
interface AppGraph {
    @Provides
    fun provideHttpClient(): HttpClient = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
            })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
        }
    }

    @Provides
    fun provideApiService(httpClient: HttpClient): ApiService =
        ApiServiceImpl(httpClient, "https://api.your-project.com")

    @Provides
    fun provideAuthRepository(api: ApiService, tokenStorage: TokenStorage): AuthRepository =
        AuthRepositoryImpl(api, tokenStorage)
}
```

### @Inject

Use constructor injection for classes.

```kotlin
@Inject
class AuthRepositoryImpl(
    private val api: ApiService,
    private val tokenStorage: TokenStorage
) : AuthRepository {
    override suspend fun login(email: String, password: String): AppResult<User> {
        // Implementation
    }
}

// Used in graph
@DependencyGraph
interface AppGraph {
    val authRepository: AuthRepository  // Metro knows to create AuthRepositoryImpl
}
```

### @BindingContainer

Group related providers into modules.

```kotlin
// core/network/src/commonMain/kotlin/di/NetworkModule.kt
@BindingContainer
class NetworkModule {
    @Provides
    fun provideHttpClient(): HttpClient = HttpClient(CIO)
}
```