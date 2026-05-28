---
name: release
description: Create a new release. Bumps version, updates changelog, creates fastlane changelog, commits, tags, and pushes.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Release Skill

Create a new release for MateDroid.

## Pre-flight Checks

1. Ensure you're on the `main` branch with no uncommitted changes
2. Verify the `[Unreleased]` section in `CHANGELOG.md` has content to release

## Release Process

### 1. Determine Version

Ask the user what type of release:
- **patch** (0.10.0 → 0.10.1): Bug fixes only
- **minor** (0.10.0 → 0.11.0): New features, backwards compatible
- **major** (0.10.0 → 1.0.0): Breaking changes (requires explicit user confirmation)

### 2. Update Version in build.gradle.kts

Edit `app/build.gradle.kts`:
- Increment `versionCode` by 1
- Update `versionName` to the new version

### 3. Update CHANGELOG.md

1. Change `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` (today's date)
2. Add a new empty `## [Unreleased]` section above it
3. Add the new version link at the bottom:
   ```
   [X.Y.Z]: https://github.com/vide/matedroid/compare/vPREVIOUS...vX.Y.Z
   ```
4. Update the `[Unreleased]` link to compare from the new version

### 4. Create Fastlane Changelog (English)

Create `fastlane/metadata/android/en-US/changelogs/{versionCode}.txt` with the release notes.

Format (max 500 chars for Play Store):
```
More human readable and engaging new features and major fixes overview. Do NOT mention external contributors here.

Added:
- Feature 1
- Feature 2

Changed:
- Change 1

Fixed:
- Fix 1
```

Keep it concise - this appears in Play Store and F-Droid. Make the opening text engaging without it being too verbose or showy.

### 5. Translate Changelogs (Automatic)

Automatically translate the English changelog and write the translations to:
- `fastlane/metadata/android/it-IT/changelogs/{versionCode}.txt` (Italian)
- `fastlane/metadata/android/es-ES/changelogs/{versionCode}.txt` (Spanish)
- `fastlane/metadata/android/ca-ES/changelogs/{versionCode}.txt` (Catalan)

Do this immediately after creating the English changelog - no user interaction needed.

Translation guidelines:
- Keep the same structure and format as the English version
- Do NOT translate technical terms: AC, DC, kW, kWh, API, etc.
- Keep proper nouns unchanged: MateDroid, Teslamate, Tesla, GitHub, etc.
- Maintain the same tone: engaging but concise
- Each translation must also respect the 500 character limit

### 6. Commit and Tag

```bash
git add -A
git commit -m "chore: release vX.Y.Z"
git tag -a vX.Y.Z -m "Release X.Y.Z"
```

### 7. Push

```bash
git push origin main
git push origin vX.Y.Z
```

### 8. Create GitHub Release

Use `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file -` with the changelog content as the one in Fastlane.
Mention external contributors, highlighting new ones and giving credit. 

The GitHub Actions workflow will automatically:
- Build APK and AAB
- Upload to GitHub release
- Deploy to Google Play (alpha track)
