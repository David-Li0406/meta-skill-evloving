# Settings & Account Management

This document covers user account, privacy, subscription, and app settings.

## Overview
Users can manage their profile, privacy preferences, subscription status, and app appearance.

## Screens

### 1. `UserProfileScreen`
**Location**: `lib/presentation/views/user_profile_screen.dart`

The main profile hub.

**Sections:**
- **Profile Info**: Name, email, profile picture.
- **Medication List**: Currently taking (for safety checks).
- **Preferences**: Notification times, units (mg/mcg).
- **Logout**: Signs user out of Firebase Auth.

**Data Source:**
Fetches user data from Firebase Authentication + custom user document in Firestore.

### 2. `PrivacySettingsScreen`
**Location**: `lib/presentation/views/privacy_settings_screen.dart`

**ViewModel**: `PrivacyViewModel`

Manages GDPR/CCPA compliance features.

**Features:**
- **Export Data**: Generates a JSON file of all user logs and stacks.
- **Delete Account**: Permanent deletion with confirmation.
- **Data Sharing Preferences**: Opt-in/out of anonymized analytics.

**Current State:**
Mock implementation. Real export/delete requires backend API integration.

### 3. `SubscriptionScreen`
**Location**: `lib/presentation/views/subscription_screen.dart`

**ViewModel**: `SubscriptionViewModel`

Manages in-app purchases (Pro tier).

**Tiers:**
- **Free**: Basic tracking, 3 stacks max.
- **Pro** ($4.99/month): Unlimited stacks, advanced insights, ad-free.

**Features:**
- Restore purchases (for users switching devices).
- Subscription status display.
- Cancel/manage via app store links.

**Integration:**
Uses mock `BillingService`. Production requires `in_app_purchase` or RevenueCat.

### 4. `AppAppearanceScreen`
**Location**: `lib/presentation/views/app_appearance_screen.dart`

Customization for app UI.

**Options:**
- **Theme**: Light, Dark, Auto.
- **Icon**: Choose from 5 alternative app icons (iOS only).
- **Animations**: Toggle "Low Stimulation Mode" (disables confetti, reduces motion).

**Accessibility:**
Low Stimulation Mode is critical for users with sensory sensitivities.

### 5. `SystemHealthScreen`
**Location**: `lib/presentation/views/system_health_screen.dart`

Diagnostic screen for power users and troubleshooting.

**Displays:**
- Battery optimization status (is app exempt?).
- Notification permission status.
- Background refresh enabled.
- Storage usage by the app.

**Links:**
Deep links to OS settings for each permission.

## Related Services
- `AuthProvider`: Manages Firebase authentication state.
- `BillingService`: Handles subscription logic (currently mocked).
