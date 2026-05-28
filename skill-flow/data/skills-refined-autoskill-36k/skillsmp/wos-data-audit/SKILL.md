---
name: wos-data-audit
description: Validate game data files against sources and cross-reference checks. Use to verify data accuracy, find inconsistencies, and ensure data integrity across all JSON files.
allowed-tools: Read, Glob, Grep, Bash(python:*), WebFetch, WebSearch
---

# WoS Data Audit - Data Validation & Integrity

## Purpose
Validates game data files for accuracy, consistency, and completeness. Reports discrepancies, missing data, and outdated information.

## When to Use
- After adding new game data
- Before releases to verify data quality
- When user reports incorrect information
- Periodic audits to catch stale data

## Audit Modes

### Quick Audit (default)
Runs essential checks only:
- JSON validity
- Cross-reference integrity
- Known high-impact values

### Full Audit
Comprehensive validation:
- All JSON file validation
- Cross-reference checks across all files
- External source verification
- Confidence grade review

## Reference Documents

- `DATA_AUDIT.md` - Complete data inventory with sources and confidence
- `CHIEF_GEAR_DATA.md` - Chief Gear data locations
- `data/confidence_scoring.json` - Confidence grade definitions

## Audit Checklist

### 1. JSON Validity Checks

Validate all JSON files parse correctly:

```python
import json
from pathlib import Path

def validate_json_files(data_dir):
    errors = []
    for json_file in Path(data_dir).rglob("*.json"):
        try:
            with open(json_file, encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{json_file}: {e}")
    return errors
```

Files to validate:
- `data/*.json` - Core game data
- `data/guides/*.json` - Strategy guides
- `data/optimizer/*.json` - Engine config
- `data/upgrades/*.json` - Upgrade edges
- `data/conversions/*.json` - Resource data
- `data/raw/*.json` - Research data
- `data/validation/*.json` - Validation reports

### 2. Cross-Reference Integrity

#### Hero Data Consistency
- `data/heroes.json` hero count matches `assets/heroes/` image count
- Hero IDs consistent across `heroes.json`, `hero_stats_database.json`, `hero_power_data.json`
- Generation values sequential (1-14+)

#### Chief Gear Consistency
- Slot names match across: `chief_gear.json`, `wos_schema.json`, `quick_tips.json`
- Expected slots: Coat, Pants, Belt, Weapon, Cap, Watch
- Set bonus logic consistent (3pc Defense, 6pc Attack)

#### Quick Tips Consistency
- All category icons have mappings in `get_category_icon()`
- All priorities have mappings in `get_priority_color()` and `get_priority_label()`
- No orphaned categories in common_mistakes

### 3. High-Impact Value Verification

Cross-check these against `DATA_AUDIT.md` high-priority items:

| Value | Location | Expected | Check Against |
|-------|----------|----------|---------------|
| Chief Gear slots | `chief_gear.json` | 6 slots | CHIEF_GEAR_DATA.md |
| Set bonuses | `wos_schema.json` | 3pc=Def, 6pc=Atk | CHIEF_GEAR_DATA.md |
| Tool Enhancement | `quick_tips.json` | 0.4%-2.5%/level | Wiki |
| SvS Fire Crystal | `events.json` | 2,000 pts | In-game |
| SvS Mithril | `events.json` | 40,000 pts | In-game |

### 4. Confidence Grade Review

Check files with low confidence (C, D, E) and flag for verification:

```python
# Files with lower confidence that need review
low_confidence_files = [
    "data/conversions/gem_shadow_prices.json",      # D - estimation
    "data/conversions/resource_value_hierarchy.json", # C - pack-based
    "data/guides/combat_formulas.json",              # B - derived
]
```

### 5. Stale Data Detection

Flag data files not updated in >60 days:

```python
from datetime import datetime, timedelta

def check_stale_files(data_dir, max_age_days=60):
    stale = []
    cutoff = datetime.now() - timedelta(days=max_age_days)
    for json_file in Path(data_dir).rglob("*.json"):
        mtime = datetime.fromtimestamp(json_file.stat().st_mtime)
        if mtime < cutoff:
            stale.append((json_file, mtime))
    return stale
```

### 6. Upgrade Edge Validation

Verify edge graphs are valid DAGs:

```python
def validate_edges(edges_file):
    """Check edge graph integrity."""
    with open(edges_file, encoding='utf-8') as f:
        data = json.load(f)

    edges = data.get("edges", [])
    errors = []

    # Check required fields
    for i, edge in enumerate(edges):
        if "from" not in edge or "to" not in edge:
            errors.append(f"Edge {i}: missing from/to")
        if "cost" not in edge:
            errors.append(f"Edge {i}: missing cost")

    return errors
```

## Output Format

### Quick Audit Report

```markdown
## Data Audit Report - Quick

**Date:** 2026-01-13
**Mode:** Quick

### Summary
- JSON Files: 67 checked, 0 errors
- Cross-References: 5 checks, 0 failures
- High-Impact Values: 5 verified

### Issues Found
(none)

### Warnings
- data/conversions/gem_shadow_prices.json - Confidence D, needs verification
```

### Full Audit Report

```markdown
## Data Audit Report - Full

**Date:** 2026-01-13
**Mode:** Full

### JSON Validation
| Directory | Files | Valid | Errors |
|-----------|-------|-------|--------|
| data/ | 15 | 15 | 0 |
| data/guides/ | 7 | 7 | 0 |
| data/upgrades/ | 12 | 12 | 0 |
| ... | ... | ... | ... |

### Cross-Reference Checks
| Check | Status | Details |
|-------|--------|---------|
| Hero count match | PASS | 56 heroes, 56 images |
| Chief Gear slots | PASS | 6 slots correct |
| ... | ... | ... |

### High-Impact Values
| Value | Expected | Actual | Status |
|-------|----------|--------|--------|
| Chief Gear slots | Coat,Pants,Belt,Weapon,Cap,Watch | Coat,Pants,Belt,Weapon,Cap,Watch | VERIFIED |
| Tool Enhancement | 0.4%-2.5%/level | 0.4%-2.5%/level | VERIFIED |
| ... | ... | ... | ... |

### Confidence Review
| File | Grade | Recommendation |
|------|-------|----------------|
| gem_shadow_prices.json | D | Verify against packs |
| combat_formulas.json | B | Test against combat |

### Stale Data
| File | Last Modified | Age |
|------|---------------|-----|
| (none over 60 days) | | |

### Recommendations
1. Verify gem_shadow_prices against current pack rates
2. Test combat_formulas against actual battle results
```

## Workflow

1. **Start audit** - Determine mode (quick/full)
2. **Run JSON validation** - Check all files parse
3. **Run cross-reference checks** - Verify consistency
4. **Check high-impact values** - Verify critical data
5. **Review confidence grades** - Flag low-confidence files
6. **Check for stale data** - Flag old files
7. **Generate report** - Output findings
8. **Update DATA_AUDIT.md** - Mark verification status

## Integration

After running audit:
1. Report findings to user
2. Update `DATA_AUDIT.md` verification checkboxes
3. Create issues for any problems found
4. Recommend fixes if applicable
