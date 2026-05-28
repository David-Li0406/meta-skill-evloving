---
name: fullstory-user-consent-mobile
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
description: Mobile implementation guide for Fullstory's User Consent API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Java), Flutter (Dart), and React Native.
parent_skill: fullstory-user-consent
related_skills:
  - fullstory-user-consent
  - fullstory-identify-users
  - fullstory-capture-control
---

# Fullstory User Consent — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for consent approaches, compliance guidance, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | Delay Startup | Start Capture | Stop Capture | Set Consent |
|----------|---------------|---------------|--------------|-------------|
| iOS | Config: `startCaptureManually` | `FS.restart()` | `FS.shutdown()` | `FS.setConsent(_:)` |
| Android | Config: `enableCaptureOnStart` | `FS.restart()` | `FS.shutdown()` | `FS.setConsent(_:)` |
| Flutter | Config: `enableCaptureOnStart` | `FS.restart()` | `FS.shutdown()` | `FS.setConsent(_:)` |
| React Native | Config: `enableCaptureOnStart` | `FullStory.restart()` | `FullStory.shutdown()` | `FullStory.setConsent(_:)` |

---

## iOS (Swift/SwiftUI)

### Configuration

To delay capture until consent, configure in `Info.plist` or programmatically:

```xml
<!-- Info.plist -->
<key>FullStory</key>
<dict>
    <key>OrgId</key>
    <string>YOUR_ORG_ID</string>
    <key>StartCaptureManually</key>
    <true/>
</dict>
```

### API Reference

```swift
import FullStory

// Start capture (after consent)
FS.restart()

// Stop capture (revoked consent)
FS.shutdown()

// Element-level consent
FS.setConsent(true)   // Enable capture of consent-marked elements
FS.setConsent(false)  // Disable capture of consent-marked elements
```

### ✅ GOOD Implementation Examples

#### GDPR Consent Manager

```swift
// GOOD: Complete GDPR consent flow
import FullStory

class ConsentManager {
    static let shared = ConsentManager()
    
    private let consentKey = "fs_consent_granted"
    
    private init() {}
    
    var hasConsent: Bool {
        UserDefaults.standard.bool(forKey: consentKey)
    }
    
    func initialize() {
        // Check stored consent on app launch
        if hasConsent {
            startCapture()
        }
        // Otherwise, wait for user to grant consent
    }
    
    func grantConsent() {
        UserDefaults.standard.set(true, forKey: consentKey)
        startCapture()
        
        // If user is already logged in, identify them
        if let user = AuthManager.shared.currentUser {
            identifyUser(user)
        }
    }
    
    func revokeConsent() {
        UserDefaults.standard.set(false, forKey: consentKey)
        FS.shutdown()
    }
    
    private func startCapture() {
        FS.restart()
    }
    
    private func identifyUser(_ user: User) {
        FS.identify(user.id, userVars: [
            "displayName": user.name,
            "email": user.email
        ])
    }
}

// AppDelegate
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    ConsentManager.shared.initialize()
    return true
}
```

#### SwiftUI Consent Banner

```swift
// GOOD: SwiftUI consent implementation
import SwiftUI
import FullStory

class ConsentViewModel: ObservableObject {
    @Published var needsConsent: Bool
    @Published var hasConsent: Bool
    
    private let consentKey = "fs_consent"
    
    init() {
        let status = UserDefaults.standard.string(forKey: consentKey)
        self.needsConsent = status == nil
        self.hasConsent = status == "granted"
        
        // Start capture if already consented
        if hasConsent {
            FS.restart()
        }
    }
    
    func grantConsent() {
        UserDefaults.standard.set("granted", forKey: consentKey)
        hasConsent = true
        needsConsent = false
        FS.restart()
    }
    
    func denyConsent() {
        UserDefaults.standard.set("denied", forKey: consentKey)
        hasConsent = false
        needsConsent = false
        FS.shutdown()
    }
    
    func resetConsent() {
        UserDefaults.standard.removeObject(forKey: consentKey)
        needsConsent = true
        hasConsent = false
        FS.shutdown()
    }
}

struct ConsentBanner: View {
    @ObservedObject var viewModel: ConsentViewModel
    
    var body: some View {
        if viewModel.needsConsent {
            VStack(spacing: 16) {
                Text("We use session recording to improve your experience.")
                    .multilineTextAlignment(.center)
                
                HStack(spacing: 16) {
                    Button("Decline") {
                        viewModel.denyConsent()
                    }
                    .buttonStyle(.bordered)
                    
                    Button("Accept") {
                        viewModel.grantConsent()
                    }
                    .buttonStyle(.borderedProminent)
                }
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(radius: 8)
        }
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Starting capture without checking consent
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    FS.restart()  // BAD: No consent check!
    return true
}

// BAD: Not persisting consent
func userTappedAccept() {
    FS.restart()  // BAD: Not saved - will need consent again after restart
}
```

---

## Android (Kotlin)

### Configuration

To delay capture until consent, configure in `fullstory.xml`:

```xml
<!-- res/values/fullstory.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="fs_org_id">YOUR_ORG_ID</string>
    <bool name="fs_enable_capture_on_start">false</bool>
</resources>
```

### API Reference

```kotlin
import com.fullstory.FS

// Start capture (after consent)
FS.restart()

// Stop capture (revoked consent)
FS.shutdown()

// Element-level consent
FS.setConsent(true)   // Enable capture of consent-marked elements
FS.setConsent(false)  // Disable capture of consent-marked elements
```

### ✅ GOOD Implementation Examples

#### GDPR Consent Manager

```kotlin
// GOOD: Complete GDPR consent flow
import com.fullstory.FS
import android.content.Context
import android.content.SharedPreferences

class ConsentManager private constructor(context: Context) {
    
    companion object {
        @Volatile
        private var instance: ConsentManager? = null
        
        fun getInstance(context: Context): ConsentManager {
            return instance ?: synchronized(this) {
                instance ?: ConsentManager(context.applicationContext).also { instance = it }
            }
        }
    }
    
    private val prefs: SharedPreferences = 
        context.getSharedPreferences("fs_consent", Context.MODE_PRIVATE)
    
    private val consentKey = "consent_granted"
    
    val hasConsent: Boolean
        get() = prefs.getBoolean(consentKey, false)
    
    fun initialize() {
        if (hasConsent) {
            startCapture()
        }
    }
    
    fun grantConsent() {
        prefs.edit().putBoolean(consentKey, true).apply()
        startCapture()
        
        // If user is already logged in, identify them
        AuthManager.currentUser?.let { identifyUser(it) }
    }
    
    fun revokeConsent() {
        prefs.edit().putBoolean(consentKey, false).apply()
        FS.shutdown()
    }
    
    private fun startCapture() {
        FS.restart()
    }
    
    private fun identifyUser(user: User) {
        FS.identify(user.id, mapOf(
            "displayName" to user.name,
            "email" to user.email
        ))
    }
}

// Application class
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        ConsentManager.getInstance(this).initialize()
    }
}
```

#### Jetpack Compose Consent Banner

```kotlin
// GOOD: Jetpack Compose consent implementation
import androidx.compose.runtime.*
import androidx.compose.material3.*
import com.fullstory.FS

class ConsentViewModel(private val context: Context) : ViewModel() {
    
    private val prefs = context.getSharedPreferences("fs_consent", Context.MODE_PRIVATE)
    
    var needsConsent by mutableStateOf(prefs.getString("status", null) == null)
        private set
    
    var hasConsent by mutableStateOf(prefs.getString("status", null) == "granted")
        private set
    
    init {
        if (hasConsent) {
            FS.restart()
        }
    }
    
    fun grantConsent() {
        prefs.edit().putString("status", "granted").apply()
        hasConsent = true
        needsConsent = false
        FS.restart()
    }
    
    fun denyConsent() {
        prefs.edit().putString("status", "denied").apply()
        hasConsent = false
        needsConsent = false
        FS.shutdown()
    }
}

@Composable
fun ConsentBanner(viewModel: ConsentViewModel) {
    if (viewModel.needsConsent) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("We use session recording to improve your experience.")
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    OutlinedButton(onClick = { viewModel.denyConsent() }) {
                        Text("Decline")
                    }
                    Button(onClick = { viewModel.grantConsent() }) {
                        Text("Accept")
                    }
                }
            }
        }
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Starting capture without checking consent
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        FS.restart()  // BAD: No consent check!
    }
}

// BAD: Not persisting consent
fun onAcceptClicked() {
    FS.restart()  // BAD: Not saved - will need consent again after restart
}
```

---

## Flutter (Dart)

### Configuration

To delay capture until consent, configure in initialization:

```dart
import 'package:fullstory_flutter/fs.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await FS.init(
    orgId: 'YOUR_ORG_ID',
    enableCaptureOnStart: false,  // Don't capture until consent
  );
  
  runApp(MyApp());
}
```

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Start capture (after consent)
FS.restart();

// Stop capture (revoked consent)
FS.shutdown();

// Element-level consent
FS.setConsent(true);   // Enable capture of consent-marked elements
FS.setConsent(false);  // Disable capture of consent-marked elements
```

### ✅ GOOD Implementation Examples

#### GDPR Consent Manager

```dart
// GOOD: Complete GDPR consent flow
import 'package:fullstory_flutter/fs.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ConsentManager {
  static final ConsentManager _instance = ConsentManager._internal();
  factory ConsentManager() => _instance;
  ConsentManager._internal();
  
  static const _consentKey = 'fs_consent_granted';
  late SharedPreferences _prefs;
  
  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    
    if (hasConsent) {
      await startCapture();
    }
  }
  
  bool get hasConsent => _prefs.getBool(_consentKey) ?? false;
  
  Future<void> grantConsent() async {
    await _prefs.setBool(_consentKey, true);
    await startCapture();
    
    // If user is already logged in, identify them
    final user = AuthManager.instance.currentUser;
    if (user != null) {
      await identifyUser(user);
    }
  }
  
  Future<void> revokeConsent() async {
    await _prefs.setBool(_consentKey, false);
    FS.shutdown();
  }
  
  Future<void> startCapture() async {
    FS.restart();
  }
  
  Future<void> identifyUser(User user) async {
    FS.identify(user.id, userVars: {
      'displayName': user.name,
      'email': user.email,
    });
  }
}
```

#### Provider-Based Consent

```dart
// GOOD: Provider pattern for consent management
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fullstory_flutter/fs.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ConsentProvider extends ChangeNotifier {
  bool _needsConsent = true;
  bool _hasConsent = false;
  
  bool get needsConsent => _needsConsent;
  bool get hasConsent => _hasConsent;
  
  Future<void> initialize() async {
    final prefs = await SharedPreferences.getInstance();
    final status = prefs.getString('consent_status');
    
    _needsConsent = status == null;
    _hasConsent = status == 'granted';
    
    if (_hasConsent) {
      FS.restart();
    }
    
    notifyListeners();
  }
  
  Future<void> grantConsent() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('consent_status', 'granted');
    
    _needsConsent = false;
    _hasConsent = true;
    FS.restart();
    
    notifyListeners();
  }
  
  Future<void> denyConsent() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('consent_status', 'denied');
    
    _needsConsent = false;
    _hasConsent = false;
    FS.shutdown();
    
    notifyListeners();
  }
}

// Consent Banner Widget
class ConsentBanner extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<ConsentProvider>(
      builder: (context, consent, child) {
        if (!consent.needsConsent) return const SizedBox.shrink();
        
        return Card(
          margin: const EdgeInsets.all(16),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('We use session recording to improve your experience.'),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    OutlinedButton(
                      onPressed: consent.denyConsent,
                      child: const Text('Decline'),
                    ),
                    const SizedBox(width: 16),
                    ElevatedButton(
                      onPressed: consent.grantConsent,
                      child: const Text('Accept'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Starting capture without checking consent
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await FS.init(orgId: 'YOUR_ORG_ID');
  FS.restart();  // BAD: No consent check!
  
  runApp(MyApp());
}

// BAD: Not persisting consent
void onAcceptPressed() {
  FS.restart();  // BAD: Not saved - will need consent again after restart
}
```

---

## React Native

### Configuration

To delay capture until consent, configure in initialization:

```javascript
import FullStory from '@fullstory/react-native';

// In your app initialization
FullStory.init({
  orgId: 'YOUR_ORG_ID',
  enableCaptureOnStart: false,  // Don't capture until consent
});
```

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Start capture (after consent)
FullStory.restart();

// Stop capture (revoked consent)
FullStory.shutdown();

// Element-level consent
FullStory.setConsent(true);   // Enable capture of consent-marked elements
FullStory.setConsent(false);  // Disable capture of consent-marked elements
```

### ✅ GOOD Implementation Examples

#### GDPR Consent Hook

```jsx
// GOOD: Complete GDPR consent flow with React hooks
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import FullStory from '@fullstory/react-native';

const ConsentContext = createContext(null);

export function ConsentProvider({ children }) {
  const [consentStatus, setConsentStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    loadConsent();
  }, []);
  
  const loadConsent = async () => {
    try {
      const status = await AsyncStorage.getItem('fs_consent');
      setConsentStatus(status);
      
      if (status === 'granted') {
        FullStory.restart();
      }
    } catch (e) {
      console.error('Error loading consent:', e);
    } finally {
      setIsLoading(false);
    }
  };
  
  const grantConsent = useCallback(async () => {
    await AsyncStorage.setItem('fs_consent', 'granted');
    setConsentStatus('granted');
    FullStory.restart();
  }, []);
  
  const denyConsent = useCallback(async () => {
    await AsyncStorage.setItem('fs_consent', 'denied');
    setConsentStatus('denied');
    FullStory.shutdown();
  }, []);
  
  const resetConsent = useCallback(async () => {
    await AsyncStorage.removeItem('fs_consent');
    setConsentStatus(null);
    FullStory.shutdown();
  }, []);
  
  return (
    <ConsentContext.Provider value={{
      isLoading,
      consentStatus,
      hasConsent: consentStatus === 'granted',
      needsConsent: consentStatus === null,
      grantConsent,
      denyConsent,
      resetConsent,
    }}>
      {children}
    </ConsentContext.Provider>
  );
}

export function useConsent() {
  const context = useContext(ConsentContext);
  if (!context) {
    throw new Error('useConsent must be used within ConsentProvider');
  }
  return context;
}
```

#### Consent Banner Component

```jsx
// GOOD: React Native consent banner
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useConsent } from './ConsentProvider';

export function ConsentBanner() {
  const { needsConsent, isLoading, grantConsent, denyConsent } = useConsent();
  
  if (isLoading || !needsConsent) return null;
  
  return (
    <View style={styles.banner}>
      <Text style={styles.text}>
        We use session recording to improve your experience.
      </Text>
      <View style={styles.buttons}>
        <TouchableOpacity style={styles.declineButton} onPress={denyConsent}>
          <Text style={styles.declineText}>Decline</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.acceptButton} onPress={grantConsent}>
          <Text style={styles.acceptText}>Accept</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  banner: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    margin: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  text: {
    textAlign: 'center',
    marginBottom: 16,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
  },
  declineButton: {
    paddingVertical: 8,
    paddingHorizontal: 24,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#666',
  },
  declineText: {
    color: '#666',
  },
  acceptButton: {
    paddingVertical: 8,
    paddingHorizontal: 24,
    borderRadius: 8,
    backgroundColor: '#007AFF',
  },
  acceptText: {
    color: 'white',
  },
});
```

#### Privacy Settings Screen

```jsx
// GOOD: Settings screen with consent management
import React from 'react';
import { View, Text, Switch, TouchableOpacity, StyleSheet } from 'react-native';
import { useConsent } from './ConsentProvider';

export function PrivacySettingsScreen() {
  const { hasConsent, grantConsent, denyConsent, resetConsent } = useConsent();
  
  const toggleConsent = (value) => {
    if (value) {
      grantConsent();
    } else {
      denyConsent();
    }
  };
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Privacy Settings</Text>
      
      <View style={styles.row}>
        <View style={styles.labelContainer}>
          <Text style={styles.label}>Session Recording</Text>
          <Text style={styles.description}>
            Allow anonymous session recording to help improve the app experience.
          </Text>
        </View>
        <Switch
          value={hasConsent}
          onValueChange={toggleConsent}
        />
      </View>
      
      <TouchableOpacity style={styles.resetButton} onPress={resetConsent}>
        <Text style={styles.resetText}>Reset Privacy Preferences</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### ❌ BAD Implementation Examples

```jsx
// BAD: Starting capture without checking consent
useEffect(() => {
  FullStory.restart();  // BAD: No consent check!
}, []);

// BAD: Not persisting consent
const handleAccept = () => {
  FullStory.restart();  // BAD: Not saved - will need consent again after restart
};

// BAD: Not handling loading state
function ConsentBanner() {
  const { needsConsent, grantConsent } = useConsent();
  
  // BAD: Might flash banner before we load consent state from storage
  if (!needsConsent) return null;
  
  return <Banner onAccept={grantConsent} />;
}
```

---

## Common Patterns (All Platforms)

### Consent + User Identity

Handle the interaction between consent and user identification:

```
User Flow:
1. App loads → Check consent from storage
2. If consented → Start capture
3. User logs in → If capture started, identify user
4. User logs out → Anonymize session
5. Consent revoked → Stop capture

Key Rule: Never identify users before consent is granted
```

### Region-Based Consent

For apps serving multiple regions:

1. Detect user region (geolocation, user setting, locale)
2. EU users: Require opt-in
3. US users: Allow opt-out (CCPA)
4. Other regions: Follow local laws or default to opt-in

### Consent State Machine

```
States:
- UNKNOWN: No decision made yet
- GRANTED: User accepted
- DENIED: User declined
- WITHDRAWN: User later revoked consent

Transitions:
- UNKNOWN → GRANTED (accept)
- UNKNOWN → DENIED (decline)
- GRANTED → WITHDRAWN (revoke)
- DENIED → GRANTED (change mind)
- WITHDRAWN → GRANTED (re-accept)
```

---

## Reference Links

- **iOS Capture Control**: https://developer.fullstory.com/mobile/ios/capture-control/
- **Android Capture Control**: https://developer.fullstory.com/mobile/android/capture-control/
- **Flutter Capture Control**: https://developer.fullstory.com/mobile/flutter/capture-control/
- **React Native Capture Control**: https://developer.fullstory.com/mobile/react-native/capture-control/
- **Help Center - Consent**: https://help.fullstory.com/hc/en-us/articles/360020623374
