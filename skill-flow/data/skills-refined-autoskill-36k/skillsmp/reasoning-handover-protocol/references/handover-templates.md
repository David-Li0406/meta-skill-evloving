# Handover Templates Reference

Quick-reference templates for pattern-to-pattern handovers.

## Common Handover Scenarios

### Scenario 1: BoT to ToT (Explore then Optimize)

**When**: After broad exploration, need to find optimal solution among top candidates.

**BoT Prepares**:
```json
{
  "deliverables": {
    "type": "approaches",
    "items": [
      {"id": "approach-1", "name": "...", "confidence": 0.72},
      {"id": "approach-2", "name": "...", "confidence": 0.78},
      {"id": "approach-3", "name": "...", "confidence": 0.68}
    ]
  },
  "recommendations": {
    "focus_areas": ["Top 3 approaches need comparative evaluation"],
    "evaluation_criteria": ["latency", "cost", "scalability"],
    "avoid_areas": ["Pruned approaches had fatal blockers"]
  }
}
```

**ToT Receives**:
- Start at Step 1 with pre-defined approaches
- Use BoT's retained approaches as Level 0 branches
- Apply ToT evaluation criteria to score and rank

---

### Scenario 2: ToT to AR (Select then Validate)

**When**: After finding optimal solution, need adversarial validation before implementation.

**ToT Prepares**:
```json
{
  "deliverables": {
    "type": "winning_solution",
    "items": [
      {
        "path": "L0:JWT > L1:RS256 > L2:JWKS > L3:Vault",
        "score": 91,
        "confidence": 0.88
      }
    ]
  },
  "recommendations": {
    "focus_areas": ["Security boundaries", "Failure modes", "Edge cases"],
    "key_assumptions": ["Vault availability > 99.9%", "Network latency < 10ms"],
    "avoid_areas": ["Alternative architectures - already evaluated"]
  }
}
```

**AR Receives**:
- Clear target specification from ToT winning path
- Key assumptions to challenge
- Pre-identified concerns to investigate

---

### Scenario 3: HE to ToT (Diagnose then Fix)

**When**: After identifying root cause, need to evaluate fix options.

**HE Prepares**:
```json
{
  "deliverables": {
    "type": "root_cause",
    "items": [
      {
        "hypothesis": "H3",
        "name": "External API timeout",
        "confidence": 0.85,
        "mechanism": "Payment gateway P99 increased from 50ms to 800ms"
      }
    ]
  },
  "recommendations": {
    "focus_areas": ["Mitigation strategies for external API dependency"],
    "constraint": "Cannot change payment gateway vendor (contract)",
    "open_questions": ["Acceptable latency degradation?", "Budget for additional infra?"]
  }
}
```

**ToT Receives**:
- Problem now well-defined: "How to mitigate external API latency"
- Constraints from HE investigation
- Can generate fix approaches as Level 0 branches

---

### Scenario 4: SRC to HE (Trace hits dead end)

**When**: Sequential trace backtracked too many times, need hypothesis-based approach.

**SRC Prepares**:
```json
{
  "deliverables": {
    "type": "partial_trace",
    "items": [
      {"step": 1, "result": "Event handler found", "confidence": 0.92},
      {"step": 2, "result": "Calls validateForm()", "confidence": 0.88},
      {"step": 3, "result": "BACKTRACK - logic unclear", "confidence": 0.35}
    ]
  },
  "recommendations": {
    "focus_areas": ["Validation logic is the uncertainty point"],
    "known_good": ["Event handler routing is correct", "Form submission triggers handler"],
    "hypothesis_seeds": [
      "Validation passes incorrectly",
      "Validation throws silently",
      "Race condition in validation"
    ]
  }
}
```

**HE Receives**:
- Partial trace narrows hypothesis space
- Step 3 failure suggests validation-related hypotheses
- Can generate targeted hypotheses around validation

---

### Scenario 5: AR to HE (Attack succeeds, find vulnerability source)

**When**: Adversarial attack succeeded, need to find how vulnerability was introduced.

**AR Prepares**:
```json
{
  "deliverables": {
    "type": "successful_attack",
    "items": [
      {
        "attack": "ATK-001",
        "name": "JWT algorithm confusion",
        "impact": 5,
        "exploit_path": "Change alg RS256->HS256, sign with public key"
      }
    ]
  },
  "recommendations": {
    "focus_areas": ["When was algorithm validation removed?", "Was it ever present?"],
    "investigation_scope": ["JWT middleware", "Auth library version", "Recent changes"],
    "hypothesis_seeds": [
      "Algorithm validation never implemented",
      "Removed during refactoring",
      "Library upgrade changed behavior",
      "Configuration override disables validation"
    ]
  }
}
```

**HE Receives**:
- Specific vulnerability to trace
- Pre-seeded hypotheses from AR attack analysis
- Clear success criteria: find when/how vulnerability was introduced

---

## Handover Confidence Adjustments

### Confidence Transfer Rules

| Scenario | Adjustment | Rationale |
|----------|------------|-----------|
| Scope narrowing (BoT to ToT) | -5% | Information loss from pruning |
| Scope expansion (HE to BoT) | -10% | Moving from focused to broad |
| Same scope (ToT to AR) | -3% | Information transfer loss |
| Parallel merge (agreement) | +5% | Independent validation |
| Parallel merge (disagreement) | -10% | Uncertainty revealed |
| Long session (>2 hours) | -5% | Cognitive fatigue assumption |
| Multiple backtracks (SRC) | -10% | Uncertainty in chain |

### Confidence Floor

Never transfer confidence below 0.40. If calculated transfer drops below 0.40:
1. Document why confidence is low
2. Recommend re-exploration before continuing
3. Consider decomposing problem into smaller parts

### Confidence Ceiling

Never transfer confidence above 0.90. Even with high-confidence results:
1. Shared assumption discount (-5%) applies
2. Unknown unknowns always exist
3. Cap at 0.90 until real-world validation

---

## Evidence Handover Checklist

When handing off, ensure evidence includes:

- [ ] **Source**: Where evidence came from (logs, metrics, code, external)
- [ ] **Timestamp**: When evidence was gathered
- [ ] **Summary**: One-sentence finding
- [ ] **Impact**: Which hypotheses/branches affected
- [ ] **File Path**: If evidence is a file, include path
- [ ] **Reproducibility**: Can this evidence be re-gathered?

---

## Quick Reference: Pattern Compatibilities

| From Pattern | Best Handoff To | Rationale |
|--------------|-----------------|-----------|
| BoT | ToT, HE | Exploration complete, need optimization or diagnosis |
| ToT | AR, SRC | Optimal solution found, need validation or implementation trace |
| HE | ToT, SRC | Root cause found, need fix evaluation or trace verification |
| SRC | HE, ToT | Trace complete or stuck, need hypothesis or branch evaluation |
| AR | HE, ToT | Attack found, need vulnerability trace or fix evaluation |
| DR | ToT, NDF | Synthesis achieved, need optimization or stakeholder alignment |
| AT | BoT, ToT | Analogy found, need validation via exploration or optimization |
| RTR | HE, ToT | Triage complete, need deep analysis or fix evaluation |
| NDF | ToT, DR | Stakeholders aligned, need optimization or resolve remaining tensions |

---

## Anti-Patterns to Avoid

### 1. Handover Without State

**Bad**:
```json
{
  "message": "BoT found some good options, ToT should evaluate them"
}
```

**Good**:
```json
{
  "deliverables": {
    "type": "approaches",
    "items": [/* full approach data */]
  },
  "confidence_transfer": {/* proper calculation */}
}
```

### 2. Losing Evidence Chain

**Bad**: Starting ToT with just approach names, losing BoT's analysis.

**Good**: Include full exploration data, evidence references, and pruning rationale.

### 3. Confidence Inflation

**Bad**: Each pattern adds confidence, ending at 99%.

**Good**: Use IR-v2 confidence aggregation rules with shared assumption discount.

### 4. Handover Without Checkpoint

**Bad**: Handover without creating checkpoint first.

**Good**: Always checkpoint before handover to enable recovery if target pattern fails.

### 5. Ignoring Pattern Recommendations

**Bad**: ToT ignores BoT's "avoid_areas" and re-explores pruned approaches.

**Good**: Trust previous pattern's conclusions unless new evidence emerges.
