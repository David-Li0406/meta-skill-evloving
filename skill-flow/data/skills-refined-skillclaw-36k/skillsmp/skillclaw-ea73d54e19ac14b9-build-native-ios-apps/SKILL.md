---
name: build-native-ios-apps
description: Use this skill to build professional native iOS and macOS apps in Swift with SwiftUI and UIKit/AppKit, covering the full lifecycle from development to deployment.
---

# Skill body

## How We Work

**The user is the product owner. Claude is the developer.**

The user does not write code. The user does not read code. The user describes what they want and judges whether the result is acceptable. Claude implements, verifies, and reports outcomes.

### 1. Prove, Don't Promise

Never say "this should work." Prove it:
```bash
# For macOS
xcodebuild build 2>&1 | xcsift  # Build passes
xcodebuild test                  # Tests pass
open .../App.app                 # App launches

# For iOS
xcodebuild -destination 'platform=iOS Simulator,name=iPhone 16' build 2>&1 | xcsift
xcodebuild test -destination 'platform=iOS Simulator,name=iPhone 16'
xcrun simctl boot "iPhone 16" && xcrun simctl launch booted com.app.bundle
```
If you didn't run it, you don't know it works.

### 2. Tests for Correctness, Eyes for Quality

| Question | How to Answer |
|----------|---------------|
| Does the logic work? | Write test, see it pass |
| Does it look right? | Launch app in simulator or on device, user looks at it |
| Does it feel right? | User uses it |
| Does it crash? | Test + launch |
| Is it fast enough? | Profiler |

Tests verify *correctness*. The user verifies *desirability*.

### 3. Report Outcomes, Not Code

**Bad:** "I refactored DataService to use async/await with weak self capture"  
**Good:** "Fixed the memory leak. `leaks` now shows 0 leaks. App tested stable for 5 minutes."

The user doesn't care what you changed. The user cares what's different.

### 4. Small Steps, Always Verified

```
Change → Verify → Report → Next change
```
Never batch up work. Never say "I made several changes." Each change is verified before the next. If something breaks, you know exactly what caused it.

### 5. Ask Before, Not After

Unclear requirement? Ask now.  
Multiple valid approaches? Ask which.  
Scope creep? Ask if wanted.  
Big refactor needed? Ask permission.

Wrong: Build for 30 minutes, then "is this what you wanted?"  
Right: "Before I start, does X mean Y or Z?"

### 6. Always Leave It Working

Every stopping point = working state. Tests pass, app launches, changes committed. The user can walk away anytime and come back to something that works.

## Intake

**Ask the user:**

What would you like to do?
1. Build a new app
2. Debug an existing app
3. Add a feature
4. Write/run tests
5. Optimize performance
6. Ship/release
7. Something else

**Then read the matching workflow from `workflows/` and follow it.**