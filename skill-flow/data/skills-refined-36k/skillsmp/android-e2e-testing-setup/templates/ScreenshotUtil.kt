package {PACKAGE_NAME}.utils

import android.graphics.Bitmap
import androidx.test.runner.screenshot.Screenshot
import java.io.File
import java.io.FileOutputStream

/**
 * Utility for capturing screenshots during test failures.
 * 
 * Screenshots are automatically saved to device storage and can be
 * uploaded as artifacts in CI/CD for debugging failed tests.
 * 
 * Usage in test class:
 * ```
 * @get:Rule
 * val screenshotRule = object : TestWatcher() {
 *     override fun failed(e: Throwable?, description: Description) {
 *         ScreenshotUtil.captureOnFailure(description.methodName, true)
 *     }
 * }
 * ```
 */
object ScreenshotUtil {
    
    /**
     * Capture screenshot with given name.
     * 
     * @param name Name for the screenshot file (without extension)
     */
    fun capture(name: String) {
        try {
            val screenshot = Screenshot.capture()
            screenshot.name = sanitizeFilename(name)
            screenshot.format = Bitmap.CompressFormat.PNG
            
            // Process and save screenshot
            val processors = setOf(screenshot)
            screenshot.process(processors)
            
            println("Screenshot captured: ${screenshot.name}")
        } catch (e: Exception) {
            println("Failed to capture screenshot: ${e.message}")
        }
    }
    
    /**
     * Capture screenshot on test failure.
     * 
     * @param testName Name of the test that failed
     * @param hasFailed Whether the test has failed
     */
    fun captureOnFailure(testName: String, hasFailed: Boolean) {
        if (hasFailed) {
            val timestamp = System.currentTimeMillis()
            capture("failure_${testName}_$timestamp")
        }
    }
    
    /**
     * Capture screenshot before and after an action.
     * Useful for debugging visual regressions.
     * 
     * @param testName Name of the test
     * @param action Action to perform between screenshots
     */
    fun captureBeforeAfter(testName: String, action: () -> Unit) {
        capture("${testName}_before")
        action()
        capture("${testName}_after")
    }
    
    /**
     * Save bitmap to file manually (for more control).
     * 
     * @param bitmap The bitmap to save
     * @param filename Name for the file
     * @param directory Directory to save in (optional)
     */
    fun saveBitmap(
        bitmap: Bitmap,
        filename: String,
        directory: File? = null
    ) {
        val dir = directory ?: File("/sdcard/screenshots/")
        if (!dir.exists()) {
            dir.mkdirs()
        }
        
        val file = File(dir, "${sanitizeFilename(filename)}.png")
        FileOutputStream(file).use { out ->
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
        }
        
        println("Screenshot saved: ${file.absolutePath}")
    }
    
    /**
     * Sanitize filename to remove invalid characters.
     */
    private fun sanitizeFilename(name: String): String {
        return name.replace(Regex("[^a-zA-Z0-9._-]"), "_")
    }
}
