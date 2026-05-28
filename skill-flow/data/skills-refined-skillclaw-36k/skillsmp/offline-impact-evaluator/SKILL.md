---
name: offline-impact-evaluator
description: Validate proposed stack against offline requirements. Use after initial stack proposal to identify gaps, assess complexity, and recommend adjustments.
---

# Offline Impact Evaluator

Validate the proposed stack against the offline requirement captured in architecture-refinement. Identify gaps, assess if the solution is over-engineered, and recommend stack adjustments when needed.

## Standalone Usage

Can be invoked directly:
- "Does this stack support session-durable offline?"
- "Evaluate offline capability of Next.js + Supabase"
- "Is this architecture over-engineered for transient offline?"

## Prerequisites

Requires:
- **Architecture brief** with `offline_requirement.level`
- **Stack candidates** from candidate-generator

## Evaluation Process

### Step 1: Map Required vs. Actual Capability

| Required Level | Minimum Actual Capability |
|----------------|---------------------------|
| `none` | No offline logic needed |
| `transient` | In-memory buffering, retry logic, graceful degradation |
| `session_durable` | IndexedDB/SQLite, background sync, service worker |
| `strong_offline_first` | CRDT/event sourcing, conflict resolution, guaranteed sync |

### Step 2: Assess Each Stack Component

For each candidate, evaluate:

| Component | Offline Consideration |
|-----------|----------------------|
| **Frontend** | Service worker support, offline detection, UI graceful degradation |
| **Data Layer** | Local storage technology, query capability offline |
| **Sync** | Background sync API, conflict resolution strategy |
| **Auth** | Token caching, session persistence, refresh handling |

### Step 3: Gap Analysis

Identify:
- **Under-delivery**: Required capability not met
- **Over-engineering**: Unnecessary complexity for the requirement
- **Risk areas**: Components with weak offline story

### Step 4: Recommendations

If gaps exist:
1. Recommend component swaps or additions
2. Estimate implementation complexity delta
3. Flag if cost re-evaluation is needed

## Offline Technology Reference

| Strategy | Persistence | Sync | Complexity | Use Case |
|----------|-------------|------|------------|----------|
| **Cache-only** | None | None | Low | Static assets, read-only data |
| **IndexedDB** | Session+ | Manual/BG | Medium | Transactional local data |
| **SQLite (WASM)** | Session+ | Manual | Medium-High | Complex queries offline |
| **Event Queue** | Durable | BG Sync | Medium | Action buffering |
| **CRDT** | Durable | Automatic | High | Real-time collaboration, conflict-free |

## Output Contract

```yaml
offline_impact_evaluation:
  stack_id: "<reference>"
  
  requirement:
    level: "<none|transient|session_durable|strong_offline_first>"
    session_close_behavior: "<loses_data|persists_locally>"
    sync_strategy: "<none|background_sync|manual_sync|crdt>"
  
  assessment:
    actual_level: "<none|transient|session_durable|strong_offline_first>"
    components:
      frontend:
        capability: "<level>"
        notes: "<details>"
      data_layer:
        capability: "<level>"
        technology: "<what provides offline>"
      sync:
        capability: "<level>"
        strategy: "<how sync works>"
  
  gap_analysis:
    has_gap: true|false
    gap_description: "<what's missing>"
    over_engineered: true|false
    over_engineering_notes: "<why it's excessive>"
  
  risks:
    - risk: "<risk description>"
      severity: "<low|medium|high>"
      mitigation: "<how to address>"
  
  recommendations:
    - action: "<what to change>"
      component: "<which component>"
      impact:
        cost: "<increase|decrease|same>"
        complexity: "<increase|decrease|same>"
        timeline: "<increase|decrease|same>"
  
  verdict:
    stack_viable: true|false
    requires_stack_change: true|false
    requires_cost_reevaluation: true|false
```

## Example: Gap Analysis

```yaml
offline_impact_evaluation:
  stack_id: "next-vercel-supabase"
  
  requirement:
    level: "session_durable"
    session_close_behavior: "persists_locally"
    sync_strategy: "background_sync"
  
  assessment:
    actual_level: "transient"
    components:
      frontend:
        capability: "transient"
        notes: "No service worker configured by default"
      data_layer:
        capability: "none"
        technology: "Server-side only"
      sync:
        capability: "none"
        strategy: "N/A"
  
  gap_analysis:
    has_gap: true
    gap_description: "Stack lacks local persistence and background sync"
    over_engineered: false
  
  risks:
    - risk: "Data loss on network interruption"
      severity: "high"
      mitigation: "Add IndexedDB layer with sync"
  
  recommendations:
    - action: "Add @tanstack/query with offline persistence"
      component: "data_layer"
      impact:
        cost: "same"
        complexity: "increase"
        timeline: "increase"
    - action: "Implement service worker for caching"
      component: "frontend"
      impact:
        cost: "same"
        complexity: "increase"
        timeline: "increase"
  
  verdict:
    stack_viable: true
    requires_stack_change: false
    requires_cost_reevaluation: false
```

## Integration Points

- **Invoked by**: stack-evaluation (after candidate-generator)
- **May trigger**: Cost re-evaluation if `requires_cost_reevaluation: true`
- **Feeds into**: implementation-plan (offline phase planning)
