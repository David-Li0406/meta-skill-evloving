# Android Integration Reference

This guide covers integrating Flutter applications with Android-specific features, including Kotlin/Java development, native API access, Gradle configuration, and Android platform conventions.

## Overview

Flutter Android integration enables you to access Android-specific APIs, use native libraries, and implement features that require platform-specific code. Android integration primarily uses Kotlin (recommended) or Java for native code.

### Android Project Structure

```
android/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/         # Java source files (legacy)
│   │       ├── kotlin/       # Kotlin source files (recommended)
│   │       │   └── com/example/app/
│   │       │       └── MainActivity.kt
│   │       ├── AndroidManifest.xml
│   │       └── res/          # Resources (layouts, drawables, etc.)
│   └── build.gradle          # App-level build configuration
├── gradle/                   # Gradle wrapper
├── build.gradle              # Project-level build configuration
└── settings.gradle           # Project settings
```

## Getting Started

### MainActivity Setup

The MainActivity is the entry point for Flutter on Android and where you register platform channels and plugins.

#### Kotlin Implementation

```kotlin
package com.example.app

import android.os.Bundle
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.EventChannel

class MainActivity : FlutterActivity() {
    private val BATTERY_CHANNEL = "com.example.app/battery"
    private val LOCATION_CHANNEL = "com.example.app/location"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        // Register method channel
        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            BATTERY_CHANNEL
        ).setMethodCallHandler { call, result ->
            // Handle method calls
            handleMethodCall(call, result)
        }

        // Register event channel
        EventChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            LOCATION_CHANNEL
        ).setStreamHandler(LocationStreamHandler(this))
    }

    private fun handleMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "getBatteryLevel" -> {
                val batteryLevel = getBatteryLevel()
                result.success(batteryLevel)
            }
            else -> result.notImplemented()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Additional initialization if needed
    }

    override fun onDestroy() {
        // Cleanup resources
        super.onDestroy()
    }
}
```

#### Java Implementation

```java
package com.example.app;

import android.os.Bundle;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;
import io.flutter.plugin.common.EventChannel;

public class MainActivity extends FlutterActivity {
    private static final String BATTERY_CHANNEL = "com.example.app/battery";
    private static final String LOCATION_CHANNEL = "com.example.app/location";

    @Override
    public void configureFlutterEngine(FlutterEngine flutterEngine) {
        super.configureFlutterEngine(flutterEngine);

        new MethodChannel(
            flutterEngine.getDartExecutor().getBinaryMessenger(),
            BATTERY_CHANNEL
        ).setMethodCallHandler((call, result) -> {
            if (call.method.equals("getBatteryLevel")) {
                int batteryLevel = getBatteryLevel();
                result.success(batteryLevel);
            } else {
                result.notImplemented();
            }
        });

        new EventChannel(
            flutterEngine.getDartExecutor().getBinaryMessenger(),
            LOCATION_CHANNEL
        ).setStreamHandler(new LocationStreamHandler(this));
    }

    private int getBatteryLevel() {
        // Implementation
        return -1;
    }
}
```

## Accessing Android APIs

### Battery Level Example

Complete implementation accessing Android system APIs.

```kotlin
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build

class BatteryService(private val context: Context) {
    fun getBatteryLevel(): Int {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val batteryManager = context.getSystemService(Context.BATTERY_SERVICE)
                as BatteryManager
            batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        } else {
            val intent = ContextWrapper(context).registerReceiver(
                null,
                IntentFilter(Intent.ACTION_BATTERY_CHANGED)
            )
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
            if (level >= 0 && scale > 0) {
                (level * 100) / scale
            } else {
                -1
            }
        }
    }

    fun getBatteryInfo(): BatteryInfo {
        val batteryManager = context.getSystemService(Context.BATTERY_SERVICE)
            as BatteryManager

        val level = batteryManager.getIntProperty(
            BatteryManager.BATTERY_PROPERTY_CAPACITY
        )

        val isCharging = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            batteryManager.isCharging
        } else {
            val intent = context.registerReceiver(
                null,
                IntentFilter(Intent.ACTION_BATTERY_CHANGED)
            )
            val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
            status == BatteryManager.BATTERY_STATUS_CHARGING ||
                    status == BatteryManager.BATTERY_STATUS_FULL
        }

        return BatteryInfo(level, isCharging)
    }
}

data class BatteryInfo(val level: Int, val isCharging: Boolean)
```

### File System Access

```kotlin
import android.content.Context
import java.io.File
import java.io.IOException

class FileService(private val context: Context) {
    fun writeFile(fileName: String, content: String): Boolean {
        return try {
            context.openFileOutput(fileName, Context.MODE_PRIVATE).use { stream ->
                stream.write(content.toByteArray())
            }
            true
        } catch (e: IOException) {
            false
        }
    }

    fun readFile(fileName: String): String? {
        return try {
            context.openFileInput(fileName).bufferedReader().use { reader ->
                reader.readText()
            }
        } catch (e: IOException) {
            null
        }
    }

    fun deleteFile(fileName: String): Boolean {
        return context.deleteFile(fileName)
    }

    fun listFiles(): List<String> {
        return context.fileList().toList()
    }

    fun getExternalStorageDir(): String? {
        return context.getExternalFilesDir(null)?.absolutePath
    }
}
```

### Camera Access

```kotlin
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.camera2.CameraAccessException
import android.hardware.camera2.CameraManager
import androidx.core.content.ContextCompat

class CameraService(private val context: Context) {
    private val cameraManager: CameraManager =
        context.getSystemService(Context.CAMERA_SERVICE) as CameraManager

    fun hasCameraPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    }

    fun getCameraIds(): List<String> {
        return try {
            cameraManager.cameraIdList.toList()
        } catch (e: CameraAccessException) {
            emptyList()
        }
    }

    fun hasFlash(): Boolean {
        return try {
            val cameraIds = cameraManager.cameraIdList
            cameraIds.any { id ->
                val characteristics = cameraManager.getCameraCharacteristics(id)
                characteristics.get(
                    android.hardware.camera2.CameraCharacteristics.FLASH_INFO_AVAILABLE
                ) == true
            }
        } catch (e: Exception) {
            false
        }
    }

    fun toggleFlashlight(enable: Boolean): Boolean {
        return try {
            val cameraIds = cameraManager.cameraIdList
            if (cameraIds.isNotEmpty()) {
                cameraManager.setTorchMode(cameraIds[0], enable)
                true
            } else {
                false
            }
        } catch (e: Exception) {
            false
        }
    }
}
```

## Permissions

### Declaring Permissions

Edit `AndroidManifest.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />

    <!-- Features -->
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />

    <application
        android:label="My App"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
                android:name="io.flutter.embedding.android.NormalTheme"
                android:resource="@style/NormalTheme" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### Runtime Permission Handling

```kotlin
import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity

class MainActivity : FlutterActivity() {
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        permissions.entries.forEach { entry ->
            val permission = entry.key
            val isGranted = entry.value
            notifyPermissionResult(permission, isGranted)
        }
    }

    fun requestPermissions(permissions: List<String>) {
        requestPermissionLauncher.launch(permissions.toTypedArray())
    }

    fun checkPermission(permission: String): Boolean {
        return ContextCompat.checkSelfPermission(
            this,
            permission
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun notifyPermissionResult(permission: String, granted: Boolean) {
        // Notify Flutter side via method channel
        val channel = MethodChannel(
            flutterEngine?.dartExecutor?.binaryMessenger!!,
            "com.example.app/permissions"
        )
        channel.invokeMethod(
            "onPermissionResult",
            mapOf("permission" to permission, "granted" to granted)
        )
    }
}
```

### Permission Flow with Flutter

```kotlin
// Android side
private fun requestLocationPermission(result: MethodChannel.Result) {
    val permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.ACCESS_BACKGROUND_LOCATION
        )
    } else {
        arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
    }

    // Store result callback for later
    pendingPermissionResult = result

    requestPermissionLauncher.launch(permissions)
}
```

## Gradle Configuration

### App-Level build.gradle

```gradle
plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}

android {
    namespace "com.example.app"
    compileSdkVersion 34
    ndkVersion flutter.ndkVersion

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = '1.8'
    }

    defaultConfig {
        applicationId "com.example.app"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName

        // MultiDex support for large apps
        multiDexEnabled true
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
            // Shrinking and obfuscation
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            applicationIdSuffix ".debug"
            debuggable true
        }
    }

    // Build flavors
    flavorDimensions "environment"
    productFlavors {
        development {
            dimension "environment"
            applicationIdSuffix ".dev"
        }
        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
        }
        production {
            dimension "environment"
        }
    }
}

flutter {
    source "../.."
}

dependencies {
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'

    // Android X libraries
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'com.google.android.material:material:1.11.0'

    // Coroutines for async operations
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'

    // Google Play Services (example)
    implementation 'com.google.android.gms:play-services-location:21.1.0'

    // Image loading
    implementation 'com.github.bumptech.glide:glide:4.16.0'

    // JSON parsing
    implementation 'com.google.code.gson:gson:2.10.1'

    // MultiDex
    implementation 'androidx.multidex:multidex:2.0.1'
}
```

### ProGuard Rules

Create `android/app/proguard-rules.pro`:

```proguard
# Flutter wrapper
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Keep native methods
-keepclassmembers class * {
    native <methods>;
}

# Gson
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Your data classes
-keep class com.example.app.models.** { *; }
```

## Background Processing

### WorkManager Integration

```kotlin
import android.content.Context
import androidx.work.*
import java.util.concurrent.TimeUnit

class BackgroundSyncWorker(
    context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        return try {
            // Perform background work
            performSync()
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }

    private suspend fun performSync() {
        // Implementation
    }

    companion object {
        fun schedule(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()

            val workRequest = PeriodicWorkRequestBuilder<BackgroundSyncWorker>(
                15, TimeUnit.MINUTES
            )
                .setConstraints(constraints)
                .setBackoffCriteria(
                    BackoffPolicy.LINEAR,
                    PeriodicWorkRequest.MIN_BACKOFF_MILLIS,
                    TimeUnit.MILLISECONDS
                )
                .build()

            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                "background_sync",
                ExistingPeriodicWorkPolicy.KEEP,
                workRequest
            )
        }
    }
}
```

Add dependency:

```gradle
dependencies {
    implementation 'androidx.work:work-runtime-ktx:2.9.0'
}
```

### Foreground Service

```kotlin
import android.app.*
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

class LocationTrackingService : Service() {
    private val CHANNEL_ID = "LocationTracking"
    private val NOTIFICATION_ID = 1

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)

        // Start location tracking
        startLocationUpdates()

        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Location Tracking",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Tracking your location in the background"
            }

            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Location Tracking Active")
            .setContentText("Tracking your location")
            .setSmallIcon(R.drawable.ic_location)
            .setContentIntent(pendingIntent)
            .build()
    }

    private fun startLocationUpdates() {
        // Implementation
    }

    override fun onDestroy() {
        super.onDestroy()
        // Cleanup
    }
}
```

Register service in AndroidManifest.xml:

```xml
<service
    android:name=".LocationTrackingService"
    android:enabled="true"
    android:exported="false"
    android:foregroundServiceType="location" />
```

## Native Views (Platform Views)

### Creating Custom Android View

```kotlin
import android.content.Context
import android.view.View
import android.widget.TextView
import io.flutter.plugin.platform.PlatformView

class CustomNativeView(
    context: Context,
    id: Int,
    creationParams: Map<String?, Any?>?
) : PlatformView {
    private val textView: TextView = TextView(context).apply {
        text = creationParams?.get("text") as? String ?: "Native View"
        textSize = 20f
        setPadding(16, 16, 16, 16)
    }

    override fun getView(): View = textView

    override fun dispose() {
        // Cleanup
    }

    fun updateText(text: String) {
        textView.text = text
    }
}
```

### Factory and Registration

```kotlin
import android.content.Context
import io.flutter.plugin.common.StandardMessageCodec
import io.flutter.plugin.platform.PlatformView
import io.flutter.plugin.platform.PlatformViewFactory

class CustomNativeViewFactory : PlatformViewFactory(StandardMessageCodec.INSTANCE) {
    override fun create(
        context: Context,
        viewId: Int,
        args: Any?
    ): PlatformView {
        val creationParams = args as? Map<String?, Any?>
        return CustomNativeView(context, viewId, creationParams)
    }
}

// In MainActivity
override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)

    flutterEngine
        .platformViewsController
        .registry
        .registerViewFactory(
            "custom-native-view",
            CustomNativeViewFactory()
        )
}
```

## Coroutines for Async Operations

```kotlin
import kotlinx.coroutines.*
import io.flutter.plugin.common.MethodChannel

class NetworkService {
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    fun fetchData(result: MethodChannel.Result) {
        scope.launch {
            try {
                val data = withContext(Dispatchers.IO) {
                    // Network call on IO thread
                    performNetworkRequest()
                }
                // Result callback on main thread
                result.success(data)
            } catch (e: Exception) {
                result.error("NETWORK_ERROR", e.message, null)
            }
        }
    }

    private suspend fun performNetworkRequest(): String {
        delay(1000) // Simulate network delay
        return "Data from network"
    }

    fun cleanup() {
        scope.cancel()
    }
}
```

## Intents and Activity Results

### Launching Activities

```kotlin
import android.content.Intent
import android.provider.MediaStore
import androidx.activity.result.contract.ActivityResultContracts

class MainActivity : FlutterActivity() {
    private val takePictureLauncher = registerForActivityResult(
        ActivityResultContracts.TakePicture()
    ) { success ->
        if (success) {
            notifyPictureTaken()
        }
    }

    private val pickImageLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri ->
        uri?.let { notifyImagePicked(it.toString()) }
    }

    fun takePicture(outputUri: Uri) {
        takePictureLauncher.launch(outputUri)
    }

    fun pickImage() {
        pickImageLauncher.launch("image/*")
    }
}
```

## Testing

### Unit Testing Kotlin Code

```kotlin
// test/kotlin/com/example/app/BatteryServiceTest.kt
import org.junit.Test
import org.junit.Assert.*
import org.mockito.Mockito.*

class BatteryServiceTest {
    @Test
    fun testGetBatteryLevel() {
        val context = mock(Context::class.java)
        val batteryManager = mock(BatteryManager::class.java)

        `when`(context.getSystemService(Context.BATTERY_SERVICE))
            .thenReturn(batteryManager)
        `when`(batteryManager.getIntProperty(
            BatteryManager.BATTERY_PROPERTY_CAPACITY
        )).thenReturn(75)

        val service = BatteryService(context)
        val level = service.getBatteryLevel()

        assertEquals(75, level)
    }
}
```

Add dependencies:

```gradle
dependencies {
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.mockito:mockito-core:5.7.0'
    testImplementation 'org.mockito.kotlin:mockito-kotlin:5.2.1'
}
```

## Best Practices

### Lifecycle Management
- Clean up resources in `onDestroy()`
- Handle configuration changes properly
- Unregister listeners and receivers

### Threading
- Use coroutines for async operations
- Keep UI operations on main thread
- Use appropriate dispatchers (IO, Default, Main)

### Error Handling
- Catch and report exceptions
- Provide meaningful error messages
- Use proper error codes

### Performance
- Avoid blocking the main thread
- Use ProGuard for release builds
- Profile with Android Profiler

### Security
- Validate all inputs from Flutter
- Use HTTPS for network calls
- Store sensitive data securely (EncryptedSharedPreferences)

## Related Resources

- [Platform Channels](platform-channels.md)
- [iOS Integration](ios-integration.md)
- [Plugin Development](plugin-development.md)
