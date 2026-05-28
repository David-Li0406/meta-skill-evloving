# flywheel-xcode

iOS/macOS build-test loop with xcodebuildmcp integration.

## philosophy

> "build, test, fix, repeat - let the tools drive"

xcodebuildmcp provides direct Xcode integration. use it for builds, tests, and diagnostics.

## prerequisites

| requirement | check |
|-------------|-------|
| xcodebuildmcp | `claude mcp list \| grep xcodebuild` |
| Xcode project | `ls *.xcodeproj *.xcworkspace` |
| simulator | `xcrun simctl list devices available` |

## MCP tools

| tool | purpose |
|------|---------|
| xcodebuild_build | build project |
| xcodebuild_test | run tests |
| xcodebuild_clean | clean build folder |
| xcodebuild_schemes | list schemes |
| xcodebuild_destinations | list destinations |

## flywheel sequence

### 1. discover

```bash
# list schemes
xcodebuild -list

# available simulators
xcrun simctl list devices available | grep -E "iPhone|iPad"
```

### 2. build

```bash
# via MCP: xcodebuild_build
# fallback CLI:
xcodebuild -scheme "AppScheme" -destination "platform=iOS Simulator,name=iPhone 15 Pro" build
```

### 3. test

```bash
# via MCP: xcodebuild_test
# fallback CLI:
xcodebuild -scheme "AppScheme" -destination "platform=iOS Simulator,name=iPhone 15 Pro" test
```

### 4. diagnose failures

```bash
# parse test output for failures
xcrun xcresulttool get --path ./build/Logs/Test/*.xcresult --format json | jq '.issues'

# get specific test failure
xcrun xcresulttool get --path ./build/Logs/Test/*.xcresult --id $FAILURE_ID
```

### 5. fix & repeat

on test failure:
1. read failure message
2. locate source file
3. consult-light for fix approach
4. apply fix
5. rebuild & retest

## copilot integration

use copilot with opus-4.5 for xcode analysis:

```bash
copilot -p --model claude-opus-4.5 --workspace $(pwd) "
Xcode build analysis.

Build output:
$BUILD_OUTPUT

Test failures:
$TEST_FAILURES

Task: Diagnose and propose fixes.

Output JSON:
{
  \"diagnosis\": \"root cause\",
  \"fixes\": [{\"file\": \"path\", \"change\": \"description\"}],
  \"confidence\": 0-10
}
"
```

## common issues

| symptom | likely cause | fix |
|---------|--------------|-----|
| code signing error | provisioning profile | check team, automatic signing |
| module not found | SPM not resolved | `xcodebuild -resolvePackageDependencies` |
| simulator unavailable | wrong destination | `xcrun simctl list` |
| test timeout | async test issue | check XCTestExpectation usage |

## projects

| project | path | scheme |
|---------|------|--------|
| zo-apple | ~/Developer/zo/zo-apple | Zo |
| sine | ~/Developer/sine/sine-xyz | Sine |
| kumori-apple | ~/Developer/kumori/kumori-apple | Kumori |

## anti-patterns

- **building without MCP**: use xcodebuildmcp when available
- **ignoring warnings**: warnings often predict failures
- **skipping clean**: when stuck, clean first
- **manual simulator**: let tools pick destination
