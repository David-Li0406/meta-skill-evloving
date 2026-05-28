# ADHD Supplement App

A cross-platform mobile application built with Flutter for ADHD supplement education and referral tracking.

## Architecture

This project uses a hybrid of **Hexagonal Architecture** and **MVVM**:

- **domain/**: Models and Repository interfaces (Pure logic).
- **application/**: ViewModels managing state.
- **infrastructure/**: Firebase and Local service implementations.
- **presentation/**: UI Screens (Views) and Widgets.
- **config/**: Dependency Injection (GetIt) and global settings.

## Dependencies

- **Firebase**: Backend, Authentication, and Firestore.
- **URL Launcher**: Opening referral links.
- **Local Notifications**: User reminders and alerts.
- **Provider & GetIt**: State management and Dependency Injection.

## Getting Started

1. Ensure you have Flutter installed.
2. Run `flutter pub get` to install dependencies.
3. For Firebase, add your `google-services.json` (Android) and `GoogleService-Info.plist` (iOS) to the respective platforms.
