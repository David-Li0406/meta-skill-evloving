---
name: flutter-platform-integration
description: Comprehensive guidance on Flutter platform integration including platform channels, native code integration, plugin development, and platform views. Use when working with platform-specific features, creating plugins, or integrating native Android/iOS code with Flutter applications.
version: 1.0.0
---

# Flutter Platform Integration Skill

This skill provides comprehensive guidance on Flutter platform integration, covering platform channels, native code integration, plugin development, and platform views. Use this skill when working with platform-specific features, creating plugins, or integrating native Android/iOS code with Flutter applications.

## When to Use This Skill

Use this skill when:

1. **Platform Channel Communication**: Implementing MethodChannel, EventChannel, or BasicMessageChannel for Flutter-native communication
2. **Native Code Integration**: Calling Android (Kotlin/Java) or iOS (Swift/Objective-C) code from Dart
3. **Plugin Development**: Creating reusable Flutter plugins for pub.dev or internal use
4. **Platform Views**: Embedding native Android views or iOS UIKit views in Flutter apps
5. **Platform-Specific Features**: Accessing device capabilities not available through Dart alone
6. **FFI Integration**: Binding to native C/C++ libraries using dart:ffi
7. **Custom Native UI**: Integrating native UI components that aren't available in Flutter
8. **Hardware Access**: Working with cameras, sensors, battery status, or other device features

## Skill Overview

Flutter's platform integration system enables you to build cross-platform apps while accessing platform-specific functionality when needed. This skill covers the complete spectrum from simple method calls to complex native integrations.

### Core Concepts

**Platform Channels**: Asynchronous message-passing channels between Flutter (Dart) and native code:
- **MethodChannel**: One-way method invocations with return values (most common)
- **EventChannel**: Streaming data from native to Flutter (sensors, location updates)
- **BasicMessageChannel**: Bidirectional message passing

**Native Integration**: Three primary approaches:
- **Platform Channels**: String-based method calls with StandardMessageCodec
- **Pigeon**: Type-safe code generation for platform communication
- **FFI (Foreign Function Interface)**: Direct C/C++ library bindings

**Plugin Architecture**: Reusable packages combining Dart APIs with platform-specific implementations:
- **Dart Packages**: Pure Dart code (no native code)
- **Plugin Packages**: Dart + native code (Android, iOS, web, desktop)
- **Federated Plugins**: Modular architecture with platform-specific packages

### Architecture Pattern

The typical platform integration flow:

```
┌─────────────────────────────────────────────────────┐
│                    Flutter (Dart)                   │
│  ┌──────────────────────────────────────────────┐  │
│  │          Your Flutter Widget/App             │  │
│  └────────────────┬─────────────────────────────┘  │
│                   │                                 │
│  ┌────────────────▼─────────────────────────────┐  │
│  │    MethodChannel / EventChannel / FFI        │  │
│  └────────────────┬─────────────────────────────┘  │
└───────────────────┼─────────────────────────────────┘
                    │ Asynchronous Messages
┌───────────────────▼─────────────────────────────────┐
│             Platform-Specific Code                  │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │  Android         │      │  iOS             │    │
│  │  (Kotlin/Java)   │      │  (Swift/Obj-C)   │    │
│  └──────────────────┘      └──────────────────┘    │
│                                                     │
│  Platform APIs: Camera, Location, Battery, etc.    │
└─────────────────────────────────────────────────────┘
```

### Key Principles

**1. Asynchronous by Design**: All platform channel communications are asynchronous to maintain UI responsiveness. Never block the UI thread waiting for native responses.

**2. Type-Safe Communication**: Use StandardMessageCodec for automatic type conversion between Dart and native types, or leverage Pigeon for compile-time type safety.

**3. Main Thread Constraint**: Channel method handlers must execute on the platform's main thread (UI thread). Use dispatchers/handlers to switch threads when needed.

**4. Error Handling**: Always implement robust error handling on both sides:
- Dart: Catch `PlatformException` with try-catch blocks
- Native: Return error codes, messages, and details for debugging

**5. Cross-Platform Consistency**: Design APIs that work consistently across platforms while respecting platform-specific conventions and limitations.

## Reference Documentation

This skill includes comprehensive reference documentation:

- **[Platform Channels](references/platform-channels.md)**: MethodChannel, EventChannel, message codecs, threading, and Pigeon integration
- **[Android Integration](references/android-integration.md)**: Kotlin/Java integration, JNI, Gradle configuration, and Android-specific patterns
- **[iOS Integration](references/ios-integration.md)**: Swift/Objective-C integration, CocoaPods, Xcode configuration, and iOS-specific patterns
- **[Plugin Development](references/plugin-development.md)**: Creating plugins, federated architecture, publishing to pub.dev, and best practices
- **[Platform Views](references/platform-views.md)**: Embedding native Android views and iOS UIKit views in Flutter apps

## Practical Examples

This skill includes complete working examples:

- **[Custom Plugin Example](examples/custom-plugin.md)**: Battery level plugin demonstrating MethodChannel implementation for Android and iOS
- **[Native Features](examples/native-features.md)**: Camera integration showing EventChannel, permissions, and platform-specific UI

## Development Workflow

### 1. Design Phase
- Identify platform-specific requirements
- Choose integration approach (channels vs FFI vs existing plugins)
- Design cross-platform API surface
- Document platform limitations and differences

### 2. Implementation Phase
- Create plugin or add platform channels to existing app
- Implement Dart API layer
- Write platform-specific code (Android, iOS, etc.)
- Connect Dart and native via channels or FFI
- Handle errors and edge cases on both sides

### 3. Testing Phase
- Unit test Dart API layer
- Test native implementations separately
- Integration test cross-platform behavior
- Test error handling and edge cases
- Verify threading and performance

### 4. Documentation Phase
- Document public APIs with dartdoc comments
- Provide usage examples and code samples
- Document platform-specific requirements
- Create README with setup instructions
- Maintain CHANGELOG for versions

### 5. Publication Phase (for plugins)
- Validate with `flutter pub publish --dry-run`
- Ensure all metadata is complete (pubspec.yaml)
- Add Flutter Favorite criteria where applicable
- Publish to pub.dev
- Monitor issues and feedback

## Best Practices

### API Design
- **Simplicity First**: Expose simple, intuitive Dart APIs regardless of native complexity
- **Consistency**: Maintain consistent naming and patterns across platforms
- **Async/Await**: Use Future-based APIs for asynchronous operations
- **Null Safety**: Fully support Dart null safety with proper annotations
- **Documentation**: Provide comprehensive dartdoc comments with examples

### Platform Channels
- **Unique Names**: Use reverse domain notation for channel names (e.g., `com.example.app/battery`)
- **Type Safety**: Consider Pigeon for type-safe code generation
- **Error Handling**: Always catch `PlatformException` and provide helpful error messages
- **Threading**: Ensure handlers run on main thread; offload heavy work to background
- **Data Types**: Use StandardMessageCodec-supported types or custom codecs

### Native Code
- **Separation of Concerns**: Keep channel logic separate from business logic
- **Platform Conventions**: Follow platform-specific naming and architectural patterns
- **Resource Management**: Properly manage native resources (memory, file handles, etc.)
- **Permissions**: Handle runtime permissions gracefully with clear user messaging
- **Backward Compatibility**: Support reasonable range of OS versions

### Plugin Development
- **Modular Design**: Consider federated plugins for large projects
- **Examples**: Include comprehensive example app demonstrating all features
- **Testing**: Provide unit tests for Dart code and native code where possible
- **Documentation**: Maintain README, CHANGELOG, and API documentation
- **Versioning**: Follow semantic versioning strictly

### Performance
- **Minimize Crossings**: Reduce frequency of platform channel calls
- **Batch Operations**: Combine multiple operations into single calls when possible
- **Background Work**: Move heavy computation off the main thread
- **Memory Management**: Be mindful of data copied across channel boundaries
- **Platform Views**: Use sparingly due to performance overhead; prefer placeholder textures during animations

## Common Patterns

### Pattern 1: Simple Method Call
```dart
// Dart
final result = await platform.invokeMethod('getBatteryLevel');
```

### Pattern 2: Method with Arguments
```dart
// Dart
final result = await platform.invokeMethod('processImage', {
  'path': imagePath,
  'quality': 85,
});
```

### Pattern 3: Event Streaming
```dart
// Dart
final stream = EventChannel('com.example/events').receiveBroadcastStream();
stream.listen((event) => handleEvent(event));
```

### Pattern 4: Error Handling
```dart
// Dart
try {
  final result = await platform.invokeMethod('riskyOperation');
} on PlatformException catch (e) {
  print('Error: ${e.code} - ${e.message}');
}
```

### Pattern 5: Multi-Platform Support
```dart
// Dart
switch (defaultTargetPlatform) {
  case TargetPlatform.android:
    return AndroidView(viewType: 'my-view');
  case TargetPlatform.iOS:
    return UiKitView(viewType: 'my-view');
  default:
    throw UnsupportedError('Platform not supported');
}
```

## Tools and Resources

### Development Tools
- **Android Studio**: For Android native development and debugging
- **Xcode**: For iOS native development and debugging
- **VS Code**: With Flutter and platform-specific extensions
- **ffigen**: For generating FFI bindings from C headers
- **Pigeon**: For type-safe platform channel code generation

### Official Resources
- [Platform Integration Docs](https://docs.flutter.dev/platform-integration/)
- [Developing Packages & Plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages)
- [Platform Channels](https://docs.flutter.dev/platform-integration/platform-channels)
- [pub.dev](https://pub.dev): Flutter package repository

### Code Generation
- [Pigeon Package](https://pub.dev/packages/pigeon): Type-safe platform channels
- [ffigen Package](https://pub.dev/packages/ffigen): FFI binding generation

## Troubleshooting

### Common Issues

**MissingPluginException**: Plugin not registered properly
- Android: Check MainActivity.kt registers the plugin
- iOS: Check AppDelegate.swift registers the plugin
- Run `flutter clean` and rebuild

**PlatformException**: Native code threw an error
- Check native logs (logcat for Android, Console.app for iOS)
- Verify error handling in native code
- Ensure method names match exactly

**Type Mismatch**: Data not serializing correctly
- Verify types are supported by StandardMessageCodec
- Check null handling on both sides
- Consider custom MessageCodec if needed

**Threading Issues**: Crashes or unresponsive UI
- Ensure handlers run on main thread
- Move heavy work to background threads
- Use proper dispatchers/handlers to switch threads

**Platform View Performance**: Laggy animations
- Use placeholder textures during animations
- Consider flutter-only alternatives
- Profile with DevTools to identify bottlenecks

## Advanced Topics

### Custom Message Codecs
Create custom codecs for complex data types not supported by StandardMessageCodec.

### Background Isolates
Use `BackgroundIsolateBinaryMessenger` to invoke platform channels from isolates other than the root isolate.

### Federated Plugin Architecture
Split plugins into app-facing interface, platform interface, and platform implementations for modularity and maintainability.

### FFI vs Platform Channels
Choose FFI for synchronous, low-level C/C++ library access. Choose platform channels for platform APIs and async operations.

### Platform-Specific Implementations
Implement features on some platforms while gracefully degrading on others. Document platform support clearly.

## Related Skills

- **Flutter Core**: Fundamental Flutter concepts and patterns
- **Flutter State Management**: Managing state across platform integrations
- **Flutter Testing**: Testing platform-specific code and plugins
- **Dart FFI**: Deep dive into Foreign Function Interface

## Conclusion

Flutter's platform integration system provides a powerful bridge between cross-platform Dart code and native platform capabilities. Whether you're calling a simple native API, creating a comprehensive plugin, or embedding native UI components, the patterns and practices in this skill will guide you toward robust, maintainable implementations.

Start with platform channels for most use cases, leverage Pigeon for type safety when complexity grows, and consider FFI for direct C/C++ library access. Always prioritize error handling, documentation, and cross-platform consistency to create excellent developer experiences.

For specific implementation details, consult the reference documentation and examples provided in this skill.
