package {PACKAGE_NAME}.base

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import androidx.test.espresso.Espresso
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.rule.GrantPermissionRule
import org.junit.After
import org.junit.Before
import org.junit.Rule

/**
 * Base class for all instrumented tests.
 * Provides common setup, teardown, and utilities.
 * 
 * Usage:
 * ```
 * class MyTest : BaseTest() {
 *     @get:Rule
 *     val activityRule = ActivityScenarioRule(MyActivity::class.java)
 *     
 *     @Test
 *     fun myTest() {
 *         // Test implementation
 *     }
 * }
 * ```
 */
abstract class BaseTest {
    
    /**
     * Grants common dangerous permissions for testing.
     * Override in subclass if different permissions needed.
     * 
     * Remove or modify permissions based on your app's requirements.
     */
    @get:Rule
    val permissionRule: GrantPermissionRule = GrantPermissionRule.grant(
        android.Manifest.permission.CAMERA,
        android.Manifest.permission.ACCESS_FINE_LOCATION,
        android.Manifest.permission.READ_EXTERNAL_STORAGE,
        android.Manifest.permission.WRITE_EXTERNAL_STORAGE
    )
    
    /**
     * Application context for accessing resources.
     */
    protected val context: Context by lazy {
        InstrumentationRegistry.getInstrumentation().targetContext
    }
    
    /**
     * Application instance (if you have a custom Application class).
     */
    protected val application: Context by lazy {
        ApplicationProvider.getApplicationContext()
    }
    
    @Before
    open fun setUp() {
        // Common setup for all tests
        // Override in subclass for test-specific setup
    }
    
    @After
    open fun tearDown() {
        // Common cleanup
        // Screenshots on failure handled by test runner
    }
    
    /**
     * Wait for Espresso to be idle (animations complete, AsyncTasks done).
     * Prefer this over Thread.sleep() for more reliable tests.
     */
    protected fun waitForIdle() {
        Espresso.onIdle()
    }
    
    /**
     * Force wait (use sparingly, prefer waitForIdle()).
     * Only use when you specifically need to wait for non-Espresso operations.
     */
    protected fun wait(millis: Long = 1000) {
        Thread.sleep(millis)
    }
    
    /**
     * Get string resource for testing.
     */
    protected fun getString(resId: Int): String {
        return context.getString(resId)
    }
    
    /**
     * Get string resource with format args.
     */
    protected fun getString(resId: Int, vararg formatArgs: Any): String {
        return context.getString(resId, *formatArgs)
    }
}
