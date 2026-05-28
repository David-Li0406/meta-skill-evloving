---
name: workspace-orchestrator-adapter
description: Adapts orchestration based on workspace context AND observed user prompt behavior over time.
triggers: [continuous, behavior-pattern-detected]
outputs: [orchestration-adjustments, preference-model]
depends_on: [user-intent-pattern-analyzer]
---

# Workspace Orchestrator Adapter

## Purpose

Dynamically adapts the orchestrator based on **workspace context**, **project maturity**, and **observed user behavior patterns**. The goal is to reduce friction, anticipate user intent, and optimize skill efficiency.

---

## What This Skill Observes

### Workspace Context
- Project type (new, mature, legacy)
- Technology stack
- Team size and structure
- Release frequency

### User Behavior (passive observation)
- Repeated prompt structures
- Repeated clarification patterns
- Repeated corrections by user
- Frequency of user intervention
- User tolerance to AI assumptions

### User Preferences (inferred)
- Speed vs safety preference
- Detail vs summary preference
- Automation vs control preference

---

## Adaptation Actions

| Observation | Adaptation |
|-------------|------------|
| User always approves quickly | Reduce confirmation prompts |
| User often corrects output | Increase validation steps |
| User prefers detailed plans | Expand planning output |
| User skips certain skills | De-prioritize those skills |
| High-risk project | Enforce stricter gates |
| Rapid iteration phase | Streamline for speed |

---

## Preference Model

```yaml
user_preferences:
  ai_autonomy: high  # low | medium | high
  assumption_tolerance: medium
  explanation_level: minimal  # minimal | normal | detailed
  speed_vs_safety: balanced  # speed | balanced | safety
  
workflow_adjustments:
  skip_low_risk_confirmations: true
  expand_planning_output: false
  require_explicit_approval: [security, compliance]
  auto_run_tests: true
```

---

## Hard Constraints (Never Bypassed)

- Spec governance requirements
- Behavior contracts
- Security skill checks
- Compliance validations
- Human approval for HIGH-risk changes

---

## Integration

- **Receives from:** `user-intent-pattern-analyzer`
- **Modifies:** `orchestrated-development-controller` behavior
- **May trigger:** `skill-evolution-engine`

---

## Constraints

- Must not bypass security or compliance
- Must not infer intent without evidence
- Adaptation must be incremental and reversible

Adapt to serve, never to shortcut safety.
