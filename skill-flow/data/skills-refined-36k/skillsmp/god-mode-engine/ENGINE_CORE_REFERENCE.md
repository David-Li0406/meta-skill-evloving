# Engine Core Reference

Quick reference for the `engine_core.py` GameEngine class.

## Class Overview

```python
from src.engine.engine_core import GameEngine

engine = GameEngine(supabase_client)
```

## Main Methods

### fetch_next_hand(user_id, game_id, current_level)
Routes to appropriate engine based on `game_registry.engine_type`:
- **PIO**: Returns `HandResult` with solver hand + suit isomorphism
- **CHART**: Returns `ChartInstruction` for static range UI
- **SCENARIO**: Returns `ScenarioInstruction` for mental game drill

### resolve_villain_action(solver_node)
Weighted RNG for villain action selection. Returns `VillainAction` with:
- `action`: "CHECK", "BET", "FOLD", etc.
- `sizing`: Bet size as % of pot
- `next_node`: Next position in game tree

### calculate_hp_loss(user_action, solver_node)
Returns `HPResult` with:
- `is_correct`: True if matches max EV or indifferent
- `hp_damage`: 0-25 damage points
- `ev_loss`: Numeric EV difference

## Suit Isomorphism (The Magic Trick)

24x content multiplication from finite solver files:
```python
# All 4! = 24 possible suit permutations
suit_map = {"s": "h", "h": "d", "d": "c", "c": "s"}
variant_hash = "s=h,h=d,d=c,c=s"

# Same hand appears visually different
"AhKs" → "AdKh"  # Rotation key 1
"AhKs" → "AcKd"  # Rotation key 2
```

## Indifference Rule

Actions with ≥40% solver frequency OR EV within 0.05 of max = **CORRECT** (0 damage)

## HP Damage Scaling

| EV Loss % | HP Damage |
|-----------|-----------|
| 0% | 0 |
| 1-5% | 1-5 |
| 6-25% | 6-15 |
| 25%+ | 16-25 (max) |
