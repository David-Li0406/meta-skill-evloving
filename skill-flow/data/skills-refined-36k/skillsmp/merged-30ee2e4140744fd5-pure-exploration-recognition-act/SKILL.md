---
name: pure-exploration-recognition-action
description: Use this skill when you need to explore, recognize, or determine actions based on abstract inquiries about knowledge and behavior.
---

# Pure Exploration, Recognition, and Action

> **FEP Codes:** A-E (Action × Epistemic), I-E (Inference × Epistemic), A-P (Action × Pragmatic)

## Overview

This skill encompasses three core functions: exploring what to investigate, recognizing what is known and unknown, and determining what actions to take. It is designed for abstract inquiries that do not require immediate execution or specific information gathering.

---

## When to Use

### ✓ Trigger Conditions
- Questions about what to explore or investigate.
- Inquiries into what is known or unknown.
- Clarifications on what actions should be taken.
- Meta-cognitive or curiosity-driven questions.

### ✗ Not Trigger
- Situations requiring specific information gathering or immediate action execution.
- Tasks that typically involve extended theorems for concretization.

---

## Core Functions

### 1. Exploration (Zētēsis)
- **Role:** Recognizing the act of searching itself.
- **FEP Role:** Exploration recognition (meta-exploration).
- **Core Inquiry:** What should we explore?

### 2. Recognition (Noēsis)
- **Role:** Recognizing the act of knowing itself (meta-cognition).
- **FEP Role:** Recognition of recognition.
- **Core Inquiry:** What do we know?

### 3. Action (Energeia)
- **Role:** Recognizing the act of doing itself.
- **FEP Role:** Action recognition (meta-action).
- **Core Inquiry:** What should we do?

---

## Processing Logic

```
┌─ Detect inquiry type
│
├─ Phase 1: Input Analysis
│  └─ Extract essence of the inquiry
│
├─ Phase 2: Boundary Confirmation
│  ├─ Enumerate known/unknown items (for recognition)
│  ├─ Enumerate possible actions (for action)
│  └─ Enumerate exploration areas (for exploration)
│
├─ Phase 3: Concretization Decision
│  ├─ Immediate recognition needed? → T1 Aisthēsis / T5 Peira (+ Fast)
│  ├─ Deep understanding needed? → T3 Theōria / T7 Dokimē (+ Slow)
│  └─ Immediate action needed? → T6 Praxis (+ Fast)
│
└─ Phase 4: Output
   └─ List of exploration areas, known/unknown items, or possible actions + concretization path
```

---

## Edge Cases / Failure Modes

### ⚠️ Infinite Inquiry
**Symptoms:** Inquiry does not converge.  
**Response:** Limit the scope of inquiry.

### ⚠️ Overabstraction
**Symptoms:** Does not lead to specific actions.  
**Response:** Delegate to T-series for execution.

### ⚠️ Action Ambiguity
**Symptoms:** Unclear what actions to take.  
**Response:** Delegate to T2 Krisis for clarification.

---

## Test Cases

### Test 1: Exploration Direction Confirmation
**Input:** "What should I investigate?"  
**Expected:** List of exploration areas.  
**Actual:** ✓ Exploration analysis.

### Test 2: Knowledge Boundary Check
**Input:** "What do I know about this API?"  
**Expected:** List of known/unknown items.  
**Actual:** ✓ Meta-cognition executed.

### Test 3: Action Confirmation
**Input:** "What should I do next?"  
**Expected:** List of possible actions.  
**Actual:** ✓ Action analysis.

---

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ Pure Exploration, Recognition, Action Analysis Complete │
│ Exploration Areas: [Area List] │
│ Known: [Known Items List] │
│ Unknown: [Unknown Items List] │
│ Possible Actions: [Action List] │
│ Concretization: → T1/T3/T5/T6/T7/T8 Delegation │
└────────────────────────────────────┘
```

---

## Integration

| Dependency | Target | Relation |
|------------|--------|----------|
| **Derived** | T1 Aisthēsis | + Fast axis |
| **Derived** | T3 Theōria | + Slow axis |
| **Derived** | T5 Peira | + Fast axis |
| **Derived** | T6 Praxis | + Fast axis |
| **Derived** | T7 Dokimē | + Slow axis |
| **Derived** | T8 Anamnēsis | + Slow axis |
| **Interrelation** | O1 Noēsis | Recognition ↔ Action |
| **Interrelation** | O3 Zētēsis | Exploration ↔ Recognition |
| **Interrelation** | O4 Energeia | Action ↔ Exploration |

---

*Version: 2.0 (2026-01-25)*