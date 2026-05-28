---
name: build-ios-project
description: Build the AIQ iOS project to verify compilation succeeds. Use this skill to confirm code changes compile correctly before running tests or committing.
allowed-tools: Bash
---

# Build iOS Project Skill

This skill builds the AIQ iOS project using `xcodebuild` to verify that the project compiles successfully.

## Usage

When this skill is invoked, build the iOS project to verify compilation.

### Build the Project

Run the following command to build the project:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild build -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' 2>&1
```

### Build for Release (Optional)

If specifically requested, build in Release configuration:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild build -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' -configuration Release 2>&1
```

### Clean Build (Optional)

If a clean build is requested or there are stale build artifacts:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild clean build -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' 2>&1
```

## Arguments

When invoked with arguments, parse them to determine the build type:

- **No arguments**: Standard debug build
- **`clean`**: Clean and rebuild
- **`release`**: Build in Release configuration
- **`clean release`**: Clean and rebuild in Release configuration

## Interpreting Results

- **Build Succeeded**: The project compiles without errors
- **Build Failed**: Check the output for:
  - Compilation errors (syntax errors, type mismatches)
  - Linker errors (missing symbols, duplicate symbols)
  - Missing dependencies or frameworks

### Common Build Errors

| Error Type | Cause | Solution |
|------------|-------|----------|
| `Cannot find type 'X'` | Missing import or type not defined | Add import or check spelling |
| `Value of type 'X' has no member 'Y'` | Property/method doesn't exist | Verify API or add the member |
| `Missing argument for parameter` | Function call missing required params | Add missing arguments |
| `Cannot convert value` | Type mismatch | Check types and add conversion |
| `Undefined symbol` | Linker can't find implementation | Ensure file is added to target |

## Troubleshooting

### Simulator Not Found

If the destination simulator isn't available, list available simulators:

```bash
xcrun simctl list devices available
```

Then adjust the `-destination` parameter accordingly.

### Derived Data Issues

If builds fail with strange caching issues, clean derived data:

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/AIQ-*
```

### Missing Files in Target

If files compile locally but fail in build, verify they're added to the Xcode project using the `/xcode-file-manager` skill.

## When to Use This Skill

Use this skill:
- After writing or modifying Swift code to verify it compiles
- Before running tests to catch compilation errors early
- Before committing changes to ensure the project builds
- When debugging build failures reported by CI

## Related Skills

- `/run-ios-test`: Run the test suite after confirming the build succeeds
- `/xcode-file-manager`: Add new Swift files to the Xcode project
