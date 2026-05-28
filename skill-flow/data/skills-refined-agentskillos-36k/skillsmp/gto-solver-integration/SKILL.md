---
name: GTO Solver Integration
description: Integrate PioSolver data with the poker training system
---

# GTO Solver Integration Skill

## Overview
Integrate PioSolver-solved hands with the Smarter.Poker training and AI systems.

## Database Tables

### solved_spots_gold (Postflop Engine)
```sql
-- Query structure
SELECT * FROM solved_spots_gold 
WHERE street = 'Flop'
  AND stack_depth = 40
  AND game_type = 'MTT'
  AND topology = '6-Max'
  AND mode = 'ICM';
```

**Key fields:**
- `scenario_hash` - Unique identifier
- `board_cards` - Array like `['As', '7d', '2h']`
- `strategy_matrix` - JSONB with all 1,326 hands
- `macro_metrics` - Range advantage, SPR, etc.

### memory_charts_gold (Preflop Engine)
```sql
-- Query structure
SELECT chart_grid FROM memory_charts_gold
WHERE chart_name = 'UTG_Open_100bb_9Max';
```

**Chart grid format:**
```json
{
  "AA": {"action": "Raise", "freq": 1.0, "size": "3bb"},
  "AKs": {"action": "Raise", "freq": 1.0, "size": "3bb"},
  "72o": {"action": "Fold", "freq": 1.0}
}
```

## Strategy Matrix Format
```json
{
  "AhKd": {
    "best_action": "Raise",
    "max_ev": 10.5,
    "ev_loss": 0,
    "actions": {
      "Raise": {"ev": 10.5, "freq": 1.0, "size": "66%"},
      "Call": {"ev": 8.2, "freq": 0.0},
      "Fold": {"ev": 0.0, "freq": 0.0}
    },
    "is_mixed": false
  }
}
```

## Helper Functions

### Get Horse Action (applies personality bias)
```sql
SELECT get_horse_action(
  1,  -- author_id
  '{"Raise": {"freq": 0.45}, "Call": {"freq": 0.35}, "Fold": {"freq": 0.20}}'::jsonb
);
-- Returns: 'Raise', 'Call', or 'Fold' based on personality
```

### Get Horse Personality
```sql
SELECT get_horse_personality(1);
-- Returns full JSONB with gto_adherence, mixed_strategy_bias, etc.
```

## Training Integration

### Scenario Selection
1. Query `solved_spots_gold` for matching conditions
2. Extract hero's hand from `strategy_matrix`
3. Present options to user
4. Compare to GTO frequencies
5. Calculate EV loss for feedback

### Example Flow
```javascript
// 1. Get solved spot
const { data: spot } = await supabase
  .from('solved_spots_gold')
  .select('strategy_matrix, macro_metrics')
  .eq('scenario_hash', scenarioHash)
  .single();

// 2. Get hero's hand strategy
const heroStrategy = spot.strategy_matrix[heroHand];

// 3. Calculate EV loss if user picks wrong
const evLoss = heroStrategy.max_ev - heroStrategy.actions[userAction].ev;
```

## Ingestion Script
Located at: `/scripts/ingest_god_mode.py`
- Processes PioSolver CSV exports
- Uploads to Supabase
- Creates scenario hashes

## Best Practices
1. Always check `is_mixed` before presenting single action
2. Show frequencies for mixed spots (e.g., "Raise 45%, Call 55%")
3. Use `macro_metrics` for context (range advantage, SPR)
4. Cache frequently-used spots for performance
