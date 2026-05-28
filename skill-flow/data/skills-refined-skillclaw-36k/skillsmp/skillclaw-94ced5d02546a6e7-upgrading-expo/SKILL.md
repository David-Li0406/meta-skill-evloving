---
name: upgrading-expo
description: Use this skill when upgrading Expo SDK versions and resolving dependency issues.
---

# Step-by-Step Upgrade Process

1. **Upgrade Expo and dependencies**
   ```bash
   npx expo install expo@latest
   npx expo install --fix
   ```

2. **Run diagnostics**
   ```bash
   npx expo-doctor
   ```

3. **Clear caches and reinstall**
   ```bash
   npx expo export -p ios --clear
   rm -rf node_modules .expo
   watchman watch-del-all
   ```

## Breaking Changes Checklist

- Check for removed APIs in release notes.
- Update import paths for moved modules.
- Review native module changes requiring prebuild.
- Test all camera, audio, and video features.
- Verify navigation still works correctly.

## Prebuild for Native Changes

If upgrading requires native changes:
```bash
npx expo prebuild --clean
```
Ensure the project is not a bare workflow app before running this command.

## Clear caches for bare workflow

- Clear the cocoapods cache for iOS:
   ```bash
   cd ios && pod install --repo-update
   ```
- Clear derived data for Xcode:
   ```bash
   npx expo run:ios --no-build-cache
   ```
- Clear the Gradle cache for Android:
   ```bash
   cd android && ./gradlew clean
   ```

## Housekeeping

- Review release notes for the target SDK version at [Expo Changelog](https://expo.dev/changelog).
- If using Expo SDK 54 or later, ensure `react-native-worklets` is installed for `react-native-reanimated` to work.
- Enable React Compiler in SDK 54+ by adding `"experiments": { "reactCompiler": true }` to `app.json`.
- Delete `sdkVersion` from `app.json` to let Expo manage it automatically.
- Remove implicit packages from `package.json`: `@babel/core`, `babel-preset-expo`, `expo-constants`.
- If `babel.config.js` only contains 'babel-preset-expo', delete the file.
- If `metro.config.js` only contains Expo defaults, delete the file.

## Deprecated Packages

| Old Package          | Replacement                                          |
| -------------------- | ---------------------------------------------------- |
| `expo-av`            | `expo-audio` and `expo-video`                       |
| `expo-permissions`   | Individual package permission APIs                   |