# Demo Story Return Path Targets

This document identifies knots in `web/stories/demo.ink` that are suitable as return path targets for the AI Director when routing AI-generated branches back to scripted content.

## Overview

The expanded demo story contains **25 knots** with varied narrative contexts. The Director can use any knot as a return target, but some are better suited than others based on:

1. **Narrative neutrality** - Entry doesn't require specific prior context
2. **Multiple entry points** - Already has incoming paths from different scenes
3. **Meaningful continuation** - Offers interesting choices after arrival

## Recommended Return Path Targets

### Tier 1: Primary Return Points (Best)

| Knot | Context | Why Suitable |
|------|---------|--------------|
| `return_with_supplies` | Camp return | Natural convergence point; accepts any prior state; leads to meaningful choices |
| `return_empty` | Camp return | Alternative return state; branching continues |
| `campfire` | Camp scene | Central hub; player can redirect to forest or wait |
| `pines` | Forest entry | Gateway to multiple paths; narratively flexible |

### Tier 2: Secondary Return Points (Good)

| Knot | Context | Why Suitable |
|------|---------|--------------|
| `watchtower` | Discovery | Self-contained scene; doesn't require prior context |
| `tower_interior` | Exploration | Multiple exit paths available |
| `beacon_platform` | Discovery climax | Strong visual moment; multiple outcomes |
| `tense_return` | Tension | Works with or without wolves_spotted flag |
| `underbrush` | Forest exploration | Alternative forest path; self-contained |

### Tier 3: Contextual Return Points (Use Carefully)

| Knot | Context | Considerations |
|------|---------|----------------|
| `stranger_dialogue` | Dialogue | Requires met_stranger context for coherence |
| `wolves_warning` | Tension | Best if wolves_spotted is set |
| `artifact_mystery` | Discovery | Best if found_artifact is set |
| `escorted_return` | Dialogue | Implies stranger is present |

### Endings (Not Return Targets)

These knots terminate the story and should NOT be used as return paths:

- `rescue_end` - Terminal
- `waiting_end` - Terminal
- `quiet_end` - Terminal
- `lost_end` - Terminal
- `tower_gathering_end` - Terminal
- `urgent_return_end` - Terminal
- `revelation_end` - Terminal

## Scene Types for Branch Testing

The expanded story provides these narrative contexts for testing different AI branch types:

| Scene Type | Example Knots | Good For Testing |
|------------|---------------|------------------|
| **Dialogue** | `stranger_dialogue`, `escorted_return`, `philosophical_moment` | Character interactions, conversation branches |
| **Exploration** | `pines`, `trail`, `underbrush`, `tower_interior` | Environmental discovery, navigation choices |
| **Tension** | `wolves_warning`, `tense_return` | Urgency, stakes, time pressure |
| **Discovery** | `watchtower`, `artifact_mystery`, `smoke_pattern` | Mystery, revelation, hidden knowledge |
| **Introspection** | `meditation_moment` | Character development, reflection |

## State Variables

The Director should be aware of these story variables when evaluating branch coherence:

| Variable | Type | Effect |
|----------|------|--------|
| `campfire_log` | bool | Affects signal success in return scenes |
| `pocket_compass` | bool | Indicates compass was used |
| `courage` | int | Tracks bold choices |
| `caution` | int | Tracks careful choices |
| `met_stranger` | bool | Enables stranger-related dialogue |
| `found_artifact` | bool | Enables artifact-related content |
| `wolves_spotted` | bool | Adds tension to forest scenes |

## Usage Notes

1. **Preferred return points**: Use Tier 1 knots for most AI branches
2. **Context matching**: When using Tier 2/3 knots, ensure branch content sets up appropriate state
3. **Avoid endings**: Never route to `*_end` knots as return targets
4. **Test coverage**: Each recommended return point should have at least one test case in the validation corpus
