---
name: multiplayer-testing
description: Multiplayer testing with multi-client browser contexts for server-authoritative validation
category: validation
depends-on: [browser-testing]
---

# Multiplayer Testing Skill

> "Server-authoritative code must be validated with actual server connections."

## When to Use This Skill

Use for **EVERY task** marked with `serverAuthoritative: true` or `multiplayerTested: true`.

## Critical Architecture Principle

**Single-browser testing is INSUFFICIENT for multiplayer validation.**

You must verify:
- Server receives input from clients
- Server validates and processes input
- Server broadcasts state to all clients
- All clients see synchronized state

## Quick Start: Multi-Client Test Pattern

```typescript
// tests/e2e/multiplayer-suite.spec.ts
import { test, expect } from '@playwright/test';

test('server-authoritative movement sync', async ({ browser }) => {
  // Create 2 separate browser contexts (simulate 2 players)
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();

  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  // Both connect to same server room
  await page1.goto('http://localhost:3000?room=test_room');
  await page2.goto('http://localhost:3000?room=test_room');

  // Wait for connection
  await page1.waitForFunction(() => window.isConnected?.() === true);
  await page2.waitForFunction(() => window.isConnected?.() === true);

  // Player 1 moves (WASD input)
  await page1.keyboard.press('KeyW');
  await page1.waitForTimeout(500);

  // Player 2 should see Player 1's new position
  const player1PosOnPage2 = await page2.evaluate(() => {
    return window.getRemotePlayerPosition?.('player1');
  });

  expect(player1PosOnPage2.z).toBeLessThan(0); // Moved forward
});
```

## Test Categories

| Category | What to Validate |
|----------|------------------|
| Connection | Multiple clients connect to same room |
| State Sync | All clients see same server state |
| Movement | Client input → Server validate → All clients see result |
| Shooting | Client fires → Server validates → All clients see paint |
| Spawning | Server assigns spawn → All clients see same location |
| Tamper Detection | Server rejects invalid inputs |
| Latency | Client prediction + server reconciliation |

## Server Validation Checklist

Before writing multiplayer tests, verify server is running:

```bash
# Terminal 1: Start server
npm run server
# Expected output: "listening on wss://localhost:2567"

# Terminal 2: Start client
npm run dev
# Expected output: "Local: http://localhost:3000"
```

**If server is NOT running, FAIL the validation immediately.**

## Progressive Guide

### Level 1: Multi-Client Connection

```typescript
test('two clients connect to same room', async ({ browser }) => {
  const page1 = await browser.newPage();
  const page2 = await browser.newPage();

  // Both connect
  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  // Verify connection on both
  const connected1 = await page1.evaluate(() => window.gameState?.connected);
  const connected2 = await page2.evaluate(() => window.gameState?.connected);

  expect(connected1).toBe(true);
  expect(connected2).toBe(true);

  // Verify same room
  const room1 = await page1.evaluate(() => window.gameState?.roomId);
  const room2 = await page2.evaluate(() => window.gameState?.roomId);
  expect(room1).toBe(room2);
});
```

### Level 2: State Synchronization

```typescript
test('movement syncs between clients', async ({ browser }) => {
  const page1 = await browser.newPage();
  const page2 = await browser.newPage();

  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  // Wait for both players to spawn
  await page1.waitForFunction(() => window.gameState?.players?.size >= 2);
  await page2.waitForFunction(() => window.gameState?.players?.size >= 2);

  // Get initial positions
  const initialPos = await page1.evaluate(() => {
    const localId = window.gameState?.localPlayerId;
    return window.gameState?.players?.get(localId)?.position;
  });

  // Player 1 moves forward
  await page1.click('canvas');
  await page1.keyboard.down('KeyW');
  await page1.waitForTimeout(1000); // Move for 1 second
  await page1.keyboard.up('KeyW');

  // Wait for server sync
  await page1.waitForTimeout(200);

  // Verify Player 1 moved locally
  const localPos = await page1.evaluate(() => {
    const localId = window.gameState?.localPlayerId;
    return window.gameState?.players?.get(localId)?.position;
  });

  // Verify Player 2 sees Player 1's new position
  const remotePos = await page2.evaluate(() => {
    const players = window.gameState?.players;
    for (const [id, player] of players?.entries()) {
      if (id !== window.gameState?.localPlayerId) {
        return player.position;
      }
    }
  });

  expect(localPos.z).not.toBe(initialPos.z); // Local player moved
  expect(Math.abs(remotePos.z - localPos.z)).toBeLessThan(1); // Sync within tolerance
});
```

### Level 3: Server Authority Validation

```typescript
test('server validates input (anti-cheat)', async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  // Expose game internals for testing
  const networkManager = await page.evaluate(() => window.networkManager);

  // Attempt to send impossible input (speed hack)
  // This should be REJECTED by server
  await page.evaluate(() => {
    window.networkManager?.send({
      type: 'player_input',
      input: {
        forward: true,
        speed: 999999, // Impossible speed - server should reject
      }
    });
  });

  // Verify position didn't teleport
  const posBefore = await page.evaluate(() => window.gameState?.localPlayer?.position);
  await page.waitForTimeout(500);
  const posAfter = await page.evaluate(() => window.gameState?.localPlayer?.position);

  // Position should NOT have changed dramatically
  expect(Math.abs(posAfter.x - posBefore.x)).toBeLessThan(5);
});
```

### Level 4: Paint Shooting Validation

```typescript
test('shooting syncs between clients', async ({ browser }) => {
  const page1 = await browser.newPage();
  const page2 = await browser.newPage();

  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  await page1.waitForFunction(() => window.gameState?.players?.size >= 2);
  await page2.waitForFunction(() => window.gameState?.players?.size >= 2);

  // Player 1 shoots
  await page1.click('canvas');
  await page1.mouse.click(400, 300); // Center of screen

  await page1.waitForTimeout(100);

  // Both clients should see the paint splat
  const paintCount1 = await page1.evaluate(() => window.gameState?.paintSplats?.size || 0);
  const paintCount2 = await page2.evaluate(() => window.gameState?.paintSplats?.size || 0);

  expect(paintCount1).toBeGreaterThan(0);
  expect(paintCount1).toBe(paintCount2); // Same count on both clients
});
```

### Level 5: Network Latency Simulation

```typescript
test('client prediction works with latency', async ({ browser, context }) => {
  // Simulate high latency
  await context.route('**/*', async (route) => {
    await new Promise(resolve => setTimeout(resolve, 200)); // 200ms delay
    route.continue();
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  // Client should still feel responsive (prediction)
  // Even with 200ms latency, input should feel immediate
  await page.click('canvas');

  const posBefore = await page.evaluate(() => window.gameState?.localPlayer?.position);
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(100);
  await page.keyboard.up('KeyW');

  const predictedPos = await page.evaluate(() => window.gameState?.localPlayer?.position);

  // Local prediction should have applied
  expect(predictedPos.z).toBeLessThan(posBefore.z);
});
```

## Server-Side Integration Tests

Create server tests alongside client tests:

```typescript
// server/tests/integration/room.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { GameRoom } from '../rooms/GameRoom';
import { Client, Room } from 'colyseus';

describe('GameRoom Server Authority', () => {
  let room: GameRoom;

  beforeEach(() => {
    room = new GameRoom();
    room.onCreate({});
  });

  it('validates player input speed', () => {
    const mockClient = { sessionId: 'test-player' } as Client;
    room.onJoin(mockClient);

    const player = room.state.players.get('test-player');

    // Send input with impossible speed
    room.onMessage(mockClient, {
      type: 'player_input',
      input: { speed: 9999 }
    });

    // Position should NOT have changed dramatically
    expect(player.x).toBeCloseTo(0, 0); // Still near spawn
  });

  it('validates shooting cooldown', () => {
    const mockClient = { sessionId: 'test-player' } as Client;
    room.onJoin(mockClient);

    const player = room.state.players.get('test-player');
    player.lastShotTime = Date.now();

    // Try to shoot again immediately (should be rejected)
    room.onMessage(mockClient, {
      type: 'shoot',
      aim: { x: 1, y: 0, z: 0 }
    });

    // No projectile should have been created
    expect(room.projectiles?.length || 0).toBe(0);
  });
});
```

## Tamper Detection Tests

Verify server rejects client manipulation attempts:

```typescript
test('server rejects position hacks', async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  const posBefore = await page.evaluate(() => {
    return window.gameState?.localPlayer?.position;
  });

  // Try to directly manipulate local position (client-side hack simulation)
  await page.evaluate(() => {
    const localId = window.gameState?.localPlayerId;
    window.gameState.players.get(localId).position = { x: 9999, y: 0, z: 9999 };
  });

  // Wait for server correction
  await page.waitForTimeout(500);

  // Server should have overridden the hacked position
  const posAfter = await page.evaluate(() => {
    return window.gameState?.localPlayer?.position;
  });

  expect(posAfter.x).not.toBe(9999); // Server corrected it
  expect(Math.abs(posAfter.x - posBefore.x)).toBeLessThan(10); // Still near original
});
```

## Testing Checklist

For each multiplayer validation:

- [ ] Server running (`npm run server`)
- [ ] Dev server running (`npm run dev`)
- [ ] 2+ browser contexts created
- [ ] All clients connect to same room
- [ ] Client input sends to server (not local state)
- [ ] Server validates input (check logs)
- [ ] Server broadcasts state updates
- [ ] All clients see synchronized state
- [ ] Tamper attempts are rejected
- [ ] No console errors on any client
- [ ] No server errors in terminal

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Test with 1 browser context | Test with 2+ contexts (multi-client) |
| Don't check server logs | Verify server receives and processes input |
| Assume state syncs | Assert state values match across clients |
| Test local state only | Test REMOTE player state from other client |
| Ignore server validation | Test that invalid inputs are rejected |

## Anti-Patterns

❌ **DON'T:**

- Test multiplayer features with only 1 browser
- Skip checking server logs
- Assume state sync without assertions
- Test only local player state
- Skip tamper detection tests

✅ **DO:**

- Always test with 2+ browser contexts
- Monitor server logs for input processing
- Assert state synchronization explicitly
- Test remote player state from other client's perspective
- Include tamper detection tests

## Validation Failure Criteria

**FAIL the validation if:**

- Server is not running
- Clients cannot connect to same room
- State does not sync between clients within 500ms
- Server logs show no input processing
- Invalid inputs are not rejected
- Console errors on any client
- Server crashes or throws errors

## Reference

- [agents/developer/skills/backend-multiplayer.md](../developer/skills/backend-multiplayer.md) — Server-authoritative architecture
- [agents/qa/skills/browser-testing.md](browser-testing.md) — Single-client browser testing
- [agents/qa/skills/validation-workflow.md](validation-workflow.md) — Full validation workflow
- [Colyseus Testing Guide](https://docs.colyseus.io/colyseus/server/testing/) — Server-side testing
