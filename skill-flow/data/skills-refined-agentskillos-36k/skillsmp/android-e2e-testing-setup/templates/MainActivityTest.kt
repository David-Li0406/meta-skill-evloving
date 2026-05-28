package {PACKAGE_NAME}.screens

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import {PACKAGE_NAME}.{MAIN_ACTIVITY}
import {PACKAGE_NAME}.R
import {PACKAGE_NAME}.base.BaseTest
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Tests for {MAIN_ACTIVITY} navigation and interactions.
 * 
 * These tests verify user flows and interactions work correctly.
 * Replace placeholder IDs with actual view IDs from your layouts.
 */
@RunWith(AndroidJUnit4::class)
class MainActivityTest : BaseTest() {
    
    @get:Rule
    val activityRule = ActivityScenarioRule({MAIN_ACTIVITY}::class.java)
    
    /**
     * Test navigation from main screen to another screen.
     * Replace R.id.button_next with your actual button ID.
     */
    @Test
    fun clickButton_navigatesToNextScreen() {
        // Click navigation button
        onView(withId(R.id.button_next))
            .perform(click())
        
        // Wait for navigation to complete
        waitForIdle()
        
        // Verify we're on the next screen
        // Replace R.id.next_screen_title with actual view ID
        onView(withId(R.id.next_screen_title))
            .check(matches(isDisplayed()))
    }
    
    /**
     * Test text input functionality.
     * Replace R.id.edit_text_input with your actual EditText ID.
     */
    @Test
    fun enterText_displaysCorrectly() {
        val testInput = "Test Input Text"
        
        // Type into EditText
        onView(withId(R.id.edit_text_input))
            .perform(typeText(testInput), closeSoftKeyboard())
        
        // Verify text was entered correctly
        onView(withId(R.id.edit_text_input))
            .check(matches(withText(testInput)))
    }
    
    /**
     * Test button click interaction.
     * Replace R.id.button_action with your actual button ID.
     */
    @Test
    fun clickButton_performsAction() {
        // Click action button
        onView(withId(R.id.button_action))
            .perform(click())
        
        // Wait for action to complete
        waitForIdle()
        
        // Verify result of action
        // Replace with actual verification for your app
        onView(withId(R.id.result_text))
            .check(matches(withText("Action completed")))
    }
    
    /**
     * Test scrolling interaction (for RecyclerView/ScrollView).
     * Replace R.id.recycler_view with your actual RecyclerView ID.
     */
    @Test
    fun scrollToItem_itemIsVisible() {
        // Scroll to specific position
        onView(withId(R.id.recycler_view))
            .perform(scrollToPosition<androidx.recyclerview.widget.RecyclerView.ViewHolder>(5))
        
        // Verify item at position is visible
        onView(withText("Item 5"))
            .check(matches(isDisplayed()))
    }
}
