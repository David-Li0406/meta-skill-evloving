# Hilt - Android

**Pages:** 6

---

## Optional inject

**URL:** https://dagger.dev/hilt/optional-inject.html

**Contents:**
- Optional inject
- Why would you need optional injection?
- How to use @OptionalInject

Hilt fragments need to be attached to Hilt activities and Hilt activities need to be attached to Hilt applications. While this is a natural restriction for pure Hilt codebases, it may be an issue during a migration to Hilt if you have a fragment or activity that is used in a non-Hilt context. For example, say you want to migrate a fragment to Hilt but it is used in too many places to migrate at once. Without optional injection, you would have to migrate every activity that uses that fragment to Hilt first otherwise the fragment will crash when looking for the Hilt components when it is trying to inject itself. Depending on the size of your codebase, this could be a large undertaking.

If you mark an @AndroidEntryPoint class with @OptionalInject then it will only try to inject if the parent is using Hilt and not require it. Using this annotation will also cause a wasInjectedByHilt() method to be generated on the generated base class that returns true if it was successful injecting.

Note: Because API generated on the base class is inaccessible to users of the gradle plugin, there is an alternative API to access this functionality using a static helper method in OptionalInjectCheck.

This gives you the chance to provide dependencies in a different way (usually whichever way you were getting dependencies before using Hilt).

Note that for activities, because Hilt injection is usually run as a part of super.onCreate() and it is recommended to do your own injection before fragments are restored which also happens during super.onCreate(), you likely need to use an OnContextAvailableListener to run your non-Hilt injection code. Hilt uses the same listener under the hood, so then the order would be Hilt’s OnContextAvailableListener would run, then yours, then fragments would be restored.

**Examples:**

Example 1 (java):
```java
@OptionalInject
@AndroidEntryPoint
public final class MyFragment extends Fragment {

  @Inject Foo foo;

  @Override public void onAttach(Activity activity) {
    super.onAttach(activity);  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 2 (unknown):
```unknown
@OptionalInject
@AndroidEntryPoint
public final class MyFragment extends Fragment {

  @Inject Foo foo;

  @Override public void onAttach(Activity activity) {
    super.onAttach(activity);  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 3 (kotlin):
```kotlin
@OptionalInject
@AndroidEntryPoint
class MyFragment : Fragment() {

  @Inject lateinit var foo: Foo

  override fun onAttach(activity: Activity) {
    super.onAttach(activity)  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 4 (unknown):
```unknown
@OptionalInject
@AndroidEntryPoint
class MyFragment : Fragment() {

  @Inject lateinit var foo: Foo

  override fun onAttach(activity: Activity) {
    super.onAttach(activity)  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

---

## Android Entry Points

**URL:** https://dagger.dev/hilt/android-entry-point.html

**Contents:**
- Android Entry Points
- Android types
  - Retained Fragments
  - Views with Fragment bindings

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

Once you have enabled members injection in your Application, you can start enabling members injection in your other Android classes using the @AndroidEntryPoint annotation. You can use @AndroidEntryPoint on the following types:

Note that ViewModels are supported via a separate API @HiltViewModel. ContentProviders are not directly supported due to their onCreate being called at startup, but you can access dependencies via an entry point.

The following example shows how to add the annotation to an activity, but the process is the same for other types. When adding to other types, note that as a general rule, Hilt types need to be attached to other Hilt types to work. So before adding [@AndroidEntryPoint] to a fragment, the activity must be annotated as well.

To enable members injection in your activity, annotate your class with @AndroidEntryPoint.

Note: Hilt currently only supports activities that extend ComponentActivity and fragments that extend androidx library Fragment, not the (now deprecated) Fragment in the Android platform.

Calling setRetainInstance(true) in a Fragment’s onCreate method will keep a fragment instance across configuration changes (instead of destroying and recreating it).

A Hilt fragment should never be retained because it holds a reference to the component (responsible for injection), and that component holds references to the previous Activity instance. In addition, scoped bindings and providers that are injected into the fragment can also cause memory leaks if a Hilt fragment is retained. To prevent Hilt fragments from being retained, a runtime exception will be thrown on configuration change if a retained Hilt fragment is detected.

A non-Hilt fragment can be retained, even if attached to a Hilt activity. However, if that fragment contains a Hilt child fragment, a runtime exception will be thrown when a configuration change occurs.

Note: While it’s not recommended, Hilt fragments can be detached and reattached to the same activity instance. In this case, the Hilt fragment will only be injected on the first call to onAttach. Note that this is not the same as retaining a fragment, because a retained fragment will be reattached to a different instance of the activity. Again, this is not recommended, and it is often less confusing to just create a new fragment instance for each usage.

By default, only SingletonComponent and ActivityComponent bindings can be injected into the view. To enable fragment bindings in your view, add the @WithFragmentBindings annotation to your class.

Unlike the other supported Android classes, BroadcastReceivers do not have their own Dagger component and are instead simply injected from the SingletonComponent. ↩

**Examples:**

Example 1 (java):
```java
@AndroidEntryPoint
public final class MyActivity extends MyBaseActivity {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject Bar bar;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    // Injection happens in super.onCreate().
    super.onCreate();

    // Do something with bar ...
  }
}
```

Example 2 (unknown):
```unknown
@AndroidEntryPoint
public final class MyActivity extends MyBaseActivity {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject Bar bar;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    // Injection happens in super.onCreate().
    super.onCreate();

    // Do something with bar ...
  }
}
```

Example 3 (kotlin):
```kotlin
@AndroidEntryPoint
class MyActivity : MyBaseActivity() {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject lateinit var bar: Bar

  override fun onCreate(savedInstanceState: Bundle?) {
    // Injection happens in super.onCreate().
    super.onCreate()

    // Do something with bar ...
  }
}
```

Example 4 (unknown):
```unknown
@AndroidEntryPoint
class MyActivity : MyBaseActivity() {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject lateinit var bar: Bar

  override fun onCreate(savedInstanceState: Bundle?) {
    // Injection happens in super.onCreate().
    super.onCreate()

    // Do something with bar ...
  }
}
```

---

## View Models

**URL:** https://dagger.dev/hilt/view-model.html

**Contents:**
- View Models
- Hilt View Models
- View Model Scope
- Assisted Injection

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

A Hilt View Model is a Jetpack ViewModel that is constructor injected by Hilt. To enable injection of a ViewModel by Hilt use the @HiltViewModel annotation:

Then an activity or fragments annotated with @AndroidEntryPoint can get the ViewModel instance as normal using ViewModelProvider or the by viewModels() KTX extension:

Warning: Even though the view model has an @Inject constructor, it is an error to request it from Dagger directly (for example, via field injection) since that would result in multiple instances. View Models must be retrieved through the ViewModelProvider API. This is checked at compile time by Hilt.

Only dependencies from the ViewModelComponent and its parent components can be provided into the ViewModel.

The ViewModelComponent also comes with two default bindings available:

All Hilt View Models are provided by the ViewModelComponent which follows the same lifecycle as a ViewModel, i.e. it survives configuration changes. To scope a dependency to a ViewModel use the @ViewModelScoped annotation.

A @ViewModelScoped type will make it so that a single instance of the scoped type is provided across all dependencies injected into the Hilt View Model. Other instances of a ViewModel that requests the scoped instance will receive a different instance. Scoping to the ViewModelComponent allows for flexible and granular scope since View Models survive configuration changes and their lifecycle is controlled by the activity or fragment. If a single instance needs to be shared across various View Models then it should be scoped using either @ActivityRetainedScoped or @Singleton.

For example, we can scope a dependency to be shared within a single ViewModel as such:

Hilt View Models can also be assisted injected. Compared to using SavedStateHandle, this enables passing data that are not Parcelable to a Hilt View Model easily. To use assisted injection, annotate the view model constructor with @AssistedInject and the assisted parameters with @Assisted, and specify the assisted factory in the @HiltViewModel annotation:

Note: Unlike SavedStateHandle, the values passed through assisted parameters to a Hilt View Model do not get saved to disk. They have the same scope as the view model and do not persist after the lifecycle of the view model has ended, e.g. containing activity gets popped off the stack or process death. Consider using normal injection with SavedStateHandle instead or other mechanisms if persistence is needed.

Next, define the assisted factory with an abstract factory method that returns the view model:

Note: It is an error to request the assisted factory for view models from Dagger directly since the factory may be used to create view model instances that are not stored correctly. This is checked at compile time by Hilt.

Finally, pass a callback to the helper function HiltViewModelExtensions.withCreationCallback() to create a CreationExtras that can be used with the ViewModelProvider API or other view model functions like by viewModels(). Use the passed in factory to create a view model instance inside the callback:

Warning: Do not pass any objects that have a smaller lifecycle than the view model (e.g. an Activity, Fragment, or View) or any objects that reference them to the assisted factory as that would be leaking them.

Note: Unlike normal @AssistedInject types, a Hilt View Models, like all View Models, are memoized by the owner. Once a Hilt View Model instance has been created, the callback will be ignored as long as the view model’s lifecycle has not ended. For example, Hilt does not call the callback to create a new view model instance after configuration changes, nor will it update the values of assisted parameters in the existing view model instances.

**Examples:**

Example 1 (java):
```java
@HiltViewModel
public final class FooViewModel extends ViewModel {

  @Inject
  FooViewModel(SavedStateHandle handle, Foo foo) {
    // ...
  }
}
```

Example 2 (unknown):
```unknown
@HiltViewModel
public final class FooViewModel extends ViewModel {

  @Inject
  FooViewModel(SavedStateHandle handle, Foo foo) {
    // ...
  }
}
```

Example 3 (kotlin):
```kotlin
@HiltViewModel
class FooViewModel @Inject constructor(
  val handle: SavedStateHandle,
  val foo: Foo
) : ViewModel()
```

Example 4 (unknown):
```unknown
@HiltViewModel
class FooViewModel @Inject constructor(
  val handle: SavedStateHandle,
  val foo: Foo
) : ViewModel()
```

---

## Android Entry Points

**URL:** https://dagger.dev/hilt/android-entry-point

**Contents:**
- Android Entry Points
- Android types
  - Retained Fragments
  - Views with Fragment bindings

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

Once you have enabled members injection in your Application, you can start enabling members injection in your other Android classes using the @AndroidEntryPoint annotation. You can use @AndroidEntryPoint on the following types:

Note that ViewModels are supported via a separate API @HiltViewModel. ContentProviders are not directly supported due to their onCreate being called at startup, but you can access dependencies via an entry point.

The following example shows how to add the annotation to an activity, but the process is the same for other types. When adding to other types, note that as a general rule, Hilt types need to be attached to other Hilt types to work. So before adding [@AndroidEntryPoint] to a fragment, the activity must be annotated as well.

To enable members injection in your activity, annotate your class with @AndroidEntryPoint.

Note: Hilt currently only supports activities that extend ComponentActivity and fragments that extend androidx library Fragment, not the (now deprecated) Fragment in the Android platform.

Calling setRetainInstance(true) in a Fragment’s onCreate method will keep a fragment instance across configuration changes (instead of destroying and recreating it).

A Hilt fragment should never be retained because it holds a reference to the component (responsible for injection), and that component holds references to the previous Activity instance. In addition, scoped bindings and providers that are injected into the fragment can also cause memory leaks if a Hilt fragment is retained. To prevent Hilt fragments from being retained, a runtime exception will be thrown on configuration change if a retained Hilt fragment is detected.

A non-Hilt fragment can be retained, even if attached to a Hilt activity. However, if that fragment contains a Hilt child fragment, a runtime exception will be thrown when a configuration change occurs.

Note: While it’s not recommended, Hilt fragments can be detached and reattached to the same activity instance. In this case, the Hilt fragment will only be injected on the first call to onAttach. Note that this is not the same as retaining a fragment, because a retained fragment will be reattached to a different instance of the activity. Again, this is not recommended, and it is often less confusing to just create a new fragment instance for each usage.

By default, only SingletonComponent and ActivityComponent bindings can be injected into the view. To enable fragment bindings in your view, add the @WithFragmentBindings annotation to your class.

Unlike the other supported Android classes, BroadcastReceivers do not have their own Dagger component and are instead simply injected from the SingletonComponent. ↩

**Examples:**

Example 1 (java):
```java
@AndroidEntryPoint
public final class MyActivity extends MyBaseActivity {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject Bar bar;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    // Injection happens in super.onCreate().
    super.onCreate();

    // Do something with bar ...
  }
}
```

Example 2 (unknown):
```unknown
@AndroidEntryPoint
public final class MyActivity extends MyBaseActivity {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject Bar bar;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    // Injection happens in super.onCreate().
    super.onCreate();

    // Do something with bar ...
  }
}
```

Example 3 (kotlin):
```kotlin
@AndroidEntryPoint
class MyActivity : MyBaseActivity() {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject lateinit var bar: Bar

  override fun onCreate(savedInstanceState: Bundle?) {
    // Injection happens in super.onCreate().
    super.onCreate()

    // Do something with bar ...
  }
}
```

Example 4 (unknown):
```unknown
@AndroidEntryPoint
class MyActivity : MyBaseActivity() {
  // Bindings in SingletonComponent or ActivityComponent
  @Inject lateinit var bar: Bar

  override fun onCreate(savedInstanceState: Bundle?) {
    // Injection happens in super.onCreate().
    super.onCreate()

    // Do something with bar ...
  }
}
```

---

## View Models

**URL:** https://dagger.dev/hilt/view-model

**Contents:**
- View Models
- Hilt View Models
- View Model Scope
- Assisted Injection

Note: Examples on this page assume usage of the Gradle plugin. If you are not using the plugin, please read this page for details.

A Hilt View Model is a Jetpack ViewModel that is constructor injected by Hilt. To enable injection of a ViewModel by Hilt use the @HiltViewModel annotation:

Then an activity or fragments annotated with @AndroidEntryPoint can get the ViewModel instance as normal using ViewModelProvider or the by viewModels() KTX extension:

Warning: Even though the view model has an @Inject constructor, it is an error to request it from Dagger directly (for example, via field injection) since that would result in multiple instances. View Models must be retrieved through the ViewModelProvider API. This is checked at compile time by Hilt.

Only dependencies from the ViewModelComponent and its parent components can be provided into the ViewModel.

The ViewModelComponent also comes with two default bindings available:

All Hilt View Models are provided by the ViewModelComponent which follows the same lifecycle as a ViewModel, i.e. it survives configuration changes. To scope a dependency to a ViewModel use the @ViewModelScoped annotation.

A @ViewModelScoped type will make it so that a single instance of the scoped type is provided across all dependencies injected into the Hilt View Model. Other instances of a ViewModel that requests the scoped instance will receive a different instance. Scoping to the ViewModelComponent allows for flexible and granular scope since View Models survive configuration changes and their lifecycle is controlled by the activity or fragment. If a single instance needs to be shared across various View Models then it should be scoped using either @ActivityRetainedScoped or @Singleton.

For example, we can scope a dependency to be shared within a single ViewModel as such:

Hilt View Models can also be assisted injected. Compared to using SavedStateHandle, this enables passing data that are not Parcelable to a Hilt View Model easily. To use assisted injection, annotate the view model constructor with @AssistedInject and the assisted parameters with @Assisted, and specify the assisted factory in the @HiltViewModel annotation:

Note: Unlike SavedStateHandle, the values passed through assisted parameters to a Hilt View Model do not get saved to disk. They have the same scope as the view model and do not persist after the lifecycle of the view model has ended, e.g. containing activity gets popped off the stack or process death. Consider using normal injection with SavedStateHandle instead or other mechanisms if persistence is needed.

Next, define the assisted factory with an abstract factory method that returns the view model:

Note: It is an error to request the assisted factory for view models from Dagger directly since the factory may be used to create view model instances that are not stored correctly. This is checked at compile time by Hilt.

Finally, pass a callback to the helper function HiltViewModelExtensions.withCreationCallback() to create a CreationExtras that can be used with the ViewModelProvider API or other view model functions like by viewModels(). Use the passed in factory to create a view model instance inside the callback:

Warning: Do not pass any objects that have a smaller lifecycle than the view model (e.g. an Activity, Fragment, or View) or any objects that reference them to the assisted factory as that would be leaking them.

Note: Unlike normal @AssistedInject types, a Hilt View Models, like all View Models, are memoized by the owner. Once a Hilt View Model instance has been created, the callback will be ignored as long as the view model’s lifecycle has not ended. For example, Hilt does not call the callback to create a new view model instance after configuration changes, nor will it update the values of assisted parameters in the existing view model instances.

**Examples:**

Example 1 (java):
```java
@HiltViewModel
public final class FooViewModel extends ViewModel {

  @Inject
  FooViewModel(SavedStateHandle handle, Foo foo) {
    // ...
  }
}
```

Example 2 (unknown):
```unknown
@HiltViewModel
public final class FooViewModel extends ViewModel {

  @Inject
  FooViewModel(SavedStateHandle handle, Foo foo) {
    // ...
  }
}
```

Example 3 (kotlin):
```kotlin
@HiltViewModel
class FooViewModel @Inject constructor(
  val handle: SavedStateHandle,
  val foo: Foo
) : ViewModel()
```

Example 4 (unknown):
```unknown
@HiltViewModel
class FooViewModel @Inject constructor(
  val handle: SavedStateHandle,
  val foo: Foo
) : ViewModel()
```

---

## Optional inject

**URL:** https://dagger.dev/hilt/optional-inject

**Contents:**
- Optional inject
- Why would you need optional injection?
- How to use @OptionalInject

Hilt fragments need to be attached to Hilt activities and Hilt activities need to be attached to Hilt applications. While this is a natural restriction for pure Hilt codebases, it may be an issue during a migration to Hilt if you have a fragment or activity that is used in a non-Hilt context. For example, say you want to migrate a fragment to Hilt but it is used in too many places to migrate at once. Without optional injection, you would have to migrate every activity that uses that fragment to Hilt first otherwise the fragment will crash when looking for the Hilt components when it is trying to inject itself. Depending on the size of your codebase, this could be a large undertaking.

If you mark an @AndroidEntryPoint class with @OptionalInject then it will only try to inject if the parent is using Hilt and not require it. Using this annotation will also cause a wasInjectedByHilt() method to be generated on the generated base class that returns true if it was successful injecting.

Note: Because API generated on the base class is inaccessible to users of the gradle plugin, there is an alternative API to access this functionality using a static helper method in OptionalInjectCheck.

This gives you the chance to provide dependencies in a different way (usually whichever way you were getting dependencies before using Hilt).

Note that for activities, because Hilt injection is usually run as a part of super.onCreate() and it is recommended to do your own injection before fragments are restored which also happens during super.onCreate(), you likely need to use an OnContextAvailableListener to run your non-Hilt injection code. Hilt uses the same listener under the hood, so then the order would be Hilt’s OnContextAvailableListener would run, then yours, then fragments would be restored.

**Examples:**

Example 1 (java):
```java
@OptionalInject
@AndroidEntryPoint
public final class MyFragment extends Fragment {

  @Inject Foo foo;

  @Override public void onAttach(Activity activity) {
    super.onAttach(activity);  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 2 (unknown):
```unknown
@OptionalInject
@AndroidEntryPoint
public final class MyFragment extends Fragment {

  @Inject Foo foo;

  @Override public void onAttach(Activity activity) {
    super.onAttach(activity);  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 3 (kotlin):
```kotlin
@OptionalInject
@AndroidEntryPoint
class MyFragment : Fragment() {

  @Inject lateinit var foo: Foo

  override fun onAttach(activity: Activity) {
    super.onAttach(activity)  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

Example 4 (unknown):
```unknown
@OptionalInject
@AndroidEntryPoint
class MyFragment : Fragment() {

  @Inject lateinit var foo: Foo

  override fun onAttach(activity: Activity) {
    super.onAttach(activity)  // Injection will happen here, but only if the Activity used Hilt
    if (!OptionalInjectCheck.wasInjectedByHilt(this)) {
      // Get Dagger components the previous way and inject
    }
  }
}
```

---
