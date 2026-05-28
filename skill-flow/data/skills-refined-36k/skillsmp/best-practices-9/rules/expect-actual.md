# Expect/Actual Rules

## expect-interface - Prefer interfaces over expect/actual

Use interfaces with platform-specific implementations when possible.

### Incorrect

```kotlin
// commonMain
expect class PlatformLogger() {
    fun log(message: String)
    fun error(message: String, throwable: Throwable?)
}

// androidMain
actual class PlatformLogger {
    actual fun log(message: String) = Log.d(TAG, message)
    actual fun error(message: String, throwable: Throwable?) = Log.e(TAG, message, throwable)
}

// iosMain
actual class PlatformLogger {
    actual fun log(message: String) = NSLog(message)
    actual fun error(message: String, throwable: Throwable?) = NSLog("$message: $throwable")
}
```

### Correct

```kotlin
// commonMain
interface Logger {
    fun log(message: String)
    fun error(message: String, throwable: Throwable? = null)
}

expect fun createLogger(): Logger

// androidMain
actual fun createLogger(): Logger = AndroidLogger()

class AndroidLogger : Logger {
    override fun log(message: String) = Log.d(TAG, message)
    override fun error(message: String, throwable: Throwable?) = Log.e(TAG, message, throwable)
}

// iosMain
actual fun createLogger(): Logger = IosLogger()

class IosLogger : Logger {
    override fun log(message: String) = NSLog(message)
    override fun error(message: String, throwable: Throwable?) = NSLog("$message: $throwable")
}
```

---

## expect-minimal - Keep expect declarations minimal

Only use expect/actual for truly platform-specific code.

### Incorrect

```kotlin
// commonMain - too much in expect
expect fun formatDate(timestamp: Long): String
expect fun formatTime(timestamp: Long): String
expect fun formatDateTime(timestamp: Long): String
expect fun parseDate(dateString: String): Long
expect fun parseTime(timeString: String): Long
```

### Correct

```kotlin
// commonMain - minimal expect
expect class DateFormatter() {
    fun format(timestamp: Long, pattern: String): String
    fun parse(dateString: String, pattern: String): Long
}

// Common logic using minimal expect
fun formatDate(timestamp: Long): String = DateFormatter().format(timestamp, "yyyy-MM-dd")
fun formatTime(timestamp: Long): String = DateFormatter().format(timestamp, "HH:mm")
fun formatDateTime(timestamp: Long): String = DateFormatter().format(timestamp, "yyyy-MM-dd HH:mm")

// Or prefer kotlinx-datetime for fully common implementation
import kotlinx.datetime.*

fun formatDate(timestamp: Long): String {
    val instant = Instant.fromEpochMilliseconds(timestamp)
    val dateTime = instant.toLocalDateTime(TimeZone.currentSystemDefault())
    return "${dateTime.year}-${dateTime.monthNumber.toString().padStart(2, '0')}-${dateTime.dayOfMonth.toString().padStart(2, '0')}"
}
```

---

## expect-default - Provide default implementations where appropriate

Use interfaces with default implementations to minimize platform code.

### Correct

```kotlin
// commonMain
interface PlatformCapabilities {
    val hasCamera: Boolean
    val hasBiometrics: Boolean
    val hasNfc: Boolean get() = false  // Default: not available

    fun openUrl(url: String)
    fun shareText(text: String)
    fun vibrate(durationMs: Long) {}  // Default: no-op
}

expect fun createPlatformCapabilities(): PlatformCapabilities

// androidMain - only override what differs
actual fun createPlatformCapabilities(): PlatformCapabilities = AndroidCapabilities()

class AndroidCapabilities(private val context: Context) : PlatformCapabilities {
    override val hasCamera = context.packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA)
    override val hasBiometrics = BiometricManager.from(context).canAuthenticate() == BIOMETRIC_SUCCESS
    override val hasNfc = context.packageManager.hasSystemFeature(PackageManager.FEATURE_NFC)

    override fun openUrl(url: String) {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }

    override fun shareText(text: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, text)
        }
        context.startActivity(Intent.createChooser(intent, "Share"))
    }

    override fun vibrate(durationMs: Long) {
        val vibrator = context.getSystemService<Vibrator>()
        vibrator?.vibrate(VibrationEffect.createOneShot(durationMs, DEFAULT_AMPLITUDE))
    }
}
```

---

## expect-sealed - Use sealed classes for platform variations

Use sealed classes to represent platform-specific variations.

### Correct

```kotlin
// commonMain
sealed class StorageLocation {
    data class Internal(val subPath: String = "") : StorageLocation()
    data class External(val subPath: String = "") : StorageLocation()
    data class Cache(val subPath: String = "") : StorageLocation()
}

expect fun getStoragePath(location: StorageLocation): String

// androidMain
actual fun getStoragePath(location: StorageLocation): String {
    val context = getApplicationContext()
    return when (location) {
        is StorageLocation.Internal -> File(context.filesDir, location.subPath).absolutePath
        is StorageLocation.External -> File(context.getExternalFilesDir(null), location.subPath).absolutePath
        is StorageLocation.Cache -> File(context.cacheDir, location.subPath).absolutePath
    }
}

// iosMain
actual fun getStoragePath(location: StorageLocation): String {
    val fileManager = NSFileManager.defaultManager
    return when (location) {
        is StorageLocation.Internal -> {
            val urls = fileManager.URLsForDirectory(NSDocumentDirectory, NSUserDomainMask)
            (urls.firstOrNull() as? NSURL)?.path + "/" + location.subPath
        }
        is StorageLocation.External -> getStoragePath(StorageLocation.Internal(location.subPath))
        is StorageLocation.Cache -> {
            val urls = fileManager.URLsForDirectory(NSCachesDirectory, NSUserDomainMask)
            (urls.firstOrNull() as? NSURL)?.path + "/" + location.subPath
        }
    } ?: throw IllegalStateException("Cannot get storage path")
}
```

---

## expect-test - Test platform implementations independently

Write tests for each platform implementation.

### Correct

```kotlin
// commonTest
abstract class DateFormatterTest {
    abstract fun createFormatter(): DateFormatter

    @Test
    fun formatDate_returnsCorrectFormat() {
        val formatter = createFormatter()
        val timestamp = 1609459200000L // 2021-01-01 00:00:00 UTC

        val result = formatter.format(timestamp, "yyyy-MM-dd")

        assertEquals("2021-01-01", result)
    }

    @Test
    fun parse_roundTrips() {
        val formatter = createFormatter()
        val original = "2021-06-15"

        val timestamp = formatter.parse(original, "yyyy-MM-dd")
        val formatted = formatter.format(timestamp, "yyyy-MM-dd")

        assertEquals(original, formatted)
    }
}

// androidTest
class AndroidDateFormatterTest : DateFormatterTest() {
    override fun createFormatter(): DateFormatter = AndroidDateFormatter()

    @Test
    fun format_usesDeviceLocale() {
        // Android-specific test
    }
}

// iosTest
class IosDateFormatterTest : DateFormatterTest() {
    override fun createFormatter(): DateFormatter = IosDateFormatter()

    @Test
    fun format_usesNSDateFormatter() {
        // iOS-specific test
    }
}
```
