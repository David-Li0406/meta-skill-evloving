# M2 Telemetry Schema and Observability Design

This document specifies the telemetry events collected from the M2 AI-assisted branching system and how to use them for post-launch analysis and iteration.

## Overview

**Telemetry** is the critical feedback loop for M2. During Phase 2 (soft launch), the system collects detailed events about:
- Branch proposal generation and validation
- Director decision-making
- Player engagement with branches
- Outcome: did player find branch coherent?
- Policy violations and sanitization effectiveness

**Learning happens between phases**: Phase 2 telemetry informs Phase 3 Director tuning, policy rule updates, and LORE model refinement.

## Telemetry Event Architecture

### Event Structure

All telemetry events follow this base schema:

```json
{
  "event_id": "uuid",
  "event_type": "branch_proposal_generated",
  "timestamp": "2026-01-20T14:30:22Z",
  "session_id": "player_session_uuid",
  "player_id": "anonymous_hash",
  "game_version": "1.2.3",
  "m2_version": "2.0",
  
  "event_data": {
    // Type-specific fields
  },
  
  "context": {
    "player_level": 7,
    "current_scene": "act2.campfire",
    "play_time_seconds": 3600,
    "save_slot": 1
  }
}
```

### Event Types

M2 emits events at 7 key decision points:

#### Event 1: Branch Proposal Generated

**When**: AI Writer generates a proposal (Outline or Detail stage)

**Purpose**: Track generation quality and volume

```json
{
  "event_type": "branch_proposal_generated",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "branch_type": "companion_dialogue",
    "generation_stage": "detail",
    "generation_latency_ms": 2150,
    
    "lore_context": {
      "lore_hash": "a2f4c8d1e6b9",
      "npcs_in_context": ["lyra"],
      "themes": ["loyalty", "sacrifice"]
    },
    
    "writer_parameters": {
      "director_creativity": 0.65,
      "director_seed": 42591847,
      "llm_model": "gpt-4-turbo",
      "llm_version": "2024-01-15"
    },
    
    "proposal_metadata": {
      "estimated_playtime_seconds": 55,
      "dialogue_options_count": 3,
      "confidence_score": 0.87
    }
  }
}
```

**Metrics extracted**:
- Generation latency distribution
- Confidence score distribution
- Branch type frequency
- Creativity parameter vs. generation latency
- LLM version performance

#### Event 2: Validation Pipeline Executed

**When**: Proposal runs through validation pipeline

**Purpose**: Track policy rule effectiveness and violation frequency

```json
{
  "event_type": "validation_pipeline_executed",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "validation_status": "approved_clean",
    
    "rules_executed": [
      {
        "rule_id": "profanity_filter",
        "rule_category": "content_safety",
        "result": "pass",
        "severity": "critical",
        "execution_time_ms": 45
      },
      {
        "rule_id": "explicit_content_filter",
        "result": "pass",
        "execution_time_ms": 38
      },
      {
        "rule_id": "lore_consistency_check",
        "result": "pass",
        "violations_found": 0,
        "execution_time_ms": 120
      },
      {
        "rule_id": "character_voice_consistency",
        "result": "pass",
        "execution_time_ms": 89
      }
    ],
    
    "sanitizations_applied": [],
    "total_validation_time_ms": 292,
    "risk_score": 0.15
  }
}
```

**Metrics extracted**:
- Pass/fail rate per rule
- Sanitization frequency and type
- Validation latency distribution
- Risk score distribution by branch type
- Most common violations (to prioritize rule tuning)

#### Event 3: Director Decision Made (`director_decision`)

**When**: Director evaluates a proposal and makes an accept/reject decision.

**Purpose**: Track Director heuristics and decision patterns.

##### Schema (web demo payload)

The web demo emits a **flat** `director_decision` payload (no nested `event_data` envelope) with these fields:

| Field | Type | Required | Notes |
|---|---:|:---:|---|
| `proposal_id` | string | ✅ | Correlates with proposal lifecycle events; falls back to a UUID if missing. |
| `decision` | string | ✅ | `approve` or `reject` (demo enums). |
| `reason` | string | ✅ | Human-readable rationale (e.g., `Risk acceptable`, `Return path check failed`). |
| `riskScore` | number | ✅ | Overall risk (0.0–1.0). Lower is better. |
| `latencyMs` | number | ✅ | Director evaluation latency (ms). |
| `writerMs` | number | ✅ | Writer latency passed in for telemetry (ms). |
| `directorMs` | number | ✅ | Same as `latencyMs` in the demo (ms). |
| `totalMs` | number | ✅ | `writerMs + directorMs`. |
| `timestamp` | string | ✅ | ISO timestamp generated at emission time. |
| `metrics.confidence` | number \| null | ❌ | Fit metric 0.0–1.0 (higher is better). |
| `metrics.pacing` | number \| null | ❌ | Fit metric 0.0–1.0 (higher is better). |
| `metrics.returnPath` | number \| null | ❌ | Fit metric 0.0–1.0 (higher is better). |
| `metrics.thematic` | number \| null | ❌ | Placeholder fit metric. |
| `metrics.lore` | number \| null | ❌ | Placeholder fit metric. |
| `metrics.voice` | number \| null | ❌ | Placeholder fit metric. |

##### Example

```json
{
  "event_type": "director_decision",
  "payload": {
    "proposal_id": "proposal-87f4c290",
    "decision": "approve",
    "reason": "Risk acceptable",
    "riskScore": 0.18,
    "latencyMs": 92,
    "writerMs": 240,
    "directorMs": 92,
    "totalMs": 332,
    "timestamp": "2026-01-20T14:30:22Z",
    "metrics": {
      "confidence": 0.87,
      "pacing": 0.12,
      "returnPath": 0.90,
      "thematic": null,
      "lore": null,
      "voice": null
    }
  }
}
```

##### Implementation note: buffering

In the web demo, `director_decision` events are buffered in **`sessionStorage`** under the key `ge-hch.director.telemetry` as a ring buffer of the **last 50 events**. This ensures:
- no server dependency for local dev
- events survive simple page navigations
- bounded memory vs `localStorage`

(If the buffer is cleared, only in-session telemetry is impacted; gameplay state is unaffected.)

**Design reference**: `docs/dev/m2-design/telemetry-schema.md` (this document) and `docs/dev/m2-design/director-algorithm.md` (Telemetry Emission section).

**Metrics extracted**:
- Risk score distribution
- Decision threshold sensitivity
- Engagement-to-creativity mapping effectiveness
- Director decision latency
- Success rate by risk metric
- Player preference prediction accuracy (compare predicted fit vs. actual engagement)
- Branch type preference trends across player segments

#### Event 3b: Placement Stage Outcome

**When**: Director attempts to place approved proposal into story script

**Purpose**: Track placement success rate, retry patterns, and deferred proposals

```json
{
  "event_type": "placement_outcome",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "placement_status": "placement_successful",
    
    "placement_details": {
      "insertion_points_found": 2,
      "best_confidence_score": 0.92,
      "placement_latency_ms": 180
    }
  }
}
```

OR (if placement failed and retrying):

```json
{
  "event_type": "placement_retry",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "retry_count": 1,
    "max_retries": 3,
    
    "failure_reason": "no_viable_insertion_points",
    "relevance_status": "still_relevant",
    
    "adjustments_applied": [
      "relaxed_thematic_threshold",
      "alternative_return_path"
    ],
    
    "retry_outcome": "placement_successful"
  }
}
```

OR (if deferred for future reuse):

```json
{
  "event_type": "placement_deferred",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "failure_reason": "story_progression_mismatch",
    "relevance_status": "no_longer_relevant",
    
    "current_story_position": "chapter_3.temple_entrance",
    "branch_required_position": "chapter_2.guard_encounter",
    
    "reuse_metadata": {
      "reuse_eligible": true,
      "applicable_story_phases": ["chapter_2"],
      "quality_score": 0.88
    },
    
    "storage_action": "archive_for_future_runs"
  }
}
```

**Metrics extracted**:
- Placement success rate
- Retry frequency and success rate after retry
- Deferral rate (proposals saved for future playthroughs)
- Story position mismatches (indicates timing issues in proposal generation)
- Average retries before success/deferral
- Reuse pool size and utilization

#### Event 4: Player Encounters Branch Choice

**When**: Branch is offered to player as a choice option

**Purpose**: Track branch presentation and player engagement

```json
{
  "event_type": "branch_choice_presented",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "presentation_context": "dialogue_choice",
    "hook_point": "scene_act2_campfire",
    
    "choice_offered": {
      "branch_title": "Lyra's Plea at Dusk",
      "branch_type": "companion_dialogue",
      "description_shown_to_player": "Lyra needs your help with something important."
    },
    
    "alternative_choices": [
      {
        "type": "main_story",
        "title": "Continue main story",
        "choice_id": "main_act2_choice_1"
      }
    ],
    
    "presentation_time_timestamp": "2026-01-20T14:35:10Z",
    "choice_presentation_latency_ms": 850  // Time from hook point to choice appearance
  }
}
```

**Metrics extracted**:
- Branch presentation latency
- Branch offer frequency by type
- Player demographics (level, play style) for each branch type
- Hook point utilization

#### Event 5: Player Accepts/Declines Branch

**When**: Player makes choice to accept or decline branch

**Purpose**: Track branch adoption rate and player preferences

```json
{
  "event_type": "branch_choice_made",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "player_choice": "accepted",
    "choice_deliberation_time_seconds": 12,
    
    "branch_integration": {
      "status": "integrated_successfully",
      "integration_latency_ms": 450
    }
  }
}
```

OR (if declined):

```json
{
  "event_type": "branch_choice_made",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "player_choice": "declined",
    "choice_deliberation_time_seconds": 3,
    "decline_reason": "player_chose_main_story"
  }
}
```

**Metrics extracted**:
- Acceptance rate by branch type
- Deliberation time distribution
- Acceptance rate by player level/style
- Acceptance rate by director creativity setting

#### Event 6: Branch Execution Outcome

**When**: Branch completes or encounters critical event

**Purpose**: Track branch quality, coherence perception, and errors

```json
{
  "event_type": "branch_execution_outcome",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "outcome_status": "completed_successfully",
    
    "branch_execution": {
      "start_time_timestamp": "2026-01-20T14:35:15Z",
      "end_time_timestamp": "2026-01-20T14:36:10Z",
      "execution_duration_seconds": 55,
      "expected_playtime_seconds": 55,
      "pacing_match": 0.98,
      
      "dialogue_choices_made": 2,
      "branch_outcome": "lyra_convinced_to_accept_help"
    },
    
    "player_engagement": {
      "player_actions": [
        {"action": "dialogue_choice_1", "timestamp": "+5s", "choice_text": "Tell me what's happening"},
        {"action": "dialogue_choice_2", "timestamp": "+30s", "choice_text": "We can take a detour"}
      ],
      "skip_count": 0,
      "reload_count": 0
    },
    
    "state_consistency": {
      "validation": "passed",
      "state_after_branch": {
        "player_position": "campfire",
        "lyra_disposition": 0.85,
        "quest_state_valid": true
      }
    },
    
    "errors": [],
    "rollback_occurred": false
  }
}
```

OR (if error occurred):

```json
{
  "event_type": "branch_execution_outcome",
  "event_data": {
    "proposal_id": "proposal-87f4c290",
    "outcome_status": "rollback_required",
    
    "branch_execution": {
      "execution_duration_seconds": 28,
      "dialogue_choices_made": 1
    },
    
    "errors": [
      {
        "error_type": "ink_divert_target_missing",
        "error_message": "Ink divert target 'npc_lyra_response_2a' does not exist in story",
        "occurred_at_dialogue_choice": 2,
        "execution_stage": "executing"
      }
    ],
    
    "rollback": {
      "rollback_occurred": true,
      "rollback_successful": true,
      "rollback_latency_ms": 120
    }
  }
}
```

**Metrics extracted**:
- Branch completion rate
- Actual vs. expected playtime (pacing accuracy)
- Player choice patterns
- Reload/skip frequency (sign of confusion or bug)
- Error rate and error types
- Rollback frequency and success rate

## Observability: Post-Launch Analysis Dashboard

### Dashboard View 1: Branch Generation Health

**Questions answered**:
- How many branches are being generated?
- What's the distribution of branch types?
- Are generation latencies acceptable?
- What's the confidence score distribution?

**Metrics displayed**:

```
┌─────────────────────────────────────────────────────────────┐
│ M2 BRANCH GENERATION HEALTH (Last 24 hours)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Total Proposals Generated: 1,247                            │
│ ├─ Dialogue Branches: 620 (49.7%)                          │
│ ├─ Combat Encounters: 280 (22.4%)                          │
│ ├─ Exploration Branches: 234 (18.8%)                       │
│ └─ Other: 113 (9.1%)                                       │
│                                                               │
│ Generation Latency:                                          │
│ ├─ P50: 1,850ms                                            │
│ ├─ P95: 3,200ms                                            │
│ └─ P99: 4,500ms                                            │
│                                                               │
│ Proposal Confidence Scores:                                  │
│ ├─ High (0.80+): 982 (78.7%)                               │
│ ├─ Medium (0.60-0.80): 234 (18.8%)                         │
│ └─ Low (<0.60): 31 (2.5%)                                  │
│                                                               │
│ Trend: ↑ Latency increasing (more complex proposals)       │
│        ↑ Confidence steady (quality maintained)            │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard View 2: Validation Effectiveness

**Questions answered**:
- Which rules are most frequently triggered?
- What's the sanitization rate?
- Is the risk threshold well-calibrated?

**Metrics displayed**:

```
┌─────────────────────────────────────────────────────────────┐
│ VALIDATION PIPELINE EFFECTIVENESS (Last 7 days)             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Pass Rate: 94.2%                                            │
│                                                               │
│ Most Common Rule Triggers:                                   │
│ 1. Character Voice Consistency: 4.2% of proposals          │
│ 2. Dialogue Length: 3.8%                                   │
│ 3. Lore Consistency: 2.1%                                  │
│ 4. Thematic Alignment: 1.9%                                │
│                                                               │
│ Sanitizations Applied:                                       │
│ ├─ Dialogue Trimming: 45 proposals (3.6%)                 │
│ ├─ Profanity Redaction: 12 (0.96%)                        │
│ └─ Tone Softening: 8 (0.64%)                              │
│                                                               │
│ Risk Score Distribution:                                    │
│ ├─ Low Risk (0.0-0.2): 1,050 (84.2%)                     │
│ ├─ Medium Risk (0.2-0.5): 170 (13.6%)                    │
│ └─ High Risk (0.5+): 27 (2.2%)                            │
│                                                               │
│ Insight: Rules are well-calibrated; false positive rate ✓  │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard View 3: Director Decision Patterns

**Questions answered**:
- Is the Director accepting good branches?
- Is the creativity parameter effective?
- What's the approval rate by player engagement level?

**Metrics displayed**:

```
┌─────────────────────────────────────────────────────────────┐
│ DIRECTOR DECISION ANALYSIS (Last 7 days)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Overall Approval Rate: 76.5%                                │
│                                                               │
│ Approval Rate by Risk Score:                                │
│ ├─ Low Risk (0.0-0.2): 94.1%                              │
│ ├─ Medium Risk (0.2-0.5): 52.4%                           │
│ └─ High Risk (0.5+): 18.5%                                │
│                                                               │
│ Creativity Parameter Effectiveness:                          │
│ ├─ Low Creativity (0.3): 89% approval, 78% player accept  │
│ ├─ Medium Creativity (0.6): 76% approval, 82% accept      │
│ └─ High Creativity (0.8): 62% approval, 68% accept        │
│                                                               │
│ Risk Metrics Correlation with Player Satisfaction:         │
│ ├─ Thematic Consistency: 0.87 (strong)                    │
│ ├─ Character Voice Match: 0.84 (strong)                   │
│ ├─ Lore Adherence: 0.81 (strong)                          │
│ └─ Narrative Pacing: 0.75 (moderate)                      │
│                                                               │
│ Recommendation: Increase creativity threshold for high     │
│                 engagement players (level 10+)             │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard View 4: Player Engagement & Adoption

**Questions answered**:
- Are players accepting branches?
- What types of branches are most popular?
- Do certain player demographics prefer branches?

**Metrics displayed**:

```
┌─────────────────────────────────────────────────────────────┐
│ PLAYER BRANCH ENGAGEMENT (Last 7 days)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Total Branch Choices Presented: 3,456                       │
│ Total Branches Accepted: 2,847 (82.3%)                     │
│                                                               │
│ Acceptance Rate by Branch Type:                             │
│ ├─ Dialogue Branches: 88.5% (high engagement)             │
│ ├─ Exploration Branches: 81.2%                            │
│ ├─ Combat Encounters: 74.5%                               │
│ └─ Moral Dilemmas: 69.2% (lowest engagement)              │
│                                                               │
│ Acceptance Rate by Player Level:                            │
│ ├─ Level 1-5: 78.6%                                       │
│ ├─ Level 6-10: 84.2%                                      │
│ ├─ Level 11-15: 81.5%                                     │
│ └─ Level 16+: 76.3%                                       │
│                                                               │
│ Deliberation Time:                                          │
│ ├─ Accepted branches: avg 8.2s                            │
│ ├─ Declined branches: avg 3.1s (quick rejections)         │
│                                                               │
│ Insight: Dialogue branches are most popular; consider     │
│          increasing dialogue branch generation rate       │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard View 5: Branch Execution Quality

**Questions answered**:
- Are branches executing without errors?
- Are branches as good as the main story?
- What's the perceived coherence/quality?

**Metrics displayed**:

```
┌─────────────────────────────────────────────────────────────┐
│ BRANCH EXECUTION QUALITY (Last 7 days)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Successful Completions: 2,742 (96.3%)                     │
│ Rollbacks: 87 (3.1%)                                       │
│ Declined at Last Moment: 18 (0.6%)                        │
│                                                               │
│ Rollback Reasons:                                           │
│ ├─ Ink Divert Target Missing: 34 (39.1%)                   │
│ ├─ State Inconsistency: 28 (32.2%)                        │
│ ├─ NPC Reference Error: 15 (17.2%)                        │
│ └─ Other: 10 (11.5%)                                      │
│                                                               │
│ Pacing Accuracy:                                            │
│ ├─ Actual vs. Predicted: 97.4% match                      │
│ ├─ Players who skipped dialogue: 2.1%                     │
│ ├─ Players who reloaded during branch: 1.3%               │
│                                                               │
│ Player Satisfaction (Implicit):                             │
│ ├─ Continued playing after branch: 94.8%                  │
│ ├─ No negative markers: 91.2%                             │
│ ├─ Accepted another branch immediately: 47.3%            │
│                                                               │
│ Critical Issue Found:                                       │
│ ⚠ Dialogue node errors at 39% of rollbacks. Investigate   │
│   Writer's dialogue generation and validation.            │
└─────────────────────────────────────────────────────────────┘
```

## Privacy and Data Handling Guidelines

### Sensitive Data to Redact

```python
def redact_sensitive_data(event: dict) -> dict:
    """Remove personally identifiable information from telemetry."""
    redacted = event.copy()
    
    # Always hash player_id (already anon in base schema)
    # Remove exact timestamps (use relative time instead)
    redacted['timestamp'] = redact_to_hour(event['timestamp'])
    
    # Redact dialogue text (keep only metadata)
    if 'branch_execution' in redacted:
        for choice in redacted['branch_execution'].get('player_actions', []):
            choice['choice_text'] = '[REDACTED]'  # Keep action type only
    
    # Redact character names if needed for GDPR compliance
    if 'choice_offered' in redacted:
        redacted['choice_offered']['description_shown_to_player'] = '[REDACTED]'
    
    return redacted
```

### Data Retention Policy

- **Real-time events**: 30 days in hot storage (analysis)
- **Aggregated metrics**: 1 year (trends)
- **Audit logs (with rollbacks)**: 2 years (compliance)
- **Raw events with rollback details**: 6 months (learning)

## Analysis Workflow for Phase 3 Iteration

### Week 1: Data Collection

- Collect telemetry from Phase 2 (first soft launch week)
- Ensure data quality; flag missing fields

### Week 2: Analysis

Conduct five analyses:

1. **Validation Effectiveness**: Which rules are most effective? False positive rate?
2. **Director Heuristics**: Are risk metrics well-calibrated? Should thresholds change?
3. **Player Adoption**: Which branch types are popular? Any demographic patterns?
4. **Execution Quality**: Error rate? Rollback causes? Generation quality?
5. **Engagement Impact**: Do branches increase playtime? Reduce churn?

### Week 3: Iteration Planning

Based on findings:

- Update validation rules (add new rules, tune severity levels)
- Adjust Director risk metric weights or thresholds
- Refine Writer prompt templates for underperforming branch types
- Prioritize LORE model improvements (if LORE context is insufficient)

### Week 4: Phase 3 Tuning

- Deploy updated Director, validation rules, and Writer prompts
- Monitor for improvement in key metrics

## Open Questions for Implementation

1. **Event Volume**: Estimate: 5–10 events per player per session. Storage needed? (Answer: ~500 MB/week for 10k concurrent players)
2. **Latency Impact**: Does telemetry collection add noticeable latency? (Answer: Async logging; <10ms impact)
3. **User Consent**: Explicit opt-in for telemetry? (Answer: Opt-out by default; respects privacy settings)
4. **Real-time Dashboarding**: Should dashboards update in real-time or batch? (Answer: 5-minute batches)
5. **Anomaly Detection**: Should automated alerts fire for error spikes? (Answer: Yes; alert if rollback rate > 5%)

---

**Status**: Telemetry schema and observability fully specified. Ready for implementation and Phase 2 launch. Key insight: Telemetry is the foundation for Phase 3 iteration; comprehensive event coverage is essential.
