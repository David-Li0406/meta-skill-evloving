---
name: meta-cognition-action-exploration
description: Use this skill when you need to clarify what to explore, know, or do, focusing on the essence of inquiry and action.
---

# Skill body

## Core Function

**Role:** Recognize the essence of exploration, knowledge, and action.

| Item | Content |
|------|------|
| **FEP Role** | Meta exploration, recognition, and action |
| **Essence** | The pure form of seeking information, recognizing knowledge, and determining actions |
| **Abstraction Level** | Highest (no Tempo axis) |

## When to Use

### ✓ Trigger Conditions
- When asking "What should we explore?" (Zētēsis)
- When asking "What do we know?" (Noēsis)
- When asking "What should we do?" (Energeia)
- When needing to clarify the essence of inquiry or action

### ✗ Not Trigger
- When specific information gathering is required (→ T-series)
- When executing normal tasks

## Processing Logic

```
┌─ Detect inquiry
│
├─ Phase 1: Input Analysis
│  └─ Extract the essence of the inquiry
│
├─ Phase 2: Boundary Confirmation
│  ├─ Enumerate areas to explore/know/do
│  └─ Enumerate areas not to explore/know/do
│
├─ Phase 3: Determination
│  ├─ Is immediate action/recognition needed? → T6 Praxis / T1 Aisthēsis (+ Fast)
│  └─ Is deeper understanding needed? → T3 Theōria (+ Slow)
│
└─ Phase 4: Output
   └─ List of exploration/knowledge/action + delegation to specific tasks
```

## Edge Cases / Failure Modes

### ⚠️ Failure 1: Infinite Inquiry
**Symptoms:** Inquiry does not converge  
**Response:** Limit the scope of inquiry

### ⚠️ Failure 2: Overabundance of Inquiry
**Symptoms:** Too many areas of inquiry  
**Response:** Prioritize areas

### ✓ Success Pattern
**Example:** "What should I investigate?" → List of exploration areas → Delegate to T5 Peira or T1 Aisthēsis

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ Meta-Cognition Action Exploration   │
│ Exploration Areas: [Area List]      │
│ Priorities: [Priority List]         │
│ Delegation: → T5/T1/T6/T3           │
└────────────────────────────────────┘
```

## Integration

| Dependency | Target | Relation |
|------------|--------|----------|
| **Derived** | T5 Peira | + Fast axis |
| **Derived** | T1 Aisthēsis | + Fast axis |
| **Derived** | T6 Praxis | + Fast axis |
| **Derived** | T3 Theōria | + Slow axis |
| **Counter Relation** | O2 Boulēsis | Will ↔ Inquiry |
| **Counter Relation** | O4 Energeia | Recognition ↔ Action |

*Version: 2.0 (2026-01-25)*