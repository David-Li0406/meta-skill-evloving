# Koin Module Rules

## koin-module-organization - Organize modules by feature/layer

Structure Koin modules by feature or architectural layer for maintainability.

### Incorrect

```kotlin
val appModule = module {
    single { UserRepository() }
    single { ProductRepository() }
    single { OrderRepository() }
    viewModel { UserViewModel(get()) }
    viewModel { ProductViewModel(get()) }
    viewModel { OrderViewModel(get(), get()) }
    single { HttpClient() }
    single { Database() }
    // 50 more definitions...
}
```

### Correct

```kotlin
// Core module - infrastructure
val coreModule = module {
    single { createHttpClient() }
    single { createDatabase() }
}

// Data layer modules
val userDataModule = module {
    single<UserRepository> { UserRepositoryImpl(get()) }
    single { UserApi(get()) }
}

val productDataModule = module {
    single<ProductRepository> { ProductRepositoryImpl(get()) }
    single { ProductApi(get()) }
}

// Presentation layer modules
val userPresentationModule = module {
    viewModel { UserViewModel(get()) }
    viewModel { UserListViewModel(get()) }
}

val productPresentationModule = module {
    viewModel { ProductViewModel(get()) }
    viewModel { ProductListViewModel(get(), get()) }
}

// Combine for different contexts
val allModules = listOf(
    coreModule,
    userDataModule, productDataModule,
    userPresentationModule, productPresentationModule
)
```

---

## koin-module-scope - Use proper scoping

Use single for singletons, factory for new instances, viewModel for ViewModels.

### Incorrect

```kotlin
val module = module {
    // Wrong: Creates new HttpClient for each injection
    factory { HttpClient() }

    // Wrong: Single instance prevents proper cleanup
    single { UserViewModel(get()) }

    // Wrong: Factory for stateful repository
    factory { UserRepository(get()) }
}
```

### Correct

```kotlin
val module = module {
    // Singleton for expensive/shared resources
    single { createHttpClient() }
    single { Database() }

    // Factory for stateless utilities
    factory { DateFormatter() }
    factory<Logger> { ConsoleLogger() }

    // ViewModels with proper scope
    viewModel { UserViewModel(get()) }
    viewModel { params -> DetailViewModel(params.get(), get()) }

    // Repository as singleton (holds state/cache)
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
}
```

---

## koin-module-qualifier - Use named qualifiers for disambiguation

Use named/qualifier annotations to differentiate same-type dependencies.

### Incorrect

```kotlin
val module = module {
    single { OkHttpClient() } // For general use
    single { OkHttpClient().newBuilder().addInterceptor(authInterceptor).build() } // Conflict!
}
```

### Correct

```kotlin
val module = module {
    single(named("default")) {
        OkHttpClient.Builder().build()
    }

    single(named("authenticated")) {
        OkHttpClient.Builder()
            .addInterceptor(get<AuthInterceptor>())
            .build()
    }
}

// Usage
class ApiClient(
    private val client: OkHttpClient
) { /* ... */ }

val apiModule = module {
    single { ApiClient(get(named("authenticated"))) }
}

// Type-safe qualifiers
enum class ClientType { Default, Authenticated }

val module = module {
    single(qualifier<ClientType.Default>()) { createDefaultClient() }
    single(qualifier<ClientType.Authenticated>()) { createAuthClient() }
}
```

---

## koin-module-includes - Use includes for module composition

Compose modules using includes for cleaner organization.

### Incorrect

```kotlin
// Repetitive module loading
startKoin {
    modules(
        networkModule,
        databaseModule,
        userRepositoryModule,
        productRepositoryModule,
        orderRepositoryModule,
        userViewModelModule,
        productViewModelModule,
        orderViewModelModule,
        // ...many more
    )
}
```

### Correct

```kotlin
// Layered module composition
val coreModule = module {
    includes(networkModule, databaseModule, loggingModule)
}

val dataModule = module {
    includes(userRepositoryModule, productRepositoryModule, orderRepositoryModule)
}

val presentationModule = module {
    includes(userViewModelModule, productViewModelModule, orderViewModelModule)
}

val appModule = module {
    includes(coreModule, dataModule, presentationModule)
}

// Clean startup
startKoin {
    modules(appModule)
}
```

---

## koin-module-platform - Handle platform-specific modules

Use expect/actual for platform-specific Koin modules.

### Correct

```kotlin
// commonMain
expect val platformModule: Module

val commonModule = module {
    includes(platformModule)
    // Common dependencies
    single<UserRepository> { UserRepositoryImpl(get()) }
}

// androidMain
actual val platformModule = module {
    single<PlatformLogger> { AndroidLogger() }
    single { AndroidContext.applicationContext }
}

// iosMain
actual val platformModule = module {
    single<PlatformLogger> { IosLogger() }
    single { NSUserDefaults.standardUserDefaults }
}

// desktopMain
actual val platformModule = module {
    single<PlatformLogger> { DesktopLogger() }
    single { Preferences.userRoot() }
}
```
