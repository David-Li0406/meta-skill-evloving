# Hilt - Getting Started

**Pages:** 6

---

## Quick Start Guide

**URL:** https://dagger.dev/hilt/quick-start

**Contents:**
- Quick Start Guide
- Introduction
- Gradle vs non-Gradle users
- Hilt Application
- @AndroidEntryPoint
- Hilt Modules
  - Using @InstallIn

Hilt makes it easy to add dependency injection to your Android app. This tutorial will guide you through bootstrapping an existing app to use Hilt.

For more on the basic concepts of Hilt’s components, check out Hilt Components.

For Gradle users, the Hilt Gradle plugin makes usages of some Hilt annotations easier by avoiding references to Hilt generated classes.

Without the Gradle plugin, the base class must be specified in the annotation and the annotated class must extend the generated class:

With the Gradle plugin the annotated class can extend the base class directly:

Further examples assume usage of the Hilt Gradle plugin.

All apps using Hilt must contain an Application class annotated with @HiltAndroidApp. @HiltAndroidApp kicks off the code generation of the Hilt components and also generates a base class for your application that uses those generated components. Because the code generation needs access to all of your modules, the target that compiles your Application class also needs to have all of your Dagger modules in its transitive dependencies.

Just like other Hilt Android entry points, Applications are members injected as well. This means you can use injected fields in the Application after super.onCreate() has been called.

Note: Since all injected fields are created at the same time in onCreate, if an object is only needed later or conditionally, remember that you can use a Provider to defer injection. Especially in the Application class which is on the critical startup path, avoiding unnecessary injections can be important to performance.

For example, take the class called MyApplication that extends MyBaseApplication and has a member variable Bar:

With Hilt’s members injection, the above code becomes:

For more details, see Hilt Application.

Once you have enabled members injection in your Application, you can start enabling members injection in your other Android classes using the @AndroidEntryPoint annotation. You can use @AndroidEntryPoint on the following types:

Note that ViewModels are supported via a separate API @HiltViewModel. The following example shows how to add the annotation to an activity, but the process is the same for other types.

To enable members injection in your activity, annotate your class with @AndroidEntryPoint.

Note: Hilt currently only supports activities that extend ComponentActivity and fragments that extend androidx library Fragment, not the (now deprecated) Fragment in the Android platform.

For more details, see @AndroidEntryPoint.

Hilt modules are standard Dagger modules that have an additional @InstallIn annotation that determines which Hilt component(s) to install the module into.

When the Hilt components are generated, the modules annotated with @InstallIn will be installed into the corresponding component or subcomponent via @Component#modules or @Subcomponent#modules respectively. Just like in Dagger, installing a module into a component allows that binding to be accessed as a dependency of other bindings in that component or any child component(s) below it in the component hierarchy. They can also be accessed from the corresponding @AndroidEntryPoint classes. Being installed in a component also allows that binding to be scoped to that component.

A module is installed in a Hilt Component by annotating the module with the @InstallIn annotation. These annotations are required on all Dagger modules when using Hilt, but this check may be optionally disabled.

Note: If a module does not have an @InstallIn annotation, the module will not be part of the component and may result in compilation errors.

Specify which Hilt Component to install the module in by passing in the appropriate Component type(s) to the @InstallIn annotation. For example, to install a module so that anything in the application can use it, use SingletonComponent:

For more details, see Hilt Modules.

**Examples:**

Example 1 (java):
```java
@HiltAndroidApp(MultiDexApplication.class)
public final class MyApplication extends Hilt_MyApplication {}
```

Example 2 (unknown):
```unknown
@HiltAndroidApp(MultiDexApplication.class)
public final class MyApplication extends Hilt_MyApplication {}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidApp(MultiDexApplication::class)
class MyApplication : Hilt_MyApplication()
```

Example 4 (unknown):
```unknown
@HiltAndroidApp(MultiDexApplication::class)
class MyApplication : Hilt_MyApplication()
```

---

## Hilt Application

**URL:** https://dagger.dev/hilt/application

**Contents:**
- Hilt Application
- Hilt Application

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

All apps using Hilt must contain an Application class annotated with @HiltAndroidApp. @HiltAndroidApp kicks off the code generation of the Hilt components and also generates a base class for your application that uses those generated components. Because the code generation needs access to all of your modules, the target that compiles your Application class also needs to have all of your Dagger modules in its transitive dependencies.

Just like other Hilt Android entry points, Applications are members injected as well. This means you can use injected fields in the Application after super.onCreate() has been called.

Note: Since all injected fields are created at the same time in onCreate, if an object is only needed later or conditionally, remember that you can use a Provider to defer injection. Especially in the Application class which is on the critical startup path, avoiding unnecessary injections can be important to performance.

For example, take the class called MyApplication that extends MyBaseApplication and has a member variable Bar:

With Hilt’s members injection, the above code becomes:

**Examples:**

Example 1 (java):
```java
public final class MyApplication extends MyBaseApplication {
  @Inject Bar bar;

  @Override public void onCreate() {
    super.onCreate();

    MyComponent myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build();

    myComponent.inject(this);
  }
}
```

Example 2 (unknown):
```unknown
public final class MyApplication extends MyBaseApplication {
  @Inject Bar bar;

  @Override public void onCreate() {
    super.onCreate();

    MyComponent myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build();

    myComponent.inject(this);
  }
}
```

Example 3 (kotlin):
```kotlin
class MyApplication : MyBaseApplication() {
  @Inject lateinit var bar: Bar

  override fun onCreate() {
    super.onCreate()

    val myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build()

    myComponent.inject(this)
  }
}
```

Example 4 (unknown):
```unknown
class MyApplication : MyBaseApplication() {
  @Inject lateinit var bar: Bar

  override fun onCreate() {
    super.onCreate()

    val myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build()

    myComponent.inject(this)
  }
}
```

---

## Quick Start Guide

**URL:** https://dagger.dev/hilt/quick-start.html

**Contents:**
- Quick Start Guide
- Introduction
- Gradle vs non-Gradle users
- Hilt Application
- @AndroidEntryPoint
- Hilt Modules
  - Using @InstallIn

Hilt makes it easy to add dependency injection to your Android app. This tutorial will guide you through bootstrapping an existing app to use Hilt.

For more on the basic concepts of Hilt’s components, check out Hilt Components.

For Gradle users, the Hilt Gradle plugin makes usages of some Hilt annotations easier by avoiding references to Hilt generated classes.

Without the Gradle plugin, the base class must be specified in the annotation and the annotated class must extend the generated class:

With the Gradle plugin the annotated class can extend the base class directly:

Further examples assume usage of the Hilt Gradle plugin.

All apps using Hilt must contain an Application class annotated with @HiltAndroidApp. @HiltAndroidApp kicks off the code generation of the Hilt components and also generates a base class for your application that uses those generated components. Because the code generation needs access to all of your modules, the target that compiles your Application class also needs to have all of your Dagger modules in its transitive dependencies.

Just like other Hilt Android entry points, Applications are members injected as well. This means you can use injected fields in the Application after super.onCreate() has been called.

Note: Since all injected fields are created at the same time in onCreate, if an object is only needed later or conditionally, remember that you can use a Provider to defer injection. Especially in the Application class which is on the critical startup path, avoiding unnecessary injections can be important to performance.

For example, take the class called MyApplication that extends MyBaseApplication and has a member variable Bar:

With Hilt’s members injection, the above code becomes:

For more details, see Hilt Application.

Once you have enabled members injection in your Application, you can start enabling members injection in your other Android classes using the @AndroidEntryPoint annotation. You can use @AndroidEntryPoint on the following types:

Note that ViewModels are supported via a separate API @HiltViewModel. The following example shows how to add the annotation to an activity, but the process is the same for other types.

To enable members injection in your activity, annotate your class with @AndroidEntryPoint.

Note: Hilt currently only supports activities that extend ComponentActivity and fragments that extend androidx library Fragment, not the (now deprecated) Fragment in the Android platform.

For more details, see @AndroidEntryPoint.

Hilt modules are standard Dagger modules that have an additional @InstallIn annotation that determines which Hilt component(s) to install the module into.

When the Hilt components are generated, the modules annotated with @InstallIn will be installed into the corresponding component or subcomponent via @Component#modules or @Subcomponent#modules respectively. Just like in Dagger, installing a module into a component allows that binding to be accessed as a dependency of other bindings in that component or any child component(s) below it in the component hierarchy. They can also be accessed from the corresponding @AndroidEntryPoint classes. Being installed in a component also allows that binding to be scoped to that component.

A module is installed in a Hilt Component by annotating the module with the @InstallIn annotation. These annotations are required on all Dagger modules when using Hilt, but this check may be optionally disabled.

Note: If a module does not have an @InstallIn annotation, the module will not be part of the component and may result in compilation errors.

Specify which Hilt Component to install the module in by passing in the appropriate Component type(s) to the @InstallIn annotation. For example, to install a module so that anything in the application can use it, use SingletonComponent:

For more details, see Hilt Modules.

**Examples:**

Example 1 (java):
```java
@HiltAndroidApp(MultiDexApplication.class)
public final class MyApplication extends Hilt_MyApplication {}
```

Example 2 (unknown):
```unknown
@HiltAndroidApp(MultiDexApplication.class)
public final class MyApplication extends Hilt_MyApplication {}
```

Example 3 (kotlin):
```kotlin
@HiltAndroidApp(MultiDexApplication::class)
class MyApplication : Hilt_MyApplication()
```

Example 4 (unknown):
```unknown
@HiltAndroidApp(MultiDexApplication::class)
class MyApplication : Hilt_MyApplication()
```

---

## Gradle Build Setup

**URL:** https://dagger.dev/hilt/gradle-setup.html

**Contents:**
- Gradle Build Setup
- Hilt dependencies
- Using Hilt with Kotlin
- Hilt Gradle plugin
  - Apply Hilt Gradle Plugin with Plugins DSL
  - Why use the plugin?
  - Aggregating Task
  - Applying other processor arguments
  - Local test configuration (AGP < 4.2 only)
  - Classpath Aggregation (Deprecated)

To use Hilt, add the following build dependencies to the Android Gradle module’s build.gradle file:

If using Kotlin, then apply the kapt plugin and declare the compiler dependency using kapt instead of annotationProcessor.

Additionally configure kapt to correct error types by setting correctErrorTypes to true.

The Hilt Gradle plugin runs a bytecode transformation to make the APIs easier to use. The plugin was created for a better developer experience in the IDE since the generated class can disrupt code completion for methods on the base class. The examples throughout the docs will assume usage of the plugin. To configure the Hilt Gradle plugin first declare the dependency in your project’s root build.gradle file:

then in the build.gradle of your Android Gradle modules apply the plugin:

To configure the Hilt Gradle plugin with Gradle’s new plugins DSL , add the plugin id in your project’s root build.gradle file:

then apply the plugin in the build.gradle of your Android Gradle modules:

Warning: The Hilt Gradle plugin sets annotation processor arguments. If you are using other libraries that require annotation processor arguments, make sure you are adding arguments instead of overriding them. See below for an example.

One benefit of the Gradle plugin is that it makes using @AndroidEntryPoint and @HiltAndroidApp easier because it avoids the need to reference Hilt’s generated classes.

Without the Gradle plugin, the base class must be specified in the annotation and the annotated class must extend the generated class:

With the Gradle plugin the annotated class can extend the base class directly:

The Hilt Gradle plugin offers an option for performing Hilt’s classpath aggregation in a dedicated Gradle task. This allows the Hilt annotation processors to be isolating so they are only invoked when necessary. This reduces incremental compilation times by reducing how often an incremental change causes a rebuild of the Dagger components. Enabling this option also enables sharing test components and classpath aggregation. Note that this option replaces enableExperimentalClasspathAggregation since it has the same benefits without any of its caveats.

To enable the aggregating task, apply the following configuration in your Android module’s build.gradle:

The Hilt Gradle plugin sets annotation processor arguments. If you are using other libraries that require annotation processor arguments, make sure you are adding arguments instead of overriding them.

For example, the following notably uses += to avoid overriding the Hilt arguments.

If the + is missing and arguments are overridden, it is likely Hilt will fail to compile with errors like the following: Expected @HiltAndroidApp to have a value. Did you forget to apply the Gradle Plugin?

Warning: This flag should only be used with AGP < 4.2. Newer versions of AGP no longer need this flag.

When the Android Gradle plugin (AGP) version used in the project is less than 4.2, then the Hilt Gradle plugin by default, will only transform instrumented test classes (usually located in the androidTest source folder), but an additional configuration is required for the plugin to transform local jvm tests (usually located in the test source folder).

To enable transforming @AndroidEntryPoint classes in local jvm tests, apply the following configuration in your module’s build.gradle:

Note that the enableTransformForLocalTests configuration only works when running from the command line, e.g. ./gradlew test. It does not work when running tests with Android Studio (via the play button in the test method or class). There are a few options to work around the issue.

The first option is to upgrade the AGP version in your project to 4.2+.

The second option, is to create your own Android Studio configuration that executes tests via the Gradle task. To do this, create a new ‘Run Configuration’ of type ‘Gradle’ from within Android Studio with the following parameters:

As an example, see the setup below:

Warning: This flag is deprecated and will be removed in a future release of Dagger. Use enableAggregatingTask instead.

The Hilt Gradle plugin also offers an experimental option for configuring the compile classpath for annotation processing such that Hilt and Dagger are able to traverse and inspect classes across all transitive dependencies from within the application Gradle module. We recommend enabling this option because without it, an implementation dependency may drop important information about @InstallIn modules or @EntryPoint interfaces from the compile classpath. This can lead to subtle and/or confusing errors, that in the case of multibindings may only manifest at runtime. With this option enabled, implementation dependencies don’t have to be relaxed to api. Note that this option might have a build performance impact due to an increase in compilation classpath. For more context on the problems this solves, see issues #1991 and #970.

Warning: If the Android Gradle plugin version used in the project is less than 7.0 then android.lintOptions.checkReleaseBuilds has to be set to false when enableExperimentalClasspathAggregation is set to true due to an existing bug in prior versions of AGP.

To enable classpath aggregation, apply the following configuration in your Android module’s build.gradle:

**Examples:**

Example 1 (unknown):
```unknown
dependencies {
  implementation 'com.google.dagger:hilt-android:2.57.2'
  annotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'

  // For instrumentation tests
  androidTestImplementation  'com.google.dagger:hilt-android-testing:2.57.2'
  androidTestAnnotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'

  // For local unit tests
  testImplementation 'com.google.dagger:hilt-android-testing:2.57.2'
  testAnnotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'
}
```

Example 2 (unknown):
```unknown
dependencies {
  implementation 'com.google.dagger:hilt-android:2.57.2'
  kapt 'com.google.dagger:hilt-compiler:2.57.2'

  // For instrumentation tests
  androidTestImplementation  'com.google.dagger:hilt-android-testing:2.57.2'
  kaptAndroidTest 'com.google.dagger:hilt-compiler:2.57.2'

  // For local unit tests
  testImplementation 'com.google.dagger:hilt-android-testing:2.57.2'
  kaptTest 'com.google.dagger:hilt-compiler:2.57.2'
}

kapt {
 correctErrorTypes true
}
```

Example 3 (unknown):
```unknown
buildscript {
  repositories {
    // other repositories...
    mavenCentral()
  }
  dependencies {
    // other plugins...
    classpath 'com.google.dagger:hilt-android-gradle-plugin:2.57.2'
  }
}
```

Example 4 (unknown):
```unknown
apply plugin: 'com.android.application'
apply plugin: 'com.google.dagger.hilt.android'

android {
  // ...
}
```

---

## Hilt Application

**URL:** https://dagger.dev/hilt/application.html

**Contents:**
- Hilt Application
- Hilt Application

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

All apps using Hilt must contain an Application class annotated with @HiltAndroidApp. @HiltAndroidApp kicks off the code generation of the Hilt components and also generates a base class for your application that uses those generated components. Because the code generation needs access to all of your modules, the target that compiles your Application class also needs to have all of your Dagger modules in its transitive dependencies.

Just like other Hilt Android entry points, Applications are members injected as well. This means you can use injected fields in the Application after super.onCreate() has been called.

Note: Since all injected fields are created at the same time in onCreate, if an object is only needed later or conditionally, remember that you can use a Provider to defer injection. Especially in the Application class which is on the critical startup path, avoiding unnecessary injections can be important to performance.

For example, take the class called MyApplication that extends MyBaseApplication and has a member variable Bar:

With Hilt’s members injection, the above code becomes:

**Examples:**

Example 1 (java):
```java
public final class MyApplication extends MyBaseApplication {
  @Inject Bar bar;

  @Override public void onCreate() {
    super.onCreate();

    MyComponent myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build();

    myComponent.inject(this);
  }
}
```

Example 2 (unknown):
```unknown
public final class MyApplication extends MyBaseApplication {
  @Inject Bar bar;

  @Override public void onCreate() {
    super.onCreate();

    MyComponent myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build();

    myComponent.inject(this);
  }
}
```

Example 3 (kotlin):
```kotlin
class MyApplication : MyBaseApplication() {
  @Inject lateinit var bar: Bar

  override fun onCreate() {
    super.onCreate()

    val myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build()

    myComponent.inject(this)
  }
}
```

Example 4 (unknown):
```unknown
class MyApplication : MyBaseApplication() {
  @Inject lateinit var bar: Bar

  override fun onCreate() {
    super.onCreate()

    val myComponent =
        DaggerMyComponent
            .builder()
            ...
            .build()

    myComponent.inject(this)
  }
}
```

---

## Gradle Build Setup

**URL:** https://dagger.dev/hilt/gradle-setup

**Contents:**
- Gradle Build Setup
- Hilt dependencies
- Using Hilt with Kotlin
- Hilt Gradle plugin
  - Apply Hilt Gradle Plugin with Plugins DSL
  - Why use the plugin?
  - Aggregating Task
  - Applying other processor arguments
  - Local test configuration (AGP < 4.2 only)
  - Classpath Aggregation (Deprecated)

To use Hilt, add the following build dependencies to the Android Gradle module’s build.gradle file:

If using Kotlin, then apply the kapt plugin and declare the compiler dependency using kapt instead of annotationProcessor.

Additionally configure kapt to correct error types by setting correctErrorTypes to true.

The Hilt Gradle plugin runs a bytecode transformation to make the APIs easier to use. The plugin was created for a better developer experience in the IDE since the generated class can disrupt code completion for methods on the base class. The examples throughout the docs will assume usage of the plugin. To configure the Hilt Gradle plugin first declare the dependency in your project’s root build.gradle file:

then in the build.gradle of your Android Gradle modules apply the plugin:

To configure the Hilt Gradle plugin with Gradle’s new plugins DSL , add the plugin id in your project’s root build.gradle file:

then apply the plugin in the build.gradle of your Android Gradle modules:

Warning: The Hilt Gradle plugin sets annotation processor arguments. If you are using other libraries that require annotation processor arguments, make sure you are adding arguments instead of overriding them. See below for an example.

One benefit of the Gradle plugin is that it makes using @AndroidEntryPoint and @HiltAndroidApp easier because it avoids the need to reference Hilt’s generated classes.

Without the Gradle plugin, the base class must be specified in the annotation and the annotated class must extend the generated class:

With the Gradle plugin the annotated class can extend the base class directly:

The Hilt Gradle plugin offers an option for performing Hilt’s classpath aggregation in a dedicated Gradle task. This allows the Hilt annotation processors to be isolating so they are only invoked when necessary. This reduces incremental compilation times by reducing how often an incremental change causes a rebuild of the Dagger components. Enabling this option also enables sharing test components and classpath aggregation. Note that this option replaces enableExperimentalClasspathAggregation since it has the same benefits without any of its caveats.

To enable the aggregating task, apply the following configuration in your Android module’s build.gradle:

The Hilt Gradle plugin sets annotation processor arguments. If you are using other libraries that require annotation processor arguments, make sure you are adding arguments instead of overriding them.

For example, the following notably uses += to avoid overriding the Hilt arguments.

If the + is missing and arguments are overridden, it is likely Hilt will fail to compile with errors like the following: Expected @HiltAndroidApp to have a value. Did you forget to apply the Gradle Plugin?

Warning: This flag should only be used with AGP < 4.2. Newer versions of AGP no longer need this flag.

When the Android Gradle plugin (AGP) version used in the project is less than 4.2, then the Hilt Gradle plugin by default, will only transform instrumented test classes (usually located in the androidTest source folder), but an additional configuration is required for the plugin to transform local jvm tests (usually located in the test source folder).

To enable transforming @AndroidEntryPoint classes in local jvm tests, apply the following configuration in your module’s build.gradle:

Note that the enableTransformForLocalTests configuration only works when running from the command line, e.g. ./gradlew test. It does not work when running tests with Android Studio (via the play button in the test method or class). There are a few options to work around the issue.

The first option is to upgrade the AGP version in your project to 4.2+.

The second option, is to create your own Android Studio configuration that executes tests via the Gradle task. To do this, create a new ‘Run Configuration’ of type ‘Gradle’ from within Android Studio with the following parameters:

As an example, see the setup below:

Warning: This flag is deprecated and will be removed in a future release of Dagger. Use enableAggregatingTask instead.

The Hilt Gradle plugin also offers an experimental option for configuring the compile classpath for annotation processing such that Hilt and Dagger are able to traverse and inspect classes across all transitive dependencies from within the application Gradle module. We recommend enabling this option because without it, an implementation dependency may drop important information about @InstallIn modules or @EntryPoint interfaces from the compile classpath. This can lead to subtle and/or confusing errors, that in the case of multibindings may only manifest at runtime. With this option enabled, implementation dependencies don’t have to be relaxed to api. Note that this option might have a build performance impact due to an increase in compilation classpath. For more context on the problems this solves, see issues #1991 and #970.

Warning: If the Android Gradle plugin version used in the project is less than 7.0 then android.lintOptions.checkReleaseBuilds has to be set to false when enableExperimentalClasspathAggregation is set to true due to an existing bug in prior versions of AGP.

To enable classpath aggregation, apply the following configuration in your Android module’s build.gradle:

**Examples:**

Example 1 (unknown):
```unknown
dependencies {
  implementation 'com.google.dagger:hilt-android:2.57.2'
  annotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'

  // For instrumentation tests
  androidTestImplementation  'com.google.dagger:hilt-android-testing:2.57.2'
  androidTestAnnotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'

  // For local unit tests
  testImplementation 'com.google.dagger:hilt-android-testing:2.57.2'
  testAnnotationProcessor 'com.google.dagger:hilt-compiler:2.57.2'
}
```

Example 2 (unknown):
```unknown
dependencies {
  implementation 'com.google.dagger:hilt-android:2.57.2'
  kapt 'com.google.dagger:hilt-compiler:2.57.2'

  // For instrumentation tests
  androidTestImplementation  'com.google.dagger:hilt-android-testing:2.57.2'
  kaptAndroidTest 'com.google.dagger:hilt-compiler:2.57.2'

  // For local unit tests
  testImplementation 'com.google.dagger:hilt-android-testing:2.57.2'
  kaptTest 'com.google.dagger:hilt-compiler:2.57.2'
}

kapt {
 correctErrorTypes true
}
```

Example 3 (unknown):
```unknown
buildscript {
  repositories {
    // other repositories...
    mavenCentral()
  }
  dependencies {
    // other plugins...
    classpath 'com.google.dagger:hilt-android-gradle-plugin:2.57.2'
  }
}
```

Example 4 (unknown):
```unknown
apply plugin: 'com.android.application'
apply plugin: 'com.google.dagger.hilt.android'

android {
  // ...
}
```

---
