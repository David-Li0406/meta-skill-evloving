---
name: game-testing
description: Browser-based game control and E2E testing using Playwright MCP
category: validation
depends-on: [browser-testing]
---

# Game Testing Skill

> "Game controls must be tested with continuous input patterns, not single keypresses."

## When to Use This Skill

Use for **every game feature validation** to test:
- Character movement (WASD, arrow keys)
- Mouse aiming and interaction
- Combat mechanics and combos
- Special actions (jump, crouch, interact)
- UI navigation (menus, inventory, map)

## Quick Start

```javascript
// Continuous forward movement
await page.keyboard.down('KeyW');
await page.waitForTimeout(1000);
await page.keyboard.up('KeyW');

// Diagonal movement with sprint
await page.keyboard.down('KeyW');
await page.keyboard.down('KeyD');
await page.keyboard.down('ShiftLeft');
await page.waitForTimeout(2000);
await page.keyboard.up('ShiftLeft');
await page.keyboard.up('KeyD');
await page.keyboard.up('KeyW');

// Mouse aim and click
await page.mouse.move(x, y);
await page.waitForTimeout(100);
await page.mouse.click(x, y, { button: 'left' });
```

---

## Continuous Movement Patterns

### Basic WASD Movement

**Critical Pattern**: Use `keyboard.down()` + `waitForTimeout()` + `keyboard.up()` for continuous movement. Single `press()` calls only simulate a quick tap.

```javascript
// Forward movement
async function moveForward(page, durationMs) {
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyW');
}

// Backward movement
async function moveBackward(page, durationMs) {
  await page.keyboard.down('KeyS');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyS');
}

// Left strafe
async function strafeLeft(page, durationMs) {
  await page.keyboard.down('KeyA');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyA');
}

// Right strafe
async function strafeRight(page, durationMs) {
  await page.keyboard.down('KeyD');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyD');
}
```

### Diagonal Movement

```javascript
// Forward-left diagonal
async function moveDiagonalFL(page, durationMs) {
  await page.keyboard.down('KeyW');
  await page.keyboard.down('KeyA');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyA');
  await page.keyboard.up('KeyW');
}

// Forward-right diagonal
async function moveDiagonalFR(page, durationMs) {
  await page.keyboard.down('KeyW');
  await page.keyboard.down('KeyD');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyD');
  await page.keyboard.up('KeyW');
}

// Universal diagonal movement helper
async function moveDiagonal(page, dir1, dir2, durationMs) {
  await page.keyboard.down(dir1);
  await page.keyboard.down(dir2);
  await page.waitForTimeout(durationMs);
  await page.keyboard.up(dir2);
  await page.keyboard.up(dir1);
}
```

### Sprint/Run Combinations

```javascript
// Sprint forward
async function sprintForward(page, durationMs) {
  await page.keyboard.down('ShiftLeft');
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyW');
  await page.keyboard.up('ShiftLeft');
}

// Sprint diagonal
async function sprintDiagonal(page, direction, durationMs) {
  const dirs = {
    forward: 'KeyW',
    left: 'KeyA',
    right: 'KeyD'
  };

  await page.keyboard.down('ShiftLeft');
  await page.keyboard.down('KeyW');
  if (direction === 'left') await page.keyboard.down(dirs.left);
  if (direction === 'right') await page.keyboard.down(dirs.right);
  await page.waitForTimeout(durationMs);
  if (direction === 'left') await page.keyboard.up(dirs.left);
  if (direction === 'right') await page.keyboard.up(dirs.right);
  await page.keyboard.up('KeyW');
  await page.keyboard.up('ShiftLeft');
}
```

### Crouch Movement

```javascript
// Crouch forward
async function crouchForward(page, durationMs) {
  await page.keyboard.down('ControlLeft');
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyW');
  await page.keyboard.up('ControlLeft');
}

// Crouch in place
async function crouch(page, durationMs) {
  await page.keyboard.down('ControlLeft');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('ControlLeft');
}
```

---

## Mouse Control Patterns

### Aiming

```javascript
// Direct mouse aim (instant)
async function aimAt(page, x, y) {
  await page.mouse.move(x, y);
}

// Smooth mouse aim (simulates human movement)
async function aimSmooth(page, targetX, targetY, steps = 10) {
  const currentPosition = await page.evaluate(() => ({
    x: window.mouseX || window.innerWidth / 2,
    y: window.mouseY || window.innerHeight / 2
  }));

  const dx = (targetX - currentPosition.x) / steps;
  const dy = (targetY - currentPosition.y) / steps;

  for (let i = 0; i < steps; i++) {
    const x = Math.round(currentPosition.x + dx * (i + 1));
    const y = Math.round(currentPosition.y + dy * (i + 1));
    await page.mouse.move(x, y);
    await page.waitForTimeout(16); // ~60fps
  }
}
```

### Clicking

```javascript
// Left click (primary attack)
await page.mouse.click(x, y, { button: 'left' });

// Right click (secondary attack/alt action)
await page.mouse.click(x, y, { button: 'right' });

// Double click
await page.mouse.dblclick(x, y);

// Middle click
await page.mouse.click(x, y, { button: 'middle' });

// Hold and release (charged attack)
async function chargedAttack(page, x, y, chargeTime) {
  await page.mouse.move(x, y);
  await page.mouse.down({ button: 'left' });
  await page.waitForTimeout(chargeTime);
  await page.mouse.up({ button: 'left' });
}
```

### Dragging

```javascript
// Mouse drag (for inventory, sliders, etc.)
async function drag(page, startX, startY, endX, endY) {
  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(endX, endY);
  await page.mouse.up();
}
```

---

## Special Keys

### Jump

```javascript
// Single jump
await page.keyboard.press('Space');

// Hold jump (higher jump in some games)
async function highJump(page) {
  await page.keyboard.down('Space');
  await page.waitForTimeout(200);
  await page.keyboard.up('Space');
}
```

### Interact

```javascript
// E key interact
await page.keyboard.press('KeyE');

// F key interact (alternate)
await page.keyboard.press('KeyF');

// Hold interact
async function holdInteract(page, durationMs) {
  await page.keyboard.down('KeyE');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyE');
}
```

### Menu/UI Keys

```javascript
// Escape (menu/back)
await page.keyboard.press('Escape');

// Tab (scoreboard/inventory)
await page.keyboard.press('Tab');

// M (map)
await page.keyboard.press('KeyM');

// I (inventory)
await page.keyboard.press('KeyI');

// Enter (confirm)
await page.keyboard.press('Enter');
```

---

## Combo Sequences

### Melee Combo Pattern

```javascript
// Execute a timed combo sequence
async function executeCombo(page, sequence) {
  // sequence: [{ key: 'KeyJ', hold: 100 }, { key: 'KeyK', hold: 150 }, ...]
  for (const action of sequence) {
    await page.keyboard.down(action.key);
    await page.waitForTimeout(action.hold);
    await page.keyboard.up(action.key);
    await page.waitForTimeout(50); // Combo window between attacks
  }
}

// Three-hit light combo
async function lightCombo(page) {
  await executeCombo(page, [
    { key: 'KeyJ', hold: 100 },
    { key: 'KeyJ', hold: 100 },
    { key: 'KeyJ', hold: 100 }
  ]);
}

// Light, Light, Heavy finisher
async function llhCombo(page) {
  await executeCombo(page, [
    { key: 'KeyJ', hold: 100 },  // Light
    { key: 'KeyJ', hold: 100 },  // Light
    { key: 'KeyK', hold: 200 }   // Heavy finisher
  ]);
}
```

### Spell Cast Sequence

```javascript
// Cast spell with key combination
async function castSpell(page, spellKey, modifier) {
  await page.keyboard.down(modifier);
  await page.keyboard.press(spellKey);
  await page.keyboard.up(modifier);
}

// Example: Ctrl+Q for ability 1
await castSpell(page, 'KeyQ', 'ControlLeft');
```

### Item Use Chain

```javascript
// Use multiple items in sequence
async function useItems(page, itemKeys) {
  for (const key of itemKeys) {
    await page.keyboard.press(key);
    await page.waitForTimeout(500); // Cooldown between uses
  }
}

// Use health potion (1) then mana potion (2)
await useItems(page, ['Digit1', 'Digit2']);
```

---

## Modifier Combinations

### Helper Function

```javascript
// Press multiple modifiers together with a key
async function pressWithModifiers(page, modifiers, key) {
  for (const mod of modifiers) {
    await page.keyboard.down(mod);
  }
  await page.keyboard.press(key);
  for (const mod of [...modifiers].reverse()) {
    await page.keyboard.up(mod);
  }
}
```

### Common Combinations

```javascript
// Sprint jump
await pressWithModifiers(page, ['ShiftLeft'], 'Space');

// Crouch jump
await pressWithModifiers(page, ['ControlLeft'], 'Space');

// Alt-tab (weapon swap)
await pressWithModifiers(page, ['AltLeft'], 'KeyQ');

// Ctrl+E (crouch interact)
await pressWithModifiers(page, ['ControlLeft'], 'KeyE');

// Quick save (F5 by default)
await page.keyboard.press('F5');

// Quick load (F9 by default)
await page.keyboard.press('F9');
```

---

## Arrow Key Movement

Some games use arrow keys instead of WASD:

```javascript
// Arrow key movement helper
async function moveArrow(page, direction, durationMs) {
  const keyMap = {
    up: 'ArrowUp',
    down: 'ArrowDown',
    left: 'ArrowLeft',
    right: 'ArrowRight'
  };

  await page.keyboard.down(keyMap[direction]);
  await page.waitForTimeout(durationMs);
  await page.keyboard.up(keyMap[direction]);
}

// Circle pattern with arrow keys
async function circlePattern(page) {
  await moveArrow(page, 'up', 500);
  await moveArrow(page, 'right', 500);
  await moveArrow(page, 'down', 500);
  await moveArrow(page, 'left', 500);
}
```

---

## Number Keys

### Number Row

```javascript
// Switch weapons/items 1-9
await page.keyboard.press('Digit1');  // 1
await page.keyboard.press('Digit2');  // 2
await page.keyboard.press('Digit3');  // 3
// ... up to Digit9
```

### Numpad

```javascript
// Numpad keys (some games use these)
await page.keyboard.press('Numpad1');
await page.keyboard.press('Numpad2');
await page.keyboard.press('NumpadAdd');    // +
await page.keyboard.press('NumpadSubtract'); // -
```

---

## Complete E2E Test Example

```javascript
test('character can move, jump, and attack', async ({ page }) => {
  // Setup
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas'); // Focus game

  // Get initial position
  const initialPos = await page.evaluate(() =>
    (window as any).playerPosition || { x: 0, y: 0, z: 0 }
  );

  // Test forward movement
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(1000);
  await page.keyboard.up('KeyW');

  const afterMove = await page.evaluate(() =>
    (window as any).playerPosition || { x: 0, y: 0, z: 0 }
  );
  expect(afterMove.z).not.toBe(initialPos.z);

  // Test jump
  const beforeJump = await page.evaluate(() =>
    (window as any).playerPosition?.y || 0
  );
  await page.keyboard.press('Space');
  await page.waitForTimeout(500);

  const afterJump = await page.evaluate(() =>
    (window as any).playerPosition?.y || 0
  );
  expect(afterJump).toBeGreaterThan(beforeJump);

  // Test attack
  await page.mouse.click(400, 300, { button: 'left' });

  // Take screenshot for evidence
  await page.screenshot({ path: 'screenshots/gameplay-test.png' });
});
```

---

## Testing Checklist

For each game feature:

- [ ] Movement works in all 4 directions (WASD)
- [ ] Diagonal movement works correctly
- [ ] Sprint affects movement speed
- [ ] Jump/Space key triggers correct action
- [ ] Mouse aiming responds correctly
- [ ] Left click performs primary action
- [ ] Right click performs secondary action (if applicable)
- [ ] Interact key (E/F) works with objects
- [ ] Menu keys (Escape, Tab, I, M) open correct UI
- [ ] Combo sequences execute in order
- [ ] No input lag or delayed response
- [ ] Multiple keys can be pressed simultaneously

---

## Common Issues

### Issue: Keys don't respond

**Solution**: Ensure canvas/game has focus:
```javascript
await page.click('canvas');
// or
await page.focus('#game-container');
```

### Issue: Movement is jerky

**Solution**: Use `keyboard.down()` + `waitForTimeout()` + `keyboard.up()` instead of `press()`

### Issue: Clicks don't register

**Solution**: Add small delay before click:
```javascript
await page.mouse.move(x, y);
await page.waitForTimeout(50); // Stabilize
await page.mouse.click(x, y);
```

### Issue: Combos don't execute

**Solution**: Add combo window delay between inputs:
```javascript
await page.keyboard.up('KeyJ');
await page.waitForTimeout(50); // Combo window
await page.keyboard.down('KeyK');
```

---

## E2E Gameplay Testing Patterns

> "E2E tests validate the complete gameplay experience from player perspective."

### When to Use E2E Gameplay Tests

Use for:
- Validating complete gameplay loops
- Testing multi-step interactions
- Verifying game state persistence
- Checking win/loss conditions
- Validating scoring and progression

### Complete Gameplay Loop Test

```javascript
test('complete gameplay loop - character can move, shoot, and score', async ({ page }) => {
  // Setup
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas');

  // 1. Navigate through character selection
  await page.waitForSelector('[data-testid="character-selection"]');
  await page.click('[aria-label="next-character"]');
  await page.click('[aria-label="next-character"]');
  await page.fill('input[name="playerName"]', 'TestPlayer');
  await page.click('[data-testid="select-button"]');

  // 2. Wait for game to load
  await page.waitForSelector('[data-testid="hud"]', { timeout: 10000 });

  // 3. Test movement
  const initialPos = await page.evaluate(() => ({
    x: window.playerState?.position.x ?? 0,
    y: window.playerState?.position.y ?? 0,
    z: window.playerState?.position.z ?? 0,
  }));

  await page.keyboard.down('KeyW');
  await page.waitForTimeout(1000);
  await page.keyboard.up('KeyW');

  const afterMove = await page.evaluate(() => ({
    x: window.playerState?.position.x ?? 0,
    y: window.playerState?.position.y ?? 0,
    z: window.playerState?.position.z ?? 0,
  }));

  // Verify position changed
  expect(afterMove.z).not.toBe(initialPos.z);

  // 4. Test shooting
  const beforeInk = await page.evaluate(() => window.playerState?.ink ?? 100);

  // Aim and shoot
  await page.mouse.move(400, 300);
  await page.waitForTimeout(50);
  await page.mouse.down({ button: 'left' });
  await page.waitForTimeout(500);
  await page.mouse.up({ button: 'left' });

  const afterInk = await page.evaluate(() => window.playerState?.ink ?? 100);

  // Verify ink decreased
  expect(afterInk).toBeLessThan(beforeInk);

  // 5. Check HUD updates
  const inkDisplay = await page.textContent('[data-testid="ink-tank"]');
  expect(inkDisplay).toBeTruthy();

  // 6. Screenshot for evidence
  await page.screenshot({ path: 'screenshots/gameplay-loop.png' });
});
```

### Paint Coverage Validation

```javascript
test('painting increases team score coverage', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas');

  // Skip to gameplay (assuming character selection handled)
  await page.waitForTimeout(2000);

  // Get initial paint coverage
  const initialCoverage = await page.evaluate(() => {
    return window.gameState?.paintCoverage ?? { orange: 0, blue: 0 };
  });

  // Paint some ground
  await page.keyboard.down('KeyW');
  await page.mouse.down({ button: 'left' });
  await page.waitForTimeout(2000);
  await page.mouse.up({ button: 'left' });
  await page.keyboard.up('KeyW');

  // Check coverage increased
  const finalCoverage = await page.evaluate(() => {
    return window.gameState?.paintCoverage ?? { orange: 0, blue: 0 };
  });

  expect(finalCoverage.orange + finalCoverage.blue)
    .toBeGreaterThan(initialCoverage.orange + initialCoverage.blue);

  await page.screenshot({ path: 'screenshots/paint-coverage.png' });
});
```

### Match Completion Test

```javascript
test('match completes with winner determination', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Get initial timer
  const initialTime = await page.textContent('[data-testid="match-timer"]');

  // Wait for match to complete (in test mode, this may be accelerated)
  await page.waitForSelector('[data-testid="match-end"]', { timeout: 200000 });

  // Check winner is displayed
  const winnerText = await page.textContent('[data-testid="winner-display"]');
  expect(winnerText).toBeTruthy();
  expect(winnerText).toMatch(/Orange|Blue/);

  // Check rematch button available
  const rematchButton = await page.isVisible('[data-testid="rematch-button"]');
  expect(rematchButton).toBe(true);

  await page.screenshot({ path: 'screenshots/match-complete.png' });
});
```

### Mobile Touch Controls Test

```javascript
test('mobile touch controls work correctly', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 812 });

  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Touch joystick should be visible on mobile
  const joystick = await page.isVisible('[data-testid="virtual-joystick"]');
  expect(joystick).toBe(true);

  // Touch action buttons should be visible
  const jumpBtn = await page.isVisible('[data-testid="jump-button"]');
  const shootBtn = await page.isVisible('[data-testid="shoot-button"]');
  expect(jumpBtn).toBe(true);
  expect(shootBtn).toBe(true);

  // Simulate touch interaction
  const canvas = await page.locator('canvas').boundingBox();
  if (canvas) {
    // Touch left side for movement
    await page.touchStart({
      points: [{ x: canvas.x + 50, y: canvas.y + canvas.height / 2 }],
    });
    await page.waitForTimeout(500);
    await page.touchEnd();

    // Check player moved
    const afterTouch = await page.evaluate(() => ({
      x: window.playerState?.position.x ?? 0,
      z: window.playerState?.position.z ?? 0,
    }));

    // Touch shoot button
    await page.tap('[data-testid="shoot-button"]');
    await page.waitForTimeout(100);

    await page.screenshot({ path: 'screenshots/mobile-controls.png' });
  }
});
```

### Performance During Gameplay

```javascript
test('maintains 60 FPS during gameplay', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Collect FPS data
  const fpsData = await page.evaluate(() => {
    return new Promise((resolve) => {
      const fps = [];
      let lastTime = performance.now();
      let frames = 0;

      function measureFPS() {
        frames++;
        const now = performance.now();
        if (now >= lastTime + 1000) {
          fps.push(frames);
          frames = 0;
          lastTime = now;
          if (fps.length >= 10) {
            resolve(fps);
            return;
          }
        }
        requestAnimationFrame(measureFPS);
      }

      measureFPS();
    });
  });

  // Calculate average FPS
  const avgFPS = fpsData.reduce((a, b) => a + b, 0) / fpsData.length;

  // Should maintain at least 55 FPS (allowing some variance)
  expect(avgFPS).toBeGreaterThanOrEqual(55);

  console.log(`Average FPS: ${avgFPS.toFixed(2)}`);
});
```

### Memory Leak Detection

```javascript
test('no memory leaks during extended gameplay', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Get initial memory
  const initialMemory = await page.evaluate(() => {
    return (performance as any).memory?.usedJSHeapSize ?? 0;
  });

  // Simulate 5 minutes of gameplay
  for (let i = 0; i < 60; i++) {
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(500);
    await page.keyboard.up('KeyW');

    await page.mouse.down({ button: 'left' });
    await page.waitForTimeout(500);
    await page.mouse.up({ button: 'left' });
  }

  // Force garbage collection if available
  await page.evaluate(() => {
    if ((window as any).gc) {
      (window as any).gc();
    }
  });

  // Get final memory
  const finalMemory = await page.evaluate(() => {
    return (performance as any).memory?.usedJSHeapSize ?? 0;
  });

  // Memory should not grow more than 50MB
  const memoryGrowth = (finalMemory - initialMemory) / 1024 / 1024;
  expect(memoryGrowth).toBeLessThan(50);

  console.log(`Memory growth: ${memoryGrowth.toFixed(2)} MB`);
});
```

### HUD Integration Test

```javascript
test('HUD updates correctly during gameplay', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas');

  // Wait for HUD to be visible
  await page.waitForSelector('[data-testid="hud"]');

  // Check initial HUD state
  const initialInk = await page.textContent('[data-testid="ink-tank"]');
  const initialScore = await page.textContent('[data-testid="team-score"]');

  // Shoot to deplete ink
  await page.mouse.down({ button: 'left' });
  await page.waitForTimeout(1000);
  await page.mouse.up({ button: 'left' });

  // Check ink tank updated
  const afterShootInk = await page.textContent('[data-testid="ink-tank"]');
  expect(afterShootInk).not.toBe(initialInk);

  // Wait for ink regeneration
  await page.waitForTimeout(3000);
  const regeneratedInk = await page.textContent('[data-testid="ink-tank"]');

  // Ink should have regenerated
  expect(regeneratedInk).not.toBe(afterShootInk);

  await page.screenshot({ path: 'screenshots/hud-updates.png' });
});
```

## E2E Test Checklist

For complete gameplay validation:

- [ ] Character selection flow works
- [ ] Player can move in all directions
- [ ] Shooting depletes ink tank
- [ ] Ink regenerates over time
- [ ] Paint decals appear on surfaces
- [ ] Team scores update correctly
- [ ] Match timer counts down
- [ ] Match end triggers correctly
- [ ] Winner is determined properly
- [ ] Rematch button appears
- [ ] Mobile touch controls work
- [ ] Performance stays above 55 FPS
- [ ] No memory leaks during extended play
- [ ] No console errors during gameplay

## Reference

- [Playwright Keyboard API](https://playwright.dev/docs/api/class-keyboard)
- [Playwright Mouse API](https://playwright.dev/docs/api/class-mouse)
- [Playwright Touch API](https://playwright.dev/docs/touch)
- [`agents/qa/skills/browser-testing.md`](browser-testing.md) — Basic browser testing
- [`agents/qa/skills/visual-testing.md`](visual-testing.md) — Visual validation
