---
name: github-actions-debugging
description: Use this skill when debugging GitHub Actions workflows, CI build failures, or deployment issues.
---

# GitHub Actions Debugging Skill

This skill provides expert guidance for analyzing and fixing GitHub Actions workflow failures, CI build issues, and deployment problems.

## When to Use This Skill

- GitHub Actions workflow failures
- CI build errors that don't occur locally
- Test failures only in CI environment
- Artifact upload/download issues
- Secret/credential problems
- Cache-related failures
- Timeout issues
- Deployment failures

## Workflow Overview

1. **Identify Failed Runs**: Use `gh run list` to find failed workflows.
2. **Analyze Logs**: Access logs via GitHub UI or CLI to diagnose issues.
3. **Diagnose Issues**: Identify root causes from log output.
4. **Fix Issues**: Apply necessary fixes to workflow files or source code.
5. **Verify**: Re-run workflows to confirm fixes.

## Accessing Workflow Logs

### Via GitHub UI
1. Go to repository → Actions tab
2. Click on failed workflow run
3. Click on failed job
4. Expand failed step to see logs

### Via GitHub CLI
```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# Download logs
gh run download <run-id>
```

## Common CI Failure Patterns

### Flutter/Dart Setup Issues
**Error**: Flutter not found or wrong version
```yaml
- name: Setup Flutter
  uses: subosito/flutter-action@v2
  with:
    flutter-version: '<version>'  # Verify this matches requirements
    channel: 'stable'
    cache: true
```
**Solution**: Update Flutter version in `.github/workflows/build.yml` and ensure it exists on the stable channel.

### Gradle Build Failures
**Error**: Gradle daemon issues or out of memory
```yaml
- name: Setup Gradle for CI
  run: cp android/gradle-ci.properties android/gradle.properties
```
**Solution**: Check `android/gradle-ci.properties` settings and ensure heap size is adequate.

### Dependency Issues
**Error**: Package resolution failures
```yaml
- name: Get dependencies
  run: flutter pub get
```
**Solution**: Check `pubspec.yaml` for invalid dependencies and verify versions.

### Test Failures
**Error**: Tests pass locally but fail in CI
```yaml
- name: Run tests with coverage
  run: flutter test --coverage --concurrency=$(nproc)
```
**Solution**: Check for timing issues and ensure file paths are relative.

### Cache Issues
**Error**: Build slower or cache not working
```yaml
- name: Cache Flutter packages
  uses: actions/cache@v4
  with:
    path: |
      ~/.pub-cache
      ${{ github.workspace }}/.dart_tool
    key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
```
**Solution**: Verify cache key and paths.

### Artifact Upload Issues
**Error**: Artifacts not found or upload fails
```yaml
- name: Upload APK
  uses: actions/upload-artifact@v5
  with:
    name: android-apk
    path: build/app/outputs/flutter-apk/app-release.apk
    retention-days: 7
```
**Solution**: Ensure build succeeded and file paths are correct.

## Quick CI Debug Checklist

- [ ] Check workflow logs in GitHub Actions tab
- [ ] Verify Flutter version matches project requirements
- [ ] Confirm Java version is correct
- [ ] Review gradle-ci.properties settings
- [ ] Check all required secrets are set
- [ ] Verify dependency versions in pubspec.yaml
- [ ] Test same commands locally
- [ ] Review cache configuration
- [ ] Check artifact paths

## Best Practices

1. **Always test locally first**: Run same commands as CI.
2. **Use verbose logging**: Add `--verbose` to debug commands.
3. **Check all secrets**: Verify secrets exist and are correct.
4. **Monitor cache usage**: Clear cache if builds become inconsistent.
5. **Keep workflows simple**: Complex workflows are harder to debug.

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter CI/CD Guide](https://docs.flutter.dev/deployment/cd)
- [Gradle Build Performance](https://docs.gradle.org/current/userguide/performance.html)