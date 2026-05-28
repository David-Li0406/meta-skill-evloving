---
name: run-e2e-tests
description: Use when user says "執行 e2e 測試" or "run e2e tests" - run end-to-end tests with proper server setup
---

# Run E2E Tests

## Overview

Execute end-to-end tests for Swift StateTree project with automatic server management and encoding mode support.

**Announce at start:** "I'm using the run-e2e-tests skill to execute E2E tests."

## When to Use

- User says "執行 e2e 測試" or "run e2e tests"
- Before submitting PRs (all E2E tests must pass)
- When verifying feature implementation
- When debugging integration issues

## The Process

### Option 1: Use Test Script (Recommended)

**Command:**
```bash
cd Tools/CLI && ./test-e2e-ci.sh
```

**What it does:**
- Automatically handles server startup/shutdown
- Tests all three encoding modes sequentially (`jsonObject`, `opcodeJsonArray`, `messagepack`)
- Shows server logs on failure
- Cleans up after completion

**When to use:** Always prefer this option for automated testing.

### Option 2: Manual Steps

**Step 1: Start DemoServer**
```bash
cd Examples/HummingbirdDemo && swift run DemoServer
```
- Run in background
- Default encoding: JSON
- Wait 2-3 seconds for server startup

**Step 2: Run E2E Tests**
```bash
cd Tools/CLI && npm test
```
- Runs protocol tests + counter/cookie E2E tests
- Tests both `jsonObject` and `opcodeJsonArray` modes
- Tests automatically start servers with correct encoding via environment variables

**Step 3: Verify Results**
- All tests must pass
- If any test fails, investigate and fix before proceeding

### Full Test Suite (Including Game Tests)

**Step 1: Start DemoServer**
```bash
cd Examples/HummingbirdDemo && swift run DemoServer
```

**Step 2: Start GameServer (Optional)**
```bash
cd Examples/GameDemo && swift run GameServer
```
- Runs on same port 8080, different endpoint
- Required for game-specific tests

**Step 3: Run All Tests**
```bash
cd Tools/CLI && npm run test:e2e:with-game
```
- Requires both servers running
- Tests all land types including hero-defense

## Encoding Modes

Tests run in all three encoding modes:

1. **JSON Object** (`jsonObject`)
   - `TRANSPORT_ENCODING=json`
   - JSON messages + JSON object state updates

2. **Opcode JSON Array** (`opcodeJsonArray`)
   - `TRANSPORT_ENCODING=jsonOpcode`
   - JSON messages + opcode JSON array state updates

3. **MessagePack** (`messagepack`)
   - `TRANSPORT_ENCODING=messagepack`
   - MessagePack binary encoding for both messages and state updates

**Note:** When running tests manually, ensure the server is started with the matching encoding mode.

## Test Coverage

- ✅ **Core Features**: Actions, Events, State Sync, Error Handling, Multi-Encoding
- ✅ **Lifecycle**: Tick Handler, OnJoin Handler
- ⚠️ **Partial**: Per-Player State, Broadcast State (single client only)
- ❌ **Not Covered**: Multi-Player Scenarios, OnLeave Handler (requires disconnect testing)

## Connection Info

- **Base URL**: `http://localhost:8080`
- **WebSocket Endpoints**:
  - `cookie`: `ws://localhost:8080/game/cookie` (DemoServer)
  - `counter`: `ws://localhost:8080/game/counter` (DemoServer)
  - `hero-defense`: `ws://localhost:8080/game/hero-defense` (GameServer)
- **Admin Keys**:
  - DemoServer: `demo-admin-key`
  - GameServer: `hero-defense-admin-key`

## Important Notes

- **AI must ensure all tests pass before submitting PRs**
- Each test uses unique land instance ID to ensure clean state
- Tests verify exact state values (not ranges) for precision
- **Proactive Testing**: AI agents are encouraged to create new JSON scenarios in `Tools/CLI/scenarios/` (organized by Land subdirectories) to verify specific features or bug fixes
- Scenarios should use the `assert` step to ensure correctness

## Creating New Test Scenarios

Add JSON file to `Tools/CLI/scenarios/{land-type}/` directory:

```json
{
  "steps": [
    {
      "action": "increment",
      "expectedState": { "count": 1 }
    },
    {
      "assert": {
        "path": "/count",
        "value": 1
      }
    }
  ]
}
```

## Error Handling

If tests fail:
1. Check server logs for errors
2. Verify server is running on correct port
3. Check encoding mode matches test expectations
4. Verify test scenarios are valid JSON
5. Check for port conflicts or resource issues
