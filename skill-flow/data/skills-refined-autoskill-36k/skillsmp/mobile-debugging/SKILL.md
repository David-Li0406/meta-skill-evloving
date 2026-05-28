---
name: mobile-debugging
description: Use for React Native / Expo troubleshooting (Metro bundler, native modules, simulator/emulator issues).
---

## Workflow

1. Capture the exact error and environment (RN/Expo version, platform, device).
2. Separate concerns:
   - bundler issues (Metro)
   - native build issues (Xcode/Gradle)
   - runtime issues (permissions, network, JS exceptions)
3. Reproduce with the smallest command set (e.g., one `expo start` / `npx react-native run-*`).
4. Validate configuration files and dependencies align with the chosen workflow.
5. Apply minimal change; re-run the exact failing path.

## Common checks

- Clear caches only after capturing logs (e.g., Metro/Gradle).
- Confirm environment variables and platform-specific config are consistent.
