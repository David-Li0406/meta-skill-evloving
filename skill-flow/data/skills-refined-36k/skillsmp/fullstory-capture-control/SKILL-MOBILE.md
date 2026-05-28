---
name: fullstory-capture-control-mobile
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
description: Mobile implementation guide for Fullstory's Capture Control APIs (shutdown/restart). Includes API reference and code examples for iOS, Android, Flutter, and React Native.
parent_skill: fullstory-capture-control
related_skills:
  - fullstory-capture-control
  - fullstory-user-consent
  - fullstory-identify-users
---

# Fullstory Capture Control — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for capture control concepts and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | Shutdown | Restart |
|----------|----------|---------|
| iOS | `FS.shutdown()` | `FS.restart()` |
| Android | `FS.shutdown()` | `FS.restart()` |
| Flutter | `FS.shutdown()` | `FS.restart()` |
| React Native | `FullStory.shutdown()` | `FullStory.restart()` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Stop capture
FS.shutdown()

// Resume capture (starts NEW session)
FS.restart()
```

### ✅ GOOD Implementation Examples

#### Privacy Zone Manager

```swift
// GOOD: Stop capture in sensitive areas
class PrivacyZoneManager {
    static let shared = PrivacyZoneManager()
    
    private var isInPrivacyZone = false
    private var userBeforeShutdown: User?
    
    func enterPrivacyZone(named zoneName: String) {
        guard !isInPrivacyZone else { return }
        
        // Store current user for re-identification
        userBeforeShutdown = AuthManager.shared.currentUser
        
        // Track before shutdown
        FS.event(name: "Privacy Zone Entered", properties: [
            "zone": zoneName
        ])
        
        // Shutdown capture
        FS.shutdown()
        isInPrivacyZone = true
        
        print("Entered privacy zone: \(zoneName)")
    }
    
    func exitPrivacyZone(named zoneName: String) {
        guard isInPrivacyZone else { return }
        
        // Restart capture
        FS.restart()
        isInPrivacyZone = false
        
        // Re-identify user
        if let user = userBeforeShutdown {
            FS.identify(user.id, userVars: [
                "displayName": user.name,
                "email": user.email
            ])
        }
        
        // Track after restart
        FS.event(name: "Privacy Zone Exited", properties: [
            "zone": zoneName
        ])
        
        userBeforeShutdown = nil
        print("Exited privacy zone: \(zoneName)")
    }
}

// Usage
PrivacyZoneManager.shared.enterPrivacyZone(named: "payment-form")
// ... user completes payment ...
PrivacyZoneManager.shared.exitPrivacyZone(named: "payment-form")
```

#### SwiftUI View Modifier

```swift
// GOOD: SwiftUI modifier for privacy zones
struct PrivacyZoneModifier: ViewModifier {
    let zoneName: String
    
    func body(content: Content) -> some View {
        content
            .onAppear {
                PrivacyZoneManager.shared.enterPrivacyZone(named: zoneName)
            }
            .onDisappear {
                PrivacyZoneManager.shared.exitPrivacyZone(named: zoneName)
            }
    }
}

extension View {
    func privacyZone(_ name: String) -> some View {
        modifier(PrivacyZoneModifier(zoneName: name))
    }
}

// Usage
struct PaymentFormView: View {
    var body: some View {
        Form {
            // Payment fields...
        }
        .privacyZone("payment-form")
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Forgot to re-identify
func pauseAndResume() {
    FS.shutdown()
    // ... do work ...
    FS.restart()
    // User is anonymous now!
}

// BAD: No exit path
func handleSensitiveScreen() {
    FS.shutdown()
    // No way to restart!
}
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Stop capture
FS.shutdown()

// Resume capture (starts NEW session)
FS.restart()
```

### ✅ GOOD Implementation Examples

#### Privacy Zone Manager

```kotlin
// GOOD: Stop capture in sensitive areas
object PrivacyZoneManager {
    private var isInPrivacyZone = false
    private var userBeforeShutdown: User? = null
    
    fun enterPrivacyZone(zoneName: String) {
        if (isInPrivacyZone) return
        
        // Store current user for re-identification
        userBeforeShutdown = AuthManager.currentUser
        
        // Track before shutdown
        FS.event("Privacy Zone Entered", mapOf("zone" to zoneName))
        
        // Shutdown capture
        FS.shutdown()
        isInPrivacyZone = true
        
        Log.d("PrivacyZone", "Entered privacy zone: $zoneName")
    }
    
    fun exitPrivacyZone(zoneName: String) {
        if (!isInPrivacyZone) return
        
        // Restart capture
        FS.restart()
        isInPrivacyZone = false
        
        // Re-identify user
        userBeforeShutdown?.let { user ->
            FS.identify(user.id, mapOf(
                "displayName" to user.name,
                "email" to user.email
            ))
        }
        
        // Track after restart
        FS.event("Privacy Zone Exited", mapOf("zone" to zoneName))
        
        userBeforeShutdown = null
        Log.d("PrivacyZone", "Exited privacy zone: $zoneName")
    }
}

// Usage
PrivacyZoneManager.enterPrivacyZone("payment-form")
// ... user completes payment ...
PrivacyZoneManager.exitPrivacyZone("payment-form")
```

#### Compose Effect

```kotlin
// GOOD: Compose effect for privacy zones
@Composable
fun PrivacyZone(
    zoneName: String,
    content: @Composable () -> Unit
) {
    DisposableEffect(zoneName) {
        PrivacyZoneManager.enterPrivacyZone(zoneName)
        
        onDispose {
            PrivacyZoneManager.exitPrivacyZone(zoneName)
        }
    }
    
    content()
}

// Usage
@Composable
fun PaymentFormScreen() {
    PrivacyZone(zoneName = "payment-form") {
        PaymentForm()
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Forgot to re-identify
fun pauseAndResume() {
    FS.shutdown()
    // ... do work ...
    FS.restart()
    // User is anonymous now!
}

// BAD: No exit path
fun handleSensitiveScreen() {
    FS.shutdown()
    // No way to restart!
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Stop capture
FS.shutdown();

// Resume capture (starts NEW session)
FS.restart();
```

### ✅ GOOD Implementation Examples

#### Privacy Zone Manager

```dart
// GOOD: Stop capture in sensitive areas
class PrivacyZoneManager {
  static final PrivacyZoneManager _instance = PrivacyZoneManager._internal();
  factory PrivacyZoneManager() => _instance;
  PrivacyZoneManager._internal();
  
  bool _isInPrivacyZone = false;
  User? _userBeforeShutdown;
  
  void enterPrivacyZone(String zoneName) {
    if (_isInPrivacyZone) return;
    
    // Store current user for re-identification
    _userBeforeShutdown = AuthManager.instance.currentUser;
    
    // Track before shutdown
    FS.event(name: 'Privacy Zone Entered', properties: {
      'zone': zoneName,
    });
    
    // Shutdown capture
    FS.shutdown();
    _isInPrivacyZone = true;
    
    debugPrint('Entered privacy zone: $zoneName');
  }
  
  void exitPrivacyZone(String zoneName) {
    if (!_isInPrivacyZone) return;
    
    // Restart capture
    FS.restart();
    _isInPrivacyZone = false;
    
    // Re-identify user
    final user = _userBeforeShutdown;
    if (user != null) {
      FS.identify(user.id, userVars: {
        'displayName': user.name,
        'email': user.email,
      });
    }
    
    // Track after restart
    FS.event(name: 'Privacy Zone Exited', properties: {
      'zone': zoneName,
    });
    
    _userBeforeShutdown = null;
    debugPrint('Exited privacy zone: $zoneName');
  }
}
```

#### Widget Wrapper

```dart
// GOOD: Widget wrapper for privacy zones
class PrivacyZone extends StatefulWidget {
  final String zoneName;
  final Widget child;
  
  const PrivacyZone({
    required this.zoneName,
    required this.child,
    Key? key,
  }) : super(key: key);
  
  @override
  State<PrivacyZone> createState() => _PrivacyZoneState();
}

class _PrivacyZoneState extends State<PrivacyZone> {
  @override
  void initState() {
    super.initState();
    PrivacyZoneManager().enterPrivacyZone(widget.zoneName);
  }
  
  @override
  void dispose() {
    PrivacyZoneManager().exitPrivacyZone(widget.zoneName);
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return widget.child;
  }
}

// Usage
class PaymentFormScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return PrivacyZone(
      zoneName: 'payment-form',
      child: PaymentForm(),
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Forgot to re-identify
void pauseAndResume() {
  FS.shutdown();
  // ... do work ...
  FS.restart();
  // User is anonymous now!
}

// BAD: No exit path
void handleSensitiveScreen() {
  FS.shutdown();
  // No way to restart!
}
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Stop capture
FullStory.shutdown();

// Resume capture (starts NEW session)
FullStory.restart();
```

### ✅ GOOD Implementation Examples

#### Privacy Zone Manager

```javascript
// GOOD: Stop capture in sensitive areas
class PrivacyZoneManager {
  constructor() {
    this.isInPrivacyZone = false;
    this.userBeforeShutdown = null;
  }
  
  enterPrivacyZone(zoneName) {
    if (this.isInPrivacyZone) return;
    
    // Store current user for re-identification
    this.userBeforeShutdown = AuthManager.getCurrentUser();
    
    // Track before shutdown
    FullStory.event('Privacy Zone Entered', { zone: zoneName });
    
    // Shutdown capture
    FullStory.shutdown();
    this.isInPrivacyZone = true;
    
    console.log(`Entered privacy zone: ${zoneName}`);
  }
  
  exitPrivacyZone(zoneName) {
    if (!this.isInPrivacyZone) return;
    
    // Restart capture
    FullStory.restart();
    this.isInPrivacyZone = false;
    
    // Re-identify user
    if (this.userBeforeShutdown) {
      FullStory.identify(this.userBeforeShutdown.id, {
        displayName: this.userBeforeShutdown.name,
        email: this.userBeforeShutdown.email,
      });
    }
    
    // Track after restart
    FullStory.event('Privacy Zone Exited', { zone: zoneName });
    
    this.userBeforeShutdown = null;
    console.log(`Exited privacy zone: ${zoneName}`);
  }
}

export default new PrivacyZoneManager();
```

#### Custom Hook

```jsx
// GOOD: Custom hook for capture control
import { useEffect, useRef, useCallback } from 'react';
import FullStory from '@fullstory/react-native';
import PrivacyZoneManager from './PrivacyZoneManager';

export function usePrivacyZone(zoneName) {
  useEffect(() => {
    PrivacyZoneManager.enterPrivacyZone(zoneName);
    
    return () => {
      PrivacyZoneManager.exitPrivacyZone(zoneName);
    };
  }, [zoneName]);
}

// Usage
function PaymentFormScreen() {
  usePrivacyZone('payment-form');
  
  return <PaymentForm />;
}
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Forgot to re-identify
function pauseAndResume() {
  FullStory.shutdown();
  // ... do work ...
  FullStory.restart();
  // User is anonymous now!
}

// BAD: No exit path
function handleSensitiveScreen() {
  FullStory.shutdown();
  // No way to restart!
}
```

---

## Common Patterns (All Platforms)

### Privacy Zone Flow

```
1. User enters sensitive screen/area
2. Track "Privacy Zone Entered" event
3. Save current user identity
4. Call shutdown()
5. User interacts with sensitive content (not captured)
6. User exits sensitive screen/area
7. Call restart()
8. Re-identify the user
9. Track "Privacy Zone Exited" event
```

### Screen-Based Privacy

For entire screens that should not be captured:
- Enter privacy zone in `viewDidLoad`/`onCreate`/`initState`/`useEffect`
- Exit privacy zone in `viewDidDisappear`/`onDestroy`/`dispose`/cleanup

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/capture-data/
- **Android**: https://developer.fullstory.com/mobile/android/capture-data/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/capture-data/
- **React Native**: https://developer.fullstory.com/mobile/react-native/capture-data/
