---
name: visual-testing
description: Visual regression testing and image-based validation using Vision MCP and Playwright
category: validation
depends-on: [browser-testing, game-testing]
---

# Visual Testing Skill

> "Visual validation catches bugs that functional tests miss."

## When to Use This Skill

Use for **every game feature validation** to:
- Compare screenshots against baseline images
- Detect game states (menu, playing, game over, win)
- Validate UI elements (HUD, health bars, buttons)
- Verify visual appearance matches design specifications

## Quick Start

```javascript
// Capture screenshot
await page.screenshot({ path: 'screenshots/validation.png' });

// Detect game state using Vision MCP
const gameState = await detectGameState('screenshots/validation.png');

// Compare with baseline
await expect(page).toHaveScreenshot('baseline.png', {
  maxDiffPixelRatio: 0.01
});
```

---

## Game State Detection

### Detecting Game States

Use Vision MCP to analyze screenshots and determine current game state:

```javascript
// Detect game state from screenshot
async function detectGameState(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `Analyze this game screenshot and determine:
    1. Is this a menu screen, gameplay, game over, victory, or loading screen?
    2. What UI elements are visible? (HUD, health bar, minimap, inventory, etc.)
    3. Is a player character visible?
    4. Are there any error messages or alerts?

    Respond in JSON format:
    {
      "state": "menu|playing|gameover|win|loading|error",
      "uiElements": ["hud", "healthBar", "minimap", ...],
      "playerVisible": true|false,
      "details": "description"
    }`
  });

  return JSON.parse(analysis);
}

// Usage
const state = await detectGameState('screenshot.png');
console.log(state.state); // "playing"
console.log(state.uiElements); // ["hud", "healthBar", "minimap"]
```

### State-Specific Validation

```javascript
// Menu state validation
async function validateMenuState(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `This should be a main menu screen. Check for:
    1. Game title or logo visible
    2. Menu buttons (Start, Settings, Quit, etc.)
    3. No gameplay elements visible

    Return { "valid": true|false, "issues": ["list of issues"] }`
  });

  return JSON.parse(analysis);
}

// Gameplay state validation
async function validateGameplayState(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `This should be active gameplay. Check for:
    1. Player character is visible
    2. HUD elements present (health, ammo, minimap if applicable)
    3. Game world is rendered (not a menu)

    Return { "valid": true|false, "issues": ["list of issues"] }`
  });

  return JSON.parse(analysis);
}

// Game over state validation
async function validateGameOverState(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `This should be a game over screen. Check for:
    1. "Game Over" or similar text visible
    2. Score summary visible
    3. Restart/continue button visible

    Return { "valid": true|false, "issues": ["list of issues"] }`
  });

  return JSON.parse(analysis);
}
```

---

## Baseline Management

### Creating Baselines

```javascript
// Capture baseline screenshots for each game state
async function createBaselines(page, taskId) {
  const baselineDir = `tests/baselines/${taskId}`;

  // Menu baseline
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: `${baselineDir}/menu.png` });

  // Gameplay baseline
  await page.click('canvas');
  await page.keyboard.press('Enter'); // Start game
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `${baselineDir}/playing.png` });

  // Game over baseline (trigger game over)
  await page.keyboard.press('KeyK'); // Suicide command if available
  await page.waitForTimeout(2000);
  await page.screenshot({ path: `${baselineDir}/gameover.png` });
}
```

### Comparing Against Baselines

```javascript
// Pixel-perfect comparison with Playwright
async function compareWithBaseline(page, baselinePath, options = {}) {
  const screenshot = await page.screenshot();

  // Use Playwright's built-in comparison
  const comparison = await compareImages(screenshot, baselinePath, {
    maxDiffPixelRatio: options.threshold || 0.01,
    maxDiffPixels: options.maxPixels || 1000
  });

  return {
    matches: comparison.diffPixels < (options.maxPixels || 1000),
    diffPixels: comparison.diffPixels,
    diffRatio: comparison.diffPixelRatio
  };
}

// Semantic comparison with Vision MCP
async function compareSemantic(currentPath, baselinePath) {
  const comparison = await visionAnalyze([baselinePath, currentPath], {
    prompt: `Compare these two game screenshots.
    Image 1 is the baseline (expected).
    Image 2 is the current (actual).

    Determine:
    1. Are they showing the same game state?
    2. What are the visual differences?
    3. Are the differences acceptable (animation, dynamic content) or bugs?

    Return { "sameState": true|false, "differences": ["list"], "acceptable": true|false }`
  });

  return JSON.parse(comparison);
}
```

---

## UI Element Validation

### HUD Detection

```javascript
// Validate HUD elements are present
async function validateHUD(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `Check if this gameplay screenshot has the required HUD elements:
    1. Health bar - is it visible? What percentage is it showing?
    2. Score/counter - is it visible?
    3. Minimap (if applicable) - is it visible?
    4. Ammo count (if applicable) - is it visible?

    Return {
      "healthBar": { "visible": true|false, "value": "percentage" },
      "score": { "visible": true|false, "value": "number" },
      "minimap": { "visible": true|false },
      "ammo": { "visible": true|false, "value": "count" }
    }`
  });

  return JSON.parse(analysis);
}
```

### Button Detection

```javascript
// Validate menu buttons are present and visible
async function validateMenuButtons(screenshotPath, expectedButtons) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `Check if this menu screenshot has the following buttons:
    ${expectedButtons.join(', ')}

    For each button, return:
    - "visible": true|false
    - "enabled": true|false (can you tell if it's grayed out?)
    - "position": "top|middle|bottom" (approximate)

    Return {
      "buttons": {
        "Play": { "visible": true|false, "enabled": true|false, "position": "..." },
        "Settings": { ... },
        ...
      }
    }`
  });

  return JSON.parse(analysis);
}
```

### Character Detection

```javascript
// Validate player character is visible and correct
async function validatePlayerCharacter(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `In this gameplay screenshot:
    1. Is a player character visible?
    2. What is the character doing? (idle, running, jumping, attacking)
    3. Is the character facing the expected direction?
    4. Are there any visual glitches with the character?

    Return {
      "visible": true|false,
      "action": "idle|running|jumping|attacking|...",
      "facing": "left|right|up|down",
      "issues": ["list of visual problems if any"]
    }`
  });

  return JSON.parse(analysis);
}
```

---

## Visual Regression Testing

### Full Workflow

```javascript
// Complete visual regression test
async function runVisualRegression(page, taskId) {
  const baselineDir = `tests/baselines/${taskId}`;
  const currentDir = `screenshots/${taskId}`;
  const results = [];

  // Define states to test
  const states = ['menu', 'playing', 'gameover'];

  for (const state of states) {
    const baselinePath = `${baselineDir}/${state}.png`;
    const currentPath = `${currentDir}/${state}.png`;

    // Capture current state
    await navigateToState(page, state);
    await page.screenshot({ path: currentPath });

    // Pixel comparison
    const pixelResult = await compareWithBaseline(page, baselinePath, {
      threshold: 0.01,
      maxPixels: 1000
    });

    // Semantic comparison
    const semanticResult = await compareSemantic(currentPath, baselinePath);

    results.push({
      state,
      pixelMatch: pixelResult.matches,
      diffPixels: pixelResult.diffPixels,
      semanticMatch: semanticResult.sameState,
      differences: semanticResult.differences
    });
  }

  return results;
}
```

### Tolerance Guidelines

| Scenario | Max Diff Ratio | Max Pixels |
|----------|---------------|------------|
| Static UI (menus) | 0.001 | 100 |
| Gameplay (animations) | 0.05 | 5000 |
| Particle effects | 0.10 | 10000 |
| Text content | 0.0001 | 10 |

---

## GDD Compliance Validation

### Validate Against Design Specs

```javascript
// Validate visuals match GDD description
async function validateAgainstGDD(screenshotPath, gddDescription) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `According to the Game Design Document:
    "${gddDescription}"

    Does this screenshot match that description?
    Check:
    1. Overall visual style matches
    2. Required elements are present
    3. Colors/theme are correct
    4. Layout matches specification

    Return {
      "matches": true|false,
      "deviations": [
        { "element": "name", "expected": "description", "actual": "what you see" }
      ],
      "overall": "accurate|minor-deviations|major-deviations"
    }`
  });

  return JSON.parse(analysis);
}

// Example usage
const characterGDD = "A knight in silver armor with a blue cape, holding a broadsword";
const result = await validateAgainstGDD('screenshot.png', characterGDD);
```

---

## Screenshot Evidence Management

### Screenshot File Organization

```
screenshots/
├── baselines/
│   ├── feat-001/
│   │   ├── menu.png
│   │   ├── playing.png
│   │   └── gameover.png
├── validation/
│   ├── feat-001-initial.png
│   ├── feat-001-after-fix.png
│   └── feat-001-final.png
└── bugs/
    ├── bug-001-visual-glitch.png
    └── bug-002-hud-missing.png
```

### Screenshot Naming Convention

```
{taskId}-{state}-{timestamp}.{ext}

Examples:
- feat-001-menu-20250121.png
- feat-001-playing-after-jump.png
- feat-001-gameover.png
- bug-001-health-bar-missing.png
```

---

## Vision MCP Integration

### Vision MCP Prompt Patterns

**State Detection:**
```
"Analyze this game screenshot. What state is it in? (menu|playing|gameover|win|loading)
Describe visible UI elements. Is player character visible?"
```

**Comparison:**
```
"Compare Image 1 (baseline) and Image 2 (current).
List visual differences. Are differences acceptable (animations) or bugs?"
```

**Validation:**
```
"Check if this screenshot meets criteria: [criteria]
Return { valid: true|false, issues: [list] }"
```

**GDD Compliance:**
```
"Given this GDD spec: [spec]
Does screenshot match? List deviations with severity (low|medium|high)"
```

---

## Testing Checklist

For each validation:

- [ ] Baseline screenshots captured for all game states
- [ ] Current screenshots compared against baselines
- [ ] Game state detection returns correct state
- [ ] UI elements validated (HUD, buttons, menus)
- [ ] Visual appearance matches design/GDD
- [ ] No visual glitches detected
- [ ] Screenshots saved as evidence
- [ ] Deviations documented with severity

---

## Common Issues

### Issue: False positives in comparison

**Solution**: Use semantic comparison for dynamic content:
```javascript
// Pixel comparison alone fails with animations
// Use Vision MCP for semantic understanding
const semantic = await compareSemantic(current, baseline);
if (semantic.acceptable) {
  // Pass even if pixels differ
}
```

### Issue: State detection inaccurate

**Solution**: Provide more specific prompts:
```javascript
const analysis = await visionAnalyze(screenshot, {
  prompt: `Look SPECIFICALLY for:
  1. "Game Over" text or similar death indicator
  2. Score summary screen
  3. Respawn/continue button

  Only return "gameover" if at least 2 of 3 are present.`
});
```

### Issue: Baselines become stale

**Solution**: Version your baselines:
```javascript
const baselineVersion = await getGameVersion(); // from package.json
const baselinePath = `baselines/v${baselineVersion}/${state}.png`;
```

---

## Complete Example

```javascript
test('visual validation of new character', async ({ page }) => {
  const taskId = 'feat-001';

  // Navigate to game
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(1000);

  // Capture screenshot
  const screenshot = `screenshots/${taskId}-character.png`;
  await page.screenshot({ path: screenshot });

  // Detect game state
  const state = await detectGameState(screenshot);
  expect(state.state).toBe('playing');
  expect(state.playerVisible).toBe(true);

  // Validate character appearance
  const character = await validatePlayerCharacter(screenshot);
  expect(character.visible).toBe(true);
  expect(character.issues).toHaveLength(0);

  // Compare with baseline (semantic)
  const baseline = `tests/baselines/${taskId}/character.png`;
  const comparison = await compareSemantic(screenshot, baseline);
  expect(comparison.sameState).toBe(true);

  // If deviations exist, document them
  if (comparison.differences.length > 0) {
    console.log('Visual deviations:', comparison.differences);
  }
});
```

---

## Reference

- [Playwright Screenshot API](https://playwright.dev/docs/api/class-page#page-screenshot)
- [Playwright Visual Testing](https://playwright.dev/docs/test-snapshots)
- [`agents/qa/skills/browser-testing.md`](browser-testing.md) — Basic browser testing
- [`agents/qa/skills/game-testing.md`](game-testing.md) — Game control patterns
