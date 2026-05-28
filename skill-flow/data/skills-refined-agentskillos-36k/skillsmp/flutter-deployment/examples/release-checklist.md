# Release Checklist

Comprehensive pre-release checklist for Flutter app deployments to ensure quality, compliance, and successful releases.

## Pre-Release Preparation

### Version Management

- [ ] Update version number in `pubspec.yaml`
  - [ ] Follow semantic versioning (MAJOR.MINOR.PATCH)
  - [ ] Increment build number
  - [ ] Ensure version is higher than previous release

- [ ] Update CHANGELOG.md
  - [ ] Document new features
  - [ ] List bug fixes
  - [ ] Note breaking changes
  - [ ] Credit contributors

- [ ] Tag release in Git
  ```bash
  git tag -a v1.2.3 -m "Release version 1.2.3"
  git push origin v1.2.3
  ```

### Code Quality

- [ ] Run static analysis
  ```bash
  flutter analyze
  ```

- [ ] Check code formatting
  ```bash
  dart format --set-exit-if-changed .
  ```

- [ ] Run all unit tests
  ```bash
  flutter test
  ```

- [ ] Run integration tests
  ```bash
  flutter test integration_test/
  ```

- [ ] Verify test coverage meets threshold (e.g., >80%)
  ```bash
  flutter test --coverage
  genhtml coverage/lcov.info -o coverage/html
  ```

- [ ] Review and address all TODO/FIXME comments

- [ ] Remove debug code and console logs

### Dependencies

- [ ] Update dependencies to latest stable versions
  ```bash
  flutter pub upgrade
  ```

- [ ] Check for security vulnerabilities
  ```bash
  flutter pub outdated
  ```

- [ ] Verify no deprecated APIs are used

- [ ] Remove unused dependencies

- [ ] Review dependency licenses for compliance

### Configuration

- [ ] Update API endpoints for production
- [ ] Verify environment-specific configurations
- [ ] Check API keys and secrets are not hardcoded
- [ ] Verify analytics and crash reporting are configured
- [ ] Update feature flags for production
- [ ] Review and update app permissions

## Platform-Specific Checks

### Android

#### Build Configuration

- [ ] Verify `applicationId` is correct in `build.gradle.kts`
- [ ] Check `minSdk`, `targetSdk`, and `compileSdk` versions
- [ ] Ensure ProGuard/R8 rules are properly configured
- [ ] Review signing configuration

#### Testing

- [ ] Test on multiple Android versions (minimum supported to latest)
- [ ] Test on different screen sizes (phone, tablet)
- [ ] Test on different manufacturers (Samsung, Google, etc.)
- [ ] Verify app works on low-end devices
- [ ] Test with different languages/locales
- [ ] Test deep linking and notifications
- [ ] Verify permissions are properly requested

#### Play Store Requirements

- [ ] Update store listing
  - [ ] App description (4000 chars max)
  - [ ] Short description (80 chars max)
  - [ ] Feature graphic (1024x500)
  - [ ] Screenshots (min 2, max 8 per device type)
  - [ ] App icon (512x512)
  - [ ] Video (optional but recommended)

- [ ] Complete content rating questionnaire

- [ ] Review privacy policy URL (required if app collects data)

- [ ] Prepare release notes (500 chars max per language)

- [ ] Set up pricing and distribution

- [ ] Configure in-app products (if applicable)

#### Build and Upload

- [ ] Build signed app bundle
  ```bash
  flutter build appbundle --release --obfuscate --split-debug-info=symbols/
  ```

- [ ] Test app bundle installation locally
  ```bash
  bundletool build-apks --bundle=app.aab --output=app.apks
  bundletool install-apks --apks=app.apks
  ```

- [ ] Upload to Play Console internal testing first

- [ ] Verify build processes successfully

- [ ] Save symbols for crash reporting

### iOS

#### Build Configuration

- [ ] Verify Bundle ID matches App Store Connect
- [ ] Check deployment target matches minimum iOS version
- [ ] Review Xcode project settings (signing, capabilities)
- [ ] Ensure correct provisioning profiles

#### Testing

- [ ] Test on multiple iOS versions (minimum supported to latest)
- [ ] Test on iPhone and iPad
- [ ] Test on different screen sizes
- [ ] Test with VoiceOver (accessibility)
- [ ] Test deep linking and universal links
- [ ] Verify push notifications work
- [ ] Test app in different locales
- [ ] Test with TestFlight before production

#### App Store Requirements

- [ ] Update App Store listing
  - [ ] App name (30 chars max)
  - [ ] Subtitle (30 chars max)
  - [ ] Promotional text (170 chars, updatable without review)
  - [ ] Description (4000 chars max)
  - [ ] Keywords (100 chars, comma-separated)
  - [ ] Screenshots (all required sizes)
  - [ ] App icon (1024x1024, no alpha)
  - [ ] App preview video (optional)

- [ ] Complete privacy policy information

- [ ] Fill in App Review Information
  - [ ] Contact information
  - [ ] Demo account credentials (if login required)
  - [ ] Notes for reviewer
  - [ ] Attachments (if needed)

- [ ] Complete export compliance information

- [ ] Prepare What's New in This Version (4000 chars max)

#### Build and Upload

- [ ] Build IPA
  ```bash
  flutter build ipa --release --obfuscate --split-debug-info=symbols/
  ```

- [ ] Upload to App Store Connect via Transporter or Xcode

- [ ] Wait for build processing (typically 15-30 minutes)

- [ ] Distribute to TestFlight for final verification

- [ ] Submit for App Store review

### Web

- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)

- [ ] Verify responsive design on different screen sizes

- [ ] Test PWA installation

- [ ] Verify service worker caching

- [ ] Test offline functionality

- [ ] Check performance (Lighthouse audit score >90)

- [ ] Verify SEO metadata

- [ ] Test deep linking

- [ ] Build production web app
  ```bash
  flutter build web --release --web-renderer canvaskit
  ```

- [ ] Deploy to hosting platform

- [ ] Verify deployed version works correctly

## Security Checks

### Code Security

- [ ] Remove all debug/test code
- [ ] Ensure no API keys or secrets in code
- [ ] Verify certificate pinning (if implemented)
- [ ] Check for hardcoded credentials
- [ ] Review third-party library security

### Data Security

- [ ] Verify sensitive data is encrypted at rest
- [ ] Check network traffic uses HTTPS
- [ ] Review data retention policies
- [ ] Ensure proper authentication implementation
- [ ] Verify secure storage of user data

### Permissions

- [ ] Request only necessary permissions
- [ ] Provide clear explanations for each permission
- [ ] Implement runtime permission requests properly
- [ ] Handle permission denials gracefully

## Performance Optimization

- [ ] Run app in profile mode and analyze performance
  ```bash
  flutter run --profile
  ```

- [ ] Check app startup time (<3 seconds ideal)

- [ ] Verify smooth animations (60fps)

- [ ] Monitor memory usage and check for leaks

- [ ] Optimize image sizes and formats

- [ ] Analyze bundle size
  ```bash
  flutter build apk --analyze-size
  ```

- [ ] Verify network requests are optimized

- [ ] Check battery usage is acceptable

## Compliance and Legal

- [ ] Review terms of service

- [ ] Verify privacy policy is up to date

- [ ] Check compliance with GDPR/CCPA (if applicable)

- [ ] Review app store guidelines
  - [ ] [Google Play Policy](https://play.google.com/about/developer-content-policy/)
  - [ ] [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

- [ ] Verify age rating is appropriate

- [ ] Check content complies with policies

- [ ] Review all third-party content usage rights

## Monitoring and Analytics

- [ ] Verify crash reporting is configured
  - [ ] Firebase Crashlytics
  - [ ] Sentry
  - [ ] Bugsnag

- [ ] Ensure analytics tracking is working
  - [ ] Google Analytics
  - [ ] Firebase Analytics
  - [ ] Amplitude

- [ ] Set up alerts for critical errors

- [ ] Configure performance monitoring

- [ ] Test that events are being tracked correctly

## Documentation

- [ ] Update README.md

- [ ] Update API documentation (if applicable)

- [ ] Document known issues

- [ ] Update user guides/help documentation

- [ ] Prepare internal release notes for team

- [ ] Document deployment process changes

## Backup and Rollback Plan

- [ ] Backup current production version

- [ ] Save keystore/certificates securely

- [ ] Save symbol files for crash reporting

- [ ] Document rollback procedure

- [ ] Keep previous version available for quick rollback

- [ ] Test rollback process in staging

## Final Verification

### Pre-Submission Checklist

- [ ] All automated tests passing

- [ ] Manual QA testing complete

- [ ] No critical or high-priority bugs

- [ ] Performance benchmarks met

- [ ] Security audit passed

- [ ] Legal compliance verified

- [ ] Store listings complete and reviewed

- [ ] Release notes written and reviewed

- [ ] Team notified of pending release

### Post-Build Verification

- [ ] Install and test release build on real devices

- [ ] Verify app icon displays correctly

- [ ] Check app name is correct

- [ ] Test critical user flows end-to-end

- [ ] Verify in-app purchases work (if applicable)

- [ ] Test push notifications

- [ ] Verify deep links work

## Submission

### Internal Testing (Recommended First Step)

**Android:**
- [ ] Upload to Play Store Internal Testing track
- [ ] Share with QA team
- [ ] Collect feedback
- [ ] Fix any critical issues

**iOS:**
- [ ] Upload to TestFlight
- [ ] Distribute to Internal Testing group
- [ ] Collect feedback
- [ ] Fix any critical issues

### Beta Testing (Optional)

**Android:**
- [ ] Promote to Closed/Open Testing track
- [ ] Recruit beta testers
- [ ] Monitor feedback and crash reports
- [ ] Iterate based on feedback

**iOS:**
- [ ] Submit for TestFlight External Testing review
- [ ] Distribute to external beta testers
- [ ] Monitor feedback and crash reports
- [ ] Iterate based on feedback

### Production Submission

**Android:**
- [ ] Upload to Production track
- [ ] Set rollout percentage (recommend starting with 10-20%)
- [ ] Monitor crash reports and ratings
- [ ] Gradually increase rollout
- [ ] Complete rollout to 100%

**iOS:**
- [ ] Submit for App Store Review
- [ ] Monitor review status
- [ ] Respond to reviewer questions promptly
- [ ] Upon approval, release according to plan
- [ ] Consider phased release option

## Post-Release

### Monitoring (First 24 Hours)

- [ ] Monitor crash rate (<1% is good)

- [ ] Watch for spike in 1-star ratings

- [ ] Check for critical bugs in reviews

- [ ] Monitor analytics for unusual patterns

- [ ] Verify update adoption rate

- [ ] Check server load if backend-dependent

### Communication

- [ ] Announce release to users (social media, email, in-app)

- [ ] Notify customer support team of changes

- [ ] Update website with new features

- [ ] Publish blog post about release (optional)

- [ ] Monitor and respond to user reviews

### Documentation

- [ ] Update internal wiki/documentation

- [ ] Document any issues encountered during release

- [ ] Note improvements for next release process

- [ ] Update release timeline/calendar

- [ ] Archive build artifacts and symbols

### Retrospective

- [ ] Schedule release retrospective meeting

- [ ] Document lessons learned

- [ ] Identify process improvements

- [ ] Update release checklist based on learnings

## Emergency Rollback

If critical issues are discovered:

**Android:**
```bash
# Halt staged rollout
# In Play Console: Release > Production > Halt rollout

# Or promote previous version
# In Play Console: Release > Production > Manage > Promote previous version
```

**iOS:**
```bash
# Submit new build with fix as soon as possible
# App Store doesn't support rollback, only phased release pause

# In App Store Connect:
# My Apps > [App] > App Store > [Version] > Phased Release > Pause
```

**Web:**
```bash
# Deploy previous version
git checkout v1.2.2  # Previous stable version
flutter build web --release
firebase deploy --only hosting
```

## Quick Reference

### Essential Commands

```bash
# Version check
grep "^version:" pubspec.yaml

# Tests
flutter analyze
flutter test --coverage

# Builds
flutter build apk --release
flutter build appbundle --release --obfuscate --split-debug-info=symbols/
flutter build ipa --release --obfuscate --split-debug-info=symbols/
flutter build web --release

# Size analysis
flutter build apk --analyze-size
```

### Version Bump Script

```bash
#!/bin/bash
# bump-version.sh

OLD_VERSION=$(grep "^version:" pubspec.yaml | cut -d' ' -f2)
echo "Current version: $OLD_VERSION"

echo "Enter new version (MAJOR.MINOR.PATCH):"
read NEW_VERSION

# Update pubspec.yaml
sed -i.bak "s/^version: .*/version: $NEW_VERSION+$BUILD_NUMBER/" pubspec.yaml

# Update CHANGELOG.md
echo "## $NEW_VERSION - $(date +%Y-%m-%d)" | cat - CHANGELOG.md > temp && mv temp CHANGELOG.md

echo "Version updated to $NEW_VERSION"
```

## Summary

Following this comprehensive checklist ensures:
- ✅ High-quality releases with minimal bugs
- ✅ Compliance with app store policies
- ✅ Proper security and privacy measures
- ✅ Smooth user experience across platforms
- ✅ Quick rollback capability if needed
- ✅ Effective monitoring and issue detection
- ✅ Team coordination and communication
- ✅ Continuous improvement of release process

Customize this checklist for your specific app and team workflow. Keep it as a living document that evolves with your release process. Consider automating as many checks as possible through CI/CD pipelines.

**Pro tip:** Use a project management tool (Jira, Asana, Trello) to create a release checklist template that can be copied for each release, ensuring nothing is missed and providing visibility to the entire team.
