# Branch Proposal Lifecycle

## Overview

The **branch proposal lifecycle** defines the multi-stage process from initial concept to runtime execution. This document clarifies the states, transitions, and decision points a proposal goes through from conception to player experience.

---

## Proposal States & Lifecycle

```
[1] OUTLINE STAGE
    ↓
    Outline created (mini Save-the-Cat structure)
    Director reviews outline (coherence, thematic fit, return path feasibility)
    ↓
    ├─ REJECTED (incoherent, off-theme, no viable return)
    └─ APPROVED_FOR_DETAIL
    
[2] DETAIL STAGE (if approved)
    ↓
    Full Save-the-Cat definition developed
    Validation pipeline runs (policy checks, sanitization)
    Director reviews detailed proposal (risk scoring, final approval)
    ↓
    ├─ REJECTED (policy violation, coherence issues)
    ├─ APPROVED_WITH_SANITIZATION (passed with transformations applied)
    └─ APPROVED_CLEAN (passed all checks cleanly)
    
[3] PLACEMENT STAGE (if approved)
    ↓
    Director identifies narrative insertion points in authored script
    (scene boundaries, choice points where branch can be offered)
    Director maps return path from branch ending back to scripted content
    ↓
    ├─ PLACEMENT_FAILED (cannot find viable insertion points)
    └─ READY_FOR_RUNTIME
    
[4] RUNTIME STAGE (if placement successful)
    ↓
    Player encounters choice point and follows the branch
    AI Writer dynamically generates interactions/dialogue following Save-the-Cat beats
    Interactions sanitized in real-time before display to player
    ↓
    ├─ ACTIVE (currently executing)
    └─ COMPLETED (player reached end of branch; returned to scripted content)
    
[5] TERMINAL STATES
    ├─ ARCHIVED (proposal passed all stages, executed successfully)
    ├─ REVERTED (branch caused issues; player reverted to last checkpoint)
    └─ DEPRECATED (proposal disabled/superseded by newer version)
```

---

## Stage 1: Outline (High-Level Concept)

### Purpose
Rapidly evaluate branch feasibility before investing effort in full development.

### Input
- Current scene and player state
- Recent story events and player actions
- Story themes and character profiles
- Director's creativity parameter (0.0–1.0)

### Outline Structure (Save-the-Cat Simplified)
```
{
  "proposal_id": "outline-550e8400-...",
  "type": "outline",
  "story_context": { ... },
  
  "outline": {
    "hook": "Brief setup/inciting incident (1–2 sentences)",
    "rising_action": "Conflict/complication (1–2 sentences)",
    "climax": "Key decision point (1 sentence)",
    "resolution": "Outcome/consequence (1–2 sentences)",
    "return_path_hint": "Expected return to scripted content (e.g., 'chapter_2.after_choice')"
  },
  
  "metadata": {
    "created_at": "2026-01-16T10:45:00Z",
    "confidence_score": 0.85,
    "estimated_scenes": 2,
    "themes_covered": ["redemption", "choice"],
    "estimated_length": "3–5 player choices"
  }
}
```

### Director's Outline Review
**Evaluation criteria**:
1. **Thematic fit**: Does outline align with story themes?
2. **LORE coherence**: Is it consistent with established facts?
3. **Return path viability**: Can we plausibly return to scripted content?
4. **Character voice**: Do character arcs make sense?
5. **Narrative pacing**: Appropriate for current story phase?

**Decision outcomes**:
- **REJECTED**: Outline fails coherence check → Discard (no further work)
- **APPROVED_FOR_DETAIL**: Outline passes → Proceed to full development

### Rejection Examples
- "Outline contradicts LORE: compass creation date is wrong"
- "No viable return path: outline ends in a dead-end"
- "Off-theme: outline emphasizes violence, but story theme is redemption"

---

## Stage 2: Detail (Full Save-the-Cat Definition)

### Purpose
Develop complete branch content with all story beats, dialogue, and mechanics fully specified.

### Input
- Approved outline from Stage 1
- Expanded story context (inventory, character states, emotional beats)
- Character voice samples and dialogue guidelines
- Ink runtime constraints

### Full Save-the-Cat Definition
```
{
  "proposal_id": "detail-550e8400-...",
  "type": "detail",
  "outline_id": "outline-550e8400-...",
  "story_context": { ... },
  
  "full_structure": {
    "setup": {
      "scene": "Current scene name",
      "narrative": "Detailed setup prose (100–150 tokens)",
      "player_choice": "What choice triggers this branch"
    },
    
    "beat_1_hook": {
      "narrative": "Inciting incident narrative (80–120 tokens)",
      "character_voice": "Which character speaks",
      "emotional_beat": "fear, curiosity, determination",
      "ink_tags": ["dialogue", "revelation"]
    },
    
    "beat_2_rising_action": {
      "narrative": "Complication/conflict (100–150 tokens)",
      "choice_point": "Optional: does player get a choice here?",
      "emotional_beat": "tension, doubt, resolve"
    },
    
    "beat_3_climax": {
      "narrative": "Key decision/confrontation (60–100 tokens)",
      "character_voice": "protagonist's internal monologue or dialogue",
      "emotional_beat": "peak tension, vulnerability",
      "choice_point": "Player makes critical choice (required)"
    },
    
    "beat_4_resolution": {
      "narrative": "Consequence/outcome (80–120 tokens)",
      "emotional_beat": "relief, realization, acceptance",
      "character_arcs_affected": ["guard_captain (relationship +1)", "player (morale +0.1)"]
    },
    
    "return_path": {
      "target_scene": "chapter_2.after_choice",
      "bridging_narrative": "How to smoothly transition from branch end to scripted content",
      "player_state_changes": ["inventory.add('guard_trust')", "reputation.shift('trusted')"],
      "estimated_scenes_in_branch": 3,
      "estimated_choices_before_return": 2
    }
  },
  
  "metadata": {
    "created_at": "2026-01-16T10:50:00Z",
    "confidence_score": 0.88,
    "total_tokens_static": 650,
    "total_tokens_dynamic": "estimated 150–200 per player interaction",
    "estimated_playtime": "2–3 minutes"
  }
}
```

### Validation Pipeline (Stage 2a)
**Rules applied**:
- Profanity filter, explicit content filter, hate speech detector
- LORE consistency check
- Character voice consistency
- Theme consistency check
- Narrative pacing check
- Ink syntax validation (if Ink fragments are included)
- Length limit check
- Return-path reachability check

**Outcomes**:
- **REJECTED**: Critical policy violation (e.g., profanity) → Stop
- **APPROVED_WITH_SANITIZATION**: Policy violation but sanitizable → Apply transforms, proceed with caution
- **APPROVED_CLEAN**: No violations → Proceed

### Director's Detailed Review (Stage 2b)
**Decision logic**:
1. If validation REJECTED → Return to Stage 1 (outline revision)
2. If validation APPROVED → Run Director risk scoring:
   - Thematic consistency risk
   - LORE adherence risk
   - Character voice risk
   - Narrative pacing risk
   - Player preference risk (will player enjoy this branch?)
   - Return-path coherence risk
3. If aggregate risk > THRESHOLD → REJECTED
4. If aggregate risk ≤ THRESHOLD → APPROVED (proceed to Stage 3)

**Decision outcomes**:
- **REJECTED**: Risk score too high → Discard or request revision
- **APPROVED_WITH_SANITIZATION**: Passed, but some content was sanitized → Mark for monitoring
- **APPROVED_CLEAN**: Passed all checks cleanly → Proceed to placement

---

## Stage 3: Placement (Integration Point Identification)

### Purpose
Identify where in the authored narrative this branch should be offered to players.

### Director's Placement Algorithm
```
def find_placement_points(proposal, story_script, player_state):
    """
    Find choice points in authored script where this branch can be inserted.
    Criteria:
    1. Choice point must occur BEFORE the return_path
    2. Branch must lead to return_path within N scenes
    3. Branch thematic context must match scene context
    4. Player must have prerequisite items/state for branch to make sense
    """
    
    placement_candidates = []
    
    # Scan authored script for choice points
    for choice_point in story_script.all_choice_points():
        # [1] Is this choice point before return path?
        if not can_reach(choice_point, proposal.return_path, story_script):
            continue
        
        # [2] Does player have prerequisites?
        if not player_has_prerequisites(player_state, choice_point):
            continue
        
        # [3] Is thematic context aligned?
        thematic_distance = compute_thematic_distance(
            choice_point.scene_theme,
            proposal.themes
        )
        if thematic_distance > THRESHOLD:
            continue
        
        # [4] Can we smoothly bridge to return path?
        bridge_score = assess_bridge_quality(
            proposal.resolution,
            story_script.scene(proposal.return_path)
        )
        if bridge_score < 0.5:
            continue
        
        # Candidate is viable
        placement_candidates.append({
            "choice_point": choice_point,
            "thematic_distance": thematic_distance,
            "bridge_score": bridge_score,
            "confidence": bridge_score * (1 - thematic_distance)
        })
    
    # Sort by confidence and return top N
    return sorted(placement_candidates, key=lambda x: x['confidence'], reverse=True)[:3]
```

### Placement Result
```
{
  "proposal_id": "detail-550e8400-...",
  "placement_status": "PLACEMENT_SUCCESSFUL",
  
  "placement_points": [
    {
      "offer_point": "chapter_2.guard_confrontation_choice",
      "choice_text": "Confront the guard directly",
      "confidence": 0.92,
      "rationale": "Player has 'grandfather_compass'; guard has 'suspicious' mood; theme matches"
    },
    {
      "offer_point": "chapter_2.tavern_choice_alt",
      "choice_text": "Question the innkeeper about the compass",
      "confidence": 0.78,
      "rationale": "Alternative placement if first choice is too early"
    }
  ],
  
  "return_path_mapping": {
    "from": "proposal.resolution",
    "to": "chapter_2.after_confrontation",
    "bridging_narrative": "The guard, now understanding your bloodline, steps aside with newfound respect. You proceed into the fortress, your compass warm in your pocket.",
    "narrative_coherence_score": 0.89
  },
  
  "player_state_adjustments": [
    "inventory.add('guard_trust')",
    "relationships.guard_captain.mood = 'respectful'",
    "reputation.add_trust(0.15)"
  ],
  
  "ready_for_runtime": true
}
```

### Placement Failure Handling

When placement fails, the Director evaluates whether the branch is still relevant to the current story state:

#### Decision Flow for PLACEMENT_FAILED
```
PLACEMENT_FAILED
    ↓
Director checks: Is branch still relevant to current story position?
    ↓
    ├─ YES (story hasn't progressed past branch context)
    │   → RETRY_PLACEMENT
    │   → Return to Placement Stage with adjusted parameters
    │   → May adjust return_path or relax thematic constraints
    │
    └─ NO (story has progressed; branch context is stale)
        → DEFERRED_FOR_REUSE
        → Flag proposal for potential reuse in future playthroughs
        → Reject for current run
```

#### Path 1: RETRY_PLACEMENT (Branch Still Relevant)

If the story hasn't progressed past the branch's context, the proposal can be retried:

```json
{
  "proposal_id": "detail-550e8400-...",
  "placement_status": "PLACEMENT_FAILED",
  "relevance_check": "STILL_RELEVANT",
  "decision": "RETRY_PLACEMENT",
  
  "failure_reason": "No viable insertion points with current return_path",
  "retry_strategy": {
    "action": "adjust_return_path",
    "original_return_path": "chapter_2.after_confrontation",
    "suggested_return_paths": [
      "chapter_2.guard_post_exit",
      "chapter_2.courtyard_entrance"
    ],
    "relaxations_applied": [
      "thematic_distance_threshold: 0.3 → 0.4",
      "bridge_score_minimum: 0.5 → 0.4"
    ]
  },
  
  "retry_count": 1,
  "max_retries": 3,
  "next_action": "re_run_placement_algorithm"
}
```

**Retry limits**: Maximum 3 placement retries before escalating to DEFERRED_FOR_REUSE.

#### Path 2: DEFERRED_FOR_REUSE (Branch No Longer Relevant)

If the story has progressed past the branch's context (e.g., player is now in chapter 3, but branch requires chapter 2 context), the proposal is flagged for future reuse:

```json
{
  "proposal_id": "detail-550e8400-...",
  "placement_status": "PLACEMENT_FAILED",
  "relevance_check": "NO_LONGER_RELEVANT",
  "decision": "DEFERRED_FOR_REUSE",
  
  "failure_reason": "Story has progressed past branch context. Player is now in chapter_3; branch requires chapter_2 scene state.",
  
  "current_story_position": "chapter_3.temple_entrance",
  "branch_required_position": "chapter_2.guard_encounter",
  
  "reuse_metadata": {
    "reuse_eligible": true,
    "applicable_story_phases": ["chapter_2"],
    "required_player_state": {
      "has_item": "grandfather_compass",
      "reputation_range": ["neutral", "wary_outsider"]
    },
    "themes": ["redemption", "family_legacy"],
    "quality_score": 0.88
  },
  
  "storage_action": "archive_for_future_runs",
  "current_run_status": "REJECTED"
}
```

**Reuse pool**: Deferred proposals are stored in a reuse pool, indexed by:
- Applicable story phases/chapters
- Required player state prerequisites
- Thematic tags
- Quality score

When a new playthrough reaches a matching context, the Director can retrieve and re-attempt placement for these proposals.

### Placement Failure Telemetry

```json
{
  "event_type": "placement_failed",
  "proposal_id": "detail-550e8400-...",
  "timestamp": "2026-01-16T11:00:00Z",
  "failure_reason": "story_progression_mismatch",
  "relevance_status": "no_longer_relevant",
  "decision": "deferred_for_reuse",
  "current_story_position": "chapter_3.temple_entrance",
  "branch_context": "chapter_2.guard_encounter",
  "reuse_eligible": true
}
```

```json
{
  "event_type": "placement_retry",
  "proposal_id": "detail-550e8400-...",
  "timestamp": "2026-01-16T11:00:05Z",
  "retry_count": 2,
  "adjustments_applied": ["relaxed_thematic_threshold", "alternative_return_path"],
  "outcome": "placement_successful"
}
```

---

## Stage 4: Runtime (Execution)

### Purpose
Execute the approved branch in response to player choice, with dynamic content generation.

### Runtime Flow
```
[Player approaches a choice point in the story]
    ↓
Director checks if any READY_FOR_RUNTIME branches apply:
- Is player in a scene where a branch can be offered?
- Does player meet prerequisites (inventory, state, relationships)?
- Is the return path still reachable from here?
    ↓
If checks pass: PRESENT BRANCH as a choice option
    ↓
[Player sees choice: branch option OR continue main story]
    ↓
    ├─ Player chooses main story → Branch remains READY_FOR_RUNTIME (may be offered later)
    └─ Player chooses branch → ACTIVATE BRANCH
        ↓
    [Beat 1: Hook]
        ↓
    AI Writer generates dynamic interaction/dialogue
        (Uses Save-the-Cat beat as structure)
        ↓
    Sanitize content in real-time
        (Run policy filters on generated text)
        ↓
    Display to player
        ↓
    [Player can make choices within the branch OR skip]
        ↓
    [Beats 2, 3, 4: Rising Action, Climax, Resolution]
        ↓
    (Same dynamic generation, sanitization, display loop)
        ↓
    [Branch reaches resolution]
        ↓
    Apply player state changes (inventory, relationships, reputation)
        ↓
    Transition to return path using bridging narrative
        ↓
    Resume scripted content
        ↓
    Log telemetry: branch completed successfully
```

**Critical**: The Director validates branch eligibility *before* presenting the choice to the player. Players should never see a branch option that isn't valid for their current state. The checks that happen at choice-point time are:

1. **Scene match**: Is the player at a valid offer point for this branch?
2. **Prerequisites met**: Does player have required items/state/relationships?
3. **Return path viable**: Can the branch still return to scripted content from here?
4. **Not already offered**: Has this branch been declined recently? (avoid spam)

If any check fails, the branch is simply not shown as an option.

### Key Insight: Two-Phase Runtime Generation

**Important**: Both Stage 2 (Detail) and Stage 4 (Execution) happen at runtime, but they serve different purposes and occur at different moments:

| Aspect | Stage 2 (Detail) | Stage 4 (Execution) |
|--------|------------------|---------------------|
| **When** | Background, before player reaches choice point | Real-time, as player progresses through branch |
| **Player awareness** | None - happens invisibly | Direct - player sees generated content |
| **What's generated** | Save-the-Cat structure, beats, guidelines | Actual dialogue, descriptions, choices |
| **Latency tolerance** | Higher (1-3s acceptable) | Lower (must feel responsive) |
| **Trigger** | Director anticipates upcoming opportunities | Player selects branch option |

**Why this two-phase approach matters**:
- **Stage 2 (Background)**: The system prepares branch structures ahead of time while the player is engaged elsewhere. This pre-validation ensures only coherent, on-theme branches are ever offered. The player never waits for this work.
- **Stage 4 (Player-Facing)**: When the player actually enters a branch, the Writer generates specific dialogue and descriptions following the pre-approved structure. This keeps content fresh and responsive to the player's exact choices within the branch.

**Benefits**:
- Director validates structure before player sees any option (no broken branches offered)
- Fresh dialogue on each playthrough (not pre-baked text)
- Writer can react to player choices within the branch
- Director can adjust creativity based on real-time player engagement
- Generation latency is masked by player reading time

### Dynamic Generation Example

**Stage 2 (Background - player unaware):**
While the player is exploring chapter 1, the system generates and validates a branch structure:
```
"beat_2_rising_action": {
  "narrative": "The guard's suspicion deepens. He questions your motives.",
  "choice_point": true,
  "emotional_beat": "tension, mounting doubt",
  "character_voice": "guard_captain"
}
```
This structure is validated, risk-scored, and marked READY_FOR_RUNTIME before the player ever reaches chapter 2.

**Stage 4 (Player-facing - in direct response to player):**
When the player selects the branch option, the Writer generates actual dialogue:
Writer is called with:
```
{
  "beat": "rising_action",
  "context": {
    "player_state": { "reputation": "wary_outsider", "health": 85 },
    "guard_state": { "mood": "suspicious", "weapon_drawn": false },
    "recent_player_actions": ["showed compass", "claimed family heir"],
    "creativity_parameter": 0.7
  }
}
```

Writer generates:
```
"The guard's eyes narrow. 'Family heir, you say? Prove it. Tell me 
something only a true heir would know—what did your grandfather trade 
for that compass?' His hand rests on his sword hilt. Behind you, you 
hear footsteps. The other guards are moving closer."

[Choice 1: 'He won it in a card game in Samarkand']
[Choice 2: 'He sacrificed something precious for it—his freedom']
[Choice 3: 'That's not your concern. Step aside.']
```

---

## Stage 5: Terminal States

### ARCHIVED
- Branch executed successfully
- Player reached the end
- Returned to scripted content
- Telemetry shows positive engagement
- Stored in archive for learning/analysis

### REVERTED
- Player encountered an error or confusing branch
- Checkpointed back to pre-branch state
- Branch marked for analysis
- Director learns: this branch structure isn't working for some players

### DEPRECATED
- Branch replaced by newer version
- Or policy rule changed and branch no longer acceptable
- Flagged in telemetry to prevent future offers
- Preserved for historical analysis

---

## State Transition Matrix

| From State | Trigger | To State | Notes |
|-----------|---------|----------|-------|
| (Created) | Outline review | REJECTED | Discard, no further work |
| (Created) | Outline review | APPROVED_FOR_DETAIL | Proceed to Stage 2 |
| APPROVED_FOR_DETAIL | Validation fails (critical) | REJECTED | Stop, discard |
| APPROVED_FOR_DETAIL | Validation passes | APPROVED_CLEAN or APPROVED_WITH_SANITIZATION | Proceed to Stage 2b |
| APPROVED_CLEAN/SANITIZED | Director risk check | REJECTED | Discard or revise |
| APPROVED_CLEAN/SANITIZED | Director risk check | READY_FOR_PLACEMENT | Proceed to Stage 3 |
| READY_FOR_PLACEMENT | Placement algorithm runs | PLACEMENT_FAILED | Evaluate relevance |
| PLACEMENT_FAILED | Branch still relevant | RETRY_PLACEMENT | Retry with adjusted params (max 3) |
| PLACEMENT_FAILED | Branch no longer relevant | DEFERRED_FOR_REUSE | Archive for future playthroughs |
| RETRY_PLACEMENT | Retry succeeds | READY_FOR_RUNTIME | Approve for player offering |
| RETRY_PLACEMENT | Max retries exceeded | DEFERRED_FOR_REUSE | Archive for future playthroughs |
| READY_FOR_PLACEMENT | Placement algorithm runs | READY_FOR_RUNTIME | Approve for player offering |
| READY_FOR_RUNTIME | Player triggers choice | ACTIVE | Branch executing |
| ACTIVE | Player completes branch | COMPLETED | Runtime execution done |
| COMPLETED | Success logged | ARCHIVED | Success; learn from it |
| COMPLETED | Error detected | REVERTED | Rollback; analyze failure |
| DEFERRED_FOR_REUSE | New playthrough matches context | READY_FOR_PLACEMENT | Re-attempt placement |
| (Any) | Policy rule change/deprecation | DEPRECATED | Mark obsolete; don't offer |

---

## Telemetry Events by Stage

### Stage 1: Outline
```json
{
  "event_type": "outline_created",
  "proposal_id": "outline-...",
  "story_id": "demo-story-2024",
  "timestamp": "2026-01-16T10:45:00Z",
  "themes": ["redemption", "choice"],
  "estimated_length": 3
}
```

```json
{
  "event_type": "outline_reviewed",
  "proposal_id": "outline-...",
  "decision": "approved_for_detail",
  "confidence": 0.85,
  "director_notes": "Thematic fit strong; return path viable"
}
```

### Stage 2: Detail
```json
{
  "event_type": "proposal_validated",
  "proposal_id": "detail-...",
  "validation_status": "approved_clean",
  "rules_passed": 15,
  "rules_failed": 0
}
```

```json
{
  "event_type": "proposal_risk_scored",
  "proposal_id": "detail-...",
  "overall_risk": 0.35,
  "director_decision": "approved",
  "recommendation": "ready_for_placement"
}
```

### Stage 3: Placement
```json
{
  "event_type": "placement_complete",
  "proposal_id": "detail-...",
  "placement_status": "successful",
  "offer_points": 2,
  "best_confidence": 0.92,
  "state": "ready_for_runtime"
}
```

### Stage 4: Runtime
```json
{
  "event_type": "branch_activated",
  "proposal_id": "detail-...",
  "player_id": "player-123",
  "offer_point": "chapter_2.guard_confrontation_choice",
  "timestamp": "2026-01-16T11:15:30Z"
}
```

```json
{
  "event_type": "branch_beat_generated",
  "proposal_id": "detail-...",
  "beat": "hook",
  "generation_time_ms": 450,
  "generated_tokens": 95,
  "sanitization_applied": false
}
```

```json
{
  "event_type": "branch_completed",
  "proposal_id": "detail-...",
  "player_id": "player-123",
  "playtime_seconds": 180,
  "player_choices_made": 3,
  "player_satisfaction": 0.92,
  "coherence_rating": 0.89,
  "final_state": "archived"
}
```

---

## Key Design Principles

1. **Two-Stage Approval**: Outline (fast, high-level) → Detail (thorough, risk-scored)
2. **Clear Decision Points**: Each stage has explicit rejection/approval criteria
3. **Late Content Generation**: Save-the-Cat structure defined early; actual dialogue generated at runtime
4. **Director-Driven Placement**: Not author-decided; Director finds best insertion points algorithmically
5. **Dynamic Adaptation**: Runtime writer adjusts content based on real-time player state and creativity parameter
6. **Deterministic Validation, Varied Execution**: Policy checks are deterministic; runtime generation is responsive
7. **Full Auditability**: Every decision logged; can trace why proposal was accepted/rejected

---

## Ink-Specific Implementation Notes

### Ink Features Used

M2 AI-assisted branching uses these Ink language features:

| Ink Feature | M2 Usage |
|-------------|----------|
| **Knots** (`=== knot ===`) | Branch structure; each branch is typically one or more knots |
| **Stitches** (`= stitch`) | Sub-sections within branches for beat organization |
| **Choices** (`* [text] -> target`) | Player decision points within branches |
| **Diverts** (`-> knot.stitch`) | Navigation between knots; used for return paths |
| **Variables** (`VAR x = 0`) | Player state tracked in Ink (health, reputation, etc.) |
| **Tags** (`# tag`) | Metadata for styling/animation (e.g., `# dialogue`, `# action`) |
| **External functions** | Host integration for dynamic content (see below) |

### Dynamic Content via External Functions

Runtime dialogue generation uses Ink external functions to inject AI-generated content:

```ink
EXTERNAL get_ai_dialogue(beat_id)
EXTERNAL get_ai_choice(choice_id)

=== ai_branch_hook ===
{get_ai_dialogue("hook")}

* [{get_ai_choice("accept")}] -> branch_rising_action
* [{get_ai_choice("decline")}] -> decline_branch

=== branch_rising_action ===
{get_ai_dialogue("rising_action")}
// ... continues with more beats
```

**Host Implementation** (JavaScript/TypeScript):
```javascript
story.BindExternalFunction("get_ai_dialogue", (beatId) => {
    return aiWriter.generateDialogue(beatId, currentLore, directorCreativity);
});

story.BindExternalFunction("get_ai_choice", (choiceId) => {
    return aiWriter.generateChoiceText(choiceId, currentLore);
});
```

This enables:
- Fresh dialogue on each playthrough
- Director-controlled creativity adjustment in real-time
- Responsive content that adapts to player choices

### Ink Features NOT Used (M2 Scope)

The following advanced Ink features are **out of scope for M2** to reduce complexity:

| Feature | Reason for Exclusion |
|---------|---------------------|
| **Threads** (`<- thread`) | Parallel execution complicates rollback and state management |
| **Tunnels** (`-> tunnel ->`) | Subroutine patterns not needed for linear branch structure |
| **Complex conditions in choices** | Keep choice logic simple; complex branching happens at Director level |
| **Nested knots (deep)** | Limit nesting to 2 levels (knot.stitch) for clarity |

These features may be considered in future phases if player feedback indicates demand for more complex narrative structures.

---

## Example: Complete Lifecycle

**Scenario**: "Guard confrontation branch"

**Stage 1 (Outline)**: 
- Writer submits: "Guard challenges player about compass. Player reveals family connection. Guard allows passage."
- Director reviews: "Thematic fit good; return path (chapter_2.after_confrontation) viable; approved for detail."

**Stage 2 (Detail)**:
- Writer expands: Full Save-the-Cat with 4 beats, character arcs, dialogue guidelines, emotional pacing
- Validation: Passes profanity, character voice, theme, and return-path checks
- Director risk score: 0.35 (low risk); approves for placement

**Stage 3 (Placement)**:
- Director scans story: Finds "guard_confrontation_choice" at chapter_2.encounter_with_guard
- Checks prerequisites: Player has "grandfather_compass" ✓
- Bridges to return path: "Guard steps aside with respect. You proceed..." ✓
- Marks as READY_FOR_RUNTIME

**Stage 4 (Runtime)**:
- Player reaches chapter 2, approaches guard encounter choice point
- Director checks: Player has "grandfather_compass"? ✓ Return path viable? ✓
- Director presents branch as choice option: "Confront the guard directly"
- Player selects branch option (activates branch)
- Beat 1 (Hook): Writer generates description of guard's suspicion
- Player makes choice within branch
- Beat 2 (Rising Action): Writer generates guard's challenge about compass
- Player reveals family connection
- Beat 3 (Climax): Writer generates guard's moment of recognition
- Beat 4 (Resolution): Writer generates guard allowing passage with newfound respect
- Transitions via bridging narrative to chapter_2.after_confrontation
- Logs ARCHIVED with high player satisfaction

---

## Future Enhancements

1. **Multi-Stage Branches**: Support branches that themselves offer sub-branches
2. **Branching Convergence**: Multiple branches that converge back to same return path
3. **Permanent State Changes**: Some branches permanently alter world state (careful design required)
4. **Branch Fallback**: If dynamic generation fails, have pre-written fallback dialogue
5. **A/B Testing**: Track which branch variants perform better with players
6. **ML Optimization**: Learn optimal creativity parameter from successful playthroughs
