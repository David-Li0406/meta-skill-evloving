---
name: fullstory-async-methods-mobile
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
description: Mobile platform guide for asynchronous Fullstory operations. Explains platform-specific patterns since the Async suffix pattern is web-only.
parent_skill: fullstory-async-methods
related_skills:
  - fullstory-async-methods
  - fullstory-observe-callbacks
  - fullstory-capture-control
---

# Fullstory Async Methods — Mobile Platforms

> **Core Concepts**: See [SKILL.md](./SKILL.md) for general async concepts.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for the JavaScript `Async` suffix pattern.

---

## Platform Differences

The `FS('methodNameAsync')` pattern is **specific to the web/browser SDK**. Mobile platforms use different asynchronous mechanisms native to each platform.

| Platform | Async Mechanism |
|----------|-----------------|
| Web | `FS('methodAsync')` returns Promise-like |
| iOS | Completion handlers, delegates |
| Android | Listeners, callbacks |
| Flutter | Future-based async/await |
| React Native | Promise-based (JavaScript) |

---

## iOS (Swift)

iOS uses completion handlers and the delegate pattern for asynchronous operations.

### Session URL Retrieval

```swift
import FullStory

// Get current session URL (synchronous - returns immediately if available)
if let sessionUrl = FS.currentSessionURL() {
    print("Session URL: \(sessionUrl)")
}

// For session URL updates, use FSDelegate
class AppDelegate: UIResponder, UIApplicationDelegate, FSDelegate {
    
    func application(_ application: UIApplication, 
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        FS.delegate = self
        FS.start()
        return true
    }
    
    // Called when session URL becomes available or changes
    func fullstoryDidStartSession(_ sessionUrl: String) {
        print("Session started: \(sessionUrl)")
        // Forward to error tracking, support tools, etc.
    }
}
```

### Async Operations

```swift
// Most FS methods are synchronous in iOS
// They queue internally and execute when ready

// Identify user
FS.identify(userId, userVars: [
    "displayName": userName,
    "email": userEmail
])

// Track event
FS.event("Purchase Completed", [
    "orderId": orderId,
    "revenue": revenue
])

// These don't block - they queue and execute asynchronously
```

---

## Android (Kotlin)

Android uses listeners and callbacks for asynchronous operations.

### Session URL Retrieval

```kotlin
import com.fullstory.FS

// Get current session URL (synchronous - returns immediately if available)
val sessionUrl = FS.getCurrentSessionURL()
if (sessionUrl != null) {
    Log.d("Fullstory", "Session URL: $sessionUrl")
}

// For session URL updates, use FSSessionListener
class MyApplication : Application(), FS.SessionListener {
    
    override fun onCreate() {
        super.onCreate()
        FS.setSessionListener(this)
    }
    
    // Called when session URL becomes available or changes
    override fun onSessionChanged(sessionUrl: String) {
        Log.d("Fullstory", "Session started: $sessionUrl")
        // Forward to error tracking, support tools, etc.
    }
}
```

### Async Operations

```kotlin
// Most FS methods are synchronous in Android
// They queue internally and execute when ready

// Identify user
FS.identify(userId, mapOf(
    "displayName" to userName,
    "email" to userEmail
))

// Track event
FS.event("Purchase Completed", mapOf(
    "orderId" to orderId,
    "revenue" to revenue
))

// These don't block - they queue and execute asynchronously
```

---

## Flutter (Dart)

Flutter uses Dart's Future-based async/await pattern.

### Session URL Retrieval

```dart
import 'package:fullstory_flutter/fs.dart';

// Get current session URL
Future<void> getSessionUrl() async {
  final sessionUrl = await FS.currentSessionURL;
  if (sessionUrl != null) {
    print('Session URL: $sessionUrl');
  }
}

// Listen for session changes
class _MyAppState extends State<MyApp> {
  StreamSubscription? _sessionSubscription;
  
  @override
  void initState() {
    super.initState();
    _sessionSubscription = FS.sessionUrlStream.listen((url) {
      print('Session URL changed: $url');
    });
  }
  
  @override
  void dispose() {
    _sessionSubscription?.cancel();
    super.dispose();
  }
}
```

### Async Operations

```dart
// Flutter methods are generally synchronous but queue internally

// Identify user
FS.identify(userId, {
  'displayName': userName,
  'email': userEmail,
});

// Track event
FS.event('Purchase Completed', {
  'orderId': orderId,
  'revenue': revenue,
});
```

---

## React Native

React Native uses JavaScript Promises, similar to web but with different method names.

### Session URL Retrieval

```javascript
import FullStory from '@fullstory/react-native';

// Get current session URL (async)
async function getSessionUrl() {
  try {
    const sessionUrl = await FullStory.getCurrentSessionURL();
    console.log('Session URL:', sessionUrl);
    return sessionUrl;
  } catch (error) {
    console.warn('Could not get session URL:', error);
    return null;
  }
}

// Listen for session changes
useEffect(() => {
  const subscription = FullStory.onSession((sessionUrl) => {
    console.log('Session URL changed:', sessionUrl);
  });
  
  return () => subscription.remove();
}, []);
```

### Async Operations

```javascript
// Identify user
FullStory.identify(userId, {
  displayName: userName,
  email: userEmail,
});

// Track event
FullStory.event('Purchase Completed', {
  orderId: orderId,
  revenue: revenue,
});

// These methods are fire-and-forget in React Native
// Use getCurrentSessionURL() for async session URL retrieval
```

---

## Equivalent Patterns

### Getting Session URL

| Platform | Method |
|----------|--------|
| Web | `await FS('getSessionAsync')` |
| iOS | `FS.currentSessionURL()` + `FSDelegate` |
| Android | `FS.getCurrentSessionURL()` + `SessionListener` |
| Flutter | `await FS.currentSessionURL` + Stream |
| React Native | `await FullStory.getCurrentSessionURL()` |

### Waiting for Initialization

| Platform | Pattern |
|----------|---------|
| Web | `await FS('getSessionAsync')` or observer |
| iOS | `FSDelegate.fullstoryDidStartSession()` |
| Android | `FS.SessionListener.onSessionChanged()` |
| Flutter | `FS.sessionUrlStream.listen()` |
| React Native | `FullStory.onSession()` callback |

---

## Best Practices (All Platforms)

1. **Don't block on Fullstory** — Always allow your app to function if Fullstory is unavailable
2. **Use platform-native patterns** — Delegates on iOS, Listeners on Android, Streams on Flutter
3. **Handle unavailability gracefully** — Check for null/undefined session URLs
4. **Clean up subscriptions** — Remove listeners/observers when components unmount

---

## Reference Links

- **iOS SDK**: https://developer.fullstory.com/mobile/ios/
- **Android SDK**: https://developer.fullstory.com/mobile/android/
- **Flutter SDK**: https://developer.fullstory.com/mobile/flutter/
- **React Native SDK**: https://developer.fullstory.com/mobile/react-native/
