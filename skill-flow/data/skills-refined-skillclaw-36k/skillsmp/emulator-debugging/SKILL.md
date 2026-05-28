---
name: emulator-debugging
description: Diagnoses Firebase Emulator issues across Android Emulator, physical devices, and web without modifying production behavior.
---

# Emulator Debugging

## When to use this skill

- When the Flutter app fails to connect to Firestore/Auth/Functions in DEV.
- When physical Android devices show "Connection refused" or network errors.
- When switching between Emulators and Production.

## How to use it

1. **Check Initialization Order**:
   - Verify `Firebase.initializeApp()` runs _before_ any emulator connection code.
   - Verify emulator config runs _immediately after_.
2. **Verify Host Configuration**:
   - **Android Emulator**: Use `10.0.2.2`.
   - **Physical Device**: Use the computer's local LAN IP (e.g., `192.168.1.x`). DO NOT use `localhost` or `127.0.0.1`.
   - **Web**: Use `localhost`.
3. **Network Security (Android)**:
   - Ensure `android/app/src/main/res/xml/network_security_config.xml` allows cleartext traffic for the emulator IP.
   - Ensure `AndroidManifest.xml` references this config.
4. **Auth Emulator Check**:
   - Remember: Google Sign-In and other 3rd party providers often fail on physical devices pointing to the Auth Emulator due to redirect issues. Prefer real Auth for physical device testing if possible, or ensure strict redirect URL handling.
