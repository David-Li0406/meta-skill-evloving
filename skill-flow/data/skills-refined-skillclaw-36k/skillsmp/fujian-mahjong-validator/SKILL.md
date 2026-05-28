---
name: fujian-mahjong-validator
description: Validate Fujian Mahjong game logic including hands, sets, winning conditions, Gold tile rules, and scoring. Use when testing mahjong game code, checking if a hand wins, calculating scores, or verifying move legality.
---

# Fujian Mahjong Validator

Validates game logic for Fujian (Fuzhou) Mahjong, also known as "Gold Rush Mahjong" (金麻将).

**Current Features**: Full game with Kongs, Golden Pair bonus (+30), All One Suit bonus (+60), dealer streak.

## When to Use

- Validate if a hand is a winning hand
- Check if sets (chows, pungs) are valid
- Calculate scores for a winning hand
- Verify move legality (chow, pung, win calls)
- Test Gold tile substitution logic

## Rules Reference

- `mahjong-fujian-rules.md` — Complete rules
- `app/FUTURE_FEATURES.md` — Roadmap for planned features

## Tile Representation

```
Suits (108 tiles):
  dots_1 to dots_9 (4 copies each = 36)
  bamboo_1 to bamboo_9 (4 copies each = 36)
  characters_1 to characters_9 (4 copies each = 36)

Bonus (20 tiles):
  wind_east, wind_south, wind_west, wind_north (4 copies each = 16)
  dragon_red (4 copies = 4)

Gold:
  One suit tile flipped at game start (not used in play)
  Only 3 Gold tiles remain in the game
  Gold tiles can substitute for ANY tile
```

## Validation Functions

### 1. Three Golds Detection (Check First!)

**Three Golds**: Player collects all 3 Gold tiles → instant automatic win

```javascript
function hasThreeGolds(hand, goldTileType) {
  const goldCount = hand.filter(t => t === goldTileType).length;
  return goldCount === 3;
}
```

- Check after EVERY draw (normal, replacement, bonus)
- Cannot be declined — triggers automatically
- Counts as self-draw (×2 multiplier)
- +20 special bonus

### 2. Hand Validation

**During play**: 16 tiles (concealed + exposed melds)
**After draw**: 17 tiles temporarily
**Winning hand**: 5 sets + 1 pair = 17 tiles

Sets can be Chow, Pung, or Kong (quad counts as one set)

### 3. Set Validation

**Chow (顺子)**: 3 consecutive same-suit tiles
```javascript
// Valid: bamboo_2, bamboo_3, bamboo_4
// Valid with Gold: bamboo_2, GOLD, bamboo_4 (Gold = bamboo_3)
```

**Pung (刻子)**: 3 identical tiles
```javascript
// Valid: dots_7, dots_7, dots_7
// Valid with Gold: dots_7, dots_7, GOLD (Gold = dots_7)
```

**Pair (眼)**: 2 identical tiles
```javascript
// Valid: characters_5, characters_5
// Valid with Gold: characters_5, GOLD (Gold = characters_5)
```

Gold tiles can substitute in any position.

### 4. Win Detection Algorithm

```javascript
function isWinningHand(tiles, goldTileType) {
  // tiles should be 17 tiles (hand + drawn tile)

  // Step 1: Check Three Golds first
  if (hasThreeGolds(tiles, goldTileType)) {
    return { winning: true, type: 'three_golds' };
  }

  // Step 2: Try to form 5 sets + 1 pair
  const goldCount = tiles.filter(t => t === goldTileType).length;
  const nonGoldTiles = tiles.filter(t => t !== goldTileType);

  return tryFormWinningHand(nonGoldTiles, goldCount);
}

function tryFormWinningHand(tiles, goldsRemaining) {
  // Try each possible pair
  const uniqueTiles = [...new Set(tiles)];

  for (const pairTile of uniqueTiles) {
    const remaining = removeTiles(tiles, [pairTile, pairTile]);
    if (remaining !== null && canFormFiveSets(remaining, goldsRemaining)) {
      return { winning: true, pair: pairTile };
    }
  }

  // Try using Gold(s) as pair
  if (goldsRemaining >= 2) {
    if (canFormFiveSets(tiles, goldsRemaining - 2)) {
      return { winning: true, pair: 'gold_pair' };
    }
  }
  if (goldsRemaining >= 1) {
    for (const pairTile of uniqueTiles) {
      const remaining = removeTiles(tiles, [pairTile]);
      if (remaining !== null && canFormFiveSets(remaining, goldsRemaining - 1)) {
        return { winning: true, pair: pairTile };
      }
    }
  }

  return { winning: false };
}

function canFormFiveSets(tiles, goldsRemaining, setsFormed = 0) {
  if (tiles.length === 0 && setsFormed === 5) return true;
  if (tiles.length === 0 && setsFormed < 5) {
    // Can we complete remaining sets with Golds?
    const setsNeeded = 5 - setsFormed;
    return goldsRemaining >= setsNeeded * 3;
  }
  if (tiles.length < 3 && goldsRemaining < 3 - tiles.length) return false;

  // Sort tiles for consistent processing
  tiles = sortTiles(tiles);
  const firstTile = tiles[0];

  // Try Pung
  if (countTile(tiles, firstTile) >= 3) {
    const remaining = removeTiles(tiles, [firstTile, firstTile, firstTile]);
    if (canFormFiveSets(remaining, goldsRemaining, setsFormed + 1)) {
      return true;
    }
  }

  // Try Pung with Gold(s)
  if (countTile(tiles, firstTile) === 2 && goldsRemaining >= 1) {
    const remaining = removeTiles(tiles, [firstTile, firstTile]);
    if (canFormFiveSets(remaining, goldsRemaining - 1, setsFormed + 1)) {
      return true;
    }
  }
  if (countTile(tiles, firstTile) === 1 && goldsRemaining >= 2) {
    const remaining = removeTiles(tiles, [firstTile]);
    if (canFormFiveSets(remaining, goldsRemaining - 2, setsFormed + 1)) {
      return true;
    }
  }

  // Try Chow (only for suit tiles)
  if (isSuitTile(firstTile)) {
    const [suit, num] = parseTile(firstTile);
    const tile2 = `${suit}_${num + 1}`;
    const tile3 = `${suit}_${num + 2}`;

    if (hasTile(tiles, tile2) && hasTile(tiles, tile3)) {
      const remaining = removeTiles(tiles, [firstTile, tile2, tile3]);
      if (canFormFiveSets(remaining, goldsRemaining, setsFormed + 1)) {
        return true;
      }
    }

    // Try Chow with Gold substitutions (multiple combinations)
    // ... (similar pattern with goldsRemaining)
  }

  return false;
}
```

### 5. Score Calculation

```javascript
function calculateScore(winner) {
  const { bonusTiles, goldsInHand, isSelfDraw, isThreeGolds,
          concealedKongs, exposedKongs, hasGoldenPair, isAllOneSuit } = winner;

  // Non-special points
  let points = 1;                          // Base
  points += bonusTiles.length;             // +1 per bonus tile
  points += goldsInHand;                   // +1 per Gold
  points += concealedKongs * 2;            // +2 per concealed Kong
  points += exposedKongs * 1;              // +1 per exposed Kong

  // Self-draw multiplier
  if (isSelfDraw || isThreeGolds) {
    points = points * 2;
  }

  // Special bonuses (added after multiplier)
  if (isThreeGolds) points += 20;
  if (hasGoldenPair) points += 30;         // 2 Golds form the pair
  if (isAllOneSuit) points += 60;          // All tiles same suit

  return {
    points,
    eachLoserPays: points,
    totalFromLosers: points * 3
  };
}
```

**Scoring Formula**:
```
points = (1 + bonus + golds + kong_bonuses) × 2 if self_draw
       + 20 if three_golds
       + 30 if golden_pair
       + 60 if all_one_suit
```

### 6. Move Legality

**Chow**:
- Only from player to your LEFT (previous in turn order)
- Need 2 sequential tiles in hand
- Gold CANNOT be used for calling

**Pung**:
- From ANY player's discard
- Need 2 matching tiles in hand
- Gold CANNOT be used for calling

**Win**:
- From any discard that completes hand, OR
- Self-draw that completes hand
- Winning is OPTIONAL (can decline, except Three Golds)

**Priority**: Win > Pung > Chow

**Tie-breaker**: Closest to discarder (counter-clockwise) wins

### 7. Calling System Validation

```javascript
function getValidCalls(player, discardedTile, discarderIndex, playerIndex) {
  const calls = [];
  const hand = player.concealedTiles;

  // Check Win
  const testHand = [...hand, discardedTile];
  if (isWinningHand(testHand, goldTileType).winning) {
    calls.push('win');
  }

  // Check Pung (need 2 matching, NOT Gold)
  const matchCount = hand.filter(t => t === discardedTile && t !== goldTileType).length;
  if (matchCount >= 2) {
    calls.push('pung');
  }

  // Check Chow (only from left player)
  const isLeftPlayer = (discarderIndex + 1) % 4 === playerIndex;
  if (isLeftPlayer && isSuitTile(discardedTile)) {
    // Check for sequential tiles (not using Gold)
    const [suit, num] = parseTile(discardedTile);
    const hasSequence =
      (hasTile(hand, `${suit}_${num-2}`) && hasTile(hand, `${suit}_${num-1}`)) ||
      (hasTile(hand, `${suit}_${num-1}`) && hasTile(hand, `${suit}_${num+1}`)) ||
      (hasTile(hand, `${suit}_${num+1}`) && hasTile(hand, `${suit}_${num+2}`));
    if (hasSequence) {
      calls.push('chow');
    }
  }

  // Pass is always available
  calls.push('pass');

  return calls;
}
```

## Testing Checklist

When validating game code, verify:

- [ ] 16 tiles (concealed + exposed) maintained during play
- [ ] 17 tiles after draw, before discard/win
- [ ] Only 3 Gold tiles in play (1 exposed, not used)
- [ ] Wind/dragon tiles auto-exposed with replacement draws
- [ ] Taking discard skips normal draw
- [ ] **Three Golds**: instant automatic win when player collects all 3 Golds
- [ ] Kong replacement draw from back of wall
- [ ] Scoring includes kong bonuses (+2 concealed, +1 exposed)
- [ ] Golden Pair bonus (+30) when 2 Golds form the pair
- [ ] All One Suit bonus (+60) for flush hands
- [ ] Payment: all 3 losers pay winner
- [ ] Call priority: Win > Kong > Pung > Chow
- [ ] Chow only from player to your left
- [ ] Gold cannot be used for calling (Chow/Pung/Kong)
- [ ] Winning is optional (except Three Golds)
- [ ] All players must manually pass (no auto-pass)

## Not Yet Implemented

- ❌ Calling phase timer (reverted due to Firebase sync issues)
- ❌ Robbing the Kong
- ❌ No Bonus/Kong bonus (+10)
