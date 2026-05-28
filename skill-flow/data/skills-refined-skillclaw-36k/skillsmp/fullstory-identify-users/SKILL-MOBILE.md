---
name: fullstory-identify-users-mobile
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
description: Mobile implementation guide for Fullstory's User Identification API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-identify-users
related_skills:
  - fullstory-identify-users
  - fullstory-anonymize-users
  - fullstory-user-properties
---

# Fullstory Identify Users — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for identity linking, session behavior, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | SDK | Identify Method | Anonymize Method |
|----------|-----|-----------------|------------------|
| iOS | `FullStory` | `FS.identify(uid:userVars:)` | `FS.anonymize()` |
| Android | `FullStory` | `FS.identify(uid, userVars)` | `FS.anonymize()` |
| Flutter | `fullstory_flutter` | `FS.identify(uid: '', userVars: {})` | `FS.anonymize()` |
| React Native | `@fullstory/react-native` | `FullStory.identify(uid, userVars)` | `FullStory.anonymize()` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Identify user
FS.identify(uid: String, userVars: [String: Any]?)

// Anonymize (logout)
FS.anonymize()
```

### ✅ GOOD Implementation Examples

#### Basic Login Identification

```swift
// GOOD: Call identify immediately after successful login
func handleLogin(credentials: LoginCredentials) async throws {
    let response = try await authenticateUser(credentials)
    let user = response.user
    
    // Identify user in Fullstory right after successful auth
    FS.identify(uid: user.id, userVars: [
        "displayName": user.fullName,
        "email": user.email,
        "accountType": user.plan,
        "signupDate": ISO8601DateFormatter().string(from: user.createdAt)
    ])
    
    // Continue with login flow
    navigateToDashboard()
}
```

#### App Launch with Existing Session

```swift
// GOOD: Check auth state and identify on app launch
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication, 
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        initializeFullstory()
        return true
    }
    
    private func initializeFullstory() {
        guard let currentUser = AuthManager.shared.currentUser else {
            // User is not logged in - remains anonymous
            return
        }
        
        FS.identify(uid: currentUser.id, userVars: [
            "displayName": currentUser.name,
            "email": currentUser.email,
            "role": currentUser.role,
            "companyId": currentUser.organizationId ?? "",
            "plan": currentUser.subscription.plan
        ])
    }
}
```

#### SwiftUI Integration

```swift
// GOOD: SwiftUI app with identity management
@main
struct MyApp: App {
    @StateObject private var authManager = AuthManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .onAppear {
                    setupFullstoryIdentity()
                }
                .onChange(of: authManager.currentUser) { user in
                    updateFullstoryIdentity(user: user)
                }
        }
    }
    
    private func setupFullstoryIdentity() {
        if let user = authManager.currentUser {
            FS.identify(uid: user.id, userVars: [
                "displayName": user.name,
                "email": user.email
            ])
        }
    }
    
    private func updateFullstoryIdentity(user: User?) {
        if let user = user {
            FS.identify(uid: user.id, userVars: [
                "displayName": user.name,
                "email": user.email
            ])
        } else {
            FS.anonymize()
        }
    }
}
```

#### OAuth Callback Handling

```swift
// GOOD: Identify after OAuth callback
func handleOAuthCallback(url: URL) async {
    guard let code = URLComponents(url: url, resolvingAgainstBaseURL: false)?
            .queryItems?.first(where: { $0.name == "code" })?.value else {
        redirectToLogin()
        return
    }
    
    do {
        let (user, tokens) = try await exchangeOAuthCode(code)
        
        // Store tokens
        KeychainManager.shared.setTokens(tokens)
        
        // Identify in Fullstory
        FS.identify(uid: user.id, userVars: [
            "displayName": user.name,
            "email": user.email,
            "authProvider": "google",
            "ssoOrganization": user.hostedDomain ?? ""
        ])
        
        navigateToDashboard()
    } catch {
        handleOAuthError(error)
    }
}
```

#### Account Switching

```swift
// GOOD: Properly handle account switching
class AccountSwitcher {
    func switchToAccount(_ newUser: User) {
        // First, anonymize the current session
        FS.anonymize()
        
        // Then identify as the new user
        FS.identify(uid: newUser.id, userVars: [
            "displayName": newUser.name,
            "email": newUser.email
        ])
    }
    
    func logout() {
        FS.anonymize()
        AuthManager.shared.clearSession()
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Using email as UID
FS.identify(uid: user.email, userVars: nil)

// BAD: Identifying before auth completes
func handleLoginTap() {
    FS.identify(uid: usernameField.text!, userVars: nil)  // Don't do this!
    authenticateUser(credentials)  // This might fail
}

// BAD: Missing displayName and email
FS.identify(uid: user.id, userVars: nil)
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Identify user
FS.identify(uid: String, userVars: Map<String, Any>?)

// Anonymize (logout)
FS.anonymize()
```

### ✅ GOOD Implementation Examples

#### Basic Login Identification

```kotlin
// GOOD: Call identify immediately after successful login
suspend fun handleLogin(credentials: LoginCredentials) {
    try {
        val response = authenticateUser(credentials)
        val user = response.user
        
        // Identify user in Fullstory right after successful auth
        FS.identify(user.id, mapOf(
            "displayName" to user.fullName,
            "email" to user.email,
            "accountType" to user.plan,
            "signupDate" to user.createdAt.toIsoString()
        ))
        
        // Continue with login flow
        navigateToDashboard()
    } catch (e: Exception) {
        handleLoginError(e)
    }
}
```

#### Application Startup

```kotlin
// GOOD: Check auth state and identify on app start
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        
        initializeFullstory()
    }
    
    private fun initializeFullstory() {
        val currentUser = AuthManager.currentUser ?: return
        
        FS.identify(currentUser.id, mapOf(
            "displayName" to currentUser.name,
            "email" to currentUser.email,
            "role" to currentUser.role,
            "companyId" to (currentUser.organizationId ?: ""),
            "plan" to currentUser.subscription.plan
        ))
    }
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: Compose app with identity management
@Composable
fun MyApp(authViewModel: AuthViewModel = hiltViewModel()) {
    val currentUser by authViewModel.currentUser.collectAsState()
    
    LaunchedEffect(currentUser) {
        currentUser?.let { user ->
            FS.identify(user.id, mapOf(
                "displayName" to user.name,
                "email" to user.email
            ))
        } ?: FS.anonymize()
    }
    
    AppNavigation()
}
```

#### OAuth Callback Handling

```kotlin
// GOOD: Identify after OAuth callback
suspend fun handleOAuthCallback(intent: Intent) {
    val uri = intent.data ?: return
    val code = uri.getQueryParameter("code") ?: run {
        redirectToLogin()
        return
    }
    
    try {
        val (user, tokens) = exchangeOAuthCode(code)
        
        // Store tokens
        TokenManager.setTokens(tokens)
        
        // Identify in Fullstory
        FS.identify(user.id, mapOf(
            "displayName" to user.name,
            "email" to user.email,
            "authProvider" to "google",
            "ssoOrganization" to (user.hostedDomain ?: "")
        ))
        
        navigateToDashboard()
    } catch (e: Exception) {
        handleOAuthError(e)
    }
}
```

#### Account Switching

```kotlin
// GOOD: Properly handle account switching
class AccountSwitcher @Inject constructor() {
    fun switchToAccount(newUser: User) {
        // First, anonymize the current session
        FS.anonymize()
        
        // Then identify as the new user
        FS.identify(newUser.id, mapOf(
            "displayName" to newUser.name,
            "email" to newUser.email
        ))
    }
    
    fun logout() {
        FS.anonymize()
        AuthManager.clearSession()
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Using email as UID
FS.identify(user.email, null)

// BAD: Identifying before auth completes
fun handleLoginClick() {
    FS.identify(usernameField.text, null)  // Don't do this!
    authenticateUser(credentials)  // This might fail
}

// BAD: Missing displayName and email
FS.identify(user.id, null)
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Identify user
FS.identify(uid: String, userVars: Map<String, dynamic>?);

// Anonymize (logout)
FS.anonymize();
```

### ✅ GOOD Implementation Examples

#### Basic Login Identification

```dart
// GOOD: Call identify immediately after successful login
Future<void> handleLogin(LoginCredentials credentials) async {
  try {
    final response = await authenticateUser(credentials);
    final user = response.user;
    
    // Identify user in Fullstory right after successful auth
    FS.identify(uid: user.id, userVars: {
      'displayName': user.fullName,
      'email': user.email,
      'accountType': user.plan,
      'signupDate': user.createdAt.toIso8601String(),
    });
    
    // Continue with login flow
    navigateToDashboard();
  } catch (e) {
    handleLoginError(e);
  }
}
```

#### App Startup

```dart
// GOOD: Check auth state and identify on app start
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Fullstory
  await initializeFullstory();
  
  runApp(MyApp());
}

Future<void> initializeFullstory() async {
  final currentUser = await AuthManager.instance.getCurrentUser();
  
  if (currentUser != null) {
    FS.identify(uid: currentUser.id, userVars: {
      'displayName': currentUser.name,
      'email': currentUser.email,
      'role': currentUser.role,
      'companyId': currentUser.organizationId ?? '',
      'plan': currentUser.subscription.plan,
    });
  }
}
```

#### Provider/Riverpod Integration

```dart
// GOOD: Using Provider for identity management
class AuthNotifier extends ChangeNotifier {
  User? _currentUser;
  
  User? get currentUser => _currentUser;
  
  Future<void> login(LoginCredentials credentials) async {
    final response = await authenticateUser(credentials);
    _currentUser = response.user;
    
    // Identify in Fullstory
    FS.identify(uid: _currentUser!.id, userVars: {
      'displayName': _currentUser!.name,
      'email': _currentUser!.email,
    });
    
    notifyListeners();
  }
  
  void logout() {
    FS.anonymize();
    _currentUser = null;
    notifyListeners();
  }
}
```

#### OAuth Callback Handling

```dart
// GOOD: Identify after OAuth callback
Future<void> handleOAuthCallback(Uri uri) async {
  final code = uri.queryParameters['code'];
  
  if (code == null) {
    redirectToLogin();
    return;
  }
  
  try {
    final result = await exchangeOAuthCode(code);
    final user = result.user;
    final tokens = result.tokens;
    
    // Store tokens
    await TokenStorage.setTokens(tokens);
    
    // Identify in Fullstory
    FS.identify(uid: user.id, userVars: {
      'displayName': user.name,
      'email': user.email,
      'authProvider': 'google',
      'ssoOrganization': user.hostedDomain ?? '',
    });
    
    navigateToDashboard();
  } catch (e) {
    handleOAuthError(e);
  }
}
```

#### Account Switching

```dart
// GOOD: Properly handle account switching
class AccountSwitcher {
  void switchToAccount(User newUser) {
    // First, anonymize the current session
    FS.anonymize();
    
    // Then identify as the new user
    FS.identify(uid: newUser.id, userVars: {
      'displayName': newUser.name,
      'email': newUser.email,
    });
  }
  
  void logout() {
    FS.anonymize();
    AuthManager.instance.clearSession();
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Using email as UID
FS.identify(uid: user.email, userVars: null);

// BAD: Identifying before auth completes
void handleLoginTap() {
  FS.identify(uid: usernameController.text, userVars: null);  // Don't do this!
  authenticateUser(credentials);  // This might fail
}

// BAD: Missing displayName and email
FS.identify(uid: user.id, userVars: null);
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Identify user
FullStory.identify(uid: string, userVars?: object);

// Anonymize (logout)
FullStory.anonymize();
```

### ✅ GOOD Implementation Examples

#### Basic Login Identification

```javascript
// GOOD: Call identify immediately after successful login
async function handleLogin(credentials) {
  try {
    const response = await authenticateUser(credentials);
    const user = response.user;
    
    // Identify user in Fullstory right after successful auth
    FullStory.identify(user.id, {
      displayName: user.fullName,
      email: user.email,
      accountType: user.plan,
      signupDate: user.createdAt,  // ISO8601 format
    });
    
    // Continue with login flow
    navigation.navigate('Dashboard');
  } catch (error) {
    handleLoginError(error);
  }
}
```

#### App Startup

```javascript
// GOOD: Check auth state and identify on app start
import { useEffect } from 'react';
import FullStory from '@fullstory/react-native';

function App() {
  useEffect(() => {
    initializeFullstory();
  }, []);
  
  return <AppNavigator />;
}

async function initializeFullstory() {
  const currentUser = await AuthManager.getCurrentUser();
  
  if (currentUser) {
    FullStory.identify(currentUser.id, {
      displayName: currentUser.name,
      email: currentUser.email,
      role: currentUser.role,
      companyId: currentUser.organizationId || '',
      plan: currentUser.subscription.plan,
    });
  }
}
```

#### React Hook Integration

```jsx
// GOOD: Custom hook for Fullstory identity
import { useEffect } from 'react';
import { useAuth } from './auth-context';
import FullStory from '@fullstory/react-native';

export function useFullstoryIdentity() {
  const { user, isAuthenticated, isLoading } = useAuth();
  
  useEffect(() => {
    if (isLoading) return;
    
    if (isAuthenticated && user) {
      FullStory.identify(user.id, {
        displayName: `${user.firstName} ${user.lastName}`,
        email: user.email,
        role: user.role,
        features: user.enabledFeatures,
        lastLoginAt: new Date().toISOString(),
      });
    } else {
      FullStory.anonymize();
    }
  }, [user, isAuthenticated, isLoading]);
}

// Usage
function App() {
  useFullstoryIdentity();
  return <AppContent />;
}
```

#### OAuth Callback Handling

```javascript
// GOOD: Identify after OAuth callback
async function handleOAuthCallback(url) {
  const params = new URLSearchParams(url.split('?')[1]);
  const code = params.get('code');
  
  if (!code) {
    navigation.navigate('Login');
    return;
  }
  
  try {
    const { user, tokens } = await exchangeOAuthCode(code);
    
    // Store tokens
    await AsyncStorage.setItem('tokens', JSON.stringify(tokens));
    
    // Identify in Fullstory
    FullStory.identify(user.id, {
      displayName: user.name,
      email: user.email,
      authProvider: 'google',
      ssoOrganization: user.hostedDomain || '',
    });
    
    navigation.navigate('Dashboard');
  } catch (error) {
    handleOAuthError(error);
  }
}
```

#### Account Switching

```javascript
// GOOD: Properly handle account switching
class AccountSwitcher {
  switchToAccount(newUser) {
    // First, anonymize the current session
    FullStory.anonymize();
    
    // Then identify as the new user
    FullStory.identify(newUser.id, {
      displayName: newUser.name,
      email: newUser.email,
    });
  }
  
  logout() {
    FullStory.anonymize();
    AuthManager.clearSession();
  }
}
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Using email as UID
FullStory.identify(user.email);

// BAD: Identifying before auth completes
function handleLoginPress() {
  FullStory.identify(usernameInput);  // Don't do this!
  authenticateUser(credentials);  // This might fail
}

// BAD: Missing displayName and email
FullStory.identify(user.id);

// BAD: Identifying on every render
function ProfileScreen({ user }) {
  // This runs on EVERY render!
  FullStory.identify(user.id, { displayName: user.name });
  
  return <View>...</View>;
}
```

---

## Common Patterns (All Platforms)

### Identity Manager Class

Create a centralized service to standardize identity management:

| Platform | Pattern |
|----------|---------|
| iOS | Singleton class |
| Android | Hilt-injected class or object |
| Flutter | Singleton or Provider |
| React Native | Custom hook or context |

### Account Switching Flow

```
1. Call anonymize() to end current identified session
2. Call identify() with new user's uid and properties
3. Track current user state in your app
```

### Progressive Identification

For guest → account creation flows:

```
1. Keep user anonymous during guest flow
2. Track events (Guest Checkout Started, etc.)
3. Call identify() when user creates account
4. All prior anonymous sessions automatically link
```

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/identification/identify-users/
- **Android**: https://developer.fullstory.com/mobile/android/identification/identify-users/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/identification/identify-users/
- **React Native**: https://developer.fullstory.com/mobile/react-native/identification/identify-users/
