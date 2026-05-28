package {PACKAGE_NAME}.utils

import android.content.Context
import android.view.View
import android.view.ViewGroup
import androidx.annotation.StringRes
import androidx.test.espresso.matcher.BoundedMatcher
import org.hamcrest.Description
import org.hamcrest.Matcher
import java.util.concurrent.TimeoutException

/**
 * Utility functions for Espresso tests.
 * 
 * These helpers make tests more readable and reduce code duplication.
 */
object TestUtils {
    
    /**
     * Custom matcher to check if a view is at a specific position in its parent.
     * 
     * Usage:
     * ```
     * onView(withPosition(3)).check(matches(isDisplayed()))
     * ```
     */
    fun withPosition(position: Int): Matcher<View> {
        return object : BoundedMatcher<View, View>(View::class.java) {
            override fun describeTo(description: Description) {
                description.appendText("at position $position in parent")
            }
            
            override fun matchesSafely(item: View): Boolean {
                val parent = item.parent
                if (parent is ViewGroup) {
                    return parent.indexOfChild(item) == position
                }
                return false
            }
        }
    }
    
    /**
     * Wait for a condition to be true with timeout.
     * Polls the condition every 100ms until it's true or timeout occurs.
     * 
     * Usage:
     * ```
     * TestUtils.waitUntil { someCondition() }
     * TestUtils.waitUntil(10000) { someSlowCondition() }
     * ```
     * 
     * @param timeoutMillis Maximum time to wait (default 5 seconds)
     * @param condition Lambda that returns true when condition is met
     * @throws TimeoutException if condition not met within timeout
     */
    fun waitUntil(
        timeoutMillis: Long = 5000,
        condition: () -> Boolean
    ) {
        val startTime = System.currentTimeMillis()
        while (!condition()) {
            if (System.currentTimeMillis() - startTime > timeoutMillis) {
                throw TimeoutException(
                    "Condition not met within $timeoutMillis ms"
                )
            }
            Thread.sleep(100)
        }
    }
    
    /**
     * Wait for a view to appear with timeout.
     * Useful for views that appear after async operations.
     * 
     * Usage:
     * ```
     * TestUtils.waitForView(R.id.loading_spinner, visible = false)
     * ```
     */
    fun waitForView(viewId: Int, visible: Boolean = true, timeoutMillis: Long = 5000) {
        waitUntil(timeoutMillis) {
            try {
                onView(withId(viewId)).check(
                    if (visible) matches(isDisplayed())
                    else doesNotExist()
                )
                true
            } catch (e: Exception) {
                false
            }
        }
    }
    
    /**
     * Get string resource for testing.
     * 
     * Usage:
     * ```
     * val expected = TestUtils.getString(context, R.string.welcome_message)
     * onView(withText(expected)).check(matches(isDisplayed()))
     * ```
     */
    fun getString(context: Context, @StringRes resId: Int): String {
        return context.getString(resId)
    }
    
    /**
     * Get string resource with format arguments.
     */
    fun getString(context: Context, @StringRes resId: Int, vararg formatArgs: Any): String {
        return context.getString(resId, *formatArgs)
    }
    
    /**
     * Custom matcher for RecyclerView item at position.
     * 
     * Usage:
     * ```
     * onView(withRecyclerView(R.id.recycler_view).atPosition(3))
     *     .check(matches(hasDescendant(withText("Item 3"))))
     * ```
     */
    fun withRecyclerView(recyclerViewId: Int): RecyclerViewMatcher {
        return RecyclerViewMatcher(recyclerViewId)
    }
}

/**
 * Matcher for RecyclerView items at specific positions.
 */
class RecyclerViewMatcher(private val recyclerViewId: Int) {
    
    fun atPosition(position: Int): Matcher<View> {
        return atPositionOnView(position, -1)
    }
    
    fun atPositionOnView(position: Int, targetViewId: Int): Matcher<View> {
        return object : BoundedMatcher<View, View>(View::class.java) {
            private var childView: View? = null
            
            override fun describeTo(description: Description) {
                description.appendText("RecyclerView with id $recyclerViewId at position $position")
            }
            
            override fun matchesSafely(view: View): Boolean {
                if (childView == null) {
                    val recyclerView = view.rootView.findViewById<androidx.recyclerview.widget.RecyclerView>(
                        recyclerViewId
                    )
                    if (recyclerView?.id == recyclerViewId) {
                        val viewHolder = recyclerView.findViewHolderForAdapterPosition(position)
                        childView = viewHolder?.itemView
                    } else {
                        return false
                    }
                }
                
                if (targetViewId == -1) {
                    return view == childView
                } else {
                    val targetView = childView?.findViewById<View>(targetViewId)
                    return view == targetView
                }
            }
        }
    }
}
