# God Mode Engine Examples

## Example 1: Suit Rotation (Isomorphism)

```python
from src.engine.engine_core import GameEngine

# Original hand
hero_hand = "AhKs"
board = "Qh7c2d"

# Apply rotation #1 (s→h, h→d, d→c, c→s)
rotated_hand = GameEngine.rotate_suits(hero_hand, 1)  # "AdKh"
rotated_board = GameEngine.rotate_suits(board, 1)      # "Qd7s2c"

# Same solver solution, different visual = unique training hand
```

## Example 2: Active Villain

```python
from src.engine.engine_core import GameEngine

# Solver says: check 60%, bet 50% pot 25%, bet 100% pot 15%
solver_node = {
    'actions': {
        'check': {'frequency': 0.60, 'ev': 5.0},
        'bet_50': {'frequency': 0.25, 'ev': 7.0},
        'bet_100': {'frequency': 0.15, 'ev': 6.5}
    }
}

# Villain picks action based on weighted RNG
villain = GameEngine.resolve_villain_action(solver_node)
print(f"Villain chose: {villain.action.value}")
# Output varies: "check" (~60%), "bet" (~40%)
```

## Example 3: Damage Calculation

```python
from src.engine.engine_core import GameEngine

solver_node = {
    'actions': {
        'call': {'frequency': 0.55, 'ev': 12.5},
        'raise': {'frequency': 0.45, 'ev': 12.3},
        'fold': {'frequency': 0.0, 'ev': 0.0}
    }
}

# User folds (wrong)
result = GameEngine.calculate_damage('fold', None, solver_node, pot_size=50)
print(result.is_correct)    # False
print(result.ev_loss)       # 12.5
print(result.chip_penalty)  # 6

# User calls (correct)
result = GameEngine.calculate_damage('call', None, solver_node, pot_size=50)
print(result.is_correct)    # True

# User raises (indifferent - 45% freq >= 40% threshold)
result = GameEngine.calculate_damage('raise', None, solver_node, pot_size=50)
print(result.is_correct)    # True (indifference rule)
print(result.is_indifferent) # True
```

## Example 4: Bet Slider Snapping

```tsx
// User drags slider to 53%
const visualValue = 53;

// Snap to nearest solver node
const SOLVER_NODES = [0, 25, 33, 50, 66, 75, 100, 150, 200];
const snappedValue = SOLVER_NODES.reduce((prev, curr) =>
  Math.abs(curr - visualValue) < Math.abs(prev - visualValue) ? curr : prev
);
// snappedValue = 50

// UI shows 53%, API receives 50%
```

## Example 5: Director Animation

```tsx
const actionHistory = [
  'Hero:raises 2.5x',
  'Villain:3-bets 8x',
  'Hero:calls'
];

// Director shows typewriter effect:
// "🎬 Setting the scene..."
// "Hero raises 2.5x..."
// "Villain 3-bets 8x..."
// "Hero calls..."
// "⚡ Your turn to act!"
// THEN table renders
```

## Example 6: API Usage

```javascript
// Fetch hand
const response = await fetch('/api/god-mode/fetch-hand', {
  method: 'POST',
  body: JSON.stringify({ gameId: 'short-stack-ninja', userId })
});
const { hand } = await response.json();
// hand.heroHand = "AdKh" (already rotated)

// Submit action
const result = await fetch('/api/god-mode/submit-action', {
  method: 'POST',
  body: JSON.stringify({
    gameId: 'short-stack-ninja',
    userId,
    action: 'raise',
    sizing: 50,
    fileId: hand.fileId,
    variantHash: hand.variantHash
  })
});
const damage = await result.json();
// damage.isCorrect, damage.chipPenalty, damage.feedback
```
