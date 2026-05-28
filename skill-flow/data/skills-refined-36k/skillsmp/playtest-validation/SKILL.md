---
name: playtest-validation
description: Playwright-based game playtesting and design validation
category: gamedesign
depends-on: []
---

# Playtest Validation

## Overview

This skill provides guidance for using Playwright MCP to playtest games and validate implementation against the GDD.

## When to Use This Skill

Use when:
- PM sends `playtest_request` message
- Participating in retrospective
- Validating implementation vs design
- Testing new features

## ⚠️ MANDATORY: Playtest Requirements

**Every retrospective requires:**

1. **Playwright MCP Usage** - NO manual testing alternatives
2. **Screenshot Evidence** - At minimum: start state, after key actions, end state
3. **Vision MCP Analysis** - Game state detection, GDD compliance validation
4. **playtest_report Message** - MUST be sent to PM (not just retrospective.txt contribution)

**Non-negotiable evidence:**
- [ ] Screenshots saved to `.claude/session/screenshots/playtest-*.png`
- [ ] Vision MCP game state analysis performed
- [ ] At least one continuous movement test (WASD pattern with key down/up)
- [ ] `playtest_report` message sent to PM

**If Playwright MCP unavailable:**
- Report to PM immediately: `question` with "Playwright MCP unavailable - cannot playtest"
- DO NOT attempt manual testing workaround

## Playtest Process

### Step 1: Setup

```powershell
# Start the dev server
npm run dev

# Wait for server ready
Start-Sleep -Seconds 5
```

### Step 2: Launch Game via Playwright

```javascript
// Navigate to game
await page.goto('http://localhost:3000');

// Wait for game to load
await page.waitForLoadState('networkidle');

// Capture initial state
await page.screenshot({ path: 'screenshots/playtest-start.png' });
```

### Step 3: Test Core Mechanics

For each mechanic in GDD:

```javascript
// Test movement
await page.keyboard.press('KeyW');
await page.waitForTimeout(1000);
await page.keyboard.up('KeyW');

// Test interaction
await page.click('[data-testid="interact-button"]');

// Test combat
await page.click('[data-testid="attack-button"]');

// Capture state
await page.screenshot({ path: 'screenshots/mechanic-tested.png' });
```

### Step 4: Validate vs GDD

For each GDD requirement:
- [ ] Implemented? (yes/no/partial)
- [ ] Matches design? (yes/no/deviates)
- [ ] Fun factor? (scale 1-5)
- [ ] Issues found?

### Step 5: Document Findings

Create playtest report:

```json
{
  "taskId": "feat-001",
  "playtestedAt": "2025-01-21T12:00:00Z",
  "gddCompliance": {
    "mechanic-name": {
      "status": "matches|deviates|missing",
      "notes": "Description"
    }
  },
  "deviations": [
    {
      "feature": "Mechanic name",
      "expected": "GDD description",
      "actual": "What happens in game",
      "severity": "low|medium|high",
      "screenshot": "path/to/evidence"
    }
  ],
  "issues": [
    {
      "type": "bug|missing|polish",
      "description": "Issue description",
      "severity": "low|medium|high|critical",
      "steps": "How to reproduce"
    }
  ],
  "screenshots": [
    "path/to/screenshot1.png",
    "path/to/screenshot2.png"
  ],
  "overall": {
    "status": "pass|fail|partial",
    "funFactor": 4,
    "notes": "Overall assessment"
  }
}
```

## Playwright MCP Usage

### Starting the Game

```javascript
// Navigate and wait for load
await page.goto('http://localhost:3000');
await page.waitForLoadState('networkidle');
```

### Testing Controls

```javascript
// Keyboard input
await page.keyboard.press('KeyW');
await page.keyboard.up('KeyW');

// Mouse input
await page.mouse.click(x, y);
await page.mouse.down();
await page.mouse.up();

// Touch simulation
await page.touchscreen.tap(x, y);
```

### Continuous Movement (Critical for Games)

```javascript
// For game character movement, use key down/up patterns
// Single press() only simulates a quick tap

// Forward movement
await page.keyboard.down('KeyW');
await page.waitForTimeout(1000);  // Move for 1 second
await page.keyboard.up('KeyW');

// Diagonal movement with sprint
await page.keyboard.down('KeyW');
await page.keyboard.down('KeyD');
await page.keyboard.down('ShiftLeft');
await page.waitForTimeout(2000);
await page.keyboard.up('ShiftLeft');
await page.keyboard.up('KeyD');
await page.keyboard.up('KeyW');

// Combo sequence
async function executeCombo(page, sequence) {
  for (const action of sequence) {
    await page.keyboard.down(action.key);
    await page.waitForTimeout(action.hold);
    await page.keyboard.up(action.key);
    await page.waitForTimeout(50); // Combo window
  }
}

// Three-hit melee combo
await executeCombo(page, [
  { key: 'KeyJ', hold: 100 },
  { key: 'KeyJ', hold: 100 },
  { key: 'KeyK', hold: 200 }
]);
```

### Game State Detection (Vision MCP)

Use Vision MCP to analyze screenshots and determine current game state:

```javascript
// Detect game state from screenshot
async function detectGameState(screenshotPath) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `Analyze this game screenshot and determine:
    1. Is this a menu screen, gameplay, game over, victory, or loading?
    2. What UI elements are visible? (HUD, health bar, minimap, inventory)
    3. Is the player character visible?
    4. Are there any error messages?

    Respond in JSON:
    {
      "state": "menu|playing|gameover|win|loading|error",
      "uiElements": ["hud", "healthBar", ...],
      "playerVisible": true|false,
      "details": "description"
    }`
  });

  return JSON.parse(analysis);
}

// Usage during playtest
await page.screenshot({ path: 'playtest/state-1.png' });
const state = await detectGameState('playtest/state-1.png');
console.log('Current state:', state.state);
```

### Visual GDD Compliance Validation

```javascript
// Compare implementation against GDD visual requirements
async function validateVisualGDD(screenshotPath, gddRequirement) {
  const analysis = await visionAnalyze(screenshotPath, {
    prompt: `According to this GDD requirement:
    "${gddRequirement}"

    Does the screenshot match? Check:
    1. Required elements are present
    2. Visual style is correct
    3. Colors/theme match specification
    4. Layout is as described

    Return {
      "matches": true|false,
      "deviations": [
        { "element": "name", "expected": "spec", "actual": "observed" }
      ],
      "severity": "low|medium|high"
    }`
  });

  return JSON.parse(analysis);
}

// Example: Validate character appearance
const characterGDD = "A knight in silver armor with blue cape, holding sword";
const result = await validateVisualGDD('playtest/character.png', characterGDD);
```

### Screenshot Comparison Analysis

```javascript
// Compare current state with baseline or previous state
async function comparePlaytestStates(beforePath, afterPath) {
  const comparison = await visionAnalyze([beforePath, afterPath], {
    prompt: `Compare these two gameplay screenshots.
    Image 1 is BEFORE the action.
    Image 2 is AFTER the action.

    What changed?
    1. Did player position change?
    2. Did UI elements change (health, score, ammo)?
    3. Are there new visual effects?
    4. Any bugs or glitches visible?

    Return {
      "playerMoved": true|false,
      "uiChanges": ["health decreased", "score increased", ...],
      "newEffects": ["explosion", "particle", ...],
      "issues": ["list of visual problems"]
    }`
  });

  return JSON.parse(comparison);
}
```

### Monitoring State

```javascript
// Get console messages
page.on('console', msg => {
  console.log(msg.text());
});

// Get page content
const content = await page.content();
```

### Capturing Evidence

```javascript
// Screenshot
await page.screenshot({
  path: 'screenshots/evidence.png',
  fullPage: true
});

// PDF
await page.pdf({
  path: 'report.pdf'
});

// Video (if supported)
// Start recording before gameplay
```

## Validation Categories

### Functional Validation

Does the feature work as intended?
- [ ] Mechanic functions correctly
- [ ] Inputs register properly
- [ ] Outputs are correct
- [ ] Edge cases handled

### Design Validation

Does it match the GDD?
- [ ] Mechanics match description
- [ ] Visuals match art style
- [ ] Audio matches sound design
- [ ] UX matches specifications

### Experience Validation

Is it fun?
- [ ] Game feels good
- [ ] Feedback is satisfying
- [ ] Challenge is appropriate
- [ ] Flow is engaging

## Common Issues to Check

| Issue | Check Method |
|-------|--------------|
| Console errors | Check browser console |
| Visual glitches | Compare to reference |
| Input lag | Test responsiveness |
| Performance | Monitor FPS |
| Crashes | Try stress scenarios |

## Playtest Report Template

```markdown
# Playtest Report - [Task Name]
**Date:** YYYY-MM-DD
**Tester:** Game Designer Agent
**GDD Version:** X.X.X

## Summary
[Overall assessment]

## GDD Compliance

| Mechanic | Status | Notes |
|----------|--------|-------|
| [Name] | ✅/❌/⚠️ | [Details] |

## Deviations Found

| Feature | Expected | Actual | Severity |
|---------|----------|-------|----------|
| [Name] | [GDD] | [Actual] | [High/Med/Low] |

## Issues Found

| ID | Type | Description | Severity | Status |
|----|------|-------------|----------|--------|
| 1 | [Type] | [Description] | [Level] | [Open] |

## Recommendations

1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

## Screenshots
![Screenshot 1](path/to/ss1.png)
![Screenshot 2](path/to/ss2.png)
```

## Sending Playtest Report

After completing playtest:

```powershell
Send-AgentMessage -From "gamedesigner" -To "pm" -Type "playtest_report" -Payload $report
```

## Retrospective Participation

When retrospective initiated:

1. **Play the game** - Full playthrough if possible
2. **Test each mechanic** - Systematic validation
3. **Capture evidence** - Screenshots of key moments
4. **Compare vs GDD** - Note all deviations
5. **Document findings** - Comprehensive report
6. **Send report** - To PM via message
7. **Write to retrospective.txt** - Team contribution

## Playtest Checklist

Before completing playtest:

- [ ] All core mechanics tested
- [ ] Edge cases explored
- [ ] Screenshots captured (before/after for key actions)
- [ ] **Game state detection verified via Vision MCP**
- [ ] **Visual GDD compliance validated via Vision MCP**
- [ ] Console checked for errors
- [ ] Performance monitored
- [ ] GDD compliance validated
- [ ] Findings documented
- [ ] Report sent to PM
