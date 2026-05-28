# Custom Plugin Example: Battery Level Plugin

This example demonstrates creating a complete Flutter plugin from scratch that accesses platform-specific battery information. The plugin provides a clean Dart API while implementing native code for both Android and iOS.

## Plugin Overview

**Name:** battery_level_plugin
**Purpose:** Get device battery level and charging status
**Platforms:** Android, iOS
**Features:**
- Get current battery level (0-100%)
- Get charging status
- Stream battery level changes
- Cross-platform API

## Project Setup

```bash
# Create the plugin
flutter create \
  --org com.example \
  --template=plugin \
  --platforms=android,ios \
  -a kotlin \
  -i swift \
  battery_level_plugin

cd battery_level_plugin
```

## Implementation

### 1. Dart API Layer

Edit `lib/battery_level_plugin.dart`:

```dart
import 'dart:async';
import 'package:flutter/services.dart';

/// A Flutter plugin for accessing battery information.
///
/// This plugin provides access to the device's battery level and charging
/// status across Android and iOS platforms.
class BatteryLevelPlugin {
  /// Private constructor to enforce singleton pattern
  BatteryLevelPlugin._();

  /// Singleton instance
  static final BatteryLevelPlugin instance = BatteryLevelPlugin._();

  /// Method channel for one-time queries
  static const MethodChannel _methodChannel =
      MethodChannel('com.example.battery_level_plugin/methods');

  /// Event channel for streaming updates
  static const EventChannel _eventChannel =
      EventChannel('com.example.battery_level_plugin/battery');

  /// Gets the current battery level.
  ///
  /// Returns the battery level as a percentage (0-100), or null if unavailable.
  ///
  /// Throws [PlatformException] if the battery level cannot be determined.
  ///
  /// Example:
  /// ```dart
  /// final level = await BatteryLevelPlugin.instance.getBatteryLevel();
  /// print('Battery level: $level%');
  /// ```
  Future<int?> getBatteryLevel() async {
    try {
      final int? batteryLevel =
          await _methodChannel.invokeMethod<int>('getBatteryLevel');
      return batteryLevel;
    } on PlatformException catch (e) {
      print('Failed to get battery level: ${e.message}');
      return null;
    }
  }

  /// Gets detailed battery information.
  ///
  /// Returns a map containing:
  /// - `level`: Battery level (0-100)
  /// - `isCharging`: Whether the device is charging
  /// - `status`: Battery status string
  ///
  /// Example:
  /// ```dart
  /// final info = await BatteryLevelPlugin.instance.getBatteryInfo();
  /// print('Level: ${info['level']}%');
  /// print('Charging: ${info['isCharging']}');
  /// ```
  Future<Map<String, dynamic>?> getBatteryInfo() async {
    try {
      final Map<dynamic, dynamic>? info =
          await _methodChannel.invokeMethod('getBatteryInfo');
      return info?.cast<String, dynamic>();
    } on PlatformException catch (e) {
      print('Failed to get battery info: ${e.message}');
      return null;
    }
  }

  /// Stream of battery level updates.
  ///
  /// Emits the battery level (0-100) whenever it changes.
  ///
  /// Example:
  /// ```dart
  /// BatteryLevelPlugin.instance.batteryLevelStream.listen((level) {
  ///   print('Battery level changed: $level%');
  /// });
  /// ```
  Stream<int> get batteryLevelStream {
    return _eventChannel.receiveBroadcastStream().map((dynamic event) {
      if (event is int) {
        return event;
      }
      throw Exception('Invalid battery level received: $event');
    });
  }
}
```

### 2. Android Implementation

Edit `android/src/main/kotlin/com/example/battery_level_plugin/BatteryLevelPlugin.kt`:

```kotlin
package com.example.battery_level_plugin

import android.content.BroadcastReceiver
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

class BatteryLevelPlugin : FlutterPlugin, MethodCallHandler {
    private lateinit var methodChannel: MethodChannel
    private lateinit var eventChannel: EventChannel
    private lateinit var context: Context
    private var batteryStreamHandler: BatteryStreamHandler? = null

    override fun onAttachedToEngine(@NonNull flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {
        context = flutterPluginBinding.applicationContext

        // Setup method channel
        methodChannel = MethodChannel(
            flutterPluginBinding.binaryMessenger,
            "com.example.battery_level_plugin/methods"
        )
        methodChannel.setMethodCallHandler(this)

        // Setup event channel
        eventChannel = EventChannel(
            flutterPluginBinding.binaryMessenger,
            "com.example.battery_level_plugin/battery"
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
            "getBatteryInfo" -> {
                val info = getBatteryInfo()
                result.success(info)
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

    private fun getBatteryInfo(): Map<String, Any> {
        val level = getBatteryLevel()
        val intent = context.registerReceiver(
            null,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        )

        val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
        val isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING ||
                status == BatteryManager.BATTERY_STATUS_FULL

        val statusString = when (status) {
            BatteryManager.BATTERY_STATUS_CHARGING -> "charging"
            BatteryManager.BATTERY_STATUS_DISCHARGING -> "discharging"
            BatteryManager.BATTERY_STATUS_FULL -> "full"
            BatteryManager.BATTERY_STATUS_NOT_CHARGING -> "not_charging"
            else -> "unknown"
        }

        return mapOf(
            "level" to level,
            "isCharging" to isCharging,
            "status" to statusString
        )
    }

    override fun onDetachedFromEngine(@NonNull binding: FlutterPlugin.FlutterPluginBinding) {
        methodChannel.setMethodCallHandler(null)
        eventChannel.setStreamHandler(null)
        batteryStreamHandler = null
    }
}

class BatteryStreamHandler(private val context: Context) : EventChannel.StreamHandler {
    private var receiver: BroadcastReceiver? = null

    override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
        receiver = object : BroadcastReceiver() {
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
                } else {
                    events.error("UNAVAILABLE", "Battery level not available", null)
                }
            }
        }

        context.registerReceiver(receiver, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
    }

    override fun onCancel(arguments: Any?) {
        receiver?.let { context.unregisterReceiver(it) }
        receiver = null
    }
}
```

### 3. iOS Implementation

Edit `ios/Classes/BatteryLevelPlugin.swift`:

```swift
import Flutter
import UIKit

public class BatteryLevelPlugin: NSObject, FlutterPlugin, FlutterStreamHandler {
    private var eventSink: FlutterEventSink?

    public static func register(with registrar: FlutterPluginRegistrar) {
        let methodChannel = FlutterMethodChannel(
            name: "com.example.battery_level_plugin/methods",
            binaryMessenger: registrar.messenger()
        )
        let eventChannel = FlutterEventChannel(
            name: "com.example.battery_level_plugin/battery",
            binaryMessenger: registrar.messenger()
        )

        let instance = BatteryLevelPlugin()
        registrar.addMethodCallDelegate(instance, channel: methodChannel)
        eventChannel.setStreamHandler(instance)
    }

    public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "getBatteryLevel":
            getBatteryLevel(result: result)
        case "getBatteryInfo":
            getBatteryInfo(result: result)
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

    private func getBatteryInfo(result: FlutterResult) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        let level = Int(device.batteryLevel * 100)
        let isCharging = device.batteryState == .charging || device.batteryState == .full

        let statusString: String
        switch device.batteryState {
        case .unknown:
            statusString = "unknown"
        case .unplugged:
            statusString = "discharging"
        case .charging:
            statusString = "charging"
        case .full:
            statusString = "full"
        @unknown default:
            statusString = "unknown"
        }

        let info: [String: Any] = [
            "level": level,
            "isCharging": isCharging,
            "status": statusString
        ]

        result(info)
    }

    // FlutterStreamHandler implementation
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
        NotificationCenter.default.removeObserver(
            self,
            name: UIDevice.batteryLevelDidChangeNotification,
            object: nil
        )
        NotificationCenter.default.removeObserver(
            self,
            name: UIDevice.batteryStateDidChangeNotification,
            object: nil
        )
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

### 4. Example App

Edit `example/lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:battery_level_plugin/battery_level_plugin.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _plugin = BatteryLevelPlugin.instance;
  int? _batteryLevel;
  bool _isCharging = false;
  String _status = 'Loading...';

  @override
  void initState() {
    super.initState();
    _initPlugin();
  }

  Future<void> _initPlugin() async {
    try {
      // Get initial battery info
      final info = await _plugin.getBatteryInfo();
      if (info != null) {
        setState(() {
          _batteryLevel = info['level'] as int;
          _isCharging = info['isCharging'] as bool;
          _status = info['status'] as String;
        });
      }

      // Listen to battery changes
      _plugin.batteryLevelStream.listen(
        (level) {
          setState(() {
            _batteryLevel = level;
          });
        },
        onError: (error) {
          setState(() {
            _status = 'Error: $error';
          });
        },
      );
    } catch (e) {
      setState(() {
        _status = 'Failed to initialize: $e';
      });
    }
  }

  Future<void> _refreshBatteryInfo() async {
    final info = await _plugin.getBatteryInfo();
    if (info != null) {
      setState(() {
        _batteryLevel = info['level'] as int;
        _isCharging = info['isCharging'] as bool;
        _status = info['status'] as String;
      });
    }
  }

  Color _getBatteryColor() {
    if (_batteryLevel == null) return Colors.grey;
    if (_batteryLevel! > 50) return Colors.green;
    if (_batteryLevel! > 20) return Colors.orange;
    return Colors.red;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Battery Level Plugin Example'),
          actions: [
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: _refreshBatteryInfo,
            ),
          ],
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Battery level circle
                SizedBox(
                  width: 200,
                  height: 200,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      CircularProgressIndicator(
                        value: _batteryLevel != null ? _batteryLevel! / 100 : 0,
                        strokeWidth: 20,
                        backgroundColor: Colors.grey[300],
                        valueColor: AlwaysStoppedAnimation<Color>(
                          _getBatteryColor(),
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            _batteryLevel != null ? '$_batteryLevel%' : '--',
                            style: const TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          if (_isCharging)
                            const Icon(
                              Icons.bolt,
                              color: Colors.amber,
                              size: 32,
                            ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
                // Status information
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildInfoRow('Status:', _status),
                        const SizedBox(height: 8),
                        _buildInfoRow(
                          'Charging:',
                          _isCharging ? 'Yes' : 'No',
                        ),
                        const SizedBox(height: 8),
                        _buildInfoRow(
                          'Level:',
                          _batteryLevel != null ? '$_batteryLevel%' : 'Unknown',
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
        Text(
          value,
          style: const TextStyle(fontSize: 16),
        ),
      ],
    );
  }
}
```

## Testing the Plugin

Run the example app:

```bash
cd example
flutter run
```

## Key Takeaways

1. **Clean API Design**: The Dart API provides a simple, intuitive interface
2. **Platform Channels**: MethodChannel for queries, EventChannel for streams
3. **Error Handling**: Proper exception handling on both Dart and native sides
4. **Cross-Platform**: Same API works on both Android and iOS
5. **Real-time Updates**: EventChannel enables streaming battery changes
6. **Complete Example**: Full working app demonstrates all features

This plugin demonstrates the fundamental patterns for creating Flutter plugins that access platform-specific functionality.
