---
name: fullstory-logging-mobile
version: v3
platforms:
  - ios
  - android
  - flutter
  - react-native
sdks:
  - fullstory-swift
  - fullstory-android
  - fullstory-flutter
  - fullstory-react-native
description: Mobile implementation guide for Fullstory's Logging API. Includes API reference and code examples for iOS, Android, Flutter, and React Native.
parent_skill: fullstory-logging
related_skills:
  - fullstory-logging
  - fullstory-analytics-events
---

# Fullstory Logging — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for log levels and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | Method |
|----------|--------|
| iOS | `FS.log(level: .info, msg: "message")` |
| Android | `FS.log(FS.LogLevel.INFO, "message")` |
| Flutter | `FS.log(level: LogLevel.info, msg: "message")` |
| React Native | `FullStory.log(LogLevel.Info, "message")` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Log with level
FS.log(level: .info, msg: "Your message here")

// Log levels
FS.LogLevel.log
FS.LogLevel.debug
FS.LogLevel.info
FS.LogLevel.warn
FS.LogLevel.error
```

### ✅ GOOD Implementation Examples

```swift
// GOOD: Error logging with context
func logError(_ error: Error, context: [String: Any] = [:]) {
    let contextString = context.isEmpty ? "" : " | Context: \(context)"
    FS.log(level: .error, msg: "Error: \(error.localizedDescription)\(contextString)")
}

// GOOD: API response logging
func logAPIResponse(url: String, statusCode: Int, duration: TimeInterval) {
    let level: FS.LogLevel = statusCode >= 400 ? .warn : .info
    FS.log(level: level, msg: "API \(statusCode): \(url) (\(Int(duration * 1000))ms)")
}

// GOOD: Centralized logger
struct AppLogger {
    static func info(_ message: String) {
        FS.log(level: .info, msg: "[INFO] \(message)")
    }
    
    static func error(_ message: String, error: Error? = nil) {
        var msg = "[ERROR] \(message)"
        if let error = error {
            msg += "\nError: \(error.localizedDescription)"
        }
        FS.log(level: .error, msg: msg)
    }
}
```

---

## Android (Kotlin)

### API Reference

```kotlin
import com.fullstory.FS

// Log with level
FS.log(FS.LogLevel.INFO, "Your message here")

// Log levels
FS.LogLevel.LOG
FS.LogLevel.DEBUG
FS.LogLevel.INFO
FS.LogLevel.WARN
FS.LogLevel.ERROR
```

### ✅ GOOD Implementation Examples

```kotlin
// GOOD: Error logging with context
fun logError(error: Throwable, context: Map<String, Any> = emptyMap()) {
    val contextString = if (context.isEmpty()) "" else " | Context: $context"
    FS.log(FS.LogLevel.ERROR, "Error: ${error.message}$contextString")
}

// GOOD: API response logging
fun logAPIResponse(url: String, statusCode: Int, durationMs: Long) {
    val level = if (statusCode >= 400) FS.LogLevel.WARN else FS.LogLevel.INFO
    FS.log(level, "API $statusCode: $url (${durationMs}ms)")
}

// GOOD: Centralized logger
object AppLogger {
    fun info(message: String) {
        FS.log(FS.LogLevel.INFO, "[INFO] $message")
    }
    
    fun error(message: String, error: Throwable? = null) {
        var msg = "[ERROR] $message"
        error?.let { msg += "\nError: ${it.message}" }
        FS.log(FS.LogLevel.ERROR, msg)
    }
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Log with level
FS.log(level: LogLevel.info, msg: 'Your message here');

// Log levels
LogLevel.log
LogLevel.debug
LogLevel.info
LogLevel.warn
LogLevel.error
```

### ✅ GOOD Implementation Examples

```dart
// GOOD: Error logging with context
void logError(Object error, {Map<String, dynamic>? context}) {
  final contextString = context?.isNotEmpty == true ? ' | Context: $context' : '';
  FS.log(level: LogLevel.error, msg: 'Error: $error$contextString');
}

// GOOD: API response logging
void logAPIResponse(String url, int statusCode, int durationMs) {
  final level = statusCode >= 400 ? LogLevel.warn : LogLevel.info;
  FS.log(level: level, msg: 'API $statusCode: $url (${durationMs}ms)');
}

// GOOD: Centralized logger
class AppLogger {
  static void info(String message) {
    FS.log(level: LogLevel.info, msg: '[INFO] $message');
  }
  
  static void error(String message, {Object? error}) {
    var msg = '[ERROR] $message';
    if (error != null) {
      msg += '\nError: $error';
    }
    FS.log(level: LogLevel.error, msg: msg);
  }
}
```

---

## React Native

### API Reference

```javascript
import FullStory, { LogLevel } from '@fullstory/react-native';

// Log with level
FullStory.log(LogLevel.Info, 'Your message here');

// Log levels
LogLevel.Log
LogLevel.Debug
LogLevel.Info
LogLevel.Warn
LogLevel.Error
```

### ✅ GOOD Implementation Examples

```javascript
// GOOD: Error logging with context
function logError(error, context = {}) {
  const contextString = Object.keys(context).length > 0 
    ? ` | Context: ${JSON.stringify(context)}` 
    : '';
  FullStory.log(LogLevel.Error, `Error: ${error.message}${contextString}`);
}

// GOOD: API response logging
function logAPIResponse(url, statusCode, durationMs) {
  const level = statusCode >= 400 ? LogLevel.Warn : LogLevel.Info;
  FullStory.log(level, `API ${statusCode}: ${url} (${durationMs}ms)`);
}

// GOOD: Centralized logger
const AppLogger = {
  info(message) {
    FullStory.log(LogLevel.Info, `[INFO] ${message}`);
  },
  
  error(message, error = null) {
    let msg = `[ERROR] ${message}`;
    if (error) {
      msg += `\nError: ${error.message}`;
    }
    FullStory.log(LogLevel.Error, msg);
  }
};
```

---

## ❌ BAD Implementation Examples (All Platforms)

```
// BAD: Logging sensitive data
FS.log("User login: password=secret123")  // Never log passwords!

// BAD: Excessive logging in loops
for item in items {
    FS.log("Processing item: \(item)")  // Too many logs!
}

// BAD: Non-string messages (where applicable)
// Always convert to string before logging
```

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/logging/
- **Android**: https://developer.fullstory.com/mobile/android/logging/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/logging/
- **React Native**: https://developer.fullstory.com/mobile/react-native/logging/
