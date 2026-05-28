# AI Director Algorithm Design for M2

## Overview

The **AI Director** is a runtime governance component that evaluates incoming branch proposals from the AI Writer in real-time. Its core responsibility is:

> **Seek to ensure that any approved branch will coherently return to the scripted narrative within the configured "return window" (N player choice points), while maintaining narrative quality and player immersion.**

This document specifies the Director's decision-making logic, risk-scoring algorithm, return-path validation, and fail-safe mechanisms.

---

## Core Responsibilities

1. **Return-path enforcement**: Ensure approved branches have a viable path back to scripted content within N choices
2. **Risk assessment**: Compute a coherence score reflecting narrative quality and thematic alignment
3. **Creativity control**: Set the AI Writer's creativity parameter (0.0–1.0) based on player state and desired outcome
4. **Real-time decision**: Approve/reject incoming proposals within <500ms (latency-critical)
5. **Fail-safe mechanism**: If no return path is found, revert to scripted content and alert operators
6. **Telemetry emission**: Log all decisions with confidence scores and risk metrics

---

## Decision Flow

```
Branch Proposal from AI Writer
    ↓
[1] Validation Report Check
    - Is proposal status "passed" or "rejected_with_sanitization"?
    - CRITICAL FAIL → Reject immediately
    - PASS/SANITIZED → Continue
    ↓
[2] Return-Path Feasibility Check
    - Does return_path exist in story script?
    - Is it reachable from current scene?
    - NO → Reject with alert (no return path)
    - YES → Continue
    ↓
[3] Risk Scoring
    - Compute thematic consistency score
    - Compute LORE adherence score
    - Compute character voice consistency
    - Compute narrative pacing fit
    - Compute player preference fit
    - Aggregate into overall risk score (0.0–1.0)
    ↓
[4] Return-Path Coherence Check
    - Does the branch content lead naturally to return_path?
    - HIGH DOUBT → Reject with alert
    - ADEQUATE → Continue
    ↓
[5] Final Decision Threshold
    - If (risk_score < RISK_THRESHOLD and return_path_confidence > 0.7):
        APPROVE
    - Else:
        REJECT
    ↓
Decision + Telemetry Event
```

---

## 1. Validation Report Check

**Input**: Proposal + associated validation report

**Logic**:
```
if validation_report.status == "failed":
    decision = REJECT
    reason = "Proposal failed policy validation"
    confidence = 1.0
    return decision
elif validation_report.status == "rejected_with_sanitization":
    # Sanitization was applied; Director still evaluates
    proposal = validation_report.sanitized_proposal
    note = "Using sanitized version"
elif validation_report.status == "passed":
    note = "Passed all validations"
```

---

## 2. Return-Path Feasibility Check

**Goal**: Verify that the target return knot exists and is reachable.

**Input**: 
- Proposal with `content.return_path` (e.g., "chapter_2.after_confrontation")
- Story script (as Ink AST or flat knot list)

**Algorithm**:
```
def check_return_path_feasibility(proposal, story_script):
    return_path = proposal.content.return_path
    current_scene = proposal.story_context.current_scene
    
    # [1] Check if return_path knot exists
    if return_path not in story_script.all_knots():
        return (False, "Return path knot does not exist", 0.0)
    
    # [2] Check if return_path is reachable (BFS or DFS from current scene)
    if not is_reachable(current_scene, return_path, story_script):
        return (False, "Return path is not reachable from current scene", 0.0)
    
    # [3] Estimate distance to return path
    distance = shortest_path_distance(current_scene, return_path, story_script)
    if distance > RETURN_WINDOW * 2:  # Allow 2x overshoot
        return (False, "Return path is too far (exceeds 2x return window)", 0.3)
    
    return (True, "Return path is feasible", 0.9)
```

**Tuning parameters**:
- `RETURN_WINDOW` (int): Number of player choice points (default: 3–5)
- Reachability tolerance: How indirect can the path be? (default: direct paths preferred, indirect allowed with confidence penalty)

---

## 3. Risk Scoring

**Goal**: Compute an aggregate risk score reflecting narrative quality.

**Formula**:
```
risk_score = weighted_avg([
    thematic_consistency_risk,
    lore_adherence_risk,
    character_voice_risk,
    narrative_pacing_risk,
    player_preference_risk,
    proposal_confidence_risk
])

where each risk is in [0.0, 1.0], 0.0 = low risk, 1.0 = high risk
```

**Weights** (tunable):
```
thematic_consistency_weight: 0.20
lore_adherence_weight: 0.20
character_voice_weight: 0.15
narrative_pacing_weight: 0.15
player_preference_weight: 0.20
proposal_confidence_weight: 0.10
```

### 3a. Thematic Consistency Risk

**Goal**: Assess whether branch tone/mood/themes align with story themes.

**Algorithm**:
```
def thematic_consistency_risk(proposal, story_themes, narrative_pacing_hint):
    # Extract theme embeddings
    branch_embedding = embed(proposal.content.text)
    story_embedding = embed(story_themes)
    
    # Compute semantic similarity
    similarity = cosine_similarity(branch_embedding, story_embedding)
    
    # Adjust for narrative phase
    if narrative_pacing_hint == "climactic":
        # Climactic branches should be intense; penalize if too calm
        intensity = assess_intensity(proposal.content.text)
        intensity_penalty = max(0, 0.3 - intensity) * 0.5
    else:
        intensity_penalty = 0
    
    # Risk = 1 - similarity, adjusted for phase
    risk = (1.0 - similarity) + intensity_penalty
    return clamp(risk, 0.0, 1.0)
```

**Inputs**:
- `proposal.content.text`: Branch narrative
- `proposal.story_context.story_themes`: Key story themes (e.g., "redemption", "betrayal")
- `proposal.story_context.narrative_pacing_hint`: Current phase (exposition, climactic, etc.)

**Tuning parameters**:
- `embedding_similarity_threshold` (0.0–1.0): Minimum acceptable similarity (default: 0.6)
- `intensity_tolerance` (0.0–1.0): How much tone variation is acceptable (default: 0.2)

### 3b. LORE Adherence Risk

**Goal**: Check whether branch content contradicts established LORE facts.

**Algorithm**:
```
def lore_adherence_risk(proposal, lore_facts):
    # Extract facts asserted in branch
    branch_facts = extract_facts(proposal.content.text)
    
    # For each fact, compute similarity to LORE
    contradiction_scores = []
    for branch_fact in branch_facts:
        best_match = max_similarity(branch_fact, lore_facts)
        if best_match < CONTRADICTION_THRESHOLD:
            # Likely a contradiction
            contradiction_scores.append(1.0 - best_match)
    
    if len(contradiction_scores) == 0:
        return 0.0  # No contradictions detected
    
    # Average contradiction score
    avg_contradiction = mean(contradiction_scores)
    return clamp(avg_contradiction, 0.0, 1.0)
```

**Inputs**:
- `proposal.content.text`: Branch narrative
- `lore_facts`: Curated set of immutable story facts (e.g., "compass_origin = 1847")

**Tuning parameters**:
- `CONTRADICTION_THRESHOLD` (0.0–1.0): How similar must branch fact be to LORE to not count as contradiction (default: 0.75)
- `enforce_strictly` (boolean): If false, allow minor contradictions; if true, reject any (default: false)

### 3c. Character Voice Consistency Risk

**Goal**: Assess whether dialogue and mannerisms match established character profiles.

**Algorithm**:
```
def character_voice_risk(proposal, character_state):
    risk = 0.0
    
    for character_name, character_profile in character_state.items():
        if character_name not in proposal.content.text:
            continue  # Character not mentioned; no risk
        
        # Extract dialogue/actions for this character
        character_excerpts = extract_character_dialogue(proposal.content.text, character_name)
        
        # Compare against character voice profile
        voice_embedding = embed(character_profile.voice_sample)
        excerpt_embeddings = [embed(e) for e in character_excerpts]
        
        # Compute average distance from expected voice
        distances = [cosine_distance(e, voice_embedding) for e in excerpt_embeddings]
        character_risk = mean(distances)
        
        risk += character_risk
    
    # Average across all characters
    if character_state:
        risk = risk / len(character_state)
    
    return clamp(risk, 0.0, 1.0)
```

**Inputs**:
- `proposal.content.text`: Branch narrative
- `proposal.story_context.character_state`: Character profiles with voice samples and personality traits

**Tuning parameters**:
- `voice_distance_threshold` (0.0–1.0): Maximum acceptable distance from expected voice (default: 0.4)
- `ooc_tolerance` (0.0–1.0): How much variation from character personality is allowed (default: 0.3)

### 3d. Narrative Pacing Risk

**Goal**: Check whether branch length and intensity fit the current narrative phase.

**Algorithm**:
```
def narrative_pacing_risk(proposal, narrative_pacing_hint):
    branch_length = proposal.content.length_tokens
    intensity = assess_intensity(proposal.content.text)
    
    # Expected targets by phase
    phase_targets = {
        "exposition": {"length": (100, 250), "intensity": (0.2, 0.5)},
        "slow_buildup": {"length": (80, 200), "intensity": (0.3, 0.6)},
        "climactic": {"length": (40, 120), "intensity": (0.7, 1.0)},
        "resolution": {"length": (100, 200), "intensity": (0.1, 0.4)}
    }
    
    target = phase_targets.get(narrative_pacing_hint, {})
    length_min, length_max = target.get("length", (0, 1000))
    intensity_min, intensity_max = target.get("intensity", (0.0, 1.0))
    
    # Compute deviation
    length_penalty = 0
    if branch_length < length_min:
        length_penalty = (length_min - branch_length) / length_min
    elif branch_length > length_max:
        length_penalty = (branch_length - length_max) / length_max
    
    intensity_penalty = 0
    if intensity < intensity_min:
        intensity_penalty = (intensity_min - intensity)
    elif intensity > intensity_max:
        intensity_penalty = (intensity - intensity_max)
    
    pacing_risk = (length_penalty + intensity_penalty) / 2
    return clamp(pacing_risk, 0.0, 1.0)
```

**Inputs**:
- `proposal.content.length_tokens`: Token count
- `proposal.content.text`: Branch narrative (for intensity assessment)
- `proposal.story_context.narrative_pacing_hint`: Current phase

**Tuning parameters**:
- `phase_length_targets`: Expected length ranges per phase (tunable per story)
- `phase_intensity_targets`: Expected intensity ranges per phase

### 3e. Proposal Confidence Risk

**Goal**: Penalize proposals with low self-assessed confidence.

**Algorithm**:
```
def proposal_confidence_risk(proposal):
    # AI Writer's confidence score is already in proposal
    confidence = proposal.metadata.confidence_score
    
    # Convert to risk (inverse)
    risk = 1.0 - confidence
    
    # Apply a curve: very low confidence (<0.5) is penalized more heavily
    if confidence < 0.5:
        risk = risk ** 0.5  # Exponentiate to penalize low confidence
    
    return clamp(risk, 0.0, 1.0)
```

**Inputs**:
- `proposal.metadata.confidence_score`: AI Writer's confidence (0.0–1.0)

### 3f. Player Preference Risk

**Goal**: Assess whether the branch aligns with the player's demonstrated preferences and play style, predicting whether they will enjoy the branch.

**Algorithm**:
```
def player_preference_risk(proposal, player_profile):
    risk = 0.0
    
    # [1] Branch type preference match
    branch_type = proposal.content.branch_type  # e.g., "dialogue", "combat", "exploration"
    type_preference = player_profile.branch_type_preferences.get(branch_type, 0.5)
    type_risk = 1.0 - type_preference  # Low preference = high risk
    
    # [2] Theme preference match
    branch_themes = proposal.content.themes  # e.g., ["redemption", "mystery"]
    theme_matches = [
        player_profile.theme_preferences.get(theme, 0.5)
        for theme in branch_themes
    ]
    theme_preference = mean(theme_matches) if theme_matches else 0.5
    theme_risk = 1.0 - theme_preference
    
    # [3] Complexity preference (based on player's historical choices)
    branch_complexity = proposal.metadata.complexity_score  # 0.0 = simple, 1.0 = complex
    preferred_complexity = player_profile.preferred_complexity  # Learned from history
    complexity_deviation = abs(branch_complexity - preferred_complexity)
    complexity_risk = complexity_deviation
    
    # [4] Engagement prediction (based on similar past branches)
    similar_branch_outcomes = find_similar_branch_outcomes(
        proposal, 
        player_profile.branch_history
    )
    if similar_branch_outcomes:
        # Historical engagement with similar branches
        avg_engagement = mean([o.engagement_score for o in similar_branch_outcomes])
        engagement_risk = 1.0 - avg_engagement
    else:
        # No history; use neutral risk
        engagement_risk = 0.5
    
    # [5] Pacing preference (does player like frequent branches or sparse?)
    time_since_last_branch = player_profile.time_since_last_branch_minutes
    preferred_frequency = player_profile.preferred_branch_frequency_minutes
    if time_since_last_branch < preferred_frequency * 0.5:
        # Too soon; player may feel overwhelmed
        frequency_risk = 0.3
    elif time_since_last_branch > preferred_frequency * 2.0:
        # Overdue; player may welcome a branch
        frequency_risk = 0.0
    else:
        frequency_risk = 0.1
    
    # Weighted combination
    risk = (
        type_risk * 0.25 +
        theme_risk * 0.25 +
        complexity_risk * 0.15 +
        engagement_risk * 0.25 +
        frequency_risk * 0.10
    )
    
    return clamp(risk, 0.0, 1.0)
```

**Inputs**:
- `proposal.content.branch_type`: Type of branch (dialogue, combat, exploration, moral_dilemma, etc.)
- `proposal.content.themes`: Themes present in the branch
- `proposal.metadata.complexity_score`: Estimated complexity (0.0–1.0)
- `player_profile.branch_type_preferences`: Dict mapping branch types to preference scores (0.0–1.0)
- `player_profile.theme_preferences`: Dict mapping themes to preference scores (0.0–1.0)
- `player_profile.preferred_complexity`: Player's preferred complexity level (learned)
- `player_profile.branch_history`: List of past branch outcomes with engagement scores
- `player_profile.time_since_last_branch_minutes`: Minutes since last branch was offered
- `player_profile.preferred_branch_frequency_minutes`: Estimated preferred frequency

**Player Profile Learning**:
The player profile is built incrementally from telemetry:
- **Branch type preferences**: Updated based on accept/decline rates per type
- **Theme preferences**: Updated based on engagement scores with themed branches
- **Complexity preference**: Learned from which branches player completes vs. abandons
- **Preferred frequency**: Learned from accept rates relative to time gaps

**Cold Start Handling**:
For new players with no history:
- Use population-level defaults (average preferences across all players)
- Apply conservative risk estimate (0.4–0.5 for unknown factors)
- Update preferences aggressively during first 5 branches

**Tuning parameters**:
- `type_preference_weight` (0.0–1.0): Weight for branch type match (default: 0.25)
- `theme_preference_weight` (0.0–1.0): Weight for theme match (default: 0.25)
- `complexity_weight` (0.0–1.0): Weight for complexity match (default: 0.15)
- `engagement_weight` (0.0–1.0): Weight for historical engagement (default: 0.25)
- `frequency_weight` (0.0–1.0): Weight for timing preference (default: 0.10)
- `cold_start_risk` (0.0–1.0): Default risk for new players (default: 0.45)

---

## 4. Return-Path Coherence Check

**Goal**: Verify that the branch content leads naturally to the return path without narrative jarring.

**Algorithm**:
```
def return_path_coherence_check(proposal):
    # Get branch ending and return path opening
    branch_ending = extract_last_sentences(proposal.content.text, num_sentences=3)
    return_path_opening = extract_opening(proposal.story_context.return_path, num_sentences=2)
    
    # Compute semantic coherence
    branch_embedding = embed(branch_ending)
    return_embedding = embed(return_path_opening)
    coherence = cosine_similarity(branch_embedding, return_embedding)
    
    # Convert to confidence score
    if coherence > 0.7:
        return (True, "Strong coherence with return path", 0.9)
    elif coherence > 0.5:
        return (True, "Adequate coherence; may feel slight jump", 0.6)
    else:
        return (False, "Poor coherence; jarring transition likely", 0.2)
```

**Inputs**:
- `proposal.content.text`: Branch narrative
- `proposal.story_context.return_path`: Target return knot

**Tuning parameters**:
- `coherence_threshold` (0.0–1.0): Minimum acceptable coherence (default: 0.5)
- `strong_coherence_threshold` (0.0–1.0): High confidence threshold (default: 0.7)

---

## 5. Final Decision Threshold

**Algorithm**:
```
def make_decision(risk_score, return_path_feasibility, return_path_confidence):
    if risk_score > RISK_THRESHOLD:
        decision = REJECT
        reason = f"Risk score too high: {risk_score:.2f} > {RISK_THRESHOLD}"
    elif not return_path_feasibility:
        decision = REJECT
        reason = "Return path is not feasible"
    elif return_path_confidence < 0.5:
        decision = REJECT
        reason = f"Return path confidence too low: {return_path_confidence:.2f}"
    else:
        decision = APPROVE
        reason = f"Passed all checks (risk={risk_score:.2f}, return_path_conf={return_path_confidence:.2f})"
    
    return (decision, reason, risk_score)
```

**Tuning parameters**:
- `RISK_THRESHOLD` (0.0–1.0): Maximum acceptable risk score (default: 0.4)
- `RETURN_PATH_CONFIDENCE_MIN` (0.0–1.0): Minimum acceptable return path confidence (default: 0.5)

---

## Fail-Safe Mechanism

**Goal**: If anything goes wrong, safely revert to scripted content without corrupting game state.

**Algorithm**:
```
def apply_branch_with_failsafe(proposal, branch_proposal_id):
    try:
        # [1] Apply branch to runtime
        save_state_before = serialize_game_state()
        apply_branch_to_story(proposal)
        
        # [2] Test that story can continue
        test_continue_story(save_state_before)
        
        # [3] Log successful integration
        log_telemetry_event({
            "event_type": "branch_integrated",
            "proposal_id": branch_proposal_id,
            "status": "success"
        })
        
    except Exception as e:
        # [FAILSAFE] Revert to saved state
        restore_game_state(save_state_before)
        
        log_telemetry_event({
            "event_type": "branch_integration_failed",
            "proposal_id": branch_proposal_id,
            "error": str(e),
            "severity": "high"
        })
        
        # Alert operators
        send_alert_to_operators({
            "message": f"Branch {branch_proposal_id} failed to integrate; reverted to scripted path",
            "error_details": str(e)
        })
```

**Key points**:
- Always save game state before applying
- Test that story can continue after applying
- Revert immediately on any error
- Alert operators to high-severity issues
- Never silently drop a branch; always log

---

## Telemetry Emission

**For each decision, emit a telemetry event:**

```json
{
  "event_type": "director_decision",
  "timestamp": "2026-01-16T10:45:23Z",
  "proposal_id": "550e8400-e29b-41d4-a716-446655440001",
  "story_id": "demo-story-2024",
  "decision": "approve",
  "reason": "Passed all checks",
  "risk_score": 0.35,
  "return_path_feasible": true,
  "return_path_confidence": 0.88,
  "thematic_consistency_risk": 0.20,
  "lore_adherence_risk": 0.15,
  "character_voice_risk": 0.25,
  "narrative_pacing_risk": 0.30,
  "proposal_confidence_risk": 0.08,
  "creativity_parameter_set": 0.65,
  "player_engagement_level": 0.78,
  "decision_latency_ms": 245,
  "director_version": "v1.0.0"
}
```

**For each Writer request, also emit:**

```json
{
  "event_type": "writer_request",
  "timestamp": "2026-01-16T10:45:18Z",
  "story_id": "demo-story-2024",
  "creativity_parameter": 0.65,
  "reason_for_creativity_level": "Player engaged (0.78), recent success rate 0.82, climactic phase",
  "player_state": {
    "confusion_level": 0.2,
    "engagement": 0.78,
    "recent_actions": 3
  },
  "narrative_phase": "climactic"
}
```

---

## Performance Profile

**Target latency**: <500ms per decision

**Breakdown** (estimated):
- Validation report check: 10ms
- Return-path feasibility check: 50–100ms (depends on story size)
- Risk scoring (embeddings): 200–250ms (parallelizable)
- Return-path coherence check: 50–75ms
- Final decision: 1–5ms
- **Total**: ~320–440ms (with optimizations)

**Optimization strategies**:
- Pre-compute story embeddings and knot graphs at load time
- Cache character voice embeddings
- Parallelize risk score computations (different risk metrics are independent)
- Use quantized embeddings for faster similarity checks

---

## Test Scenarios

### Success Scenario: Well-Formed Branch
- Proposal with high confidence (0.9+)
- Return path clearly specified and reachable
- Risk scores all low (<0.3)
- Expected: APPROVE in <300ms

### Failure Scenario: No Return Path
- Proposal with valid content but missing `return_path`
- Expected: REJECT with alert "Return path not feasible"

### Failure Scenario: LORE Contradiction
- Branch asserts something that contradicts established LORE
- LORE adherence risk: 0.8+
- Risk score: >0.4
- Expected: REJECT with alert "LORE contradiction detected"

### Edge Case: Sanitized Proposal
- Proposal failed validation but was sanitized (profanity removed)
- Otherwise high quality
- Expected: APPROVE if risk is low, using sanitized version

### Edge Case: Ambiguous Return Path
- Return path is reachable but coherence is low (0.3)
- Director detects potential jarring transition
- Expected: REJECT or APPROVE_WITH_CAUTION (depending on threshold tuning)

---

## Configuration Example

```yaml
# director-config.yaml

risk_scoring:
  thematic_consistency_weight: 0.25
  lore_adherence_weight: 0.25
  character_voice_weight: 0.20
  narrative_pacing_weight: 0.15
  proposal_confidence_weight: 0.15
  
  thematic_consistency:
    embedding_similarity_threshold: 0.6
    intensity_tolerance: 0.2
  
  lore_adherence:
    contradiction_threshold: 0.75
    enforce_strictly: false
  
  character_voice:
    voice_distance_threshold: 0.4
    ooc_tolerance: 0.3
  
  narrative_pacing:
    phase_length_targets:
      exposition: [100, 250]
      slow_buildup: [80, 200]
      climactic: [40, 120]
      resolution: [100, 200]
    phase_intensity_targets:
      exposition: [0.2, 0.5]
      slow_buildup: [0.3, 0.6]
      climactic: [0.7, 1.0]
      resolution: [0.1, 0.4]

return_path:
  feasibility_check_enabled: true
  coherence_threshold: 0.5
  strong_coherence_threshold: 0.7
  reachability_tolerance: 2.0  # Allow up to 2x return window distance

final_decision:
  risk_threshold: 0.4
  return_path_confidence_min: 0.5

performance:
  target_latency_ms: 500
  timeout_ms: 1000  # Hard timeout; revert if decision takes >1s

failsafe:
  enabled: true
  auto_revert_on_error: true
  alert_operators: true
```

---

## Future Enhancements

1. **Learned heuristics**: Train ML model on playtest feedback to refine risk weights
2. **Adaptive return window**: Adjust return window based on player exploration patterns
3. **Narrative flow analysis**: Use plot structure analysis to detect incongruent branch insertions
4. **Multi-branch coherence**: Consider multiple concurrent branches and their interactions
5. **Player state prediction**: Predict player emotional state and match branch intensity accordingly
6. **Adaptive creativity**: Learn optimal creativity levels from playtest feedback and telemetry

---

## Creativity Control Loop

The Director does not just approve/reject proposals—it also controls the **creativity parameter** sent to the AI Writer when requesting proposals.

**Creativity parameter** (0.0–1.0):
- `0.0`: Minimal creativity; Writer produces conservative, safe, predictable branches (low temperature)
- `0.5`: Balanced creativity; Writer produces novel but grounded branches
- `1.0`: Maximum creativity; Writer produces imaginative, surprising branches (high temperature)

**Director controls creativity based on**:
- **Player state**: If player is confused or lost, reduce creativity; if player is engaged and progressing well, increase it
- **Recent success rate**: If recent branches were well-received, increase creativity; if rejected, decrease it
- **Narrative phase**: In climactic phases, allow higher creativity; in exposition, prefer lower creativity
- **Risk tolerance**: If risk_score is high, request lower creativity proposals; if low, can request more creative content

**Algorithm**:
```
def compute_creativity_parameter(player_state, recent_success_rate, narrative_phase, risk_tolerance):
    base_creativity = 0.5
    
    # Adjust for player engagement
    if player_state.confusion_level > 0.7:
        base_creativity -= 0.2  # Reduce creativity if player is confused
    elif player_state.engagement > 0.8:
        base_creativity += 0.1  # Increase if highly engaged
    
    # Adjust for recent success
    success_delta = recent_success_rate - 0.75  # Target 75% acceptance rate
    base_creativity += success_delta * 0.3  # Weight 30% toward success feedback
    
    # Adjust for narrative phase
    phase_creativity = {
        "exposition": 0.3,
        "slow_buildup": 0.5,
        "climactic": 0.8,
        "resolution": 0.4
    }
    base_creativity = 0.6 * base_creativity + 0.4 * phase_creativity.get(narrative_phase, 0.5)
    
    # Adjust for risk tolerance
    risk_multiplier = 1.0 - (risk_tolerance * 0.3)  # Higher risk → lower multiplier
    base_creativity *= risk_multiplier
    
    return clamp(base_creativity, 0.0, 1.0)
```

**Benefits**:
- Keeps proposals fresh and varied (no deterministic reproduction)
- Adapts to player engagement and confusion in real-time
- Allows Director to "dial down" creativity if safety/coherence concerns arise
- Learns from feedback loop: success → more creativity; failure → less creativity
- Prevents monotony (same context won't always produce same proposal type)
