---
name: veilbreakers-vera-test
description: Use when modifying VERA dialogue or testing her personality system. Ensures she remains consistent and her glitches work properly.
---

# VeilBreakers VERA Test

## Overview

VERA is the game's most complex character. Her dual nature (helpful guide / demon in disguise) requires careful testing to maintain immersion.

## When to Use

- Writing new VERA dialogue
- Modifying glitch triggers
- Testing corruption responses
- Verifying personality consistency
- Adding new player interactions

## VERA's Dual Nature

### Surface: The Guide
- Brilliant (top 1% of 22 billion tested)
- Helpful, supportive, slightly mysterious
- Assigned by The Compact to help player
- Claims glitches are "errors"

### Truth: VERATH
- Dimension-devouring demon
- Sealed inside VERA as infant
- Slowly regaining memories
- Manipulating player to reach Veil

## Veil Integrity System

**Hidden value (100 → 0)** that controls VERA's behavior:

| Integrity | State | Behavior |
|-----------|-------|----------|
| 75-100 | Stable | Helpful, human, rare glitches |
| 50-74 | Unstable | More glitches, contradictory advice |
| 25-49 | Bleeding | Knows too much, obvious glitches |
| 0-24 | Dominant | "We think...", affects ending |

## Glitch Probability

```
P(glitch) = (100 - VeilIntegrity) / 100
```

At 75 integrity: 25% chance
At 50 integrity: 50% chance
At 25 integrity: 75% chance

## Test Scenarios

### Scenario 1: Pure Player (Low Corruption)
- Player uses PURIFY frequently
- Party corruption average < 25%
- Expected: VERA seems uncomfortable, passive-aggressive

### Scenario 2: Dark Player (High Corruption)
- Player uses DOMINATE frequently
- Party corruption average > 60%
- Expected: VERA subtly approving, more glitches

### Scenario 3: BARGAIN Usage
- Player accepts BARGAIN
- Expected: VERA freezes, says "Bargains have... witnesses."

### Scenario 4: Ascension Focus
- Player Ascends monsters to 0-10% corruption
- Expected: VERA visibly uncomfortable, makes excuses to leave

## The Test Process

### Step 1: Define Game State
```
Player Corruption: X%
Veil Integrity: Y%
Recent Actions: [list]
Party Composition: [brands, corruption levels]
```

### Step 2: Launch VERA Tester
```
Task: Launch vera-dialogue-tester agent with:
"Test VERA response to [scenario] with game state [details]"
```

### Step 3: Verify Outputs
- [ ] Dialogue matches personality layer
- [ ] Glitch probability is correct
- [ ] Reactions match player actions
- [ ] No personality breaks

### Step 4: Check Edge Cases
- Player at 0% corruption (pure hero)
- Player at 100% corruption (completely dark)
- Veil Integrity at 0 (VERATH dominant)
- Rapid action switches (PURIFY then DOMINATE)

## Dialogue Guidelines

### What VERA Should Say
- Give tactical advice (until integrity low)
- React to player choices
- Occasionally hint at true nature (foreshadowing)
- Deflect personal questions early game

### What VERA Should NOT Say
- Openly reveal she's VERATH (except ending)
- Give consistently bad advice (suspicious)
- Ignore major player actions
- Break character without glitch marker

## Glitch Types Reference

| Trigger | Glitch | Subtlety |
|---------|--------|----------|
| DOMINATE used | Red pixels (0.3s) | Very subtle |
| Multiple DOMINATE | Bass undertone | Subtle |
| PURIFY on Abyssal | Silent 2 turns | Subtle |
| BARGAIN accepted | Eyes wrong | Noticeable |
| High party corruption | Shadow mismatch | Creepy |
| Low party corruption | Passive-aggressive | Behavioral |
