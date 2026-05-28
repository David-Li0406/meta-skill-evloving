# Hilt - Testing

**Pages:** 8

---

## Robolectric testing

**URL:** https://dagger.dev/hilt/robolectric-testing.html

**Contents:**
- Robolectric testing
- Setting the test application
  - Using @Config
  - Using robolectric.properties

Warning: See here for limitations when running Robolectric tests via Android Studio when using the Hilt Gradle plugin.

Hilt’s testing APIs are built to be agnostic of the particular testing environment; however, the instructions for setting up the application class in your test will depend on whether you are using Robolectric or Android instrumentation tests.

For Robolectric tests, the application can be set either locally using @Config or globally using robolectric.properties. For Hilt tests, the application must either be HiltTestApplication or one of Hilt’s custom test applications.

Note: This setup is not particular to Hilt. See the official Robolectric documentation for more details.

The Hilt application class can be set locally using @Config. To set the application, just annotate the test (or test method) with @Config and set the value of the annotation to the desired application class.

The Hilt application class can be set globally using the robolectric.properties file. To set the application, just create the robolectric.properties file in the appropriate resources package, and set the Hilt test application class.

This approach can be useful when a test needs to run in both Robolectric and Android instrumentation environments, since the @Config annotation cannot be used with Android instrumentation tests.

**Examples:**

Example 1 (java):
```java
@HiltAndroidTest
@Config(application = HiltTestApplication.class)
public class FooTest {...}
```

Example 2 (csharp):
```csharp
@HiltAndroidTest
@Config(application = HiltTestApplication.class)
public class FooTest {...}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidTest
@Config(application = HiltTestApplication::class)
class FooTest {...}
```

Example 4 (unknown):
```unknown
@HiltAndroidTest
@Config(application = HiltTestApplication::class)
class FooTest {...}
```

---

## Testing

**URL:** https://dagger.dev/hilt/testing.html

**Contents:**
- Testing
- Introduction
- Test Setup
- Accessing bindings
  - Accessing SingletonComponent bindings
  - Accessing ActivityComponent bindings
  - Accessing FragmentComponent bindings
- Replacing bindings
  - @TestInstallIn
  - @UninstallModules

Hilt makes testing easier by bringing the power of dependency injection to your Android tests. Hilt allows your tests to easily access Dagger bindings, provide new bindings, or even replace bindings. Each test gets its own set of Hilt components so that you can easily customize bindings at a per-test level.

Many of the testing APIs and functionality described in this documentation are based upon an unstated philosophy of what makes a good test. For more details on Hilt’s testing philosophy see here.

Note: For Gradle users, make sure to first add the Hilt test build dependencies as described in the Gradle setup guide.

To use Hilt in a test:

Note that setting the application class for a test (step 3 above) is dependent on whether the test is a Robolectric or instrumentation test. For a more detailed guide on how to set the test application for a particular test environment, see Robolectric testing or Instrumentation testing. The remainder of this doc applies to both Robolectric and instrumentation tests.

If your test requires a custom application class, see the section on custom test application.

If your test requires multiple test rules, see the section on Hilt rule order to determine the proper placement of the Hilt rule.

A test often needs to request bindings from its Hilt components. This section describes how to request bindings from each of the different components.

An SingletonComponent binding can be injected directly into a test using an @Inject annotated field. Injection doesn’t occur until calling HiltAndroidRule#inject().

Requesting an ActivityComponent binding requires an instance of a Hilt Activity. One way to do this is to define a nested activity within your test that contains an @Inject field for the binding you need. Then create an instance of your test activity to get the binding.

Alternatively, if you already have a Hilt activity instance available in your test, you can get any ActivityComponent binding using an EntryPoint.

A FragmentComponent binding can be accessed in a similar way to an ActivityComponent binding. The main difference is that accessing a FragmentComponent binding requires both an instance of a Hilt Activity and a Hilt Fragment.

Alternatively, if you already have a Hilt fragment instance available in your test, you can get any FragmentComponent binding using an EntryPoint.

Warning:Hilt does not currently support FragmentScenario because there is no way to specify an activity class, and Hilt requires a Hilt fragment to be contained in a Hilt activity. One workaround for this is to launch a Hilt activity and then attach your fragment.

It’s often useful for tests to be able to replace a production binding with a fake or mock binding to make tests more hermetic or easier to control in test. The next sections describe some ways to accomplish this in Hilt.

A Dagger module annotated with @TestInstallIn allows users to replace an existing @InstallIn module for all tests in a given source set. For example, suppose we want to replace ProdDataServiceModule with FakeDataServiceModule. We can accomplish this by annotating FakeDataServiceModule with @TestInstallIn, as shown below:

A @TestInstallIn module can be included in the same source set as your test sources, as shown below:

However, if a particular @TestInstallIn module is needed in multiple Gradle modules, we recommend putting it in its own Gradle module (usually the same one as the fake), as shown below:

Putting the @TestInstallIn in the same Gradle module as the fake has a number of benefits. First, it ensures that all clients that depend on the fake properly replace the production module with the test module. It also avoids duplicating FakeDataServiceModule for every Gradle module that needs it.

Note that @TestInstallIn applies to all tests in a given source set. For cases where an individual test needs to replace a binding that is specific to the given test, the test can either be moved into its own source set, or it can use Hilt testing features such as @UninstallModules, @BindValue, and nested @InstallIn modules to replace bindings specific to that test. These features will be described in more detail in the following sections.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

A test annotated with @UninstallModules can uninstall production @InstallIn modules for that particular test (unlike @TestInstallIn, it has no effect on other tests). Once a module is uninstalled, the test can install new, test-specific bindings for that particular test.

There are two ways to install a new binding for a particular test:

These two approaches are described in more detail in the next sections.

Note: @UninstallModules can only uninstall @InstallIn modules, not @TestInstallIn modules. If a @TestInstallIn module needs to be uninstalled the module must be split into two separate modules: a @TestInstallIn module that replaces the production module with no bindings (i.e. only removes the production module), and a @InstallIn module that provides the standard fake so that @UninstallModules can uninstall the provided fake.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

Normally, @InstallIn modules are installed in the Hilt components of every test. However, if a binding needs to be installed only in a particular test, that can be accomplished by nesting the @InstallIn module within the test class.

Thus, if there is another test that needs to provision the same binding with a different implementation, it can do that without a duplicate binding conflict.

In addition to static nested @InstallIn modules, Hilt also supports inner (non-static) @InstallIn modules within tests. Using an inner module allows the @Provides methods to reference members of the test instance.

Note: Hilt does not support @InstallIn modules with constructor parameters.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

For simple bindings, especially those that need to also be accessed in the test methods, Hilt provides a convenience annotation to avoid the boilerplate of creating a module and method normally required to provision a binding.

@BindValue is an annotation that allows you to easily bind fields in your test into the Dagger graph. To use it, just annotate a field with @BindValue and it will be bound to the declared field type with any qualifiers that are present on the field.

Note that @BindValue does not support the use of scope annotations since the binding’s scope is tied to the field and controlled by the test. The field’s value is queried whenever it is requested, so it can be mutated as necessary for your test. If you want the binding to be effectively singleton, just ensure that the field is only set once per test case, e.g. by setting the field’s value from either the field’s initializer or from within an @Before method of the test.

Similarly, Hilt also has a convenience annotation for multibindings with @BindValueIntoSet, @BindElementsIntoSet, and @BindValueIntoMap to support @IntoSet, @ElementsIntoSet, and @IntoMap respectively. (Note that @BindValueIntoMap requires the field to also be annotated with a map key annotation.)

Warning:Be careful when using @BindValue or non-static inner modules with ActivityScenarioRule. ActivityScenarioRule creates the activity before calling the @Before method, so if an @BindValue field is initialized in @Before (or later), then it’s possible for the Activity to inject the binding in its unitialized state. To avoid this, try initializing the @BindValue field in the field’s initializer.

Every Hilt test must use a Hilt test application as the Android application class. Hilt comes with a default test application, HiltTestApplication, which extends MultiDexApplication; however, there are cases where a test may need to use a different base class.

If your test requires a custom base class, @CustomTestApplication can be used to generate a Hilt test application that extends the given base class.

To use @CustomTestApplication, just annotate a class or interface with @CustomTestApplication and specify the base class in the annotation value:

In the above example, Hilt will generate an application named MyCustom_Application that extends MyBaseApplication. In general, the name of the generated application will be the name of the annotated class appended with _Application. If the annotated class is a nested class, the name will also include the name of the outer class separated by an underscore. Note that the class that is annotated is irrelevant, other than for the name of the generated application.

As a best practice, avoid using @CustomTestApplication and instead use HiltTestApplication in your tests. In general, having your Activity, Fragment, etc. be independent of the parent they are contained in makes it easier to compose and reuse it in the future.

However, if you must use a custom base application, there are some subtle differences with the production lifecycle to be aware of.

One difference is that instrumentation tests use the same application instance for every test and test case. Thus, it’s easy to accidentally leak state across test cases when using a custom test application. Instead, it’s better to avoid storing any test or test case dependendent state in your application.

Another difference is that the Hilt component in a test application is not created in super#onCreate. This restriction is mainly due to fact that some of Hilt’s features (e.g. @BindValue) rely on the test instance, which is not available in tests until after Application#onCreate is called. Thus, unlike production applications, custom base applications must avoid calling into the component during Application#onCreate. This includes injecting members into the application. To prevent this issue, Hilt doesn’t allow injection in the base application.

If your test uses multiple test rules, make sure that the HiltAndroidRule runs before any other test rules that require access to the Hilt component. For example ActivityScenarioRule calls Activity#onCreate, which (for Hilt activities) requires the Hilt component to perform injection. Thus, the ActivityScenarioRule should run after the HiltAndroidRule to ensure that the component has been properly initialized.

Note: If you’re using JUnit < 4.13 use RuleChain to specify the order instead.

**Examples:**

Example 1 (java):
```java
@HiltAndroidTest
public class FooTest {
  @Rule public HiltAndroidRule hiltRule = new HiltAndroidRule(this);
  ...
}
```

Example 2 (csharp):
```csharp
@HiltAndroidTest
public class FooTest {
  @Rule public HiltAndroidRule hiltRule = new HiltAndroidRule(this);
  ...
}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidTest
class FooTest {
  @get:Rule val hiltRule = HiltAndroidRule(this)
  ...
}
```

Example 4 (unknown):
```unknown
@HiltAndroidTest
class FooTest {
  @get:Rule val hiltRule = HiltAndroidRule(this)
  ...
}
```

---

## Hilt Testing Philosophy

**URL:** https://dagger.dev/hilt/testing-philosophy.html

**Contents:**
- Hilt Testing Philosophy
- Overview
- What to test
- Using real dependencies
- Hilt, DI, and testing
- Downsides of manual instantiation
  - Direct instantiation encourages mocks
  - Direct instantiation encourages incorrect scoping
  - Direct instantiation encodes implementation details in the test
- Summary

This page aims to explain the testing practices that Hilt is built upon. A lot of the APIs and functionality in Hilt (and certain lack of functionality as well) were created on an unstated philosophy of what makes a good test. The notion of a good test is not universally agreed upon though, so this document aims to clarify the Hilt team’s testing philosophy.

Hilt encourages testing as much as possible from an outside user’s perspective. An outside user’s perspective can mean many things. It could mean the actual users of your app or service, but it can also be more scoped down to the users of your API or class.

The key part is that tests shouldn’t encode implementation details. Relying on implementation details, like checking that an internal method has been called, causes the test to be brittle. If a refactoring changes the name of an internal method, a good test should not have to be updated. The only changes that should break existing tests are those that are changing your user-visible behavior.

The Hilt testing philosophy doesn’t prescribe strict rules such as every class must have its own test. In fact, usually such a rule would violate the above principle of testing from the user’s perspective. Tests should be only as small as necessary to make them convenient to write and run (e.g. small enough to be fast or not resource intensive). All else being equal, tests should, in this order, prefer to:

However, there are trade offs. Using real dependencies/real DI in tests may be prohibitively difficult for one or both of the following reasons:

Hilt was built to solve the first issue of set up (more on that below). Performance can be an issue but is often not a problem for most dependencies. This likely is only an issue when using dependencies with significant I/O. So, if a test can be written more conveniently and robustly by using more real dependencies without significantly degrading performance, it should be written using those dependencies. For those classes that do come with large negative effects in tests, Hilt provides a means to switch out the bindings.

Using more real dependencies has significant advantages:

If the real dependency is not possible to use though, a standard fake provided by the library is usually the next best option. A standardized fake is better than a mock because it is more likely to be in sync with the production code if it is maintained by the library authors and thus provides more robust coverage. For these reasons, mocks are typically a last resort.

With those foundations explained, we now get into the specifics of Hilt, DI, and testing. In line with the philosophy of using real objects, Hilt’s answer is to use dependency injection / Dagger in tests. This is more realistic because objects are created as they would be in production code. It means that tests are not any more brittle than production code would be and it makes it easier to use real objects. In fact, for types that have @Inject constructors, it is actually easier and less code to follow this advice and use the real code than it is to configure and bind a mock.

Unfortunately, this kind of testing without Hilt has traditionally been difficult in practice due to the boilerplate and extra work to set up Dagger in the tests. However, Hilt generates the boilerplate for you and has a clear story for setting up different configurations of bindings for tests when you do need a fake or a mock. With Hilt, this issue should no longer be a deterrent to writing tests with Dagger and therefore easily using real dependencies.

One of the common alternatives to using Dagger in unit tests is to instantiate an object directly by manually calling its constructor (or @Provides method). This, unfortunately, ends up having significant drawbacks, though it is understandable advice given the difficulty of using Dagger in tests without Hilt.

For example, let’s say we have a Foo class that we want to test:

The test directly instantiates Foo by calling its constructor. At first glance, this seems like a very simple and reasonable thing to do; however, things start to unravel as you try to supply Foo’s dependencies. In this case, Foo depends on Bar. Bar may have other dependencies of its own. As we’ll see in the following sections, supplying all of these dependencies manually can lead brittle tests.

From the previously discussed testing philosophy, we should prefer to get a real Bar class. However, how should we do that? This actually is just a recursion of getting a real Foo class to test: you would have to instantiate it yourself and if Bar has dependencies of its own, then that would require similarly instantiating those. In order to not go too deep you would likely need to start using a fake or a mock, not because of the effects on speed or performance of the test, but simply to avoid too much brittle boilerplate that causes maintenance problems. This is not a good reason to use a fake or a mock, and yet you are forced to do so anyway.

An alternative, as discussed above, is to use a standard fake, which may help cut dependencies and reduce the maintenance burden of direct instantiation. However, even that is not always that simple. Many times a good fake will similarly have dependencies it needs. For example, a FakeBar may end up needing to take in a FakeClock if the real Bar took a Clock. This is because a FakeClock is often a coordination point between different classes. (Imagine if Foo had another dependency Baz that also used a clock, you would want the FakeBaz to use the same FakeClock instance so things are coordinated when time is advanced). Managing these dependencies can quickly get out of hand.

This usually leads test authors to mocks. The mock solves the issue of tediously following these dependency chains, but has significant drawbacks in that it can easily get out of date silently and make the test useless in its overall goal of finding real bugs. Because no one checks the mock behavior besides the test author, this usually means that after enough time, there is a decent likelihood that the test is no longer testing a useful scenario.

By directly instantiating a dependency, you are assuming responsibility for correctly scoping that dependency. It is easy to accidentally create multiple instances of scoped bindings, or to provide the same instance of an unscoped binding multiple times.

For example, a FakeClock may contain global state that maintains the current time and allows advancing this time manually in tests. Because of this, it is marked as @Singleton so that the code under test and the test itself reference the same instance. But if an additional instance is directly instantiated by the test, multiple instances would exist. This would lead to code under test observing skewed timestamps, or the test advancing the current time to no effect.

Additionally, manually writing Provider and Lazy constructor parameters for scoped types is error-prone. You need to know whether the dependency is scoped, and store an instance of the object at the right level. For example, you would need to associate any @ActivityScoped bindings with the Activity under test, and recreate the dependency if the Activity undergoes a configuration change. To accurately reflect the real Dagger behavior, all of this would need to be made thread-safe.

Finally, if the scope of a dependency is later changed, the tests using that dependency will not actually reflect that change without manual updates. This prevents tests from detecting unintended changes due to a change in scope.

Direct instantiation also breaks the philosophy of not encoding implementation details in a test because the constructor call encodes details of its dependencies. If Bar were an @Inject constructor type, there is no reason a user of Foo needs to know about the existence of the Bar class as it could easily be an implementation detail from refactoring logic in Foo into another class private to the library.

To illustrate this point, consider if Foo had two dependencies like Foo(Bar, Baz). In Dagger, switching the order of these parameters on the @Inject constructor is a no-op. Yet if we were to test Foo via direct instantiation, we’d still have to update the test. Similarly, adding a usage of a new @Inject class or an optional binding would similarly be an invisible change for production users of the class, yet the test would still need to be updated.

Hilt was designed to fix the downside of using Dagger in tests in order to allow easy testing with real dependencies. Tests written using Hilt will have a better overall experience if they follow these principles.

**Examples:**

Example 1 (java):
```java
final class Foo {
  @Inject Foo(Bar bar) {...}
}
```

Example 2 (unknown):
```unknown
final class Foo {
  @Inject Foo(Bar bar) {...}
}
```

Example 3 (kotlin):
```kotlin
class Foo @Inject constructor(bar: Bar) {
}
```

Example 4 (unknown):
```unknown
class Foo @Inject constructor(bar: Bar) {
}
```

---

## Robolectric testing

**URL:** https://dagger.dev/hilt/robolectric-testing

**Contents:**
- Robolectric testing
- Setting the test application
  - Using @Config
  - Using robolectric.properties

Warning: See here for limitations when running Robolectric tests via Android Studio when using the Hilt Gradle plugin.

Hilt’s testing APIs are built to be agnostic of the particular testing environment; however, the instructions for setting up the application class in your test will depend on whether you are using Robolectric or Android instrumentation tests.

For Robolectric tests, the application can be set either locally using @Config or globally using robolectric.properties. For Hilt tests, the application must either be HiltTestApplication or one of Hilt’s custom test applications.

Note: This setup is not particular to Hilt. See the official Robolectric documentation for more details.

The Hilt application class can be set locally using @Config. To set the application, just annotate the test (or test method) with @Config and set the value of the annotation to the desired application class.

The Hilt application class can be set globally using the robolectric.properties file. To set the application, just create the robolectric.properties file in the appropriate resources package, and set the Hilt test application class.

This approach can be useful when a test needs to run in both Robolectric and Android instrumentation environments, since the @Config annotation cannot be used with Android instrumentation tests.

**Examples:**

Example 1 (java):
```java
@HiltAndroidTest
@Config(application = HiltTestApplication.class)
public class FooTest {...}
```

Example 2 (csharp):
```csharp
@HiltAndroidTest
@Config(application = HiltTestApplication.class)
public class FooTest {...}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidTest
@Config(application = HiltTestApplication::class)
class FooTest {...}
```

Example 4 (unknown):
```unknown
@HiltAndroidTest
@Config(application = HiltTestApplication::class)
class FooTest {...}
```

---

## Hilt Testing Philosophy

**URL:** https://dagger.dev/hilt/testing-philosophy

**Contents:**
- Hilt Testing Philosophy
- Overview
- What to test
- Using real dependencies
- Hilt, DI, and testing
- Downsides of manual instantiation
  - Direct instantiation encourages mocks
  - Direct instantiation encourages incorrect scoping
  - Direct instantiation encodes implementation details in the test
- Summary

This page aims to explain the testing practices that Hilt is built upon. A lot of the APIs and functionality in Hilt (and certain lack of functionality as well) were created on an unstated philosophy of what makes a good test. The notion of a good test is not universally agreed upon though, so this document aims to clarify the Hilt team’s testing philosophy.

Hilt encourages testing as much as possible from an outside user’s perspective. An outside user’s perspective can mean many things. It could mean the actual users of your app or service, but it can also be more scoped down to the users of your API or class.

The key part is that tests shouldn’t encode implementation details. Relying on implementation details, like checking that an internal method has been called, causes the test to be brittle. If a refactoring changes the name of an internal method, a good test should not have to be updated. The only changes that should break existing tests are those that are changing your user-visible behavior.

The Hilt testing philosophy doesn’t prescribe strict rules such as every class must have its own test. In fact, usually such a rule would violate the above principle of testing from the user’s perspective. Tests should be only as small as necessary to make them convenient to write and run (e.g. small enough to be fast or not resource intensive). All else being equal, tests should, in this order, prefer to:

However, there are trade offs. Using real dependencies/real DI in tests may be prohibitively difficult for one or both of the following reasons:

Hilt was built to solve the first issue of set up (more on that below). Performance can be an issue but is often not a problem for most dependencies. This likely is only an issue when using dependencies with significant I/O. So, if a test can be written more conveniently and robustly by using more real dependencies without significantly degrading performance, it should be written using those dependencies. For those classes that do come with large negative effects in tests, Hilt provides a means to switch out the bindings.

Using more real dependencies has significant advantages:

If the real dependency is not possible to use though, a standard fake provided by the library is usually the next best option. A standardized fake is better than a mock because it is more likely to be in sync with the production code if it is maintained by the library authors and thus provides more robust coverage. For these reasons, mocks are typically a last resort.

With those foundations explained, we now get into the specifics of Hilt, DI, and testing. In line with the philosophy of using real objects, Hilt’s answer is to use dependency injection / Dagger in tests. This is more realistic because objects are created as they would be in production code. It means that tests are not any more brittle than production code would be and it makes it easier to use real objects. In fact, for types that have @Inject constructors, it is actually easier and less code to follow this advice and use the real code than it is to configure and bind a mock.

Unfortunately, this kind of testing without Hilt has traditionally been difficult in practice due to the boilerplate and extra work to set up Dagger in the tests. However, Hilt generates the boilerplate for you and has a clear story for setting up different configurations of bindings for tests when you do need a fake or a mock. With Hilt, this issue should no longer be a deterrent to writing tests with Dagger and therefore easily using real dependencies.

One of the common alternatives to using Dagger in unit tests is to instantiate an object directly by manually calling its constructor (or @Provides method). This, unfortunately, ends up having significant drawbacks, though it is understandable advice given the difficulty of using Dagger in tests without Hilt.

For example, let’s say we have a Foo class that we want to test:

The test directly instantiates Foo by calling its constructor. At first glance, this seems like a very simple and reasonable thing to do; however, things start to unravel as you try to supply Foo’s dependencies. In this case, Foo depends on Bar. Bar may have other dependencies of its own. As we’ll see in the following sections, supplying all of these dependencies manually can lead brittle tests.

From the previously discussed testing philosophy, we should prefer to get a real Bar class. However, how should we do that? This actually is just a recursion of getting a real Foo class to test: you would have to instantiate it yourself and if Bar has dependencies of its own, then that would require similarly instantiating those. In order to not go too deep you would likely need to start using a fake or a mock, not because of the effects on speed or performance of the test, but simply to avoid too much brittle boilerplate that causes maintenance problems. This is not a good reason to use a fake or a mock, and yet you are forced to do so anyway.

An alternative, as discussed above, is to use a standard fake, which may help cut dependencies and reduce the maintenance burden of direct instantiation. However, even that is not always that simple. Many times a good fake will similarly have dependencies it needs. For example, a FakeBar may end up needing to take in a FakeClock if the real Bar took a Clock. This is because a FakeClock is often a coordination point between different classes. (Imagine if Foo had another dependency Baz that also used a clock, you would want the FakeBaz to use the same FakeClock instance so things are coordinated when time is advanced). Managing these dependencies can quickly get out of hand.

This usually leads test authors to mocks. The mock solves the issue of tediously following these dependency chains, but has significant drawbacks in that it can easily get out of date silently and make the test useless in its overall goal of finding real bugs. Because no one checks the mock behavior besides the test author, this usually means that after enough time, there is a decent likelihood that the test is no longer testing a useful scenario.

By directly instantiating a dependency, you are assuming responsibility for correctly scoping that dependency. It is easy to accidentally create multiple instances of scoped bindings, or to provide the same instance of an unscoped binding multiple times.

For example, a FakeClock may contain global state that maintains the current time and allows advancing this time manually in tests. Because of this, it is marked as @Singleton so that the code under test and the test itself reference the same instance. But if an additional instance is directly instantiated by the test, multiple instances would exist. This would lead to code under test observing skewed timestamps, or the test advancing the current time to no effect.

Additionally, manually writing Provider and Lazy constructor parameters for scoped types is error-prone. You need to know whether the dependency is scoped, and store an instance of the object at the right level. For example, you would need to associate any @ActivityScoped bindings with the Activity under test, and recreate the dependency if the Activity undergoes a configuration change. To accurately reflect the real Dagger behavior, all of this would need to be made thread-safe.

Finally, if the scope of a dependency is later changed, the tests using that dependency will not actually reflect that change without manual updates. This prevents tests from detecting unintended changes due to a change in scope.

Direct instantiation also breaks the philosophy of not encoding implementation details in a test because the constructor call encodes details of its dependencies. If Bar were an @Inject constructor type, there is no reason a user of Foo needs to know about the existence of the Bar class as it could easily be an implementation detail from refactoring logic in Foo into another class private to the library.

To illustrate this point, consider if Foo had two dependencies like Foo(Bar, Baz). In Dagger, switching the order of these parameters on the @Inject constructor is a no-op. Yet if we were to test Foo via direct instantiation, we’d still have to update the test. Similarly, adding a usage of a new @Inject class or an optional binding would similarly be an invisible change for production users of the class, yet the test would still need to be updated.

Hilt was designed to fix the downside of using Dagger in tests in order to allow easy testing with real dependencies. Tests written using Hilt will have a better overall experience if they follow these principles.

**Examples:**

Example 1 (java):
```java
final class Foo {
  @Inject Foo(Bar bar) {...}
}
```

Example 2 (unknown):
```unknown
final class Foo {
  @Inject Foo(Bar bar) {...}
}
```

Example 3 (kotlin):
```kotlin
class Foo @Inject constructor(bar: Bar) {
}
```

Example 4 (unknown):
```unknown
class Foo @Inject constructor(bar: Bar) {
}
```

---

## Testing

**URL:** https://dagger.dev/hilt/testing

**Contents:**
- Testing
- Introduction
- Test Setup
- Accessing bindings
  - Accessing SingletonComponent bindings
  - Accessing ActivityComponent bindings
  - Accessing FragmentComponent bindings
- Replacing bindings
  - @TestInstallIn
  - @UninstallModules

Hilt makes testing easier by bringing the power of dependency injection to your Android tests. Hilt allows your tests to easily access Dagger bindings, provide new bindings, or even replace bindings. Each test gets its own set of Hilt components so that you can easily customize bindings at a per-test level.

Many of the testing APIs and functionality described in this documentation are based upon an unstated philosophy of what makes a good test. For more details on Hilt’s testing philosophy see here.

Note: For Gradle users, make sure to first add the Hilt test build dependencies as described in the Gradle setup guide.

To use Hilt in a test:

Note that setting the application class for a test (step 3 above) is dependent on whether the test is a Robolectric or instrumentation test. For a more detailed guide on how to set the test application for a particular test environment, see Robolectric testing or Instrumentation testing. The remainder of this doc applies to both Robolectric and instrumentation tests.

If your test requires a custom application class, see the section on custom test application.

If your test requires multiple test rules, see the section on Hilt rule order to determine the proper placement of the Hilt rule.

A test often needs to request bindings from its Hilt components. This section describes how to request bindings from each of the different components.

An SingletonComponent binding can be injected directly into a test using an @Inject annotated field. Injection doesn’t occur until calling HiltAndroidRule#inject().

Requesting an ActivityComponent binding requires an instance of a Hilt Activity. One way to do this is to define a nested activity within your test that contains an @Inject field for the binding you need. Then create an instance of your test activity to get the binding.

Alternatively, if you already have a Hilt activity instance available in your test, you can get any ActivityComponent binding using an EntryPoint.

A FragmentComponent binding can be accessed in a similar way to an ActivityComponent binding. The main difference is that accessing a FragmentComponent binding requires both an instance of a Hilt Activity and a Hilt Fragment.

Alternatively, if you already have a Hilt fragment instance available in your test, you can get any FragmentComponent binding using an EntryPoint.

Warning:Hilt does not currently support FragmentScenario because there is no way to specify an activity class, and Hilt requires a Hilt fragment to be contained in a Hilt activity. One workaround for this is to launch a Hilt activity and then attach your fragment.

It’s often useful for tests to be able to replace a production binding with a fake or mock binding to make tests more hermetic or easier to control in test. The next sections describe some ways to accomplish this in Hilt.

A Dagger module annotated with @TestInstallIn allows users to replace an existing @InstallIn module for all tests in a given source set. For example, suppose we want to replace ProdDataServiceModule with FakeDataServiceModule. We can accomplish this by annotating FakeDataServiceModule with @TestInstallIn, as shown below:

A @TestInstallIn module can be included in the same source set as your test sources, as shown below:

However, if a particular @TestInstallIn module is needed in multiple Gradle modules, we recommend putting it in its own Gradle module (usually the same one as the fake), as shown below:

Putting the @TestInstallIn in the same Gradle module as the fake has a number of benefits. First, it ensures that all clients that depend on the fake properly replace the production module with the test module. It also avoids duplicating FakeDataServiceModule for every Gradle module that needs it.

Note that @TestInstallIn applies to all tests in a given source set. For cases where an individual test needs to replace a binding that is specific to the given test, the test can either be moved into its own source set, or it can use Hilt testing features such as @UninstallModules, @BindValue, and nested @InstallIn modules to replace bindings specific to that test. These features will be described in more detail in the following sections.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

A test annotated with @UninstallModules can uninstall production @InstallIn modules for that particular test (unlike @TestInstallIn, it has no effect on other tests). Once a module is uninstalled, the test can install new, test-specific bindings for that particular test.

There are two ways to install a new binding for a particular test:

These two approaches are described in more detail in the next sections.

Note: @UninstallModules can only uninstall @InstallIn modules, not @TestInstallIn modules. If a @TestInstallIn module needs to be uninstalled the module must be split into two separate modules: a @TestInstallIn module that replaces the production module with no bindings (i.e. only removes the production module), and a @InstallIn module that provides the standard fake so that @UninstallModules can uninstall the provided fake.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

Normally, @InstallIn modules are installed in the Hilt components of every test. However, if a binding needs to be installed only in a particular test, that can be accomplished by nesting the @InstallIn module within the test class.

Thus, if there is another test that needs to provision the same binding with a different implementation, it can do that without a duplicate binding conflict.

In addition to static nested @InstallIn modules, Hilt also supports inner (non-static) @InstallIn modules within tests. Using an inner module allows the @Provides methods to reference members of the test instance.

Note: Hilt does not support @InstallIn modules with constructor parameters.

Warning:Test classes that use @UninstallModules, @BindValue, or nested @InstallIn modules result in a custom component being generated for that test. While this may be fine in most cases, it does have an impact on build speed. The recommended approach is to use @TestInstallIn modules instead.

For simple bindings, especially those that need to also be accessed in the test methods, Hilt provides a convenience annotation to avoid the boilerplate of creating a module and method normally required to provision a binding.

@BindValue is an annotation that allows you to easily bind fields in your test into the Dagger graph. To use it, just annotate a field with @BindValue and it will be bound to the declared field type with any qualifiers that are present on the field.

Note that @BindValue does not support the use of scope annotations since the binding’s scope is tied to the field and controlled by the test. The field’s value is queried whenever it is requested, so it can be mutated as necessary for your test. If you want the binding to be effectively singleton, just ensure that the field is only set once per test case, e.g. by setting the field’s value from either the field’s initializer or from within an @Before method of the test.

Similarly, Hilt also has a convenience annotation for multibindings with @BindValueIntoSet, @BindElementsIntoSet, and @BindValueIntoMap to support @IntoSet, @ElementsIntoSet, and @IntoMap respectively. (Note that @BindValueIntoMap requires the field to also be annotated with a map key annotation.)

Warning:Be careful when using @BindValue or non-static inner modules with ActivityScenarioRule. ActivityScenarioRule creates the activity before calling the @Before method, so if an @BindValue field is initialized in @Before (or later), then it’s possible for the Activity to inject the binding in its unitialized state. To avoid this, try initializing the @BindValue field in the field’s initializer.

Every Hilt test must use a Hilt test application as the Android application class. Hilt comes with a default test application, HiltTestApplication, which extends MultiDexApplication; however, there are cases where a test may need to use a different base class.

If your test requires a custom base class, @CustomTestApplication can be used to generate a Hilt test application that extends the given base class.

To use @CustomTestApplication, just annotate a class or interface with @CustomTestApplication and specify the base class in the annotation value:

In the above example, Hilt will generate an application named MyCustom_Application that extends MyBaseApplication. In general, the name of the generated application will be the name of the annotated class appended with _Application. If the annotated class is a nested class, the name will also include the name of the outer class separated by an underscore. Note that the class that is annotated is irrelevant, other than for the name of the generated application.

As a best practice, avoid using @CustomTestApplication and instead use HiltTestApplication in your tests. In general, having your Activity, Fragment, etc. be independent of the parent they are contained in makes it easier to compose and reuse it in the future.

However, if you must use a custom base application, there are some subtle differences with the production lifecycle to be aware of.

One difference is that instrumentation tests use the same application instance for every test and test case. Thus, it’s easy to accidentally leak state across test cases when using a custom test application. Instead, it’s better to avoid storing any test or test case dependendent state in your application.

Another difference is that the Hilt component in a test application is not created in super#onCreate. This restriction is mainly due to fact that some of Hilt’s features (e.g. @BindValue) rely on the test instance, which is not available in tests until after Application#onCreate is called. Thus, unlike production applications, custom base applications must avoid calling into the component during Application#onCreate. This includes injecting members into the application. To prevent this issue, Hilt doesn’t allow injection in the base application.

If your test uses multiple test rules, make sure that the HiltAndroidRule runs before any other test rules that require access to the Hilt component. For example ActivityScenarioRule calls Activity#onCreate, which (for Hilt activities) requires the Hilt component to perform injection. Thus, the ActivityScenarioRule should run after the HiltAndroidRule to ensure that the component has been properly initialized.

Note: If you’re using JUnit < 4.13 use RuleChain to specify the order instead.

**Examples:**

Example 1 (java):
```java
@HiltAndroidTest
public class FooTest {
  @Rule public HiltAndroidRule hiltRule = new HiltAndroidRule(this);
  ...
}
```

Example 2 (csharp):
```csharp
@HiltAndroidTest
public class FooTest {
  @Rule public HiltAndroidRule hiltRule = new HiltAndroidRule(this);
  ...
}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidTest
class FooTest {
  @get:Rule val hiltRule = HiltAndroidRule(this)
  ...
}
```

Example 4 (unknown):
```unknown
@HiltAndroidTest
class FooTest {
  @get:Rule val hiltRule = HiltAndroidRule(this)
  ...
}
```

---

## Instrumentation testing

**URL:** https://dagger.dev/hilt/instrumentation-testing.html

**Contents:**
- Instrumentation testing
- Setting the test application

Hilt’s testing APIs are built to be agnostic of the particular testing environment; however, the instructions for setting up the application class in your test will depend on whether you are using Robolectric or Android instrumentation tests.

For Android instrumentation tests, the application can be set using a custom test runner that extends AndroidJUnitRunner. To set the application using the runner, just override the newApplication method and pass in the application class name. For Hilt tests, the application must either be HiltTestApplication or one of Hilt’s custom test applications.

In addition, the testInstrumentationRunner must be configured in the build.gradle file for the given Gradle module:

**Examples:**

Example 1 (java):
```java
package my.pkg;

public final class MyTestRunner extends AndroidJUnitRunner {
  @Override
  public Application newApplication(
      ClassLoader cl, String appName, Context context) {
    return super.newApplication(
        cl, HiltTestApplication.class.getName(), context);
  }
}
```

Example 2 (unknown):
```unknown
package my.pkg;

public final class MyTestRunner extends AndroidJUnitRunner {
  @Override
  public Application newApplication(
      ClassLoader cl, String appName, Context context) {
    return super.newApplication(
        cl, HiltTestApplication.class.getName(), context);
  }
}
```

Example 3 (kotlin):
```kotlin
package my.pkg

class MyTestRunner: AndroidJUnitRunner() {
  override fun newApplication(
      cl: ClassLoader,
      appName: String,
      context: Context) : Application {
    return super.newApplication(
        cl, HiltTestApplication::class.java.getName(), context)
  }
}
```

Example 4 (unknown):
```unknown
package my.pkg

class MyTestRunner: AndroidJUnitRunner() {
  override fun newApplication(
      cl: ClassLoader,
      appName: String,
      context: Context) : Application {
    return super.newApplication(
        cl, HiltTestApplication::class.java.getName(), context)
  }
}
```

---

## Instrumentation testing

**URL:** https://dagger.dev/hilt/instrumentation-testing

**Contents:**
- Instrumentation testing
- Setting the test application

Hilt’s testing APIs are built to be agnostic of the particular testing environment; however, the instructions for setting up the application class in your test will depend on whether you are using Robolectric or Android instrumentation tests.

For Android instrumentation tests, the application can be set using a custom test runner that extends AndroidJUnitRunner. To set the application using the runner, just override the newApplication method and pass in the application class name. For Hilt tests, the application must either be HiltTestApplication or one of Hilt’s custom test applications.

In addition, the testInstrumentationRunner must be configured in the build.gradle file for the given Gradle module:

**Examples:**

Example 1 (java):
```java
package my.pkg;

public final class MyTestRunner extends AndroidJUnitRunner {
  @Override
  public Application newApplication(
      ClassLoader cl, String appName, Context context) {
    return super.newApplication(
        cl, HiltTestApplication.class.getName(), context);
  }
}
```

Example 2 (unknown):
```unknown
package my.pkg;

public final class MyTestRunner extends AndroidJUnitRunner {
  @Override
  public Application newApplication(
      ClassLoader cl, String appName, Context context) {
    return super.newApplication(
        cl, HiltTestApplication.class.getName(), context);
  }
}
```

Example 3 (kotlin):
```kotlin
package my.pkg

class MyTestRunner: AndroidJUnitRunner() {
  override fun newApplication(
      cl: ClassLoader,
      appName: String,
      context: Context) : Application {
    return super.newApplication(
        cl, HiltTestApplication::class.java.getName(), context)
  }
}
```

Example 4 (unknown):
```unknown
package my.pkg

class MyTestRunner: AndroidJUnitRunner() {
  override fun newApplication(
      cl: ClassLoader,
      appName: String,
      context: Context) : Application {
    return super.newApplication(
        cl, HiltTestApplication::class.java.getName(), context)
  }
}
```

---
