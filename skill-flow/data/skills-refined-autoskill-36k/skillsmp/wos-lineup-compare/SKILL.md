---
name: wos-lineup-compare
description: Run lineup recommendation comparisons between Claude and OpenAI. Validates the lineup engine, identifies improvement areas, and builds training data for future fine-tuning.
allowed-tools: Bash, Read, Glob, Grep
---

# WoS Lineup Comparison Tool

## Purpose
Compare lineup recommendations from Claude (direct) vs OpenAI (API) to:
1. Validate the lineup engine's recommendations
2. Identify disagreements for analysis
3. Build curated training data for fine-tuning
4. Track improvements over time

## Quick Start

### Run Full Comparison (195 tests)
```bash
cd /c/Users/adam/PycharmProjects/WoS && .venv/Scripts/python.exe scripts/run_lineup_comparison.py
```

### Run Specific Profiles Only
```bash
.venv/Scripts/python.exe scripts/run_lineup_comparison.py --profiles Gen10_Early,Gen10_Developed
```

### Run Specific Scenarios Only
```bash
.venv/Scripts/python.exe scripts/run_lineup_comparison.py --scenarios bear_trap,crazy_joe
```

### Analyze Existing Run
```bash
.venv/Scripts/python.exe scripts/run_lineup_comparison.py --analyze-run 8
```

## Key Files

| File | Purpose |
|------|---------|
| `scripts/run_lineup_comparison.py` | Main comparison runner |
| `scripts/test_lineups.py` | Test profile definitions (39 profiles) |
| `scripts/export_lineup_training_data.py` | Export curated training data |
| `.claude/lineup_comparison_run8_analysis.md` | Latest analysis document |

## Test Profiles (39 Total)

### Generation Baselines (14 profiles)
`Gen2_Early`, `Gen2_Developed`, `Gen4_Early`, `Gen4_Developed`, `Gen6_Early`, `Gen6_Developed`, `Gen8_Early`, `Gen8_Developed`, `Gen10_Early`, `Gen10_Developed`, `Gen12_Early`, `Gen12_Developed`, `Gen14_Early`, `Gen14_Developed`

### Level Impact (6 profiles)
`Levels_AllLow`, `Levels_AllMid`, `Levels_AllHigh`, `Levels_MetaHigh`, `Levels_NonMetaHigh`, `Levels_Top5Max`

### Hero Gear Impact (6 profiles)
`Gear_None`, `Gear_AllBlue`, `Gear_AllPurple`, `Gear_AllGold`, `Gear_MythicOnMeta`, `Gear_AllMythic`

### Chief Gear Impact (4 profiles)
`ChiefGear_Gray`, `ChiefGear_Blue`, `ChiefGear_Purple`, `ChiefGear_Gold`

### Charm Impact (4 profiles)
`Charms_None`, `Charms_Level5`, `Charms_Level10`, `Charms_Level16`

### Edge Cases (5 profiles)
`Edge_InfantryFocus`, `Edge_MarksmanFocus`, `Edge_FewHeroes`, `Edge_SpreadThin`, `Edge_UndergearedMeta`

## Scenarios Tested

| Scenario | Description | Key Hero |
|----------|-------------|----------|
| `bear_trap` | Bear Trap rally leader | Marksman lead |
| `crazy_joe` | Crazy Joe rally leader | Infantry (Jeronimo vs Wu Ming) |
| `garrison_joiner` | Garrison defense joiner | Sergey |
| `rally_joiner` | Rally attack joiner | Jessie |
| `svs_march` | SvS field march | Infantry lead |

## Understanding Results

### Agreement Categories

| Result | Meaning |
|--------|---------|
| `MATCH` | Both AIs picked same slot 1 hero |
| `DIFF` | Different slot 1 picks |
| `Heroes: 5/5` | All 5 hero slots matched |

### Quality Flags for Training Data

| Flag | Include in Training? | Meaning |
|------|---------------------|---------|
| `gold_standard` | YES | Both agreed - high confidence |
| `valid_alternative` | YES | Both answers valid (strategic debate) |
| `claude_correct` | YES | OpenAI violated roster constraints |
| `parser_false_positive` | NO | Same answer, parsing issue |
| `needs_review` | NO | Unclear - needs manual review |

## Export Training Data

```bash
# Export run 8 with quality annotations
.venv/Scripts/python.exe scripts/export_lineup_training_data.py --run-id 8

# Include items needing review (for manual curation)
.venv/Scripts/python.exe scripts/export_lineup_training_data.py --run-id 8 --include-needs-review
```

Output files:
- `data/ai/lineup_training_run8.jsonl` - For Ollama fine-tuning
- `data/ai/lineup_training_run8.json` - For review/analysis

## Previous Run Results

### Run 8 (Full Suite)
- **Total:** 195 comparisons
- **Agreement:** 85.5% slot 1 match
- **Joiner Scenarios:** 92% agreement
- **Rally Joiner:** 100% (Jessie always picked)
- **Cost:** $3.55 OpenAI, $0 Claude

### Key Findings from Run 8
1. **Parser issues:** OpenAI returns `Mia (Marksman, Gen 3)` - need to strip parentheticals
2. **Roster violations:** OpenAI sometimes recommends heroes not in roster
3. **Wu Ming vs Jeronimo:** Valid debate for Crazy Joe (both are S+ Infantry)
4. **Joiner mechanics:** Both AIs understand Jessie/Sergey importance

## Adding New Test Profiles

Edit `scripts/test_lineups.py`:

```python
def get_test_profiles():
    profiles = []

    # Add new profile
    profiles.append({
        'name': 'MyNewProfile',
        'group': 'edge',
        'generation': 10,
        'heroes': [
            {'name': 'Natalia', 'level': 70, 'stars': 5, 'gear_quality': 6},
            {'name': 'Jeronimo', 'level': 65, 'stars': 4, 'gear_quality': 5},
            # ... more heroes
        ]
    })

    return profiles
```

## Database Tables

| Table | Purpose |
|-------|---------|
| `lineup_test_runs` | Metadata for each test run |
| `lineup_test_results` | Individual comparison results |

Query results:
```sql
SELECT profile_name, scenario, slot1_match_openai, quality_flag
FROM lineup_test_results
WHERE test_run_id = 8
ORDER BY profile_name, scenario;
```

## Troubleshooting

### API Key Not Set
```bash
# Windows
set OPENAI_API_KEY=your-key-here

# Check if set
echo %OPENAI_API_KEY%
```

### Database Locked
Close any running Streamlit instances before running comparisons.

### Rate Limiting
The script includes delays between API calls. If you hit rate limits, increase the delay in `run_lineup_comparison.py`.

## Workflow for New Comparison Run

1. **Add new profiles** (if needed) in `scripts/test_lineups.py`
2. **Run comparison:**
   ```bash
   .venv/Scripts/python.exe scripts/run_lineup_comparison.py
   ```
3. **Review output** for disagreements
4. **Analyze patterns** - are disagreements valid debates or errors?
5. **Export training data:**
   ```bash
   .venv/Scripts/python.exe scripts/export_lineup_training_data.py --run-id <ID>
   ```
6. **Document findings** in `.claude/lineup_comparison_runX_analysis.md`
7. **Fix engine** if systematic issues found
