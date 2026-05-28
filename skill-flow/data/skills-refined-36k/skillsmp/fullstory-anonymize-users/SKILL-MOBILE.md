---
name: fullstory-anonymize-users-mobile
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
description: Mobile implementation guide for Fullstory's User Anonymization API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-anonymize-users
related_skills:
  - fullstory-anonymize-users
  - fullstory-identify-users
  - fullstory-user-consent
---

# Fullstory Anonymize Users — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for session lifecycle, when to anonymize, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | SDK | Anonymize Method |
|----------|-----|------------------|
| iOS | `FullStory` | `FS.anonymize()` |
| Android | `FullStory` | `FS.anonymize()` |
| Flutter | `fullstory_flutter` | `FS.anonymize()` |
| React Native | `@fullstory/react-native` | `FullStory.anonymize()` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Anonymize the current user
FS.anonymize()
```

### ✅ GOOD Implementation Examples

#### Basic Logout Handler

```swift
// GOOD: Proper logout with Fullstory anonymization
class AuthManager {
    
    func logout() async {
        do {
            // 1. Call backend logout endpoint
            try await APIClient.shared.post("/auth/logout")
            
            // 2. Track logout event before anonymizing
            FS.event(name: "User Logged Out", properties: [
                "logoutMethod": "manual",
                "sessionDuration": getSessionDuration()
            ])
            
            // 3. Clear local authentication state
            clearAuthTokens()
            clearUserState()
            
            // 4. Anonymize in Fullstory
            FS.anonymize()
            
            // 5. Navigate to login
            await MainActor.run {
                navigateToLogin()
            }
        } catch {
            print("Logout failed: \(error)")
            // Still anonymize even if backend fails
            FS.anonymize()
            await MainActor.run {
                navigateToLogin()
            }
        }
    }
}
```

**Why this is good:**
- ✅ Tracks event before anonymizing
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

#### Account Switching

```swift
// GOOD: Clean account switching with proper session boundaries
class AccountSwitcher {
    
    func switchAccount(to newAccountId: String) async throws {
        let newUser = try await fetchAccountDetails(newAccountId)
        
        // Track the switch event under current user
        FS.event(name: "Account Switch Initiated", properties: [
            "targetAccountId": newAccountId
        ])
        
        // Step 1: Anonymize current session
        FS.anonymize()
        
        // Step 2: Set up new account context
        try await setupAccountContext(newUser)
        
        // Step 3: Identify as new user
        FS.identify(newUser.id, userVars: [
            "displayName": newUser.name,
            "email": newUser.email,
            "accountType": newUser.type
        ])
        
        // Refresh UI
        await MainActor.run {
            refreshUserInterface()
        }
    }
}
```

#### Session Timeout Handler

```swift
// GOOD: Handling session timeout with Fullstory
class SessionManager: ObservableObject {
    private let timeoutDuration: TimeInterval = 30 * 60 // 30 minutes
    private var timeoutTimer: Timer?
    private var lastActivityDate = Date()
    private var isMonitoring = false
    
    func startMonitoring() {
        // Guard against duplicate observer registration
        guard !isMonitoring else { return }
        isMonitoring = true
        
        resetTimeout()
        
        // Monitor app lifecycle to detect user returning to app
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(appDidBecomeActive),
            name: UIApplication.didBecomeActiveNotification,
            object: nil
        )
        
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(appWillResignActive),
            name: UIApplication.willResignActiveNotification,
            object: nil
        )
    }
    
    func stopMonitoring() {
        guard isMonitoring else { return }
        isMonitoring = false
        
        timeoutTimer?.invalidate()
        timeoutTimer = nil
        NotificationCenter.default.removeObserver(self)
    }
    
    deinit {
        stopMonitoring()
    }
    
    @objc private func appDidBecomeActive() {
        // User returned to app - check if session timed out while away
        let inactiveDuration = Date().timeIntervalSince(lastActivityDate)
        if inactiveDuration > timeoutDuration {
            handleSessionTimeout()
        } else {
            resetTimeout()
        }
    }
    
    @objc private func appWillResignActive() {
        // App going to background - record last activity time
        lastActivityDate = Date()
        timeoutTimer?.invalidate()
    }
    
    /// Call this method when user interacts with the app
    func recordUserActivity() {
        lastActivityDate = Date()
        resetTimeout()
    }
    
    private func resetTimeout() {
        timeoutTimer?.invalidate()
        
        timeoutTimer = Timer.scheduledTimer(
            withTimeInterval: timeoutDuration,
            repeats: false
        ) { [weak self] _ in
            self?.handleSessionTimeout()
        }
    }
    
    private func handleSessionTimeout() {
        // Track timeout event while still identified
        let inactivityDuration = Date().timeIntervalSince(lastActivityDate)
        FS.event(name: "Session Timeout", properties: [
            "inactivityDuration": Int(inactivityDuration),
            "lastScreen": currentScreenName()
        ])
        
        // Anonymize the session
        FS.anonymize()
        
        // Clear auth and show timeout UI
        DispatchQueue.main.async {
            self.clearAuthState()
            self.showTimeoutAlert()
        }
    }
}
```

#### SwiftUI Integration

```swift
// GOOD: SwiftUI logout with Fullstory
struct SettingsView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var showingLogoutConfirmation = false
    
    var body: some View {
        List {
            // Settings items...
            
            Section {
                Button("Sign Out", role: .destructive) {
                    showingLogoutConfirmation = true
                }
            }
        }
        .confirmationDialog(
            "Are you sure you want to sign out?",
            isPresented: $showingLogoutConfirmation
        ) {
            Button("Sign Out", role: .destructive) {
                performLogout()
            }
        }
    }
    
    private func performLogout() {
        // Track before anonymizing
        FS.event(name: "User Logged Out", properties: [
            "logoutMethod": "settings_menu"
        ])
        
        // Anonymize
        FS.anonymize()
        
        // Clear auth state
        authManager.logout()
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Forgetting to anonymize on logout
func handleLogout() {
    clearAuthTokens()
    clearUserState()
    navigateToLogin()
    // Missing FS.anonymize()!
}

// BAD: Anonymizing multiple times
func handleLogout() {
    FS.anonymize()
    FS.anonymize()
    FS.anonymize()  // Wasteful!
    navigateToLogin()
}

// BAD: Not tracking event before anonymize
func handleLogout() {
    FS.anonymize()  // Lost opportunity to track logout event
    navigateToLogin()
}
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Anonymize the current user
FS.anonymize()
```

### ✅ GOOD Implementation Examples

#### Basic Logout Handler

```kotlin
// GOOD: Proper logout with Fullstory anonymization
class AuthManager @Inject constructor(
    private val apiClient: ApiClient,
    private val prefsManager: PreferencesManager
) {
    
    suspend fun logout() {
        try {
            // 1. Call backend logout endpoint
            apiClient.post("/auth/logout")
            
            // 2. Track logout event before anonymizing
            FS.event("User Logged Out", mapOf(
                "logoutMethod" to "manual",
                "sessionDuration" to getSessionDuration()
            ))
            
            // 3. Clear local authentication state
            prefsManager.clearAuthTokens()
            prefsManager.clearUserState()
            
            // 4. Anonymize in Fullstory
            FS.anonymize()
            
            // 5. Navigate to login
            navigationManager.navigateToLogin()
            
        } catch (e: Exception) {
            Log.e("AuthManager", "Logout failed", e)
            // Still anonymize even if backend fails
            FS.anonymize()
            navigationManager.navigateToLogin()
        }
    }
}
```

**Why this is good:**
- ✅ Tracks event before anonymizing
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

#### Account Switching

```kotlin
// GOOD: Clean account switching with proper session boundaries
class AccountSwitcher @Inject constructor(
    private val accountRepository: AccountRepository
) {
    
    suspend fun switchAccount(newAccountId: String) {
        val newUser = accountRepository.fetchAccountDetails(newAccountId)
        
        // Track the switch event under current user
        FS.event("Account Switch Initiated", mapOf(
            "targetAccountId" to newAccountId
        ))
        
        // Step 1: Anonymize current session
        FS.anonymize()
        
        // Step 2: Set up new account context
        accountRepository.setupAccountContext(newUser)
        
        // Step 3: Identify as new user
        FS.identify(newUser.id, mapOf(
            "displayName" to newUser.name,
            "email" to newUser.email,
            "accountType" to newUser.type
        ))
        
        // Refresh UI
        refreshUserInterface()
    }
}
```

#### Session Timeout Handler

```kotlin
// GOOD: Handling session timeout with Fullstory
class SessionManager @Inject constructor(
    private val application: Application
) {
    private val timeoutDuration = 30 * 60 * 1000L // 30 minutes
    private var lastActivityTime = System.currentTimeMillis()
    private val handler = Handler(Looper.getMainLooper())
    private val timeoutRunnable = Runnable { handleSessionTimeout() }
    
    // Store callback reference for cleanup
    private var lifecycleCallbacks: Application.ActivityLifecycleCallbacks? = null
    
    fun startMonitoring() {
        resetTimeout()
        
        // Listen for user interactions via activity lifecycle
        lifecycleCallbacks = object : Application.ActivityLifecycleCallbacks {
            override fun onActivityResumed(activity: Activity) {
                resetTimeout()
            }
            override fun onActivityPaused(activity: Activity) {
                lastActivityTime = System.currentTimeMillis()
            }
            override fun onActivityCreated(activity: Activity, savedInstanceState: Bundle?) {}
            override fun onActivityStarted(activity: Activity) {}
            override fun onActivityStopped(activity: Activity) {}
            override fun onActivitySaveInstanceState(activity: Activity, outState: Bundle) {}
            override fun onActivityDestroyed(activity: Activity) {}
        }
        
        application.registerActivityLifecycleCallbacks(lifecycleCallbacks!!)
    }
    
    fun stopMonitoring() {
        handler.removeCallbacks(timeoutRunnable)
        lifecycleCallbacks?.let {
            application.unregisterActivityLifecycleCallbacks(it)
        }
        lifecycleCallbacks = null
    }
    
    private fun resetTimeout() {
        lastActivityTime = System.currentTimeMillis()
        handler.removeCallbacks(timeoutRunnable)
        handler.postDelayed(timeoutRunnable, timeoutDuration)
    }
    
    private fun handleSessionTimeout() {
        // Track timeout event while still identified
        val inactivityDuration = System.currentTimeMillis() - lastActivityTime
        FS.event("Session Timeout", mapOf(
            "inactivityDuration" to inactivityDuration,
            "lastScreen" to getCurrentScreenName()
        ))
        
        // Anonymize the session
        FS.anonymize()
        
        // Clear auth and show timeout UI
        clearAuthState()
        showTimeoutDialog()
    }
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: Compose settings screen with logout
@Composable
fun SettingsScreen(
    viewModel: SettingsViewModel = hiltViewModel(),
    onLoggedOut: () -> Unit
) {
    var showLogoutDialog by remember { mutableStateOf(false) }
    
    Column {
        // Settings items...
        
        Button(
            onClick = { showLogoutDialog = true },
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        ) {
            Text("Sign Out")
        }
    }
    
    if (showLogoutDialog) {
        AlertDialog(
            onDismissRequest = { showLogoutDialog = false },
            title = { Text("Sign Out") },
            text = { Text("Are you sure you want to sign out?") },
            confirmButton = {
                TextButton(
                    onClick = {
                        showLogoutDialog = false
                        viewModel.logout()
                        onLoggedOut()
                    }
                ) {
                    Text("Sign Out")
                }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}

// ViewModel
@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val authManager: AuthManager
) : ViewModel() {
    
    fun logout() {
        viewModelScope.launch {
            // Track before anonymizing
            FS.event("User Logged Out", mapOf(
                "logoutMethod" to "settings_menu"
            ))
            
            // Anonymize
            FS.anonymize()
            
            // Clear auth state
            authManager.logout()
        }
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Forgetting to anonymize on logout
fun handleLogout() {
    clearAuthTokens()
    clearUserState()
    navigateToLogin()
    // Missing FS.anonymize()!
}

// BAD: Anonymizing multiple times
fun handleLogout() {
    FS.anonymize()
    FS.anonymize()
    FS.anonymize()  // Wasteful!
    navigateToLogin()
}

// BAD: Not tracking event before anonymize
fun handleLogout() {
    FS.anonymize()  // Lost opportunity to track logout event
    navigateToLogin()
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Anonymize the current user
FS.anonymize();
```

### ✅ GOOD Implementation Examples

#### Basic Logout Handler

```dart
// GOOD: Proper logout with Fullstory anonymization
class AuthManager {
  final ApiClient _apiClient;
  final PreferencesManager _prefsManager;
  final NavigationService _navigationService;

  AuthManager(this._apiClient, this._prefsManager, this._navigationService);

  Future<void> logout() async {
    try {
      // 1. Call backend logout endpoint
      await _apiClient.post('/auth/logout');

      // 2. Track logout event before anonymizing
      FS.event(name: 'User Logged Out', properties: {
        'logoutMethod': 'manual',
        'sessionDuration': getSessionDuration(),
      });

      // 3. Clear local authentication state
      await _prefsManager.clearAuthTokens();
      await _prefsManager.clearUserState();

      // 4. Anonymize in Fullstory
      FS.anonymize();

      // 5. Navigate to login
      _navigationService.navigateToLogin();

    } catch (e) {
      debugPrint('Logout failed: $e');
      // Still anonymize even if backend fails
      FS.anonymize();
      _navigationService.navigateToLogin();
    }
  }
}
```

**Why this is good:**
- ✅ Tracks event before anonymizing
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

#### Account Switching

```dart
// GOOD: Clean account switching with proper session boundaries
class AccountSwitcher {
  final AccountRepository _accountRepository;

  AccountSwitcher(this._accountRepository);

  Future<void> switchAccount(String newAccountId) async {
    final newUser = await _accountRepository.fetchAccountDetails(newAccountId);

    // Track the switch event under current user
    FS.event(name: 'Account Switch Initiated', properties: {
      'targetAccountId': newAccountId,
    });

    // Step 1: Anonymize current session
    FS.anonymize();

    // Step 2: Set up new account context
    await _accountRepository.setupAccountContext(newUser);

    // Step 3: Identify as new user
    FS.identify(newUser.id, userVars: {
      'displayName': newUser.name,
      'email': newUser.email,
      'accountType': newUser.type,
    });

    // Refresh UI
    refreshUserInterface();
  }
}
```

#### Session Timeout Handler

```dart
// GOOD: Handling session timeout with Fullstory
class SessionManager {
  static const _timeoutDuration = Duration(minutes: 30);
  Timer? _timeoutTimer;
  DateTime _lastActivityTime = DateTime.now();
  bool _isMonitoring = false;

  void startMonitoring() {
    if (_isMonitoring) return; // Prevent duplicate monitoring
    _isMonitoring = true;
    resetTimeout();
    
    // Listen for user interactions via GestureDetector wrapper
    // or through a global listener
  }

  void stopMonitoring() {
    _isMonitoring = false;
    _timeoutTimer?.cancel();
    _timeoutTimer = null;
  }

  /// Call this when the SessionManager is no longer needed
  void dispose() {
    stopMonitoring();
  }

  void resetTimeout() {
    _lastActivityTime = DateTime.now();
    _timeoutTimer?.cancel();
    
    _timeoutTimer = Timer(_timeoutDuration, () {
      handleSessionTimeout();
    });
  }

  void handleSessionTimeout() {
    // Track timeout event while still identified
    final inactivityDuration = DateTime.now().difference(_lastActivityTime);
    FS.event(name: 'Session Timeout', properties: {
      'inactivityDuration': inactivityDuration.inMilliseconds,
      'lastScreen': getCurrentScreenName(),
    });

    // Anonymize the session
    FS.anonymize();

    // Clear auth and show timeout UI
    clearAuthState();
    showTimeoutDialog();
  }
}
```

#### Widget Integration

```dart
// GOOD: Settings screen with logout
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          // Settings items...
          
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text(
              'Sign Out',
              style: TextStyle(color: Colors.red),
            ),
            onTap: () => _showLogoutConfirmation(context),
          ),
        ],
      ),
    );
  }

  void _showLogoutConfirmation(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sign Out'),
        content: const Text('Are you sure you want to sign out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _performLogout(context);
            },
            child: const Text(
              'Sign Out',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );
  }

  void _performLogout(BuildContext context) {
    // Track before anonymizing
    FS.event(name: 'User Logged Out', properties: {
      'logoutMethod': 'settings_menu',
    });

    // Anonymize
    FS.anonymize();

    // Navigate to login
    Navigator.of(context).pushNamedAndRemoveUntil(
      '/login',
      (route) => false,
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Forgetting to anonymize on logout
void handleLogout() {
  clearAuthTokens();
  clearUserState();
  navigateToLogin();
  // Missing FS.anonymize()!
}

// BAD: Anonymizing multiple times
void handleLogout() {
  FS.anonymize();
  FS.anonymize();
  FS.anonymize();  // Wasteful!
  navigateToLogin();
}

// BAD: Not tracking event before anonymize
void handleLogout() {
  FS.anonymize();  // Lost opportunity to track logout event
  navigateToLogin();
}
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Anonymize the current user
FullStory.anonymize();
```

### ✅ GOOD Implementation Examples

#### Basic Logout Handler

```javascript
// GOOD: Proper logout with Fullstory anonymization
import FullStory from '@fullstory/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

class AuthManager {
  async logout() {
    try {
      // 1. Call backend logout endpoint
      await fetch('/api/auth/logout', { method: 'POST' });

      // 2. Track logout event before anonymizing
      FullStory.event('User Logged Out', {
        logoutMethod: 'manual',
        sessionDuration: getSessionDuration(),
      });

      // 3. Clear local authentication state
      await AsyncStorage.multiRemove(['authToken', 'userState']);

      // 4. Anonymize in Fullstory
      FullStory.anonymize();

      // 5. Navigate to login
      NavigationService.navigate('Login');

    } catch (error) {
      console.error('Logout failed:', error);
      // Still anonymize even if backend fails
      FullStory.anonymize();
      NavigationService.navigate('Login');
    }
  }
}

export default new AuthManager();
```

**Why this is good:**
- ✅ Tracks event before anonymizing
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

#### Account Switching

```javascript
// GOOD: Clean account switching with proper session boundaries
async function switchAccount(newAccountId) {
  const newUser = await fetchAccountDetails(newAccountId);

  // Track the switch event under current user
  FullStory.event('Account Switch Initiated', {
    targetAccountId: newAccountId,
  });

  // Step 1: Anonymize current session
  FullStory.anonymize();

  // Step 2: Set up new account context
  await setupAccountContext(newUser);

  // Step 3: Identify as new user
  FullStory.identify(newUser.id, {
    displayName: newUser.name,
    email: newUser.email,
    accountType: newUser.type,
  });

  // Refresh UI
  refreshUserInterface();
}
```

#### Custom Hook for Logout

```jsx
// GOOD: Custom hook for logout
import { useCallback } from 'react';
import { useNavigation } from '@react-navigation/native';
import FullStory from '@fullstory/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export function useLogout() {
  const navigation = useNavigation();

  const logout = useCallback(async (reason = 'user_initiated') => {
    // Track logout event before anonymizing
    FullStory.event('User Logged Out', {
      logoutMethod: reason,
      sessionDuration: getSessionDuration(),
    });

    // Clear auth state
    await AsyncStorage.multiRemove(['authToken', 'userState']);

    // Anonymize
    FullStory.anonymize();

    // Navigate to login
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }],
    });
  }, [navigation]);

  return logout;
}

// Usage
function SettingsScreen() {
  const logout = useLogout();

  return (
    <Button title="Sign Out" onPress={() => logout()} />
  );
}
```

#### Settings Screen Component

```jsx
// GOOD: Settings screen with logout confirmation
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Alert, StyleSheet } from 'react-native';
import FullStory from '@fullstory/react-native';

function SettingsScreen({ navigation }) {
  const handleLogout = () => {
    Alert.alert(
      'Sign Out',
      'Are you sure you want to sign out?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Sign Out',
          style: 'destructive',
          onPress: performLogout,
        },
      ]
    );
  };

  const performLogout = async () => {
    // Track before anonymizing
    FullStory.event('User Logged Out', {
      logoutMethod: 'settings_menu',
    });

    // Anonymize
    FullStory.anonymize();

    // Navigate to login
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }],
    });
  };

  return (
    <View style={styles.container}>
      {/* Settings items... */}
      
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Sign Out</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  logoutButton: { 
    padding: 16, 
    backgroundColor: '#ff3b30', 
    borderRadius: 8 
  },
  logoutText: { 
    color: '#fff', 
    textAlign: 'center', 
    fontWeight: '600' 
  },
});

export default SettingsScreen;
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Forgetting to anonymize on logout
function handleLogout() {
  clearAuthTokens();
  clearUserState();
  navigateToLogin();
  // Missing FullStory.anonymize()!
}

// BAD: Anonymizing multiple times
function handleLogout() {
  FullStory.anonymize();
  FullStory.anonymize();
  FullStory.anonymize();  // Wasteful!
  navigateToLogin();
}

// BAD: Not tracking event before anonymize
function handleLogout() {
  FullStory.anonymize();  // Lost opportunity to track logout event
  navigateToLogin();
}

// BAD: Tracking after anonymize
function handleLogout() {
  FullStory.anonymize();
  // This event is now anonymous, not attributed to the user!
  FullStory.event('User Logged Out', {});
  navigateToLogin();
}
```

---

## Common Patterns (All Platforms)

### Logout Flow Order

All platforms should follow this order:

```
1. Track "User Logged Out" event (attributed to user)
2. Clear local authentication state
3. Call FS.anonymize() / FullStory.anonymize()
4. Navigate to login screen
```

### Session Timeout Pattern

```
1. Monitor user activity
2. Reset timer on activity
3. When timeout fires:
   a. Track "Session Timeout" event
   b. Anonymize
   c. Show timeout UI
   d. Navigate to login
```

### Account Switching Pattern

```
1. Track "Account Switch" event (current user)
2. Anonymize current session
3. Set up new account context
4. Identify as new user with new properties
5. Refresh UI
```

### Kiosk/Shared Device Pattern

```
1. Identify user when session starts
2. Set session timeout (shorter for kiosks)
3. Track session end event
4. Anonymize
5. Return to welcome/start screen
```

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/identification/anonymize-users/
- **Android**: https://developer.fullstory.com/mobile/android/identification/anonymize-users/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/identification/anonymize-users/
- **React Native**: https://developer.fullstory.com/mobile/react-native/identification/anonymize-users/
