# Branch Proposal Schema Documentation

## Overview

The **Branch Proposal Schema** defines the structure and metadata for AI-generated story branches in the M2 AI-assisted branching system. This schema is used by the AI Writer to produce proposals, by the Director to evaluate them, and by the validation pipeline to assess compliance with policy rules.

## Design Goals

1. **Determinism**: Include all context needed to reproduce the same proposal given the same inputs and seed.
2. **Provenance Tracking**: Record which LLM, version, and parameters generated each proposal.
3. **Auditability**: Support full audit trails and rollback operations.
4. **Validation**: Provide all information needed by policy and sanitization checks.
5. **Player Experience**: Enable decisions by the Director to maintain narrative coherence and immersion.

## Top-Level Fields

### `id` (string, required)
**Pattern**: UUID v4 format (e.g., `550e8400-e29b-41d4-a716-446655440001`)

Unique identifier for this proposal. Used for:
- Tracking proposals through the validation pipeline
- Audit and rollback operations
- Linking telemetry events to proposals
- Deduplication if the same context is processed multiple times

### `metadata` (object, required)
Contains provenance, generation details, and confidence metrics.

#### `metadata.created_at` (ISO 8601 datetime, required)
When the proposal was generated (server time, not client time).

#### `metadata.llm_model` (string, required)
The LLM model used, e.g.:
- `gpt-4-turbo`
- `claude-3-opus`
- `local-model-v1`
- `anthropic-claude`

Used for:
- Tracking which model generated which proposals
- Disabling/rotating models if quality degrades
- Correlating model versions with player feedback

#### `metadata.llm_version` (string, optional)
Release date or semantic version of the model, e.g., `2024-01-15` or `1.0.0`.

#### `metadata.llm_seed` (integer, optional, null allowed)
Random seed used during generation. If null, the model did not use a fixed seed.

**Reproducibility implications**:
- If seed is set: `same context + same seed + same model version → same proposal` (exact reproducibility).
- If seed is null: same context may produce different proposals (sampling enabled).

#### `metadata.context_hash` (SHA-256 hex string)
Hash of the serialized input context (story_context + constraints used during generation).

**Use cases**:
- Detect if the same context was processed multiple times
- Verify reproducibility: `regenerate(context) → hash should match`
- Link proposals to their source context for audits

#### `metadata.confidence_score` (number, 0.0–1.0, required)
AI Writer's self-assessed confidence that the proposal is coherent, on-theme, and playable.

**Interpretation**:
- `0.9–1.0`: Highly confident; minimal risk
- `0.75–0.9`: Moderately confident; routine validation
- `0.5–0.75`: Low confidence; likely rejected or heavily scrutinized
- `<0.5`: Very low confidence; usually auto-rejected

**Used by**:
- Director risk scoring
- Validation pipeline thresholds
- Telemetry and monitoring

#### `metadata.generation_time_ms` (integer, >=0)
Time in milliseconds from prompt submission to proposal returned.

**Budgeting**: Should typically be 1000–3000 ms for full proposal generation.

#### `metadata.actor` (string, optional)
Which component/agent submitted the proposal, e.g.:
- `ai_writer_v1`
- `story_author_agent`
- `batch_generator`

---

## `story_context` (object, required)
Story state and context at the moment the branch decision was made.

### `story_context.story_id` (string, required)
Identifier of the story being played, e.g., `demo-story-2024` or `chapter-3-revised`.

Used by:
- Feature flags (enable/disable AI branches per story)
- Grouping telemetry and analytics
- Replay testing

### `story_context.story_title` (string, optional)
Human-readable title, e.g., "The Lost Expedition".

### `story_context.current_scene` (string, required)
The current scene/knot in Ink script (e.g., `chapter_2.encounter_with_guard`).

**Format**: Use Ink knot notation (`knot.stitch` or `knot.stitch.nested`).

**Ink Terminology Note**: This field represents the game-level scene identifier, which maps directly to an Ink knot or knot.stitch path:
- `act2.campfire` maps to Ink: `=== act2 === = campfire`
- `chapter_2.encounter_with_guard` maps to Ink: `=== chapter_2 === = encounter_with_guard`

The value must be a valid Ink divert target that exists in the compiled story.

### `story_context.player_action` (string, optional)
The choice or action the player took that triggered branch generation, e.g., "chose to confront the guard directly".

### `story_context.player_inventory` (array of strings, optional)
List of items the player has acquired (e.g., `["torn_map", "grandfather_compass", "leather_satchel"]`).

**Use**: Provides context for narrative coherence (e.g., "if player has the compass, they might recall its history").

### `story_context.player_state` (object, optional)
Relevant player variables as key-value pairs, e.g.:
```json
{
  "health": 85,
  "reputation": "cautious_stranger",
  "morale": 0.7,
  "exhaustion": 0.5
}
```

**Common keys**:
- `health`: 0–100
- `morale`: 0.0–1.0
- `exhaustion`: 0.0–1.0
- `reputation`: string (thematic label)
- Custom domain-specific variables

Used by Director to assess branch fit (e.g., "if player is exhausted, branch should be contemplative").

### `story_context.character_state` (object, optional)
State and definitions of key characters mentioned in the story at this point.

Example:
```json
{
  "guard_captain": {
    "mood": "suspicious",
    "relationship": "neutral",
    "objective": "protect_fortress_entrance"
  },
  "narrator": {
    "tone": "mysterious",
    "pov": "third_person_limited"
  }
}
```

Used by:
- AI Writer to preserve character voice
- Director to check thematic consistency

### `story_context.recent_events` (array of strings, optional)
Recent story events (last 5–10) to provide narrative momentum, e.g.:
```
[
  "Player discovered cryptic message in old library",
  "Player traveled three days to the fortress",
  "Guard demanded papers at the gate"
]
```

Used by AI Writer to maintain narrative continuity and pacing.

### `story_context.narrative_pacing_hint` (enum, optional)
Hint about the current narrative phase:
- `slow_buildup`: Exposition, mystery setup
- `climactic`: Rising tension, key decision point
- `resolution`: Climax, aftermath, denouement
- `exposition`: Information delivery

Used by AI Writer to modulate tone and length (e.g., climactic branches are shorter, more intense).

### `story_context.story_themes` (array of strings, optional)
Key themes of the story, e.g., `["discovery", "redemption", "forbidden_knowledge"]`.

Used by Director to validate thematic consistency of the branch.

---

## `content` (object, required)
The generated branch content.

### `content.branch_type` (enum, required)
Type of content structure:
- `ink_fragment`: A snippet of Ink syntax (no choice points) to be injected at the current position.
- `narrative_delta`: Prose narrative (no Ink) to be displayed as narration; typically used for flavor text or internal monologue.
- `ink_knot`: A full Ink knot with choice points and sub-flows; used for more complex branches that may spawn multiple child scenarios.

**Recommendation**: Favor `ink_fragment` and `narrative_delta` for M2 MVP; `ink_knot` for more advanced scenarios.

### `content.text` (string, required)
The actual branch content. Format depends on `branch_type`:
- **ink_fragment**: Valid Ink syntax (e.g., `"He smiled. 'Welcome back.'"`)
- **narrative_delta**: Plain prose (e.g., `"The innkeeper's eyes narrowed..."`)
- **ink_knot**: Full Ink knot syntax including choice points and subflows

### `content.character_voice` (string, optional)
Who is speaking/narrating, e.g.:
- `narrator`
- `guard_captain`
- `player_inner_monologue`
- `antagonist`

Used by Director to verify voice consistency with `character_state`.

### `content.length_tokens` (integer, >=0, optional)
Approximate token count of the content using the same tokenizer as the validation pipeline.

Used by validation pipeline for length-limit checks (e.g., "reject if >500 tokens").

### `content.ink_tags` (array of strings, optional)
Ink tags used in the fragment, e.g., `["action", "dialogue", "internal", "atmosphere"]`.

Example: `<span class="action">The guard drew his sword.</span> # action`

Used for:
- Routing branches to styling/animation systems
- Validating that all tags are whitelisted
- Analytics (e.g., count dialogue vs. action branches)

### `content.return_path` (string, optional)
The scripted scene/knot this branch should return to, e.g., `chapter_2.after_confrontation`.

**Ink Implementation**: This value must be a valid Ink divert target. At branch completion, the runtime executes:
```ink
-> chapter_2.after_confrontation
```

The validation pipeline checks that this knot (and stitch, if specified) exists in the compiled story using `story.allKnots` or equivalent InkJS API.

**Critical for Director**: Guides the return-path algorithm. If omitted, the Director must infer a return path.

### `content.return_path_confidence` (number, 0.0–1.0, optional)
AI Writer's confidence that the return path is narratively coherent.

Used by Director to weight return-path decisions (low confidence → increased scrutiny or rejection).

---

## `constraints` (object, optional)
Constraints applied during generation; useful for understanding generation parameters and validating compliance.

### `constraints.max_length_tokens` (integer, optional)
Maximum token length enforced during generation (e.g., 100 or 200).

### `constraints.prohibited_patterns` (array of strings, optional)
Patterns that were excluded during generation, e.g., `["sudden_violence", "out_of_character_dialogue"]`.

### `constraints.style_template` (string, optional)
Style template applied, e.g., `noir_explorer`, `fantasy_epic`, `sci_fi_noir`.

---

## Validation and Determinism

### Reproducibility Guarantee
A proposal is reproducible if, given the same inputs (story_context, constraints, LLM seed), the same proposal is generated:

```
Proposal(context_A, seed_42, model_v1) == Proposal(context_A, seed_42, model_v1)
```

**Implications for storage and testing**:
1. Always store `context_hash` and `llm_seed`.
2. For validation testing, regenerate proposals and compare hashes.
3. If regeneration fails, log the mismatch (indicates model drift or context mutation).

### Schema Validation
The provided `branch-proposal.json` is a JSON Schema (draft-07) that can validate proposals using standard validators:

```bash
# Validate with ajv (Node.js)
ajv validate -s branch-proposal.json -d example_01.json
```

---

## Example Usage

See the `examples/` directory for 10 real-world branch proposals covering:
1. Guard confrontation (dialogue, tension)
2. Tavern meeting (exposition, character reveal)
3. Forest passage (atmosphere, foreshadowing)
4. Temple spirit (supernatural, choice point)
5. Journal discovery (discovery, hint)
6. Betrayal moment (emotional, moral choice)
7. Rival encounter (competition, stakes)
8. Artifact chamber (revelation, legacy)
9. Revelation scene (emotional climax)
10. Final choice (agency, resolution)

---

## Integration Checklist

- [ ] Validate all proposals against this schema before acceptance
- [ ] Hash context and store `context_hash` for audit trails
- [ ] Check that `current_scene` matches game state at proposal time
- [ ] Verify `return_path` points to a valid, reachable knot in the story
- [ ] Log all proposals and validation results for analysis
- [ ] Monitor `confidence_score` distribution to detect quality trends

---

## Future Enhancements

1. **Embedded LORE**: Include full LORE context directly in proposals for better auditability (currently external).
2. **Execution trace**: Record which LLM API calls were made during generation (for debugging and cost tracking).
3. **Multi-language support**: Extend schema to support non-English branches.
4. **Branch metrics**: Pre-compute quality metrics (semantic similarity to original story, embedding distance from theme, etc.) at generation time.
