---
name: metro-di-mobile
description: Use this skill for compile-time dependency injection, graphs, providers, and multi-module DI setup in Kotlin Multiplatform applications.
---

# Metro DI for Kotlin Multiplatform

Metro is a compile-time dependency injection framework for Kotlin Multiplatform (KMP), proven in production at Cash App.

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

Root container for dependencies, one per application entry point.

```kotlin
@DependencyGraph
interface AppGraph {
    val authRepository: AuthRepository
    val homeComponent: HomeComponent

    fun createHomeComponent(context: ComponentContext): HomeComponent
}

// Create instance
val graph = createGraph<AppGraph>()
val authRepo = graph.authRepository
```

### @Provides

Define how to create instances.

```kotlin
@DependencyGraph
interface AppGraph {
    @Provides
    fun provideHttpClient(): HttpClient = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
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

Constructor injection for classes.

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
```

### @BindingContainer

Group related providers into modules.

```kotlin
@BindingContainer
class NetworkModule {
    @Provides
    fun provideHttpClient(): HttpClient = HttpClient(CIO) {
        install(ContentNegotiation) { json() }
    }

    @Provides
    fun provideApiService(httpClient: HttpClient): ApiService =
        ApiServiceImpl(httpClient)
}

@BindingContainer
class DataModule {
    @Provides
    fun provideTokenStorage(): TokenStorage = TokenStorageImpl()

    @Provides
    fun providePreferencesDataStore(context: PlatformContext): DataStore<Preferences> =
        PreferenceDataStoreFactory.createWithPath(
            produceFile = { Path(createDataStorePath(context)) }
        )
}
```

### Platform-Specific Graphs

```kotlin
@BindingContainer
class AndroidPlatformModule {
    @Provides
    fun providePlatformContext(context: Context): PlatformContext = context

    @Provides
    fun provideTokenStorage(context: Context): TokenStorage =
        AndroidTokenStorage(context)
}

@BindingContainer
class IosPlatformModule {
    @Provides
    fun providePlatformContext(): PlatformContext = PlatformContext()

    @Provides
    fun provideTokenStorage(): TokenStorage = IosTokenStorage()
}

@DependencyGraph(
    bindingContainers = [
        CommonNetworkModule::class,
        CommonDataModule::class,
        AndroidPlatformModule::class
    ]
)
interface AndroidAppGraph {
    val authRepository: AuthRepository
    fun createRootComponent(context: ComponentContext): RootComponent
}

@DependencyGraph(
    bindingContainers = [
        CommonNetworkModule::class,
        CommonDataModule::class,
        IosPlatformModule::class
    ]
)
interface IosAppGraph {
    val authRepository: AuthRepository
    fun createRootComponent(context: ComponentContext): RootComponent
}
```

## Multi-Module DI Pattern

### Feature Module Bindings

```kotlin
@BindingContainer
class AuthModule {
    @Provides
    fun provideAuthRepository(api: ApiService, tokenStorage: TokenStorage): AuthRepository =
        AuthRepositoryImpl(api, tokenStorage)

    @Provides
    fun provideLoginUseCase(authRepository: AuthRepository): LoginUseCase = LoginUseCase(authRepository)
}

@BindingContainer
class HomeModule {
    @Provides
    fun provideHomeRepository(api: ApiService, database: AppDatabase): HomeRepository =
        HomeRepositoryImpl(api, database)
}
```

### Assembly in App Graph

```kotlin
@DependencyGraph(
    bindingContainers = [
        CommonNetworkModule::class,
        CommonDataModule::class,
        AndroidPlatformModule::class,
        AuthModule::class,
        HomeModule::class
    ]
)
interface AndroidAppGraph {
    val httpClient: HttpClient
    val authRepository: AuthRepository
    val homeRepository: HomeRepository

    fun createRootComponent(context: ComponentContext): RootComponent
}
```

## Advanced Features

### Scopes

```kotlin
@DependencyGraph(
    scope = "app",
    additionalScopes = ["activity"]
)
interface AppGraph {
    @Provides
    @Scope("app")
    fun provideAppDatabase(): AppDatabase = AppDatabase()

    @Provides
    @Scope("activity")
    fun provideNavigator(): Navigator = Navigator()
}
```

### Assisted Injection

For dependencies that need runtime parameters.

```kotlin
@Inject
class HomeComponent(
    private val repository: HomeRepository,
    @Assisted val componentContext: ComponentContext
) : ComponentContext by componentContext {
    // Component logic
}

@AssistedFactory
interface HomeComponentFactory {
    fun create(componentContext: ComponentContext): HomeComponent
}
```

### Lazy and Provider

```kotlin
@Inject
class SomeService(
    private val lazyDatabase: Lazy<AppDatabase>,
    private val userProvider: Provider<User>
) {
    fun doWork() {
        val db = lazyDatabase.value
        val user1 = userProvider.get()
        val user2 = userProvider.get()
    }
}
```

### Multibindings

```kotlin
@DependencyGraph
interface AppGraph {
    @Multibinds
    val interceptors: Set<Interceptor>

    @Multibinds
    val handlers: Map<String, Handler>
}
```

## Decompose Integration

### Component with DI

```kotlin
interface HomeComponent {
    val state: Value<HomeState>
    fun onItemClick(item: HomeItem)
}

@Inject
class DefaultHomeComponent(
    private val repository: HomeRepository,
    @Assisted componentContext: ComponentContext
) : HomeComponent, ComponentContext by componentContext {
    // Implementation
}
```

### Root Component Factory

```kotlin
interface RootComponent {
    val childStack: Value<ChildStack<Config, Child>>

    sealed class Child {
        data class Auth(val component: AuthComponent) : Child()
        data class Home(val component: HomeComponent) : Child()
    }
}

@Inject
class DefaultRootComponent(
    private val authComponentFactory: AuthComponent.Factory,
    private val homeComponentFactory: HomeComponent.Factory,
    @Assisted componentContext: ComponentContext
) : RootComponent, ComponentContext by componentContext {
    // Implementation
}
```

## Testing

### Test Modules

```kotlin
@BindingContainer
class TestNetworkModule {
    @Provides
    fun provideFakeApiService(): ApiService = FakeApiService()
}

@DependencyGraph(
    bindingContainers = [
        TestNetworkModule::class,
        DataModule::class
    ]
)
interface TestAppGraph {
    val authRepository: AuthRepository
}
```

## Best Practices

### Do's
- One `@DependencyGraph` per platform entry point
- Use `@BindingContainer` to organize providers by feature/layer
- Use `@Assisted` for runtime parameters
- Prefer constructor injection over `@Provides`
- Keep binding containers in the same module as implementations

### Don'ts
- Don't create multiple graphs for the same platform
- Don't expose implementation types from graphs
- Don't put platform-specific code in common binding containers

## Comparison with Koin

| Feature | Metro | Koin |
|---------|-------|------|
| Type safety | Compile-time | Runtime |
| Error detection | Build time | Runtime crash |
| Performance | No reflection | Some reflection |
| KMP support | Full | Full |
| Learning curve | Medium (Dagger-like) | Low |
| Build speed | 47-56% faster than KAPT | No code gen |

## Resources

- [Metro GitHub](https://github.com/ZacSweers/metro)
- [Metro Documentation](https://zacsweers.github.io/metro/)
- [Cash App Migration](https://code.cash.app/cash-android-moves-to-metro)