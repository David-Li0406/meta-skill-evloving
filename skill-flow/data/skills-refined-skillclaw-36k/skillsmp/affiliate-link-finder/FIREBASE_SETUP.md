# Firebase Setup Guide

This guide will walk you through setting up Firebase for the Daily Stack ADHD supplement tracking app.

## Prerequisites

- Flutter SDK installed
- Google account for Firebase
- Xcode (for iOS deployment)
- Android Studio (for Android deployment)

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `daily-stack-adhd` (or your preferred name)
4. Enable Google Analytics (recommended)
5. Select or create an Analytics account
6. Click "Create project"

## Step 2: Register iOS App

1. In Firebase Console, click the iOS icon
2. Enter iOS bundle ID: `com.yourcompany.adhdSupplementApp`
   - Find this in `ios/Runner.xcodeproj/project.pbxproj` (look for `PRODUCT_BUNDLE_IDENTIFIER`)
3. Download `GoogleService-Info.plist`
4. Move the file to `ios/Runner/` directory
5. Open `ios/Runner.xcworkspace` in Xcode
6. Right-click `Runner` folder → Add Files to "Runner"
7. Select `GoogleService-Info.plist` (ensure "Copy items if needed" is checked)

## Step 3: Register Android App

1. In Firebase Console, click the Android icon
2. Enter Android package name: `com.yourcompany.adhd_supplement_app`
   - Find this in `android/app/build.gradle` (look for `applicationId`)
3. Download `google-services.json`
4. Move the file to `android/app/` directory

### Update Android Build Files

**`android/build.gradle`:**
```gradle
buildscript {
    dependencies {
        // Add this line
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

**`android/app/build.gradle`:**
```gradle
// Add at the bottom of the file
apply plugin: 'com.google.gms.google-services'
```

## Step 4: Enable Firebase Services

### Enable Authentication

1. In Firebase Console, go to **Build** → **Authentication**
2. Click "Get started"
3. Enable **Email/Password** provider
4. Click "Save"

### Enable Firestore Database

1. In Firebase Console, go to **Build** → **Firestore Database**
2. Click "Create database"
3. Choose **Production mode** (we'll configure rules later)
4. Select a location (choose closest to your users)
5. Click "Enable"

### Configure Firestore Security Rules

Go to **Firestore Database** → **Rules** and paste:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Supplements collection (read-only for authenticated users)
    match /supplements/{supplementId} {
      allow read: if request.auth != null;
      allow write: if false; // Admin only via backend
    }
    
    // User stacks
    match /stacks/{stackId} {
      allow read, write: if request.auth != null && resource.data.userId == request.auth.uid;
    }
    
    // Daily logs
    match /logs/{logId} {
      allow read, write: if request.auth != null && resource.data.userId == request.auth.uid;
    }
  }
}
```

## Step 5: Install Dependencies

Run in your project directory:

```bash
flutter pub get
```

If you need to add Firebase CLI tools:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize FlutterFire
flutterfire configure
```

## Step 6: Initialize Firebase in App

The app already includes Firebase initialization in `main.dart`:

```dart
await Firebase.initializeApp();
```

## Step 7: Test Authentication

1. Run the app: `flutter run`
2. Try creating a new account
3. Check Firebase Console → Authentication → Users to see the new user

## Step 8: Seed Sample Data (Optional)

### Add Sample Supplements to Firestore

Go to Firestore Database → Add collection → `supplements`:

**Document 1 (Omega-3):**
```json
{
  "id": "omega-3",
  "name": "Omega-3 Fish Oil",
  "category": "Essential Fatty Acids",
  "dosage": "1000mg",
  "timeOfDay": "morning",
  "benefits": ["Focus", "Brain Health", "Mood"],
  "evidenceLevel": "high",
  "notes": "Take with food for better absorption"
}
```

**Document 2 (L-Theanine):**
```json
{
  "id": "l-theanine",
  "name": "L-Theanine",
  "category": "Nootropic",
  "dosage": "200mg",
  "timeOfDay": "morning",
  "benefits": ["Calm Focus", "Anxiety Reduction"],
  "evidenceLevel": "moderate",
  "notes": "Synergizes well with caffeine"
}
```

**Document 3 (Magnesium):**
```json
{
  "id": "magnesium",
  "name": "Magnesium Glycinate",
  "category": "Mineral",
  "dosage": "400mg",
  "timeOfDay": "evening",
  "benefits": ["Sleep", "Relaxation", "Muscle Recovery"],
  "evidenceLevel": "high",
  "notes": "Take before bed"
}
```

## Troubleshooting

### iOS Build Fails

- Ensure `GoogleService-Info.plist` is properly added to Xcode project
- Clean build: `flutter clean && flutter pub get`
- Check `ios/Podfile` has minimum deployment target iOS 11+

### Android Build Fails

- Verify `google-services.json` is in `android/app/`
- Check `build.gradle` files have correct plugin dependencies
- Run `cd android && ./gradlew clean`

### Authentication Errors

- Verify Email/Password provider is enabled in Firebase Console
- Check that `firebase_core` initializes before any Firebase calls
- Clear app data and try again

### Firestore Permission Errors

- Verify security rules are published
- Ensure user is authenticated before accessing Firestore
- Check that document paths match security rules

## Next Steps

Once Firebase is configured:

1. **Test the authentication flow** - Create account, login, logout
2. **Add real supplement data** to Firestore
3. **Implement supplement loading** in LibraryScreen
4. **Add user stack persistence** in StackBuilder
5. **Implement daily logging** in DailyStackScreen

## Additional Resources

- [FlutterFire Documentation](https://firebase.flutter.dev/)
- [Firebase Console](https://console.firebase.google.com/)
- [Firestore Data Modeling Best Practices](https://firebase.google.com/docs/firestore/data-model)
- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)

## Security Checklist

- [ ] Firebase project created
- [ ] iOS app registered with `GoogleService-Info.plist`
- [ ] Android app registered with `google-services.json`
- [ ] Email/Password authentication enabled
- [ ] Firestore database created
- [ ] Firestore security rules configured
- [ ] Test user account created
- [ ] Sample data seeded (optional)
- [ ] App successfully authenticates users
- [ ] Data reads/writes work correctly

---

**Last Updated:** January 2026  
**Maintained By:** Development Team
