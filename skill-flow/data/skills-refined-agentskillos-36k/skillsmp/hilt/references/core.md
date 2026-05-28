# Hilt - Core

**Pages:** 13

---

## Creating extensions

**URL:** https://dagger.dev/hilt/creating-extensions

**Contents:**
- Creating extensions
- Generating modules and entry points
  - @GeneratesRootInput
  - @OriginatingElement

Hilt is particularly well-suited for extensions or libraries that want to integrate with Hilt due to the standard components and the way modules and entry points are picked up from the classpath.

However, extensions that generate an @InstallIn module or entry point will need to add some extra information to the generated classes in order for them to be picked up by Hilt correctly.

Because Hilt picks up modules and entry points from the classpath implicitly, Hilt needs extra information to know if it needs to wait for your extension to generate code before it tries to generate the Dagger components. This is done by annotating your annotation class that triggers your code generation with @GeneratesRootInput.

For example, if an extension generated a module every time someone used a @GenerateMyModule annotation, @GenerateMyModule would need to be annotated like so:

Note that if not annotated, Hilt is not necessarily guaranteed to miss your modules because it may still pick them up if waiting on something else to be generated. This is of course unreliable.

As described in the testing page, nested modules in tests are isolated to the enclosing test. Generated modules for a test, however, cannot be generated as a nested class. To properly support this, generated code should be annotated with an @OriginatingElement annotation with the top-level class as the value. Note that this is not always the same as the enclosing class since there may be many layers of nesting.

For example, assume an extension is triggered by the following code and generates a module called FooTest_FooModule.

Then the generated FooTest_FooModule would need to be annotated like so:

**Examples:**

Example 1 (java):
```java
@GeneratesRootInput
public @interface GenerateMyModule {}
```

Example 2 (unknown):
```unknown
@GeneratesRootInput
public @interface GenerateMyModule {}
```

Example 3 (kotlin):
```kotlin
@GeneratesRootInput
annotation class GenerateMyModule {}
```

Example 4 (unknown):
```unknown
@GeneratesRootInput
annotation class GenerateMyModule {}
```

---

## Entry Points

**URL:** https://dagger.dev/hilt/entry-points.html

**Contents:**
- Entry Points
- What is an entry point?
- When do you need an entry point?
- How to use an entry point?
  - Create an EntryPoint
  - Access an EntryPoint
- Best practice: where to define an entry point interface?
    - Best practice
    - Bad practice
- Visibility

An entry point is the boundary where you can get Dagger-provided objects from code that cannot use Dagger to inject its dependencies. It is the point where code first enters into the graph of objects managed by Dagger.

If you’re already familiar with Dagger components, an entry point is just an interface that the Hilt generated component will extend.

You will need an entry point when interfacing with non-Dagger libraries or Android components that are not yet supported in Hilt and need to get access to Dagger objects.

In general though, most entry points will be at Android instantiated locations like the activities, fragments, etc. @AndroidEntryPoint is a specialized tool to handle the definition of entry points and access to the entry points (among other things) for these classes. Since this is already handled specially for those Android classes, for the following docs, we’ll assume the entry point is needed in some other type of class.

To create an entry point, define an interface with an accessor method for each binding type needed (including its qualifier) and mark the interface with the @EntryPoint annotation. Then add @InstallIn to specify the component in which to install the entry point.

To access an entry point, use the EntryPoints class passing as a parameter the component instance or the @AndroidEntryPoint object which acts as a component holder. Make sure the component you pass in matches the @InstallIn annotation on the @EntryPoint interface that you pass in as well.

Using the entry point interface we defined above:

Additionally, the methods in EntryPointAccessors are more appropriate and type safe for retrieving entry points from the standard Android components.

If implementing a class instantiated from a non-Hilt library and a Foo class is needed from Dagger, should the entry point interface be defined with the using class or with Foo?

In general, the answer is that the entry point should be defined with the using class since that class is the reason for needing the entry point interface, not Foo. If that class later needs more dependencies, extra methods can easily be added to the entry point interface to get them. Essentialy, the entry point interface acts in place of the @Inject constructor for that class. If instead the entry point were defined with Foo, then other people may be confused about if they should inject Foo or use the entry point interface. It would also result in more entry point interfaces being added if other dependencies are needed in the future.

All types returned from an entry point’s method must be public. This is because the generated Dagger component, which is often not in the same package, must implement the entry point method.

**Examples:**

Example 1 (java):
```java
@EntryPoint
@InstallIn(SingletonComponent.class)
public interface FooBarInterface {
  @Foo Bar bar();
}
```

Example 2 (unknown):
```unknown
@EntryPoint
@InstallIn(SingletonComponent.class)
public interface FooBarInterface {
  @Foo Bar bar();
}
```

Example 3 (kotlin):
```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface FooBarInterface {
  @Foo fun bar(): Bar
}
```

Example 4 (unknown):
```unknown
@EntryPoint
@InstallIn(SingletonComponent::class)
interface FooBarInterface {
  @Foo fun bar(): Bar
}
```

---

## Hilt Components

**URL:** https://dagger.dev/hilt/components

**Contents:**
- Hilt Components
- Component hierarchy
- Components used for injection
- Component lifetimes
    - Scoped vs unscoped bindings
    - Scoping in modules
    - When to scope?
- Component default bindings

Note: The following page assumes a basic knowledge of Dagger, including components, modules, scopes, and bindings. (For a refresher, see Dagger users guide.)

Unlike traditional Dagger, Hilt users never define or instantiate Dagger components directly. Instead, Hilt offers predefined components that are generated for you. Hilt comes with a built-in set of components (and corresponding scope annotations) that are automatically integrated into the various lifecycles of an Android application. The diagram below shows the standard Hilt component hierarchy. The annotation above each component is the scoping annotation used to scope bindings to the lifetime of that component. The arrow below a component points to any child components. As normal, a binding in a child component can have dependencies on any binding in an ancestor component.

Note: When scoping a binding within an @InstallIn module, the scope on the binding must match the scope of the component. For example, a binding within an @InstallIn(ActivityComponent.class) module can only be scoped with @ActivityScoped.

When using Hilt APIs like @AndroidEntryPoint to inject your Android classes, the standard Hilt components are used as the injectors. The component used as the injector will determine which bindings are visible to that Android class. The components used are shown in the table below:

The lifetime of a component is important because it relates to the lifetime of your bindings in two important ways:

Component lifetimes are generally bounded by the creation and destruction of a corresponding instance of an Android class. The table below lists the scope annotation and bounded lifetime for each component.

By default, all bindings in Dagger are “unscoped”. This means that each time the binding is requested, Dagger will create a new instance of the binding.

However, Dagger also allows a binding to be “scoped” to a particular component (see the scope annotations in the table above). A scoped binding will only be created once per instance of the component it’s scoped to, and all requests for that binding will share the same instance.

Warning: A common misconception is that all fragment instances will share the same instance of a binding scoped with @FragmentScoped. However, this is not true. Each fragment instance gets a new instance of the fragment component, and thus a new instance of all its scoped bindings.

The previous section showed how to scope a binding declared with an @Inject constructor, but a binding declared in a module can also be scoped in a similar way.

Warning: A common misconception is that all bindings declared in a module will be scoped to the component the module is installed in. However, this isn’t true. Only bindings declarations annotated with a scope annotation will be scoped.

Scoping a binding has a cost on both the generated code size and its runtime performance so use scoping sparingly. The general rule for determining if a binding should be scoped is to only scope the binding if it’s required for the correctness of the code. If you think a binding should be scoped for purely performance reasons, first verify that the performance is an issue, and if it is consider using @Reusable instead of a component scope.

Each Hilt component comes with a set of default bindings that can be injected as dependencies into your own custom bindings. Each component listed has the corresponding default bindings as well as any default bindings from an ancestor component.

ActivityRetainedComponent lives across configuration changes, so it is created at the first onCreate and last onDestroy. ↩ ↩2

The Application binding is available using either @ApplicationContext Context or Application. [^3]: @ActivityRetainedSavedState SavedStateHandlemust be used with @OptIn(UnstableApi.class). This binding relies on an experimental implementation to lazily create SavedStateHandle, which should be safe to rely on, but it is still possible that a future release may remove the binding if a bug is uncovered. ↩

**Examples:**

Example 1 (java):
```java
// This binding is "unscoped".
// Each request for this binding will get a new instance.
final class UnscopedBinding {
  @Inject UnscopedBinding() {}
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
final class ScopedBinding {
  @Inject ScopedBinding() {}
}
```

Example 2 (unknown):
```unknown
// This binding is "unscoped".
// Each request for this binding will get a new instance.
final class UnscopedBinding {
  @Inject UnscopedBinding() {}
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
final class ScopedBinding {
  @Inject ScopedBinding() {}
}
```

Example 3 (kotlin):
```kotlin
// This binding is "unscoped".
// Each request for this binding will get a new instance.
class UnscopedBinding @Inject constructor() {
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
class ScopedBinding @Inject constructor() {
}
```

Example 4 (unknown):
```unknown
// This binding is "unscoped".
// Each request for this binding will get a new instance.
class UnscopedBinding @Inject constructor() {
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
class ScopedBinding @Inject constructor() {
}
```

---

## Subcomponents vs Component dependencies

**URL:** https://dagger.dev/hilt/subcomponents-vs-deps.html

**Contents:**
- Subcomponents vs Component dependencies
- Overview
- Single binding key space
- Propagating bindings with component dependencies defeats Dagger pruning
- Configuration at the root and build speed

Hilt is based around using Dagger subcomponents as opposed to component dependencies. This page explains some of the reasons why Hilt was designed this way.

Subcomponents propagate all bindings by default. This includes multibindings which can be difficult to propagate via component dependencies. This creates a merged binding key space. This generally makes it easier to understand the Dagger graph because you don’t have to worry about considering if a binding is propagated or not from a parent component to a child component. Also, if bindings are not propagated with component dependencies, it is possible to use two different definitions of the same binding key in different components. This can make it difficult to walk through code when debugging issues as the binding definition will be based on the context of the usage.

One of the downsides of a single binding key space is that it can be extra work to place restrictions on code usage (e.g. if one feature shouldn’t use bindings from another feature). For this we generally recommend using qualifier annotations that are restricted visibility or using an SPI plugin to enforce separation of code. Using a qualifier or an SPI plugin is better than building these concerns into the structure of your Dagger component dependencies graph because often these rules encode policy. Policy decisions like this are often in flux (or need to have exceptions allowed) and having to restructure a Dagger component dependencies graph based on those changes can be costly.

Since Dagger can see the entry points to the graph, it can figure out which bindings are unused and not generate code for those bindings. This optimization goes through subcomponents, but it is defeated by component dependencies because propagating bindings through component dependencies adds entry point methods. So even if entry point methods are only used by other Dagger components and across the components the binding is unused, Dagger will be forced to still generate that dead code to adhere to its contract.

One of the main advantages of component dependencies is building Dagger code separately and in parallel. This can be done because of the lack of implicit sharing that make components black boxes with respect to each other. However, Hilt is already based on the idea of central configuration based on build dependencies. Since Hilt has to aggregate modules, all components would be generated at the same time anyway so we wouldn’t be able to take advantage of building in parallel.

Instead, to address build speed, Hilt recommends making smaller test apps for individual feature development. Without Hilt, this would have been difficult to do because of all of the repeated Dagger boilerplate for the small test app. However, with Hilt generating all of the Dagger portion based on build dependencies, putting together a small test app should be much easier.

---

## Entry Points

**URL:** https://dagger.dev/hilt/entry-points

**Contents:**
- Entry Points
- What is an entry point?
- When do you need an entry point?
- How to use an entry point?
  - Create an EntryPoint
  - Access an EntryPoint
- Best practice: where to define an entry point interface?
    - Best practice
    - Bad practice
- Visibility

An entry point is the boundary where you can get Dagger-provided objects from code that cannot use Dagger to inject its dependencies. It is the point where code first enters into the graph of objects managed by Dagger.

If you’re already familiar with Dagger components, an entry point is just an interface that the Hilt generated component will extend.

You will need an entry point when interfacing with non-Dagger libraries or Android components that are not yet supported in Hilt and need to get access to Dagger objects.

In general though, most entry points will be at Android instantiated locations like the activities, fragments, etc. @AndroidEntryPoint is a specialized tool to handle the definition of entry points and access to the entry points (among other things) for these classes. Since this is already handled specially for those Android classes, for the following docs, we’ll assume the entry point is needed in some other type of class.

To create an entry point, define an interface with an accessor method for each binding type needed (including its qualifier) and mark the interface with the @EntryPoint annotation. Then add @InstallIn to specify the component in which to install the entry point.

To access an entry point, use the EntryPoints class passing as a parameter the component instance or the @AndroidEntryPoint object which acts as a component holder. Make sure the component you pass in matches the @InstallIn annotation on the @EntryPoint interface that you pass in as well.

Using the entry point interface we defined above:

Additionally, the methods in EntryPointAccessors are more appropriate and type safe for retrieving entry points from the standard Android components.

If implementing a class instantiated from a non-Hilt library and a Foo class is needed from Dagger, should the entry point interface be defined with the using class or with Foo?

In general, the answer is that the entry point should be defined with the using class since that class is the reason for needing the entry point interface, not Foo. If that class later needs more dependencies, extra methods can easily be added to the entry point interface to get them. Essentialy, the entry point interface acts in place of the @Inject constructor for that class. If instead the entry point were defined with Foo, then other people may be confused about if they should inject Foo or use the entry point interface. It would also result in more entry point interfaces being added if other dependencies are needed in the future.

All types returned from an entry point’s method must be public. This is because the generated Dagger component, which is often not in the same package, must implement the entry point method.

**Examples:**

Example 1 (java):
```java
@EntryPoint
@InstallIn(SingletonComponent.class)
public interface FooBarInterface {
  @Foo Bar bar();
}
```

Example 2 (unknown):
```unknown
@EntryPoint
@InstallIn(SingletonComponent.class)
public interface FooBarInterface {
  @Foo Bar bar();
}
```

Example 3 (kotlin):
```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface FooBarInterface {
  @Foo fun bar(): Bar
}
```

Example 4 (unknown):
```unknown
@EntryPoint
@InstallIn(SingletonComponent::class)
interface FooBarInterface {
  @Foo fun bar(): Bar
}
```

---

## Design Overview

**URL:** https://dagger.dev/hilt/design-overview

**Contents:**
- Design Overview
- Component generation and module/entry point installation
- @AndroidEntryPoint injection

Hilt generates components by finding all of the modules and entry points in the transitive classpath. The @InstallIn annotation on every module and entry point generates a small metadata class in a defined package. The special package is inspected when processing @HiltAndroidApp to find all of the aggregated items that need to be installed in the components. The same strategy is used for other helper classes like @DefineComponent and @AliasOf.

Since the Android Application is generated at the same time, the generated Application has a direct reference to the root generated component which is the SingletonComponent.

Since the HiltTestApplication must support multiple tests, unlike in the production application, reflection is used to find the generated components. This is helpful because it allows the test application to be decoupled from building with the tests which allows Hilt to provide a convenient default instead of requiring each project to code generate a test application. Reflection is not used in production because it provides less value and reflection may have more costs.

Aggregating all of the modules in the classpath works well for tests because it means tests can easily add bindings by just nesting classes in the test class (or even better using @BindValue which generates the module). Similarly, the module detection also allows classes to embed @Module classes as inner classes. This can be used to ensure the class cannot be used without the associated Dagger bindings and makes its usage less error prone (e.g. pairing a class with an @BindsOptionalOf it consumes or an @Binds to an interface).

@AndroidEntryPoint works by generating a base class that the user code extends either directly or indirectly via a transform in the Gradle plugin. This base class is responsible for retrieving the parent component (via Hilt interfaces on the parent), creating the component, injecting the class, and exposing the component to children via Hilt interfaces.

For example, to inject the activity the generated code essentially does the following (simplified for readability):

The generation of all of this glue code makes breaking dependencies with unsafe casts safe and easy. Also, the automatic discovery combined with the fact that the interfaces are generated with the activity that uses them makes it so that including or removing an @AndroidEntryPoint adds/takes all of its dependencies with it. This allows apps built with Hilt to be modular.

Most of the time the parent component is easy to get, but in the case of views and fragments it isn’t so easy because views get the activity context. To support views with fragment bindings, the generated base class for fragments override getLayoutInflater to wrap the Context in a ContextWrapper that holds the Dagger component for the view to get.

By standardizing all of these design decisions in Hilt, integrating libraries with activities/fragments/views should be much easier.

**Examples:**

Example 1 (unknown):
```unknown
@Override public void onCreate(Bundled savedInstanceState) {
  // This gets the parent component from the Application (in reality there is
  // actually the activity retained component as the parent).
  Object parentComponent =
      ((GeneratedComponentManager) getApplication()).generatedComponent();
  // This creates the activity component. This involves an unsafe cast
  // to know the parent component has the methods to build the activity component.
  Object activityComponent = ((ActivityComponentBuilderEntryPoint) parentComponent)
      .activityComponentBuilder()
      .activity(this)
      .build();
  // This injects the activity. It also involves an unsafe cast to get access
  // to the activity inject method. Like the other unsafe casts, these casts
  // break build dependencies and are safe because they are code generated and
  // guaranteed via the classpath discovery of modules/interfaces.
  (MyActivity_GeneratedInjector) activityComponent).inject(this).
}
```

---

## Modules

**URL:** https://dagger.dev/hilt/modules

**Contents:**
- Modules
- Hilt Modules
  - Using @InstallIn
  - Installing a module in multiple components
- App Build variants
- Bazel: Organizing your BUILD files
- Hilt module visibility best practice

Hilt modules are standard Dagger modules that have an additional @InstallIn annotation that determines which Hilt component(s) to install the module into.

When the Hilt components are generated, the modules annotated with @InstallIn will be installed into the corresponding component or subcomponent via @Component#modules or @Subcomponent#modules respectively. Just like in Dagger, installing a module into a component allows that binding to be accessed as a dependency of other bindings in that component or any child component(s) below it in the component hierarchy. They can also be accessed from the corresponding @AndroidEntryPoint classes. Being installed in a component also allows that binding to be scoped to that component.

A module is installed in a Hilt Component by annotating the module with the @InstallIn annotation. These annotations are required on all Dagger modules when using Hilt, but this check may be optionally disabled.

Note: If a module does not have an @InstallIn annotation, the module will not be part of the component and may result in compilation errors.

Specify which Hilt Component to install the module in by passing in the appropriate Component type(s) to the @InstallIn annotation. For example, to install a module so that anything in the application can use it, use SingletonComponent:

Each component comes with a scoping annotation that can be used to memoize a binding to the lifetime of the component. For example, to scope a binding to the SingletonComponent component, use the @Singleton annotation:

In addition, each component has bindings that are available to it by default. (See Hilt Components for a complete list.) For example, the SingletonComponent component provides the Application binding:

A module can be installed in multiple components. For example, maybe you have a binding in ViewComponent and ViewWithFragmentComponent and do not want to duplicate modules. @InstallIn({ViewComponent.class, ViewWithFragmentComponent.class}) will install a module in both components.

There are three rules to follow when installing a module in multiple components:

Most Android apps will want to pull in different modules and bindings depending on the build variant of the app (e.g. production, debug, testing, etc.).

In Hilt, if your binary’s build target transitively depends on a module, then that module will be installed in the appropriate component for your app. This makes configuration as easy as defining a different build target and pulling different deps into your binary definition.

Because Bazel tends to enourage separation into finer-grained build targets, it is often better for tests to just avoid depending on modules you intend to replace in tests instead of uninstalling them. This is because it reduces the build dependencies of your test which can lead to overall faster build times.

When organizing your BUILD target for a module, you should consider if this module should be replaceable in tests or other configurations of your app. If it should never be replaced, then feel free to include the module with your other code sources.

If it should be replaceable though, you should create a separate target for your module. This target can then be pulled in at the root of your app so that each test root (or other configuration root) can decide whether to use your module or not.

There are two ways to organize your BUILD targets with regards to modules depending on the situation:

It is recommended to choose the first method by default and use the second method only for bindings that need to be replaceable in tests. It is expected, though, that many libraries will use both methods.

In Dagger, modules are usually public visibility because they are referenced by other components or other modules installing them. However, in Hilt, because modules are installed just by being in the transitive dependencies, modules don’t really need to be public for the same reason (technical aside: Hilt will actually generate public wrappers to get around visibility requirements for compilation).

In fact, doing the opposite and restricting visibility of Hilt modules is a best practice because it prevents non-Hilt Dagger components from installing the modules. Installing a Hilt module in a non-Hilt Dagger component would be confusing because it wouldn’t be a component in the @InstallIn annotation. For libraries where you want a module for Hilt and non-Hilt users, it is usually best to have two separate modules for each case. If the code is going to be the same for both, have the Hilt module just be an empty module that uses @Module(includes = ...) to include the non-Hilt module.

**Examples:**

Example 1 (java):
```java
@Module
@InstallIn(SingletonComponent.class) // Installs FooModule in the generate SingletonComponent.
final class FooModule {
  @Provides
  static Bar provideBar() {...}
}
```

Example 2 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent.class) // Installs FooModule in the generate SingletonComponent.
final class FooModule {
  @Provides
  static Bar provideBar() {...}
}
```

Example 3 (kotlin):
```kotlin
@Module
@InstallIn(SingletonComponent::class) // Installs FooModule in the generate SingletonComponent.
internal object FooModule {
  @Provides
  fun provideBar(): Bar {...}
}
```

Example 4 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent::class) // Installs FooModule in the generate SingletonComponent.
internal object FooModule {
  @Provides
  fun provideBar(): Bar {...}
}
```

---

## Modules

**URL:** https://dagger.dev/hilt/modules.html

**Contents:**
- Modules
- Hilt Modules
  - Using @InstallIn
  - Installing a module in multiple components
- App Build variants
- Bazel: Organizing your BUILD files
- Hilt module visibility best practice

Hilt modules are standard Dagger modules that have an additional @InstallIn annotation that determines which Hilt component(s) to install the module into.

When the Hilt components are generated, the modules annotated with @InstallIn will be installed into the corresponding component or subcomponent via @Component#modules or @Subcomponent#modules respectively. Just like in Dagger, installing a module into a component allows that binding to be accessed as a dependency of other bindings in that component or any child component(s) below it in the component hierarchy. They can also be accessed from the corresponding @AndroidEntryPoint classes. Being installed in a component also allows that binding to be scoped to that component.

A module is installed in a Hilt Component by annotating the module with the @InstallIn annotation. These annotations are required on all Dagger modules when using Hilt, but this check may be optionally disabled.

Note: If a module does not have an @InstallIn annotation, the module will not be part of the component and may result in compilation errors.

Specify which Hilt Component to install the module in by passing in the appropriate Component type(s) to the @InstallIn annotation. For example, to install a module so that anything in the application can use it, use SingletonComponent:

Each component comes with a scoping annotation that can be used to memoize a binding to the lifetime of the component. For example, to scope a binding to the SingletonComponent component, use the @Singleton annotation:

In addition, each component has bindings that are available to it by default. (See Hilt Components for a complete list.) For example, the SingletonComponent component provides the Application binding:

A module can be installed in multiple components. For example, maybe you have a binding in ViewComponent and ViewWithFragmentComponent and do not want to duplicate modules. @InstallIn({ViewComponent.class, ViewWithFragmentComponent.class}) will install a module in both components.

There are three rules to follow when installing a module in multiple components:

Most Android apps will want to pull in different modules and bindings depending on the build variant of the app (e.g. production, debug, testing, etc.).

In Hilt, if your binary’s build target transitively depends on a module, then that module will be installed in the appropriate component for your app. This makes configuration as easy as defining a different build target and pulling different deps into your binary definition.

Because Bazel tends to enourage separation into finer-grained build targets, it is often better for tests to just avoid depending on modules you intend to replace in tests instead of uninstalling them. This is because it reduces the build dependencies of your test which can lead to overall faster build times.

When organizing your BUILD target for a module, you should consider if this module should be replaceable in tests or other configurations of your app. If it should never be replaced, then feel free to include the module with your other code sources.

If it should be replaceable though, you should create a separate target for your module. This target can then be pulled in at the root of your app so that each test root (or other configuration root) can decide whether to use your module or not.

There are two ways to organize your BUILD targets with regards to modules depending on the situation:

It is recommended to choose the first method by default and use the second method only for bindings that need to be replaceable in tests. It is expected, though, that many libraries will use both methods.

In Dagger, modules are usually public visibility because they are referenced by other components or other modules installing them. However, in Hilt, because modules are installed just by being in the transitive dependencies, modules don’t really need to be public for the same reason (technical aside: Hilt will actually generate public wrappers to get around visibility requirements for compilation).

In fact, doing the opposite and restricting visibility of Hilt modules is a best practice because it prevents non-Hilt Dagger components from installing the modules. Installing a Hilt module in a non-Hilt Dagger component would be confusing because it wouldn’t be a component in the @InstallIn annotation. For libraries where you want a module for Hilt and non-Hilt users, it is usually best to have two separate modules for each case. If the code is going to be the same for both, have the Hilt module just be an empty module that uses @Module(includes = ...) to include the non-Hilt module.

**Examples:**

Example 1 (java):
```java
@Module
@InstallIn(SingletonComponent.class) // Installs FooModule in the generate SingletonComponent.
final class FooModule {
  @Provides
  static Bar provideBar() {...}
}
```

Example 2 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent.class) // Installs FooModule in the generate SingletonComponent.
final class FooModule {
  @Provides
  static Bar provideBar() {...}
}
```

Example 3 (kotlin):
```kotlin
@Module
@InstallIn(SingletonComponent::class) // Installs FooModule in the generate SingletonComponent.
internal object FooModule {
  @Provides
  fun provideBar(): Bar {...}
}
```

Example 4 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent::class) // Installs FooModule in the generate SingletonComponent.
internal object FooModule {
  @Provides
  fun provideBar(): Bar {...}
}
```

---

## Monolithic components

**URL:** https://dagger.dev/hilt/monolithic

**Contents:**
- Monolithic components
- Overview
- Single binding key space
- Simplicity for configuration
- Less generated code
- fastInit and start up latency

Hilt uses a monolithic component system. This means that a single activity component definition is used to inject all activity classes. Same for Fragments and other Android types. Each activity has a separate instance of the component though, just the class definition is shared. This is as opposed to a polylithic component system where each activity has a separate component definition. A polylithic system is the default mode when using dagger.android’s @ContributesAndroidInjector. This page goes through some of the reasons Hilt was designed using monolithic components along with tradeoffs between the two models.

One of the main benefits of using a monolithic system like in Hilt is that the binding key space is merged. If you are in a fragment injecting a Foo class, it is much easier to find where that Foo binding came from because it cannot differ based on the activity the fragment is attached to. Polylithic components give you more flexibility to define different bindings per activity, but this usually ends up making things more confusing as code bases become larger and harder to trace.

For keeping bindings private to only code that should use them, we recommend using qualifier annotations that are protected through restricted visibility or using an SPI plugin to enforce separation of code.

The single binding key space also makes configuration a lot easier. It reduces the number of places that a module might be installed which makes swapping out bindings for testing easier. It also means you don’t have to worry about propagating modules for features to all the places that use that feature. This can be really useful for features that make use of different scopes. In a polylithic world, a feature using a fragment scoped object and activity scoped object might have to have the user include modules into the fragment and then into all the activities that use that fragment. Oftentimes, this configuration code just adds to boilerplate and breaks encapsulation.

Using a monolithic system also means less generated code. When a common module is used across many subcomponents (as may be the case with a common activity helper class), this means the generated Dagger code has to be repeated for every subcomponent. While it may not initially seem like a lot, it can quickly add up across many activities and be multiplied further by many fragments or views.

Some users may be worried about how this will affect startup latency. If you are using the fastInit compile option, monolithic components should not have a noticeable effect on startup latency. This is the default setting for Hilt gradle users using the plugin and should generally be the Dagger compilation mode used on Android.

---

## Custom Components

**URL:** https://dagger.dev/hilt/custom-components

**Contents:**
- Custom Components
- Is a custom component needed?
  - Custom component limitations
- Adding a custom Hilt component

Hilt has predefined components for Android that are managed for you. However, there may be situations where the standard Hilt components do not match the object lifetimes or needs of a particular feature. In these cases, you may want a custom component. However, before creating a custom component, consider if you really need one as not every place where you can logically add a custom component deserves one.

For example, consider a background task. The task has a reasonably well-defined lifetime that could make sense for a scope. Also, if there were a request object for that task, binding that into Dagger may save some work passing that around as a parameter. However, for most background tasks, a component really isn’t necessary and only adds complexity where simply passing a couple objects on the call stack is simpler and sufficient. Before commiting to adding a custom component, consider the following drawbacks.

Adding a custom component has the following drawbacks:

With those in mind, these are some criteria you should use for deciding if a custom component is needed:

Custom component definitions currently have some limitations:

To create a custom Hilt component, create a class annotated with @DefineComponent. This will be the class used in @InstallIn annotations.

The parent of your component should be defined in the value of the @DefineComponent annotation. Your @DefineComponent class can also be annotated with a scope annotation to allow scoping objects to this component.

A builder interface must also be defined. If this builder is missing, the component will not be generated since there will be no way to construct the component. This interface will be injectable from the parent component and will be the interface for creating new instances of your component. As these are custom components, once instances are built, it will be your job to hold on to or release component instances at the appropriate time.

Builder interfaces are defined by marking an interface with @DefineComponent.Builder. Builders must have a method that returns the @DefineComponent type. They may also have additional methods (like @BindsInstance methods) that a normal Dagger component builder may have.

While the @DefineComponent.Builder class can be nested within the @DefineComponent, it is usually better as a separate class. It may be separated into a different class as long as it is a transitive dependency of the @HiltAndroidApp application or @HiltAndroidTest test. Since the @DefineComponent class is referenced in many places via @InstallIn, it may be better to separate the builder so that dependencies in the builder do not become transitive dependencies of every module installed in the component.

For the same reason of avoiding excessive dependencies, methods are not allowed on the @DefineComponent interface. Instead, Dagger objects should be accessed via entry points.

**Examples:**

Example 1 (java):
```java
@DefineComponent(parent = SingletonComponent.class)
interface MyCustomComponent {}
```

Example 2 (unknown):
```unknown
@DefineComponent(parent = SingletonComponent.class)
interface MyCustomComponent {}
```

Example 3 (kotlin):
```kotlin
@DefineComponent(parent = SingletonComponent::class)
interface MyCustomComponent
```

Example 4 (unknown):
```unknown
@DefineComponent(parent = SingletonComponent::class)
interface MyCustomComponent
```

---

## Monolithic components

**URL:** https://dagger.dev/hilt/monolithic.html

**Contents:**
- Monolithic components
- Overview
- Single binding key space
- Simplicity for configuration
- Less generated code
- fastInit and start up latency

Hilt uses a monolithic component system. This means that a single activity component definition is used to inject all activity classes. Same for Fragments and other Android types. Each activity has a separate instance of the component though, just the class definition is shared. This is as opposed to a polylithic component system where each activity has a separate component definition. A polylithic system is the default mode when using dagger.android’s @ContributesAndroidInjector. This page goes through some of the reasons Hilt was designed using monolithic components along with tradeoffs between the two models.

One of the main benefits of using a monolithic system like in Hilt is that the binding key space is merged. If you are in a fragment injecting a Foo class, it is much easier to find where that Foo binding came from because it cannot differ based on the activity the fragment is attached to. Polylithic components give you more flexibility to define different bindings per activity, but this usually ends up making things more confusing as code bases become larger and harder to trace.

For keeping bindings private to only code that should use them, we recommend using qualifier annotations that are protected through restricted visibility or using an SPI plugin to enforce separation of code.

The single binding key space also makes configuration a lot easier. It reduces the number of places that a module might be installed which makes swapping out bindings for testing easier. It also means you don’t have to worry about propagating modules for features to all the places that use that feature. This can be really useful for features that make use of different scopes. In a polylithic world, a feature using a fragment scoped object and activity scoped object might have to have the user include modules into the fragment and then into all the activities that use that fragment. Oftentimes, this configuration code just adds to boilerplate and breaks encapsulation.

Using a monolithic system also means less generated code. When a common module is used across many subcomponents (as may be the case with a common activity helper class), this means the generated Dagger code has to be repeated for every subcomponent. While it may not initially seem like a lot, it can quickly add up across many activities and be multiplied further by many fragments or views.

Some users may be worried about how this will affect startup latency. If you are using the fastInit compile option, monolithic components should not have a noticeable effect on startup latency. This is the default setting for Hilt gradle users using the plugin and should generally be the Dagger compilation mode used on Android.

---

## Hilt Components

**URL:** https://dagger.dev/hilt/components.html

**Contents:**
- Hilt Components
- Component hierarchy
- Components used for injection
- Component lifetimes
    - Scoped vs unscoped bindings
    - Scoping in modules
    - When to scope?
- Component default bindings

Note: The following page assumes a basic knowledge of Dagger, including components, modules, scopes, and bindings. (For a refresher, see Dagger users guide.)

Unlike traditional Dagger, Hilt users never define or instantiate Dagger components directly. Instead, Hilt offers predefined components that are generated for you. Hilt comes with a built-in set of components (and corresponding scope annotations) that are automatically integrated into the various lifecycles of an Android application. The diagram below shows the standard Hilt component hierarchy. The annotation above each component is the scoping annotation used to scope bindings to the lifetime of that component. The arrow below a component points to any child components. As normal, a binding in a child component can have dependencies on any binding in an ancestor component.

Note: When scoping a binding within an @InstallIn module, the scope on the binding must match the scope of the component. For example, a binding within an @InstallIn(ActivityComponent.class) module can only be scoped with @ActivityScoped.

When using Hilt APIs like @AndroidEntryPoint to inject your Android classes, the standard Hilt components are used as the injectors. The component used as the injector will determine which bindings are visible to that Android class. The components used are shown in the table below:

The lifetime of a component is important because it relates to the lifetime of your bindings in two important ways:

Component lifetimes are generally bounded by the creation and destruction of a corresponding instance of an Android class. The table below lists the scope annotation and bounded lifetime for each component.

By default, all bindings in Dagger are “unscoped”. This means that each time the binding is requested, Dagger will create a new instance of the binding.

However, Dagger also allows a binding to be “scoped” to a particular component (see the scope annotations in the table above). A scoped binding will only be created once per instance of the component it’s scoped to, and all requests for that binding will share the same instance.

Warning: A common misconception is that all fragment instances will share the same instance of a binding scoped with @FragmentScoped. However, this is not true. Each fragment instance gets a new instance of the fragment component, and thus a new instance of all its scoped bindings.

The previous section showed how to scope a binding declared with an @Inject constructor, but a binding declared in a module can also be scoped in a similar way.

Warning: A common misconception is that all bindings declared in a module will be scoped to the component the module is installed in. However, this isn’t true. Only bindings declarations annotated with a scope annotation will be scoped.

Scoping a binding has a cost on both the generated code size and its runtime performance so use scoping sparingly. The general rule for determining if a binding should be scoped is to only scope the binding if it’s required for the correctness of the code. If you think a binding should be scoped for purely performance reasons, first verify that the performance is an issue, and if it is consider using @Reusable instead of a component scope.

Each Hilt component comes with a set of default bindings that can be injected as dependencies into your own custom bindings. Each component listed has the corresponding default bindings as well as any default bindings from an ancestor component.

ActivityRetainedComponent lives across configuration changes, so it is created at the first onCreate and last onDestroy. ↩ ↩2

The Application binding is available using either @ApplicationContext Context or Application. [^3]: @ActivityRetainedSavedState SavedStateHandlemust be used with @OptIn(UnstableApi.class). This binding relies on an experimental implementation to lazily create SavedStateHandle, which should be safe to rely on, but it is still possible that a future release may remove the binding if a bug is uncovered. ↩

**Examples:**

Example 1 (java):
```java
// This binding is "unscoped".
// Each request for this binding will get a new instance.
final class UnscopedBinding {
  @Inject UnscopedBinding() {}
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
final class ScopedBinding {
  @Inject ScopedBinding() {}
}
```

Example 2 (unknown):
```unknown
// This binding is "unscoped".
// Each request for this binding will get a new instance.
final class UnscopedBinding {
  @Inject UnscopedBinding() {}
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
final class ScopedBinding {
  @Inject ScopedBinding() {}
}
```

Example 3 (kotlin):
```kotlin
// This binding is "unscoped".
// Each request for this binding will get a new instance.
class UnscopedBinding @Inject constructor() {
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
class ScopedBinding @Inject constructor() {
}
```

Example 4 (unknown):
```unknown
// This binding is "unscoped".
// Each request for this binding will get a new instance.
class UnscopedBinding @Inject constructor() {
}

// This binding is "scoped".
// Each request from the same component instance for this binding will
// get the same instance. Since this is the fragment component, this means
// each request from the same fragment.
@FragmentScoped
class ScopedBinding @Inject constructor() {
}
```

---

## Subcomponents vs Component dependencies

**URL:** https://dagger.dev/hilt/subcomponents-vs-deps

**Contents:**
- Subcomponents vs Component dependencies
- Overview
- Single binding key space
- Propagating bindings with component dependencies defeats Dagger pruning
- Configuration at the root and build speed

Hilt is based around using Dagger subcomponents as opposed to component dependencies. This page explains some of the reasons why Hilt was designed this way.

Subcomponents propagate all bindings by default. This includes multibindings which can be difficult to propagate via component dependencies. This creates a merged binding key space. This generally makes it easier to understand the Dagger graph because you don’t have to worry about considering if a binding is propagated or not from a parent component to a child component. Also, if bindings are not propagated with component dependencies, it is possible to use two different definitions of the same binding key in different components. This can make it difficult to walk through code when debugging issues as the binding definition will be based on the context of the usage.

One of the downsides of a single binding key space is that it can be extra work to place restrictions on code usage (e.g. if one feature shouldn’t use bindings from another feature). For this we generally recommend using qualifier annotations that are restricted visibility or using an SPI plugin to enforce separation of code. Using a qualifier or an SPI plugin is better than building these concerns into the structure of your Dagger component dependencies graph because often these rules encode policy. Policy decisions like this are often in flux (or need to have exceptions allowed) and having to restructure a Dagger component dependencies graph based on those changes can be costly.

Since Dagger can see the entry points to the graph, it can figure out which bindings are unused and not generate code for those bindings. This optimization goes through subcomponents, but it is defeated by component dependencies because propagating bindings through component dependencies adds entry point methods. So even if entry point methods are only used by other Dagger components and across the components the binding is unused, Dagger will be forced to still generate that dead code to adhere to its contract.

One of the main advantages of component dependencies is building Dagger code separately and in parallel. This can be done because of the lack of implicit sharing that make components black boxes with respect to each other. However, Hilt is already based on the idea of central configuration based on build dependencies. Since Hilt has to aggregate modules, all components would be generated at the same time anyway so we wouldn’t be able to take advantage of building in parallel.

Instead, to address build speed, Hilt recommends making smaller test apps for individual feature development. Without Hilt, this would have been difficult to do because of all of the repeated Dagger boilerplate for the small test app. However, with Hilt generating all of the Dagger portion based on build dependencies, putting together a small test app should be much easier.

---
