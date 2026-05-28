# AI Writer: LORE Data Model

The **LORE (Living Observed Runtime Experience)** model provides the AI Writer with contextual information about the current game state, player behavior, and narrative progression. This enables coherent, contextually-aware branch generation.

## Overview

LORE is collected at runtime from multiple sources:
- **Player state**: character attributes, inventory, relationships, progress
- **Game state**: scene, time of day, location, active quests, completed milestones
- **Narrative state**: story themes, pacing, character arcs, established lore
- **Player behavior**: recent actions, choices, dialogue preferences, engagement signals

The AI Writer injects LORE into prompts to generate proposals that feel native to the current game context.

## LORE Data Model Specification

### 1. Player State

```yaml
player:
  character:
    name: string                          # Player character name
    race: string                          # Species/ethnicity
    class: string                         # Character class (Warrior, Mage, Rogue, etc.)
    level: int                            # Current experience level
    alignment: {
      morality: [-1.0, 1.0]              # -1.0 evil → 1.0 good
      authority: [-1.0, 1.0]             # -1.0 chaotic → 1.0 lawful
    }
  
  attributes:
    strength: int                         # Physical power
    dexterity: int                        # Agility and reflexes
    constitution: int                     # Health and resilience
    intelligence: int                     # Reasoning and knowledge
    wisdom: int                           # Perception and insight
    charisma: int                         # Social influence
  
  relationships: {
    character_id: {
      name: string                        # NPC name
      disposition: [-1.0, 1.0]           # -1.0 hostile → 1.0 allied
      history: [string]                  # Brief interaction history ("saved from bandits", "stole from")
      last_interaction_time: timestamp    # When player last encountered this NPC
    }
  }
  
  inventory:
    items: [
      {
        name: string                      # Item name
        type: string                      # weapon, armor, potion, key, etc.
        rarity: string                    # common, uncommon, rare, legendary
        acquired_at: timestamp            # When obtained
      }
    ]
  
  progression:
    completed_quests: [string]            # Quest IDs
    active_quests: [string]               # Current quest IDs
    discovered_locations: [string]        # Visited places
    learned_spells: [string]              # Unlocked abilities
    achievements: [string]                # Major milestones
```

### 2. Game State

```yaml
game_state:
  current_scene:
    id: string                            # Unique scene identifier
    name: string                          # Human-readable scene name
    location: string                      # Where the scene takes place
    environment: string                   # Environment description
    npcs_present: [string]                # Character IDs in this scene
    objects: [string]                     # Interactive objects or props
  
  world_time:
    hour: int                             # 0–23
    day: int                              # In-game day count
    season: string                        # Spring, Summer, Fall, Winter
    weather: string                       # Clear, Rainy, Stormy, etc.
  
  active_state:
    player_mood: string                   # Calm, Tense, Excited, Fearful, etc.
    recent_events: [string]               # Last 3–5 major events that just happened
    last_player_action: string            # Description of what player just did
    dialogue_mode: boolean                # Is player in conversation?
    combat_active: boolean                # Is combat happening?
```

### 3. Narrative State

```yaml
narrative_context:
  story_arc:
    act: int                              # 1, 2, 3 (three-act structure)
    beat: string                          # Inciting incident, rising action, climax, resolution, etc.
    progress_percentage: float            # 0.0–1.0 estimate of story completion
  
  themes:
    primary: [string]                     # ["redemption", "betrayal", "power"]
    secondary: [string]                   # Supporting themes
    current_tone: string                  # Dark, whimsical, epic, intimate, comedic
  
  character_arcs:
    main_character: {
      arc_name: string                    # e.g., "Journey of Redemption"
      current_stage: string               # e.g., "internal conflict", "confrontation"
      established_traits: [string]        # Character flaws, strengths
    }
    antagonist: {
      arc_name: string
      current_stage: string
      relationship_to_player: string      # "unknown", "rival", "nemesis"
    }
  
  established_lore: [string]              # Key facts established so far
                                          # e.g., "The kingdom is under siege",
                                          #      "Magic has been forbidden for 100 years"
  
  player_choices_history: [
    {
      choice_text: string                 # What player chose
      consequence: string                 # What happened as a result
      timestamp: timestamp
    }
  ]
  
  pacing_state:
    action_level: float                   # 0.0 calm → 1.0 intense action
    emotional_stakes: float               # 0.0 low → 1.0 high emotional investment
    mystery_level: float                  # 0.0 clear → 1.0 mysterious/unknown
```

### 4. Player Behavior & Engagement

```yaml
player_behavior:
  play_style:
    aggression: float                     # 0.0 avoids combat → 1.0 seeks combat
    dialogue_preference: string           # terse, conversational, verbose
    exploration: float                    # 0.0 follows main path → 1.0 explores everything
    moral_tendency: float                 # -1.0 chaotic → 1.0 principled
  
  engagement_signals:
    recent_session_length: float          # Minutes in current session
    sessions_played: int                  # Total sessions
    save_frequency: float                 # Saves per hour
    reload_frequency: float               # Reloads per hour (higher = more deliberate)
    choice_deliberation: float            # Average seconds spent on choices
  
  dialogue_metrics:
    preferred_dialogue_tone: string       # sarcastic, serious, compassionate, pragmatic
    dialogue_choices_made: [string]       # History of dialogue branches taken
    interrupted_conversations: int       # How many times player skipped dialogue
  
  recent_actions: [
    {
      action: string                      # Brief description
      timestamp: timestamp
      category: string                    # combat, dialogue, exploration, crafting, etc.
    }
  ]
```

## LORE Capture Strategy

### Real-Time Capture Points

LORE is captured at key moments:

1. **Scene transitions** (player enters new location)
   - Update game_state.current_scene
   - Update world_time
   - Snapshot active NPCs

2. **Major choices** (player makes dialogue or quest decision)
   - Record choice in narrative_context.player_choices_history
   - Update relationships based on choice consequences
   - Update narrative progression

3. **Quest updates** (completed or advanced)
   - Update player.progression
   - Update narrative_context.established_lore
   - Trigger pacing recalculation

4. **Combat/tension events**
   - Update pacing_state.action_level
   - Update player_mood
   - Record recent_events

5. **Relationship changes** (NPC disposition shift)
   - Update player.relationships[character_id].disposition
   - Record history entry
   - Note timestamp

### Auto-Population Sources

Some LORE fields are auto-populated from game state:

- **player.attributes** ← character sheet
- **player.inventory.items** ← inventory system
- **game_state.current_scene** ← scene manager
- **game_state.world_time** ← time-of-day system
- **player.progression.completed_quests** ← quest log
- **narrative_context.story_arc.progress_percentage** ← auto-calculated from milestone achievements

### Manual Annotation Points

Some fields require designer/author input:

- **narrative_context.themes** — Designer specifies story themes during level/chapter design
- **narrative_context.character_arcs** — Narrative designers map character progression
- **narrative_context.established_lore** — Story designers record key lore that has been revealed
- **pacing_state** — Can be inferred from recent events OR explicitly set by pacing triggers in dialogue/cutscenes

### Fallback Defaults

If a LORE field is missing at generation time:

```yaml
fallback_defaults:
  missing_relationships: {}              # Assume neutral (0.0 disposition)
  missing_attributes: 10                 # Default ability score
  missing_dialogue_history: []           # Treat as first meeting
  missing_pacing_state: { action_level: 0.5, emotional_stakes: 0.5, mystery_level: 0.5 }
  missing_themes: ["adventure", "discovery"]
```

## LORE Representation in Prompts

When injecting LORE into Writer prompts, format as structured context blocks:

```markdown
## Character Context
**Name**: [player.character.name] (Level [player.character.level] [player.character.class])
**Alignment**: [alignment summary]
**Recent Inventory**: [last 3 items acquired]

## Current Situation
**Location**: [game_state.current_scene.name]
**NPCs Present**: [names of characters in scene]
**Recent Events**: [bullet list of last 2–3 events]

## Narrative Progress
**Story Arc**: Act [narrative_context.story_arc.act], [beat name]
**Themes**: [primary themes]
**Key Established Facts**: [bullet list of lore]

## Player Style
**Play Style**: [aggression, dialogue preference, exploration level]
**Recent Choices**: [last 2–3 dialogue choices made]
```

## LORE Context Hash

For **reproducibility and determinism**, compute a hash of the LORE context:

```python
def compute_lore_hash(lore: dict) -> str:
    """Hash the LORE context for determinism tracking."""
    # Include only deterministic fields (not timestamps)
    hashable = {
        'character_id': lore['player']['character']['name'],
        'scene_id': lore['game_state']['current_scene']['id'],
        'narrative_arc': lore['narrative_context']['story_arc'],
        'player_alignment': lore['player']['alignment'],
        'relationships': sorted([(k, v['disposition']) 
                                 for k, v in lore['player']['relationships'].items()]),
        'progression': lore['player']['progression'],
        'established_lore': sorted(lore['narrative_context']['established_lore']),
    }
    return hashlib.sha256(json.dumps(hashable, sort_keys=True).encode()).hexdigest()
```

This hash is included in the proposal metadata as `context_hash` for audit and reproducibility.

## Size and Complexity Guidelines

### Recommended LORE Size

- **Total LORE JSON**: 5–15 KB (after compression)
- **Relationships object**: ≤ 50 NPCs tracked
- **Inventory items**: ≤ 50 items
- **Player choices history**: Last 20–30 choices
- **Recent events**: Last 5–10 major events
- **Established lore**: 10–30 key facts

**Rationale**: Fits comfortably in LLM context windows while providing rich detail. Older/less-relevant entries pruned at capture time.

### Pruning Strategy

Over time, LORE grows stale. Prune periodically:

- **Relationships**: Keep recent interactions (last 5 hours playtime), prune ancient history
- **Inventory**: Remove items long sold/dropped
- **Choices history**: Keep last 30 choices, archive older decisions
- **Events**: Keep recent events (last 30 minutes playtime)
- **Lore**: Keep active lore, archive obsolete facts

## Integration with Branch Proposal Schema

The `Branch Proposal` includes LORE snapshot in its `story_context` field:

```json
{
  "id": "branch-uuid",
  "story_context": {
    "lore": { /* full LORE model */ },
    "lore_hash": "sha256hash",
    "lore_capture_timestamp": "2026-01-16T14:30:00Z"
  }
}
```

This allows:
1. **Reproducibility**: Same LORE → same proposal (with same seed)
2. **Audit trail**: Track what context was available when proposal was generated
3. **Post-analysis**: Understand why a proposal was coherent or incoherent

## Open Questions for Implementation

1. **LORE Capture Frequency**: Should LORE be captured continuously or only at proposal-generation time? (Answer: Continuous, then snapshotted at generation)
2. **NPC Memory Limit**: How many NPCs should be tracked? Should distant/forgotten characters be pruned? (Answer: 50 active, prune by recency)
3. **Time Weighting**: Should recent events be weighted more heavily in prompts? (Answer: Yes, recency bias helps)
4. **Player Behavior Inference**: Should play style be explicitly annotated or inferred from behavior? (Answer: Hybrid — infer from behavior, allow designer override)
5. **Thematic Consistency Scoring**: How to measure if a branch matches established themes? (Answer: Director's risk-scoring metric)

---

**Status**: Design complete. Ready for implementation phase.
