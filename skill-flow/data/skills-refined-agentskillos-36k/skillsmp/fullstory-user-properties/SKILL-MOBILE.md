---
name: fullstory-user-properties-mobile
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
description: Mobile implementation guide for Fullstory's User Properties API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-user-properties
related_skills:
  - fullstory-user-properties
  - fullstory-identify-users
  - fullstory-page-properties
---

# Fullstory User Properties — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for property types, special fields, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | SDK | Method |
|----------|-----|--------|
| iOS | `FullStory` | `FS.setUserVars(_:)` |
| Android | `FullStory` | `FS.setUserVars(userVars)` |
| Flutter | `fullstory_flutter` | `FS.setUserVars(userVars)` |
| React Native | `@fullstory/react-native` | `FullStory.setUserVars(userVars)` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Set user properties
FS.setUserVars(_: [String: Any])
```

### ✅ GOOD Implementation Examples

#### Post-Identification Profile Enrichment

```swift
// GOOD: Add properties after initial identification
func handleLogin(credentials: LoginCredentials) async throws {
    let response = try await authenticateUser(credentials)
    let user = response.user
    
    // Step 1: Identify user
    FS.identify(uid: user.id, userVars: [
        "displayName": user.fullName,
        "email": user.email
    ])
    
    // Step 2: Enrich with additional profile data
    loadAndSetProfileData(userId: user.id)
}

func loadAndSetProfileData(userId: String) {
    Task {
        let profile = try await fetchUserProfile(userId)
        
        FS.setUserVars([
            "companyName": profile.company.name,
            "companySize": profile.company.employeeCount,
            "industry": profile.company.industry,
            "role": profile.role,
            "department": profile.department,
            "signupSource": profile.attribution.source
        ])
    }
}
```

#### Subscription/Plan Updates

```swift
// GOOD: Track subscription changes without re-identifying
func handlePlanUpgrade(newPlan: Plan) async {
    // Process the upgrade
    await processUpgrade(newPlan)
    
    // Update user properties
    FS.setUserVars([
        "plan": newPlan.name,
        "planTier": newPlan.tier,
        "monthlyPrice": newPlan.price,
        "billingCycle": newPlan.billingCycle,
        "planChangedAt": ISO8601DateFormatter().string(from: Date()),
        "previousPlan": getCurrentPlan().name
    ])
    
    // Also track as event
    FS.event(name: "Plan Upgraded", properties: [
        "from_plan": getCurrentPlan().name,
        "to_plan": newPlan.name,
        "price_difference": newPlan.price - getCurrentPlan().price
    ])
}
```

#### Progressive Profiling (Onboarding)

```swift
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
    
    func completeBasicInfo(_ data: BasicInfoData) {
        FS.setUserVars([
            "companyName": data.companyName,
            "companySize": data.companySize,
            "onboardingStep": 1,
            "onboardingStartedAt": ISO8601DateFormatter().string(from: Date())
        ])
    }
    
    func completeUseCaseSelection(_ useCases: UseCaseSelection) {
        FS.setUserVars([
            "primaryUseCase": useCases.primary,
            "secondaryUseCases": useCases.secondary,
            "onboardingStep": 2
        ])
    }
    
    func completeIntegrationSetup(_ integrations: IntegrationSetup) {
        FS.setUserVars([
            "connectedIntegrations": integrations.connected,
            "integrationCount": integrations.connected.count,
            "onboardingStep": 3
        ])
    }
    
    func completeOnboarding() {
        FS.setUserVars([
            "onboardingComplete": true,
            "onboardingCompletedAt": ISO8601DateFormatter().string(from: Date()),
            "onboardingStep": 4
        ])
    }
}
```

#### SwiftUI Integration

```swift
// GOOD: SwiftUI view model with property management
@MainActor
class UserProfileViewModel: ObservableObject {
    @Published var user: User?
    
    func updateSubscription(_ newPlan: Plan) async {
        do {
            let result = try await SubscriptionService.upgrade(to: newPlan)
            
            // Update user properties in Fullstory
            FS.setUserVars([
                "plan": result.plan.name,
                "planTier": result.plan.tier,
                "planUpdatedAt": ISO8601DateFormatter().string(from: Date())
            ])
            
            // Update local state
            user?.subscription = result
        } catch {
            handleError(error)
        }
    }
    
    func updatePreferences(_ preferences: UserPreferences) {
        FS.setUserVars([
            "notificationsEnabled": preferences.notificationsEnabled,
            "theme": preferences.theme,
            "language": preferences.language
        ])
    }
}
```

#### Feature Usage Tracking

```swift
// GOOD: Track feature adoption at user level
class FeatureUsageTracker {
    static let shared = FeatureUsageTracker()
    
    func trackFeatureFirstUse(_ featureName: String) {
        let key = "firstUsed_\(featureName)"
        
        FS.setUserVars([
            key: ISO8601DateFormatter().string(from: Date())
        ])
    }
    
    func updateFeatureEngagement(
        featuresUsed: [String],
        mostUsedFeature: String,
        engagementScore: Int
    ) {
        FS.setUserVars([
            "featuresUsed": featuresUsed,
            "mostUsedFeature": mostUsedFeature,
            "featureUsageScore": engagementScore,
            "lastFeatureUseAt": ISO8601DateFormatter().string(from: Date())
        ])
    }
}

// Usage
FeatureUsageTracker.shared.trackFeatureFirstUse("advanced_export")
FeatureUsageTracker.shared.updateFeatureEngagement(
    featuresUsed: ["dashboard", "reports", "advanced_export"],
    mostUsedFeature: "reports",
    engagementScore: 85
)
```

### ❌ BAD Implementation Examples

```swift
// BAD: Using setUserVars instead of identify for identification
FS.setUserVars([
    "uid": user.id,  // This doesn't establish identity!
    "displayName": user.name
])

// BAD: Wrong types
FS.setUserVars([
    "price": "$49.99",     // Should be 49.99
    "quantity": "3",       // Should be 3
    "isPremium": "yes"     // Should be true
])

// BAD: Excessive calls on every interaction
func handleScroll(_ offset: CGFloat) {
    // Don't do this!
    FS.setUserVars(["lastScrollPosition": offset])
}
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Set user properties
FS.setUserVars(userVars: Map<String, Any>)
```

### ✅ GOOD Implementation Examples

#### Post-Identification Profile Enrichment

```kotlin
// GOOD: Add properties after initial identification
suspend fun handleLogin(credentials: LoginCredentials) {
    val response = authenticateUser(credentials)
    val user = response.user
    
    // Step 1: Identify user
    FS.identify(user.id, mapOf(
        "displayName" to user.fullName,
        "email" to user.email
    ))
    
    // Step 2: Enrich with additional profile data
    loadAndSetProfileData(user.id)
}

private suspend fun loadAndSetProfileData(userId: String) {
    val profile = fetchUserProfile(userId)
    
    FS.setUserVars(mapOf(
        "companyName" to profile.company.name,
        "companySize" to profile.company.employeeCount,
        "industry" to profile.company.industry,
        "role" to profile.role,
        "department" to profile.department,
        "signupSource" to profile.attribution.source
    ))
}
```

#### Subscription/Plan Updates

```kotlin
// GOOD: Track subscription changes without re-identifying
suspend fun handlePlanUpgrade(newPlan: Plan) {
    // Process the upgrade
    processUpgrade(newPlan)
    
    // Update user properties
    FS.setUserVars(mapOf(
        "plan" to newPlan.name,
        "planTier" to newPlan.tier,
        "monthlyPrice" to newPlan.price,
        "billingCycle" to newPlan.billingCycle,
        "planChangedAt" to Instant.now().toString(),
        "previousPlan" to getCurrentPlan().name
    ))
    
    // Also track as event
    FS.event("Plan Upgraded", mapOf(
        "from_plan" to getCurrentPlan().name,
        "to_plan" to newPlan.name,
        "price_difference" to (newPlan.price - getCurrentPlan().price)
    ))
}
```

#### Progressive Profiling (Onboarding)

```kotlin
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
    
    fun completeBasicInfo(data: BasicInfoData) {
        FS.setUserVars(mapOf(
            "companyName" to data.companyName,
            "companySize" to data.companySize,
            "onboardingStep" to 1,
            "onboardingStartedAt" to Instant.now().toString()
        ))
    }
    
    fun completeUseCaseSelection(useCases: UseCaseSelection) {
        FS.setUserVars(mapOf(
            "primaryUseCase" to useCases.primary,
            "secondaryUseCases" to useCases.secondary,
            "onboardingStep" to 2
        ))
    }
    
    fun completeIntegrationSetup(integrations: IntegrationSetup) {
        FS.setUserVars(mapOf(
            "connectedIntegrations" to integrations.connected,
            "integrationCount" to integrations.connected.size,
            "onboardingStep" to 3
        ))
    }
    
    fun completeOnboarding() {
        FS.setUserVars(mapOf(
            "onboardingComplete" to true,
            "onboardingCompletedAt" to Instant.now().toString(),
            "onboardingStep" to 4
        ))
    }
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: ViewModel with property management
@HiltViewModel
class UserProfileViewModel @Inject constructor(
    private val subscriptionRepository: SubscriptionRepository
) : ViewModel() {
    
    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()
    
    fun updateSubscription(newPlan: Plan) {
        viewModelScope.launch {
            try {
                val result = subscriptionRepository.upgrade(newPlan)
                
                // Update user properties in Fullstory
                FS.setUserVars(mapOf(
                    "plan" to result.plan.name,
                    "planTier" to result.plan.tier,
                    "planUpdatedAt" to Instant.now().toString()
                ))
                
                // Update local state
                _user.update { it?.copy(subscription = result) }
            } catch (e: Exception) {
                handleError(e)
            }
        }
    }
    
    fun updatePreferences(preferences: UserPreferences) {
        FS.setUserVars(mapOf(
            "notificationsEnabled" to preferences.notificationsEnabled,
            "theme" to preferences.theme,
            "language" to preferences.language
        ))
    }
}
```

#### Feature Usage Tracking

```kotlin
// GOOD: Track feature adoption at user level
object FeatureUsageTracker {
    
    fun trackFeatureFirstUse(featureName: String) {
        val key = "firstUsed_$featureName"
        
        FS.setUserVars(mapOf(
            key to Instant.now().toString()
        ))
    }
    
    fun updateFeatureEngagement(
        featuresUsed: List<String>,
        mostUsedFeature: String,
        engagementScore: Int
    ) {
        FS.setUserVars(mapOf(
            "featuresUsed" to featuresUsed,
            "mostUsedFeature" to mostUsedFeature,
            "featureUsageScore" to engagementScore,
            "lastFeatureUseAt" to Instant.now().toString()
        ))
    }
}

// Usage
FeatureUsageTracker.trackFeatureFirstUse("advanced_export")
FeatureUsageTracker.updateFeatureEngagement(
    featuresUsed = listOf("dashboard", "reports", "advanced_export"),
    mostUsedFeature = "reports",
    engagementScore = 85
)
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Using setUserVars instead of identify for identification
FS.setUserVars(mapOf(
    "uid" to user.id,  // This doesn't establish identity!
    "displayName" to user.name
))

// BAD: Wrong types
FS.setUserVars(mapOf(
    "price" to "$49.99",     // Should be 49.99
    "quantity" to "3",       // Should be 3
    "isPremium" to "yes"     // Should be true
))

// BAD: Excessive calls
fun onScrollChanged(offset: Float) {
    // Don't do this!
    FS.setUserVars(mapOf("lastScrollPosition" to offset))
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Set user properties
FS.setUserVars(Map<String, dynamic> userVars);
```

### ✅ GOOD Implementation Examples

#### Post-Identification Profile Enrichment

```dart
// GOOD: Add properties after initial identification
Future<void> handleLogin(LoginCredentials credentials) async {
  final response = await authenticateUser(credentials);
  final user = response.user;
  
  // Step 1: Identify user
  FS.identify(uid: user.id, userVars: {
    'displayName': user.fullName,
    'email': user.email,
  });
  
  // Step 2: Enrich with additional profile data
  await loadAndSetProfileData(user.id);
}

Future<void> loadAndSetProfileData(String userId) async {
  final profile = await fetchUserProfile(userId);
  
  FS.setUserVars({
    'companyName': profile.company.name,
    'companySize': profile.company.employeeCount,
    'industry': profile.company.industry,
    'role': profile.role,
    'department': profile.department,
    'signupSource': profile.attribution.source,
  });
}
```

#### Subscription/Plan Updates

```dart
// GOOD: Track subscription changes without re-identifying
Future<void> handlePlanUpgrade(Plan newPlan) async {
  // Process the upgrade
  await processUpgrade(newPlan);
  
  // Update user properties
  FS.setUserVars({
    'plan': newPlan.name,
    'planTier': newPlan.tier,
    'monthlyPrice': newPlan.price,
    'billingCycle': newPlan.billingCycle,
    'planChangedAt': DateTime.now().toIso8601String(),
    'previousPlan': getCurrentPlan().name,
  });
  
  // Also track as event
  FS.event(name: 'Plan Upgraded', properties: {
    'from_plan': getCurrentPlan().name,
    'to_plan': newPlan.name,
    'price_difference': newPlan.price - getCurrentPlan().price,
  });
}
```

#### Progressive Profiling (Onboarding)

```dart
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
  
  void completeBasicInfo(BasicInfoData data) {
    FS.setUserVars({
      'companyName': data.companyName,
      'companySize': data.companySize,
      'onboardingStep': 1,
      'onboardingStartedAt': DateTime.now().toIso8601String(),
    });
  }
  
  void completeUseCaseSelection(UseCaseSelection useCases) {
    FS.setUserVars({
      'primaryUseCase': useCases.primary,
      'secondaryUseCases': useCases.secondary,
      'onboardingStep': 2,
    });
  }
  
  void completeIntegrationSetup(IntegrationSetup integrations) {
    FS.setUserVars({
      'connectedIntegrations': integrations.connected,
      'integrationCount': integrations.connected.length,
      'onboardingStep': 3,
    });
  }
  
  void completeOnboarding() {
    FS.setUserVars({
      'onboardingComplete': true,
      'onboardingCompletedAt': DateTime.now().toIso8601String(),
      'onboardingStep': 4,
    });
  }
}
```

#### Provider/Riverpod Integration

```dart
// GOOD: Using Riverpod for property management
final userPropertiesProvider = Provider((ref) => UserPropertiesService());

class UserPropertiesService {
  
  void updateSubscription(Subscription subscription) {
    FS.setUserVars({
      'plan': subscription.plan,
      'planTier': subscription.tier,
      'mrr': subscription.mrr,
      'planUpdatedAt': DateTime.now().toIso8601String(),
    });
  }
  
  void updatePreferences(UserPreferences preferences) {
    FS.setUserVars({
      'notificationsEnabled': preferences.notificationsEnabled,
      'theme': preferences.theme,
      'language': preferences.language,
    });
  }
  
  void updateOnboardingProgress(int step, bool complete) {
    FS.setUserVars({
      'onboardingStep': step,
      'onboardingComplete': complete,
      if (complete) 'onboardingCompletedAt': DateTime.now().toIso8601String(),
    });
  }
}
```

#### Feature Usage Tracking

```dart
// GOOD: Track feature adoption at user level
class FeatureUsageTracker {
  static final FeatureUsageTracker instance = FeatureUsageTracker._();
  FeatureUsageTracker._();
  
  void trackFeatureFirstUse(String featureName) {
    final key = 'firstUsed_$featureName';
    
    FS.setUserVars({
      key: DateTime.now().toIso8601String(),
    });
  }
  
  void updateFeatureEngagement({
    required List<String> featuresUsed,
    required String mostUsedFeature,
    required int engagementScore,
  }) {
    FS.setUserVars({
      'featuresUsed': featuresUsed,
      'mostUsedFeature': mostUsedFeature,
      'featureUsageScore': engagementScore,
      'lastFeatureUseAt': DateTime.now().toIso8601String(),
    });
  }
}

// Usage
FeatureUsageTracker.instance.trackFeatureFirstUse('advanced_export');
FeatureUsageTracker.instance.updateFeatureEngagement(
  featuresUsed: ['dashboard', 'reports', 'advanced_export'],
  mostUsedFeature: 'reports',
  engagementScore: 85,
);
```

### ❌ BAD Implementation Examples

```dart
// BAD: Using setUserVars instead of identify for identification
FS.setUserVars({
  'uid': user.id,  // This doesn't establish identity!
  'displayName': user.name,
});

// BAD: Wrong types
FS.setUserVars({
  'price': '\$49.99',    // Should be 49.99
  'quantity': '3',       // Should be 3
  'isPremium': 'yes',    // Should be true
});

// BAD: Excessive calls
void onScrollUpdate(double offset) {
  // Don't do this!
  FS.setUserVars({'lastScrollPosition': offset});
}
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Set user properties
FullStory.setUserVars(userVars: object);
```

### ✅ GOOD Implementation Examples

#### Post-Identification Profile Enrichment

```javascript
// GOOD: Add properties after initial identification
async function handleLogin(credentials) {
  const response = await authenticateUser(credentials);
  const user = response.user;
  
  // Step 1: Identify user
  FullStory.identify(user.id, {
    displayName: user.fullName,
    email: user.email,
  });
  
  // Step 2: Enrich with additional profile data
  await loadAndSetProfileData(user.id);
}

async function loadAndSetProfileData(userId) {
  const profile = await fetchUserProfile(userId);
  
  FullStory.setUserVars({
    companyName: profile.company.name,
    companySize: profile.company.employeeCount,
    industry: profile.company.industry,
    role: profile.role,
    department: profile.department,
    signupSource: profile.attribution.source,
  });
}
```

#### Subscription/Plan Updates

```javascript
// GOOD: Track subscription changes without re-identifying
async function handlePlanUpgrade(newPlan) {
  // Process the upgrade
  await processUpgrade(newPlan);
  
  // Update user properties
  FullStory.setUserVars({
    plan: newPlan.name,
    planTier: newPlan.tier,
    monthlyPrice: newPlan.price,
    billingCycle: newPlan.billingCycle,
    planChangedAt: new Date().toISOString(),
    previousPlan: getCurrentPlan().name,
  });
  
  // Also track as event
  FullStory.event('Plan Upgraded', {
    from_plan: getCurrentPlan().name,
    to_plan: newPlan.name,
    price_difference: newPlan.price - getCurrentPlan().price,
  });
}
```

#### Progressive Profiling (Onboarding)

```javascript
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
  
  completeBasicInfo(data) {
    FullStory.setUserVars({
      companyName: data.companyName,
      companySize: data.companySize,
      onboardingStep: 1,
      onboardingStartedAt: new Date().toISOString(),
    });
  }
  
  completeUseCaseSelection(useCases) {
    FullStory.setUserVars({
      primaryUseCase: useCases.primary,
      secondaryUseCases: useCases.secondary,
      onboardingStep: 2,
    });
  }
  
  completeIntegrationSetup(integrations) {
    FullStory.setUserVars({
      connectedIntegrations: integrations.connected,
      integrationCount: integrations.connected.length,
      onboardingStep: 3,
    });
  }
  
  completeOnboarding() {
    FullStory.setUserVars({
      onboardingComplete: true,
      onboardingCompletedAt: new Date().toISOString(),
      onboardingStep: 4,
    });
  }
}
```

#### React Hook Integration

```jsx
// GOOD: Custom hook for user properties
import { useCallback } from 'react';
import FullStory from '@fullstory/react-native';

export function useUserProperties() {
  const setProperties = useCallback((properties) => {
    FullStory.setUserVars(properties);
  }, []);
  
  const updateSubscription = useCallback((subscription) => {
    setProperties({
      plan: subscription.plan,
      planTier: subscription.tier,
      mrr: subscription.mrr,
      planUpdatedAt: new Date().toISOString(),
    });
  }, [setProperties]);
  
  const updatePreferences = useCallback((preferences) => {
    setProperties({
      notificationsEnabled: preferences.notificationsEnabled,
      theme: preferences.theme,
      language: preferences.language,
    });
  }, [setProperties]);
  
  const updateOnboardingProgress = useCallback((step, complete) => {
    setProperties({
      onboardingStep: step,
      onboardingComplete: complete,
      ...(complete && { onboardingCompletedAt: new Date().toISOString() }),
    });
  }, [setProperties]);
  
  return { setProperties, updateSubscription, updatePreferences, updateOnboardingProgress };
}

// Usage
function SettingsScreen() {
  const { updatePreferences } = useUserProperties();
  
  const handleSavePreferences = (preferences) => {
    updatePreferences(preferences);
    savePreferences(preferences);
  };
  
  return <PreferencesForm onSave={handleSavePreferences} />;
}
```

#### Feature Usage Tracking

```javascript
// GOOD: Track feature adoption at user level
class FeatureUsageTracker {
  static trackFeatureFirstUse(featureName) {
    const key = `firstUsed_${featureName}`;
    
    FullStory.setUserVars({
      [key]: new Date().toISOString(),
    });
  }
  
  static updateFeatureEngagement({ featuresUsed, mostUsedFeature, engagementScore }) {
    FullStory.setUserVars({
      featuresUsed,
      mostUsedFeature,
      featureUsageScore: engagementScore,
      lastFeatureUseAt: new Date().toISOString(),
    });
  }
}

// Usage
FeatureUsageTracker.trackFeatureFirstUse('advanced_export');
FeatureUsageTracker.updateFeatureEngagement({
  featuresUsed: ['dashboard', 'reports', 'advanced_export'],
  mostUsedFeature: 'reports',
  engagementScore: 85,
});
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Using setUserVars instead of identify for identification
FullStory.setUserVars({
  uid: user.id,  // This doesn't establish identity!
  displayName: user.name,
});

// BAD: Wrong types
FullStory.setUserVars({
  price: '$49.99',     // Should be 49.99
  quantity: '3',       // Should be 3
  isPremium: 'yes',    // Should be true
});

// BAD: Setting properties on every render
function BadComponent({ user }) {
  // This fires on EVERY render!
  FullStory.setUserVars({ lastSeen: new Date().toISOString() });
  
  return <View>...</View>;
}

// BAD: Excessive calls
function handleScroll(event) {
  // Don't do this!
  FullStory.setUserVars({ lastScrollY: event.nativeEvent.contentOffset.y });
}
```

---

## Common Patterns (All Platforms)

### User Properties Manager

Create a centralized service to standardize property management:

| Platform | Pattern |
|----------|---------|
| iOS | Singleton class with static methods |
| Android | Object/companion object or Hilt-injected class |
| Flutter | Singleton or Provider/Riverpod |
| React Native | Custom hook or context provider |

### Property Categories

Recommended property categories for comprehensive user profiles:

```
Identity: displayName, email
Subscription: plan, planTier, billingCycle, mrr
Engagement: lastActiveAt, sessionCount, featureUsageScore
Business: companyName, companySize, industry, role
Lifecycle: signupDate, trialStartedAt, onboardingComplete
Attribution: referralSource, campaign, landingPage
```

### Events + Properties Pattern

Track **both** the change (event) and the new state (property):

```
User upgrades plan:
  1. Event: "Plan Upgraded" with from_plan, to_plan, price_change
  2. Property: plan = "enterprise", planChangedAt = now
```

### Batching Updates

For frequently changing data, batch updates to avoid rate limits:

```
1. Queue properties for batched update
2. Debounce with ~1 second delay
3. Send combined update
4. Flush immediately for important changes (subscriptions)
```

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/identification/set-user-properties/
- **Android**: https://developer.fullstory.com/mobile/android/identification/set-user-properties/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/identification/set-user-properties/
- **React Native**: https://developer.fullstory.com/mobile/react-native/identification/set-user-properties/
