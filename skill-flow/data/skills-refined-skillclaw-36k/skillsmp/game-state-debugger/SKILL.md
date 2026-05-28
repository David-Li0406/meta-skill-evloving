---
name: game-state-debugger
description: Debug Fujian Mahjong game state issues. Use when game state is inconsistent, tiles are missing/duplicated, turns are stuck, or multiplayer sync issues occur.
---

# Game State Debugger

Helps debug game state issues in Fujian Mahjong.

## When to Use

- Tiles are missing or duplicated
- Hand sizes are wrong
- Turn order is broken
- Calling phase is stuck
- Scores don't match expected
- Multiplayer state is out of sync
- Game phase transitions fail

## State Validation Functions

### 1. Tile Count Validation

Total tiles should always equal 128.

```javascript
function validateTileCount(gameState, privateHands) {
  const errors = [];
  let totalTiles = 0;
  const allTiles = [];

  // Wall
  totalTiles += gameState.wall.length;
  allTiles.push(...gameState.wall);

  // Discard pile
  totalTiles += gameState.discardPile.length;
  allTiles.push(...gameState.discardPile);

  // Exposed gold
  totalTiles += 1;
  allTiles.push(gameState.exposedGold);

  // Each player
  for (let seat = 0; seat < 4; seat++) {
    // Concealed tiles
    const concealed = privateHands[`seat${seat}`]?.concealedTiles || [];
    totalTiles += concealed.length;
    allTiles.push(...concealed);

    // Exposed melds
    const melds = gameState.exposedMelds[`seat${seat}`] || [];
    for (const meld of melds) {
      totalTiles += meld.tiles.length;
      allTiles.push(...meld.tiles);
    }

    // Bonus tiles
    const bonus = gameState.bonusTiles[`seat${seat}`] || [];
    totalTiles += bonus.length;
    allTiles.push(...bonus);
  }

  if (totalTiles !== 128) {
    errors.push({
      type: 'TILE_COUNT_MISMATCH',
      expected: 128,
      actual: totalTiles,
      difference: 128 - totalTiles
    });
  }

  return { totalTiles, allTiles, errors };
}
```

### 2. Duplicate Tile Detection

Each tile ID should appear exactly once.

```javascript
function findDuplicateTiles(allTiles) {
  const seen = new Map();
  const duplicates = [];

  for (const tile of allTiles) {
    if (seen.has(tile)) {
      duplicates.push({
        tile,
        firstLocation: seen.get(tile),
        duplicateLocation: 'unknown'  // Would need to track location
      });
    } else {
      seen.set(tile, 'found');
    }
  }

  return duplicates;
}
```

### 3. Hand Size Validation

```javascript
function validateHandSizes(gameState, privateHands) {
  const errors = [];
  const phase = gameState.phase;
  const currentPlayer = gameState.currentPlayerSeat;

  for (let seat = 0; seat < 4; seat++) {
    const concealed = privateHands[`seat${seat}`]?.concealedTiles || [];
    const melds = gameState.exposedMelds[`seat${seat}`] || [];
    const meldTileCount = melds.reduce((sum, m) => sum + m.tiles.length, 0);
    const totalInHand = concealed.length + meldTileCount;

    let expectedSize;
    let allowedSizes;

    if (phase === 'playing' && seat === currentPlayer) {
      // Current player after draw: 17 tiles
      expectedSize = 17;
      allowedSizes = [16, 17];  // 16 if just discarded, 17 if just drew
    } else {
      // Other players or non-turn: 16 tiles
      expectedSize = 16;
      allowedSizes = [16];
    }

    if (!allowedSizes.includes(totalInHand)) {
      errors.push({
        type: 'HAND_SIZE_ERROR',
        seat,
        expected: expectedSize,
        actual: totalInHand,
        concealed: concealed.length,
        melds: meldTileCount,
        phase,
        isCurrentPlayer: seat === currentPlayer
      });
    }
  }

  return errors;
}
```

### 4. Gold Tile Validation

```javascript
function validateGoldTiles(gameState, privateHands) {
  const errors = [];
  const goldType = gameState.goldTileType;

  // Find all gold tiles in play
  const goldTiles = [];

  // Check exposed gold
  if (getTileType(gameState.exposedGold) === goldType) {
    goldTiles.push({ tile: gameState.exposedGold, location: 'exposed' });
  } else {
    errors.push({
      type: 'EXPOSED_GOLD_MISMATCH',
      expected: goldType,
      actual: getTileType(gameState.exposedGold)
    });
  }

  // Check all locations for gold tiles
  for (let seat = 0; seat < 4; seat++) {
    const concealed = privateHands[`seat${seat}`]?.concealedTiles || [];
    for (const tile of concealed) {
      if (getTileType(tile) === goldType) {
        goldTiles.push({ tile, location: `seat${seat}_concealed` });
      }
    }

    const melds = gameState.exposedMelds[`seat${seat}`] || [];
    for (const meld of melds) {
      for (const tile of meld.tiles) {
        if (getTileType(tile) === goldType) {
          goldTiles.push({ tile, location: `seat${seat}_meld` });
        }
      }
    }
  }

  for (const tile of gameState.discardPile) {
    if (getTileType(tile) === goldType) {
      goldTiles.push({ tile, location: 'discard' });
    }
  }

  for (const tile of gameState.wall) {
    if (getTileType(tile) === goldType) {
      goldTiles.push({ tile, location: 'wall' });
    }
  }

  // Should be exactly 4 gold tiles (1 exposed + 3 in play)
  if (goldTiles.length !== 4) {
    errors.push({
      type: 'GOLD_TILE_COUNT_ERROR',
      expected: 4,
      actual: goldTiles.length,
      found: goldTiles
    });
  }

  return { goldTiles, errors };
}
```

### 5. Turn Order Validation

```javascript
function validateTurnOrder(gameState, actionHistory) {
  const errors = [];

  // Check that turns follow counter-clockwise order
  let expectedNext = gameState.dealerSeat;

  for (const action of actionHistory) {
    if (action.type === 'discard') {
      if (action.seat !== expectedNext) {
        // Could be valid if someone called a discard
        const previousAction = actionHistory[actionHistory.indexOf(action) - 1];
        if (!previousAction || !['pung', 'chow'].includes(previousAction.type)) {
          errors.push({
            type: 'TURN_ORDER_VIOLATION',
            expected: expectedNext,
            actual: action.seat,
            action
          });
        }
      }
      expectedNext = (action.seat + 3) % 4;  // Counter-clockwise
    } else if (action.type === 'pung' || action.type === 'chow') {
      expectedNext = action.seat;  // Caller becomes current player
    }
  }

  return errors;
}
```

### 6. Calling Phase Validation

```javascript
function validateCallingPhase(gameState) {
  const errors = [];

  if (gameState.phase !== 'calling') {
    return errors;
  }

  const calls = gameState.pendingCalls;

  // Check that exactly one player is marked as discarder
  const discarders = Object.entries(calls)
    .filter(([_, call]) => call === 'discarder');

  if (discarders.length !== 1) {
    errors.push({
      type: 'CALLING_PHASE_NO_DISCARDER',
      discarders
    });
  }

  // Check that non-discarders have valid call values
  for (const [seat, call] of Object.entries(calls)) {
    if (call === 'discarder') continue;

    const validCalls = ['win', 'pung', 'chow', 'pass', null];
    if (!validCalls.includes(call)) {
      errors.push({
        type: 'INVALID_CALL_VALUE',
        seat,
        call
      });
    }
  }

  return errors;
}
```

### 7. Meld Validation

```javascript
function validateMelds(gameState, goldTileType) {
  const errors = [];

  for (let seat = 0; seat < 4; seat++) {
    const melds = gameState.exposedMelds[`seat${seat}`] || [];

    for (const meld of melds) {
      if (!['chow', 'pung', 'kong', 'concealed_kong'].includes(meld.type)) {
        errors.push({
          type: 'INVALID_MELD_TYPE',
          seat,
          meld,
          reason: 'Valid types: chow, pung, kong, concealed_kong'
        });
        continue;
      }

      const expectedSize = meld.type.includes('kong') ? 4 : 3;
      if (meld.tiles.length !== expectedSize) {
        errors.push({
          type: 'INVALID_MELD_SIZE',
          seat,
          meld,
          expected: expectedSize,
          actual: meld.tiles.length
        });
        continue;
      }

      // Validate meld is actually valid
      const tileTypes = meld.tiles.map(t => getTileType(t));

      if (meld.type === 'pung') {
        // All tiles should be same type (accounting for gold)
        const nonGoldTypes = tileTypes.filter(t => t !== goldTileType);
        const uniqueNonGold = [...new Set(nonGoldTypes)];

        if (uniqueNonGold.length > 1) {
          errors.push({
            type: 'INVALID_PUNG',
            seat,
            meld,
            reason: 'Pung tiles are not identical'
          });
        }
      } else if (meld.type === 'chow') {
        // Should be sequential same-suit tiles
        const isValid = isValidChow(tileTypes, goldTileType);
        if (!isValid) {
          errors.push({
            type: 'INVALID_CHOW',
            seat,
            meld,
            reason: 'Chow is not a valid sequence'
          });
        }
      }
    }
  }

  return errors;
}

function isValidChow(tileTypes, goldTileType) {
  // Filter out golds and check if remaining can form sequence
  const nonGold = tileTypes.filter(t => t !== goldTileType);
  const goldCount = tileTypes.length - nonGold.length;

  if (nonGold.length === 0) {
    // All golds - technically valid as any chow
    return true;
  }

  // Parse tiles
  const parsed = nonGold.map(t => {
    const [suit, num] = t.split('_');
    return { suit, num: parseInt(num) };
  });

  // All must be same suit
  const suits = [...new Set(parsed.map(p => p.suit))];
  if (suits.length !== 1 || !['dots', 'bamboo', 'characters'].includes(suits[0])) {
    return false;
  }

  // Check if can form sequence with gold substitution
  const nums = parsed.map(p => p.num).sort((a, b) => a - b);

  // With gold(s), check if sequence is possible
  // e.g., [2, 4] with 1 gold could be 2-3-4
  // This is a simplified check
  const min = Math.min(...nums);
  const max = Math.max(...nums);

  return max - min <= 2;  // Sequence spans at most 3 numbers
}
```

## Debug Output Functions

### Full State Dump

```javascript
function dumpGameState(gameState, privateHands) {
  console.log('=== GAME STATE DEBUG ===');
  console.log('Phase:', gameState.phase);
  console.log('Current Player:', gameState.currentPlayerSeat);
  console.log('Dealer:', gameState.dealerSeat);
  console.log('Gold Type:', gameState.goldTileType);
  console.log('Wall Size:', gameState.wall.length);
  console.log('Discard Pile Size:', gameState.discardPile.length);
  console.log('Last Action:', JSON.stringify(gameState.lastAction));

  console.log('\n--- Player Hands ---');
  for (let seat = 0; seat < 4; seat++) {
    const concealed = privateHands[`seat${seat}`]?.concealedTiles || [];
    const melds = gameState.exposedMelds[`seat${seat}`] || [];
    const bonus = gameState.bonusTiles[`seat${seat}`] || [];

    console.log(`Seat ${seat}:`);
    console.log(`  Concealed (${concealed.length}):`, concealed.join(', '));
    console.log(`  Melds (${melds.length}):`, JSON.stringify(melds));
    console.log(`  Bonus (${bonus.length}):`, bonus.join(', '));
  }

  if (gameState.phase === 'calling') {
    console.log('\n--- Pending Calls ---');
    console.log(JSON.stringify(gameState.pendingCalls, null, 2));
  }
}
```

### Validation Report

```javascript
function generateValidationReport(gameState, privateHands) {
  const report = {
    timestamp: new Date().toISOString(),
    phase: gameState.phase,
    errors: [],
    warnings: []
  };

  // Run all validations
  const tileValidation = validateTileCount(gameState, privateHands);
  report.errors.push(...tileValidation.errors);

  const duplicates = findDuplicateTiles(tileValidation.allTiles);
  if (duplicates.length > 0) {
    report.errors.push({
      type: 'DUPLICATE_TILES',
      duplicates
    });
  }

  const handErrors = validateHandSizes(gameState, privateHands);
  report.errors.push(...handErrors);

  const goldValidation = validateGoldTiles(gameState, privateHands);
  report.errors.push(...goldValidation.errors);

  const callingErrors = validateCallingPhase(gameState);
  report.errors.push(...callingErrors);

  const meldErrors = validateMelds(gameState, gameState.goldTileType);
  report.errors.push(...meldErrors);

  // Summary
  report.isValid = report.errors.length === 0;
  report.errorCount = report.errors.length;
  report.warningCount = report.warnings.length;

  return report;
}
```

## Common Issues and Fixes

### Issue: Tiles Disappearing

**Symptoms**: Tile count < 128, tiles missing

**Common Causes**:
1. Tile removed from hand but not added to discard/meld
2. Replacement draw not added to hand
3. Race condition in multiplayer

**Debug Steps**:
```javascript
// Track where tiles went
function trackTileMovement(before, after, action) {
  const beforeTiles = getAllTiles(before);
  const afterTiles = getAllTiles(after);

  const missing = beforeTiles.filter(t => !afterTiles.includes(t));
  const added = afterTiles.filter(t => !beforeTiles.includes(t));

  console.log('Action:', action);
  console.log('Missing:', missing);
  console.log('Added:', added);

  if (missing.length !== added.length) {
    console.error('TILE COUNT CHANGED!');
  }
}
```

### Issue: Turn Stuck

**Symptoms**: Game phase doesn't advance, no one can act

**Common Causes**:
1. pendingCalls has null values that never get filled
2. Phase transition condition not met
3. Current player disconnected

**Debug Steps**:
```javascript
function debugStuckTurn(gameState) {
  console.log('Phase:', gameState.phase);
  console.log('Current Player:', gameState.currentPlayerSeat);

  if (gameState.phase === 'calling') {
    const calls = gameState.pendingCalls;
    const waiting = Object.entries(calls)
      .filter(([_, v]) => v === null)
      .map(([k, _]) => k);

    console.log('Waiting for responses from:', waiting);
  }

  if (gameState.phase === 'playing') {
    console.log('Waiting for seat', gameState.currentPlayerSeat, 'to act');
  }
}
```

### Issue: Wrong Score

**Symptoms**: Calculated score doesn't match expected

**Debug Steps**:
```javascript
function debugScore(winner, gameState, privateHands) {
  const hand = privateHands[`seat${winner.seat}`].concealedTiles;
  const bonus = gameState.bonusTiles[`seat${winner.seat}`];
  const goldType = gameState.goldTileType;

  const goldsInHand = hand.filter(t => getTileType(t) === goldType).length;

  console.log('Score Debug:');
  console.log('  Base: 1');
  console.log('  Bonus tiles:', bonus.length, '(+' + bonus.length + ')');
  console.log('  Golds in hand:', goldsInHand, '(+' + goldsInHand + ')');
  console.log('  Subtotal:', 1 + bonus.length + goldsInHand);
  console.log('  Self-draw:', winner.isSelfDraw ? 'Yes (×2)' : 'No');
  console.log('  Three Golds:', winner.isThreeGolds ? 'Yes (+20)' : 'No');

  let total = 1 + bonus.length + goldsInHand;
  if (winner.isSelfDraw || winner.isThreeGolds) {
    total *= 2;
  }
  if (winner.isThreeGolds) {
    total += 20;
  }

  console.log('  Calculated Total:', total);
}
```

## Usage

When debugging, call these functions with your game state:

```javascript
// Quick validation
const report = generateValidationReport(gameState, privateHands);
if (!report.isValid) {
  console.error('Game state invalid:', report.errors);
}

// Full dump
dumpGameState(gameState, privateHands);

// Specific issue
debugStuckTurn(gameState);
```
