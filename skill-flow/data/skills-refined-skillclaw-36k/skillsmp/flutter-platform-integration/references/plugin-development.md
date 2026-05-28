# Plugin Development Reference

This comprehensive guide covers creating, developing, testing, and publishing Flutter plugins. Learn how to build reusable packages that bridge Flutter with platform-specific functionality across Android, iOS, web, and desktop platforms.

## Overview

Flutter plugins are specialized packages that provide access to platform-specific features through a Dart API combined with native platform implementations. Plugins enable code reuse across projects and contribute to the Flutter ecosystem.

### Plugin Types

**Dart Packages**: Pure Dart code with no platform-specific implementations
- Example: `path`, `intl`, `provider`
- Use when: No native code required
- Created with: `flutter create --template=package`

**Plugin Packages**: Dart API with platform-specific implementations
- Example: `url_launcher`, `camera`, `shared_preferences`
- Use when: Need native platform access
- Created with: `flutter create --template=plugin`

**Federated Plugins**: Modular architecture with separate platform packages
- Example: `path_provider`, `video_player`
- Use when: Large plugins, domain expert contributions
- Architecture: App-facing + Platform interface + Platform implementations

**FFI Packages**: Dart code calling native C/C++ via dart:ffi
- Example: `objectbox`, `realm`
- Use when: Need C/C++ library bindings
- Created with: `flutter create --template=package_ffi`

## Creating a Plugin

### Initial Setup

```bash
# Create plugin with specific platforms and languages
flutter create \
  --org com.example \
  --template=plugin \
  --platforms=android,ios,linux,macos,windows,web \
  -a kotlin \
  -i swift \
  my_plugin

cd my_plugin
```

### Project Structure

```
my_plugin/
├── lib/
│   ├── my_plugin.dart              # Main Dart API
│   ├── my_plugin_platform_interface.dart  # (Optional) Platform interface
│   └── src/                        # Implementation details
├── android/
│   ├── src/main/kotlin/com/example/my_plugin/
│   │   └── MyPlugin.kt             # Android implementation
│   └── build.gradle                # Android configuration
├── ios/
│   ├── Classes/
│   │   └── MyPlugin.swift          # iOS implementation
│   └── my_plugin.podspec           # iOS pod configuration
├── linux/                          # Linux implementation
├── macos/                          # macOS implementation
├── windows/                        # Windows implementation
├── web/                            # Web implementation
├── example/                        # Example Flutter app
│   ├── lib/main.dart
│   ├── android/
│   ├── ios/
│   └── test/
├── test/                           # Unit tests
├── pubspec.yaml                    # Package metadata
├── README.md                       # Documentation
├── CHANGELOG.md                    # Version history
└── LICENSE                         # License file
```

## Implementing the Plugin

### Dart API Layer

Create a clean, intuitive API in `lib/my_plugin.dart`:

```dart
/// The main plugin class providing access to platform features.
class MyPlugin {
  /// Private constructor to prevent instantiation
  MyPlugin._();

  /// Singleton instance
  static final MyPlugin instance = MyPlugin._();

  /// The platform implementation
  static MyPluginPlatform get _platform => MyPluginPlatform.instance;

  /// Gets the current battery level.
  ///
  /// Returns the battery level as a percentage (0-100), or null if unavailable.
  ///
  /// Throws [PlatformException] if the platform doesn't support this feature.
  ///
  /// Example:
  /// ```dart
  /// final level = await MyPlugin.instance.getBatteryLevel();
  /// print('Battery level: $level%');
  /// ```
  Future<int?> getBatteryLevel() {
    return _platform.getBatteryLevel();
  }

  /// Starts monitoring battery level changes.
  ///
  /// Returns a stream of battery level updates.
  ///
  /// Example:
  /// ```dart
  /// MyPlugin.instance.batteryLevelStream.listen((level) {
  ///   print('Battery level changed: $level%');
  /// });
  /// ```
  Stream<int> get batteryLevelStream {
    return _platform.batteryLevelStream;
  }

  /// Enables or disables power save mode.
  ///
  /// Returns true if the operation was successful.
  ///
  /// Note: On iOS, power save mode can only be enabled by the user.
  /// This method will return the current state instead.
  Future<bool> setPowerSaveMode(bool enabled) {
    return _platform.setPowerSaveMode(enabled);
  }
}
```

### Platform Interface (Plugin Foundation Pattern)

Create `lib/my_plugin_platform_interface.dart`:

```dart
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:my_plugin/my_plugin_method_channel.dart';

/// The interface that platform-specific implementations must extend.
///
/// Platform implementations should extend this class rather than
/// implement it to ensure backward compatibility.
abstract class MyPluginPlatform extends PlatformInterface {
  MyPluginPlatform() : super(token: _token);

  static final Object _token = Object();

  static MyPluginPlatform _instance = MethodChannelMyPlugin();

  /// The default instance of [MyPluginPlatform] to use.
  ///
  /// Defaults to [MethodChannelMyPlugin].
  static MyPluginPlatform get instance => _instance;

  /// Platform-specific implementations should set this with their own
  /// platform-specific class that extends [MyPluginPlatform] when
  /// they register themselves.
  static set instance(MyPluginPlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  /// Gets the current battery level.
  Future<int?> getBatteryLevel() {
    throw UnimplementedError('getBatteryLevel() has not been implemented.');
  }

  /// Stream of battery level changes.
  Stream<int> get batteryLevelStream {
    throw UnimplementedError('batteryLevelStream has not been implemented.');
  }

  /// Sets power save mode.
  Future<bool> setPowerSaveMode(bool enabled) {
    throw UnimplementedError('setPowerSaveMode() has not been implemented.');
  }
}
```

### Method Channel Implementation

Create `lib/my_plugin_method_channel.dart`:

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:my_plugin/my_plugin_platform_interface.dart';

/// An implementation of [MyPluginPlatform] that uses method channels.
class MethodChannelMyPlugin extends MyPluginPlatform {
  /// The method channel used to interact with the native platform.
  @visibleForTesting
  final methodChannel = const MethodChannel('com.example.my_plugin/methods');

  /// The event channel for battery level updates.
  @visibleForTesting
  final eventChannel = const EventChannel('com.example.my_plugin/battery');

  @override
  Future<int?> getBatteryLevel() async {
    try {
      final int? level = await methodChannel.invokeMethod<int>('getBatteryLevel');
      return level;
    } on PlatformException catch (e) {
      debugPrint('Failed to get battery level: ${e.message}');
      return null;
    }
  }

  @override
  Stream<int> get batteryLevelStream {
    return eventChannel.receiveBroadcastStream().map((dynamic event) {
      if (event is int) {
        return event;
      }
      throw Exception('Invalid battery level: $event');
    });
  }

  @override
  Future<bool> setPowerSaveMode(bool enabled) async {
    try {
      final bool result = await methodChannel.invokeMethod(
        'setPowerSaveMode',
        {'enabled': enabled},
      );
      return result;
    } on PlatformException catch (e) {
      debugPrint('Failed to set power save mode: ${e.message}');
      return false;
    }
  }
}
```

### Android Implementation

Edit `android/src/main/kotlin/com/example/my_plugin/MyPlugin.kt`:

```kotlin
package com.example.my_plugin

import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import androidx.annotation.NonNull
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

class MyPlugin : FlutterPlugin, MethodCallHandler {
    private lateinit var methodChannel: MethodChannel
    private lateinit var eventChannel: EventChannel
    private lateinit var context: Context
    private var batteryStreamHandler: BatteryStreamHandler? = null

    override fun onAttachedToEngine(@NonNull flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {
        context = flutterPluginBinding.applicationContext

        methodChannel = MethodChannel(
            flutterPluginBinding.binaryMessenger,
            "com.example.my_plugin/methods"
        )
        methodChannel.setMethodCallHandler(this)

        eventChannel = EventChannel(
            flutterPluginBinding.binaryMessenger,
            "com.example.my_plugin/battery"
        )
        batteryStreamHandler = BatteryStreamHandler(context)
        eventChannel.setStreamHandler(batteryStreamHandler)
    }

    override fun onMethodCall(@NonNull call: MethodCall, @NonNull result: Result) {
        when (call.method) {
            "getBatteryLevel" -> {
                val batteryLevel = getBatteryLevel()
                if (batteryLevel != -1) {
                    result.success(batteryLevel)
                } else {
                    result.error(
                        "UNAVAILABLE",
                        "Battery level not available",
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

    private fun getBatteryLevel(): Int {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val batteryManager = context.getSystemService(Context.BATTERY_SERVICE)
                as BatteryManager
            batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        } else {
            val intent = context.registerReceiver(
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

    private fun setPowerSaveMode(enabled: Boolean): Boolean {
        // Android doesn't allow apps to change power save mode
        // Return current state instead
        val powerManager = context.getSystemService(Context.POWER_SERVICE)
            as android.os.PowerManager
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            powerManager.isPowerSaveMode
        } else {
            false
        }
    }

    override fun onDetachedFromEngine(@NonNull binding: FlutterPlugin.FlutterPluginBinding) {
        methodChannel.setMethodCallHandler(null)
        eventChannel.setStreamHandler(null)
    }
}

class BatteryStreamHandler(private val context: Context) : EventChannel.StreamHandler {
    private var receiver: android.content.BroadcastReceiver? = null

    override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
        receiver = object : android.content.BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                val scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                val batteryPct = if (level >= 0 && scale > 0) {
                    (level * 100) / scale
                } else {
                    -1
                }
                if (batteryPct >= 0) {
                    events.success(batteryPct)
                }
            }
        }

        context.registerReceiver(
            receiver,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        )
    }

    override fun onCancel(arguments: Any?) {
        receiver?.let { context.unregisterReceiver(it) }
        receiver = null
    }
}
```

### iOS Implementation

Edit `ios/Classes/MyPlugin.swift`:

```swift
import Flutter
import UIKit

public class MyPlugin: NSObject, FlutterPlugin, FlutterStreamHandler {
    private var eventSink: FlutterEventSink?

    public static func register(with registrar: FlutterPluginRegistrar) {
        let methodChannel = FlutterMethodChannel(
            name: "com.example.my_plugin/methods",
            binaryMessenger: registrar.messenger()
        )
        let eventChannel = FlutterEventChannel(
            name: "com.example.my_plugin/battery",
            binaryMessenger: registrar.messenger()
        )

        let instance = MyPlugin()
        registrar.addMethodCallDelegate(instance, channel: methodChannel)
        eventChannel.setStreamHandler(instance)
    }

    public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "getBatteryLevel":
            getBatteryLevel(result: result)
        case "setPowerSaveMode":
            if let args = call.arguments as? [String: Any],
               let enabled = args["enabled"] as? Bool {
                setPowerSaveMode(enabled: enabled, result: result)
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

    private func getBatteryLevel(result: FlutterResult) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        if device.batteryState == .unknown {
            result(FlutterError(
                code: "UNAVAILABLE",
                message: "Battery level not available",
                details: nil
            ))
        } else {
            let batteryLevel = Int(device.batteryLevel * 100)
            result(batteryLevel)
        }
    }

    private func setPowerSaveMode(enabled: Bool, result: FlutterResult) {
        // iOS doesn't allow apps to change power save mode
        // Return current state instead
        let isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled
        result(isLowPowerMode)
    }

    // FlutterStreamHandler
    public func onListen(
        withArguments arguments: Any?,
        eventSink events: @escaping FlutterEventSink
    ) -> FlutterError? {
        self.eventSink = events

        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        // Send initial value
        let batteryLevel = Int(device.batteryLevel * 100)
        events(batteryLevel)

        // Listen for changes
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(batteryLevelChanged),
            name: UIDevice.batteryLevelDidChangeNotification,
            object: nil
        )

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(batteryStateChanged),
            name: UIDevice.batteryStateDidChangeNotification,
            object: nil
        )

        return nil
    }

    public func onCancel(withArguments arguments: Any?) -> FlutterError? {
        NotificationCenter.default.removeObserver(self)
        eventSink = nil
        return nil
    }

    @objc private func batteryLevelChanged() {
        let device = UIDevice.current
        let batteryLevel = Int(device.batteryLevel * 100)
        eventSink?(batteryLevel)
    }

    @objc private func batteryStateChanged() {
        batteryLevelChanged() // Send updated level
    }
}
```

## pubspec.yaml Configuration

### Complete Plugin Metadata

```yaml
name: my_plugin
description: A Flutter plugin for accessing battery information and power settings.
version: 1.0.0
homepage: https://github.com/example/my_plugin
repository: https://github.com/example/my_plugin
issue_tracker: https://github.com/example/my_plugin/issues

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter
  plugin_platform_interface: ^2.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  plugin:
    platforms:
      android:
        package: com.example.my_plugin
        pluginClass: MyPlugin
      ios:
        pluginClass: MyPlugin
      linux:
        pluginClass: MyPlugin
      macos:
        pluginClass: MyPlugin
      windows:
        pluginClass: MyPlugin
      web:
        pluginClass: MyPluginWeb
        fileName: my_plugin_web.dart
```

### Platform-Specific Configuration

For federated plugins:

```yaml
# my_plugin_android/pubspec.yaml
flutter:
  plugin:
    implements: my_plugin  # Implements the app-facing package
    platforms:
      android:
        package: com.example.my_plugin_android
        pluginClass: MyPluginAndroid
```

## Testing

### Unit Tests

Create `test/my_plugin_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_plugin/my_plugin.dart';
import 'package:my_plugin/my_plugin_platform_interface.dart';
import 'package:my_plugin/my_plugin_method_channel.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockMyPluginPlatform
    with MockPlatformInterfaceMixin
    implements MyPluginPlatform {
  @override
  Future<int?> getBatteryLevel() => Future.value(75);

  @override
  Stream<int> get batteryLevelStream => Stream.value(75);

  @override
  Future<bool> setPowerSaveMode(bool enabled) => Future.value(true);
}

void main() {
  final MyPluginPlatform initialPlatform = MyPluginPlatform.instance;

  test('$MethodChannelMyPlugin is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelMyPlugin>());
  });

  test('getBatteryLevel', () async {
    MyPlugin myPlugin = MyPlugin.instance;
    MockMyPluginPlatform fakePlatform = MockMyPluginPlatform();
    MyPluginPlatform.instance = fakePlatform;

    expect(await myPlugin.getBatteryLevel(), 75);
  });

  test('setPowerSaveMode', () async {
    MyPlugin myPlugin = MyPlugin.instance;
    MockMyPluginPlatform fakePlatform = MockMyPluginPlatform();
    MyPluginPlatform.instance = fakePlatform;

    expect(await myPlugin.setPowerSaveMode(true), true);
  });

  test('batteryLevelStream', () async {
    MyPlugin myPlugin = MyPlugin.instance;
    MockMyPluginPlatform fakePlatform = MockMyPluginPlatform();
    MyPluginPlatform.instance = fakePlatform;

    expect(myPlugin.batteryLevelStream, emits(75));
  });
}
```

### Method Channel Tests

```dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_plugin/my_plugin_method_channel.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  MethodChannelMyPlugin platform = MethodChannelMyPlugin();
  const MethodChannel channel = MethodChannel('com.example.my_plugin/methods');

  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      channel,
      (MethodCall methodCall) async {
        if (methodCall.method == 'getBatteryLevel') {
          return 75;
        } else if (methodCall.method == 'setPowerSaveMode') {
          return true;
        }
        return null;
      },
    );
  });

  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null);
  });

  test('getBatteryLevel', () async {
    expect(await platform.getBatteryLevel(), 75);
  });

  test('setPowerSaveMode', () async {
    expect(await platform.setPowerSaveMode(true), true);
  });
}
```

## Example App

Create a comprehensive example in `example/lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:my_plugin/my_plugin.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _myPlugin = MyPlugin.instance;
  int? _batteryLevel;
  String _status = 'Unknown';

  @override
  void initState() {
    super.initState();
    _initPlugin();
  }

  Future<void> _initPlugin() async {
    try {
      final level = await _myPlugin.getBatteryLevel();
      setState(() {
        _batteryLevel = level;
        _status = 'Battery level: $level%';
      });

      // Listen to battery changes
      _myPlugin.batteryLevelStream.listen((level) {
        setState(() {
          _batteryLevel = level;
          _status = 'Battery level: $level%';
        });
      });
    } catch (e) {
      setState(() {
        _status = 'Error: $e';
      });
    }
  }

  Future<void> _setPowerSaveMode(bool enabled) async {
    try {
      final result = await _myPlugin.setPowerSaveMode(enabled);
      setState(() {
        _status = result
            ? 'Power save mode: ${enabled ? "ON" : "OFF"}'
            : 'Failed to set power save mode';
      });
    } catch (e) {
      setState(() {
        _status = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('My Plugin Example'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                _status,
                style: Theme.of(context).textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              if (_batteryLevel != null)
                CircularProgressIndicator(
                  value: _batteryLevel! / 100,
                  strokeWidth: 10,
                ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () => _setPowerSaveMode(true),
                child: const Text('Enable Power Save Mode'),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () => _setPowerSaveMode(false),
                child: const Text('Disable Power Save Mode'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## Publishing to pub.dev

### Pre-Publishing Checklist

- [ ] Complete README.md with examples and screenshots
- [ ] Update CHANGELOG.md with version history
- [ ] Add LICENSE file
- [ ] Write comprehensive API documentation
- [ ] Include example app demonstrating all features
- [ ] Test on all supported platforms
- [ ] Follow [Effective Dart](https://dart.dev/guides/language/effective-dart) guidelines
- [ ] Achieve 100+ pub points
- [ ] Consider Flutter Favorite criteria

### Validate Package

```bash
# Dry run to check for issues
flutter pub publish --dry-run

# Check package score
dart pub publish --dry-run
```

### Publish

```bash
# Publish to pub.dev (irreversible!)
flutter pub publish
```

### Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Update `pubspec.yaml` and `CHANGELOG.md`:

```yaml
version: 1.1.0
```

```markdown
## 1.1.0

- Added batteryLevelStream for real-time updates
- Improved error handling
- Updated documentation

## 1.0.0

- Initial release
- getBatteryLevel() method
- setPowerSaveMode() method
```

## Federated Plugin Architecture

### Structure

```
my_plugin/                          # App-facing package
my_plugin_platform_interface/       # Platform interface
my_plugin_android/                  # Android implementation
my_plugin_ios/                      # iOS implementation
my_plugin_web/                      # Web implementation
```

### App-Facing Package

```yaml
# my_plugin/pubspec.yaml
dependencies:
  my_plugin_platform_interface: ^1.0.0
  my_plugin_android: ^1.0.0
  my_plugin_ios: ^1.0.0
  my_plugin_web: ^1.0.0
```

### Platform Interface

```dart
// my_plugin_platform_interface/lib/my_plugin_platform_interface.dart
abstract class MyPluginPlatform extends PlatformInterface {
  // Define interface
}
```

### Platform Implementation

```yaml
# my_plugin_android/pubspec.yaml
flutter:
  plugin:
    implements: my_plugin
    platforms:
      android:
        package: com.example.my_plugin_android
        pluginClass: MyPluginAndroid
```

## Best Practices

### API Design
- Keep APIs simple and intuitive
- Use async/await for asynchronous operations
- Provide comprehensive documentation
- Follow Dart naming conventions
- Support null safety

### Error Handling
- Use PlatformException for platform errors
- Provide meaningful error codes and messages
- Document possible errors
- Handle edge cases gracefully

### Documentation
- Write dartdoc comments for all public APIs
- Include code examples
- Document platform limitations
- Provide migration guides for breaking changes

### Testing
- Write unit tests for Dart code
- Mock platform channels in tests
- Test error handling
- Provide integration tests

### Performance
- Minimize platform channel calls
- Batch operations when possible
- Cache results when appropriate
- Profile and optimize

### Maintenance
- Respond to issues promptly
- Keep dependencies updated
- Support latest Flutter versions
- Follow platform best practices

## Related Resources

- [Platform Channels](platform-channels.md)
- [Android Integration](android-integration.md)
- [iOS Integration](ios-integration.md)
