# Platform Views Reference

Platform views enable embedding native UI components from Android (Views) and iOS (UIViews) directly into Flutter applications. This allows you to leverage platform-specific widgets and UI components that aren't available in Flutter's widget catalog.

## Overview

Platform views are Flutter widgets that display native platform UI components. They integrate seamlessly with Flutter's widget tree and support standard Flutter operations like transforms, opacity, and clipping.

### When to Use Platform Views

**Good Use Cases:**
- Integrating third-party native SDKs with custom UI (Google Maps, ads, video players)
- Using platform-specific UI components (WebView, MapView)
- Displaying native controls with complex platform-specific behavior
- Leveraging hardware-accelerated rendering from native libraries

**Avoid When:**
- Flutter alternatives exist with similar functionality
- Performance is critical (use Flutter widgets when possible)
- Simple UI that can be built with Flutter widgets
- Need extensive customization (build with Flutter instead)

### Performance Considerations

Platform views have performance overhead:
- Additional compositing layers
- Memory overhead from platform view buffers
- Potential frame drops during complex animations
- GPU memory usage

**Optimization Strategies:**
- Use placeholder textures during animations
- Take screenshots and display as images during transitions
- Minimize number of platform views
- Profile performance with DevTools

## Android Platform Views

Android supports two composition modes, each with different performance characteristics.

### Composition Modes

#### 1. Hybrid Composition (Recommended)

Native Android views render normally; Flutter content renders to texture.

**Advantages:**
- Best fidelity for Android views
- Native view behavior preserved
- Proper z-ordering

**Disadvantages:**
- Lower Flutter rendering FPS
- Some transforms don't work
- Performance impact on older devices

**Requirements:** Android API 19+ (KitKat)

#### 2. Texture Layer Hybrid Composition

Android views render to texture; Flutter draws from texture.

**Advantages:**
- Better Flutter rendering performance
- All transforms work correctly
- Minimal FPS impact

**Disadvantages:**
- Jank during fast scrolling
- SurfaceView issues (accessibility breaks)
- Text magnifier problems
- Requires TextureView mode for some features

**Requirements:** Android API 20+ (Lollipop)

### Dart Implementation - Hybrid Composition

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';

class NativeMapView extends StatelessWidget {
  const NativeMapView({super.key});

  @override
  Widget build(BuildContext context) {
    const String viewType = 'native-map-view';
    final Map<String, dynamic> creationParams = {
      'latitude': 37.7749,
      'longitude': -122.4194,
      'zoom': 12.0,
    };

    return PlatformViewLink(
      viewType: viewType,
      surfaceFactory: (context, controller) {
        return AndroidViewSurface(
          controller: controller as AndroidViewController,
          gestureRecognizers: const <Factory<OneSequenceGestureRecognizer>>{
            Factory<PanGestureRecognizer>(PanGestureRecognizer.new),
            Factory<ScaleGestureRecognizer>(ScaleGestureRecognizer.new),
            Factory<TapGestureRecognizer>(TapGestureRecognizer.new),
          },
          hitTestBehavior: PlatformViewHitTestBehavior.opaque,
        );
      },
      onCreatePlatformView: (PlatformViewCreationParams params) {
        return PlatformViewsService.initSurfaceAndroidView(
          id: params.id,
          viewType: viewType,
          layoutDirection: TextDirection.ltr,
          creationParams: creationParams,
          creationParamsCodec: const StandardMessageCodec(),
          onFocus: () {
            params.onFocusChanged(true);
          },
        )
          ..addOnPlatformViewCreatedListener(params.onPlatformViewCreated)
          ..create();
      },
    );
  }
}
```

### Dart Implementation - Texture Layer

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NativeTextureView extends StatelessWidget {
  const NativeTextureView({super.key});

  @override
  Widget build(BuildContext context) {
    const String viewType = 'native-texture-view';
    final Map<String, dynamic> creationParams = {
      'text': 'Hello from native!',
      'backgroundColor': '#FF0000',
    };

    return AndroidView(
      viewType: viewType,
      layoutDirection: TextDirection.ltr,
      creationParams: creationParams,
      creationParamsCodec: const StandardMessageCodec(),
      onPlatformViewCreated: (int id) {
        print('Platform view created: $id');
      },
    );
  }
}
```

### Android Native Implementation

#### PlatformView Class

```kotlin
package com.example.app

import android.content.Context
import android.graphics.Color
import android.view.View
import android.widget.TextView
import io.flutter.plugin.platform.PlatformView

class NativeView(
    context: Context,
    id: Int,
    creationParams: Map<String?, Any?>?
) : PlatformView {
    private val textView: TextView

    init {
        textView = TextView(context).apply {
            // Extract parameters
            val text = creationParams?.get("text") as? String ?: "Native View"
            val bgColor = creationParams?.get("backgroundColor") as? String

            // Configure view
            this.text = text
            textSize = 20f
            setTextColor(Color.WHITE)
            setPadding(32, 32, 32, 32)

            // Parse and set background color
            bgColor?.let {
                try {
                    setBackgroundColor(Color.parseColor(it))
                } catch (e: IllegalArgumentException) {
                    setBackgroundColor(Color.BLUE)
                }
            } ?: setBackgroundColor(Color.BLUE)
        }
    }

    override fun getView(): View {
        return textView
    }

    override fun dispose() {
        // Clean up resources
    }

    // Optional: Add methods to update view
    fun updateText(text: String) {
        textView.text = text
    }
}
```

#### Factory Class

```kotlin
package com.example.app

import android.content.Context
import io.flutter.plugin.common.StandardMessageCodec
import io.flutter.plugin.platform.PlatformView
import io.flutter.plugin.platform.PlatformViewFactory

class NativeViewFactory : PlatformViewFactory(StandardMessageCodec.INSTANCE) {
    override fun create(
        context: Context,
        viewId: Int,
        args: Any?
    ): PlatformView {
        val creationParams = args as? Map<String?, Any?>
        return NativeView(context, viewId, creationParams)
    }
}
```

#### Registration in MainActivity

```kotlin
package com.example.app

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        flutterEngine
            .platformViewsController
            .registry
            .registerViewFactory(
                "native-map-view",
                NativeViewFactory()
            )

        flutterEngine
            .platformViewsController
            .registry
            .registerViewFactory(
                "native-texture-view",
                NativeViewFactory()
            )
    }
}
```

#### Gradle Configuration

```gradle
android {
    defaultConfig {
        minSdk = 19  // For hybrid composition
        // minSdk = 20  // For texture layer composition
    }
}
```

### Complex Android View Example

```kotlin
package com.example.app

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.platform.PlatformView

class ComplexNativeView(
    context: Context,
    id: Int,
    creationParams: Map<String?, Any?>?,
    private val messenger: io.flutter.plugin.common.BinaryMessenger
) : PlatformView, MethodChannel.MethodCallHandler {
    private val rootView: LinearLayout
    private val titleTextView: TextView
    private val counterTextView: TextView
    private val incrementButton: Button
    private var counter = 0

    private val methodChannel: MethodChannel

    init {
        // Inflate layout
        rootView = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 16, 16, 16)
        }

        // Create views
        titleTextView = TextView(context).apply {
            text = creationParams?.get("title") as? String ?: "Counter"
            textSize = 24f
        }

        counterTextView = TextView(context).apply {
            text = "0"
            textSize = 48f
        }

        incrementButton = Button(context).apply {
            text = "Increment"
            setOnClickListener {
                counter++
                updateCounter()
                notifyFlutter()
            }
        }

        // Add views to root
        rootView.addView(titleTextView)
        rootView.addView(counterTextView)
        rootView.addView(incrementButton)

        // Setup method channel for communication
        methodChannel = MethodChannel(messenger, "native_view_$id")
        methodChannel.setMethodCallHandler(this)
    }

    override fun getView(): View = rootView

    override fun dispose() {
        methodChannel.setMethodCallHandler(null)
    }

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "reset" -> {
                counter = 0
                updateCounter()
                result.success(null)
            }
            "setCounter" -> {
                val value = call.argument<Int>("value")
                if (value != null) {
                    counter = value
                    updateCounter()
                    result.success(null)
                } else {
                    result.error("INVALID_ARGUMENT", "value required", null)
                }
            }
            else -> result.notImplemented()
        }
    }

    private fun updateCounter() {
        counterTextView.text = counter.toString()
    }

    private fun notifyFlutter() {
        methodChannel.invokeMethod("onCounterChanged", mapOf("value" to counter))
    }
}
```

## iOS Platform Views

iOS uses hybrid composition exclusively, appending the native UIView to the view hierarchy.

### Dart Implementation

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NativeIOSMapView extends StatelessWidget {
  const NativeIOSMapView({super.key});

  @override
  Widget build(BuildContext context) {
    const String viewType = 'native-ios-map-view';
    final Map<String, dynamic> creationParams = {
      'latitude': 37.7749,
      'longitude': -122.4194,
      'zoom': 12.0,
    };

    return UiKitView(
      viewType: viewType,
      layoutDirection: TextDirection.ltr,
      creationParams: creationParams,
      creationParamsCodec: const StandardMessageCodec(),
      onPlatformViewCreated: (int id) {
        print('iOS platform view created: $id');
      },
    );
  }
}
```

### iOS Native Implementation (Swift)

#### PlatformView Class

```swift
import Flutter
import UIKit

class NativeView: NSObject, FlutterPlatformView {
    private let frame: CGRect
    private let viewId: Int64
    private let label: UILabel
    private let containerView: UIView

    init(
        frame: CGRect,
        viewId: Int64,
        arguments: Any?,
        binaryMessenger: FlutterBinaryMessenger
    ) {
        self.frame = frame
        self.viewId = viewId

        // Create container view
        containerView = UIView(frame: frame)
        containerView.backgroundColor = .systemBlue

        // Create label
        label = UILabel(frame: CGRect(x: 0, y: 0, width: frame.width, height: 50))
        label.textAlignment = .center
        label.textColor = .white
        label.font = .systemFont(ofSize: 20, weight: .bold)

        // Parse arguments
        if let args = arguments as? [String: Any],
           let text = args["text"] as? String {
            label.text = text
        } else {
            label.text = "Native iOS View"
        }

        containerView.addSubview(label)

        super.init()
    }

    func view() -> UIView {
        return containerView
    }

    func updateText(_ text: String) {
        label.text = text
    }
}
```

#### Factory Class

```swift
import Flutter
import UIKit

class NativeViewFactory: NSObject, FlutterPlatformViewFactory {
    private let messenger: FlutterBinaryMessenger

    init(messenger: FlutterBinaryMessenger) {
        self.messenger = messenger
        super.init()
    }

    func create(
        withFrame frame: CGRect,
        viewIdentifier viewId: Int64,
        arguments args: Any?
    ) -> FlutterPlatformView {
        return NativeView(
            frame: frame,
            viewId: viewId,
            arguments: args,
            binaryMessenger: messenger
        )
    }

    func createArgsCodec() -> FlutterMessageCodec & NSObjectProtocol {
        return FlutterStandardMessageCodec.sharedInstance()
    }
}
```

#### Registration in AppDelegate

```swift
import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController

        // Register platform view factory
        guard let registrar = self.registrar(forPlugin: "NativeView") else {
            return false
        }

        let factory = NativeViewFactory(messenger: registrar.messenger())
        registrar.register(factory, withId: "native-ios-map-view")

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
```

### Complex iOS View Example

```swift
import Flutter
import UIKit

class ComplexNativeView: NSObject, FlutterPlatformView {
    private let containerView: UIView
    private let titleLabel: UILabel
    private let counterLabel: UILabel
    private let incrementButton: UIButton
    private var counter = 0
    private let methodChannel: FlutterMethodChannel

    init(
        frame: CGRect,
        viewId: Int64,
        arguments: Any?,
        binaryMessenger: FlutterBinaryMessenger
    ) {
        // Create container
        containerView = UIView(frame: frame)
        containerView.backgroundColor = .systemBackground

        // Create title label
        titleLabel = UILabel()
        titleLabel.font = .systemFont(ofSize: 24, weight: .bold)
        titleLabel.textAlignment = .center
        titleLabel.translatesAutoresizingMaskIntoConstraints = false

        // Parse arguments
        if let args = arguments as? [String: Any],
           let title = args["title"] as? String {
            titleLabel.text = title
        } else {
            titleLabel.text = "Counter"
        }

        // Create counter label
        counterLabel = UILabel()
        counterLabel.text = "0"
        counterLabel.font = .systemFont(ofSize: 48, weight: .bold)
        counterLabel.textAlignment = .center
        counterLabel.translatesAutoresizingMaskIntoConstraints = false

        // Create button
        incrementButton = UIButton(type: .system)
        incrementButton.setTitle("Increment", for: .normal)
        incrementButton.titleLabel?.font = .systemFont(ofSize: 18)
        incrementButton.translatesAutoresizingMaskIntoConstraints = false

        // Add subviews
        containerView.addSubview(titleLabel)
        containerView.addSubview(counterLabel)
        containerView.addSubview(incrementButton)

        // Setup method channel
        methodChannel = FlutterMethodChannel(
            name: "native_view_\(viewId)",
            binaryMessenger: binaryMessenger
        )

        super.init()

        // Setup constraints
        NSLayoutConstraint.activate([
            titleLabel.topAnchor.constraint(
                equalTo: containerView.topAnchor,
                constant: 20
            ),
            titleLabel.leadingAnchor.constraint(
                equalTo: containerView.leadingAnchor,
                constant: 20
            ),
            titleLabel.trailingAnchor.constraint(
                equalTo: containerView.trailingAnchor,
                constant: -20
            ),

            counterLabel.centerYAnchor.constraint(
                equalTo: containerView.centerYAnchor
            ),
            counterLabel.centerXAnchor.constraint(
                equalTo: containerView.centerXAnchor
            ),

            incrementButton.topAnchor.constraint(
                equalTo: counterLabel.bottomAnchor,
                constant: 20
            ),
            incrementButton.centerXAnchor.constraint(
                equalTo: containerView.centerXAnchor
            ),
        ])

        // Setup button action
        incrementButton.addTarget(
            self,
            action: #selector(incrementTapped),
            for: .touchUpInside
        )

        // Setup method call handler
        methodChannel.setMethodCallHandler { [weak self] (call, result) in
            self?.handleMethodCall(call: call, result: result)
        }
    }

    func view() -> UIView {
        return containerView
    }

    @objc private func incrementTapped() {
        counter += 1
        updateCounter()
        notifyFlutter()
    }

    private func updateCounter() {
        counterLabel.text = "\(counter)"
    }

    private func notifyFlutter() {
        methodChannel.invokeMethod(
            "onCounterChanged",
            arguments: ["value": counter]
        )
    }

    private func handleMethodCall(
        call: FlutterMethodCall,
        result: @escaping FlutterResult
    ) {
        switch call.method {
        case "reset":
            counter = 0
            updateCounter()
            result(nil)
        case "setCounter":
            if let args = call.arguments as? [String: Any],
               let value = args["value"] as? Int {
                counter = value
                updateCounter()
                result(nil)
            } else {
                result(FlutterError(
                    code: "INVALID_ARGUMENT",
                    message: "value required",
                    details: nil
                ))
            }
        default:
            result(FlutterMethodNotImplemented)
        }
    }
}
```

## Multi-Platform Support

### Platform Detection

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PlatformMapView extends StatelessWidget {
  const PlatformMapView({super.key});

  @override
  Widget build(BuildContext context) {
    const String viewType = 'platform-map-view';
    final Map<String, dynamic> creationParams = {
      'latitude': 37.7749,
      'longitude': -122.4194,
      'zoom': 12.0,
    };

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return AndroidView(
          viewType: viewType,
          layoutDirection: TextDirection.ltr,
          creationParams: creationParams,
          creationParamsCodec: const StandardMessageCodec(),
        );

      case TargetPlatform.iOS:
        return UiKitView(
          viewType: viewType,
          layoutDirection: TextDirection.ltr,
          creationParams: creationParams,
          creationParamsCodec: const StandardMessageCodec(),
        );

      default:
        return Container(
          color: Colors.grey,
          child: const Center(
            child: Text('Platform views not supported on this platform'),
          ),
        );
    }
  }
}
```

### Fallback Implementation

```dart
class SafePlatformView extends StatelessWidget {
  const SafePlatformView({super.key});

  bool get _isPlatformViewSupported {
    return defaultTargetPlatform == TargetPlatform.android ||
           defaultTargetPlatform == TargetPlatform.iOS;
  }

  @override
  Widget build(BuildContext context) {
    if (_isPlatformViewSupported) {
      return const PlatformMapView();
    }

    // Fallback to Flutter implementation
    return Container(
      decoration: BoxDecoration(
        color: Colors.blue[100],
        borderRadius: BorderRadius.circular(8),
      ),
      child: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.map, size: 64, color: Colors.blue),
            SizedBox(height: 16),
            Text(
              'Map View',
              style: TextStyle(fontSize: 20),
            ),
            Text('Flutter fallback implementation'),
          ],
        ),
      ),
    );
  }
}
```

## Communication Between Flutter and Native Views

### Dart to Native

```dart
class InteractivePlatformView extends StatefulWidget {
  const InteractivePlatformView({super.key});

  @override
  State<InteractivePlatformView> createState() =>
      _InteractivePlatformViewState();
}

class _InteractivePlatformViewState extends State<InteractivePlatformView> {
  MethodChannel? _channel;
  int _counter = 0;

  void _onPlatformViewCreated(int id) {
    _channel = MethodChannel('native_view_$id');

    _channel!.setMethodCallHandler((call) async {
      if (call.method == 'onCounterChanged') {
        final value = call.arguments['value'] as int;
        setState(() {
          _counter = value;
        });
      }
    });
  }

  Future<void> _resetCounter() async {
    await _channel?.invokeMethod('reset');
  }

  Future<void> _setCounter(int value) async {
    await _channel?.invokeMethod('setCounter', {'value': value});
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: AndroidView(
            viewType: 'complex-native-view',
            onPlatformViewCreated: _onPlatformViewCreated,
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Text('Counter: $_counter', style: const TextStyle(fontSize: 18)),
              ElevatedButton(
                onPressed: _resetCounter,
                child: const Text('Reset'),
              ),
              ElevatedButton(
                onPressed: () => _setCounter(10),
                child: const Text('Set to 10'),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

## Performance Optimization

### Placeholder During Animations

```dart
class OptimizedPlatformView extends StatefulWidget {
  const OptimizedPlatformView({super.key});

  @override
  State<OptimizedPlatformView> createState() => _OptimizedPlatformViewState();
}

class _OptimizedPlatformViewState extends State<OptimizedPlatformView> {
  bool _isAnimating = false;
  Uint8List? _placeholder;

  Future<void> _captureSnapshot() async {
    // Capture screenshot of platform view
    // Store in _placeholder
  }

  @override
  Widget build(BuildContext context) {
    if (_isAnimating && _placeholder != null) {
      return Image.memory(_placeholder!);
    }

    return const AndroidView(
      viewType: 'native-view',
    );
  }
}
```

### Lazy Loading

```dart
class LazyPlatformView extends StatefulWidget {
  const LazyPlatformView({super.key});

  @override
  State<LazyPlatformView> createState() => _LazyPlatformViewState();
}

class _LazyPlatformViewState extends State<LazyPlatformView> {
  bool _isVisible = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: () => setState(() => _isVisible = !_isVisible),
          child: Text(_isVisible ? 'Hide' : 'Show'),
        ),
        if (_isVisible)
          const SizedBox(
            height: 300,
            child: AndroidView(viewType: 'native-view'),
          ),
      ],
    );
  }
}
```

## Limitations and Workarounds

### iOS Composition Limitations

**Not Supported:**
- `ShaderMask`
- `ColorFiltered`

**Partially Supported:**
- `BackdropFilter` (has limitations)

**Workaround:** Use Flutter alternatives or avoid these widgets with platform views.

### Android Surface Views

SurfaceView components are problematic:
- Move to virtual display in texture mode
- Break accessibility
- Should be avoided when possible

**Workaround:** Use TextureView or Flutter alternatives.

### Gesture Conflicts

Platform views may intercept gestures meant for Flutter.

**Solution:** Configure gesture recognizers:

```dart
AndroidViewSurface(
  controller: controller,
  gestureRecognizers: const <Factory<OneSequenceGestureRecognizer>>{
    Factory<PanGestureRecognizer>(PanGestureRecognizer.new),
    Factory<ScaleGestureRecognizer>(ScaleGestureRecognizer.new),
  },
  hitTestBehavior: PlatformViewHitTestBehavior.opaque,
)
```

## Best Practices

### Use Sparingly
- Prefer Flutter widgets when possible
- Only use for truly platform-specific UI
- Consider performance impact

### Performance
- Profile with DevTools
- Use placeholders during animations
- Minimize number of platform views
- Monitor memory usage

### Testing
- Test on multiple devices
- Verify gesture handling
- Check performance under load
- Test composition edge cases

### Documentation
- Document platform requirements
- Note performance considerations
- Explain gesture handling
- Provide usage examples

## Related Resources

- [Platform Channels](platform-channels.md)
- [Android Integration](android-integration.md)
- [iOS Integration](ios-integration.md)
- [Plugin Development](plugin-development.md)
