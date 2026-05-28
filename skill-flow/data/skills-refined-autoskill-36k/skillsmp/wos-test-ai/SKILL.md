---
name: wos-test-ai
description: Run comprehensive AI and recommendation system tests. Creates test users at different game stages (Gen 10 dolphin, Gen 4 F2P, Gen 2 whale) with farm accounts, tests recommendations, lineups, and AI question routing.
allowed-tools: Bash, Read, Glob, Grep
---

# WoS AI Test Suite

## Purpose
Run comprehensive tests of the AI recommendation and lineup systems across different player profiles to ensure advice quality and catch regressions.

## Quick Start

Run the full test suite:
```bash
cd /c/Users/adam/PycharmProjects/WoS && .venv/Scripts/python.exe scripts/test_ai_comprehensive.py
```

## What Gets Tested

### Test Profiles Created

**6 Users, 9 Profiles total:**

| User | Profile | State | Furnace | Spending | Notes |
|------|---------|-------|---------|----------|-------|
| test_gen10_dolphin | FrostKnight_560 (main) | 456 | FC30 | dolphin | Full hero roster, Mythic gear |
| | FrostKnight_Farm (farm) | 456 | FC25 | f2p | Same state, linked to main |
| test_gen4_f2p | IceWarrior_240 | 789 | FC27 | f2p | Single account player |
| test_gen2_whale | ArcticKing_80 (main) | 999 | FC25 | whale | High spender, rally lead |
| | ArcticKing_Farm (farm) | 999 | FC18 | f2p | Same state, linked to main |
| test_multi_state | Nomad_OldState | 200 | FC29 | minnow | Multi-server player |
| | Nomad_NewState | 850 | FC20 | f2p | DIFFERENT state (migration) |
| test_new_player | FreshChief_7 | 900 | FC18 | f2p | Brand new, day 7 |
| test_rally_leader | RallyCommander_380 | 350 | FC30 | orca | Leads rallies, doesn't join |

### Test Categories

1. **Recommendations** - Verifies:
   - Spending-profile-aware advice (F2P vs whale)
   - Farm account detection and specific recommendations
   - Priority ordering by relevance
   - Category distribution (hero, gear, progression)

2. **Lineups** - Verifies:
   - Rally joiner confidence (high for main, low for farm)
   - Hero slot assignments
   - Troop ratio recommendations
   - All game modes (Bear Trap, Crazy Joe, Garrison, SvS)

3. **AI Question Routing** - Verifies:
   - Simple questions go to rules engine (cost-efficient)
   - Complex analysis questions go to AI
   - Routing accuracy percentage

## Expected Results

### Good Indicators
- Farm accounts show "Focus on 1-2 heroes only" as top recommendation
- F2P accounts show limited hero recommendations (top 3 only)
- Main accounts show "high" lineup confidence
- Farm accounts show "low" lineup confidence
- 90%+ questions handled by rules engine

### Red Flags
- All heroes getting skill recommendations (should be limited by spending profile)
- Farm accounts getting exploration skill recommendations
- Low lineup confidence on well-equipped main accounts
- High AI routing percentage (indicates rules gaps)

## Analyzing Results

After running tests, look for:

1. **Recommendation Distribution**
   ```
   Gen 10 Dolphin (Main): hero: 8, progression: 1, war_academy: 1
   Gen 10 Dolphin (Farm): hero: 1, gear: 2, chief_charm: 5
   ```
   - Main accounts should have more hero recommendations
   - Farm accounts should focus on gear/charms, minimal heroes

2. **Question Routing**
   ```
   Rules: 36 (92.3%)
   AI: 3 (7.7%)
   ```
   - Target: 90%+ rules
   - If AI % is high, add more rules for common questions

3. **Lineup Confidence**
   - Main accounts: all "high"
   - Farm accounts: all "low" (expected)

## Test Users

Test users are created with password `test123`:
- `test_gen10_dolphin` - Dolphin player with main + farm in same state
- `test_gen4_f2p` - F2P player with single account
- `test_gen2_whale` - Whale player with main + farm in same state
- `test_multi_state` - Player with accounts in DIFFERENT states
- `test_new_player` - Brand new player (day 7)
- `test_rally_leader` - Orca who leads rallies (different role)

You can log in as these users in the app to manually verify recommendations.

## Modifying Tests

The test script is at `scripts/test_ai_comprehensive.py`.

Key sections:
- `create_gen10_dolphin_user()` - Hero roster for dolphin player
- `create_gen4_f2p_user()` - Hero roster for F2P player
- `create_gen2_whale_user()` - Hero roster for whale player
- `TEST_QUESTIONS` - Questions to test routing

## Troubleshooting

### Import Errors
If you see `NameError: name 'X' is not defined`, check `database/models.py` imports.

### Database Errors
Delete `wos.db` and restart to recreate the database:
```bash
rm /c/Users/adam/PycharmProjects/WoS/wos.db
```

### API Key Issues
Verify OpenAI key is set:
```bash
echo $OPENAI_API_KEY
```

## After Testing

Review the output and look for:
1. Are recommendations appropriate for each spending profile?
2. Are farm accounts getting farm-specific advice?
3. Is lineup confidence correct?
4. What percentage of questions went to AI vs rules?

If issues are found, update the analyzers in `engine/analyzers/` and re-run tests.
