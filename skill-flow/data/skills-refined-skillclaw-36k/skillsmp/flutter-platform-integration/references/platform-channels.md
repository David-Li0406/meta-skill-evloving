# Platform Channels Reference

Platform channels are Flutter's primary mechanism for communication between Dart code and native platform code. They enable bidirectional, asynchronous message passing between Flutter and Android, iOS, Windows, macOS, and Linux platforms.

## Overview

Platform channels provide an asynchronous messaging system that keeps the UI responsive while enabling access to platform-specific APIs and features. Messages are serialized using message codecs and passed through a binary messenger that routes them to the appropriate handlers.

### Architecture

```
┌─────────────────────────────────────────────────┐
│             Flutter (Dart)                      │
│                                                 │
│  MethodChannel / EventChannel / BasicChannel   │
│                      │                          │
│                      ▼                          │
│            BinaryMessenger                      │
└──────────────────────┬──────────────────────────┘
                       │ Binary Message
                       │ (Serialized with Codec)
┌──────────────────────▼──────────────────────────┐
│         Platform Native Code                    │
│                                                 │
│  MethodCallHandler / EventSink / MessageHandler │
│                      │                          │
│                      ▼                          │
│          Platform APIs & Features               │
└─────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Asynchronous**: All channel operations are async to prevent blocking the UI
2. **Type-Safe**: Message codecs handle serialization with type preservation
3. **Bidirectional**: Messages can flow from Dart to native and vice versa
4. **Thread-Safe**: With proper thread management on the native side
5. **Error-Aware**: Built-in error handling and exception propagation

## Channel Types

Flutter provides three main channel types, each optimized for different communication patterns.

### MethodChannel

MethodChannel is the most commonly used channel type for invoking methods on the native side and receiving results.

#### Use Cases
- Calling native APIs that return a single result
- Invoking platform-specific functionality
- One-time operations (get battery level, take photo, etc.)
- Request-response patterns

#### Dart Side

```dart
import 'package:flutter/services.dart';

class BatteryService {
  static const MethodChannel _channel =
      MethodChannel('com.example.app/battery');

  Future<int?> getBatteryLevel() async {
    try {
      final int? batteryLevel =
          await _channel.invokeMethod<int>('getBatteryLevel');
      return batteryLevel;
    } on PlatformException catch (e) {
      print('Failed to get battery level: ${e.message}');
      return null;
    }
  }

  Future<bool> enablePowerSaveMode(bool enable) async {
    try {
      final bool result = await _channel.invokeMethod(
        'setPowerSaveMode',
        {'enabled': enable},
      );
      return result;
    } on PlatformException catch (e) {
      print('Failed to set power save mode: ${e.message}');
      return false;
    }
  }
}
```

#### Android Side (Kotlin)

```kotlin
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.example.app/battery"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            CHANNEL
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "getBatteryLevel" -> {
                    val batteryLevel = getBatteryLevel()
                    if (batteryLevel != -1) {
                        result.success(batteryLevel)
                    } else {
                        result.error(
                            "UNAVAILABLE",
                            "Battery level not available.",
                            null
                        )
                    }
                }
                "setPowerSaveMode" -> {
                    val enabled = call.argument<Boolean>("enabled") ?: false
                    val success = setPowerSaveMode(enabled)
                    result.success(success)
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private fun getBatteryLevel(): Int {
        val batteryLevel: Int
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val batteryManager =
                getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            batteryLevel = batteryManager.getIntProperty(
                BatteryManager.BATTERY_PROPERTY_CAPACITY
            )
        } else {
            val intent = ContextWrapper(applicationContext).registerReceiver(
                null,
                IntentFilter(Intent.ACTION_BATTERY_CHANGED)
            )
            batteryLevel = intent!!.getIntExtra(
                BatteryManager.EXTRA_LEVEL,
                -1
            ) * 100 / intent.getIntExtra(
                BatteryManager.EXTRA_SCALE,
                -1
            )
        }
        return batteryLevel
    }

    private fun setPowerSaveMode(enabled: Boolean): Boolean {
        // Implementation would go here
        return true
    }
}
```

#### iOS Side (Swift)

```swift
import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller : FlutterViewController =
            window?.rootViewController as! FlutterViewController
        let batteryChannel = FlutterMethodChannel(
            name: "com.example.app/battery",
            binaryMessenger: controller.binaryMessenger
        )

        batteryChannel.setMethodCallHandler { [weak self] (call, result) in
            guard let self = self else { return }

            switch call.method {
            case "getBatteryLevel":
                self.receiveBatteryLevel(result: result)
            case "setPowerSaveMode":
                if let args = call.arguments as? [String: Any],
                   let enabled = args["enabled"] as? Bool {
                    let success = self.setPowerSaveMode(enabled: enabled)
                    result(success)
                } else {
                    result(FlutterError(
                        code: "INVALID_ARGUMENT",
                        message: "enabled argument required",
                        details: nil
                    ))
                }
            default:
                result(FlutterMethodNotImplemented)
            }
        }

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    private func receiveBatteryLevel(result: FlutterResult) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        if device.batteryState == .unknown {
            result(FlutterError(
                code: "UNAVAILABLE",
                message: "Battery level not available.",
                details: nil
            ))
        } else {
            let batteryLevel = Int(device.batteryLevel * 100)
            result(batteryLevel)
        }
    }

    private func setPowerSaveMode(enabled: Bool) -> Bool {
        // Implementation would go here
        return true
    }
}
```

### EventChannel

EventChannel enables streaming data from native code to Dart, perfect for continuous updates like sensor data, location changes, or network status.

#### Use Cases
- Sensor data streams (accelerometer, gyroscope)
- Location updates
- Network connectivity changes
- Battery status monitoring
- Progress updates for long operations
- Real-time data feeds

#### Dart Side

```dart
import 'package:flutter/services.dart';

class LocationService {
  static const EventChannel _channel =
      EventChannel('com.example.app/location');

  Stream<Map<String, double>>? _locationStream;

  Stream<Map<String, double>> get locationStream {
    _locationStream ??= _channel
        .receiveBroadcastStream()
        .map((dynamic event) => Map<String, double>.from(event));
    return _locationStream!;
  }

  void dispose() {
    _locationStream = null;
  }
}

// Usage
class LocationWidget extends StatefulWidget {
  @override
  _LocationWidgetState createState() => _LocationWidgetState();
}

class _LocationWidgetState extends State<LocationWidget> {
  final LocationService _locationService = LocationService();
  double? _latitude;
  double? _longitude;

  @override
  void initState() {
    super.initState();
    _locationService.locationStream.listen((location) {
      setState(() {
        _latitude = location['latitude'];
        _longitude = location['longitude'];
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Text('Lat: $_latitude, Lng: $_longitude');
  }
}
```

#### Android Side (Kotlin)

```kotlin
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import androidx.core.app.ActivityCompat
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.EventChannel

class MainActivity : FlutterActivity() {
    private val LOCATION_CHANNEL = "com.example.app/location"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        EventChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            LOCATION_CHANNEL
        ).setStreamHandler(object : EventChannel.StreamHandler {
            private var locationManager: LocationManager? = null
            private var locationListener: LocationListener? = null

            override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
                locationManager = getSystemService(Context.LOCATION_SERVICE)
                    as LocationManager

                locationListener = LocationListener { location ->
                    val locationData = hashMapOf(
                        "latitude" to location.latitude,
                        "longitude" to location.longitude,
                        "altitude" to location.altitude,
                        "accuracy" to location.accuracy.toDouble()
                    )
                    events.success(locationData)
                }

                if (ActivityCompat.checkSelfPermission(
                        this@MainActivity,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    ) == PackageManager.PERMISSION_GRANTED
                ) {
                    locationManager?.requestLocationUpdates(
                        LocationManager.GPS_PROVIDER,
                        1000, // 1 second
                        10f,  // 10 meters
                        locationListener!!
                    )
                } else {
                    events.error(
                        "PERMISSION_DENIED",
                        "Location permission not granted",
                        null
                    )
                }
            }

            override fun onCancel(arguments: Any?) {
                locationListener?.let { listener ->
                    locationManager?.removeUpdates(listener)
                }
                locationManager = null
                locationListener = null
            }
        })
    }
}
```

#### iOS Side (Swift)

```swift
import CoreLocation
import Flutter

class LocationStreamHandler: NSObject, FlutterStreamHandler, CLLocationManagerDelegate {
    private var eventSink: FlutterEventSink?
    private var locationManager: CLLocationManager?

    func onListen(withArguments arguments: Any?,
                  eventSink events: @escaping FlutterEventSink) -> FlutterError? {
        self.eventSink = events

        locationManager = CLLocationManager()
        locationManager?.delegate = self
        locationManager?.desiredAccuracy = kCLLocationAccuracyBest
        locationManager?.requestWhenInUseAuthorization()
        locationManager?.startUpdatingLocation()

        return nil
    }

    func onCancel(withArguments arguments: Any?) -> FlutterError? {
        locationManager?.stopUpdatingLocation()
        locationManager = nil
        eventSink = nil
        return nil
    }

    func locationManager(_ manager: CLLocationManager,
                        didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }

        let locationData: [String: Double] = [
            "latitude": location.coordinate.latitude,
            "longitude": location.coordinate.longitude,
            "altitude": location.altitude,
            "accuracy": location.horizontalAccuracy
        ]

        eventSink?(locationData)
    }

    func locationManager(_ manager: CLLocationManager,
                        didFailWithError error: Error) {
        eventSink?(FlutterError(
            code: "LOCATION_ERROR",
            message: error.localizedDescription,
            details: nil
        ))
    }
}

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController
        let locationChannel = FlutterEventChannel(
            name: "com.example.app/location",
            binaryMessenger: controller.binaryMessenger
        )

        let locationStreamHandler = LocationStreamHandler()
        locationChannel.setStreamHandler(locationStreamHandler)

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
```

### BasicMessageChannel

BasicMessageChannel provides simple bidirectional message passing without the method call structure.

#### Use Cases
- Simple message exchange
- Custom protocol implementation
- Bidirectional communication patterns
- When MethodChannel structure is too rigid

#### Dart Side

```dart
import 'package:flutter/services.dart';

class MessageService {
  static const BasicMessageChannel<String> _channel =
      BasicMessageChannel<String>(
        'com.example.app/messages',
        StringCodec(),
      );

  Future<String?> sendMessage(String message) async {
    try {
      final String? reply = await _channel.send(message);
      return reply;
    } catch (e) {
      print('Failed to send message: $e');
      return null;
    }
  }

  void setMessageHandler(Future<String> Function(String?) handler) {
    _channel.setMessageHandler(handler);
  }
}
```

#### Android Side (Kotlin)

```kotlin
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.BasicMessageChannel
import io.flutter.plugin.common.StringCodec

class MainActivity : FlutterActivity() {
    private val MESSAGE_CHANNEL = "com.example.app/messages"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        BasicMessageChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            MESSAGE_CHANNEL,
            StringCodec.INSTANCE
        ).setMessageHandler { message, reply ->
            val response = processMessage(message)
            reply.reply(response)
        }
    }

    private fun processMessage(message: String?): String {
        return "Received: $message"
    }
}
```

## Message Codecs

Message codecs handle serialization and deserialization of data passed through platform channels.

### StandardMessageCodec

The default codec supporting most common data types.

#### Supported Types

| Dart Type | Android Type | iOS Type |
|-----------|--------------|----------|
| `null` | `null` | `nil` |
| `bool` | `Boolean` | `NSNumber(Bool)` |
| `int` | `Integer` (32-bit) | `NSNumber(Int32)` |
| `int` | `Long` (64-bit) | `NSNumber(Int64)` |
| `double` | `Double` | `NSNumber(Double)` |
| `String` | `String` | `NSString` |
| `Uint8List` | `byte[]` | `FlutterStandardTypedData` |
| `Int32List` | `int[]` | `FlutterStandardTypedData` |
| `Int64List` | `long[]` | `FlutterStandardTypedData` |
| `Float64List` | `double[]` | `FlutterStandardTypedData` |
| `List` | `ArrayList` | `NSArray` |
| `Map` | `HashMap` | `NSDictionary` |

### Other Codecs

```dart
// BinaryCodec - Raw binary data
const BinaryCodec binaryCodec = BinaryCodec();

// StringCodec - UTF-8 encoded strings
const StringCodec stringCodec = StringCodec();

// JSONMessageCodec - JSON-formatted data
const JSONMessageCodec jsonCodec = JSONMessageCodec();
```

### Custom Codec Example

```dart
class CustomCodec extends StandardMessageCodec {
  const CustomCodec();

  @override
  void writeValue(WriteBuffer buffer, dynamic value) {
    if (value is MyCustomClass) {
      buffer.putUint8(128); // Custom type tag
      writeValue(buffer, value.toMap());
    } else {
      super.writeValue(buffer, value);
    }
  }

  @override
  dynamic readValueOfType(int type, ReadBuffer buffer) {
    switch (type) {
      case 128:
        return MyCustomClass.fromMap(readValue(buffer));
      default:
        return super.readValueOfType(type, buffer);
    }
  }
}
```

## Error Handling

Proper error handling is critical for robust platform channel communication.

### Dart Side Error Handling

```dart
class RobustService {
  static const MethodChannel _channel =
      MethodChannel('com.example.app/service');

  Future<String?> riskyOperation() async {
    try {
      final String result = await _channel.invokeMethod('riskyOperation');
      return result;
    } on PlatformException catch (e) {
      // Handle platform-specific errors
      switch (e.code) {
        case 'UNAVAILABLE':
          print('Service unavailable: ${e.message}');
          break;
        case 'PERMISSION_DENIED':
          print('Permission denied: ${e.message}');
          break;
        case 'NETWORK_ERROR':
          print('Network error: ${e.message}');
          break;
        default:
          print('Unknown error: ${e.code} - ${e.message}');
      }
      return null;
    } on MissingPluginException catch (e) {
      // Handle missing plugin registration
      print('Plugin not registered: ${e.message}');
      return null;
    } catch (e) {
      // Handle other errors
      print('Unexpected error: $e');
      return null;
    }
  }
}
```

### Android Error Reporting

```kotlin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
    .setMethodCallHandler { call, result ->
        try {
            when (call.method) {
                "riskyOperation" -> {
                    val data = performRiskyOperation()
                    result.success(data)
                }
                else -> result.notImplemented()
            }
        } catch (e: SecurityException) {
            result.error(
                "PERMISSION_DENIED",
                "Required permission not granted: ${e.message}",
                mapOf("exception" to e.toString())
            )
        } catch (e: IOException) {
            result.error(
                "NETWORK_ERROR",
                "Network operation failed: ${e.message}",
                null
            )
        } catch (e: Exception) {
            result.error(
                "UNKNOWN_ERROR",
                e.message ?: "Unknown error occurred",
                e.stackTraceToString()
            )
        }
    }
```

### iOS Error Reporting

```swift
batteryChannel.setMethodCallHandler { (call, result) in
    do {
        switch call.method {
        case "riskyOperation":
            let data = try self.performRiskyOperation()
            result(data)
        default:
            result(FlutterMethodNotImplemented)
        }
    } catch let error as NSError {
        if error.domain == NSCocoaErrorDomain {
            result(FlutterError(
                code: "FILE_ERROR",
                message: error.localizedDescription,
                details: error.userInfo
            ))
        } else {
            result(FlutterError(
                code: "UNKNOWN_ERROR",
                message: error.localizedDescription,
                details: nil
            ))
        }
    }
}
```

## Threading and Background Execution

Platform channels must respect threading constraints on both sides.

### Main Thread Constraint

**Critical Rule**: Channel method handlers must execute on the platform's main thread (UI thread).

### Dart to Native - Background Work

```kotlin
// Android - Moving work off UI thread
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
    .setMethodCallHandler { call, result ->
        when (call.method) {
            "heavyOperation" -> {
                // Dispatch to background thread
                CoroutineScope(Dispatchers.IO).launch {
                    val data = performHeavyComputation()

                    // Return result on main thread
                    Handler(Looper.getMainLooper()).post {
                        result.success(data)
                    }
                }
            }
        }
    }
```

```swift
// iOS - Moving work off UI thread
batteryChannel.setMethodCallHandler { (call, result) in
    switch call.method {
    case "heavyOperation":
        // Dispatch to background queue
        DispatchQueue.global(qos: .userInitiated).async {
            let data = self.performHeavyComputation()

            // Return result on main thread
            DispatchQueue.main.async {
                result(data)
            }
        }
    default:
        result(FlutterMethodNotImplemented)
    }
}
```

### Background Task Queue (Android)

```kotlin
// Android - Register channel with background task queue
val taskQueue = flutterPluginBinding.binaryMessenger.makeBackgroundTaskQueue()
channel = MethodChannel(
    flutterPluginBinding.binaryMessenger,
    "com.example.app/background",
    StandardMethodCodec.INSTANCE,
    taskQueue
)
```

### Background Isolates (Dart)

```dart
import 'dart:isolate';
import 'package:flutter/services.dart';

void backgroundIsolateMain(RootIsolateToken rootIsolateToken) async {
  // Initialize background isolate messenger
  BackgroundIsolateBinaryMessenger.ensureInitialized(rootIsolateToken);

  // Now can use platform channels
  const MethodChannel channel = MethodChannel('com.example.app/background');
  final result = await channel.invokeMethod('backgroundOperation');
  print('Background result: $result');
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Get root isolate token
  final RootIsolateToken rootIsolateToken = RootIsolateToken.instance!;

  // Spawn background isolate
  await Isolate.spawn(backgroundIsolateMain, rootIsolateToken);

  runApp(MyApp());
}
```

## Pigeon: Type-Safe Code Generation

Pigeon generates type-safe platform channel code from Dart interface definitions.

### Benefits
- Compile-time type checking
- No string-based method names
- Automatic serialization/deserialization
- Cleaner, more maintainable code
- Supports async/await naturally

### Setup

```yaml
# pubspec.yaml
dev_dependencies:
  pigeon: ^17.0.0
```

### Define API

```dart
// pigeons/api.dart
import 'package:pigeon/pigeon.dart';

@ConfigurePigeon(PigeonOptions(
  dartOut: 'lib/api.g.dart',
  kotlinOut: 'android/app/src/main/kotlin/Api.g.kt',
  kotlinOptions: KotlinOptions(package: 'com.example.app'),
  swiftOut: 'ios/Runner/Api.g.swift',
))

class BatteryInfo {
  final int level;
  final bool isCharging;
  final String status;

  BatteryInfo({
    required this.level,
    required this.isCharging,
    required this.status,
  });
}

@HostApi()
abstract class BatteryApi {
  @async
  BatteryInfo getBatteryInfo();

  @async
  bool setPowerSaveMode(bool enabled);
}

@FlutterApi()
abstract class BatteryCallbackApi {
  void onBatteryLevelChanged(int level);
  void onChargingStateChanged(bool isCharging);
}
```

### Generate Code

```bash
dart run pigeon --input pigeons/api.dart
```

### Dart Implementation

```dart
import 'api.g.dart';

class BatteryService {
  final BatteryApi _api = BatteryApi();

  Future<BatteryInfo> getBatteryInfo() {
    return _api.getBatteryInfo();
  }

  Future<bool> setPowerSaveMode(bool enabled) {
    return _api.setPowerSaveMode(enabled);
  }
}
```

### Android Implementation

```kotlin
import Api

class BatteryApiImpl : BatteryApi {
    override fun getBatteryInfo(result: (Result<BatteryInfo>) -> Unit) {
        try {
            val batteryManager = context.getSystemService(Context.BATTERY_SERVICE)
                as BatteryManager
            val level = batteryManager.getIntProperty(
                BatteryManager.BATTERY_PROPERTY_CAPACITY
            ).toLong()
            val isCharging = batteryManager.isCharging

            val info = BatteryInfo(
                level = level,
                isCharging = isCharging,
                status = "OK"
            )
            result(Result.success(info))
        } catch (e: Exception) {
            result(Result.failure(e))
        }
    }

    override fun setPowerSaveMode(enabled: Boolean,
                                  result: (Result<Boolean>) -> Unit) {
        // Implementation
        result(Result.success(true))
    }
}
```

### iOS Implementation

```swift
import Api

class BatteryApiImpl: BatteryApi {
    func getBatteryInfo(completion: @escaping (Result<BatteryInfo, Error>) -> Void) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        let info = BatteryInfo(
            level: Int64(device.batteryLevel * 100),
            isCharging: device.batteryState == .charging,
            status: "OK"
        )
        completion(.success(info))
    }

    func setPowerSaveMode(enabled: Bool,
                         completion: @escaping (Result<Bool, Error>) -> Void) {
        // Implementation
        completion(.success(true))
    }
}
```

## Best Practices

### Channel Naming
- Use reverse domain notation: `com.example.app/feature`
- Be descriptive and consistent
- Avoid conflicts with other packages

### Type Safety
- Prefer Pigeon for complex APIs
- Validate types on both sides
- Handle null values explicitly

### Error Handling
- Always catch `PlatformException` in Dart
- Provide meaningful error codes and messages
- Include details for debugging
- Document possible error codes

### Performance
- Minimize channel crossings
- Batch operations when possible
- Use EventChannel for continuous updates
- Profile and optimize hot paths

### Testing
- Mock platform channels in tests
- Test error handling paths
- Verify threading behavior
- Integration test across platforms

### Documentation
- Document method signatures clearly
- List supported platforms
- Document error codes
- Provide usage examples

## Troubleshooting

### MissingPluginException
- Verify plugin registration in MainActivity/AppDelegate
- Run `flutter clean` and rebuild
- Check channel names match exactly

### Type Errors
- Verify codec supports the data type
- Check null handling
- Consider custom codec for complex types

### Threading Issues
- Ensure handlers run on main thread
- Use proper dispatchers for background work
- Avoid blocking the UI thread

### Memory Leaks
- Clean up listeners in dispose/onCancel
- Release native resources properly
- Avoid circular references

## Related Resources

- [Android Integration](android-integration.md)
- [iOS Integration](ios-integration.md)
- [Plugin Development](plugin-development.md)
