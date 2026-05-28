# Koin - Getting Started

**Pages:** 51

---

## Koin Annotations Inventory

**URL:** https://insert-koin.io/docs/reference/koin-annotations/annotations-inventory

**Contents:**
- Koin Annotations Inventory
- Table of Contents​
- Definition Annotations​
  - @Single​
  - @Factory​
  - @Scoped​
- Scope Annotations​
  - @Scope​
  - @ViewModelScope​
  - @ActivityScope​

This document provides a comprehensive inventory of all Koin annotations, their parameters, behaviors, and usage examples.

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Declares a type or function as a single (singleton) definition in Koin. A single instance is created and shared across the application.

Behavior: All dependencies are filled by constructor injection.

With explicit binding:

With creation at start:

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Declares a type or function as a factory definition in Koin. A new instance is created each time it is requested.

Behavior: All dependencies are filled by constructor injection. Each request creates a new instance.

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Declares a type or function as a scoped definition in Koin. Must be associated with @Scope annotation. Instance is shared within a specific scope.

Behavior: Creates a scoped instance that lives within the defined scope's lifetime.

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Declares a class in a Koin scope. Scope name is described by either value (class) or name (string). By default, declares a scoped definition. Can be overridden with @Scoped, @Factory, @KoinViewModel annotations for explicit bindings.

Behavior: Creates a scope definition associated with the specified scope type or name.

Example with string name:

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Declares a class in a ViewModelScope Koin scope. This is a scope archetype for components that should live within a ViewModel's lifecycle.

Behavior: Creates a scoped definition within the viewModelScope.

Usage: The tagged class is meant to be used with ViewModel and viewModelScope function to activate the scope.

Package: org.koin.android.annotation

Target: CLASS, FUNCTION

Description: Declares a class in an Activity Koin Scope.

Behavior: Creates a scoped definition within the activityScope.

Usage: The tagged class is meant to be used with Activity and activityScope function to activate the scope.

Package: org.koin.android.annotation

Target: CLASS, FUNCTION

Description: Declares a class in an Activity Koin scope, but retained across configuration changes.

Behavior: Creates a scoped definition within the activityRetainedScope.

Usage: The tagged class is meant to be used with Activity and activityRetainedScope function to activate the scope.

Package: org.koin.android.annotation

Target: CLASS, FUNCTION

Description: Declares a class in a Fragment Koin scope.

Behavior: Creates a scoped definition within the fragmentScope.

Usage: The tagged class is meant to be used with Fragment and fragmentScope function to activate the scope.

Package: org.koin.core.annotation

Target: VALUE_PARAMETER

Description: Annotates a parameter from class constructor or function to request resolution for a given scope with Scope ID.

Behavior: Resolves the dependency from a specific scope identified by type or name.

Example with string name:

Package: org.koin.android.annotation

Target: CLASS, FUNCTION

Description: ViewModel annotation for Koin definition. Declares a type or function as a viewModel definition in Koin.

Behavior: All dependencies are filled by constructor injection. Creates a ViewModel instance managed by Koin. Works across all platforms including Android, iOS, Desktop, and Web when using Compose Multiplatform.

Example (Android/CMP):

Example (KMP/CMP shared):

Package: org.koin.android.annotation

Target: CLASS, FUNCTION

Description: Worker annotation for Koin Definition. Declares a type as a worker definition for WorkManager workers.

Behavior: Creates a worker definition for Android WorkManager integration.

Package: org.koin.core.annotation

Target: CLASS, FUNCTION, VALUE_PARAMETER

Description: Defines a qualifier for a given definition. Generates StringQualifier("...") or type-based qualifier.

Behavior: Used to distinguish between multiple definitions of the same type.

Package: org.koin.core.annotation

Target: CLASS, FUNCTION, VALUE_PARAMETER

Description: Defines a qualifier for a given definition. Similar to @Named but with reversed parameter priority.

Behavior: Used to distinguish between multiple definitions of the same type.

Package: org.koin.core.annotation

Target: VALUE_PARAMETER

Description: Annotates a constructor parameter or function parameter to resolve as a Koin property.

Behavior: Resolves the parameter value from Koin properties instead of dependency injection.

Package: org.koin.core.annotation

Description: Annotates a field value that will be a Property default value.

Behavior: Defines a default value for a property that can be used when the property is not found.

Package: org.koin.core.annotation

Description: Class annotation to help gather definitions inside a Koin module. Each function can be annotated with a Koin definition annotation.

Behavior: Gathers all annotated functions and classes within the module.

Package: org.koin.core.annotation

Description: Gathers definitions declared with Koin definition annotations. Scans current package or explicit package names.

Behavior: Scans specified packages for annotated classes. Supports both exact package names and glob patterns.

Glob Pattern Support:

Exact package names (no wildcards):

Multi-level scan including root:

Multi-level scan excluding root:

Single-level wildcard:

Example - scan current package:

Example - scan specific packages:

Example - with glob patterns:

Package: org.koin.core.annotation

Description: Applied to @Module class to associate it with one or more configurations (tags/flavors).

Behavior: Modules can be grouped into configurations for conditional loading.

Default Configuration:

This module is part of the "default" configuration.

Multiple Configurations:

This module is available in both "prod" and "test" configurations.

Available in default and test configurations.

Note: @Configuration("default") is equivalent to @Configuration

Package: org.koin.core.annotation

Description: Tags a class as a Koin application entry point. Generates Koin application bootstrap with startKoin() or koinApplication() functions.

Behavior: Generates bootstrap functions that scan for configurations and included modules.

Example - default configuration:

Example - specific configurations:

Example - with modules:

Usage with custom configuration:

Package: org.koin.core.annotation

Target: CLASS, FUNCTION

Description: Marks a class or function for automatic monitoring and performance tracing through Kotzilla Platform, the official tooling platform for Koin.

Since: Kotzilla 1.2.1

These annotations are for internal use only by the Koin compiler and code generation.

Package: org.koin.meta.annotations

Target: CLASS, FIELD, FUNCTION

Description: Internal usage for components discovery in generated package.

Package: org.koin.meta.annotations

Target: CLASS, FUNCTION, PROPERTY

Description: Meta Definition annotation to help represent definition metadata.

Package: org.koin.meta.annotations

Description: Meta Module annotation to help represent module metadata.

Package: org.koin.meta.annotations

Description: Meta Application annotation to help represent application metadata.

Package: org.koin.core.annotation

Status: DEPRECATED - ERROR level

Replacement: Use @Singleton from koin-jsr330 package instead

Description: Same as @Single but deprecated in favor of JSR-330 compliance.

Document Version: 1.0 Last Updated: 20-10-2025 Koin Annotations Version: 2.2.x+

**Examples:**

Example 1 (kotlin):
```kotlin
@Singleclass MyClass(val d : MyDependency)
```

Example 2 (kotlin):
```kotlin
single { MyClass(get()) }
```

Example 3 (kotlin):
```kotlin
@Single(binds = [MyInterface::class])class MyClass(val d : MyDependency) : MyInterface
```

Example 4 (kotlin):
```kotlin
@Single(createdAtStart = true)class MyClass(val d : MyDependency)
```

---

## Starting with Koin Annotations

**URL:** https://insert-koin.io/docs/reference/koin-annotations/start

**Contents:**
- Starting with Koin Annotations
- Getting Started​
  - Basic Module Setup​
  - Configuration-based Module Setup​
- KSP Options​
  - Compile Safety - check your Koin config at compile time (since 1.3.0)​
  - Bypass Compile Safety with @Provided (since 1.4.0)​
  - Default Module (Deprecated since 1.3.0)​
  - Kotlin KMP Setup​
  - Pro-Guard​

The goal of the Koin Annotations project is to help declare Koin definitions in a fast and intuitive way, and generate all underlying Koin DSL for you. The goal is to help developers experience scaling and go fast 🚀, thanks to Kotlin Compilers.

Not familiar with Koin? First, take a look at Koin Getting Started

Tag your components with definition & module annotations, and use the regular Koin API.

Now you can start your Koin application with @KoinApplication and explicitly specify the modules to use:

Alternatively, you can use @Configuration to create modules that are automatically loaded:

With configuration, you don't need to specify modules explicitly:

That's it, you can use your new definitions in Koin with the regular Koin API

The Koin compiler offers some options to configure. Following the official doc, you can add the following options to your project: Ksp Quickstart Doc

Koin Annotations allows the compiler plugin to verify your Koin configuration at compile time. This can be activated with the following Ksp options, to add to your Gradle module:

The compiler will check that all dependencies used in your configuration are declared, and all used modules are accessible.

Among the ignored types from the Compiler (Android common types), the compiler plugin can verify your Koin configuration at compile time. If you want to exclude a parameter from being checked, you can use @Provided on a parameter to indicate that this type is provided externally to the current Koin Annotations config.

The following indicates that MyProvidedComponent is already declared in Koin:

The default module approach is deprecated since Annotations 1.3.0. We recommend using explicit modules with @Module and @Configuration annotations for better organization and clarity.

Previously, the Koin compiler would detect any definition not bound to a module and put it in a "default module". This approach is now deprecated in favor of using @Configuration and @KoinApplication annotations.

Deprecated approach (avoid using):

Recommended approach: Use explicit module organization as shown in the examples above with @Configuration and @KoinApplication.

Please follow the KSP setup as described in the official documentation: KSP with Kotlin Multiplatform

You can also check the Hello Koin KMP project with a basic setup for Koin Annotations.

If you intend to embed the Koin Annotations application as an SDK, take a look at those pro-guard rules:

**Examples:**

Example 1 (kotlin):
```kotlin
// Tag your component to declare a definition@Singleclass MyComponent
```

Example 2 (kotlin):
```kotlin
// Declare a module and scan for annotations@Moduleclass MyModule
```

Example 3 (kotlin):
```kotlin
// The import below gives you access to generated extension functions// like MyModule.module and MyApp.startKoin() import org.koin.ksp.generated.*@KoinApplication(modules = [MyModule::class])object MyAppfun main() {    MyApp.startKoin {        printLogger()    }    // Just use your Koin API as regular    KoinPlatform.getKoin().get<MyComponent>()}
```

Example 4 (kotlin):
```kotlin
// Module with configuration - automatically included in default config@Module@Configurationclass MyModule
```

---

## Android - ViewModel

**URL:** https://insert-koin.io/docs/quickstart/android-viewmodel

**Contents:**
- Android - ViewModel
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- Displaying User with ViewModel​
- Injecting ViewModel in Android​
- Start Koin​
- Koin module: classic or constructor DSL?​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

Add the Koin Android dependency like below:

The idea of the application is to manage a list of users, and display it in our MainActivity class with a Presenter or a ViewModel:

Users -> UserRepository -> (Presenter or ViewModel) -> MainActivity

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write a ViewModel component to display a user:

UserRepository is referenced in UserViewModel`s constructor

We declare UserViewModel in our Koin module. We declare it as a viewModelOf definition, to not keep any instance in memory (avoid any leak with Android lifecycle):

The UserViewModel component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the by viewModel() delegate function:

That's it, your app is ready.

The by viewModel() function allows us to retrieve a ViewModel instances, create the associated ViewModel Factory for you and bind it to the lifecycle

We need to start Koin with our Android application. Just call the startKoin() function in the application's main entry point, our MainApplication class:

The modules() function in startKoin load the given list of modules

Here is the Koin moduel declaration for our app:

We can write it in a more compact way, by using constructors:

We can ensure that our Koin configuration is good before launching our app, by verifying our Koin configuration with a simple JUnit Test.

Add the Koin Android dependency like below:

The verify() function allow to verify the given Koin modules:

With just a JUnit test, you can ensure your definitions configuration are not missing anything!

**Examples:**

Example 1 (groovy):
```groovy
dependencies {    // Koin for Android    implementation("io.insert-koin:koin-android:$koin_version")}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Fragment Factory

**URL:** https://insert-koin.io/docs/reference/koin-android/fragment-factory

**Contents:**
- Fragment Factory
- Fragment Factory​
- Setup Fragment Factory​
- Declare & Inject your Fragment​
- Get your Fragment​
- Fragment Factory & Koin Scopes​

Since AndroidX has released androidx.fragment packages family to extend features around Android Fragment

https://developer.android.com/jetpack/androidx/releases/fragment

Since 2.1.0-alpha-3 version, has been introduced the FragmentFactory, a class dedicated to create instance of Fragment class:

https://developer.android.com/reference/kotlin/androidx/fragment/app/FragmentFactory

Koin can bring a KoinFragmentFactory to help you inject your Fragment instances directly.

At start, in your KoinApplication declaration, use the fragmentFactory() keyword to setting up a default KoinFragmentFactory instance:

To declare a Fragment instance, just declare it as a fragment in your Koin module and use constructor injection.

Given a Fragment class:

From your host Activity class, setting up your fragment factory with setupKoinFragmentFactory():

And retrieve your Fragment with your supportFragmentManager:

Put your bundle or tag using the overloaded optional params:

If you want to use the Koin Activity's Scope, you have to declare your fragment inside your scope as a scoped definition:

and setting up your Koin Fragment Factory with your scope: setupKoinFragmentFactory(lifecycleScope)

**Examples:**

Example 1 (kotlin):
```kotlin
startKoin {    // setup a KoinFragmentFactory instance    fragmentFactory()    modules(...)}
```

Example 2 (kotlin):
```kotlin
class MyFragment(val myService: MyService) : Fragment() {}
```

Example 3 (kotlin):
```kotlin
val appModule = module {    single { MyService() }    fragment { MyFragment(get()) }}
```

Example 4 (kotlin):
```kotlin
class MyActivity : AppCompatActivity() {    override fun onCreate(savedInstanceState: Bundle?) {        // Koin Fragment Factory        setupKoinFragmentFactory()        super.onCreate(savedInstanceState)        //...    }}
```

---

## Koin Component

**URL:** https://insert-koin.io/docs/reference/koin-core/koin-component

**Contents:**
- Koin Component
- Create a Koin Component​
- Unlock the Koin API with KoinComponents​
- Retrieving definitions with get & inject​
- Resolving instance from its name​

Koin is a DSL to help describe your modules & definitions, a container to make definition resolution. What we need now is an API to retrieve our instances outside the container. That's the goal of Koin components.

The KoinComponent interface is here to help you retrieve instances directly from Koin. Be careful, this links your class to the Koin container API. Avoid to use it on classes that you can declare in modules, and prefer constructor injection

To give a class the capacity to use Koin features, we need to tag it with KoinComponent interface. Let's take an example.

A module to define MyService instance

we start Koin before using definition.

Start Koin with myModule

Here is how we can write our MyComponent to retrieve instances from Koin container.

Use get() & by inject() to inject MyService instance

Once you have tagged your class as KoinComponent, you gain access to:

Koin offers two ways of retrieving instances from the Koin container:

The lazy inject form is better to define property that need lazy evaluation.

If you need you can specify the following parameter with get() or by inject()

Example of module using definitions names:

We can make the following resolutions:

**Examples:**

Example 1 (kotlin):
```kotlin
class MyServiceval myModule = module {    // Define a singleton for MyService    single { MyService() }}
```

Example 2 (kotlin):
```kotlin
fun main(vararg args : String){    // Start Koin    startKoin {        modules(myModule)    }    // Create MyComponent instance and inject from Koin container    MyComponent()}
```

Example 3 (kotlin):
```kotlin
class MyComponent : KoinComponent {    // lazy inject Koin instance    val myService : MyService by inject()    // or    // eager inject Koin instance    val myService : MyService = get()}
```

Example 4 (kotlin):
```kotlin
// is lazy evaluatedval myService : MyService by inject()// retrieve directly the instanceval myService : MyService = get()
```

---

## Ktor & Koin Isolated Context

**URL:** https://insert-koin.io/docs/reference/koin-ktor/ktor-isolated

**Contents:**
- Ktor & Koin Isolated Context
- Isolated Koin Context Plugin​

The koin-ktor module is dedicated to bring dependency injection for Ktor.

To start an Isolated Koin container in Ktor, just install the KoinIsolated plugin like follow:

By using an isolated Koin context you won't be able to use Koin outside Ktor server instance (i.e: by using GlobalContext for example)

**Examples:**

Example 1 (kotlin):
```kotlin
fun Application.main() {    // Install Koin plugin    install(KoinIsolated) {        slf4jLogger()        modules(helloAppModule)    }}
```

---

## Constructor DSL

**URL:** https://insert-koin.io/docs/reference/koin-core/dsl-update

**Contents:**
- Constructor DSL
- Available Keywords​
- DSL Options​
- Injected Parameters​
- Reflection Based DSL (Deprecated since 3.2)​

Koin now offer a new kind of DSL keyword that allow you to target a class constructor directly, and avoid to have type your definition within a lambda expression.

For a given class ClassA with following dependencies:

you can now declare those components, directly targeting the class constructor:

No need to specify dependencies in constructor anymore with get() function! 🎉

Be sure to use :: before your class name, to target your class constructor

Your constructor is filled automatically with all get(). Avoid using any default value as Koin will try to find it in the current graph.

If you need to retrieve a "named" definition, you need to use the standard DSL with lambda and get() to specify the qualifier

The following keywords are available to build your definition from constructor:

Be sure to not use any default value in your constructor, as Koin will try to fill every parameter with it.

Any Constructor DSL Definition, can also open some option within a lambda:

Usual options and DSL keywords are available in this lambda:

You can also use bind or binds operator, without any need of lambda:

With such kind of declaration, you can still use injected parameters. Koin will look in injected parameters and current dependencies to try to inject your constructor.

declared with Constructor DSL:

can be injected like this:

Koin Reflection DSL is now deprecated. Please Use Koin Constructor DSL above

**Examples:**

Example 1 (kotlin):
```kotlin
class ClassA(val b : ClassB, val c : ClassC)class ClassB()class ClassC()
```

Example 2 (kotlin):
```kotlin
module {    singleOf(::ClassA)    singleOf(::ClassB)    singleOf(::ClassC)}
```

Example 3 (kotlin):
```kotlin
module {    singleOf(::ClassA) {         // definition options        named("my_qualifier")        bind<InterfaceA>()        createdAtStart()    }}
```

Example 4 (kotlin):
```kotlin
module {    singleOf(::ClassA) bind InterfaceA::class}
```

---

## Ktor

**URL:** https://insert-koin.io/docs/quickstart/ktor

**Contents:**
- Ktor
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- The UserService Component​
- HTTP Controller​
- Declare your dependencies​
- Start and Inject​

Ktor is a framework for building asynchronous servers and clients in connected systems using the powerful Kotlin programming language. We will use Ktor here, to build a simple web application.

The source code is available at on Github

First, add the Koin dependency like below:

The idea of the application is to manage a list of users, and display it in our UserApplication class:

Users -> UserRepository -> UserService -> UserApplication

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write the UserService component to request the default user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserService in our Koin module. We declare it as a singleOf definition:

Finally, we need an HTTP Controller to create the HTTP Route. In Ktor is will be expressed through an Ktor extension function:

Check that your application.conf is configured like below, to help start the Application.main function:

Let's assemble our components with a Koin module:

Finally, let's start Koin from Ktor:

That's it! You're ready to go. Check the http://localhost:8080/hello url!

**Examples:**

Example 1 (kotlin):
```kotlin
dependencies {    // Koin for Kotlin apps    implementation("io.insert-koin:koin-ktor:$koin_version")    implementation("io.insert-koin:koin-logger-slf4j:$koin_version")}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Kotlin

**URL:** https://insert-koin.io/docs/quickstart/kotlin/

**Contents:**
- Kotlin
- Get the code​
- Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- The UserService Component​
- Injecting Dependencies in UserApplication​
- Start Koin​
- Koin module: classic or constructor DSL?​

This tutorial lets you write a Kotlin application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

First, check that the koin-core dependency is added like below:

The idea of the application is to manage a list of users, and display it in our UserApplication class:

Users -> UserRepository -> UserService -> UserApplication

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write the UserService component to request the default user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserService in our Koin module. We declare it as a single definition:

The get() function allow to ask Koin to resolve the needed dependency.

The UserApplication class will help bootstrap instances out of Koin. It will resolve the UserService, thanks to KoinComponent interface. This allows to inject it with the by inject() delegate function:

That's it, your app is ready.

The by inject() function allows us to retrieve Koin instances, in any class that extends KoinComponent

We need to start Koin with our application. Just call the startKoin() function in the application's main entry point, our main function:

The modules() function in startKoin load the given list of modules

Here is the Koin module declaration for our app:

We can write it in a more compact way, by using constructors:

**Examples:**

Example 1 (groovy):
```groovy
dependencies {        // Koin for Kotlin apps    implementation "io.insert-koin:koin-core:$koin_version"}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Why Koin?

**URL:** https://insert-koin.io/docs/setup/why

**Contents:**
- Why Koin?
- Koin in a nutshell​
  - Making your Kotlin development easy and productive​
  - Ready for Android​
  - Powering Kotlin Multiplatform​
  - Performances and Productivity​
- Koin: A Dependency Injection Framework​
  - Dependency Injection vs. Service Locator​
  - Koin’s Approach: A Blend of Flexibility and Best Practices​
  - Transparency and Design Overview​

Koin provides an easy and efficient way to incorporate dependency injection into any Kotlin application(Multiplatform, Android, backend ...)

The goals of Koin are:

Koin is a smart Kotlin dependency injection library to keep you focused on your app, not on your tools.

Koin gives you simple tools and API to let you build, assemble Kotlin related technologies into your application and let you scale your business with easiness.

Thanks to the Kotlin language, Koin extends the Android platform and provides new features as part of the original platform.

Koin provides easy and powerful API to retrieve your dependencies anywhere in Android components, with just using by inject() or by viewModel()

Sharing code between mobile platforms is one of the major Kotlin Multiplatform use cases. With Kotlin Multiplatform Mobile, you can build cross-platform mobile applications and share common code between Android and iOS.

Koin provides multiplatform dependency injection and help build your components across your native mobile applications, and web/backend applications.

Koin is a pure Kotlin framework, designed to be straight forward in terms of usage and execution. It easy to use and doesn't impact your compilation time, nor require any extra plugin configuration.

Koin is a popular dependency injection (DI) framework for Kotlin, offering a modern and lightweight solution for managing your application’s dependencies with minimal boilerplate code.

While Koin may appear similar to a service locator pattern, there are key differences that set it apart:

Service Locator: A service locator is essentially a registry of available services where you can request an instance of a service as needed. It is responsible for creating and managing these instances, often using a static, global registry.

Dependency Injection: In contrast, Koin is a pure dependency injection framework. With Koin, you declare your dependencies in modules, and Koin handles the creation and wiring of objects. It allows for the creation of multiple, independent modules with their own scopes, making dependency management more modular and avoiding potential conflicts.

Koin supports both DI and the Service Locator pattern, offering flexibility to developers. However, it strongly encourages the use of DI, particularly constructor injection, where dependencies are passed as constructor parameters. This approach promotes better testability and makes your code easier to reason about.

Koin’s design philosophy is centered around simplicity and ease of setup while allowing for complex configurations when necessary. By using Koin, developers can manage dependencies effectively, with DI being the recommended and preferred approach for most scenarios.

Koin is designed to be a versatile Inversion of Control (IoC) container that supports both Dependency Injection (DI) and Service Locator (SL) patterns. To provide a clear understanding of how Koin operates and to guide you in using it effectively, let’s explore the following aspects:

Koin combines elements of both DI and SL, which may influence how you use the framework:

Global Context Usage: By default, Koin provides a globally accessible component that acts like a service locator. This allows you to retrieve dependencies from a central registry using KoinComponent or inject functions.

Isolated Components: Although Koin encourages the use of Dependency Injection, particularly constructor injection, it also allows for isolated components. This flexibility means you can configure your application to use DI where it makes the most sense while still taking advantage of SL for specific cases.

SL in Android Components: In Android development, Koin often uses SL internally within components such as Application and Activity for ease of setup. From this point, Koin recommends DI, especially constructor injection, to manage dependencies in a more structured way. However, this is not enforced, and developers have the flexibility to use SL if needed.

Understanding the distinction between DI and SL helps in managing your application’s dependencies effectively:

Dependency Injection: Encouraged by Koin for its benefits in testability and maintainability. Constructor injection is preferred as it makes dependencies explicit and enhances code clarity.

Service Locator: While Koin supports SL for convenience, especially in Android components, relying solely on SL can lead to tighter coupling and reduced testability. Koin’s design provides a balanced approach, allowing you to use SL where it’s practical but promoting DI as the best practice.

To use Koin effectively:

Follow Best Practices: Use constructor injection where possible to align with best practices for dependency management. This approach improves testability and maintainability.

Leverage Koin’s Flexibility: Utilize Koin’s support for SL in scenarios where it simplifies setup, but aim to rely on DI for managing core application dependencies.

Refer to Documentation and Examples: Review Koin’s documentation and examples to understand how to configure and use DI and SL appropriately based on your project needs.

Visualize Dependency Management: Diagrams and examples can help illustrate how Koin resolves dependencies and manages them within different contexts. These visual aids can provide a clearer understanding of Koin’s internal workings.

By providing this guidance, we aim to help you navigate Koin’s features and design choices effectively, ensuring you can leverage its full potential while adhering to best practices in dependency management.

**Examples:**

Example 1 (kotlin):
```kotlin
class MyRepository()class MyPresenter(val repository : MyRepository) // just declare it val myModule = module {   singleOf(::MyPresenter)  singleOf(::MyRepository)}
```

Example 2 (kotlin):
```kotlin
fun main() {     // Just start Koin  startKoin {    modules(myModule)  }}
```

Example 3 (kotlin):
```kotlin
class MyApplication : Application() {  override fun onCreate() {    super.onCreate()    startKoin {      modules(myModule)    }  } }
```

Example 4 (kotlin):
```kotlin
class MyActivity : AppCompatActivity() {  val myPresenter : MyPresenter by inject()}
```

---

## Ktor & Annotations

**URL:** https://insert-koin.io/docs/quickstart/ktor-annotations

**Contents:**
- Ktor & Annotations
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- The UserService Component​
- HTTP Controller​
- Start and Inject​

Ktor is a framework for building asynchronous servers and clients in connected systems using the powerful Kotlin programming language. We will use Ktor here, to build a simple web application.

The source code is available at on Github

First, add the Koin dependency like below:

The idea of the application is to manage a list of users, and display it in our UserApplication class:

Users -> UserRepository -> UserService -> UserApplication

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the @Module annotation to declare a Koin module, from a given Kotlin class. A Koin module is the place where we define all our components to be injected.

The @ComponentScan("org.koin.sample") will help scan annotated classes from targeted package.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl. We tag it @Single

Let's write the UserService component to request the default user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserService in our Koin module. We tag with @Single annotation:

Finally, we need an HTTP Controller to create the HTTP Route. In Ktor is will be expressed through an Ktor extension function:

Check that your application.conf is configured like below, to help start the Application.main function:

Finally, let's start Koin from Ktor:

By writing the AppModule().module we use a generated extension on AppModule class.

That's it! You're ready to go. Check the http://localhost:8080/hello url!

**Examples:**

Example 1 (kotlin):
```kotlin
plugins {    id("com.google.devtools.ksp") version kspVersion}dependencies {    // Koin for Kotlin apps    implementation("io.insert-koin:koin-ktor:$koin_version")    implementation("io.insert-koin:koin-logger-slf4j:$koin_version")    implementation("io.insert-koin:koin-annotations:$koinAnnotationsVersion")    ksp("io.insert-koin:koin-ksp-compiler:$koinAnnotationsVersion")}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
@Module@ComponentScan("org.koin.sample")class AppModule
```

---

## Definitions

**URL:** https://insert-koin.io/docs/reference/koin-core/definitions

**Contents:**
- Definitions
- Writing a module​
- Defining a singleton​
- Defining your component within a lambda​
- Defining a factory​
- Resolving & injecting dependencies​
- Definition: binding an interface​
- Additional type binding​
- Definition: naming & default bindings​
- Declaring injection parameters​

By using Koin, you describe definitions in modules. In this section we will see how to declare, organize & link your modules.

A Koin module is the space to declare all your components. Use the module function to declare a Koin module:

In this module, you can declare components as described below.

Declaring a singleton component means that Koin container will keep a unique instance of your declared component. Use the single function in a module to declare a singleton:

single, factory & scoped keywords help you declare your components through a lambda expression. this lambda describe the way that you build your component. Usually we instantiate components via their constructors, but you can also use any expression.

single { Class constructor // Kotlin expression }

The result type of your lambda is the main type of your component

A factory component declaration is a definition that will provide you a new instance each time you ask for this definition (this instance is not retained by Koin container, as it won't inject this instance in other definitions later). Use the factory function with a lambda expression to build a component.

Koin container doesn't retain factory instances as it will give a new instance each time the definition is asked.

Now that we can declare components definitions, we want to link instances with dependency injection. To resolve an instance in a Koin module, just use the get() function to request the needed component instance. This get() function is usually used into constructor, to inject constructor values.

To make dependency injection with Koin container, we have to write it in constructor injection style: resolve dependencies in class constructors. This way, your instance will be created with injected instances from Koin.

Let's take an example with several classes:

A single or a factory definition use the type from their given lambda definition i.e: single { T } The matched type of the definition is the only matched type from this expression.

Let's take an example with a class and implemented interface:

In a Koin module we can use the as cast Kotlin operator as follows:

You can also use the inferred type expression:

This 2nd way of style declaration is preferred and will be used for the rest of the documentation.

In some cases, we want to match several types from just one definition.

Let's take an example with a class and interface:

To make a definition bind additional types, we use the bind operator with a class:

Note here, that we would resolve the Service type directly with get(). But if we have multiple definitions binding Service, we have to use the bind<>() function.

You can specify a name to your definition, to help you distinguish two definitions about the same type:

Just request your definition with its name:

get() and by inject() functions let you specify a definition name if needed. This name is a qualifier produced by the named() function.

By default, Koin will bind a definition by its type or by its name, if the type is already bound to a definition.

In any definition, you can use injection parameters: parameters that will be injected and used by your definition:

In contrary to resolved dependencies (resolved with get()), injection parameters are parameters passed through the resolution API. This means that those parameters are values passed with get() and by inject(), with the parametersOf function:

Further reading in the Injection Parameters Section

You can use the onClose function, to add on a definition, the callback once definition closing is called:

Koin DSL also proposes some flags.

A definition or a module can be flagged as CreatedAtStart, to be created at start (or when you want). First set the createdAtStart flag on your module or on your definition.

CreatedAtStart flag on a definition

CreatedAtStart flag on a module:

The startKoin function will automatically create definitions instances flagged with createdAtStart.

if you need to load some definition at a special time (in a background thread instead of UI for example), just get/inject the desired components.

When you have allowOverride(false) enabled for strict control, but need specific definitions to override existing ones, you can use the .override() option:

You can also use it with withOptions:

This is particularly useful for:

See Modules - Explicit Override for more details.

Koin definitions doesn't take in accounts generics type argument. For example, the module below tries to define 2 definitions of List:

Koin won't start with such definitions, understanding that you want to override one definition for the other.

To allow you, use the 2 definitions you will have to differentiate them via their name, or location (module). For example:

**Examples:**

Example 1 (kotlin):
```kotlin
val myModule = module {   // your dependencies here}
```

Example 2 (kotlin):
```kotlin
class MyService()val myModule = module {    // declare single instance for MyService class    single { MyService() }}
```

Example 3 (kotlin):
```kotlin
class Controller()val myModule = module {    // declare factory instance for Controller class    factory { Controller() }}
```

Example 4 (kotlin):
```kotlin
// Presenter <- Serviceclass Service()class Controller(val view : View)val myModule = module {    // declare Service as single instance    single { Service() }    // declare Controller as single instance, resolving View instance with get()    single { Controller(get()) }}
```

---

## Kotlin Multiplatform - Definitions and Modules Annotations

**URL:** https://insert-koin.io/docs/reference/koin-annotations/kmp

**Contents:**
- Kotlin Multiplatform - Definitions and Modules Annotations
- KSP Setup​
- Defining Definitions and Modules in Common Code​
- Sharing Patterns​
  - Sharing Definitions for native implementations​
    - Scanning for Expect/Actual definitions​
    - Declaring Expect/Actual function definitions​
  - Sharing Definitions with different native contracts​
  - Safely Sharing across platforms with Platform Wrapper​
  - Sharing Expect/Actual Module - rely on Native Module Scanning​

Please follow the KSP setup as described in the official documentation: KSP with Kotlin Multiplatform

You can also check the Hello Koin KMP project with a basic setup for Koin Annotations.

Use the annotations library in the common API:

And don't forget to configure KSP on the right sourceSet:

In your commonMain sourceSet, declare your Module, scan for definitions, or define functions as regular Kotlin Koin declarations. See Definitions and Modules.

In this section, we will see together several ways to share components with definitions and modules.

In a Kotlin Multiplatform application, some components must be implemented specifically per platform. You can share those components at the definition level, with expected/actual on the given class (definition or module). You can share a definition with expect/actual implementation, or a module with expect/actual.

Please look at Multiplatform Expect & Actual Rules documentation for general Kotlin guidance.

Expect/Actual classes can't have different constructors per platform. You need to respect the current constructor contract designed in common space

We target sharing with a Common Module + Expect/Actual Class Definition

For this first classic pattern, you can use both definitions scanning with @ComponentScan or declare a definition as a module class function.

Be aware that to use expect/actual definitions, you will use the same constructor (either the default or a custom one). This constructor has to be the same on all platforms.

In native sources, implement our actual classes:

In native sources, implement our actual classes:

We target Expect/Actual common Module + common Interface + native implementations

In some cases, you need different constructor arguments on each native implementation. Then Expect/Actual class is not your solution. You need to go with an interface to implement on each platform, and a Expect/Actual class module to allow a module to define your right platform implementation:

In native sources, implement our actual classes:

Each time you use manual access to Koin scope, you are doing dynamic wiring. Compile safety doesn't cover such wiring.

Wrap a specific platform component, as a "platform wrapper"

You can wrap a specific platform component, as a "platform wrapper", to help you minimize dynamic injection.

For example, we can do a ContextWrapper that lets us inject Android Context when needed, but doesn't impact the iOS side.

In native sources, implement our actual classes:

This way, you minimize the dynamic platform wiring to one definition, and inject safely in your entire system.

You can now use your ContextWrapper from common code, and easily pass it in your Expect/Actual classes:

In native sources, implement our actual classes:

Rely on a native module from a common module

In some cases, you don't want to have constraints, and scan for components on each native side. Define an empty module class in the common source set, and define your implementation on each platform.

If you define an empty module in the common side, each native module implementation will be generated from each native target, allowing to scan native only components for example.

In native source sets:

**Examples:**

Example 1 (kotlin):
```kotlin
plugins {    alias(libs.plugins.ksp)}
```

Example 2 (kotlin):
```kotlin
sourceSets {    commonMain.dependencies {        implementation(libs.koin.core)        api(libs.koin.annotations)        // ...    }}
```

Example 3 (kotlin):
```kotlin
dependencies {    add("kspCommonMainMetadata", libs.koin.ksp.compiler)    add("kspAndroid", libs.koin.ksp.compiler)    add("kspIosX64", libs.koin.ksp.compiler)    add("kspIosArm64", libs.koin.ksp.compiler)    add("kspIosSimulatorArm64", libs.koin.ksp.compiler)}
```

Example 4 (kotlin):
```kotlin
// commonMain@Module@ComponentScan("com.jetbrains.kmpapp.native")class NativeModuleA()// package com.jetbrains.kmpapp.native@Factoryexpect class PlatformComponentA() {    fun sayHello() : String}
```

---

## Scopes in Koin Annotations

**URL:** https://insert-koin.io/docs/reference/koin-annotations/scope

**Contents:**
- Scopes in Koin Annotations
- Defining a Scope with @Scope​
- Adding a definition in a Scope with @Scoped​
- Dependency resolution from a scope​
- Resolving outside a Scope with @ScopeId (since 1.3.0)​
- Scope Archetype Annotations​
  - Android Scope Archetypes​
    - @ActivityScope​
    - @ActivityRetainedScope​
    - @FragmentScope​

While using definitions and modules, you may need to define scopes for a particular space and time resolution.

Koin allows the use of scopes. Please refer to Koin Scopes section for more details on basics.

To declare a scope with annotations, just use @Scope annotation on a class, like this

this will be equivalent of the following scope section:

Else, if you need a scope name more than a type, you need to tag a class with @Scope(name = ) annotation, using name parameter:

this will be the equivalent of

To declare a definition inside a scope (defined or not with annotations), just tag a class with @Scope and @Scoped annotations:

This will generate the right definition inside the scope section:

You need both annotations to indicate the needed scope space (with @Scope) and the kind of component to define (with @Scoped)

From a scoped definition, you can resolve any definition from your inner Scope and from the parent scopes.

For example, the following case will work:

The component MySingle is defined as single definition, in the root. MyScopedComponent and MyOtherScopedComponent are defined in scope "my_scope_name". The dependencies resolution from MyScopedComponent is accessing the Koin root with MySingle instance, and MyOtherScopedComponent scoped instance from the current "my_scope_name" scope.

You may need to resolve a component from another scope that is not directly accessible to your scope. For this, you need to tag your dependency with @ScopeId annotation to tell Koin to find this dependency in the scope of the given scope Id.

The above code is equivalent is generated:

This example shows that MyFactory component will resolve MyScopedComponent component from a scope instance with id "my_scope_id". This scope, created with id "my_scope_id" needs to be created with the right scope definition.

The MyScopedComponent component needs to be defined in a Scope section, and a scope instance needs to be created with id "my_scope_id".

Koin Annotations provides predefined scope archetype annotations for common scope patterns, eliminating the need to manually declare scope types. These annotations combine scope declaration and component definition in a single annotation.

For Android development, you can use these predefined scope annotations:

Declare a component in an Activity scope:

Usage: The tagged class is meant to be used with Activity and the activityScope function to activate the scope.

Declare a component in an Activity Retained scope (survives configuration changes):

Usage: The tagged class is meant to be used with Activity and the activityRetainedScope function to activate the scope.

Declare a component in a Fragment scope:

Usage: The tagged class is meant to be used with Fragment and the fragmentScope function to activate the scope.

Declare a component in a ViewModel scope. This annotation is Kotlin Multiplatform (KMP) compatible and works with both Android ViewModels and Compose Multiplatform ViewModels:

Usage: The tagged class is meant to be used with ViewModel and the viewModelScope function to activate the scope.

KMP Support: Works seamlessly across all Kotlin Multiplatform targets including Android, iOS, Desktop, and Web platforms where ViewModels are used.

Scope archetype annotations work seamlessly with regular Koin scoping:

Scope archetypes can also be used on functions within modules:

Scope archetype annotations automatically create the appropriate scope definition and scoped component declaration, reducing boilerplate code for common scope patterns.

**Examples:**

Example 1 (kotlin):
```kotlin
@Scopeclass MyScopeClass
```

Example 2 (kotlin):
```kotlin
scope<MyScopeClass> {}
```

Example 3 (kotlin):
```kotlin
@Scope(name = "my_scope_name")class MyScopeClass
```

Example 4 (kotlin):
```kotlin
scope<named("my_scope_name")> {}
```

---

## Constructor DSL for Android

**URL:** https://insert-koin.io/docs/reference/koin-android/dsl-update

**Contents:**
- Constructor DSL for Android
- New Constructor DSL (Since 3.2)​
  - An Android example​
- Android Reflection DSL (Deprecated since 3.2)​

Koin now offer a new kind of DSL keyword that allow you to target a class constructor directly, and avoid to have type your definition within a lambda expression.

Check the new Constructor DSL section for more details.

For Android, this implies the following new constructor DSL Keyword:

Be sure to use :: before your class name, to target your class constructor

Given an Android application with the following components:

we can declare them like this:

Koin Reflection DSL is now deprecated. Please Use Koin Constructor DSL above

**Examples:**

Example 1 (kotlin):
```kotlin
// A simple serviceclass SimpleServiceImpl() : SimpleService// a Presenter, using SimpleService and can receive "id" injected paramclass FactoryPresenter(val id: String, val service: SimpleService)// a ViewModel that can receive "id" injected param, use SimpleService and get SavedStateHandleclass SimpleViewModel(val id: String, val service: SimpleService, val handle: SavedStateHandle) : ViewModel()// a scoped Session, that can received link to the MyActivity (from scope)class Session(val activity: MyActivity)// a Worker, using SimpleService and getting Context & WorkerParametersclass SimpleWorker(    private val simpleService: SimpleService,    appContext: Context,    private val params: WorkerParameters) : CoroutineWorker(appContext, params)
```

Example 2 (kotlin):
```kotlin
module {    singleOf(::SimpleServiceImpl){ bind<SimpleService>() }    factoryOf(::FactoryPresenter)    viewModelOf(::SimpleViewModel)    scope<MyActivity>(){        scopedOf(::Session)     }    workerOf(::SimpleWorker)}
```

---

## Koin Built-in Performance Monitoring with @Monitor

**URL:** https://insert-koin.io/docs/reference/koin-annotations/monitor

**Contents:**
- Koin Built-in Performance Monitoring with @Monitor
- Setup​
- Basic Usage​
- Generated Code​
- ViewModels Monitoring​
- Kotzilla Platform Integration​
- Requirements​

The @Monitor annotation (available since Koin Annotations 2.2.0) enables automatic performance monitoring and tracing for your Koin components through the Kotzilla Platform, the official tooling platform for Koin.

Add the Kotzilla SDK dependency:

Check the latest version on the Kotzilla documentation.

Configure the allOpen plugin to make monitored classes extensible:

Initialize Kotzilla analytics in your Koin configuration:

Simply annotate your Koin components with @Monitor:

The compiler automatically generates a proxy class that wraps your component:

Koin automatically uses the proxy instead of the original class, transparently capturing:

Monitor your ViewModels to track UI performance:

The monitoring data is automatically sent to your Kotzilla Platform workspace, providing:

Create your free Kotzilla account and configure the API key in your kotzilla.json file:

The @Monitor annotation only tracks method calls on the monitored class itself. Dependencies injected into the monitored class are not automatically monitored unless they are also annotated with @Monitor.

For complete setup instructions and advanced configuration options, visit the Kotzilla Documentation.

**Examples:**

Example 1 (kotlin):
```kotlin
dependencies {    implementation "io.kotzilla:kotzilla-core:latest.version"}
```

Example 2 (kotlin):
```kotlin
plugins {    id "org.jetbrains.kotlin.plugin.allopen"}allOpen {    annotation("org.koin.core.annotation.Monitor")}
```

Example 3 (kotlin):
```kotlin
import io.kotzilla.sdk.analytics.koin.analyticsfun initKoin() {    startKoin {        // Enable Kotzilla monitoring        analytics()        modules(appModule)    }}
```

Example 4 (kotlin):
```kotlin
@Monitor@Singleclass UserService(private val userRepository: UserRepository) {    fun findUser(id: String): User? = userRepository.findById(id)        suspend fun createUser(userData: UserData): User {        return userRepository.save(userData)    }}
```

---

## Kotlin Multiplatform - No shared UI

**URL:** https://insert-koin.io/docs/quickstart/kmp

**Contents:**
- Kotlin Multiplatform - No shared UI
- Get the code​
- Application Overview​
- The "User" Data​
- The Shared Koin module​
- The Shared Presenter​
- Native Component​
- Injecting in Android​
- Injecting in iOS​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 15 min to do the tutorial.

The source code is available at on Github

The idea of the application is to manage a list of users, and display it in our native UI, witha shared Presenter:

Users -> UserRepository -> Shared Presenter -> Native UI

All the common/shared code is located in shared Gradle project

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write a presenter component to display a user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserPresenter in our Koin module. We declare it as a factoryOf definition, to not keep any instance in memory and let the native system hold it:

The Koin module is available as function to run (appModule here), to be easily runned from iOS side, with initKoin() function.

The following native component is defined in Android and iOS:

Both get local platform implementation

All the Android app is located in androidApp Gradle project

The UserPresenter component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the koinInject compose function:

That's it, your app is ready.

The koinInject() function allows us to retrieve Koin instances, in Android Compose runtime

We need to start Koin with our Android application. Just call the KoinApplication() function in the compose application function App:

We gather Koin android configuration, from the shared KMP configuration:

We get the current Android context from Compose with LocalContext.current

And the shared KMP config:

The modules() function load the given list of modules

All the iOS app is located in iosApp folder

The UserPresenter component will be created, resolving the UserRepository instance with it. To get it into our ContentView, we need to create a function to retrieve Koin dependencies for iOS:

That's it, you can just call KoinKt.getUserPresenter().sayHello() function from iOS part.

We need to start Koin with our iOS application. In the Kotlin shared code, we can use the shared configuration with initKoin() function. Finally in the iOS main entry, we can call the KoinAppKt.doInitKoin() function that is calling our helper function above.

**Examples:**

Example 1 (kotlin):
```kotlin
data class User(val name : String)
```

Example 2 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 3 (kotlin):
```kotlin
module {    singleOf(::UserRepositoryImpl) { bind<UserRepository>() }}
```

Example 4 (kotlin):
```kotlin
class UserPresenter(private val repository: UserRepository) {    fun sayHello(name : String) : String{        val foundUser = repository.findUser(name)        val platform = getPlatform()        return foundUser?.let { "Hello '$it' from ${platform.name}" } ?: "User '$name' not found!"    }}
```

---

## CheckModules - Check Koin configuration (Deprecated)

**URL:** https://insert-koin.io/docs/reference/koin-test/checkmodules

**Contents:**
- CheckModules - Check Koin configuration (Deprecated)
  - Koin Dynamic Check - CheckModules()​
    - CheckModule DSL​
    - Allow mocking with a Junit rule​
    - Verifying modules with dynamic behavior (3.1.3+)​
    - Checking Modules for Android (3.1.3)​
    - Providing Default Values (3.1.4)​
    - Providing ParametersOf values (3.1.4)​
    - Providing Scope Links​

This API is now deprecated - since Koin 4.0

Koin allows you to verify your configuration modules, avoiding discovering dependency injection issues at runtime.

Invoke the checkModules() function within a simple JUnit test. This will launch your modules and try to run each possible definition for you.

also possible to use checkKoinModules:

For any definition that is using injected parameters, properties or dynamic instances, the checkModules DSL allows to specify how to work with the following case:

withInstance(value) - will add value instance to Koin graph (can be used in dependency or parameter)

withInstance<MyType>() - will add a mocked instance of MyType. Use MockProviderRule. (can be used in dependency or parameter)

withParameter<Type>(qualifier){ qualifier -> value } - will add value instance to be injected as parameter

withParameter<Type>(qualifier){ qualifier -> parametersOf(...) } - will add value instance to be injected as parameter

withProperty(key,value) - add property to Koin

To use mocks with checkModules, you need to provide a MockProviderRule

To verify a dynamic behavior like following, let's use the CheckKoinModules DSL to provide the missing instance data to our test:

You can verify it with the following:

This way, FactoryPresenter definition will be injected with "_my_id_value" define above.

You can also use mocked instances, to fill up your graph. You can notice that we need a MockProviderRule declaration to allow Koin mock any injected definition

Here below is how you can test your graph for a typical Android app:

also possible to use checkKoinModules:

If you need, you can set a default value for all type in the checked modules. For example, we can override all injected string values:

Let's use the withInstance() function in checkModules block, to define a default value for all definitions:

All injected definition that are using an injected String parameter, will receive "_ID_":

You can define a default value to be injected for one specific definition, with withParameter or withParameters functions:

You can link scopes by using withScopeLink function incheckModules block to inject instances from another scope's definitions:

**Examples:**

Example 1 (kotlin):
```kotlin
class CheckModulesTest : KoinTest {    @Test    fun verifyKoinApp() {                koinApplication {            modules(module1,module2)            checkModules()        }    }}
```

Example 2 (kotlin):
```kotlin
class CheckModulesTest : KoinTest {    @Test    fun verifyKoinApp() {                checkKoinModules(listOf(module1,module2))    }}
```

Example 3 (kotlin):
```kotlin
@get:Ruleval mockProvider = MockProviderRule.create { clazz ->    // Mock with your framework here given clazz }
```

Example 4 (kotlin):
```kotlin
val myModule = module {    factory { (id: String) -> FactoryPresenter(id) }}
```

---

## Navigation 3 Integration

**URL:** https://insert-koin.io/docs/reference/koin-compose/navigation3

**Contents:**
- Navigation 3 Integration
- Setup​
  - For Multiplatform Projects​
  - For Android-only Projects​
- Key Concepts​
- Declaring Navigation Entries​
  - Basic Module-level Navigation​
  - Scoped Navigation​
- Using Navigation in Compose​
  - Retrieving the EntryProvider​

Koin provides integration with AndroidX Navigation 3 to help you build type-safe navigation graphs with dependency injection.

Add the Navigation 3 integration dependency to your project:

This is an experimental API marked with @KoinExperimentalAPI. The Navigation 3 library is currently in alpha.

Navigation 3 integration introduces three main components:

Use the navigation<T>() DSL function in your Koin modules to declare navigation destinations:

You can also declare navigation entries within Koin scopes, useful for scoping ViewModels and dependencies to specific parts of your navigation graph:

Use the koinEntryProvider() composable function to retrieve the aggregated navigation entries from Koin:

You can provide a specific Koin scope to retrieve entries from:

For Android applications, you can use the ComponentCallbacks extensions to retrieve the entry provider from Activities or Fragments:

Or use eager initialization:

Navigation 3 uses type-safe routes. Access route parameters directly from the route object:

Navigation entries can leverage Koin's scoping capabilities:

Here's a complete example showing a typical navigation setup:

If you're migrating from the Navigation 2.x integration:

**Examples:**

Example 1 (kotlin):
```kotlin
commonMain.dependencies {    implementation("io.insert-koin:koin-compose-navigation3:$koin_version")}
```

Example 2 (kotlin):
```kotlin
dependencies {    implementation("io.insert-koin:koin-compose-navigation3:$koin_version")}
```

Example 3 (kotlin):
```kotlin
val appModule = module {    single { Navigator() }    viewModel { HomeViewModel() }    viewModel { DetailViewModel() }    // Declare navigation entries    navigation<HomeRoute> { route ->        HomeScreen(viewModel = koinViewModel())    }    navigation<DetailRoute> { route ->        DetailScreen(            viewModel = koinViewModel(),            itemId = route.itemId        )    }}// Define your routes@Serializableobject HomeRoute@Serializabledata class DetailRoute(val itemId: String)
```

Example 4 (kotlin):
```kotlin
val appModule = module {    // Activity scope    activityRetainedScope {        scoped { Navigator() }        viewModel { ProfileViewModel() }        navigation<ProfileRoute> { route ->            ProfileScreen(viewModel = koinViewModel())        }    }    // also with custom scope    // Activity scope    scope<ComponentActivity> {        scoped { Navigator() }        viewModel { ProfileViewModel() }        navigation<ProfileRoute> { route ->            ProfileScreen(viewModel = koinViewModel())        }    }}
```

---

## Koin Annotations

**URL:** https://insert-koin.io/docs/setup/annotations

**Contents:**
- Koin Annotations
- Current Versions​
- KSP Plugin​
- Android & Ktor App KSP Setup​
- Kotlin Multiplatform Setup​

Setup Koin Annotations for your project

You can find all Koin packages on maven central.

Here are the currently available Koin Annotations versions:

We need the Google KSP to work. Follow the official KSP Setup documentation.

Just add the Gradle plugin:

KSP Compatibility: Latest Koin/KSP compatible version is 2.1.21-2.0.2 (KSP2)

KSP version format: [Kotlin version]-[KSP version]. Make sure your KSP version is compatible with your Kotlin version.

In a standard Kotlin/Kotlin Multiplatform project, you need to setup KSP as follow:

**Examples:**

Example 1 (kotlin):
```kotlin
plugins {    id("com.google.devtools.ksp") version "$ksp_version"}
```

Example 2 (kotlin):
```kotlin
plugins {    id("com.google.devtools.ksp") version "$ksp_version"}dependencies {    // Koin    implementation("io.insert-koin:koin-android:$koin_version")    // Koin Annotations    implementation("io.insert-koin:koin-annotations:$koin_annotations_version")    // Koin Annotations KSP Compiler    ksp("io.insert-koin:koin-ksp-compiler:$koin_annotations_version")}
```

Example 3 (kotlin):
```kotlin
plugins {    id("com.google.devtools.ksp")}kotlin {    sourceSets {                // Add Koin Annotations        commonMain.dependencies {            // Koin            implementation("io.insert-koin:koin-core:$koin_version")            // Koin Annotations            api("io.insert-koin:koin-annotations:$koin_annotations_version")        }    }        // KSP Common sourceSet    sourceSets.named("commonMain").configure {        kotlin.srcDir("build/generated/ksp/metadata/commonMain/kotlin")    }       }// KSP Tasksdependencies {    add("kspCommonMainMetadata", libs.koin.ksp.compiler)    add("kspAndroid", libs.koin.ksp.compiler)    add("kspIosX64", libs.koin.ksp.compiler)    add("kspIosArm64", libs.koin.ksp.compiler)    add("kspIosSimulatorArm64", libs.koin.ksp.compiler)}// Trigger Common Metadata Generation from Native taskstasks.matching { it.name.startsWith("ksp") && it.name != "kspCommonMainKotlinMetadata" }.configureEach {    dependsOn("kspCommonMainKotlinMetadata")}
```

---

## What is Koin?

**URL:** https://insert-koin.io/docs/reference/introduction

**Contents:**
- What is Koin?

Koin is a pragmatic and lightweight dependency injection framework for Kotlin developers.

Koin is a DSL, a light container and a pragmatic API

---

## Koin DSL

**URL:** https://insert-koin.io/docs/reference/koin-core/dsl

**Contents:**
- Koin DSL
- Application & Module DSL​
- Application DSL​
- KoinApplication instance: Global vs Local​
- Starting Koin​
- Module DSL​
  - Writing a module​
  - withOptions - DSL Options (since 3.2)​

Thanks to the power of Kotlin language, Koin provides a DSL to help you describe your app instead of annotate it or generate code for it. With its Kotlin DSL, Koin offers a smart functional API to achieve to prepare your dependency injection.

Koin offers several keywords to let you describe the elements of a Koin Application:

A KoinApplication instance is a Koin container instance configuration. This will let you configure logging, properties loading and modules.

To build a new KoinApplication, use the following functions:

To configure your KoinApplication instance, you can use any of the following functions :

As you can see above, we can describe a Koin container configuration in 2 ways: koinApplication or startKoin function.

By registering your container configuration into the GlobalContext, the global API can use it directly. Any KoinComponent refers to a Koin instance. By default, we use the one from GlobalContext.

Check chapters about Custom Koin instance for more information.

Starting Koin means run a KoinApplication instance into the GlobalContext.

To start Koin container with modules, we can just use the startKoin function like that:

A Koin module gather definitions that you will inject/combine for your application. To create a new module, just use the following function:

To describe your content in a module, you can use the following functions:

Note: the named() function allow you to give a qualifier either by a string, an enum or a type. It is used to name your definitions.

A Koin module is the space to declare all your components. Use the module function to declare a Koin module:

In this module, you can declare components as described below.

Like for new Constructor DSL definitions, you can specify definition options on "regular" definitions with the withOptions operator:

Within this option lambda, you can specify the following options:

**Examples:**

Example 1 (kotlin):
```kotlin
// start a KoinApplication in Global contextstartKoin {    // declare used logger    logger()    // declare used modules    modules(coffeeAppModule)}
```

Example 2 (kotlin):
```kotlin
val myModule = module {   // your dependencies here}
```

Example 3 (kotlin):
```kotlin
module {    single { ClassA(get()) } withOptions {         named("qualifier")        createdAtStart()    }}
```

---

## Android Instrumented Testing

**URL:** https://insert-koin.io/docs/reference/koin-android/instrumented-testing

**Contents:**
- Android Instrumented Testing
- Override production modules in a custom Application class​
- Override production modules with a test rule​

Unlike unit tests, where you effectively call start Koin in each test class (i.e. startKoin or KoinTestExtension), in Instrumented tests Koin is started by your Application class.

For overriding production Koin modules, loadModules and unloadModules are often unsafe because the changes are not applied immediately. Instead, the recommended approach is to add a module of your overrides to modules used by startKoin in the Application class. If you want to keep the class that extends Application of your application untouched, you can create another one inside the AndroidTest package like:

In order to use this custom Application in yours Instrumentation tests you may need to create a custom AndroidJUnitRunner like:

And then register it inside your gradle file with:

If you want more flexibility, you still have to create the custom AndroidJUnitRunner but instead of having startKoin { ... } inside the custom application, you can put it inside a custom test rule like:

In this way we can potentially override the definitions directly from our test classes, like:

**Examples:**

Example 1 (kotlin):
```kotlin
class TestApplication : Application() {    override fun onCreate() {        super.onCreate()        startKoin {            modules(productionModule, instrumentedTestModule)        }    }}
```

Example 2 (kotlin):
```kotlin
class InstrumentationTestRunner : AndroidJUnitRunner() {    override fun newApplication(        classLoader: ClassLoader?,        className: String?,        context: Context?    ): Application {        return super.newApplication(classLoader, TestApplication::class.java.name, context)    }}
```

Example 3 (groovy):
```groovy
testInstrumentationRunner "com.example.myapplication.InstrumentationTestRunner"
```

Example 4 (kotlin):
```kotlin
class KoinTestRule(    private val modules: List<Module>) : TestWatcher() {    override fun starting(description: Description) {        if (getKoinApplicationOrNull() == null) {            startKoin {                androidContext(InstrumentationRegistry.getInstrumentation().targetContext.applicationContext)                modules(modules)            }        } else {            loadKoinModules(modules)        }    }    override fun finished(description: Description) {        unloadKoinModules(modules)    }}
```

---

## Verifying your Koin configuration

**URL:** https://insert-koin.io/docs/reference/koin-test/verify

**Contents:**
- Verifying your Koin configuration
- Koin Configuration check with Verify() - JVM Only [3.3]​
- Verifying with Injected Parameters - JVM Only [4.0]​
- Type White-Listing​
- Core Annotations - Automatically declare safe types​

Koin allows you to verify your configuration modules, avoiding discovering dependency injection issues at runtime.

Use the verify() extension function on a Koin Module. That's it! Under the hood, This will verify all constructor classes and crosscheck with the Koin configuration to know if there is a component declared for this dependency. In case of failure, the function will throw a MissingKoinDefinitionException.

Launch the JUnit test and you're done! ✅

As you may see, we use the extra Types parameter to list types used in the Koin configuration but not declared directly. This is the case for SavedStateHandle and WorkerParameters types, that are used as injected parameters. The Context is declared by androidContext() function at start.

The verify() API is ultra light to run and doesn't require any kind of mock/stub to run on your configuration.

When you have a configuration that implies injected obects with parametersOf, the verification will fail because there is no definition of the parameter's type in your configuration. However you can define a parameter type, to be injected with given definition definition<Type>(Class1::class, Class2::class ...).

We can add types as "white-listed". This means that this type is considered as present in the system for any definition. Here is how it goes:

We also introduced annotations in the main Koin project (under the koin-core-annotations module), extracted from Koin annotations. Those avoid verbose declarations by using @InjectedParam and @Provided to help Koin infer injection contracts and validate configurations. Instead of having a complex DSL configuration, this helps identify those elements. Those annotations are used only with the verify API for now.

This helps prevent subtle issues during testing or runtime without writing custom verification logic.

**Examples:**

Example 1 (kotlin):
```kotlin
val niaAppModule = module {    includes(        jankStatsKoinModule,        dataKoinModule,        syncWorkerKoinModule,        topicKoinModule,        authorKoinModule,        interestsKoinModule,        settingsKoinModule,        bookMarksKoinModule,        forYouKoinModule    )    viewModelOf(::MainActivityViewModel)}
```

Example 2 (kotlin):
```kotlin
class NiaAppModuleCheck {    @Test    fun checkKoinModule() {        // Verify Koin configuration        niaAppModule.verify()    }}
```

Example 3 (kotlin):
```kotlin
class ModuleCheck {    // given a definition with an injected definition    val module = module {        single { (a: Simple.ComponentA) -> Simple.ComponentB(a) }    }    @Test    fun checkKoinModule() {                // Verify and declare Injected Parameters        module.verify(            injections = injectedParameters(                definition<Simple.ComponentB>(Simple.ComponentA::class)            )        )    }}
```

Example 4 (kotlin):
```kotlin
class NiaAppModuleCheck {    @Test    fun checkKoinModule() {        // Verify Koin configuration        niaAppModule.verify(            // List types used in definitions but not declared directly (like parameter injection)            extraTypes = listOf(MyType::class ...)        )    }}
```

---

## Kotlin Multiplatform Dependency Injection

**URL:** https://insert-koin.io/docs/reference/koin-mp/kmp

**Contents:**
- Kotlin Multiplatform Dependency Injection
- Source Project​
- Gradle Dependencies​
- Shared Koin Module​
- Android App​
- iOS App​
  - Calling Koin​
  - Injected Classes​
  - New Native Memory Management​

You can find the Kotlin Multiplatform project here: https://github.com/InsertKoinIO/hello-kmp

Koin is a pure Kotlin library and can be used in your shared Kotlin project. Just add the core dependency:

Add koin-core in common project, declare your dependency: https://github.com/InsertKoinIO/hello-kmp/tree/main/buildSrc

Platform specific components can be declared here, and be used later in Android or iOS (declared directly with actual classes or even actual module)

You can find the shared module sources here: https://github.com/InsertKoinIO/hello-kmp/tree/main/shared

Koin modules need to be gathered via a function:

You can keep using koin-android features and reuse the common modules/classes.

The code for the Android app can be found here: https://github.com/InsertKoinIO/hello-kmp/tree/main/androidApp

The code for the iOS App can be found here: https://github.com/InsertKoinIO/hello-kmp/tree/main/iosApp

Let’s prepare a wrapper to our Koin function (in our shared code):

We can initialize it in our Main app entry:

Let’s call a Kotlin class instance from swift.

Our Kotlin component:

Activate experimental with root gradle.properties.

**Examples:**

Example 1 (kotlin):
```kotlin
// Dependencies.ktobject Versions {    const val koin = "3.2.0"}object Deps {    object Koin {        const val core = "io.insert-koin:koin-core:${Versions.koin}"        const val test = "io.insert-koin:koin-test:${Versions.koin}"        const val android = "io.insert-koin:koin-android:${Versions.koin}"    }}
```

Example 2 (kotlin):
```kotlin
// platform Moduleval platformModule = module {    singleOf(::Platform)}// KMP Class Definitionexpect class Platform() {    val name: String}// iOSactual class Platform actual constructor() {    actual val name: String =        UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion}// Androidactual class Platform actual constructor() {    actual val name: String = "Android ${android.os.Build.VERSION.SDK_INT}"}
```

Example 3 (kotlin):
```kotlin
// Common App Definitionsfun appModule() = listOf(commonModule, platformModule)
```

Example 4 (kotlin):
```kotlin
// Helper.ktfun initKoin(){    startKoin {        modules(appModule())    }}
```

---

## Passing Parameters - Injected Parameters

**URL:** https://insert-koin.io/docs/reference/koin-core/injection-parameters

**Contents:**
- Passing Parameters - Injected Parameters
- Passing values to inject​
- Defining an "injected parameter"​
- Resolving injected parameters in order​
- Resolving injected parameters from graph​
- Injected parameters: indexed values or set (3.4.3)​

In any definition, you can use injection parameters: parameters that will be injected and used by your definition.

Given a definition, you can pass parameters to that definition:

Parameters are sent to your definition with the parametersOf() function (each value separated by comma):

Below is an example of injection parameters. We established that we need a view parameter to build of Presenter class. We use the params function argument to help retrieve our injected parameters:

You can also write your injected parameters directly with the parameters object, as destructured declaration:

Even if the "destructured" declaration is more convenient and readable, it's not type safe. Kotlin won't detect that passed type are in good orders if you have several values

Instead of using get() to resolve a parameter, if you have several parameters of the same type you can use the index as follows get(index) (also same as [ ] operator):

Koin graph resolution (main tree of resolution of all definitions) also let you find your injected parameter. Just use the usual get() function:

In addition to parametersOf, the following API are accessible:

The default function parametersOf is working with both index & set of values:

You can "cascade" parameter injection with parametersOf or parameterArrayOf, to consume value based on index. Or use parametersOf or parameterSetOf to cascading based on type to resolve.

**Examples:**

Example 1 (kotlin):
```kotlin
class Presenter(val a : A, val b : B)val myModule = module {    single { params -> Presenter(a = params.get(), b = params.get()) }}
```

Example 2 (kotlin):
```kotlin
class MyComponent : View, KoinComponent {    val a : A ...    val b : B ...     // inject this as View value    val presenter : Presenter by inject { parametersOf(a, b) }}
```

Example 3 (kotlin):
```kotlin
class Presenter(val view : View)val myModule = module {    single { params -> Presenter(view = params.get()) }}
```

Example 4 (kotlin):
```kotlin
class Presenter(val view : View)val myModule = module {    single { (view : View) -> Presenter(view) }}
```

---

## Koin for Jetpack Compose and Compose Multiplatform

**URL:** https://insert-koin.io/docs/reference/koin-compose/compose

**Contents:**
- Koin for Jetpack Compose and Compose Multiplatform
- Koin Compose Multiplatform vs Koin Android Jetpack Compose​
  - What Koin package for Compose?​
- Starting over an existing Koin context​
- Starting Koin with a Compose App - KoinApplication​
- Compose Preview with KoinApplicationPreview​
- Injecting into a @Composable​
  - Injecting into a @Composable with Parameters​
- ViewModel for @Composable​
  - Shared Activity ViewModel (4.1 - Android)​

This page describe how you can inject your dependencies for your Android Jetpack Compose or your Multiplaform Compose apps.

Since mid-2024, Compose applications can be done with the Koin Multiplatform API. All APIs are identical between Koin Jetpack Compose (koin-androidx-compose) and Koin Compose Multiplatform (koin-compose).

For a pure Android app that uses only the Android Jetpack Compose API, use the following packages:

For an Android/Multiplatform app, use the following packages:

By using the startKoin function previous to your Compose application, your application is ready to welcome Koin injection. Nothing is required anymore to setup your Koin context with Compose.

KoinContext and KoinAndroidContext are deprecated

If you don't have access to a space where you can run the startKoin function, you can relay on Compose and Koin to start your Koin configuration.

The compose function KoinApplication helps to create a Koin application instance, as a Composable:

The KoinApplication function will handle the start and stop of your Koin context, regarding the cycle of the Compose context. This function starts and stops a new Koin application context.

In an Android Application, the KoinApplication will handle any need to stop/restart Koin context regarding configuration changes or drop of Activities.

(Experimental API) You can use the KoinMultiplatformApplication to replace a multiplatform entry point: it's the same as KoinApplication but injects automatically androidContext and androidLogger for you.

The KoinApplicationPreview compose function is dedicated to preview a Composable:

While writing your composable function, you gain access to the following Koin API: koinInject(), to inject instance from Koin container

For a module that declares a 'MyService' component:

We can get your instance like that:

To keep aligned on the functional aspect of Jetpack Compose, the best writing approach is to inject instances directly into functions parameters. This way allow to have default implementation with Koin, but keep open to inject instances how you want.

While you request a new dependency from Koin, you may need to inject parameters. To do this you can use parameters parameter of the koinInject function, with the parametersOf() function like this:

You can use parameters with lambda injection like koinInject<MyService>{ parametersOf("a_string") }, but this can have a performance impact if your recomposing a lot around. This version with lambda needs to unwrap your parameters on call, to help avoid remembering your parameters.

From version 4.0.2 of Koin, koinInject(Qualifier,Scope,ParametersHolder) is introduced to let you use parameters in the most efficient way

The same way you have access to classical single/factory instances, you gain access to the following Koin ViewModel API:

For a module that declares a 'MyViewModel' component:

We can get your instance like that:

We can get your instance in the function parameters:

Lazy API are not supported with updates of Jetpack Compose

You can now use the koinActivityViewModel() to inject a ViewModel from the same ViewModel host: Activity.

You can have a SavedStateHandle constructor parameter, which will be injected regarding the Compose environment (Navigation BackStack or ViewModel). Either it's injected via ViewModel CreationExtras or via Navigation BackStackEntry:

More details about SavedStateHandle injection difference: https://github.com/InsertKoinIO/koin/issues/1935#issuecomment-2362335705

Koin Compose Naviation has now a NavBackEntry.sharedKoinViewModel() function, to allow to retrieve ViewModel already stored in current NavBackEntry. Inside your navigation part, just use sharedKoinViewModel:

Koin offers you a way to load specific modules for a given Composable function. The rememberKoinModules function load Koin modules and remember on current Composable:

You can use one of the abandon function, to unload module on 2 aspects:

For this use unloadOnForgotten or unloadOnAbandoned argument for rememberKoinModules.

The composable function rememberKoinScope and KoinScope allow to handle Koin Scope in a Composable, follow-up current to close scope once Composable is ended.

this API is still unstable for now

**Examples:**

Example 1 (kotlin):
```kotlin
@Composablefun App() {    KoinApplication(application = {        modules(...)    }) {                // your screens here ...        MyScreen()    }}
```

Example 2 (kotlin):
```kotlin
@Preview(name = "1 - Pixel 2 XL", device = Devices.PIXEL_2_XL, locale = "en")@Preview(name = "2 - Pixel 5", device = Devices.PIXEL_5, locale = "en", uiMode = Configuration.UI_MODE_NIGHT_YES)@Preview(name = "3 - Pixel 7 ", device = Devices.PIXEL_7, locale = "ru", uiMode = Configuration.UI_MODE_NIGHT_YES)@Composablefun previewVMComposable(){    KoinApplicationPreview(application = { modules(appModule) }) {        ViewModelComposable()    }}
```

Example 3 (kotlin):
```kotlin
val androidModule = module {    single { MyService() }    // or constructor DSL    singleOf(::MyService)}
```

Example 4 (kotlin):
```kotlin
@Composablefun App() {    val myService = koinInject<MyService>()}
```

---

## Isolated Context with Compose Applications

**URL:** https://insert-koin.io/docs/reference/koin-compose/isolated-context

**Contents:**
- Isolated Context with Compose Applications
- Define isolated context​
- Setup isolated context with Compose​

With a Compose application, you can work the same way with an isolated context to deal with SDK or white label application, in order to not mix your Koin definitions with an end user's one.

First let's declare our isolated context holder, in order to store our isolated Koin instance in memory. This can be done with a simple Object class like this. The MyIsolatedKoinContext class is holding our Koin instance:

Adapt the MyIsolatedKoinContext class according your need of initialization

Now that you have defined an isolated Koin context, we can seting up it up to Compose to use it and override all the API. Just use the KoinIsolatedContext at the root Compose function. This will propagate your Koin context in all child composables.

All Koin Compose APIs will use your Koi isolated context after the use of KoinIsolatedContext

**Examples:**

Example 1 (kotlin):
```kotlin
object MyIsolatedKoinContext {    val koinApp = koinApplication {        // declare used modules        modules(sdkAppModule)    }}
```

Example 2 (kotlin):
```kotlin
@Composablefun App() {    // Set current Koin instance to Compose context    KoinIsolatedContext(context = MyIsolatedKoinContext.koinApp) {        MyScreen()    }}
```

---

## WorkManager

**URL:** https://insert-koin.io/docs/reference/koin-android/workmanager

**Contents:**
- WorkManager
- WorkManager DSL​
- Setup WorkManager​
- Declare ListenableWorker​
  - Creating extra work manager factories​
- A few assumptions​
  - Add manifest changes in koin lib itself​
  - DSL Improvement option:​

The koin-androidx-workmanager project is dedicated to bring Android WorkManager features.

At start, in your KoinApplication declaration, use the workManagerFactory() keyword to a setup custom WorkManager instance:

It's also important that you edit your AndroidManifest.xml to prevent Android initializing its default WorkManagerFactory, as shown in https://developer.android.com/topic/libraries/architecture/workmanager/advanced/custom-configuration#remove-default . Failing to do so will make the app crash.

You can also write a WorkManagerFactory and hand it over to Koin. It will be added as a delegate.

In case both Koin and workFactory1 provided WorkManagerFactory can instantiate a ListenableWorker, the factory provided by Koin will be the one used.

We can make it one step less for application developers if koin-androidx-workmanager's own manifest disables the default work manager. However, it can be confusing since if the app developer don't initialize koin's work manager infrastructure, he'll end up having no usable work manager factories.

That's something that checkModules could help: if any class in the project implements ListenableWorker we inspect both manifest and code and make sure they make sense?

then have koin internals do something like

**Examples:**

Example 1 (kotlin):
```kotlin
class MainApplication : Application(), KoinComponent {    override fun onCreate() {        super.onCreate()        startKoin {            // setup a WorkManager instance            workManagerFactory()            modules(...)        }        setupWorkManagerFactory()}
```

Example 2 (xml):
```xml
<application . . .>        . . .        <provider            android:name="androidx.startup.InitializationProvider"            android:authorities="${applicationId}.androidx-startup"            android:exported="false"            tools:node="merge">            <meta-data                android:name="androidx.work.WorkManagerInitializer"                android:value="androidx.startup"                tools:node="remove" />        </provider>    </application>
```

Example 3 (kotlin):
```kotlin
val appModule = module {    single { MyService() }    worker { MyListenableWorker(get()) }}
```

Example 4 (kotlin):
```kotlin
class MainApplication : Application(), KoinComponent {    override fun onCreate() {        super.onCreate()        startKoin {           workManagerFactory(workFactory1, workFactory2)           . . .        }        setupWorkManagerFactory()    }}
```

---

## Injecting in Android

**URL:** https://insert-koin.io/docs/reference/koin-android/get-instances

**Contents:**
- Injecting in Android
- Ready for Android Classes​
- Using the Android Context in a Definition​
- Android Scope & Android Context resolution​

Once you have declared some modules, and you have started Koin, how can you retrieve your instances in your Android Activity Fragments or Services?

Activity, Fragment & Service are extended with the KoinComponents extension. Any ComponentCallbacks class is accessible for the Koin extensions.

You gain access for the Kotlin extensions:

We can declare a property as lazy injected:

Or we can just directly get an instance:

if your class doesn't have extensions, just implement the KoinComponent interface in it to inject() or get() an instance from another class.

Once your Application class configures Koin you can use the androidContext function to inject Android Context so that it can be resolved later when you need it in modules:

In your definitions, The androidContext() & androidApplication() functions allows you to get the Context instance in a Koin module, to help you simply write expression that requires the Application instance.

While you have a scope that is binding the Context type, you may need to resolve the Context but from different level.

To resolve the right type in MyPresenter, use the following:

**Examples:**

Example 1 (kotlin):
```kotlin
module {    // definition of Presenter    factory { Presenter() }}
```

Example 2 (kotlin):
```kotlin
class DetailActivity : AppCompatActivity() {    // Lazy inject Presenter    override val presenter : Presenter by inject()    override fun onCreate(savedInstanceState: Bundle?) {        //...    }}
```

Example 3 (kotlin):
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {    super.onCreate(savedInstanceState)    // Retrieve a Presenter instance    val presenter : Presenter = get()}
```

Example 4 (kotlin):
```kotlin
class MainApplication : Application() {    override fun onCreate() {        super.onCreate()        startKoin {            // inject Android context            androidContext(this@MainApplication)            // ...        }            }}
```

---

## Kotlin

**URL:** https://insert-koin.io/docs/quickstart/kotlin

**Contents:**
- Kotlin
- Get the code​
- Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- The UserService Component​
- Injecting Dependencies in UserApplication​
- Start Koin​
- Koin module: classic or constructor DSL?​

This tutorial lets you write a Kotlin application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

First, check that the koin-core dependency is added like below:

The idea of the application is to manage a list of users, and display it in our UserApplication class:

Users -> UserRepository -> UserService -> UserApplication

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write the UserService component to request the default user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserService in our Koin module. We declare it as a single definition:

The get() function allow to ask Koin to resolve the needed dependency.

The UserApplication class will help bootstrap instances out of Koin. It will resolve the UserService, thanks to KoinComponent interface. This allows to inject it with the by inject() delegate function:

That's it, your app is ready.

The by inject() function allows us to retrieve Koin instances, in any class that extends KoinComponent

We need to start Koin with our application. Just call the startKoin() function in the application's main entry point, our main function:

The modules() function in startKoin load the given list of modules

Here is the Koin module declaration for our app:

We can write it in a more compact way, by using constructors:

**Examples:**

Example 1 (groovy):
```groovy
dependencies {        // Koin for Kotlin apps    implementation "io.insert-koin:koin-core:$koin_version"}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Modules

**URL:** https://insert-koin.io/docs/reference/koin-core/modules

**Contents:**
- Modules
- What is a module?​
- Using several modules​
- Overriding definition or module (3.1.0+)​
  - Disabling override globally​
  - Explicit override per definition (4.2.0+)​
- Sharing Modules​
- Overriding definition or module (before 3.1.0)​
- Linking modules strategies​
- Module Includes (since 3.2)​

By using Koin, you describe definitions in modules. In this section we will see how to declare, organize & link your modules.

A Koin module is a "space" to gather Koin definition. It's declared with the module function.

Components doesn't have to be necessarily in the same module. A module is a logical space to help you organize your definitions, and can depend on definitions from other module. Definitions are lazy, and they are resolved only when a component is requesting them.

Let's take an example, with linked components in separate modules:

Koin doesn't have any import concept. Koin definitions are lazy: a Koin definition is started with Koin container but is not instantiated. An instance is created only when a request for its type has been done.

We just have to declare list of used modules when we start our Koin container:

Koin will then resolve dependencies from all given modules.

New Koin override strategy allow to override any definition by default. You don't need to specify override = true anymore in your module.

If you have 2 definitions in different modules, that have the same mapping, the last will override the current definition.

You can check in Koin logs, about definition mapping override.

You can specify to not allow overriding in your Koin application configuration with allowOverride(false):

In the case of disabling override, Koin will throw an DefinitionOverrideException exception on any attempt of override.

When you want strict control over overrides (by using allowOverride(false)), but still need specific definitions to override existing ones, you can use the .override() function on individual definitions:

This enables targeted overrides for specific definitions without opening up all definitions to be overridden globally. This is particularly useful for:

You can also use it with the withOptions syntax:

When using the module { } function, Koin preallocate all instance factories. If you need to share a module, please consider return your module with a function.

This way, you share the definitions and avoid preallocating factories in a value.

Koin won't allow you to redefine an already existing definition (type,name,path ...). You will get an error if you try this:

To allow definition overriding, you have to use the override parameter:

Order matters when listing modules and overriding definitions. You must have your overriding definitions in last of your module list.

As definitions between modules are lazy, we can use modules to implement different strategy implementation: declare an implementation per module.

Let's take an example, of a Repository and Datasource. A repository need a Datasource, and a Datasource can be implemented in 2 ways: Local or Remote.

We can declare those components in 3 modules: Repository and one per Datasource implementation:

Then we just need to launch Koin with the right combination of modules:

A new function includes() is available in the Module class, which lets you compose a module by including other modules in an organized and structured way.

The two prominent use cases of the new feature are:

How does it work? Let's take some modules, and we include modules in parentModule:

Notice we do not need to set up all modules explicitly: by including parentModule, all the modules declared in the includes will be automatically loaded (childModule1 and childModule2). In other words, Koin is effectively loading: parentModule, childModule1 and childModule2.

An important detail to observe is that you can use includes to add internal and private modules too - that gives you flexibility over what to expose in a modularized project.

Module loading is now optimized to flatten all your module graphs and avoid duplicated definitions of modules.

Finally, you can include multiple nested or duplicates modules, and Koin will flatten all the included modules removing duplicates:

Notice that all modules will be included only once: dataModule, domainModule, featureModule1, featureModule2.

If you have any compiling issue while including modules from the same file, either use get() Kotlin attribute operator on your module or separate each module in files. See https://github.com/InsertKoinIO/koin/issues/1341 workaround

**Examples:**

Example 1 (kotlin):
```kotlin
val myModule = module {    // Your definitions ...}
```

Example 2 (kotlin):
```kotlin
// ComponentB <- ComponentAclass ComponentA()class ComponentB(val componentA : ComponentA)val moduleA = module {    // Singleton ComponentA    single { ComponentA() }}val moduleB = module {    // Singleton ComponentB with linked instance ComponentA    single { ComponentB(get()) }}
```

Example 3 (kotlin):
```kotlin
// Start Koin with moduleA & moduleBstartKoin {    modules(moduleA,moduleB)}
```

Example 4 (kotlin):
```kotlin
val myModuleA = module {    single<Service> { ServiceImp() }}val myModuleB = module {    single<Service> { TestServiceImp() }}startKoin {    // TestServiceImp will override ServiceImp definition    modules(myModuleA,myModuleB)}
```

---

## Android ViewModel & Navigation

**URL:** https://insert-koin.io/docs/reference/koin-android/viewmodel

**Contents:**
- Android ViewModel & Navigation
- Injecting your ViewModel​
- Activity Shared ViewModel​
- Passing Parameters to the Constructor​
- SavedStateHandle Injection (3.3.0)​
- Navigation Graph ViewModel​
- ViewModel Scope API​
- ViewModel Generic API​
- ViewModel API - Java Compat​

The koin-android Gradle module introduces a new viewModel DSL keyword that comes in complement of single and factory, to help declare a ViewModel component and bind it to an Android Component lifecycle. The viewModelOf keyword is also available, to let you declare a ViewModel with its constructor.

Your declared component must at least extends the android.arch.lifecycle.ViewModel class. You can specify how you inject the constructor of the class and use the get() function to inject dependencies.

The viewModel/viewModelOf keyword helps to declare a factory instance of ViewModel. This instance will be handled by internal ViewModelFactory and reattach ViewModel instance if needed. It also will let inject parameters.

To inject a ViewModel in an Activity, Fragment or Service use:

ViewModel key is calculated against Key and/or Qualifier

One ViewModel instance can be shared between Fragments and their host Activity.

To inject a shared ViewModel in a Fragment use:

The sharedViewModel is deprecated in favor of activityViewModel() functions. The naming of this last one is more explicit.

Just declare the ViewModel only once:

Note: a qualifier for a ViewModel will be handled as a ViewModel's Tag

And reuse it in Activity and Fragments:

The viewModel keyword API is compatible with injection parameters.

From the injection call site:

Add a new property typed SavedStateHandle to your constructor to handle your ViewModel state:

In Koin module, just resolve it with get() or with parameters:

or with Constructor DSL:

To inject a state ViewModel in a Activity,Fragment use:

All stateViewModel functions are deprecated. You can just use the regular viewModel function to inject a SavedStateHandle

You can scope a ViewModel instance to your Navigation graph. Just retrieve with by koinNavGraphViewModel(). You just need your graph id.

see all API to be used for ViewModel and Scopes: ViewModel Scope

Koin provides some "under the hood" API to directly tweak your ViewModel instance. The available functions are viewModelForClass for ComponentActivity and Fragment:

This function is still using state: BundleDefinition, but will convert it to CreationExtras

Note that you can have access to the top level function, callable from anywhere:

Java compatibility must be added to your dependencies:

You can inject the ViewModel instance to your Java codebase by using viewModel() or getViewModel() static functions from ViewModelCompat:

**Examples:**

Example 1 (kotlin):
```kotlin
val appModule = module {    // ViewModel for Detail View    viewModel { DetailViewModel(get(), get()) }    // or directly with constructor    viewModelOf(::DetailViewModel)}
```

Example 2 (kotlin):
```kotlin
class DetailActivity : AppCompatActivity() {    // Lazy inject ViewModel    val detailViewModel: DetailViewModel by viewModel()}
```

Example 3 (kotlin):
```kotlin
val weatherAppModule = module {    // WeatherViewModel declaration for Weather View components    viewModel { WeatherViewModel(get(), get()) }}
```

Example 4 (kotlin):
```kotlin
class WeatherActivity : AppCompatActivity() {    /*     * Declare WeatherViewModel with Koin and allow constructor dependency injection     */    private val weatherViewModel by viewModel<WeatherViewModel>()}class WeatherHeaderFragment : Fragment() {    /*     * Declare shared WeatherViewModel with WeatherActivity     */    private val weatherViewModel by activityViewModel<WeatherViewModel>()}class WeatherListFragment : Fragment() {    /*     * Declare shared WeatherViewModel with WeatherActivity     */    private val weatherViewModel by activityViewModel<WeatherViewModel>()}
```

---

## KSP Compiler Options

**URL:** https://insert-koin.io/docs/reference/koin-annotations/options

**Contents:**
- KSP Compiler Options
- Available Options​
  - KOIN_CONFIG_CHECK​
  - KOIN_LOG_TIMES​
  - KOIN_DEFAULT_MODULE​
  - KOIN_GENERATION_PACKAGE​
  - KOIN_USE_COMPOSE_VIEWMODEL​
  - KOIN_EXPORT_DEFINITIONS​
- Configuration Examples​
  - Gradle Kotlin DSL​

The Koin Annotations KSP processor supports several configuration options that can be passed during compilation to customize code generation behavior.

When using KOIN_GENERATION_PACKAGE, the provided package name must:

Invalid package names will result in compilation errors with descriptive messages.

**Examples:**

Example 1 (kotlin):
```kotlin
ksp {    arg("KOIN_CONFIG_CHECK", "true")    arg("KOIN_LOG_TIMES", "true")    arg("KOIN_DEFAULT_MODULE", "false")    arg("KOIN_GENERATION_PACKAGE", "com.mycompany.koin.generated")    arg("KOIN_USE_COMPOSE_VIEWMODEL", "true")    arg("KOIN_EXPORT_DEFINITIONS", "true")}
```

Example 2 (groovy):
```groovy
ksp {    arg("KOIN_CONFIG_CHECK", "true")    arg("KOIN_LOG_TIMES", "true")    arg("KOIN_DEFAULT_MODULE", "false")    arg("KOIN_GENERATION_PACKAGE", "com.mycompany.koin.generated")    arg("KOIN_USE_COMPOSE_VIEWMODEL", "true")    arg("KOIN_EXPORT_DEFINITIONS", "true")}
```

---

## Start Koin on Android

**URL:** https://insert-koin.io/docs/reference/koin-android/start

**Contents:**
- Start Koin on Android
- From your Application class​
- Extra Configurations​
  - Koin Logging for Android​
  - Loading Properties​
- Start Koin with Androidx Startup (4.0.1) [Experimental]​
- Startup Dependency with Koin​

The koin-android project is dedicated to provide Koin powers to Android world. See the Android setup section for more details.

From your Application class you can use the startKoin function and inject the Android context with androidContext as follows:

You can also start Koin from anywhere if you don't want to start it from your Application class.

If you need to start Koin from another Android class, you can use the startKoin function and provide your Android Context instance with just like:

From your Koin configuration (in startKoin { } block code), you can also configure several parts of Koin.

Within your KoinApplication instance, we have an extension androidLogger which uses the AndroidLogger() class. This logger is an Android implementation of the Koin logger.

Up to you to change this logger if it doesn't suit to your needs.

You can use Koin properties in the assets/koin.properties file, to store keys/values:

By using Gradle packge koin-androidx-startup, we can use KoinStartup interface to declare your Koin configuration your Application class:

This replaces the startKoin function that is usally used in onCreate. The koinConfiguration function is returning a KoinConfiguration instance.

KoinStartup avoid blocking main thread at for startup time, and offers better performances.

You can make your Initializer depend on KoinInitializer if you need Koin to be setup, and allow to inject dependencies:

**Examples:**

Example 1 (kotlin):
```kotlin
class MainApplication : Application() {    override fun onCreate() {        super.onCreate()        startKoin {            // Log Koin into Android logger            androidLogger()            // Reference Android context            androidContext(this@MainApplication)            // Load modules            modules(myAppModules)        }    }}
```

Example 2 (kotlin):
```kotlin
startKoin {    //inject Android context    androidContext(/* your android context */)    // ...}
```

Example 3 (kotlin):
```kotlin
startKoin {    // use Android logger - Level.INFO by default    androidLogger()    // ...}
```

Example 4 (kotlin):
```kotlin
startKoin {    // ...    // use properties from assets/koin.properties    androidFileProperties()   }
```

---

## Android & Annotations

**URL:** https://insert-koin.io/docs/quickstart/android-annotations

**Contents:**
- Android & Annotations
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- Displaying User with Presenter​
- Injecting Dependencies in Android​
- Start Koin​
- Displaying User with ViewModel​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

Let's configure the KSP Plugin like this, and the following dependencies:

See libs.versions.toml for current versions

The idea of the application is to manage a list of users, and display it in our MainActivity class with a Presenter or a ViewModel:

Users -> UserRepository -> (Presenter or ViewModel) -> MainActivity

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Let's declare a AppModule module class like below.

Let's simply add @Single on UserRepositoryImpl class to declare it as singleton:

Let's write a presenter component to display a user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserPresenter in our Koin module. We declare it as a factory definition with the @Factory annotation, to not keep any instance in memory (avoid any leak with Android lifecycle):

The UserPresenter component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the by inject() delegate function:

That's it, your app is ready.

The by inject() function allows us to retrieve Koin instances, in Android components runtime (Activity, fragment, Service...)

We need to start Koin with our Android application. Just call the startKoin() function in the application's main entry point, our MainApplication class:

The Koin module is generated from AppModule with the .module extension: Just use the AppModule().module expression to get the Koin module from the annotations.

The import org.koin.ksp.generated.* import is required to allow to use generated Koin module content

Let's write a ViewModel component to display a user:

UserRepository is referenced in UserViewModel`s constructor

The UserViewModel is tagged with @KoinViewModel annotation to declare the Koin ViewModel definition, to not keep any instance in memory (avoid any leak with Android lifecycle).

The UserViewModel component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the by viewModel() delegate function:

Koin Annotations allows to check your Koin configuration at compile time. This is available by jusing the following Gradle option:

We can ensure that our Koin configuration is good before launching our app, by verifying our Koin configuration with a simple JUnit Test.

Add the Koin Android dependency like below:

The androidVerify() function allow to verify the given Koin modules:

With just a JUnit test, you can ensure your definitions configuration are not missing anything!

**Examples:**

Example 1 (groovy):
```groovy
plugins {    alias(libs.plugins.ksp)}dependencies {    // ...    implementation(libs.koin.annotations)    ksp(libs.koin.ksp)}// Compile time checkksp {    arg("KOIN_CONFIG_CHECK","true")}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
@Module@ComponentScan("org.koin.sample")class AppModule
```

---

## Koin

**URL:** https://insert-koin.io/docs/setup/koin

**Contents:**
- Koin
- Current Versions​
- Gradle Setup​
  - Kotlin​
  - Android​
  - Jetpack Compose or Compose Multiplatform​
  - Kotlin Multiplatform​
  - Ktor​
  - Koin BOM​

All you need to setting up Koin in your project

You can find all Koin packages on Maven Central.

Here are the currently available Koin versions:

Starting from 3.5.0 you can use BOM-version to manage all Koin library versions. When using the BOM in your app, you don't need to add any version to the Koin library dependencies themselves. When you update the BOM version, all the libraries that you're using are automatically updated to their new versions.

Add koin-bom BOM and koin-core dependency to your application:

If you are using version catalogs:

Or use an old way of specifying the exact dependency version for Koin:

You are now ready to start Koin:

If you need testing capacity:

From now you can continue on Koin Tutorials to learn about using Koin: Kotlin App Tutorial

Add koin-android dependency to your Android application:

You are now ready to start Koin in your Application class:

If you need extra features, add the following needed package:

From now you can continue on Koin Tutorials to learn about using Koin: Android App Tutorial

Add koin-compose dependency to your multiplatform application, for use Koin & Compose API:

If you are using pure Android Jetpack Compose, you can go with

Add koin-core dependency to your multiplatform application, for shared Kotlin part:

From now you can continue on Koin Tutorials to learn about using Koin: Kotlin Multiplatform App Tutorial

Add koin-ktor dependency to your Ktor application:

You are now ready to install Koin feature into your Ktor application:

From now you can continue on Koin Tutorials to learn about using Koin: Ktor App Tutorial

The Koin Bill of Materials (BOM) lets you manage all of your Koin library versions by specifying only the BOM’s version. The BOM itself has links to the stable versions of the different Koin libraries, in such a way that they work well together. When using the BOM in your app, you don't need to add any version to the Koin library dependencies themselves. When you update the BOM version, all the libraries that you're using are automatically updated to their new versions.

**Examples:**

Example 1 (kotlin):
```kotlin
implementation(project.dependencies.platform("io.insert-koin:koin-bom:$koin_version"))implementation("io.insert-koin:koin-core")
```

Example 2 (toml):
```toml
[versions]koin-bom = "x.x.x"...[libraries]koin-bom = { module = "io.insert-koin:koin-bom", version.ref = "koin-bom" }koin-core = { module = "io.insert-koin:koin-core" }...
```

Example 3 (kotlin):
```kotlin
dependencies {    implementation(project.dependencies.platform(libs.koin.bom))    implementation(libs.koin.core)}
```

Example 4 (kotlin):
```kotlin
dependencies {    implementation("io.insert-koin:koin-core:$koin_version")}
```

---

## Dependency Injection in Ktor

**URL:** https://insert-koin.io/docs/reference/koin-ktor/ktor

**Contents:**
- Dependency Injection in Ktor
- Install Koin Plugin​
  - Compatible with Ktor's DI (4.1)​
- Inject in Ktor​
  - Resolve from Ktor Request Scope (since 4.1)​
  - Declare Koin modules in Ktor module (4.1)​
  - Ktor Events​

The koin-ktor module is dedicated to bringing dependency injection for Ktor.

To start a Koin container in Ktor, just install the Koin plugin as follows:

Koin 4.1 fully supports new Ktor 3.2!

We extracted CoreResolver to abstract resolution rules for Koin and allow extension with ResolutionExtension. We added new KtorDIExtension as Ktor ResolutionExtension to help Koin resolve Ktor default DI instance.

Koin Ktor plugin is automatically setting up Ktor DI integration. Below, see how you can consume Ktor dependencies from Koin:

Koin inject() and get() functions are available from Application, Route, and Routing classes:

You can declare components to live within the Ktor request scope timeline. For this, you just need to declare your component inside a requestScope section. Given a ScopeComponent class to instantiate on the Ktor web request scope, let's declare it:

And from your HTTP call, simply call call.scope.get() to resolve the right dependency:

This allows your scoped dependency to resolve ApplicationCall as scope's source of your resolution. You can inject it directly into constructor:

For each new request, the scope will be recreated. This creates and drops scope instances for each request

Use Application.koinModule {} or Application.koinModules() directly within your app setup to declare new modules within your Ktor module:

You can listen to KTor Koin events:

**Examples:**

Example 1 (kotlin):
```kotlin
fun Application.main() {    // Install Koin    install(Koin) {        slf4jLogger()        modules(helloAppModule)    }}
```

Example 2 (kotlin):
```kotlin
// let's define a Ktor objectfun Application.setupDatabase(config: DbConfig) {    // ...    dependencies {        provide<Database> { database }    }}
```

Example 3 (kotlin):
```kotlin
// let's inject it in a Koin definitionclass CustomerRepositoryImpl(private val database: Database) : CustomerRepository    fun Application.customerDataModule() {        koinModule {            singleOf(::CustomerRepositoryImpl) bind CustomerRepository::class        }}
```

Example 4 (kotlin):
```kotlin
fun Application.main() {    // inject HelloService    val service by inject<HelloService>()    routing {        get("/hello") {            call.respondText(service.sayHello())        }    }}
```

---

## Android - Jetpack Compose

**URL:** https://insert-koin.io/docs/quickstart/android-compose

**Contents:**
- Android - Jetpack Compose
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- Displaying User with UserViewModel​
  - The UserViewModel class​
  - Injecting ViewModel in Compose​
- Displaying User with UserStateHolder​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

Add the Koin Android dependency like below:

The idea of the application is to manage a list of users, and display it in our MainActivity class with a Presenter or a ViewModel:

Users -> UserRepository -> (Presenter or ViewModel) -> Composable

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write a ViewModel component to display a user:

UserRepository is referenced in UserViewModel's constructor

We declare UserViewModel in our Koin module. We declare it as a viewModelOf definition, to not keep any instance in memory (avoid any leak with Android lifecycle):

The get() function allow to ask Koin to resolve the needed dependency.

The UserViewModel component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the koinViewModel() function:

The koinViewModel function allows us to retrieve a ViewModel instances, create the associated ViewModel Factory for you and bind it to the lifecycle

Let's write a State holder component to display a user:

UserRepository is referenced in UserViewModel's constructor

We declare UserStateHolder in our Koin module. We declare it as a factoryOf definition, to not keep any instance in memory (avoid any leak with Android lifecycle):

The UserStateHolder component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the koinInject() function:

The koinInject function allows us to retrieve a ViewModel instances, create the associated ViewModel Factory for you and bind it to the lifecycle

We need to start Koin with our Android application. Just call the startKoin() function in the application's main entry point, our MainApplication class:

The modules() function in startKoin load the given list of modules

While starting the Compose application we need to link Koin to our current Compose application, with KoinAndroidContext:

Here is the Koin moduel declaration for our app:

We can write it in a more compact way, by using constructors:

We can ensure that our Koin configuration is good before launching our app, by verifying our Koin configuration with a simple JUnit Test.

Add the Koin Android dependency like below:

The verify() function allow to verify the given Koin modules:

With just a JUnit test, you can ensure your definitions configuration are not missing anything!

**Examples:**

Example 1 (groovy):
```groovy
dependencies {    // Koin for Android    implementation "io.insert-koin:koin-androidx-compose:$koin_version"}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Multiple Koin Modules in Android

**URL:** https://insert-koin.io/docs/reference/koin-android/modules-android

**Contents:**
- Multiple Koin Modules in Android
- Using several modules​
- Module Includes (since 3.2)​
- Reducing Startup time with background module loading​
  - Key Features​
  - Parallel Loading Performance (4.2.0+)​
  - Waiting for completion​

By using Koin, you describe definitions in modules. In this section we will see how to declare, organize & link your modules.

Components don't have to be necessarily in the same module. A module is a logical space to help you organize your definitions, and can depend on definitions from another module. Definitions are lazy, and they are resolved only when a component requests them.

Let's take an example, with linked components in separate modules:

We just have to declare list of used modules when we start our Koin container:

Up to you to organise your self per Gradle module, and gather several Koin modules.

Check Koin Modules Section for more details

A new function includes() is available in the Module class, which lets you compose a module by including other modules in an organized and structured way.

The two prominent use cases of the new feature are:

How does it work? Let's take some modules, and we include modules in parentModule:

Notice we do not need to set up all modules explicitly: by including parentModule, all the modules declared in the includes will be automatically loaded (childModule1 and childModule2). In other words, Koin is effectively loading: parentModule, childModule1 and childModule2.

An important detail to observe is that you can use includes to add internal and private modules too - that gives you flexibility over what to expose in a modularized project.

Module loading is now optimized to flatten all your module graphs and avoid duplicated definitions of modules.

Finally, you can include multiple nested or duplicates modules, and Koin will flatten all the included modules removing duplicates:

Notice that all modules will be included only once: dataModule, domainModule, featureModule1, featureModule2.

You can declare "lazy" Koin modules to avoid triggering any pre-allocation of resources and load them in parallel background coroutines. This helps avoid blocking the Android startup process and significantly reduces startup time when you have multiple modules.

Starting from version 4.2.0, lazy modules are loaded in parallel, with each module getting its own coroutine job. This dramatically improves startup time:

You can wait for all lazy modules to finish loading before proceeding:

See Lazy Modules Documentation for more details on parallel loading and multiplatform support

**Examples:**

Example 1 (kotlin):
```kotlin
// ComponentB <- ComponentAclass ComponentA()class ComponentB(val componentA : ComponentA)val moduleA = module {    // Singleton ComponentA    single { ComponentA() }}val moduleB = module {    // Singleton ComponentB with linked instance ComponentA    single { ComponentB(get()) }}
```

Example 2 (kotlin):
```kotlin
class MainApplication : Application() {    override fun onCreate() {        super.onCreate()        startKoin {            // ...            // Load modules            modules(moduleA, moduleB)        }            }}
```

Example 3 (kotlin):
```kotlin
// `:feature` moduleval childModule1 = module {    /* Other definitions here. */}val childModule2 = module {    /* Other definitions here. */}val parentModule = module {    includes(childModule1, childModule2)}// `:app` modulestartKoin { modules(parentModule) }
```

Example 4 (kotlin):
```kotlin
// :feature moduleval dataModule = module {    /* Other definitions here. */}val domainModule = module {    /* Other definitions here. */}val featureModule1 = module {    includes(domainModule, dataModule)}val featureModule2 = module {    includes(domainModule, dataModule)}
```

---

## Lazy Modules and Background Loading

**URL:** https://insert-koin.io/docs/reference/koin-core/lazy-modules

**Contents:**
- Lazy Modules and Background Loading
- Defining Lazy Modules​
- Parallel Loading with Kotlin Coroutines​
  - Key Functions​
  - Parallel Loading Performance (4.2.0+)​
  - Basic Usage​
  - Platform-Specific Behavior​
  - Custom Dispatcher​
  - Suspending Alternative​
  - Limitation - Mixing Modules/Lazy Modules​

In this section we will see how to organize your modules with lazy loading approach and parallel initialization.

You can declare lazy Koin modules to avoid triggering any pre-allocation of resources and load them asynchronously in the background during Koin startup.

A good example is always better to understand:

LazyModule won't trigger any resources until it has been loaded by the following API

Once you have declared some lazy modules, you can load them in parallel in the background from your Koin configuration.

Starting from version 4.2.0, lazy modules are loaded in parallel, with each module getting its own coroutine job. This significantly improves startup time when you have multiple modules:

Multiplatform Support (4.2.0+):

You can specify a custom dispatcher for lazy module loading:

Default dispatcher for coroutines engine is Dispatchers.Default

For platforms that don't support blocking or if you're already in a coroutine context, use the suspend functions:

For now we advise to avoid mixing modules & lazy modules, in the startup. Avoid having mainModule requiring dependency in lazyReporter.

For now Koin doesn't check if your module depends on a lazy modules

**Examples:**

Example 1 (kotlin):
```kotlin
// Some lazy modulesval m2 = lazyModule {    singleOf(::ClassB)}// include m2 lazy moduleval m1 = lazyModule {    includes(m2)    singleOf(::ClassA) { bind<IClassA>() }}
```

Example 2 (kotlin):
```kotlin
val module1 = lazyModule {    singleOf(::DatabaseService)}val module2 = lazyModule {    singleOf(::NetworkService)}val module3 = lazyModule {    singleOf(::AnalyticsService)}startKoin {    // All three modules load in parallel!    lazyModules(module1, module2, module3)}
```

Example 3 (kotlin):
```kotlin
startKoin {    // load lazy Modules in background (parallel)    lazyModules(m1, m2, m3)}val koin = KoinPlatform.getKoin()// wait for loading jobs to finishkoin.waitAllStartJobs()// or run code after loading is done (JVM only)koin.runOnKoinStarted { koin ->    // run after background load complete}
```

Example 4 (kotlin):
```kotlin
startKoin {    // Load modules on IO dispatcher    lazyModules(m1, m2, dispatcher = Dispatchers.IO)}
```

---

## Injecting in Tests

**URL:** https://insert-koin.io/docs/reference/koin-test/testing

**Contents:**
- Injecting in Tests
- Making your test a KoinComponent with KoinTest​
- JUnit Rules​
  - Create a Koin context for your test​
  - Specify your Mock Provider​
- Mocking out of the box​
- Declaring a component on the fly​
- Checking your Koin modules​
- Starting & stopping Koin for your tests​
- Testing with JUnit5​

Warning: This does not apply to Android Instrumented tests. For Instrumented testing with Koin, please see Android Instrumented Testing

By tagging your class KoinTest, your class become a KoinComponent and bring you:

Don't hesitate to overload Koin modules configuration to help you partly build your app.

You can easily create and hold a Koin context for each of your test with the following rule:

To let you use the declareMock API, you need to specify a rule to let Koin know how you build your Mock instance. This let you choose the right mocking framework for your need.

Create mocks using Mockito:

Create mocks using MockK:

!> koin-test project is not tied anymore to mockito

Instead of making a new module each time you need a mock, you can declare a mock on the fly with declareMock:

declareMock can specify if you want a single or factory, and if you want to have it in a module path.

When a mock is not enough and don't want to create a module just for this, you can use declare:

Koin offers a way to test if you Koin modules are good: checkModules - walk through your definition tree and check if each definition is bound

Take attention to stop your koin instance (if you use startKoin in your tests) between every test. Else be sure to use koinApplication, for local koin instances or stopKoin() to stop the current global instance.

JUnit 5 support provides Extensions that will handle the starting and stopping of Koin context. This means that if you are using the extension you don't need to use the AutoCloseKoinTest.

For testing with JUnit5 you need to use koin-test-junit5 dependency.

You need to Register the KoinTestExtension and provide your module configuration. After this is done you can either get or inject your components to the test. Remember to use @JvmField with the @RegisterExtension.

This works the same way as in JUnit4 except you need to use @RegisterExtension.

You can also get the created koin context as a function parameter. This can be achieved by adding a function parameter to the test function.

**Examples:**

Example 1 (kotlin):
```kotlin
class ComponentAclass ComponentB(val a: ComponentA)class MyTest : KoinTest {    // Lazy inject property    val componentB : ComponentB by inject()    @Test    fun `should inject my components`() {        startKoin {            modules(                module {                    single { ComponentA() }                    single { ComponentB(get()) }                })        }        // directly request an instance        val componentA = get<ComponentA>()        assertNotNull(a)        assertEquals(componentA, componentB.a)    }
```

Example 2 (kotlin):
```kotlin
@get:Ruleval koinTestRule = KoinTestRule.create {    // Your KoinApplication instance here    modules(myModule)}
```

Example 3 (kotlin):
```kotlin
@get:Ruleval mockProvider = MockProviderRule.create { clazz ->    // Your way to build a Mock here    Mockito.mock(clazz.java)}
```

Example 4 (kotlin):
```kotlin
@get:Ruleval mockProvider = MockProviderRule.create { clazz ->    // Your way to build a Mock here    mockkClass(clazz)}
```

---

## Start Koin

**URL:** https://insert-koin.io/docs/reference/koin-core/start-koin

**Contents:**
- Start Koin
  - The startKoin function​
  - Extending your Koin start (help reuse for KMP and other ...)​
  - Behind the start - Koin instance under the hood​
  - Loading modules after startKoin​
  - Unloading modules​
  - Stop Koin - closing all resources​
- Logging​
  - Set logging at start​
- Loading properties​

Koin is a DSL, a lightweight container and a pragmatic API. Once you have declared your definitions within Koin modules, you are ready to start the Koin container.

The startKoin function is the main entry point to launch Koin container. It needs a list of Koin modules to run. Modules are loaded and definitions are ready to be resolved by the Koin container.

Once startKoin has been called, Koin will read all your modules & definitions. Koin is then ready for any get() or by inject() call to retrieve the needed instance.

Your Koin container can have several options:

The startKoin can't be called more than once. If you need several point to load modules, use the loadKoinModules function.

Koin now supports reusable and extensible configuration objects for KoinConfiguration. You can extract shared configuration for use across platforms (Android, iOS, JVM, etc.) or tailor it to different environments. This can be done with the includes() function. Below, we can reuse easily a common configuration, and extend it to add some Android environment settings:

When we start Koin, we create a KoinApplication instance that represents the Koin container configuration instance. Once launched, it will produce a Koin instance resulting of your modules and options. This Koin instance is then hold by the GlobalContext, to be used by any KoinComponent class.

The GlobalContext is a default JVM context strategy for Koin. It's called by startKoin and register to GlobalContext. This will allow us to register a different kind of context, in the perspective of Koin Multiplatform.

You can't call the startKoin function more than once. But you can use directly the loadKoinModules() functions.

This function is interesting for SDK makers who want to use Koin, because they don't need to use the startKoin() function and just use the loadKoinModules at the start of their library.

it's possible also to unload a bunch of definition, and then release theirs instance with the given function:

You can close all the Koin resources and drop instances & definitions. For this you can use the stopKoin() function from anywhere, to stop the Koin GlobalContext. Else on a KoinApplication instance, just call close()

Koin has a simple logging API to log any Koin activity (allocation, lookup ...). The logging API is represented by the class below:

Koin proposes some implementation of logging, in function of the target platform:

By default, Koin use the EmptyLogger. You can use directly the PrintLogger as following:

You can load several type of properties at start:

Be sure to load properties at Koin start:

In a Koin module, you can get a property by its key:

in /src/main/resources/koin.properties file

Just load it with getProperty function:

Your Koin application can now activate some experimental features through a dedicated options section, like:

**Examples:**

Example 1 (kotlin):
```kotlin
// start a KoinApplication in Global contextstartKoin {    // declare used modules    modules(coffeeAppModule)}
```

Example 2 (kotlin):
```kotlin
fun initKoin(config : KoinAppDeclaration? = null){   startKoin {        includes(config) //can include external configuration extension        modules(appModule)   }}class MainApplication : Application() {    override fun onCreate() {        super.onCreate()        initKoin {            androidContext(this@MainApplication)            androidLogger()        }    }}
```

Example 3 (kotlin):
```kotlin
loadKoinModules(module1,module2 ...)
```

Example 4 (kotlin):
```kotlin
unloadKoinModules(module1,module2 ...)
```

---

## Compose Multiplatform - Shared UI

**URL:** https://insert-koin.io/docs/quickstart/cmp

**Contents:**
- Compose Multiplatform - Shared UI
- Get the code​
- Application Overview​
- The "User" Data​
- The Shared Koin module​
- The Shared ViewModel​
- Native Component​
- Injecting in Compose​
- Compose app in iOS​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 15 min to do the tutorial.

The source code is available at on Github

The idea of the application is to manage a list of users, and display it in our native UI, witha shared ViewModel:

Users -> UserRepository -> Shared Presenter -> Compose UI

All the common/shared code is located in shared Gradle project

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write a ViewModel component to display a user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserViewModel in our Koin module. We declare it as a viewModelOf definition, to not keep any instance in memory and let the native system hold it:

The Koin module is available as function to run (appModule here), to be easily runned from iOS side, with initKoin() function.

The following native component is defined in Android and iOS:

Both get local platform implementation

All the Common Compose app is located in commonMain from composeApp Gradle module:

The UserViewModel component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the koinViewModel or koinNavViewModel compose function:

That's it, your app is ready.

We need to start Koin with our Android application. Just call the KoinApplication() function in the compose application function App:

The modules() function load the given list of modules

All the iOS app is located in iosMain folder

The MainViewController.kt is ready to start Compose for iOS:

**Examples:**

Example 1 (kotlin):
```kotlin
data class User(val name : String)
```

Example 2 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 3 (kotlin):
```kotlin
module {    singleOf(::UserRepositoryImpl) { bind<UserRepository>() }}
```

Example 4 (kotlin):
```kotlin
class UserViewModel(private val repository: UserRepository) : ViewModel() {    fun sayHello(name : String) : String{        val foundUser = repository.findUser(name)        val platform = getPlatform()        return foundUser?.let { "Hello '$it' from ${platform.name}" } ?: "User '$name' not found!"    }}
```

---

## Android

**URL:** https://insert-koin.io/docs/quickstart/android

**Contents:**
- Android
- Get the code​
- Gradle Setup​
- Application Overview​
- The "User" Data​
- The Koin module​
- Displaying User with Presenter​
- Injecting Dependencies in Android​
- Start Koin​
- Koin module: classic or constructor DSL?​

This tutorial lets you write an Android application and use Koin dependency injection to retrieve your components. You need around 10 min to do the tutorial.

The source code is available at on Github

Add the Koin Android dependency like below:

The idea of the application is to manage a list of users, and display it in our MainActivity class with a Presenter or a ViewModel:

Users -> UserRepository -> (Presenter or ViewModel) -> MainActivity

We will manage a collection of Users. Here is the data class:

We create a "Repository" component to manage the list of users (add users or find one by name). Here below, the UserRepository interface and its implementation:

Use the module function to declare a Koin module. A Koin module is the place where we define all our components to be injected.

Let's declare our first component. We want a singleton of UserRepository, by creating an instance of UserRepositoryImpl

Let's write a presenter component to display a user:

UserRepository is referenced in UserPresenter`s constructor

We declare UserPresenter in our Koin module. We declare it as a factoryOf definition, to not keep any instance in memory (avoid any leak with Android lifecycle):

The get() function allow to ask Koin to resolve the needed dependency.

The UserPresenter component will be created, resolving the UserRepository instance with it. To get it into our Activity, let's inject it with the by inject() delegate function:

That's it, your app is ready.

The by inject() function allows us to retrieve Koin instances, in Android components runtime (Activity, fragment, Service...)

We need to start Koin with our Android application. Just call the startKoin() function in the application's main entry point, our MainApplication class:

The modules() function in startKoin load the given list of modules

Here is the Koin module declaration for our app:

We can write it in a more compact way, by using constructors:

We can ensure that our Koin configuration is good before launching our app, by verifying our Koin configuration with a simple JUnit Test.

Add the Koin Android dependency like below:

The verify() function allow to verify the given Koin modules:

With just a JUnit test, you can ensure your definitions configuration are not missing anything!

**Examples:**

Example 1 (groovy):
```groovy
dependencies {    // Koin for Android    implementation("io.insert-koin:koin-android:$koin_version")}
```

Example 2 (kotlin):
```kotlin
data class User(val name : String)
```

Example 3 (kotlin):
```kotlin
interface UserRepository {    fun findUser(name : String): User?    fun addUsers(users : List<User>)}class UserRepositoryImpl : UserRepository {    private val _users = arrayListOf<User>()    override fun findUser(name: String): User? {        return _users.firstOrNull { it.name == name }    }    override fun addUsers(users : List<User>) {        _users.addAll(users)    }}
```

Example 4 (kotlin):
```kotlin
val appModule = module {    }
```

---

## Extension Manager

**URL:** https://insert-koin.io/docs/reference/koin-core/extension-manager

**Contents:**
- Extension Manager
- Defining an extension​
- Starting an extension​
- Resolver Engine & Resolution Extension​

Here is a brief description of KoinExtension manager, dedicated to add new features inside Koin framework.

A Koin extension consist in having a class inheriting from KoinExtension interface:

this interface allow to ensure you get passed a Koin instance, and the extension is called when Koin is closing.

To start an extension, just extend the right place of the system, and register it with Koin.extensionManager.

Below here is how we define the coroutinesEngine extension:

Below here is how we call the coroutinesEngine extension:

Koin's resolution algorithm has been reworked to be pluggable and extensible. The new CoreResolver and ResolutionExtension APIs allow integration with external systems or custom resolution logic.

Internally, resolution now traverses stack elements more efficiently, with cleaner propagation across scopes and parent hierarchies. This will fix many issues related to the linked scope walk-through and allow better integration of Koin in other systems.

See below a test demoing resolution extension:

**Examples:**

Example 1 (kotlin):
```kotlin
interface KoinExtension {    fun onRegister(koin : Koin)    fun onClose()}
```

Example 2 (kotlin):
```kotlin
fun KoinApplication.coroutinesEngine() {    with(koin.extensionManager) {        if (getExtensionOrNull<KoinCoroutinesEngine>(EXTENSION_NAME) == null) {            registerExtension(EXTENSION_NAME, KoinCoroutinesEngine())        }    }}
```

Example 3 (kotlin):
```kotlin
val Koin.coroutinesEngine: KoinCoroutinesEngine get() = extensionManager.getExtension(EXTENSION_NAME)
```

Example 4 (kotlin):
```kotlin
@Testfun extend_resolution_test(){    val resolutionExtension = object : ResolutionExtension {        val instanceMap = mapOf<KClass<*>, Any>(            Simple.ComponentA::class to Simple.ComponentA()        )        override val name: String = "hello-extension"        override fun resolve(            scope: Scope,            instanceContext: ResolutionContext        ): Any? {            return instanceMap[instanceContext.clazz]        }    }    val koin = koinApplication{        printLogger(Level.DEBUG)        koin.resolver.addResolutionExtension(resolutionExtension)        modules(module {            single { Simple.ComponentB(get())}        })    }.koin    assertEquals(resolutionExtension.instanceMap[Simple.ComponentA::class], koin.get<Simple.ComponentB>().a)    assertEquals(1,koin.instanceRegistry.instances.values.size)}
```

---

## Context Isolation

**URL:** https://insert-koin.io/docs/reference/koin-core/context-isolation

**Contents:**
- Context Isolation
- What is Context Isolation?​
- Testing​

For SDK Makers, you can also work with Koin in a non-global way: use Koin for the DI of your library and avoid any conflict by people using your library and Koin by isolating your context.

In a standard way, we can start Koin like that:

This uses the default Koin context to register your dependencies.

But if we want to use an isolated Koin instance, you need to declare an instance and store it in a class to hold your instance. You will have to keep your Koin Application instance available in your library and pass it to your custom KoinComponent implementation:

The MyIsolatedKoinContext class is holding our Koin instance here:

Let's use MyIsolatedKoinContext to define our IsolatedKoinComponent class, a KoinComponent that will use our isolated context:

Everything is ready, just use IsolatedKoinComponent to retrieve instances from isolated context:

To test classes that are retrieving dependencies with by inject() delegate override getKoin() method and define custom Koin module:

**Examples:**

Example 1 (kotlin):
```kotlin
// start a KoinApplication and register it in Global contextstartKoin {    // declare used modules    modules(...)}
```

Example 2 (kotlin):
```kotlin
// Get a Context for your Koin instanceobject MyIsolatedKoinContext {    private val koinApp = koinApplication {        // declare used modules        modules(coffeeAppModule)    }    val koin = koinApp.koin }
```

Example 3 (kotlin):
```kotlin
internal interface IsolatedKoinComponent : KoinComponent {    // Override default Koin instance    override fun getKoin(): Koin = MyIsolatedKoinContext.koin}
```

Example 4 (kotlin):
```kotlin
class MyKoinComponent : IsolatedKoinComponent {    // inject & get will target MyKoinContext}
```

---

## Definitions with Annotations

**URL:** https://insert-koin.io/docs/reference/koin-annotations/definitions

**Contents:**
- Definitions with Annotations
  - Generate Compose ViewModel for Kotlin Multiplatform (since 1.4.0)​
- Automatic or Specific Binding​
- Nullable Dependencies​
- Qualifier with @Named​
- Injected Parameters with @InjectedParam​
- Injecting a lazy dependency - Lazy<T>​
- Injecting a list of dependencies - List<T>​
- Properties with @Property​
  - @PropertyValue - Property with default value (since 1.4)​

Koin Annotations allow declaring the same kind of definitions as the regular Koin DSL, but with annotations. Just tag your class with the needed annotation, and it will generate everything for you!

For example, the equivalent of single { MyComponent(get()) } DSL declaration is just done by tagging with @Single like this:

Koin Annotations keep the same semantics as the Koin DSL. You can declare your components with the following definitions:

For Scopes, check the Declaring Scopes section.

The @KoinViewModel annotation generates ViewModels using the koin-core-viewmodel main DSL by default (enabled since 2.2.0). This provides Kotlin Multiplatform compatibility and uses the unified ViewModel API.

The KOIN_USE_COMPOSE_VIEWMODEL option is enabled by default:

This generates viewModel definitions with org.koin.compose.viewmodel.dsl.viewModel for multiplatform compatibility.

When declaring a component, all detected "bindings" (associated supertypes) will already be prepared for you. For example, the following definition:

Koin will declare that your MyComponent component is also tied to MyInterface. The DSL equivalent is single { MyComponent(get()) } bind MyInterface::class.

Instead of letting Koin detect things for you, you can also specify what type you really want to bind with the binds annotation parameter:

If your component is using nullable dependency, don't worry it will be handled automatically for you. Keep using your definition annotation, and Koin will guess what to do:

The generated DSL equivalent will be single { MyComponent(getOrNull()) }

Note that this also works for injected Parameters and properties

You can add a "name" to a definition (also called qualifier), to make a distinction between several definitions for the same type, with the @Named annotation:

When resolving a dependency, just use the qualifier with named function:

It is also possible to create custom qualifier annotations. Using the previous example:

You can tag a constructor member as "injected parameter", which means that the dependency will be passed in the graph when calling for resolution.

Then you can call your MyComponent and pass an instance of MyDependency:

The generated DSL equivalent will be single { params -> MyComponent(params.get()) }

Koin can automatically detect and resolve a lazy dependency. Here, for example, we want to resolve lazily the LoggerDataSource definition. You just need to use the Lazy Kotlin type as follows:

Behind it will generate the DSL like with inject() instead of get():

Koin can automatically detect and resolve a list of dependencies. Here, for example, we want to resolve all LoggerDataSource definitions. You just need to use the List Kotlin type as follows:

Behind it will generate the DSL, like with getAll() function:

To resolve a Koin property in your definition, just tag a constructor member with @Property. This will resolve the Koin property thanks to the value passed to the annotation:

The generated DSL equivalent will be factory { ComponentWithProps(getProperty("id")) }

Koin Annotations offers you the possibility to define a default value for a property, directly from your code with @PropertyValue annotation. Let's follow our sample:

The generated DSL equivalent will be factory { ComponentWithProps(getProperty("id", ComponentWithProps.DEFAULT_ID)) }

Koin Annotations provides JSR-330 (Jakarta Inject) compatible annotations through the koin-jsr330 module. These annotations are particularly useful for developers migrating from other JSR-330 compatible frameworks like Hilt, Dagger, or Guice.

Add the koin-jsr330 dependency to your project:

JSR-330 standard singleton annotation, equivalent to Koin's @Single:

This generates the same result as @Single - a singleton instance in Koin.

JSR-330 standard qualifier annotation for string-based qualifiers:

JSR-330 standard injection annotation. While Koin Annotations doesn't require explicit constructor marking, @Inject can be used for JSR-330 compatibility:

Meta-annotation for creating custom qualifier annotations:

Meta-annotation for creating custom scope annotations:

You can freely mix JSR-330 annotations with Koin annotations in the same project:

Using JSR-330 annotations provides several advantages for framework migration:

JSR-330 annotations in Koin generate the same underlying DSL as their Koin equivalents. The choice between JSR-330 and Koin annotations is purely stylistic and based on team preferences or migration requirements.

**Examples:**

Example 1 (kotlin):
```kotlin
@Singleclass MyComponent(val myDependency : MyDependency)
```

Example 2 (groovy):
```groovy
ksp {    // This is the default behavior since 2.2.0    arg("KOIN_USE_COMPOSE_VIEWMODEL","true")}
```

Example 3 (kotlin):
```kotlin
@Singleclass MyComponent(val myDependency : MyDependency) : MyInterface
```

Example 4 (kotlin):
```kotlin
@Single(binds = [MyBoundType::class])
```

---

## Application, Configuration and Modules

**URL:** https://insert-koin.io/docs/reference/koin-annotations/modules

**Contents:**
- Application, Configuration and Modules
- Application Bootstrap with @KoinApplication​
- Configuration Management with @Configuration​
  - Basic Configuration Usage​
  - Multiple Configuration Support​
  - Environment-Specific Configurations​
  - Using Configurations with @KoinApplication​
- Default Module (Deprecated since 1.3.0)​
- Class Module with @Module​
- Components Scan with @ComponentScan​

To create a complete Koin application bootstrap, you can use the @KoinApplication annotation on an entry point class. This annotation helps generate Koin application bootstrap functions:

This generates two functions for starting your Koin application:

Both generated functions support custom configuration:

The @KoinApplication annotation supports:

When no configurations are specified, it automatically loads the "default" configuration.

The @Configuration annotation allows you to organize modules into different configurations (environments, flavors, etc.). This is useful for organizing modules by deployment environment or feature sets.

The default configuration is named "default", can be used with @Configuration or @Configuration("default")

You need to use the @KoinApplication to be able to scan modules from configuration:

A module can be associated with multiple configurations:

By default, the @KoinApplication is loading all default configurations (modules tagged with @Configuration)

You can also reference these configurations in your application bootstrap:

The default module approach is deprecated since Annotations 1.3.0. We recommend using explicit modules with @Module and @Configuration annotations for better organization and clarity.

While using definitions, you may need to organize them in modules or not. Previously, you could use the "default" generated module to host definitions without explicit modules.

If you don't want to specify any module, Koin provides a default one to host all your definitions. The defaultModule is ready to be used directly:

Recommended approach: Instead of using the default module, organize your definitions in explicit modules:

Don't forget to use the org.koin.ksp.generated.* import

To declare a module, just tag a class with @Module annotation:

To load your module in Koin, just use the .module extension generated for any @Module class. Just create a new instance of your module MyModule().module:

Don't forget to use the org.koin.ksp.generated.* import

To scan and gather annotated components into a module, just use the @ComponentScan annotation on a module:

This will scan the current package and subpackages for annotated components. You can specify to scan a given package with @ComponentScan("com.my.package")

When using @ComponentScan annotation, KSP traverses across all Gradle modules for the same package. (since 1.4)

To define a definition directly in your code, you can annotate a function with definition annotations:

Note: @InjectedParam (for injected parameters from startKoin) and @Property (for property injection) are also usable on function members. See the definitions documentation for more details on these annotations.

To include other class modules in your module, use the includes attribute of the @Module annotation:

This way you can just run your root module:

**Examples:**

Example 1 (kotlin):
```kotlin
@KoinApplication // load default configurationobject MyApp@KoinApplication(    configurations = ["default", "production"],     modules = [MyModule::class])object MyApp
```

Example 2 (kotlin):
```kotlin
// The import below gives you access to generated extension functionsimport org.koin.ksp.generated.*fun main() {    // Option 1: Start Koin directly    MyApp.startKoin()        // Option 2: Get KoinApplication instance    val koinApp = MyApp.koinApplication()}
```

Example 3 (kotlin):
```kotlin
fun main() {    MyApp.startKoin {        printLogger()        // Add other Koin configuration    }        // Or with koinApplication    MyApp.koinApplication {        printLogger()    }}
```

Example 4 (kotlin):
```kotlin
// Put module in default Configuration@Module@Configurationclass CoreModule
```

---

## Android Scopes

**URL:** https://insert-koin.io/docs/reference/koin-android/scope

**Contents:**
- Android Scopes
- Working with the Android lifecycle​
- Scope for Android Components (since 3.2.1)​
  - Declare an Android Scope​
  - Android Scope Classes​
  - Android Scope API​
  - AndroidScopeComponent and handling Scope closing​
  - Scope Archetypes (4.1.0)​
  - ViewModel Scope (updated in 4.1.0)​
- Scope Links​

Android components are mainly managed by their lifecycle: we can't directly instantiate an Activity nor a Fragment. The system make all creation and management for us, and make callbacks on methods: onCreate, onStart...

That's why we can't describe our Activity/Fragment/Service in a Koin module. We need then to inject dependencies into properties and also respect the lifecycle: Components related to the UI parts must be released on soon as we don't need them anymore.

Long live components can be easily described as single definitions. For medium and short live components we can have several approaches.

In the case of MVP architecture style, the Presenter is a short live component to help/support the UI. The presenter must be created each time the screen is showing, and dropped once the screen is gone.

A new Presenter is created each time

We can describe it in a module:

Most of Android memory leaks come from referencing a UI/Android component from a non Android component. The system keeps a reference on it and can't totally drop it via garbage collection.

To scope dependencies on an Android component, you have to declare a scope section with the scope block like follow:

Koin offers ScopeActivity, RetainedScopeActivity and ScopeFragment classes to let you use directly a declared scope for Activity or Fragment:

Under the hood, Android scopes needs to be used with AndroidScopeComponent interface to implement scope field like this:

We need to use the AndroidScopeComponent interface and implement the scope property. This will setting up the default scope used by your class.

To create a Koin scope bound to an Android component, just use the following functions:

Those functions are available as delegate, to implement different kind of scope:

We can also to setting up a retained scope (backed by a ViewModel lifecycle) with the following:

If you don't want to use Android Scope classes, you can work with your own and use AndroidScopeComponent with the Scope creation API

You can run code before Koin Scope is destroyed, by overriding the onCloseScope function from AndroidScopeComponent:

If you try to access Scope from onDestroy() function, the scope will already be closed.

As a new feature, you can now declare scope by archetype: you don't need to define a scope against a specific type, but for an "archetype" (a kind of scope class). You can declare a scope for "Activity", "Fragment", or "ViewModel". You can now use the following DSL sections:

This allows for better reuse of definitions between scopes easily. No need to use a specific type like scope<>{ }, apart from if you need scope on a precise object.

See Android Scope API to see how to use by activityScope(), by activityRetainedScope(), and by fragmentScope() functions to activate your Android scope. Those functions will trigger scope archetypes.

For example, you can easily scope a defintion to an activity like that, with Scope Archetypes:

ViewModel is only created against the root scope to avoid any leaking (leaking Activity or Fragment ...). This guards for the visibility problem, where the ViewModel could have access to incompatible scopes.

:::warn ViewModel can't access to Activity or Fragment scope. Why? Because ViewModel is lasting long than Activity and Fragment, and then it would leak dependencies outside of proper scopes. If you need to bridge a dependency from outside a ViewModel scope, you can use "injected parameters" to pass some objects to your ViewModel: viewModel { p -> } :::

Declare your ViewModel scope as follows, tied to your ViewModel class or using the viewModelScope DSL section:

Once you have declared your ViewModel and your scoped components, you can choose between:

Now just call your ViewModel from your Activity or Fragment:

Scope links allow sharing instances between components with custom scopes. By default, Fragment's scope are linked to parent Activity scope.

In a more extended usage, you can use a Scope instance across components. For example, if we need to share a UserSession instance.

First, declare a scope definition:

When needed to begin use a UserSession instance, create a scope for it:

Then use it anywhere you need it:

**Examples:**

Example 1 (kotlin):
```kotlin
class DetailActivity : AppCompatActivity() {    // injected Presenter    override val presenter : Presenter by inject()
```

Example 2 (kotlin):
```kotlin
val androidModule = module {    // Factory instance of Presenter    factory { Presenter() }}
```

Example 3 (kotlin):
```kotlin
val androidModule = module {    scope<DetailActivity> {        scoped { Presenter() }    }}
```

Example 4 (kotlin):
```kotlin
class MyPresenter()class MyAdapter(val presenter : MyPresenter)module {  // Declare scope for MyActivity  scope<MyActivity> {   // get MyPresenter instance from current scope    scoped { MyAdapter(get()) }   scoped { MyPresenter() }  }   // or  activityScope {   scoped { MyAdapter(get()) }   scoped { MyPresenter() }  }}
```

---

## Scopes

**URL:** https://insert-koin.io/docs/reference/koin-core/scopes

**Contents:**
- Scopes
- What is a scope?​
- Scope definition​
  - Scope Id & Scope Name​
  - Scope Component: Associate a scope to a component [2.2.0]​
  - Resolving dependencies within a scope​
  - Close a scope​
  - Getting scope's source value​
  - Scope Linking​
  - Scope Archetypes​

Koin brings a simple API to let you define instances that are tied to a limit lifetime.

Scope is a fixed duration of time or method calls in which an object exists. Another way to look at this is to think of scope as the amount of time an object’s state persists. When the scope context ends, any objects bound under that scope cannot be injected again (they are dropped from the container).

By default, in Koin, we have 3 kind of scopes:

To declare a scoped definition, use the scoped function like follow. A scope gathers scoped definitions as a logical unit of time.

Declaring a scope for a given type, we need to use the scope keyword:

A Koin Scope is defined by its:

scope<A> { } is equivalent to scope(named<A>()){ } , but more convenient to write. Note that you can also use a string qualifier like: scope(named("SCOPE_NAME")) { }

From a Koin instance, you can access:

By default calling createScope on an object, doesn't pass the "source" of the scope. You need to pass it as parameters: T.createScope(<source>)

Koin has the concept of KoinScopeComponent to help bring a scope instance to its class:

The KoinScopeComponent interface brings several extensions:

Let's define a scope for A, to resolve B:

We can then resolve instance of B directly thanks to org.koin.core.scope get & inject extensions:

To resolve a dependency using the scope's get & inject functions: val presenter = scope.get<Presenter>()

The interest of a scope is to define a common logical unit of time for scoped definitions. It's allow also to resolve definitions from within the given scope

The dependency resolution is then straight forward:

By default, all scopes fallback to resolve in the main scope if no definition is found in the current scope

Once you are finished with your scope instance, just close it with the close() function:

Beware that you can't inject instances anymore from a closed scope.

Koin Scope API in 2.1.4 allow you to pass the original source of a scope, in a definition. Let's take an example below. Let's have a singleton instance A:

By creating A's scope, we can forward the reference of the scope's source (A instance), to underlying definitions of the scope: scoped { BofA(getSource()) } or even scoped { BofA(get()) }

This in order to avoid cascading parameter injection, and just retrieve our source value directly in scoped definition.

Difference between getSource() and get(): getSource will directly get the source value. Get will try to resolve any definition, and fallback to source value if possible. getSource() is then more efficient in terms of performances.

Koin Scope API in 2.1 allow you to link a scope to another, and then allow to resolve joined definition space. Let's take an example. Here we are defining, 2 scopes spaces: a scope for A and a scope for B. In A's scope, we don't have access to C (defined in B's scope).

With scope linking API, we can allow to resolve B's scope instance C, directly from A's scope. For this we use linkTo() on scope instance:

Scope "Archetypes" are scope spaces for a generic kind of classes. For example, you can have Scope Archetypes for Android (Activity, Fragment, ViewModel) or even Ktor (RequestScope). Scope Archetype is Koin's TypeQualifier pass to different APIs, to request scope space for a given

An archetype consists of:

**Examples:**

Example 1 (kotlin):
```kotlin
module {    scope<MyType>{        scoped { Presenter() }        // ...    }}
```

Example 2 (kotlin):
```kotlin
class A : KoinScopeComponent {    override val scope: Scope by lazy { createScope(this) }}class B
```

Example 3 (kotlin):
```kotlin
module {    scope<A> {        scoped { B() } // Tied to A's scope    }}
```

Example 4 (kotlin):
```kotlin
class A : KoinScopeComponent {    override val scope: Scope by lazy { newScope(this) }    // resolve B as inject    val b : B by inject() // inject from scope    // Resolve B    fun doSomething(){        val b = get<B>()    }    fun close(){        scope.close() // don't forget to close current scope    }}
```

---
