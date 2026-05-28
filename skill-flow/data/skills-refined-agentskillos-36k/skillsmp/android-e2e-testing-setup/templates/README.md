# Android Instrumented Tests

This directory contains end-to-end (E2E) tests for the Android app using Espresso.

## Overview

Instrumented tests run on an Android device or emulator and can interact with the UI, test navigation, and verify app behavior end-to-end.

## Running Tests

### Locally with Connected Device/Emulator

```bash
# Run all instrumented tests
./gradlew connectedAndroidTest

# Run tests for specific build variant
./gradlew connectedDebugAndroidTest
./gradlew connectedReleaseAndroidTest

# Run specific test class
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.ExampleInstrumentedTest

# Run specific test method
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.ExampleInstrumentedTest#appLaunches

# Run with test orchestrator (better isolation, slower)
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.useTestOrchestrator=true

# View HTML test report after running
open app/build/reports/androidTests/connected/index.html
```

### In Android Studio

1. Right-click on test file or test method
2. Select "Run '<test name>'"
3. View results in Run window

### In CI/CD

Tests run automatically on pull requests via GitHub Actions.
See `.github/workflows/android-test.yml` for configuration.

## Test Structure

```
androidTest/
├── base/
│   └── BaseTest.kt           # Common test setup and utilities
├── screens/
│   ├── MainActivityTest.kt   # Tests for MainActivity
│   └── ...                   # Other screen-specific tests
├── utils/
│   ├── TestUtils.kt          # Test helper functions
│   └── ScreenshotUtil.kt     # Screenshot capture utilities
└── ExampleInstrumentedTest.kt # Smoke tests
```

## Test Categories

### Smoke Tests (`ExampleInstrumentedTest.kt`)
- Verify app launches without crashing
- Check basic app structure
- Fast tests that run on every commit
- Should complete in < 10 seconds

### Screen Tests (`screens/`)
- Test specific screens and their interactions
- Verify navigation between screens
- Test user input and form validation
- Check data display and updates

### Integration Tests
- Test multiple screens working together
- Verify end-to-end user flows
- Test data persistence across screens
- Check background operations

## Writing Tests

### Basic Test Structure

```kotlin
@RunWith(AndroidJUnit4::class)
class MyTest : BaseTest() {
    
    @get:Rule
    val activityRule = ActivityScenarioRule(MyActivity::class.java)
    
    @Test
    fun myTest() {
        // Arrange: Set up test conditions
        
        // Act: Perform actions
        onView(withId(R.id.button))
            .perform(click())
        
        // Assert: Verify results
        onView(withId(R.id.result))
            .check(matches(withText("Expected")))
    }
}
```

### Common Espresso Actions

```kotlin
// Click
onView(withId(R.id.button)).perform(click())

// Type text
onView(withId(R.id.editText))
    .perform(typeText("Hello"), closeSoftKeyboard())

// Scroll
onView(withId(R.id.scrollView)).perform(scrollTo())

// Swipe
onView(withId(R.id.view)).perform(swipeLeft())

// Replace text
onView(withId(R.id.editText)).perform(replaceText("New text"))
```

### Common Espresso Assertions

```kotlin
// Check displayed
onView(withId(R.id.view)).check(matches(isDisplayed()))

// Check text
onView(withId(R.id.textView)).check(matches(withText("Expected")))

// Check enabled/disabled
onView(withId(R.id.button)).check(matches(isEnabled()))
onView(withId(R.id.button)).check(matches(not(isEnabled())))

// Check checked (checkbox/radio)
onView(withId(R.id.checkbox)).check(matches(isChecked()))

// Check doesn't exist
onView(withId(R.id.view)).check(doesNotExist())
```

### Custom Matchers

Use `TestUtils` for custom matchers:

```kotlin
// Match view at specific position
onView(withPosition(3)).check(matches(isDisplayed()))

// Match RecyclerView item
onView(withRecyclerView(R.id.recyclerView).atPosition(5))
    .check(matches(hasDescendant(withText("Item 5"))))
```

## Best Practices

### 1. Keep Tests Fast
- Each test should complete in < 5 seconds
- Use `waitForIdle()` instead of `Thread.sleep()`
- Disable animations in test environment
- Use test data instead of network calls

### 2. Make Tests Isolated
- Each test should be independent
- Don't rely on test execution order
- Clean up state in `@After` method
- Use test orchestrator for complete isolation

### 3. Use Descriptive Names
```kotlin
@Test
fun whenUserClicksLoginButton_andCredentialsAreValid_thenNavigatesToHome() {
    // Test implementation
}
```

### 4. Follow AAA Pattern
- **Arrange**: Set up test conditions
- **Act**: Perform the action being tested
- **Assert**: Verify the expected outcome

### 5. Test Real User Flows
- Test how users actually interact with the app
- Include error cases and edge cases
- Test both success and failure scenarios
- Verify error messages and validation

### 6. Use Page Object Pattern
For complex screens, create helper classes:

```kotlin
class LoginScreen {
    fun enterUsername(username: String) {
        onView(withId(R.id.username))
            .perform(typeText(username), closeSoftKeyboard())
    }
    
    fun clickLogin() {
        onView(withId(R.id.loginButton)).perform(click())
    }
    
    fun verifyErrorDisplayed(message: String) {
        onView(withId(R.id.errorText))
            .check(matches(withText(message)))
    }
}
```

## Troubleshooting

### "No tests found"
- Check package names match between main and androidTest
- Verify test runner is configured in build.gradle
- Ensure test methods have `@Test` annotation
- Check test class is public

### "ViewMatchers not found"
- Ensure Espresso dependencies are in build.gradle
- Sync Gradle files
- Invalidate caches and restart Android Studio

### "AmbiguousViewMatcherException"
- Multiple views match the matcher
- Use more specific matchers (combine with `allOf()`)
- Add unique IDs to views in layouts
- Use `withParent()` or `withContentDescription()`

### "PerformException: Error performing 'click'"
- View might not be visible
- Check if view is enabled
- Wait for animations to complete
- Use `scrollTo()` if view is off-screen

### "Tests pass locally but fail in CI"
- Disable animations in emulator settings
- Check API level matches between local and CI
- Verify emulator has enough resources
- Check for race conditions and timing issues

### "Tests are flaky"
- Use Espresso idling resources for async operations
- Avoid `Thread.sleep()`, use `waitForIdle()`
- Enable test orchestrator for better isolation
- Check for race conditions

## Debugging Tests

### 1. Screenshots
Use `ScreenshotUtil` to capture screenshots:

```kotlin
@Test
fun myTest() {
    // ... test code ...
    ScreenshotUtil.capture("test_state")
    // ... more test code ...
}
```

### 2. Test Watcher for Failures
Add to test class:

```kotlin
@get:Rule
val screenshotRule = object : TestWatcher() {
    override fun failed(e: Throwable?, description: Description) {
        ScreenshotUtil.captureOnFailure(description.methodName, true)
    }
}
```

### 3. Layout Inspector
Use Android Studio's Layout Inspector during test execution to see view hierarchy.

### 4. Verbose Logging
Enable verbose Espresso logging:

```kotlin
adb shell setprop log.tag.ViewInteraction VERBOSE
```

## Resources

- [Espresso Documentation](https://developer.android.com/training/testing/espresso)
- [Espresso Cheat Sheet](https://developer.android.com/training/testing/espresso/cheat-sheet)
- [Testing on Android](https://developer.android.com/training/testing)
- [AndroidX Test](https://developer.android.com/training/testing/set-up-project)
- [Test Samples](https://github.com/android/testing-samples)

## CI/CD Configuration

Tests automatically run in GitHub Actions on:
- Pull requests to main/develop
- Pushes to main/develop

Configuration: `.github/workflows/android-test.yml`

Results are uploaded as artifacts and can be viewed in the Actions tab.
