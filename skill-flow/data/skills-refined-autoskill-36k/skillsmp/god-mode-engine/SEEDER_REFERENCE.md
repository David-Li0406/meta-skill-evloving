# Game Seeder Reference

Quick reference for the `seed_games.py` script.

## Commands

```bash
# Show engine distribution
python3 scripts/seed_games.py --stats

# Preview without database changes
python3 scripts/seed_games.py --dry-run

# Generate SQL file
python3 scripts/seed_games.py --output database/migrations/seed.sql

# Execute upsert (requires env vars)
SUPABASE_URL=xxx SUPABASE_KEY=xxx python3 scripts/seed_games.py
```

## Engine Assignment Keywords

### CHART Engine (19 games)
```
push/fold, bubble, satellite, icm, preflop, bounty, 
registration, ranges, resteal, squeeze, ante theft, 
chip & chair, blind defense, stop & go, 50/50, 
short stack, phase shifting
```

### SCENARIO Engine (21 games)
```
mental, tilt, zen, focus, discipline, ego, fear, habits, 
mind, patience, confidence, stamina, detachment, blindness, 
bankroll, autopilot, cooler, pressure chamber, winners tilt,
snap decision, table image
```

### PIO Engine (60 games)
Everything else (default for C-Bet, Cash, Postflop games)

## Config Auto-Generation

| Pattern | Stack | Players |
|---------|-------|---------|
| "Short Stack", "Push/Fold" | 20 | 6 |
| "Deep Stack" | 200 | 6 |
| "Hyper" | 10 | 6 |
| "Heads Up", "Duel" | 100 | 2 |
| "3-Max", "Spin" | 100 | 3 |
| Default | 100 | 6 |

## Output Distribution

```
PIO         60 ████████████████████████████████████████████████████████████
SCENARIO    21 █████████████████████
CHART       19 ███████████████████
TOTAL      100
```
