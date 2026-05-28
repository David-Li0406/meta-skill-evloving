---
name: deploying-mobile-apps
description: Automate build and deployment. Use when setting up CI/CD pipelines, configuring Fastlane, or preparing release builds for iOS and Android.
---

# Deployment Pipeline

## When to use this skill
- When setting up CI/CD (GitHub Actions, Bitrise, etc.).
- When configuring Fastlane.
- When preparing production or beta releases.
- When troubleshooting build failures in CI.

## Environment Setup
Define distinct environments with separate configuration (API keys, Bundle IDs):
1.  **Development**: Debug builds, localhost/dev API.
2.  **Staging**: Release/Profile builds, staging API, distributed via TestFlight/Firebase.
3.  **Production**: Release builds, prod API, App Store/Play Store.

## Build Process
Automate these steps in your CI pipeline:
1.  **Linting**: Run ESLint and TypeScript check (`tsc --noEmit`).
2.  **Testing**: Run unit and integration tests. Fail build on error.
3.  **Build**: Generate the binary (.ipa / .aab) for the target environment.
4.  **Source Maps**: Upload source maps to error tracking service (Sentry/BugSnag).

## iOS Deployment (Fastlane)
- **Certificates**: Use `match` to manage code signing certificates and profiles securely in a private repo.
- **Versioning**: Automate build number incrementation (`increment_build_number`).
- **Beta**: Upload to TestFlight.
- **Release**: Submit to App Store Review (or hold for manual release).

## Android Deployment
- **Signing**: Securely manage Keystore and signing keys (inject via CI secrets).
- **Versioning**: Increment `versionCode` automatically.
- **Formats**: Always deploy App Bundles (`.aab`) to Play Console, not APKs.
- **Tracks**: Deploy to `internal` or `alpha` tracks first, then promote to `production`.

## Pre-deployment Checklist
Before triggering a production release:
- [ ] **Tests**: All unit and E2E tests passing?
- [ ] **Clean Console**: No critical errors or warnings in logs?
- [ ] **Performance**: Startup time and frame rate within limits?
- [ ] **Accessibility**: Basic a11y checks passed?
- [ ] **Legal**: Privacy policy up to date?
- [ ] **Store Assets**: Screenshots and descriptions ready?
