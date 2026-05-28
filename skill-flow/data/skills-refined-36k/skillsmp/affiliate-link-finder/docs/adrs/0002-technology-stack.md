# 2. Technology Stack Selection

Date: 2026-01-18

## Status

Accepted

## Context

We need to build a performant, cross-platform mobile application for ADHD supplement education. The stack needs to support rapid development, reliable backend services, and easy state management.

## Decision

We have selected the following technology stack:

- **Framework**: **Flutter** (Dart) for cross-platform mobile development (iOS/Android).
- **Backend / DB**: **Firebase** (Firestore) for real-time database and authentication.
- **State Management**: **Provider** for dependency injection and state management.
- **Navigation**: Standard Flutter Navigator 2.0 (MaterialPageRoutes).
- **External Services**:
    - `url_launcher` for opening affiliate links.
    - `flutter_local_notifications` for future reminders.

## Consequences

### Positive
- **Single Codebase**: Flutter allows deploying to both iOS and Android from a single Dart codebase.
- **Rapid Iteration**: Firebase provides "backend-as-a-service," reducing the need for custom server maintenance.
- **Community Support**: Provider is a standard, widely-supported solution for state management in Flutter.

### Negative
- **Vendor Lock-in**: Heavy reliance on Firebase makes migrating to another backend provider more difficult later.
- **App Size**: Flutter apps can have a larger initial download size compared to native apps.
