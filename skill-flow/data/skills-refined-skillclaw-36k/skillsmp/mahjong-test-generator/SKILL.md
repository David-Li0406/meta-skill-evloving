---
name: mahjong-test-generator
description: Generate test scenarios for Fujian Mahjong game logic. Use when you need test cases for win detection, Gold substitution, calling validation, edge cases, or scoring calculations.
---

# Mahjong Test Generator

Generates test scenarios for validating Fujian Mahjong game logic.

## When to Use

- Generate winning hands for win detection testing
- Create hands that are N tiles away from winning
- Generate Three Golds scenarios
- Create edge cases (wall exhaustion, bonus chains)
- Generate invalid hands to test rejection
- Create calling scenarios (multiple players can call)
- Generate scoring test cases

## Test Case Categories

### 1. Winning Hand Tests

#### Basic Winning Hands (No Gold)

```javascript
// All Chows
const allChowsHand = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'bamboo_4', 'bamboo_5', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'dots_7', 'dots_8', 'dots_9',
    'characters_3', 'characters_4', 'characters_5',
    'characters_1', 'characters_1'  // Pair
  ],
  goldTileType: 'dots_5',  // Not in hand
  expected: { winning: true, sets: 5, pair: 'characters_1' }
};

// All Pungs
const allPungsHand = {
  tiles: [
    'bamboo_1', 'bamboo_1', 'bamboo_1',
    'bamboo_5', 'bamboo_5', 'bamboo_5',
    'dots_3', 'dots_3', 'dots_3',
    'dots_9', 'dots_9', 'dots_9',
    'characters_7', 'characters_7', 'characters_7',
    'characters_2', 'characters_2'  // Pair
  ],
  goldTileType: 'dots_5',
  expected: { winning: true, sets: 5, pair: 'characters_2' }
};

// Mixed Chows and Pungs
const mixedHand = {
  tiles: [
    'bamboo_2', 'bamboo_3', 'bamboo_4',  // Chow
    'dots_5', 'dots_5', 'dots_5',         // Pung
    'characters_7', 'characters_8', 'characters_9',  // Chow
    'bamboo_6', 'bamboo_6', 'bamboo_6',   // Pung
    'dots_1', 'dots_2', 'dots_3',         // Chow
    'characters_1', 'characters_1'        // Pair
  ],
  goldTileType: 'bamboo_9',
  expected: { winning: true }
};
```

#### Winning Hands with Gold Substitution

```javascript
// Gold completing a Chow
const goldInChow = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_2', 'dots_4', 'dots_3',  // Gold is dots_3
    'characters_1', 'characters_1'
  ],
  goldTileType: 'dots_3',
  goldsInHand: 1,
  expected: { winning: true, goldUsedAs: 'dots_3' }
};

// Gold completing a Pung
const goldInPung = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',  // One dots_5 is actually Gold
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1', 'characters_1'
  ],
  goldTileType: 'dots_5',
  goldsInHand: 1,
  expected: { winning: true }
};

// Gold as part of pair
const goldInPair = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1', 'characters_1'  // One is Gold acting as characters_1
  ],
  goldTileType: 'characters_1',
  goldsInHand: 1,
  expected: { winning: true }
};

// Multiple Golds
const twoGoldsHand = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',  // Two are Golds
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1', 'characters_1'
  ],
  goldTileType: 'dots_5',
  goldsInHand: 2,
  expected: { winning: true }
};
```

### 2. Three Golds Tests

```javascript
// Three Golds instant win
const threeGoldsHand = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',  // All 3 are Gold
    'characters_7', 'characters_8',
    'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2',
    'characters_1', 'characters_1',
    'bamboo_9', 'bamboo_9'
  ],
  goldTileType: 'dots_5',
  goldsInHand: 3,
  expected: {
    winning: true,
    type: 'three_golds',
    instantWin: true
  }
};

// Three Golds during replacement draw
const threeGoldsDuringReplacement = {
  scenario: 'Player has 2 Golds, draws bonus tile, replacement is 3rd Gold',
  initialGolds: 2,
  bonusTileDrawn: 'wind_east',
  replacementTile: 'dots_5',  // This is the Gold type
  expected: { instantWin: true, type: 'three_golds' }
};
```

### 3. Non-Winning Hand Tests

```javascript
// One tile away (tenpai)
const oneTileAway = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1'  // Missing pair tile
  ],
  goldTileType: 'bamboo_9',
  waitingFor: ['characters_1'],
  expected: { winning: false, tenpai: true }
};

// Invalid hand - wrong tile count
const wrongTileCount = {
  tiles: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5', 'dots_5',
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3'
    // Only 15 tiles, missing pair
  ],
  expected: { winning: false, reason: 'wrong_tile_count' }
};

// Cannot form valid sets
const invalidSets = {
  tiles: [
    'bamboo_1', 'bamboo_3', 'bamboo_5',  // Not sequential
    'dots_5', 'dots_6', 'dots_5',         // Not a valid set
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1', 'characters_1'
  ],
  goldTileType: 'bamboo_9',
  expected: { winning: false }
};
```

### 4. Calling Scenario Tests

```javascript
// Multiple players can call same discard
const multipleCallersScenario = {
  discard: { tile: 'dots_5', playerIndex: 0 },
  players: [
    { index: 0, hand: [], canCall: [] },  // Discarder
    {
      index: 1,  // To the right of discarder
      hand: ['dots_5', 'dots_5', ...otherTiles],
      canCall: ['pung', 'pass']
    },
    {
      index: 2,  // Across from discarder
      hand: ['dots_4', 'dots_6', ...otherTiles],  // Can't chow (not left)
      canCall: ['pass']
    },
    {
      index: 3,  // To the left of discarder (next in turn)
      hand: ['dots_4', 'dots_6', ...otherTiles],
      canCall: ['chow', 'pass']
    }
  ],
  expected: {
    player1ValidCalls: ['pung', 'pass'],
    player2ValidCalls: ['pass'],
    player3ValidCalls: ['chow', 'pass'],
    ifBothCall: 'player1 wins (pung > chow)'
  }
};

// Win vs Pung priority
const winVsPungScenario = {
  discard: { tile: 'dots_5', playerIndex: 0 },
  players: [
    { index: 0, hand: [] },
    {
      index: 1,
      hand: ['dots_5', 'dots_5'],  // Can Pung
      canCall: ['pung']
    },
    {
      index: 2,
      // Completing hand with dots_5
      canCall: ['win']
    }
  ],
  expected: {
    winner: 2,
    reason: 'win > pung priority'
  }
};

// Chow restriction test
const chowRestrictionTest = {
  discard: { tile: 'bamboo_5', playerIndex: 2 },
  players: [
    {
      index: 0,  // NOT to right of player 2
      hand: ['bamboo_4', 'bamboo_6'],
      canCall: ['pass'],  // Cannot chow
      reason: 'Not left of discarder'
    },
    {
      index: 1,
      hand: ['bamboo_4', 'bamboo_6'],
      canCall: ['pass'],
      reason: 'Not left of discarder'
    },
    { index: 2, hand: [] },  // Discarder
    {
      index: 3,  // Left of player 2 (next in turn order)
      hand: ['bamboo_4', 'bamboo_6'],
      canCall: ['chow', 'pass'],
      reason: 'Is left of discarder'
    }
  ]
};

// Gold cannot be used for calling
const goldCallingRestriction = {
  discard: { tile: 'dots_5', playerIndex: 0 },
  goldTileType: 'dots_5',
  player: {
    hand: ['dots_5', 'dots_5'],  // Both are actually Gold tiles
    canCall: ['pass'],  // Cannot Pung with Golds
    reason: 'Gold cannot be used for calling'
  }
};
```

### 5. Scoring Tests

```javascript
// Basic win (discard)
const basicDiscardWin = {
  winner: {
    bonusTiles: [],
    goldsInHand: 0,
    isSelfDraw: false
  },
  expected: {
    base: 1,
    bonus: 0,
    golds: 0,
    subtotal: 1,
    multiplier: 1,
    total: 1
  }
};

// Self-draw win
const selfDrawWin = {
  winner: {
    bonusTiles: [],
    goldsInHand: 0,
    isSelfDraw: true
  },
  expected: {
    base: 1,
    subtotal: 1,
    multiplier: 2,
    total: 2
  }
};

// With bonus tiles
const withBonusTiles = {
  winner: {
    bonusTiles: ['wind_east', 'wind_south', 'dragon_red'],
    goldsInHand: 0,
    isSelfDraw: true
  },
  expected: {
    base: 1,
    bonus: 3,
    subtotal: 4,
    multiplier: 2,
    total: 8
  }
};

// With Golds
const withGolds = {
  winner: {
    bonusTiles: ['wind_east'],
    goldsInHand: 2,
    isSelfDraw: true
  },
  expected: {
    base: 1,
    bonus: 1,
    golds: 2,
    subtotal: 4,
    multiplier: 2,
    total: 8
  }
};

// Three Golds
const threeGoldsScoring = {
  winner: {
    bonusTiles: [],
    goldsInHand: 3,
    isSelfDraw: true,  // Three Golds counts as self-draw
    isThreeGolds: true
  },
  expected: {
    base: 1,
    golds: 3,
    subtotal: 4,
    multiplier: 2,
    afterMultiplier: 8,
    threeGoldsBonus: 20,
    total: 28
  }
};

// Maximum MVP score
const maxMvpScore = {
  winner: {
    bonusTiles: Array(10).fill('wind_east'),  // 10 bonus tiles (unlikely but test)
    goldsInHand: 3,
    isSelfDraw: true,
    isThreeGolds: true
  },
  expected: {
    base: 1,
    bonus: 10,
    golds: 3,
    subtotal: 14,
    multiplier: 2,
    afterMultiplier: 28,
    threeGoldsBonus: 20,
    total: 48
  }
};
```

### 6. Edge Case Tests

```javascript
// Wall exhaustion during bonus replacement
const wallExhaustionDuringReplacement = {
  scenario: 'Player draws bonus tile when wall has 0 tiles',
  wallCount: 0,
  drawnTile: 'wind_east',  // Bonus tile
  expected: {
    result: 'draw_game',
    reason: 'Cannot draw replacement'
  }
};

// Last tile in wall wins
const lastTileWins = {
  scenario: 'Player draws last tile and it completes hand',
  wallCount: 1,
  expected: {
    canWin: true,
    isSelfDraw: true
  }
};

// Last tile is bonus
const lastTileBonus = {
  scenario: 'Player draws last tile and it is a bonus tile',
  wallCount: 1,
  drawnTile: 'dragon_red',
  expected: {
    result: 'draw_game',
    reason: 'Last tile is bonus, cannot replace'
  }
};

// Winning after calling
const winAfterCalling = {
  scenario: 'Player Pungs a tile and hand is now complete',
  handBefore: [
    'bamboo_1', 'bamboo_2', 'bamboo_3',
    'dots_5', 'dots_5',  // Will Pung dots_5
    'characters_7', 'characters_8', 'characters_9',
    'bamboo_6', 'bamboo_6', 'bamboo_6',
    'dots_1', 'dots_2', 'dots_3',
    'characters_1', 'characters_1'
  ],
  discardedTile: 'dots_5',
  action: 'pung',
  expected: {
    handComplete: true,
    canDeclareWin: true,
    mustWin: false,  // Optional
    isSelfDraw: false  // Won from discard
  }
};

// Bonus tile chain
const bonusTileChain = {
  scenario: 'Player draws multiple bonus tiles in a row',
  draws: [
    { tile: 'wind_east', type: 'bonus', action: 'expose_and_replace' },
    { tile: 'wind_south', type: 'bonus', action: 'expose_and_replace' },
    { tile: 'dragon_red', type: 'bonus', action: 'expose_and_replace' },
    { tile: 'bamboo_5', type: 'suit', action: 'add_to_hand' }
  ],
  expected: {
    bonusTilesExposed: 3,
    tilesDrawn: 4,
    finalHandSize: 16  // or 17 if after normal draw
  }
};
```

## Generating Random Test Cases

```javascript
function generateRandomWinningHand(goldTileType) {
  // Generate 5 random valid sets
  const sets = [];
  for (let i = 0; i < 5; i++) {
    if (Math.random() > 0.5) {
      sets.push(generateRandomChow());
    } else {
      sets.push(generateRandomPung());
    }
  }

  // Generate random pair
  const pair = generateRandomPair();

  return {
    tiles: [...sets.flat(), ...pair],
    goldTileType,
    expected: { winning: true }
  };
}

function generateRandomChow() {
  const suits = ['dots', 'bamboo', 'characters'];
  const suit = suits[Math.floor(Math.random() * 3)];
  const start = Math.floor(Math.random() * 7) + 1;  // 1-7
  return [
    `${suit}_${start}`,
    `${suit}_${start + 1}`,
    `${suit}_${start + 2}`
  ];
}

function generateRandomPung() {
  const suits = ['dots', 'bamboo', 'characters'];
  const suit = suits[Math.floor(Math.random() * 3)];
  const num = Math.floor(Math.random() * 9) + 1;
  const tile = `${suit}_${num}`;
  return [tile, tile, tile];
}

function generateRandomPair() {
  const suits = ['dots', 'bamboo', 'characters'];
  const suit = suits[Math.floor(Math.random() * 3)];
  const num = Math.floor(Math.random() * 9) + 1;
  const tile = `${suit}_${num}`;
  return [tile, tile];
}
```

## Usage

When you need test cases, describe what you're testing and this skill will help generate appropriate scenarios. Specify:

1. What feature you're testing (win detection, calling, scoring, etc.)
2. Whether you need passing or failing cases
3. Any specific edge cases to cover
4. Whether Gold tiles should be involved
