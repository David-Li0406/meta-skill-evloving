---
name: neuro-symbolic
description: Neuro-symbolic architecture patterns. Use when building the bridge between LLM (Neural) and Python rules (Symbolic).
---

# Neuro-Symbolic Architecture

## The Two Layers

### Neural Layer (LLM)
- Handles narrative, dialogue, improvisation
- Parses player intent into structured actions
- Wraps mechanical results in story

### Symbolic Layer (Python)
- Enforces SRD 5e rules strictly
- Uses RNG for dice (never LLM prediction)
- Validates all state changes

## The Resolution Loop

```
Player Input ("I attack the goblin")
    ↓
Neural: Parse Intent → AttackAction(target="Goblin")
    ↓
Symbolic: Execute Rules (roll dice, check AC, calculate damage)
    ↓
Result: {success: true, damage: 8}
    ↓
Neural: Narrate → "Your blade catches the goblin's shoulder..."
```

## Implementation Patterns

### Skill Functions (Symbolic)
```python
def resolve_attack(attacker: Entity, target: Entity) -> AttackResult:
    """Pure function. Takes data, returns data. No LLM calls."""
    roll = roll_dice("1d20")
    # ... SRD logic ...
    return AttackResult(hit=True, damage=8)
```

### Agent Prompts (Neural)
```python
PARSE_INTENT_PROMPT = """
Given the player's action, extract the structured intent.
Output JSON matching the ActionIntent schema.
"""

NARRATE_RESULT_PROMPT = """
Given the mechanical result, write engaging narrative.
Maintain the tone and pacing of the scene.
"""
```

## Core Axiom

> **Dolt is for Truth, Neo4j is for Search**

- Kill a goblin → Event in Dolt (can rollback/fork)
- Goblin's brother hates you → Relationship in Neo4j (for retrieval)
