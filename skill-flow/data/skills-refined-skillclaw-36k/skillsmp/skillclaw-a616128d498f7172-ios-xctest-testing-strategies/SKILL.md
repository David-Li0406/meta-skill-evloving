---
name: ios-xctest-testing-strategies
description: Use this skill when designing and implementing testing strategies for iOS applications using XCTest and XCUITest, focusing on test type selection, mock design, and ensuring reliable test execution.
---

# Skill body

## Overview

This skill provides expert guidance on testing strategies for iOS applications using XCTest and XCUITest. It covers test type selection, mock vs. stub vs. spy decisions, async testing strategies, and best practices for maintaining reliable and deterministic tests.

## Decision Trees

### Test Type Selection

```
What are you testing?
├─ Pure business logic (no I/O, no UI)
│  └─ Unit test
│     Fast, isolated, many of these
│
├─ Component interactions (services, repositories)
│  └─ Integration test
│     Test real interactions, fewer than unit
│
├─ User-visible behavior
│  └─ Does it require visual verification?
│     ├─ YES → Snapshot test or manual QA
│     └─ NO → UI test (XCUITest)
│        Slowest, fewest of these
│
└─ Performance characteristics
   └─ Performance test with measure {}
```

### Mock vs Stub vs Spy

```
What do you need from the test double?
├─ Just return canned data
│  └─ Stub
│     Simplest, no verification
│
├─ Verify interactions (was method called?)
│  └─ Spy
│     Records calls, verifiable
│
└─ Both return data AND verify calls
   └─ Mock (stub + spy)
      Most flexible, most complex
```

### Async Test Strategy

```
Is the async operation...
├─ Returning a value (async/await)?
│  └─ Use async test function
│     func testFetch() async throws { }
│
├─ Using completion handlers?
│  └─ Use XCTestExpectation
│     expectation.fulfill() in callback
│
└─ Publishing via Combine?
   └─ Use XCTestExpectation + sink
      Or use async-aware Combine helpers
```

## Best Practices for UI Testing

### Device Matrix (Simulator vs Real Devices)

- Default: simulators for PR gates; real devices for nightly/release validation.
- Keep the matrix small and risk-based:
  - One “small phone”, one “large phone”, and one iPad if the UI supports it.
  - Add OS versions only when you support multiple major releases.

### UI Test Flake Control (Determinism)

- Disable/limit animations in test builds where possible.
- Control time: fixed timezone/locale; avoid relying on wall-clock.
- Control network: stub at the boundary for most UI tests; avoid third-party dependencies.
- Control permissions: set predictable permission states; avoid manual prompts.
- Isolation: reset app state between tests; avoid ordering dependence and shared accounts.

### CI Economics and Debugging Ergonomics

- PR gate: small smoke UI suite + unit/integration; full UI suite on schedule.
- Always collect actionable artifacts:
  - `xcresult` bundles, screenshots, and logs on failure.
- Prefer “fail fast” diagnostics: assert early on navigation/state instead of letting tests time out.

## Do / Avoid

### Do:
- Make UI tests independent and idempotent.
- Use test data builders and dedicated test accounts/tenants.

### Avoid:
- Relying on test ordering or global state.
- UI tests that require real network access for core flows.

### NEVER Do

**NEVER** test implementation details:
```swift
// ❌ Testing internal state
func testLogin() async {
    await sut.login(email: "test@example.com", password: "pass")

    XCTAssertEqual(sut.authService.callCount, 1)  // Impl
}
```