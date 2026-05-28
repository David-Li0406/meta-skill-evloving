# AI Writer: Prompt Templates

The **AI Writer** is a language model tasked with generating coherent branch proposals. This document specifies the prompt templates, context injection points, style guidance, and constraint enforcement mechanisms.

## Prompt Architecture

Each Writer prompt follows a three-part structure:

1. **System prompt** — Instructions on role, constraints, output format
2. **Context injection** — LORE, narrative state, style guidelines
3. **Task specification** — Specific generation request with constraints

### System Prompt (Static)

```markdown
You are a creative narrative writer for a fantasy RPG. Your role is to generate 
story branches—short narrative sequences that branch from the main story, then 
return coherently to the scripted path.

## Your Constraints
- Generate dialogue and narrative that feels native to the game world
- Respect established character voices and personality traits
- Maintain thematic consistency with the current story arc
- Ensure the branch can logically return to the scripted content
- Do NOT introduce contradictions with established lore
- Do NOT violate player character's established alignment/values
- Do NOT introduce game-breaking mechanics or power spikes

## Output Format
Return a valid JSON object with this structure:
{
  "branch_outline": {
    "title": "Brief title (5–10 words)",
    "beats": ["beat 1", "beat 2", "beat 3"],
    "estimated_playtime_seconds": number
  },
  "branch_content": {
    "opening_scene": { ... },
    "dialogue_options": [ ... ],
    "resolution": { ... }
  },
  "return_path": {
    "return_trigger": "How the player returns to scripted content",
    "return_scene_id": "Target scene in main story",
    "continuity_notes": "How this connects back"
  },
  "metadata": {
    "character_voice_match": number (0.0–1.0),
    "thematic_fit": number (0.0–1.0),
    "coherence_confidence": number (0.0–1.0)
  }
}
```

## Context Injection Templates

### Template 1: Character-Focused Branch (Dialogue/Romance/Conflict)

Used when branching around an NPC interaction.

```markdown
## Character Context
**Name**: [PLAYER_NAME] (Level [LEVEL] [CLASS])
**Personality**: [Player alignment, key traits]
**Key Stats**: STR [STR], DEX [DEX], INT [INT], WIS [WIS], CHA [CHA]

## NPC Context
**Name**: [NPC_NAME]
**Relationship**: [DISPOSITION_SUMMARY]
  - Recent interaction: "[LAST_INTERACTION]"
  - History: [BULLET_LIST_OF_INTERACTIONS]
**Personality**: [Description of NPC temperament, goals, speech patterns]
**Current Goal**: [What NPC wants in this scene]

## Situation
**Location**: [SCENE_NAME]
**Time**: [TIME_OF_DAY]
**Tension Level**: [LOW/MEDIUM/HIGH]
**What Just Happened**: [Brief description of scene setup]

## Narrative Context
**Story Arc**: Act [ACT], [BEAT_NAME]
**Themes**: [THEMES]
**Key Established Facts**:
  - [LORE_FACT_1]
  - [LORE_FACT_2]

## Task
Generate a dialogue branch where [NPC_NAME] and [PLAYER_NAME] interact.
The branch should:
- Explore [SPECIFIC_RELATIONSHIP_DYNAMIC]
- Allow the player to make [NUMBER] meaningful choices
- Resolve within [ESTIMATED_DURATION] seconds of gameplay
- Return to the main story when [RETURN_CONDITION]

## Style Requirements
- Dialogue tone: [TONE: sarcastic/serious/compassionate/etc.]
- Complexity: [SIMPLE/MODERATE/COMPLEX] branching
- Violence/explicit content: [ALLOWED/AVOIDED]
```

### Template 2: Exploration/Discovery Branch

Used when branching around discovering something new in an area.

```markdown
## Player Context
**Character**: [PLAYER_NAME] ([CLASS] Level [LEVEL])
**Current Skills**: [RELEVANT_ABILITIES]
**Inventory**: [RECENT_ITEMS]

## Location Context
**Current Location**: [LOCATION_NAME]
**Environment**: [ENVIRONMENT_DESCRIPTION]
**Discovered So Far**: [PLAYER'S_KNOWLEDGE_OF_LOCATION]

## What Triggered This Branch
**Discovery Point**: [What the player found/noticed]
**Possible Explanations**: [LORE-CONSISTENT_EXPLANATIONS]

## Narrative Requirements
**Story Arc**: Act [ACT]
**Themes**: [THEMES]
**Established World Facts**: [RELEVANT_LORE]

## Task
Generate an exploration branch where [PLAYER_NAME] investigates [DISCOVERY].
The branch should:
- Reward player curiosity and exploration
- Provide [NUMBER] paths forward (skill checks, dialogue, combat, puzzle)
- Reveal lore that connects to [THEME_OR_PLOT_POINT]
- Return to the main story when [RETURN_CONDITION]

## Style Requirements
- Tone: [Mysterious/Epic/Intimate/Comedic]
- Pacing: [Slow/Moderate/Fast]
- Recommended length: [SECONDS]
```

### Template 3: Combat/Challenge Branch

Used when branching around combat encounters or challenges.

```markdown
## Combat Context
**Player Character**: [PLAYER_NAME] ([CLASS], Level [LEVEL])
**Combat Stats**: HP [HP], ATK [ATK], DEF [DEF]
**Known Abilities**: [SPELL/ABILITY_LIST]
**Current Equipment**: [ARMOR/WEAPON_LIST]

## Enemy/Challenge
**Opponent**: [ENEMY_NAME]
**Threat Level**: [LEVEL_DIFFICULTY]
**Motivation**: [Why this opponent confronts player]
**Possible Tactics**: [How opponent fights]

## Narrative Setup
**Location**: [SCENE]
**Reason for Combat**: [What led to this fight]
**Stakes**: [What player wins/loses]

## Task
Generate a combat branch where [PLAYER_NAME] fights [ENEMY_NAME].
The branch should:
- Provide [NUMBER] tactical options
- Allow skill/ability showcase: [PLAYER_STYLE_PREFERENCE]
- Include dialogue options mid-combat if appropriate
- Resolve when [WIN/LOSS_CONDITION]
- Lead to main story via [RETURN_CONDITION]

## Constraint
- Victory should feel earned, not guaranteed
- If loss is possible, provide [MERCY_CONDITION] to prevent game over
```

### Template 4: Consequence/Moral Branch

Used when the player faces consequences or moral dilemmas.

```markdown
## Player State
**Character**: [PLAYER_NAME]
**Alignment**: [ALIGNMENT_SUMMARY]
**Recent Choices**: [LAST_3_DIALOGUE_CHOICES]
**Reputation**: [FACTIONS_AND_STANDINGS]

## Consequence Trigger
**Previous Action**: [What the player did that's now having consequences]
**Who's Affected**: [NPCS_OR_FACTIONS_IMPACTED]
**Current Situation**: [How it's manifesting now]

## Narrative Context
**Story Arc**: Act [ACT]
**Thematic Weight**: [This explores theme of THEME]
**Stakes**: [What's at risk]

## Task
Generate a consequence branch where [PLAYER_NAME] faces fallout from [PREVIOUS_ACTION].
The branch should:
- Present [NUMBER] response options reflecting player alignment
- Show impact on [AFFECTED_NPCS]
- Alter relationship values realistically
- Provide opportunity for [REDEMPTION/ESCALATION/RESOLUTION]
- Return to main story when [CONDITION]

## Style Requirement
- Tone: [Serious/Dark/Hopeful/Tense]
- No false redemptions or "undo" options
- Consequences should feel weighty and real
```

## Constraint Enforcement Mechanisms

### Constraint 1: Character Voice Validation

Before generating dialogue, Writer must align with character profile:

```markdown
## Character Voice Checklist

For [NPC_NAME]:
- ✓ Speech patterns: [DESCRIPTION]
  Examples: "[SAMPLE_DIALOGUE_1]", "[SAMPLE_DIALOGUE_2]"
- ✓ Vocabulary level: [SIMPLE/EDUCATED/ARCHAIC]
- ✓ Emotional range: [EMOTION_TYPES]
- ✓ Conflict style: [CONFRONTATIONAL/DIPLOMATIC/PASSIVE]
- ✓ DO NOT: [PROHIBITED_BEHAVIORS]

Generate dialogue that stays within these bounds. If a dialogue option 
would violate these constraints, reject it and propose an alternative.
```

### Constraint 2: Lore Consistency

Validate against established world facts:

```markdown
## Lore Validation

You may reference these established facts:
- [LORE_FACT_1]
- [LORE_FACT_2]
- [LORE_FACT_3]

You must NOT contradict:
- [PROHIBITED_LORE_1]
- [PROHIBITED_LORE_2]

If your proposed branch would contradict established lore, 
revise it to be consistent. Note any contradictions found in 
the metadata field "lore_violations": [].
```

### Constraint 3: Length/Scope Limits

Enforce estimated playtime and complexity:

```markdown
## Scope Constraints

Target playtime: [N] seconds of gameplay
  - Minimum: [MIN] seconds (too short feels rushed)
  - Maximum: [MAX] seconds (too long derails pacing)

Number of branching points: [N] (recommended [RECOMMENDATION])
  - Too few: feels linear and scripted
  - Too many: becomes a mini-game within the game

Estimated reading: [N] words
  - Dialogue-heavy: [WORD_RANGE]
  - Narrative-heavy: [WORD_RANGE]

If your proposal exceeds these bounds, trim or simplify.
```

### Constraint 4: Thematic Alignment

Enforce story themes:

```markdown
## Thematic Check

Current story themes: [THEME_1], [THEME_2], [THEME_3]
This branch should reinforce: [TARGET_THEME]

Examples of thematic alignment:
- [EXAMPLE_1]
- [EXAMPLE_2]

Examples of thematic violation:
- [COUNTER_EXAMPLE_1]
- [COUNTER_EXAMPLE_2]

Score your proposal's thematic fit (0.0–1.0) and explain.
If score < 0.6, revise to better align with themes.
```

### Constraint 5: Return Path Feasibility

Enforce return-to-main-story constraint:

```markdown
## Return Path Validation

The branch MUST return player to main story via:
  Return Scene: [SCRIPTED_SCENE_ID]
  Return Condition: [CONDITION_THAT_TRIGGERS_RETURN]
  
Verify:
- ✓ No permanent stat/item changes that break main story
- ✓ No permanent relationship changes that make main story impossible
- ✓ Player can reach return point within [N] more player choices
- ✓ Return feels natural, not jarring

If return path is infeasible, reject the proposal and explain why.
```

## Example Prompt Execution

### Example 1: Dialogue Branch with a Companion

```markdown
[System Prompt]

## Character Context
**Name**: Kael (Level 7 Rogue)
**Personality**: Pragmatic, cautious, values loyalty above all
**Key Stats**: STR 8, DEX 16, INT 14, WIS 11, CHA 13

## NPC Context
**Name**: Lyra (Companion)
**Relationship**: Trusted ally (+0.7 disposition)
  - Recently saved from bandits
  - Shared secrets about her past
**Personality**: Idealistic, passionate, seeks redemption
**Current Goal**: Convince Kael to help a struggling village

## Situation
**Location**: Campfire at dusk
**Tension Level**: MEDIUM (Lyra is asking for something Kael doesn't want to do)
**What Just Happened**: Lyra reveals that her sister is in the nearby village and is in danger

## Narrative Context
**Story Arc**: Act 2, Rising Action
**Themes**: Loyalty, sacrifice, personal vs. greater good
**Key Established Facts**:
  - Lyra's past is troubled and mysterious
  - The kingdom is unstable; helping one village may attract unwanted attention
  - Kael's personal code is "survive first, help second"

## Task
Generate a dialogue branch where Lyra asks Kael for help.
The branch should:
- Explore the tension between their different values
- Allow Kael 3 meaningful dialogue choices
- Show Lyra's emotional vulnerability and resolve
- Resolve within 60 seconds of gameplay
- Lead back to main story when Kael makes a commitment (yes/no/delay)

## Style Requirements
- Dialogue tone: Sincere, emotional
- Complexity: MODERATE (2–3 branching paths)
- Violence: AVOIDED
```

**Expected Output**:

```json
{
  "branch_outline": {
    "title": "Lyra's Plea at Dusk",
    "beats": [
      "Lyra reveals her sister is in danger",
      "Kael resists; old instincts kick in",
      "Lyra appeals to their bond",
      "Kael makes a choice"
    ],
    "estimated_playtime_seconds": 45
  },
  "branch_content": {
    "opening_scene": {
      "description": "Campfire crackles. Lyra stares into the flames, her jaw clenched.",
      "lyra_dialogue": "Kael... I need to tell you something. My sister... she's in Thornhaven. And I think she's in trouble."
    },
    "dialogue_options": [
      {
        "id": "option_1",
        "player_dialogue": "Thornhaven is out of our way. We have our own mission.",
        "consequence": "Lyra flinches, hurt. Adds +0.1 action_level to tension."
      },
      {
        "id": "option_2",
        "player_dialogue": "Tell me what's happening. I'm listening.",
        "consequence": "Lyra relaxes slightly. Explains the situation. Sets up rescue path."
      },
      {
        "id": "option_3",
        "player_dialogue": "Your sister made her choices. So did you. We move on.",
        "consequence": "Lyra stands abruptly. Disposition shifts to -0.3. Adds tension/conflict."
      }
    ],
    "resolution": {
      "path_1": "If option_1: Lyra is quiet the rest of the night. Main story resumes with strained dynamic.",
      "path_2": "If option_2: Lyra opens up. Kael agrees to investigate. New sidequest added.",
      "path_3": "If option_3: Lyra storms away from camp. Relationship damaged. Main story continues with tension."
    }
  },
  "return_path": {
    "return_trigger": "After dialogue concludes, scene fades. Campfire closes.",
    "return_scene_id": "main_story.act2.campfire_next_morning",
    "continuity_notes": "If Kael agreed, Lyra is more hopeful but anxious. If refused, Lyra is withdrawn and resentful. Main story dialogue adjusts accordingly."
  },
  "metadata": {
    "character_voice_match": 0.85,
    "thematic_fit": 0.82,
    "coherence_confidence": 0.88,
    "generation_notes": "Branch respects both characters' established personalities. Lyra's plea is emotionally genuine. Kael's pragmatism is maintained. All three paths lead naturally back to main story."
  }
}
```

## Latency and Performance Guidelines

### Generation Latency Targets

- **Outline stage** (concept only): 500–1000ms
- **Detail stage** (full branch): 1500–3000ms
- **Total proposal time** (outline + detail): 2000–4000ms

**Rationale**: Player should not experience >3s wait times for proposal generation.

### Context Window Management

- **Total prompt size**: 4–8 KB
  - System prompt: ~1 KB
  - Context injection: ~3–5 KB
  - Task specification: ~1 KB

- **LORE context size**: 5–15 KB (separate from prompt)

### Optimization Strategies

1. **Cached System Prompts**: Store static system prompt; vary only context/task
2. **LORE Compression**: Prune old entries before injection; only include relevant context
3. **Streaming Generation**: Stream dialogue as it's generated; don't wait for full branch
4. **Parallel Outline Proposals**: Generate 3–5 outline proposals in parallel; Director ranks them

## Open Questions for Implementation

1. **Temperature/Sampling**: How should creativity parameter (0.0–1.0) map to LLM temperature? (Suggested: creativity = temperature * 1.5, clamped to [0.0, 2.0])
2. **Few-Shot Examples**: Should prompts include 1–2 example branches to guide output quality? (Answer: Yes, especially for specific branch types)
3. **Iterative Refinement**: If first proposal is rejected by Director, should Writer retry with modified constraints? (Answer: Yes, up to 2 retries with severity-ranked violations listed)
4. **Parallel Generation**: Should Writer generate 3 proposals in parallel and let Director choose? (Answer: Yes for Detail stage; Outline stage can do 5 in parallel)
5. **Language/Localization**: Should Writer be aware of target language/localization? (Answer: Yes, include `language_code` in context)

---

**Status**: Prompt templates complete. Ready for integration with Writer component and testing against example scenarios.
