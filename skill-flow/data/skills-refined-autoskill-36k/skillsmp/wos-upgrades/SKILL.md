---
name: wos-upgrades
description: Access upgrade cost data for cost-aware recommendations. Use when user asks about upgrade costs, materials needed, ROI calculations, or "what do I need to reach X?". Uses tables-first data model with verified sources.
allowed-tools: Read, Glob, Bash(python:*)
---

# WoS Upgrade Costs - Cost-Aware Recommendations

## Purpose
Provides accurate upgrade cost data for calculating ROI and resource requirements. Enables "what do I need to upgrade X to Y?" queries.

## Data Files

### Upgrade Cost Data (UpgradeEdge model)
- `data/upgrades/manifest.json` - Dataset metadata and file listing
- `data/upgrades/sources.json` - Source registry for traceability
- `data/upgrades/chief_gear.steps.json` - Chief gear tier/step costs
- `data/upgrades/war_academy.steps.json` - War Academy FC step costs
- `data/validation/formula_checks.json` - Formula validation tests

### Related Schemas
- `data/upgrade_costs_schema.json` - UpgradeEdge data model documentation
- `data/confidence_scoring.json` - How to score data confidence
- `data/explanation_builder.json` - How to explain recommendations

## UpgradeEdge Data Model

Every upgrade is stored as an "edge" from one state to another:

```json
{
  "upgrade_id": "chief_gear:red-0:step1->step2",
  "system": "chief_gear",
  "from": { "tier": "red-0", "step": 1 },
  "to": { "tier": "red-0", "step": 2 },
  "cost": {
    "hardened_alloy": 12500,
    "polishing_solution": 132,
    "design_plan": 21,
    "lunar_amber": 2
  },
  "source_ids": ["SRC_WIKI_CHIEF_GEAR"],
  "confidence": { "grade": "A", "reason": "direct table row" }
}
```

## Instructions

### 1. Finding Upgrade Costs

To find cost for a specific upgrade:
1. Read the appropriate steps file (chief_gear, war_academy, etc.)
2. Match `from` state to user's current state
3. Return the `cost` object

```python
# Example: Find cost for chief gear red-0 step 1 -> step 2
edges = load_json("data/upgrades/chief_gear.steps.json")["edges"]
for edge in edges:
    if edge["from"]["tier"] == "red-0" and edge["from"]["step"] == 1:
        return edge["cost"]
```

### 2. Calculating Total Cost for Range

To calculate cost from level A to level B:
1. Find all edges in the path
2. Sum costs for each resource type

```python
def total_cost(system, from_state, to_state):
    edges = get_edges_in_path(system, from_state, to_state)
    totals = {}
    for edge in edges:
        for resource, amount in edge["cost"].items():
            totals[resource] = totals.get(resource, 0) + amount
    return totals
```

### 3. ROI Calculations

When comparing upgrades:
```
ROI = weighted_benefit_score / weighted_resource_cost
```

Resource scarcity weights vary by spender profile:
- F2P: Premium resources weighted heavily
- Whale: All resources weighted similarly

### 4. Prerequisites

War Academy and some systems have prerequisites:
```json
"prereq": [{ "system": "furnace", "level": "FC6" }]
```

Always check prerequisites before recommending an upgrade.

## Verified Sources

All data must be traceable to sources in `data/upgrades/sources.json`:

| Source ID | Type | Use |
|-----------|------|-----|
| SRC_WIKI_CHIEF_GEAR | wiki | Chief gear step costs |
| SRC_WHITEOUTAPP_WAR_ACADEMY | community_tool | War Academy costs |
| SRC_QUACKULATOR_CHIEF_GEAR | community_tool | Cross-validation |
| SRC_QUACKULATOR_BUILDING | community_tool | Building costs |
| SRC_ONECHILLEDGAMER_TROOP | community_tool | Troop costs |

## Systems Covered

### Currently Available
- **chief_gear** - Tier/step upgrade costs (red-0 through mythic)
- **war_academy** - FC level costs with prerequisites

### Planned (to be ingested)
- **troops** - Training/promotion costs by tier
- **buildings** - All building upgrade costs
- **hero_skills** - Manual costs per skill level
- **hero_levels** - XP costs per level
- **hero_stars** - Shard costs per star

## Output Format

When answering upgrade cost questions:

```
## Upgrade: Chief Gear Coat (Infantry) - Red-0 Step 1 → Step 2

### Cost
| Resource | Amount |
|----------|--------|
| Hardened Alloy | 12,500 |
| Polishing Solution | 132 |
| Design Plan | 21 |
| Lunar Amber | 2 |

### Source
Whiteout Survival Wiki - Chief Gear (Grade A confidence)

### Next Step
Red-0 Step 2 → Step 3 will cost...
```

**Note:** Chief Gear has 6 slots: Coat, Pants (Infantry), Belt, Weapon (Marksman), Cap, Watch (Lancer).
Keep all 6 at SAME TIER for set bonuses. When pushing to next tier, Infantry first.

## Confidence Rules

- **Grade A**: Direct table row from verified source
- **Grade B**: Calculated from verified formula, validated against table
- **Grade C**: Community consensus, may vary
- **Grade D**: Estimated, needs verification

Always show confidence grade with cost data.

## Integration with Recommendations

When wos-recommend needs cost data:
1. Call this skill to get upgrade costs
2. Factor costs into priority scoring
3. Include cost in recommendation explanation

Example integration:
```
### [HIGH] Upgrade Chief Gear Coat (Infantry) to Red-1
**Reason**: Infantry frontline first when pushing to next tier (all 6 pieces at same tier for set bonus)
**Cost**: 12,500 Hardened Alloy, 132 Polishing Solution, 21 Design Plan, 2 Lunar Amber
**ROI**: High (6-piece set bonus gives Attack to ALL troops)
```
