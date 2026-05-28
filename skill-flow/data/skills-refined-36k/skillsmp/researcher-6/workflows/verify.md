# Workflow: Verify

Targeted verification of specific claims flagged by the Critic or marked low-confidence.

## Prerequisites
- Specific claim(s) to verify
- Usually triggered by CRITIC mode flagging "verification_needed"

## Input

Either from `/workspace/critiques.json`:
```json
{
  "verification_needed": "Find replication studies for the 23% automation bias reduction claim"
}
```

Or direct request:
```
Verify: "Cognitive friction improves decision quality in high-stakes domains"
```

## Steps

### 1. Clarify the Claim

State exactly what needs verification:
- The specific claim
- The current evidence supporting it
- The current confidence level
- What would raise/lower confidence

### 2. Define Verification Criteria

What would CONFIRM this claim?
- Replication studies
- Independent sources agreeing
- Meta-analyses
- Primary data

What would REFUTE this claim?
- Contradicting studies
- Failed replications
- Methodological critiques
- Alternative explanations fitting the data

### 3. Targeted Search

Search specifically for:

**Confirmation searches:**
```
web_search("[claim keywords] meta-analysis")
web_search("[claim keywords] replication")
web_search("[original author] [topic] confirmed")
```

**Refutation searches:**
```
web_search("[claim keywords] criticism OR critique")
web_search("[claim keywords] failed OR disproven")
web_search("[claim keywords] alternative explanation")
```

**Context searches:**
```
web_search("[claim keywords] boundary conditions")
web_search("[claim keywords] when does it fail")
web_search("[claim keywords] limitations")
```

### 4. Evaluate New Evidence

For each new source:

| Question | Answer |
|----------|--------|
| Does it directly address the claim? | |
| Is it independent of original source? | |
| What's the source quality? | |
| Does it confirm, refute, or complicate? | |
| Does it reveal boundary conditions? | |

### 5. Update Evidence

Add new evidence to `/workspace/evidence.json`:

```json
{
  "id": "ev_015",
  "claim": "The 23% reduction replicates in financial decision contexts",
  "source": {...},
  "confidence": 0.75,
  "retrieval_path": [
    "verification_search: cognitive forcing functions replication",
    "web_fetch: ..."
  ],
  "verification_of": "ev_003",
  "verification_result": "partial_confirmation",
  "notes": "Replicated in finance, but effect size was smaller (18%)"
}
```

### 6. Adjust Confidence

Based on verification results:

| Finding | Confidence Adjustment |
|---------|----------------------|
| Multiple independent confirmations | +0.2 |
| Single strong confirmation | +0.1 |
| Reveals boundary conditions | -0.1 (but more accurate) |
| Methodological concerns raised | -0.15 |
| Direct contradiction found | -0.3 or flag for LATERAL |
| Failed replication | -0.25 |

Update the original evidence item's confidence score.

### 7. Resolve or Escalate

**If verified (confidence now ≥ 0.7):**
- Update `/workspace/critiques.json` to mark resolved
- Note verification in evidence

**If refuted (confidence now ≤ 0.3):**
- Flag for removal from argument
- Note what was learned
- Consider: Does this change the thesis?

**If complicated (mixed evidence):**
- Document both sides
- Trigger Alternative Ruling Protocol
- Generate both Consensus and Contrarian views
- Consider escalating to LATERAL mode

### 8. Report Verification Result

```json
{
  "verification_request": "Find replication studies for automation bias claim",
  "original_claim": "ev_003",
  "original_confidence": 0.65,
  "searches_conducted": [
    "cognitive forcing replication study",
    "automation bias reduction meta-analysis",
    "diagnostic timeout criticism"
  ],
  "new_evidence_found": ["ev_015", "ev_016"],
  "result": "partial_confirmation",
  "new_confidence": 0.75,
  "notes": "Replicates in medical and financial contexts; effect size varies; no evidence for consumer contexts",
  "remaining_uncertainty": "Unclear if generalizes beyond expert decision-making"
}
```

## Verification Principles

1. **Seek disconfirmation**: Actively look for what would prove the claim wrong
2. **Independence matters**: 10 sources citing each other = 1 source
3. **Methodology over conclusion**: A well-designed study that complicates is better than a weak study that confirms
4. **Boundary conditions are valuable**: Learning when something is true/false is progress
5. **Update, don't anchor**: Be willing to significantly revise confidence

## When to Stop

Verification is complete when:
- [ ] At least 3 independent sources consulted
- [ ] Both confirmation and refutation actively sought
- [ ] Confidence level is justified by evidence
- [ ] Boundary conditions documented
- [ ] Remaining uncertainty is explicit
