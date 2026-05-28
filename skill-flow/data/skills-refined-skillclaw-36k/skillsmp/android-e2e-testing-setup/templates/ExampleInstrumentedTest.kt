package {PACKAGE_NAME}

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import {PACKAGE_NAME}.base.BaseTest
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Instrumented smoke test to verify app launches successfully.
 * 
 * This is the most basic E2E test - if the app can't launch,
 * all other tests will fail. This should be fast and run on every commit.
 * 
 * Replace {MAIN_ACTIVITY} with your actual main activity class name.
 */
@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest : BaseTest() {
    
    @get:Rule
    val activityRule = ActivityScenarioRule({MAIN_ACTIVITY}::class.java)
    
    /**
     * Verify app package name is correct.
     * Ensures we're testing the right app.
     */
    @Test
    fun appLaunches_correctPackage() {
        assertEquals("{PACKAGE_NAME}", context.packageName)
    }
    
    /**
     * Verify main activity displays without crashing.
     * Replace R.id.{MAIN_VIEW_ID} with an actual view ID from your main layout.
     */
    @Test
    fun mainActivity_displaysContent() {
        // Wait for activity to be fully loaded
        waitForIdle()
        
        // Verify main content is visible
        // TODO: Replace with actual view ID from your layout
        onView(withId(R.id.{MAIN_VIEW_ID}))
            .check(matches(isDisplayed()))
    }
    
    /**
     * Verify app doesn't crash on launch.
     * Simply launching and waiting should not cause crashes.
     */
    @Test
    fun appLaunches_noCrash() {
        // Wait for all async operations to complete
        waitForIdle()
        
        // If we get here without exception, test passes
        // This catches initialization crashes, null pointers, etc.
    }
}
