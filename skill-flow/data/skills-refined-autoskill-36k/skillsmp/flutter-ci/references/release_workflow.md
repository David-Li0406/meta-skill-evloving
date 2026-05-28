# Release Workflow

## Complete Release Automation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

env:
  FLUTTER_VERSION: '3.19.0'

jobs:
  # ==================== VALIDATION ====================
  validate:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      build_number: ${{ steps.version.outputs.build_number }}

    steps:
      - uses: actions/checkout@v4

      - name: Extract version info
        id: version
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          echo "version=$VERSION" >> $GITHUB_OUTPUT

          # Get build number from pubspec
          BUILD=$(grep "version:" pubspec.yaml | sed 's/.*+//')
          echo "build_number=$BUILD" >> $GITHUB_OUTPUT

      - name: Validate version format
        run: |
          if ! [[ "${{ steps.version.outputs.version }}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Invalid version format. Expected: X.Y.Z"
            exit 1
          fi

  # ==================== TESTING ====================
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
          cache: true

      - run: flutter pub get
      - run: flutter analyze --fatal-infos
      - run: flutter test --coverage

      - name: Check coverage
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}' | tr -d '%')
          echo "Coverage: $COVERAGE%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "::error::Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

  # ==================== BUILD ANDROID ====================
  build-android:
    needs: [validate, test]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
          cache: true

      - name: Setup signing
        run: |
          echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 -d > android/app/upload-keystore.jks
          cat > android/key.properties << EOF
          storePassword=${{ secrets.ANDROID_STORE_PASSWORD }}
          keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
          keyAlias=magentaline
          storeFile=upload-keystore.jks
          EOF

      - run: flutter pub get

      - name: Build APK
        run: flutter build apk --release --split-per-abi

      - name: Build AAB
        run: flutter build appbundle --release

      - uses: actions/upload-artifact@v4
        with:
          name: android-release
          path: |
            build/app/outputs/flutter-apk/*.apk
            build/app/outputs/bundle/release/*.aab

  # ==================== BUILD iOS ====================
  build-ios:
    needs: [validate, test]
    runs-on: macos-14

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
          cache: true

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: ios

      - name: Setup keychain
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
        run: |
          security create-keychain -p "$MATCH_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$MATCH_PASSWORD" build.keychain
          security set-keychain-settings -lut 21600 build.keychain

      - name: Fetch certificates
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_URL: ${{ secrets.MATCH_GIT_URL }}
        run: cd ios && bundle exec fastlane match appstore --readonly

      - run: flutter pub get
      - run: cd ios && pod install

      - name: Build IPA
        run: flutter build ipa --release --export-options-plist=ios/ExportOptions.plist

      - uses: actions/upload-artifact@v4
        with:
          name: ios-release
          path: build/ios/ipa/*.ipa

  # ==================== DEPLOY ====================
  deploy-android:
    needs: [build-android]
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: actions/download-artifact@v4
        with:
          name: android-release
          path: build/

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: android

      - name: Create Play Store key
        run: echo '${{ secrets.PLAY_STORE_JSON }}' > android/fastlane/play-store-key.json

      - name: Deploy to internal track
        run: |
          cd android && bundle exec fastlane supply \
            --aab ../build/bundle/release/app-release.aab \
            --track internal

  deploy-ios:
    needs: [build-ios]
    runs-on: macos-14
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: actions/download-artifact@v4
        with:
          name: ios-release
          path: build/ios/ipa/

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: ios

      - name: Upload to TestFlight
        env:
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_KEY }}
        run: |
          cd ios && bundle exec fastlane pilot upload \
            --ipa ../build/ios/ipa/MagentaLine.ipa \
            --skip_waiting_for_build_processing

  # ==================== GITHUB RELEASE ====================
  github-release:
    needs: [build-android, build-ios, validate]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Generate changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREVIOUS_TAG" ]; then
            CHANGELOG=$(git log --pretty=format:"- %s" $PREVIOUS_TAG..HEAD)
          else
            CHANGELOG=$(git log --pretty=format:"- %s" HEAD~10..HEAD)
          fi
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGELOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          name: MagentaLine v${{ needs.validate.outputs.version }}
          body: |
            ## What's Changed

            ${{ steps.changelog.outputs.changelog }}

            ## Downloads

            ### Android
            - **APK (arm64-v8a)**: For most modern Android devices
            - **APK (armeabi-v7a)**: For older Android devices
            - **AAB**: For Play Store distribution

            ### iOS
            - **IPA**: Available via TestFlight

          files: |
            artifacts/android-release/*.apk
            artifacts/android-release/*.aab
            artifacts/ios-release/*.ipa
          draft: false
          prerelease: ${{ contains(github.ref, 'beta') || contains(github.ref, 'alpha') }}

  # ==================== NOTIFICATIONS ====================
  notify:
    needs: [deploy-android, deploy-ios, github-release]
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Notify success
        if: ${{ !contains(needs.*.result, 'failure') }}
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{
              "text": "✅ MagentaLine v${{ needs.validate.outputs.version }} released successfully!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*MagentaLine v${{ needs.validate.outputs.version }}* has been released!\n• Android: Deployed to internal track\n• iOS: Uploaded to TestFlight\n• GitHub Release: Created"
                  }
                }
              ]
            }'

      - name: Notify failure
        if: ${{ contains(needs.*.result, 'failure') }}
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{
              "text": "❌ MagentaLine release failed!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Release Failed*\nCheck the workflow run for details."
                  }
                }
              ]
            }'
```

## Version Bumping

```yaml
# .github/workflows/version-bump.yml
name: Version Bump

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.PAT }}

      - name: Bump version
        id: bump
        run: |
          CURRENT=$(grep "version:" pubspec.yaml | head -1 | awk '{print $2}' | cut -d'+' -f1)
          IFS='.' read -r major minor patch <<< "$CURRENT"

          case "${{ inputs.bump_type }}" in
            major) major=$((major + 1)); minor=0; patch=0 ;;
            minor) minor=$((minor + 1)); patch=0 ;;
            patch) patch=$((patch + 1)) ;;
          esac

          NEW_VERSION="$major.$minor.$patch"
          BUILD=$(($(grep "version:" pubspec.yaml | head -1 | cut -d'+' -f2) + 1))

          sed -i "s/version: .*/version: $NEW_VERSION+$BUILD/" pubspec.yaml

          echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
          echo "build_number=$BUILD" >> $GITHUB_OUTPUT

      - name: Commit and tag
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add pubspec.yaml
          git commit -m "chore: bump version to ${{ steps.bump.outputs.new_version }}"
          git tag "v${{ steps.bump.outputs.new_version }}"
          git push && git push --tags
```
