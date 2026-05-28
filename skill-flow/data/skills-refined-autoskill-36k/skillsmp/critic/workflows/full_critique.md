# Workflow: Full Critique

Comprehensive adversarial review of a draft or collected evidence.

## Prerequisites
- Draft in `/workspace/drafts/current.md` OR
- Evidence in `/workspace/evidence.json`
- Hypotheses in `/workspace/hypotheses.json` (if any)

## Overview

Run all four critique modes in sequence:
1. Evidence Audit
2. Logic Audit  
3. Bias Audit
4. Black Swan Generation

Then synthesize findings.

---

## Phase 1: Evidence Audit

For EACH piece of evidence in `evidence.json`:

### Check Source Quality
| Question | Red Flag |
|----------|----------|
| Is this source authoritative for THIS claim? | General source making specific claim |
| Is the quote in context? | Cherry-picked excerpt |
| Is the methodology sound? | No methodology described |
| Is this primary or secondary? | Summary of a summary |
| How old is this? | Outdated for fast-moving field |

### Check Confidence Calibration
| Current Confidence | Appropriate If... |
|-------------------|-------------------|
| 0.9+ | Multiple independent authoritative sources |
| 0.7-0.9 | Single strong source OR multiple moderate |
| 0.5-0.7 | Plausible but not definitive |
| < 0.5 | Should be flagged, not used as foundation |

### Check Claim-Evidence Alignment
- Does the retrieved text ACTUALLY support the stated claim?
- Is the claim overstated relative to the evidence?
- Are there qualifications in the source that are missing in the claim?

### Record Evidence Critiques

```json
{
  "id": "cr_001",
  "target": "ev_003",
  "target_type": "evidence",
  "mode": "evidence_audit",
  "type": "insufficient_evidence",
  "severity": "high",
  "issue": "Single study from 2018; no replication found",
  "suggestion": "Search for replication studies or meta-analyses",
  "verification_needed": "Find independent confirmation of 23% effect size"
}
```

---

## Phase 2: Logic Audit

For each CLAIM or ARGUMENT in the draft:

### Fallacy Scan

Work through systematically:

**Confirmation Bias**
- Is evidence selected to support a predetermined conclusion?
- Where's the contradicting evidence?
- Critique if: Only supporting evidence, no complications

**Appeal to Authority**
- Is status substituting for argument?
- What's the actual reasoning?
- Critique if: "Expert says X" without explaining why X is true

**Circular Reasoning**
- Does the conclusion appear in the premises?
- Critique if: "X is true because Y, and Y is true because X"

**False Dichotomy**
- Are options artificially limited?
- Critique if: "Either A or B" when C, D, E also possible

**Straw Man**
- Is the opposing view fairly represented?
- Critique if: Weakest version of counterargument addressed

**Correlation ≠ Causation**
- Is causality assumed from correlation?
- Critique if: "X correlates with Y, therefore X causes Y"

**Post Hoc Fallacy**
- Is sequence assumed to be causation?
- Critique if: "Y happened after X, therefore X caused Y"

**Hasty Generalization**
- Is conclusion drawn from insufficient examples?
- Critique if: "One study showed..." → sweeping claim

### Record Logic Critiques

```json
{
  "id": "cr_005",
  "target": "Section 2.3",
  "target_type": "section",
  "target_text": "Since friction mechanisms were adopted, error rates declined by 40%",
  "mode": "logic_auditor",
  "type": "logical_fallacy",
  "severity": "medium",
  "issue": "Post hoc fallacy: temporal sequence doesn't prove causation",
  "suggestion": "Add alternative explanations or cite controlled study showing causation",
  "alternative_hypothesis": "Error rates may have declined due to concurrent training improvements"
}
```

---

## Phase 3: Bias Audit

### Check for Cherry-Picking
- Are results selectively reported?
- Are contradicting findings acknowledged?
- Is the evidence sample representative?

### Check for Motivated Reasoning
- Does the conclusion benefit the author?
- Is the argument suspiciously convenient?
- Would the conclusion change if evidence pointed the other way?

### Check for Missing Perspectives
- Whose voice is absent?
- What stakeholder's view isn't represented?
- What field might see this differently?

### Check for Framing Effects
- How does word choice shape perception?
- Would different framing lead to different conclusions?
- Are loaded terms used?

### Record Bias Critiques

```json
{
  "id": "cr_008",
  "target": "entire_draft",
  "target_type": "draft",
  "mode": "bias_hunter",
  "type": "missing_context",
  "severity": "medium",
  "issue": "No perspective from UX designers who might oppose friction",
  "suggestion": "Research and include the case against friction from user experience perspective"
}
```

---

## Phase 4: Black Swan Generation

Generate 3-5 scenarios where the thesis fails catastrophically.

### Scenario Template

For each scenario:
1. **Hidden assumption**: What assumption, if false, collapses the argument?
2. **Scenario**: Describe a plausible situation where this assumption fails
3. **Consequence**: What happens to the argument?
4. **Probability**: Low/Medium (Black Swans are rare but consequential)
5. **Mitigation**: How could the argument be hedged?

### Example Black Swans

```json
{
  "id": "cr_010",
  "target": "thesis",
  "target_type": "hypothesis",
  "mode": "counter_factualist",
  "type": "risk",
  "severity": "medium",
  "issue": "Black Swan: What if friction mechanisms get gamed?",
  "reasoning": "Users might learn to bypass friction ritualistically without engaging cognitively, making friction theater rather than substance",
  "alternative_hypothesis": "Over time, any friction mechanism becomes routinized and loses effectiveness",
  "suggestion": "Acknowledge this risk; cite evidence about friction mechanism decay over time"
}
```

---

## Phase 5: Synthesize

### Severity Summary

Count critiques by severity:
- BLOCKING: [count] — Must resolve before proceeding
- HIGH: [count] — Must resolve before finalizing
- MEDIUM: [count] — Should address
- LOW: [count] — Nice to fix

### Conflict Detection

Did any critiques reveal:
- Direct contradictions between evidence?
- Unresolvable tensions in the argument?
- Claims that can't be supported?

If yes → Flag CONFLICT_DETECTED, recommend LATERAL mode.

### Alternative Ruling Check

For contested claims, did you generate:
- Consensus View?
- Contrarian View?

If not, do so now.

### Overall Assessment

```
DRAFT QUALITY: Weak | Moderate | Strong

Key Strengths:
- [list what works]

Critical Issues (BLOCKING/HIGH):
- [list with cr_ids]

Main Recommendations:
1. [priority action]
2. [priority action]
3. [priority action]

Recommended Next Step: 
- [ ] Return to RESEARCHER for verification
- [ ] Proceed to LATERAL for conflict resolution
- [ ] Proceed to WRITER for revision
```

---

## Update State

After completing critique:

```json
{
  "current_state": "critiquing",
  "critique_summary": {
    "blocking": 0,
    "high": 3,
    "medium": 5,
    "low": 2,
    "conflicts_detected": false,
    "ready_for_revision": true
  }
}
```

If BLOCKING issues: State remains "critiquing" until resolved.
If conflicts detected: State becomes "conflict_detected".
If clear: State can move to "revising".
