---
name: conflict-game
description: "Game design rules, mechanics, and conventions for the Conflict: Middle East Political Simulator remake"
globs:
  - "src/engine/**/*.ts"
  - "src/store/**/*.ts"
  - "data/*.yaml"
  - "src/types/**/*.ts"
---

# Conflict Game Design Skill

This skill provides context for working on the Conflict remake project. Always consult the design documents in `/mnt/user-data/outputs/` for authoritative details.

## Core Documents

| Document | Purpose |
|----------|---------|
| `docs\conflict-remake-gdd-v2.md` | Complete game design, all systems |
| `docs\conflict-remake-tech-spec.md` | Technical architecture, types |
| `docs\conflict-remake-weapons-detail.md` | 26 weapons with 3D specs |
| `docs\conflict-remake-art-assets.md` | Visual/audio requirements |
| `docs\conflict-remake-research.md` | Original game research |

## Architecture Rules

### Engine Purity (CRITICAL)
All code in `src/engine/` MUST be:
- Pure TypeScript with NO React dependencies
- Pure functions: `(state, action) => newState`
- No side effects, no async operations
- No imports from `src/components/` or `src/screens/`

```typescript
// ✅ CORRECT - Pure engine function
export function calculateDiplomaticShift(
  current: RelationshipLevel,
  action: DiplomaticAction,
  leaderTraits: LeaderTraits
): RelationshipLevel {
  // Pure calculation
}

// ❌ WRONG - React dependency in engine
import { useGameStore } from '../store/gameStore'; // NEVER DO THIS
```

### Data-Driven Design
Game rules live in YAML files, not hardcoded:
- `data/countries.yaml` - Country definitions, borders, starting states
- `data/weapons.yaml` - All 26 weapons with stats, counters
- `data/enums.yaml` - Relationship levels, stability levels, etc.
- `data/combat.yaml` - Combat resolution tables
- `data/leaders.yaml` - Leader personalities and traits

When adding new mechanics, prefer YAML configuration over code changes.

## Game Mechanics Quick Reference

### Relationship Levels (9 total, best → worst)
1. `military_pact` - Can coordinate military actions
2. `profitable` - Trade bonuses
3. `beneficial` - Minor bonuses
4. `favourable` - Neutral positive
5. `satisfactory` - True neutral
6. `cool` - Neutral negative
7. `lamentable` - Trade penalties
8. `hostile` - War possible
9. `war` - Active conflict

### Stability Levels (6 total)
1. `very_solid` - Maximum stability
2. `solid` - Normal operations
3. `good` - Minor concerns
4. `weak` - Extreme measures available
5. `critical` - Collapse imminent
6. `collapse` - Country defeated

### Countries
- **Player:** Israel
- **Neighbors (must defeat):** Egypt, Syria, Jordan, Lebanon
- **Regional:** Iraq, Iran, Libya
- **Superpowers (not directly in game):** USA, USSR

### Win/Lose Conditions
- **Win:** All 4 neighbors reach `collapse` stability
- **Lose:** Israel collapses, nuclear holocaust, impeachment (Knesset ≥10), assassination

### Turn Phases
1. News (AI headlines)
2. Events (if triggered)
3. Diplomatic
4. Intelligence
5. Military (point of no return)
6. End Turn → Resolution

## Combat System

### Weapon Categories
- `infantry` - Basic ground forces
- `light_armor` - M60, Chieftain, AMX-30, T-62
- `main_battle_tank` - M1A1, Challenger, Leclerc, T-72
- `attack_helicopter` - Apache, Lynx, Tiger, Hind
- `sam_battery` - Patriot, Rapier, Crotale, S-300
- `fighter` - F-15, F-16, Mirage 2000, MiG-29
- `sead` - F-4G Wild Weasel, Su-24M

### Combat Resolution (4 Phases)
1. **Air Superiority** - Fighters vs fighters
2. **SEAD** - Suppress enemy SAMs
3. **Close Air Support** - Attack helicopters vs ground
4. **Ground Battle** - Armor vs armor with infantry

### Rock-Paper-Scissors Counters
- SAMs counter aircraft
- SEAD counters SAMs
- Fighters counter SEAD
- Attack helicopters counter armor
- Main battle tanks counter light armor

## TypeScript Conventions

### Type Definitions
```typescript
// Use union types for enums
type CountryId = 'israel' | 'egypt' | 'syria' | 'jordan' | 'lebanon' | 'iraq' | 'iran' | 'libya';
type RelationshipLevel = 'military_pact' | 'profitable' | ... | 'war';

// Use interfaces for state objects
interface CountryState {
  id: CountryId;
  stability: StabilityLevel;
  leader: LeaderState;
  military: MilitaryState;
}
```

### Zustand Store Pattern
```typescript
// Actions are thin wrappers around engine functions
endTurn: async () => {
  const newState = GameEngine.resolveTurn(get().gameState);
  set({ gameState: newState });
}
```

## Common Mistakes to Avoid

1. **Don't hardcode game values** - Put them in YAML
2. **Don't add React to engines** - Keep them pure
3. **Don't skip validation** - Use Zod for AI responses
4. **Don't forget mobile** - Design portrait-first
5. **Don't over-format** - Keep UI minimal, not cluttered

## Testing Requirements

- Unit tests for all engine functions
- Test combat resolution edge cases
- Validate YAML schemas on load
- Mock AI service for deterministic tests
