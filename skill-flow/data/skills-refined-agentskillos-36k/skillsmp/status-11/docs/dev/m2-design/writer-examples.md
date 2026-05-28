# AI Writer: Generated Proposal Examples

This document provides 5 complete example proposals showing how the AI Writer generates branches across different narrative scenarios. Each example demonstrates prompt → output flow and Writer design principles.

## Schema Relationship: Internal vs. Submission Format

**Important**: The examples in this document show the **internal expanded format** that the AI Writer uses during the Detail stage to fully specify branch structure. This format is richer than the formal `branch-proposal.json` schema because:

1. **Internal format** (shown here): Contains full dialogue trees, continuation paths, consequence mappings, and beat-by-beat structure. Used by the Writer and Director during validation.

2. **Submission format** (`branch-proposal.json`): A flattened representation for storage, API transmission, and audit logging. The `content.text` field contains either:
   - An Ink fragment for direct injection (`branch_type: "ink_fragment"`)
   - A narrative delta for prose additions (`branch_type: "narrative_delta"`)
   - A serialized JSON string of the expanded structure for complex branches (`branch_type: "ink_knot"`)

### Format Mapping

| Internal Format Field | Submission Schema Field |
|-----------------------|-------------------------|
| `id` | `id` |
| `branch_type` | `content.branch_type` (mapped to enum) |
| `title` | Stored in `content.text` metadata |
| `branch_outline.beats` | Serialized into `content.text` |
| `branch_content.*` | Serialized into `content.text` |
| `return_path.return_scene_id` | `content.return_path` |
| `metadata.coherence_confidence` | `metadata.confidence_score` |
| `metadata.character_voice_match` | Used for validation, not stored |
| `metadata.thematic_fit` | Used for validation, not stored |
| `version_info.*` | `metadata.*` fields |

### Conversion Example

The internal format:
```json
{
  "id": "proposal-87f4c290",
  "branch_type": "companion_dialogue",
  "title": "Lyra's Plea at Dusk",
  "branch_outline": { "beats": [...] },
  "branch_content": { "opening_scene": {...}, "dialogue_options": [...] },
  "return_path": { "return_scene_id": "main_story.act2.campfire_next_morning" },
  "metadata": { "coherence_confidence": 0.89 }
}
```

Converts to submission format:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "metadata": {
    "created_at": "2026-01-16T14:30:22Z",
    "llm_model": "gpt-4-turbo",
    "confidence_score": 0.89
  },
  "story_context": { "current_scene": "act2.campfire", ... },
  "content": {
    "branch_type": "ink_knot",
    "text": "{serialized JSON of branch_outline + branch_content}",
    "return_path": "main_story.act2.campfire_next_morning",
    "return_path_confidence": 0.89
  }
}
```

The internal format is used during generation and validation; the submission format is used for storage and API calls.

---

## Example 1: Companion Dialogue Branch (Character-Focused)

### Input Context (LORE Snapshot)

```json
{
  "player": {
    "character": {
      "name": "Kael",
      "race": "Human",
      "class": "Rogue",
      "level": 7,
      "alignment": {"morality": 0.2, "authority": -0.3}
    },
    "relationships": {
      "lyra": {
        "name": "Lyra",
        "disposition": 0.7,
        "history": ["saved from bandits", "shared secrets"],
        "last_interaction_time": "2h ago"
      }
    }
  },
  "game_state": {
    "current_scene": {
      "id": "act2.campfire",
      "name": "Campfire at Dusk",
      "environment": "Forest clearing, stars appearing"
    },
    "world_time": {"hour": 20, "day": 15}
  },
  "narrative_context": {
    "story_arc": {"act": 2, "beat": "rising_action", "progress_percentage": 0.45},
    "themes": ["loyalty", "sacrifice", "personal_vs_greater_good"],
    "established_lore": [
      "The kingdom is unstable",
      "Lyra's past is mysterious",
      "Kael's code is survival first"
    ]
  }
}
```

### Prompt (Simplified)

```markdown
[System Prompt: Standard narrative writer constraints]

## Character Context
**Name**: Kael (Level 7 Rogue)
**Personality**: Pragmatic, cautious, values loyalty above all
**Alignment**: Morally gray (-0.3), chaotic (authority -0.3)

## NPC Context
**Name**: Lyra (Companion)
**Relationship**: Trusted ally (+0.7 disposition)
**Personality**: Idealistic, passionate, seeks redemption
**Current Goal**: Convince Kael to help a struggling village

## Situation
**Location**: Campfire at dusk
**What Just Happened**: Lyra reveals her sister is in danger in Thornhaven

## Task
Generate a dialogue branch where Lyra appeals to Kael for help.
Provide 3 dialogue choices reflecting Kael's pragmatic nature.
Resolve within 60 seconds of gameplay.
Return to main story when Kael makes a commitment.
```

### Generated Proposal Output

```json
{
  "id": "proposal-87f4c290",
  "branch_type": "companion_dialogue",
  "title": "Lyra's Plea at Dusk",
  "branch_outline": {
    "beats": [
      "Lyra reveals her sister is in danger",
      "Kael resists; pragmatism vs. loyalty clash",
      "Lyra appeals to their bond",
      "Kael makes a commitment"
    ],
    "estimated_playtime_seconds": 55
  },
  "branch_content": {
    "opening_scene": {
      "description": "The campfire crackles, casting dancing shadows. Lyra sits across from you, her jaw clenched. She hasn't spoken much since you made camp an hour ago.",
      "npc_action": "Lyra takes a deep breath and locks eyes with you. 'Kael, I need to tell you something. My sister... she's in Thornhaven. And I think she's in trouble.'"
    },
    "dialogue_options": [
      {
        "id": "choice_1",
        "player_text": "Thornhaven is out of our way. We have our own mission.",
        "speaker": "Kael",
        "consequence": {
          "lyra_response": "Lyra flinches as if slapped. Her eyes narrow. 'I see. The mission comes first. As always.'",
          "disposition_change": -0.15,
          "action_level_change": +0.2,
          "path_forward": "continue_to_choice_2"
        },
        "narrative_note": "Kael's pragmatism wins. Lyra is hurt but composed."
      },
      {
        "id": "choice_2",
        "player_text": "Tell me what's happening. I'm listening.",
        "speaker": "Kael",
        "consequence": {
          "lyra_response": "Relief floods Lyra's face. She leans forward, speaking quickly. 'When we left the capital, I heard rumors. Thornhaven's trade post was raided. Slavers, maybe. She was taking work there as a scribe. I... I haven't heard from her in weeks.'",
          "disposition_change": +0.1,
          "action_level_change": 0,
          "path_forward": "continue_to_choice_3"
        },
        "narrative_note": "Kael's loyalty overrides caution. Lyra opens up about her fears."
      },
      {
        "id": "choice_3",
        "player_text": "Your sister made her choices. So did you. We move on.",
        "speaker": "Kael",
        "consequence": {
          "lyra_response": "Lyra stands abruptly, her hand moving to her sword. 'That's cruel, even for you.' She turns away. 'I thought you were different.'",
          "disposition_change": -0.35,
          "action_level_change": +0.4,
          "path_forward": "continue_to_choice_4"
        },
        "narrative_note": "Kael shows his darker side. Lyra is genuinely angry. This damages trust."
      }
    ],
    "continuation_paths": {
      "path_choice_1": {
        "continuation_text": "Lyra stares into the fire. Long moments pass. 'You're right,' she says quietly. 'I knew you'd say that. I just... hoped.' She pauses. 'But I can't ignore this. If you won't help, I'll go alone.'",
        "next_choices": [
          {
            "id": "choice_1a",
            "player_text": "I'm not letting you go alone into slavers' territory.",
            "consequence": "Kael caves to pragmatic concerns. Commits to helping, but frames it as protecting Lyra, not saving her sister. Disposition: +0.2"
          },
          {
            "id": "choice_1b",
            "player_text": "Then go. I'll catch up.",
            "consequence": "Kael maintains his distance but keeps Lyra in sight. Ambiguous commitment. Disposition: -0.05. Main story resumes with subtle tension."
          }
        ]
      },
      "path_choice_2": {
        "continuation_text": "You nod. Lyra tells you everything—the rumors, the lack of contact, her fears. As she speaks, you see the idealist you first met, not the hardened warrior she's become. 'She's my only family,' Lyra whispers. 'I can't lose her. Not without trying.'",
        "next_choices": [
          {
            "id": "choice_2a",
            "player_text": "We can take a detour. Thornhaven is only three days north.",
            "consequence": "Kael commits fully to helping. This opens a sidequest: investigate Thornhaven. Disposition: +0.25. Main story continues with Lyra as motivated ally."
          },
          {
            "id": "choice_2b",
            "player_text": "Let's get more information first. We need to know what we're facing.",
            "consequence": "Kael is supportive but cautious. Opens sidequest with intelligence-gathering phase. Disposition: +0.15. Builds narrative anticipation."
          }
        ]
      },
      "path_choice_3": {
        "continuation_text": "Lyra's hand drops from her sword. 'You know what? Maybe I did trust the wrong person.' She turns back, her eyes hard. 'I'm leaving tomorrow. With or without you. But if you're coming, I'm not waiting.' She walks away from the fire, leaving you alone.",
        "next_choices": [
          {
            "id": "choice_3a",
            "player_text": "Lyra, wait. I was wrong. Let me help.",
            "consequence": "Kael attempts repair. Lyra is guarded but agrees. Disposition: -0.15 (recovery from -0.35, net -0.2). Opens sidequest with strained dynamic. More difficult negotiations with Lyra throughout."
          },
          {
            "id": "choice_3b",
            "player_text": "Let her go. You made your choice.",
            "consequence": "Lyra leaves the party. Major consequence. Sidequest unavailable. Main story continues without her. Significant impact on later plot."
          }
        ]
      }
    }
  },
  "return_path": {
    "return_trigger": "After final dialogue choice, scene fades to black. Campfire closes.",
    "return_scene_id": "main_story.act2.campfire_next_morning",
    "continuity_notes": "If Kael agreed to help: Lyra is more hopeful but anxious. She's awake before dawn, checking supplies. Main story dialogue adjusts—she pushes to move quickly northward. If Kael refused and later apologized: Lyra is professional but distant. She speaks less, avoids eye contact. If Lyra left the party: She's gone. Main story continues with Kael solo or recruiting a different companion later."
  },
  "metadata": {
    "character_voice_match": 0.87,
    "thematic_fit": 0.85,
    "coherence_confidence": 0.89,
    "lore_violations": [],
    "generation_notes": "Branch respects both Kael's pragmatism and Lyra's idealism. Dialogue feels emotionally genuine without being melodramatic. All three initial paths are coherent. Disposition changes are realistic. Return paths integrate naturally with main story. No plot contradictions."
  },
  "version_info": {
    "input_hash": "a2f4c8d1e6b9",
    "llm_seed": 42591847,
    "director_seed": 42591847,
    "director_creativity": 0.65,
    "llm_model": "gpt-4-turbo",
    "llm_version": "2024-01-15",
    "writer_version": "1.0.0",
    "generation_timestamp": "2026-01-16T14:30:22Z"
  }
}
```

---

## Example 2: Combat Encounter Branch

### Input Context (LORE Snapshot)

```json
{
  "player": {
    "character": {
      "name": "Kael",
      "class": "Rogue",
      "level": 7,
      "attributes": {"strength": 10, "dexterity": 16, "constitution": 13}
    },
    "skills": ["backstab", "dodge", "lockpicking"],
    "equipment": {
      "weapon": "Shortsword (enchanted)",
      "armor": "Leather armor"
    }
  },
  "game_state": {
    "current_scene": {
      "id": "cave_ruins",
      "name": "Crumbling Stone Chamber",
      "environment": "Ancient ruins, rubble, narrow passages"
    }
  },
  "narrative_context": {
    "story_arc": {"act": 2, "beat": "rising_action"},
    "themes": ["survival", "legacy"],
    "recent_events": ["Discovered ancient artifact", "Awakened something in ruins"]
  }
}
```

### Generated Proposal Output

```json
{
  "id": "proposal-92f3b4c6",
  "branch_type": "combat_encounter",
  "title": "The Stone Guardian's Challenge",
  "branch_outline": {
    "beats": [
      "Ancient construct awakens",
      "Initial confrontation and assessment",
      "Combat: tactics and skill checks",
      "Victory or mercy option"
    ],
    "estimated_playtime_seconds": 120
  },
  "branch_content": {
    "opening_scene": {
      "description": "The moment your fingers touch the stone pedestal, the chamber trembles. Dust cascades from the ceiling. Then, with a grinding sound that echoes through the ruins, a figure emerges from the far wall—a humanoid construct of stone and ancient magic, its surface glowing with runes that haven't seen light in centuries.",
      "enemy_reveal": "The Stone Guardian, height 8 feet, radiates cold and purpose. Its eyes glow pale blue."
    },
    "combat_setup": {
      "enemy": {
        "name": "Stone Guardian",
        "threat_level": "Moderate (CR 6 for level 7 party)",
        "hp_estimate": 80,
        "attacks": [
          {"name": "Stone Fist", "damage": "2d8+4 bludgeoning", "range": "melee"},
          {"name": "Arcane Pulse", "damage": "2d6 force", "range": "30ft", "aoe": true}
        ],
        "special_abilities": ["Hardened Exterior (reduce damage by 5)", "Slow (ground-based, low mobility)"]
      },
      "environment": {
        "terrain": "Rubble-strewn chamber, narrow passages on sides",
        "tactical_advantages": "Kael can use narrow passages and high ground to avoid direct combat",
        "hazards": "Unstable rubble (3d6 damage if triggered)"
      }
    },
    "combat_options": [
      {
        "id": "combat_1",
        "option": "Direct melee assault",
        "description": "Charge in and use your speed advantage. Guardian is slower.",
        "success_condition": "Kael can get 2–3 rounds of uncontested backstabs before Guardian closes",
        "outcome": "Quick victory if Kael plays to rogue strengths. Combat ends in 4–5 rounds."
      },
      {
        "id": "combat_2",
        "option": "Use environment for evasion",
        "description": "Stay mobile in narrow passages, strike and retreat.",
        "success_condition": "Keep distance, use high ground, make Guardian chase you",
        "outcome": "Longer combat (8–10 rounds), but Kael takes minimal damage. Guardian falls to environment hazard."
      },
      {
        "id": "combat_3",
        "option": "Attempt to disable/disarm",
        "description": "Target the runes on Guardian's body to disable abilities.",
        "success_condition": "Intelligence check (DC 15) to identify vulnerable runes; Dexterity check (DC 14) to strike accurately",
        "outcome": "If successful, Guardian loses Hardened Exterior. If failed, Guardian becomes enraged (+2 damage). Combat becomes high-risk/high-reward."
      }
    ],
    "dialogue_during_combat": [
      {
        "trigger": "After first round of combat",
        "guardian_speech": "A voice, ancient and grinding like stone on stone, echoes from the construct. 'An intruder. The seal is broken. You have awakened something that should have slept.'",
        "player_options": [
          {"text": "I'm not here to fight you.", "effect": "Guardian pauses; rolls Wisdom save (DC 15). If succeed, becomes willing to negotiate. If fail, attacks with renewed fury."},
          {"text": "Then show me what you're defending.", "effect": "Guardian respects the boldness. Grants one free round to move/prepare before attacking."},
          {"text": "[Attack] No more talking!", "effect": "Combat continues without pause. No special effect."}
        ]
      }
    ],
    "victory_scenarios": [
      {
        "scenario": "Kael defeats Guardian (HP reaches 0)",
        "outcome": "Guardian collapses into dust. Runes fade. Chamber falls silent.",
        "discovery": "A stone tablet is revealed beneath the Guardian's position. Contains lore about the artifact's purpose.",
        "rewards": "XP (450), unique loot: 'Guardian's Amulet' (increases DEX by +1)"
      }
    ],
    "mercy_scenario": {
      "trigger": "Guardian HP < 25% AND Kael hasn't killed any construct allies",
      "option": "Offer a truce or allow the Guardian to stand down",
      "outcome": "Guardian ceases combat. Recognizes Kael as 'one who respects the old ways.' Allows access to inner chamber.",
      "consequence": "No loot, but unlocks unique dialogue with Guardian. Artifact is revealed non-violently. Stronger narrative resolution."
    }
  },
  "return_path": {
    "return_trigger": "After Guardian is defeated (or truce is made), the chamber stabilizes and main story resumes.",
    "return_scene_id": "main_story.act2.artifact_chamber",
    "continuity_notes": "If Kael showed mercy: Guardian becomes a recurring NPC with useful knowledge. Can be recruited later. If Kael killed Guardian: Artifact is taken, but a new threat emerges (the Guardian's death alerts nearby enemies). Main story continues with increased urgency."
  },
  "metadata": {
    "character_voice_match": 0.92,
    "thematic_fit": 0.88,
    "coherence_confidence": 0.91,
    "combat_balance": "Tuned for level 7 solo Rogue. Victory is achievable but not trivial. Reward is meaningful.",
    "lore_violations": [],
    "generation_notes": "Combat encounter respects Rogue abilities (stealth, evasion, precision damage). Environment offers tactical options beyond 'hit enemy.' Dialogue with Guardian adds narrative depth. Mercy option provides meaningful choice beyond combat optimization."
  },
  "version_info": {
    "input_hash": "c7e2a9d5f1b8",
    "llm_seed": 28374019,
    "director_creativity": 0.55,
    "llm_model": "gpt-4-turbo",
    "generation_timestamp": "2026-01-16T14:31:45Z"
  }
}
```

---

## Example 3: Moral Consequence Branch

### Generated Proposal Output (Simplified)

```json
{
  "id": "proposal-73c8a2e9",
  "branch_type": "moral_consequence",
  "title": "The Merchant's Widow",
  "branch_outline": {
    "beats": [
      "Kael encounters victim of his past theft",
      "Moment of recognition and guilt",
      "Choice: flee, make amends, or double down on cruelty",
      "Consequence unfolds"
    ],
    "estimated_playtime_seconds": 90
  },
  "summary": "Kael robbed a merchant three weeks ago (established lore). Now the merchant is dead, and his widow blames Kael. This branch explores whether Kael has a conscience.",
  "metadata": {
    "thematic_fit": 0.87,
    "coherence_confidence": 0.85,
    "character_voice_match": 0.83,
    "lore_violations": []
  },
  "version_info": {
    "director_creativity": 0.45
  }
}
```

---

## Example 4: Discovery/Exploration Branch

### Generated Proposal Output (Simplified)

```json
{
  "id": "proposal-51e6b3d4",
  "branch_type": "exploration_discovery",
  "title": "The Hidden Shrine",
  "branch_outline": {
    "beats": [
      "Kael finds a hidden door behind collapsed rubble",
      "Shrine to forgotten goddess revealed",
      "Puzzle or offering required to proceed",
      "Discovery of ancient lore relevant to main quest"
    ],
    "estimated_playtime_seconds": 75
  },
  "summary": "Rewarding player curiosity with lore and optional treasure. Connects to established themes of 'legacy' and 'forgotten magic.'",
  "metadata": {
    "thematic_fit": 0.91,
    "coherence_confidence": 0.89,
    "lore_violations": []
  }
}
```

---

## Example 5: Failure/Mercy Path

### Generated Proposal Output (Simplified)

```json
{
  "id": "proposal-84f2c7b1",
  "branch_type": "failure_mercy",
  "title": "The Bandit's Offer",
  "branch_outline": {
    "beats": [
      "Kael is cornered by bandits (potentially losing combat)",
      "Bandit leader offers mercy: work for them or die",
      "Kael can negotiate, escape, or surrender",
      "Non-lethal resolution or partnership formed"
    ],
    "estimated_playtime_seconds": 60
  },
  "summary": "Instead of death, Kael gets a mercy option. Opens sidequest to work off debt or double-cross bandits later.",
  "metadata": {
    "thematic_fit": 0.80,
    "coherence_confidence": 0.84,
    "lore_violations": []
  }
}
```

---

## Generation Quality Metrics

### Across All Examples

| Metric | Target | Example 1 | Example 2 | Example 3 | Example 4 | Example 5 |
|--------|--------|-----------|-----------|-----------|-----------|-----------|
| **Coherence Confidence** | >0.80 | 0.89 | 0.91 | 0.85 | 0.89 | 0.84 |
| **Character Voice Match** | >0.80 | 0.87 | 0.92 | 0.83 | 0.85 | 0.88 |
| **Thematic Fit** | >0.80 | 0.85 | 0.88 | 0.87 | 0.91 | 0.80 |
| **Lore Violations** | 0 | 0 | 0 | 0 | 0 | 0 |
| **Return Path Quality** | Clear | ✓ | ✓ | ✓ | ✓ | ✓ |

### Key Observations

1. **Dialogue examples** (Ex. 1) achieve highest character voice match due to specific NPC personality guidance
2. **Combat examples** (Ex. 2) show strong coherence and thematic fit when mechanics are specified
3. **Moral examples** (Ex. 3) lower on character voice match (harder to balance cruelty with player agency)
4. **Exploration examples** (Ex. 4) highest thematic fit (pure narrative-driven)
5. **All examples** have zero lore violations (validation pipeline working)

## Generalization Patterns

These 5 examples show Writer's ability to:

- ✓ Generate emotionally coherent dialogue
- ✓ Balance multiple dialogue paths
- ✓ Create mechanically sound combat encounters
- ✓ Respect character voice and personality
- ✓ Maintain thematic consistency
- ✓ Design return paths that integrate with main story
- ✓ Provide multiple player agency options
- ✓ Scale complexity based on director_creativity parameter

## Expected Latency

- **Outline generation** (3–5 parallel): 800ms
- **Detail generation** (single): 2200ms
- **Total proposal time**: ~3000ms (3 seconds)

This is acceptable for: pre-generated pools, background generation, offline generation during cutscenes.

---

**Status**: Example proposals demonstrate Writer's capability across multiple branch types. Ready for integration testing with runtime and Director.
