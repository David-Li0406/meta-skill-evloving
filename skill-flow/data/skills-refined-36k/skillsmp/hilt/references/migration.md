# Hilt - Migration

**Pages:** 10

---

## Early entry points

**URL:** https://dagger.dev/hilt/early-entry-point

**Contents:**
- Early entry points
- Background
- Usage
- Caveats
- When not to use EarlyEntryPoint
  - Entry points for Application getter methods
  - Entry points for initialization/configuration

The @EarlyEntryPoint annotation provides an escape hatch when a Hilt entry point needs to be created before the singleton component is available in a Hilt test.

Note that, although @EarlyEntryPoint and EarlyEntryPoints are mostly used in production code, they only have an effect during Hilt tests. In production, these entry points behave the same as @EntryPoint and EntryPoints, respectively.

In a Hilt test, the singleton component’s lifetime is scoped to the lifetime of a test case rather than the lifetime of the Application. This is useful to prevent leaking state across test cases, but it makes it impossible to access entry points from a component outside of a test case.

To get a better understanding of why/when this becomes an issue, let’s look at a typical lifecycle of an Android Gradle instrumentation test.

As the lifecycle above shows, Application#onCreate() is called before any SingletonComponent can be created, so calling an entry point from Application#onCreate() is not possible. (For the same reason, there are similar issues with calling entry points from ContentProvider#onCreate()).

While these cases should be rare, sometimes they are unavoidable. This is where @EarlyEntryPoint comes in.

Annotating an entry point with @EarlyEntryPoint instead of @EntryPoint allows the entry point to be called at any point during the lifecyle of a test application. (Note that an @EarlyEntryPoint can only be installed in the SingletonComponent). For example:

Once annotated with @EarlyEntryPoint, all usages of the entry point must go through EarlyEntryPoints#get() (rather than EntryPoints#get() ) to get an instance of the entry point. This requirement makes it clear at the call site which component will be used during a Hilt test. For example:

The component used with EarlyEntryPoints does not share any state with the singleton component used for a given test case. Even @Singleton scoped bindings will not be shared.

The component used with EarlyEntryPoints does not have access to any test-specific bindings (i.e. bindings created within a specific test class such as @BindValue or a nested module).

Finally, the component used with EarlyEntryPoints lives for the lifetime of the application, so it can leak state across multiple test cases (e.g. in Android Gradle instrumentation tests).

Most usages of @EarlyEntryPoint are needed to allow calling entry points from within Application#onCreate() or ContentProvider#onCreate(). However, before switching to @EarlyEntryPoint, try the alternatives listed below.

If the entry point is used to initialize a field that will later be returned in a getter method, consider removing the field and getter method and replacing it with a @Singleton scoped binding that other classes can inject directly rather than going through the application class.

If the getter method is required (e.g. the application must extend an interface that requires it to be overriden) then try replacing the field with a @Singleton scoped binding and calling EntryPoints.get() lazily from the getter method.

If the entry point is used to perform initialization/configuration (e.g. setting up a logger or prefetching data) then first consider whether this work is necessary for your tests. Most tests, e.g. tests for activities and fragments should not be dependent on this initialization to work properly, since activities and fragments should generally be designed to be reusable in other applications.

If your test needs the initialization/configuration, consider whether it’s okay to only run the initialization/configuration once and share any state of that run between tests. If that’s not okay, then you may need to consider moving the logic into a TestRule instead.

**Examples:**

Example 1 (unknown):
```unknown
# Typical Application lifecycle during an Android Gradle instrumentation test
- Application created
    - Application.onCreate() called
    - Test1 created
        - SingletonComponent created
        - testCase1() called
    - Test1 created
        - SingletonComponent created
        - testCase2() called
    ...
    - Test2 created
        - SingletonComponent created
        - testCase1() called
    - Test2 created
        - SingletonComponent created
        - testCase2() called
    ...
- Application destroyed
```

Example 2 (java):
```java
@EarlyEntryPoint
@InstallIn(SingletonComponent.class)
public interface FooEntryPoint {
  Foo foo();
}
```

Example 3 (unknown):
```unknown
@EarlyEntryPoint
@InstallIn(SingletonComponent.class)
public interface FooEntryPoint {
  Foo foo();
}
```

Example 4 (kotlin):
```kotlin
@EarlyEntryPoint
@InstallIn(SingletonComponent::class)
interface FooEntryPoint {
  fun foo(): Foo
}
```

---

## Benefits of using Hilt

**URL:** https://dagger.dev/hilt/benefits

**Contents:**
- Benefits of using Hilt
- Reduced boilerplate
- Decoupled build dependencies
- Configuration
- Testing
- Standardization

The goal of Hilt is to enable users to focus on the Dagger binding definitions and usages without needing to worry about the rest of the Dagger setup. This means hiding things like component definitions with module and interface lists, code to create and hold on to components at the right points in the lifecycle, interfaces and casts to get the parent component, etc.

Some of the simplicity also comes from Hilt using monolithic components (i.e. using a single component for all activities, a single component for all fragments, etc). Hilt tries to encourage an essentially global binding namespace so that it is easy to know what binding definition is being used without having to trace back which activity or fragment you were injected from. For more information about this design decision, read here.

A naive usage of Dagger may introduce build problems if code references the Dagger component directly. These problems occur because the Dagger component has references to all of the modules installed. This can lead to bloated dependencies that slow down builds. The natural way to solve this involves interfaces and unsafe casts. This is a tradeoff though because these can introduce runtime errors. For example, introducing a new injector interface avoids directly depending on the component but then forgetting to make your component extend the injector interface results in a cast exception.

By code generating the interfaces, unsafe casts, and module/interface lists under the hood, Hilt makes these runtime unsafe casts safe due to the guarantees of the code generation and module/entry point discovery.

Apps often have different builds configurations like a production or development build that has different features. These different sets of features often mean a different set of Dagger modules. In a normal Dagger build, a different set of modules requires having a separate component tree (a separate component for every scope) with usually lots of portions repeated. Because Hilt installs modules via build dependencies and code generates the components, creating a different flavor of your build is as simple as compiling with an added or removed dependency.

Testing with Dagger can be hard, due to the configuration issue mentioned above. Hilt similarly makes changing out test modules and bindings easier due to the code generation of components. Hilt has specific test utilities built-in to make managing modules and providing test bindings easier so that tests can use Dagger. Using Dagger in tests helps reduce boilerplate in tests and makes tests more robust by instantiating code in the same way it is instantiated in production.

Hilt standardizes the component hierarchy. This means that libraries that integrate with Hilt can easily add or consume bindings from these known components. This allows for more complex libraries to be built that can integrate cleanly and more simply into any Hilt app.

---

## Early entry points

**URL:** https://dagger.dev/hilt/early-entry-point.html

**Contents:**
- Early entry points
- Background
- Usage
- Caveats
- When not to use EarlyEntryPoint
  - Entry points for Application getter methods
  - Entry points for initialization/configuration

The @EarlyEntryPoint annotation provides an escape hatch when a Hilt entry point needs to be created before the singleton component is available in a Hilt test.

Note that, although @EarlyEntryPoint and EarlyEntryPoints are mostly used in production code, they only have an effect during Hilt tests. In production, these entry points behave the same as @EntryPoint and EntryPoints, respectively.

In a Hilt test, the singleton component’s lifetime is scoped to the lifetime of a test case rather than the lifetime of the Application. This is useful to prevent leaking state across test cases, but it makes it impossible to access entry points from a component outside of a test case.

To get a better understanding of why/when this becomes an issue, let’s look at a typical lifecycle of an Android Gradle instrumentation test.

As the lifecycle above shows, Application#onCreate() is called before any SingletonComponent can be created, so calling an entry point from Application#onCreate() is not possible. (For the same reason, there are similar issues with calling entry points from ContentProvider#onCreate()).

While these cases should be rare, sometimes they are unavoidable. This is where @EarlyEntryPoint comes in.

Annotating an entry point with @EarlyEntryPoint instead of @EntryPoint allows the entry point to be called at any point during the lifecyle of a test application. (Note that an @EarlyEntryPoint can only be installed in the SingletonComponent). For example:

Once annotated with @EarlyEntryPoint, all usages of the entry point must go through EarlyEntryPoints#get() (rather than EntryPoints#get() ) to get an instance of the entry point. This requirement makes it clear at the call site which component will be used during a Hilt test. For example:

The component used with EarlyEntryPoints does not share any state with the singleton component used for a given test case. Even @Singleton scoped bindings will not be shared.

The component used with EarlyEntryPoints does not have access to any test-specific bindings (i.e. bindings created within a specific test class such as @BindValue or a nested module).

Finally, the component used with EarlyEntryPoints lives for the lifetime of the application, so it can leak state across multiple test cases (e.g. in Android Gradle instrumentation tests).

Most usages of @EarlyEntryPoint are needed to allow calling entry points from within Application#onCreate() or ContentProvider#onCreate(). However, before switching to @EarlyEntryPoint, try the alternatives listed below.

If the entry point is used to initialize a field that will later be returned in a getter method, consider removing the field and getter method and replacing it with a @Singleton scoped binding that other classes can inject directly rather than going through the application class.

If the getter method is required (e.g. the application must extend an interface that requires it to be overriden) then try replacing the field with a @Singleton scoped binding and calling EntryPoints.get() lazily from the getter method.

If the entry point is used to perform initialization/configuration (e.g. setting up a logger or prefetching data) then first consider whether this work is necessary for your tests. Most tests, e.g. tests for activities and fragments should not be dependent on this initialization to work properly, since activities and fragments should generally be designed to be reusable in other applications.

If your test needs the initialization/configuration, consider whether it’s okay to only run the initialization/configuration once and share any state of that run between tests. If that’s not okay, then you may need to consider moving the logic into a TestRule instead.

**Examples:**

Example 1 (unknown):
```unknown
# Typical Application lifecycle during an Android Gradle instrumentation test
- Application created
    - Application.onCreate() called
    - Test1 created
        - SingletonComponent created
        - testCase1() called
    - Test1 created
        - SingletonComponent created
        - testCase2() called
    ...
    - Test2 created
        - SingletonComponent created
        - testCase1() called
    - Test2 created
        - SingletonComponent created
        - testCase2() called
    ...
- Application destroyed
```

Example 2 (java):
```java
@EarlyEntryPoint
@InstallIn(SingletonComponent.class)
public interface FooEntryPoint {
  Foo foo();
}
```

Example 3 (unknown):
```unknown
@EarlyEntryPoint
@InstallIn(SingletonComponent.class)
public interface FooEntryPoint {
  Foo foo();
}
```

Example 4 (kotlin):
```kotlin
@EarlyEntryPoint
@InstallIn(SingletonComponent::class)
interface FooEntryPoint {
  fun foo(): Foo
}
```

---

## Migrating to Hilt

**URL:** https://dagger.dev/hilt/migration-guide

**Contents:**
- Migrating to Hilt
- Table of Contents
- 0. Plan your migration
  - Compare component hierarchies
  - Be aware of when Hilt injects classes
  - Migration Overview
- 1. Migrate the Application
  - Migrating a Component
    - a. Handle the modules
    - b. Handle any extended interfaces or methods

Migrating to Hilt can vary widely in difficulty depending on the state of your codebase and which practices or patterns your codebase follows. This page offers advice on some common issues migrating apps may encounter. This page assumes that you already generally understand the basic Hilt APIs. If that is not the case, take a look at our Quick Start guide for Hilt first. This page also assumes a general understanding of Dagger, which should be the case since this page is only useful for those migrating a codebase that already uses Dagger. If your codebase does not use Dagger, add Hilt to your app by going through the Quick Start guide as this guide only deals with migrations from non-Hilt Dagger setups.

Refactoring tip: Whenever you modify the code of a class, check that the unused or no longer existing imports are removed from the file.

When migrating to Hilt, you’ll want to organize your work into steps. This guide should lay out the general approach that should work for most cases, but every migration will be different. The recommended approach is to start at the Application or @Singleton component and incrementally grow from there. After Application and @Singleton, migrate activities and then fragments after that. This should generally be doable as an incremental migration. Even if you have a relatively small codebase, doing the migration incrementally will give you a chance to build in between steps to check your progress.

The first thing to do is to compare your current component hierarchy to the one in Hilt. You’ll want to decide which components map to which Hilt component. Hopefully these should be relatively straightforward, but if there is not a clear mapping, you can keep custom components as manual Dagger components. These components can be children of the Hilt components. However, Hilt does not allow inserting components into the hierarchy (e.g. changing the parent of a Hilt component). See the custom components section of the guide below. The rest of this guide assumes a migration where the components all map directly to Hilt components.

Also, if your code uses component dependencies, you should read the component dependencies section below first as well. The rest of this guide assumes usage of subcomponents.

If you are using the dagger.android @ContributesAndroidInjector and are unsure about your component hierarchy, then your hierarchy should roughly match the Hilt components.

You can find out when Hilt injects classes for each Android class here. These hopefully should be similar to where your code currently injects, but if not, be aware in case it causes any differences in your code.

At the end of the migration, the code should be changed as follows:

The first thing to change will be to migrate your Application and @Singleton component to the generated Hilt SingletonComponent. To do this, we’ll first want to make sure that everything that is installed in your current component is installed in the Hilt SingletonComponent.

To migrate the Application, we need to migrate everything in the pre-existing @Singleton component to the SingletonComponent.

First, we should install all of the modules into the SingletonComponent. This can be done by annotating each module currently installed in your component with @InstallIn(SingletonComponent.class). If there are a lot of modules, instead of changing all of those now, you can create and install a single aggregator @Module class that includes all of the current modules. This is just a temporary solution, however, since in order to take full advantage of Hilt features like replacing bindings, you will need to break up the aggregator module in the future.

Warning: Modules that are not annotated with @InstallIn are not used by Hilt. Hilt by default raises an error when unannotated modules are found, but this error can be disabled.

A similar process can be used for any interfaces your current component extends using @EntryPoint.

Interfaces on components are generally used to either add inject methods or get access to types like bindings or subcomponents. In Hilt many of these won’t be needed once the migration is complete because Hilt will generate them for you or they will be replaced by Hilt tools. For the migration though, this section will describe how to preserve current behavior so that code continues to work. You should be looking at all of these methods though and evaluating if they are still needed as the migration continues.

Annotate any interface your component extends with @EntryPoint and @InstallIn(SingletonComponent.class). If there are many interfaces, create a single aggregator interface to collect them all just like the modules. Any method defined directly on the component interface can be moved to either the aggregator interface or one the aggregator extends.

Hilt handles injecting your Application class under the hood, so if you had any inject methods for the Application, those can be removed. Inject methods for other Android types should also eventually be removed as those are later migrated to use @AndroidEntryPoint.

Your code likely has a method where you returned the component either directly or as one of the interface types so that other code could get access to inject methods or accessor methods. To keep this code working as you migrate, you can get a reference by using the EntryPoints class. As your migration continues, you should be able to remove these methods and have calling code use the Hilt EntryPoints API directly.

When migrating a component to Hilt, you’ll also need to migrate your bindings to use the Hilt scope annotations. In the case of the SingletonComponent, this is @Singleton. You can find which annotations correspond to which component in the component lifetimes section. If you aren’t using @Singleton and have your own scoping annotation, you can tell Hilt that your annotation is equivalent to a Hilt scoping annotation using scope aliases. This will allow you to migrate and remove your scoping annotation at your leisure later in the process.

Hilt components cannot take component arguments because the initialization of the component is hidden from users. Usually, this is used to get an application instance (or for other components an activity/fragment instance) into the Dagger graph. For these cases, you should switch to using the predefined bindings in Hilt that are listed here.

If your component has any other arguments either through module instances passed to the builder or @BindsInstance, read this section on handling those. Once you handle those, you can just remove your @Component.Builder interface as it will be unused.

If you used an aggregator module or entry point, you will eventually need to go back and remove the aggregator module and entry point class. You can do this by individually annotating all of the included modules and implemented interfaces with the same @InstallIn annotation used on the aggregator.

Now you can just annotate your Application with @HiltAndroidApp as described in our Quick Start guide. Apart from that, it should be empty of any code related to building or storing an instance of your component. You can delete your @Component class and @Component.Builder class if you haven’t already.

If your Application either extends from DaggerApplication or implements HasAndroidInjector, keep this code until all your dagger.android activities/fragments have been also migrated. This will likely be one of the final steps of your migration. These parts of dagger.android are there for making sure getting dependencies works (e.g. when an Activity tries to inject itself). The difference is now they are being satisfied by the Hilt SingletonComponent instead of the component removed in the above steps.

For example, a migrated dagger.android Application that supports both Hilt activities and dagger.android activities may look like this:

Or if you were using DaggerApplication before you can do the following. The @EntryPoint class is to make the Dagger component implement AndroidInjector<MyApplication>. This is likely what your previous Dagger component was doing before.

When you have migrated all of the other dagger.android usages and are ready to remove this code, simply extend from Application and remove the overridden methods and the DispatchingAndroidInjector classes.

If your application will be used in a Hilt test, then it’s important to note that Hilt does not currently allow field injection in test applications. (See “Early Entry Points” for more details). Thus, your test application cannot extend DaggerApplication since that class uses field injection under the hood. Instead, implement HasAndroidInjector and use an entry point to get the DispatchingAndroidInjector, as shown below:

You should be able to stop and build/run your app successfully at this point. Your app is successfully using Hilt for the SingletonComponent.

Now that the application supports Hilt, you should be able to start migrating your activities and then fragments to Hilt. While migrating your app, it is okay to have @AndroidEntryPoint activities and non-@AndroidEntryPoint activities together. The same is true for fragments within an activity. The only restriction with mixing Hilt with non-Hilt code is on the parent. Hilt activities need to be attached to Hilt applications. Hilt fragments must be attached to Hilt activities. We recommend doing all the activities before doing any of the fragments, but if that is problematic there is a tool to help relax that constraint with optional injection.

Migrating activities and fragments are going to be pretty similar to the application component in terms of mechanics. You should take all the modules from your current component and install them in the proper component with an @InstallIn module. Similarly, take all of the current component’s extended interfaces and install them in the proper component with an @InstallIn entry point. Go back to this section above for details, but also read below on some of the extra consideration that must be taken for activities and fragments.

Note: If you are using dagger.android’s @ContributesAndroidInjector, then when following this section on migrating a component the modules in @ContributesAndroidInjector are the modules you need to migrate. You do not have any interfaces to migrate with @EntryPoint.

One of the design decisions of Hilt is to use a single component for all of the activities and a single component for all of the fragments. If you’re interested, you can read about the reasons here. The reason this is important is that if you had a separate component for each activity (as is the default in dagger.android), you will be merging the components into a single component when migrating to Hilt. Depending on your code base, you could run into problems.

The two most frequent issues are:

This occurs if you defined the same binding key differently in two activities. When they are merged, you get a duplicate binding. This is a limitation of the global binding key space of Hilt and you’ll need to redefine that binding to have a single definition. Usually this isn’t too bad and is done by basing logic off of the injected activity. See the section on component arguments for examples.

Because of the merged component, bindings for a FooActivity or BarActivity often won’t make sense anymore since when the component is used for a BarActivity (or any other activity), a FooActivity binding won’t be able to be satisfied. Usually code doesn’t really rely on the actual child type of the activity and just needs an Activity or common subtype like FragmentActivity. Code using the child type needs to be refactored to use a more generic type. If you need a common subtype that isn’t automatically provided by Hilt, you can provide a binding with a cast (example here), but be careful!

Example of replacing a usage with a common subtype:

Hilt does not support retained fragments. You can find more info about why here. If you have any retained fragments, a common way to address this is to move any retained state into a ViewModel.

Now you can just annotate your Activity or Fragment with @AndroidEntryPoint as described in our Quick Start guide. Base classes, even if they perform field injection, don’t need to be annotated (unless there is a situation where they are instantiated directly as the childmost class).

Note: Even if your activity doesn’t need field injection, if there are fragments attached to it that use @AndroidEntryPoint, you must migrate the activity to use @AndroidEntryPoint as well.

Now you can remove any component initialization code or injection interfaces if you have them.

If you are using @ContributesAndroidInjector for this class, you can remove that now. You can also remove any calls to AndroidInjection/AndroidSupportInjection if you have them. If your class implements HasAndroidInjector, and it is not the parent of any non-Hilt fragments or views, you can remove that code now.

If your Activity or Fragment either extends from DaggerAppCompatActivity, DaggerFragment, or similar classes, these need to be removed and replaced with non-Dagger equivalents (like AppCompatActivity or a regular Fragment). If you have any child fragments or views that are still using dagger.android, you’ll need to implement HasAndroidInjector by injecting a DispatchingAndroidInjector (see example below).

When you have migrated all of the children off of dagger.android, come back later to remove the HasAndroidInjector code.

The following example shows migrating an activity while still allowing it to support both Hilt and dagger.android fragments.

Intermediate state that allows both Hilt and dagger.android fragments:

You should be able to stop and build/run your app successfully after migrating an activity or fragment. It is a good idea to check after migrating each class to make sure you’re on the right track.

View, Service, and BroadcastReceiver types should follow the same formula as above and be ready to migrate now. Once you have moved everything, you are done!

The qualifiers you have in your project are still valid, they’ll be used by Hilt in the same way they were used by Dagger.

If you have your own @ApplicationContext and @ActivityContext qualifiers to differentiate between different Contexts in your app, you can add an @Binds to map them together and then choose to replace your usage with the Hilt qualifiers at your leisure.

Because component instantiation is hidden when using Hilt, it is not possible to add in your own component arguments with either module instances or @BindsInstance calls. If you have these in your component, you’ll need to refactor your code away from using these. Hilt comes with a set of default bindings in each component which can be seen here. Depending on what your component arguments are, you may want to have some of them depend on those default bindings. This sometimes requires a slight redesign, but most cases can be solved this way using the following strategies. If that is not the case though, you may need to consider using a custom component.

For example, in the simplest case, sometimes the binding didn’t need to be passed in at all and it could be just a regular static @Provides method. In another simple case, your argument may just be a variation of the default binding like a custom BaseFragment type. Hilt can’t know that all Fragments are going to be an instance of your BaseFragment, so if you need the actual type bound to be your BaseFragment, you’ll need to do that with a cast.

In other cases, your argument may be something on one of the default bindings, like the activity Intent.

Finally, you may have to redesign some things if they were configured differently for different activity or fragment components. For example, you could use a new interface on the activity to provide the object.

If you have other components that do not map to the Hilt components, you should first consider if they can be simplified into the Hilt components. If not though, you can keep your components as manual Dagger components. Choose the section below based on if you want to use component dependencies or subcomponents.

Component dependencies can be hooked up with an @EntryPoint.

For example, if you had a component dependency off of the SingletonComponent, you can keep it working by factoring out the needed methods into an interface that is annotated with @EntryPoint.

When building the custom component, you can get an instance of the CustomComponentDependencies by using EntryPoints.

Subcomponents can be added as a child of any Hilt component in the same way you would install a normal subcomponent with an injectable subcomponent builder in Dagger. Just install the subcomponent in a module with the appropriate @InstallIn of the parent.

For example, if you have a FooSubcomponent that is a child of the SingletonComponent, you can install it like the following example:

If you currently use component dependencies and your components map relatively well to the Hilt components, then as you migrate you’ll also need to keep in the mind the differences between component dependencies and subcomponents. You may also want to check out this page which describes some of the reasons Hilt chose to use subcomponents.

The main differences to be aware of will be that bindings are automatically inherited from the parent. This means likely getting rid of extra methods for exposing bindings as well as dealing with any duplicate bindings that may arise if a binding is defined in both the parent and child components. Getting rid of those extra methods for exposing bindings is optional as they will not technically break your build, but it is recommended as they can prevent some dead code pruning. They can be safely migrated though as described in this section.

Here is an example of the exposed bindings:

Then when you follow steps above to migrate components, if your component has a dep on a component that is equivalent to the Hilt parent, just remove the dep as you remove the rest of the component.

**Examples:**

Example 1 (java):
```java
// Starting with this component
@Component(modules = {
    FooModule.class,
    BarModule.class,
    ...
})
interface MySingletonComponent {
}

// Becomes the following classes
@InstallIn(SingletonComponent.class)
@Module(includes = {
    FooModule.class,
    BarModule.class,
    ...
})
interface AggregatorModule {}
```

Example 2 (unknown):
```unknown
// Starting with this component
@Component(modules = {
    FooModule.class,
    BarModule.class,
    ...
})
interface MySingletonComponent {
}

// Becomes the following classes
@InstallIn(SingletonComponent.class)
@Module(includes = {
    FooModule.class,
    BarModule.class,
    ...
})
interface AggregatorModule {}
```

Example 3 (kotlin):
```kotlin
// Starting with this component
@Component(modules = [
    FooModule::class,
    BarModule::class,
    ...
])
interface MySingletonComponent {
}

// Becomes the following classes
@InstallIn(SingletonComponent::class)
@Module(includes = [
    FooModule::class,
    BarModule::class,
    ...
])
interface AggregatorModule {}
```

Example 4 (unknown):
```unknown
// Starting with this component
@Component(modules = [
    FooModule::class,
    BarModule::class,
    ...
])
interface MySingletonComponent {
}

// Becomes the following classes
@InstallIn(SingletonComponent::class)
@Module(includes = [
    FooModule::class,
    BarModule::class,
    ...
])
interface AggregatorModule {}
```

---

## Flags

**URL:** https://dagger.dev/hilt/flags.html

**Contents:**
- Flags
- Compiler Options
  - Turning off the @InstallIn check
- Sharing test components
  - Entry point method return types must be public
  - Entry point method names must be unique
  - Modules with non-static/non-abstract methods must be public
- Turning off the cross compilation root validation
- Runtime flags
  - Disable Fragment.getContext() fix

By default, Hilt checks @Module classes for the @InstallIn annotation and raises an error if it is missing. This is because if someone accidentally forgets to put @InstallIn on a module, it could be very hard to debug that Hilt isn’t picking it up.

This check can sometimes be overly broad though, especially if in the middle of a migration. To turn off this check, this flag can be used:

-Adagger.hilt.disableModulesHaveInstallInCheck=true.

Alternatively, the check can be disabled at the individual module level by annotating the module with @DisableInstallInCheck.

In cases where a test does not define @BindValue fields or inner modules, it can share a generated component with other tests in the same compilation unit. Sharing components may reduce the amount of generated code that javac needs to compile, improving build times.

When component sharing is enabled, all test components are generated in a separate package from your test class. This may cause visibility and name collision issues. Those issues are described in the sections below.

Sharing components is enabled by default. If your project does not build due to component sharing, you can disable this behavior and have Hilt generate a Dagger separate @Component for each @HiltAndroidTest using this flag:

-Adagger.hilt.shareTestComponents=false

However, consider the following fixes in order to avoid disabling this behavior.

Because the shared components must be generated in a common package location that is outside of the tests’ packages, any entry points included by the test must only provide publicly visible bindings. This is in order to be referenced by the generated components. You may find that you will have to mark some Java types as public (or remove internal in Kotlin).

Because the shared components must include entry points from every test class, explicit @EntryPoint methods must not clash. Test @EntryPoint methods must either be uniquely named across test classes, or must return the same type.

The generated Dagger component must be able to instantiate modules that have methods that are non-static and non-abstract. This requires referencing the module type explicitly across package boundaries. You may need to mark some package-private test modules as public.

By default, Hilt checks that:

This check can sometimes be overly broad though, especially if in the middle of a migration. To turn off this check, this flag can be used:

-Adagger.hilt.disableCrossCompilationRootValidation=true.

Runtime flags to control Hilt behavior for rollout of changes. These flags are usually meant to be temporary and so defaults may change with releases and then these flags may eventually be removed, just like compiler options with similar purposes.

See https://github.com/google/dagger/pull/2620 for the change that introduces the getContext() fix. This flag controls if fragment code should use the fixed getContext() behavior where it correctly returns null after a fragment is removed. This fixed behavior matches the behavior of a regular, non-Hilt fragment and can help catch issues where a removed or leaked fragment is incorrectly used. This is a runtime flag though because code previous relying on the method returning a non-null value after fragment removal could break.

By default, the fix is turned off (e.g. the flag for disabling is true), but the fixed version may be used by setting the flag at runtime. The default for this flag may change in a future release.

In order to set the flag, bind a boolean value qualified with DisableFragmentGetContextFix into a set in the SingletonComponent. A set is used instead of an optional binding to avoid a dependency on Guava. Only one value may be bound into the set within a given app. Example for binding the value:

This flag used to be paired with a compiler option flag dagger.hilt.android.useFragmentGetContextFix, however, as of Dagger 2.40 this compiler option has now been removed and this behavior is only controlled via the runtime flag.

**Examples:**

Example 1 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent.class)
public final class DisableFragmentGetContextFixModule {
@Provides
@IntoSet
@FragmentGetContextFix.DisableFragmentGetContextFix
  static Boolean provideDisableFragmentGetContextFix() {
    // Return true or false depending on some rollout logic for your app
    // True is the default value if unset. Use false to use the fixed behavior.
 }
}
```

---

## Scope aliases

**URL:** https://dagger.dev/hilt/scope-aliases.html

**Contents:**
- Scope aliases
- Why would you need a scope alias?
- How to use @AliasOf

Scope aliases are useful during a migration to Hilt if you have a lot of code using a previous scope annotation that you now want to switch to one of the Hilt provided scope annotations. Depending on the size of your codebase, this could mean changing the scope annotation in a lot of places. By adding a scope alias, you can make the changes incrementally.

Using a scope alias just tells Dagger and Hilt that these scope annotations should be treated the same.

If you mark a scope annotation with @AliasOf, it will tell Hilt that the annotated scope annotation should be treated the same as the one in the value of the @AliasOf annotation. The annotation value must be a scope annotation used in a @DefineComponent type so that Hilt knows what to do with it.

For example, the following takes a previous @MyActivityScoped annotation and makes it equivalent to the Hilt @ActivityScoped. Now it should be easy to incrementally replace @MyActivityScoped with the Hilt version.

**Examples:**

Example 1 (unknown):
```unknown
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped.class)
public @interface MyActivityScoped {}
```

Example 2 (kotlin):
```kotlin
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped::class)
annotation class MyActivityScoped {}
```

Example 3 (unknown):
```unknown
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped::class)
annotation class MyActivityScoped {}
```

---

## Scope aliases

**URL:** https://dagger.dev/hilt/scope-aliases

**Contents:**
- Scope aliases
- Why would you need a scope alias?
- How to use @AliasOf

Scope aliases are useful during a migration to Hilt if you have a lot of code using a previous scope annotation that you now want to switch to one of the Hilt provided scope annotations. Depending on the size of your codebase, this could mean changing the scope annotation in a lot of places. By adding a scope alias, you can make the changes incrementally.

Using a scope alias just tells Dagger and Hilt that these scope annotations should be treated the same.

If you mark a scope annotation with @AliasOf, it will tell Hilt that the annotated scope annotation should be treated the same as the one in the value of the @AliasOf annotation. The annotation value must be a scope annotation used in a @DefineComponent type so that Hilt knows what to do with it.

For example, the following takes a previous @MyActivityScoped annotation and makes it equivalent to the Hilt @ActivityScoped. Now it should be easy to incrementally replace @MyActivityScoped with the Hilt version.

**Examples:**

Example 1 (unknown):
```unknown
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped.class)
public @interface MyActivityScoped {}
```

Example 2 (kotlin):
```kotlin
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped::class)
annotation class MyActivityScoped {}
```

Example 3 (unknown):
```unknown
@Scope
@AliasOf(dagger.hilt.android.scopes.ActivityScoped::class)
annotation class MyActivityScoped {}
```

---

## Flags

**URL:** https://dagger.dev/hilt/flags

**Contents:**
- Flags
- Compiler Options
  - Turning off the @InstallIn check
- Sharing test components
  - Entry point method return types must be public
  - Entry point method names must be unique
  - Modules with non-static/non-abstract methods must be public
- Turning off the cross compilation root validation
- Runtime flags
  - Disable Fragment.getContext() fix

By default, Hilt checks @Module classes for the @InstallIn annotation and raises an error if it is missing. This is because if someone accidentally forgets to put @InstallIn on a module, it could be very hard to debug that Hilt isn’t picking it up.

This check can sometimes be overly broad though, especially if in the middle of a migration. To turn off this check, this flag can be used:

-Adagger.hilt.disableModulesHaveInstallInCheck=true.

Alternatively, the check can be disabled at the individual module level by annotating the module with @DisableInstallInCheck.

In cases where a test does not define @BindValue fields or inner modules, it can share a generated component with other tests in the same compilation unit. Sharing components may reduce the amount of generated code that javac needs to compile, improving build times.

When component sharing is enabled, all test components are generated in a separate package from your test class. This may cause visibility and name collision issues. Those issues are described in the sections below.

Sharing components is enabled by default. If your project does not build due to component sharing, you can disable this behavior and have Hilt generate a Dagger separate @Component for each @HiltAndroidTest using this flag:

-Adagger.hilt.shareTestComponents=false

However, consider the following fixes in order to avoid disabling this behavior.

Because the shared components must be generated in a common package location that is outside of the tests’ packages, any entry points included by the test must only provide publicly visible bindings. This is in order to be referenced by the generated components. You may find that you will have to mark some Java types as public (or remove internal in Kotlin).

Because the shared components must include entry points from every test class, explicit @EntryPoint methods must not clash. Test @EntryPoint methods must either be uniquely named across test classes, or must return the same type.

The generated Dagger component must be able to instantiate modules that have methods that are non-static and non-abstract. This requires referencing the module type explicitly across package boundaries. You may need to mark some package-private test modules as public.

By default, Hilt checks that:

This check can sometimes be overly broad though, especially if in the middle of a migration. To turn off this check, this flag can be used:

-Adagger.hilt.disableCrossCompilationRootValidation=true.

Runtime flags to control Hilt behavior for rollout of changes. These flags are usually meant to be temporary and so defaults may change with releases and then these flags may eventually be removed, just like compiler options with similar purposes.

See https://github.com/google/dagger/pull/2620 for the change that introduces the getContext() fix. This flag controls if fragment code should use the fixed getContext() behavior where it correctly returns null after a fragment is removed. This fixed behavior matches the behavior of a regular, non-Hilt fragment and can help catch issues where a removed or leaked fragment is incorrectly used. This is a runtime flag though because code previous relying on the method returning a non-null value after fragment removal could break.

By default, the fix is turned off (e.g. the flag for disabling is true), but the fixed version may be used by setting the flag at runtime. The default for this flag may change in a future release.

In order to set the flag, bind a boolean value qualified with DisableFragmentGetContextFix into a set in the SingletonComponent. A set is used instead of an optional binding to avoid a dependency on Guava. Only one value may be bound into the set within a given app. Example for binding the value:

This flag used to be paired with a compiler option flag dagger.hilt.android.useFragmentGetContextFix, however, as of Dagger 2.40 this compiler option has now been removed and this behavior is only controlled via the runtime flag.

**Examples:**

Example 1 (unknown):
```unknown
@Module
@InstallIn(SingletonComponent.class)
public final class DisableFragmentGetContextFixModule {
@Provides
@IntoSet
@FragmentGetContextFix.DisableFragmentGetContextFix
  static Boolean provideDisableFragmentGetContextFix() {
    // Return true or false depending on some rollout logic for your app
    // True is the default value if unset. Use false to use the fixed behavior.
 }
}
```

---

## Hilt

**URL:** https://dagger.dev/hilt/

**Contents:**
- Hilt
- Hilt Design Overview

Hilt provides a standard way to incorporate Dagger dependency injection into an Android application.

The goals of Hilt are:

Hilt works by code generating your Dagger setup code for you. This takes away most of the boilerplate of using Dagger and really just leaves the aspects of defining how to create objects and where to inject them. Hilt will generate the Dagger components and the code to automatically inject your Android classes (like activities and fragments) for you.

Hilt generates a set of standard Android Dagger components based off of your transitive classpath. This requires marking your Dagger modules with Hilt annotations to tell Hilt which component they should go into. Getting objects in your Android framework classes is done by using another Hilt annotation which will generate the Dagger injection code into a base class that you will extend. For Gradle users, extending this class is done with a bytecode transformation under the hood.

In your tests, Hilt generates Dagger components for you as well just like in production. Tests have other special utilities to help with adding or replacing test bindings.

---

## Custom inject

**URL:** https://dagger.dev/hilt/custom-inject

**Contents:**
- Custom inject
- @CustomInject
- Example

In special circumstances, you may find that Hilt’s default behavior of injecting the Application class in super.onCreate is not suitable for your application. For example, there may be things that you want to do before injecting fields. In this case, you can use @CustomInject to control if/when the application is injected.

When you annotate your @HiltAndroidApp application class with @CustomInject, the injection no longer happens in onCreate. You can then use CustomInjection to inject your application at a time of your choosing.

Note: If you are not using the Gradle plugin and extend the generated Hilt base class directly, you can also just call the customInject() method which is on the generated base class.

Be aware that injection only injects the fields of the application and so is not required or necessary if there are no @Inject fields in your application or its base classes. Also note that this does not prevent the SingletonComponent from being instantiated. If other code requests the SingletonComponent like an @AndroidEntryPoint class being created, the SingletonComponent will still be created on demand.

**Examples:**

Example 1 (java):
```java
@CustomInject
@HiltAndroidApp
public final class MyApplication extends Application {
  @Inject Foo foo;

  @Override
  public void onCreate() {
    // Injection would normally happen in this super.onCreate() call, but won't
    // now because this is using CustomInject.
    super.onCreate();
    doSomethingBeforeInjection();
    // This call now injects the fields in the Application, like the foo field above.
    CustomInjection.inject(this);
  }
}
```

Example 2 (unknown):
```unknown
@CustomInject
@HiltAndroidApp
public final class MyApplication extends Application {
  @Inject Foo foo;

  @Override
  public void onCreate() {
    // Injection would normally happen in this super.onCreate() call, but won't
    // now because this is using CustomInject.
    super.onCreate();
    doSomethingBeforeInjection();
    // This call now injects the fields in the Application, like the foo field above.
    CustomInjection.inject(this);
  }
}
```

Example 3 (kotlin):
```kotlin
@CustomInject
@HiltAndroidApp
class MyApplication : Application() {
  @Inject lateinit var foo: Foo

  override fun onCreate() {
    // Injection would normally happen in this super.onCreate() call, but won't
    // now because this is using CustomInject.
    super.onCreate()
    doSomethingBeforeInjection()
    // This call now injects the fields in the Application, like the foo field above.
    CustomInjection.inject(this)
  }
}
```

Example 4 (unknown):
```unknown
@CustomInject
@HiltAndroidApp
class MyApplication : Application() {
  @Inject lateinit var foo: Foo

  override fun onCreate() {
    // Injection would normally happen in this super.onCreate() call, but won't
    // now because this is using CustomInject.
    super.onCreate()
    doSomethingBeforeInjection()
    // This call now injects the fields in the Application, like the foo field above.
    CustomInjection.inject(this)
  }
}
```

---
