# Evidence Synthesis V2

Tier-aware evidence weighting with generator validation integration.

---

## The Five Evidence Tiers

### Tier 1: Experimental Evidence (Weight: 40%)

**What counts:**
- Direct experimental confirmation
- Reproducible measurements
- Quantitative predictions verified
- Independent replication

**Scoring:**
```
3+ independent replications: 1.0
1-2 replications: 0.5
Preliminary data: 0.3
No data: 0.0
```

**Generator relevance:** G4 (Independent Validation)

**Examples:**
- ✓ Toroidal EM fields measured in heart (McFadden 2002)
- ✓ φ-ratio in brain structure (multiple studies)
- ✗ Consciousness field Ψ (not yet directly measured)

---

### Tier 2: Novel Predictions (Weight: 25%)

**What counts:**
- Framework predicts something not in inputs
- Differentiates from alternatives
- Testable (even if not yet tested)
- Specific and falsifiable

**Scoring:**
```
5+ predictions, 3+ confirmed: 1.0
3-5 predictions, 1+ confirmed: 0.6
1-2 predictions, awaiting test: 0.3
No novel predictions: 0.0
```

**Generator relevance:** G2 (Needs Contrast with alternatives)

**Examples:**
- ✓ Ψ ∝ Φ² relation (novel, awaiting test)
- ✓ Field disruption affects consciousness (testable)
- ○ IN(f) correlates with awareness (IIT already predicts)

---

### Tier 3: Explanatory Unity (Weight: 15%)

**What counts:**
- Number of domains unified
- Depth of unification (isomorphism vs analogy)
- Complexity reduction
- Cross-tier resonances

**Scoring:**
```
5+ domains, deep isomorphism: 1.0
3-4 domains, structural correspondence: 0.7
2 domains, clear connection: 0.4
Single domain or surface analogy: 0.0
```

**Generator relevance:** G1 (Iteration across scales), G3 (Morpheme closure)

**Examples:**
- ✓ Consciousness + EM fields + toroidal geometry + mathematics (4 domains)
- ✓ Structural isomorphism (not just analogy)
- ✓ Reduces to single principle (IN(f))

---

### Tier 4: Internal Consistency (Weight: 10%)

**What counts:**
- Logical coherence (no contradictions)
- Mathematical validity
- Reduces to known physics in limits
- Generator consistency

**Scoring:**
```
Fully consistent: 1.0
Minor inconsistencies (addressable): 0.5
Major contradictions: 0.0
```

**Generator relevance:** G5 (Mathematical Truth), G6 (Maintained distinctions)

**Note:** Necessary but not sufficient!

---

### Tier 5: Aesthetic Elegance (Weight: 5%)

**What counts:**
- Morphemic compression
- Conceptual simplicity
- Mathematical beauty
- Intuitive appeal

**Scoring:**
```
3+ aesthetic criteria: 1.0
2 criteria: 0.6
1 criterion: 0.3
None: 0.0
```

**Generator relevance:** G3 (Morpheme closure), G7 (φ-scaling beauty)

**Warning:** Lowest reliability tier. Beautiful theories can be wrong!

---

## Confidence Calculation

```
Base_Confidence = Σ(Tier_Score_i × Weight_i)

Example:
  T1: 0.0 × 0.40 = 0.00  (no experiments)
  T2: 0.6 × 0.25 = 0.15  (3 predictions, 1 confirmed)
  T3: 0.7 × 0.15 = 0.105 (4 domains, isomorphism)
  T4: 1.0 × 0.10 = 0.10  (fully consistent)
  T5: 1.0 × 0.05 = 0.05  (high aesthetic)
  
  Base = 0.405 (40.5%)

Generator_Factor = (generators_applying / 7) × 0.15
  6/7 × 0.15 = 0.129
  
State_Factor:
  Focused: 1.0
  Diversified: 0.9
  Biased: 0.7
  Dispersed: 0.5

Final_Confidence = Base × (1 + Generator_Factor) × State_Factor
  0.405 × 1.129 × 1.0 = 0.457 → 46%

Maximum: 50% (cap until independent experimental validation)
```

---

## Multi-Source Evidence Integration

### Independence Weighting

**Principle:** Evidence from independent sources weighs more

```
Single source: weight = 1.0
Two independent sources: weight = 1.5
Three independent sources: weight = 2.0
Each additional: weight += 0.3

But maximum weight = 3.0 (diminishing returns)
```

**What counts as "independent":**
- Different research teams
- Different methodologies
- Different domains/disciplines
- Different underlying assumptions

---

### Disconfirmation Seeking

**Principle:** Actively look for what contradicts framework

```
For each claim:
  1. What would falsify this?
  2. Has anyone tested that?
  3. What's the strongest counter-evidence?
  4. How do we explain it?

If can't explain counter-evidence:
  → Lower confidence
  → Revise framework
  → Or accept limitation
```

**Disconfirmation weight:**
```
No known counter-evidence: confidence ×1.0
Weak counter-evidence (explained): confidence ×0.9
Moderate counter-evidence: confidence ×0.7
Strong counter-evidence: confidence ×0.5 or revise
```

---

### Convergence Bonus

**Principle:** Multiple independent paths to same conclusion increases confidence

```
Single derivation: bonus = 1.0
Two derivations (different methods): bonus = 1.2
Three+ derivations: bonus = 1.4

Generator requirement: G4 must apply (independent validation)
```

**Example:**
```
Ψ ∝ Φ² derived from:
  1. IN(f) information integration principle
  2. Toroidal field recursion dynamics  
  3. Observer/observed distinction requirements

Three independent paths → convergence bonus 1.4
Confidence: base × 1.4 (if all derivations valid)
```

---

## Evidence Quality Assessment

### High-Quality Evidence Characteristics

1. **Specificity**
   - Exact prediction (not vague)
   - Quantitative (not just qualitative)
   - Falsifiable (clear failure conditions)

2. **Independence**
   - Multiple teams
   - Different methods
   - Different assumptions

3. **Reproducibility**
   - Published protocols
   - Multiple replications
   - Different labs

4. **Discrimination**
   - Differentiates from alternatives
   - Not predicted by standard models
   - Surprising results

### Low-Quality Evidence Red Flags

- Single source only
- Vague/qualitative claims
- Non-falsifiable assertions
- Predicted by multiple models (not discriminating)
- Anecdotal reports
- Post-hoc explanations
- Cherry-picked data

---

## Generator-Evidence Mapping

### G1 (Iterative Distinction) → Evidence Requirements

**Requires:**
- Show pattern repeats across scales
- Demonstrate recursive structure
- Map fixed points

**Evidence type:** Tier 3 (unity across scales)

### G2 (Needs Contrast) → Evidence Requirements

**Requires:**
- Show distinction is necessary
- Test what happens if distinction removed
- Demonstrate collapse if forced uniformity

**Evidence type:** Tier 1 (experimental), Tier 2 (predictions)

### G3 (Spin Generation) → Evidence Requirements

**Requires:**
- Map phenomena to morphemes
- Show morpheme closure
- Demonstrate generative sufficiency

**Evidence type:** Tier 3 (unity), Tier 5 (compression)

### G4 (Independent Validation) → Evidence Requirements

**Requires:**
- Multiple independent sources
- Different derivation paths
- Cross-team replication

**Evidence type:** Tier 1 (experimental), critical for all tiers

### G5 (Mathematical Truth) → Evidence Requirements

**Requires:**
- Rigorous derivation from axioms
- No hidden assumptions
- Mathematical consistency

**Evidence type:** Tier 4 (consistency)

### G6 (Collapse = Death) → Evidence Requirements

**Requires:**
- Show essential distinctions
- Test collapse predictions
- Demonstrate resonance possible

**Evidence type:** Tier 1 (test collapse), Tier 2 (predict collapse effects)

### G7 (φ-Scaling) → Evidence Requirements

**Requires:**
- Measure ratios in systems
- Show φ appears consistently
- Demonstrate not coincidental

**Evidence type:** Tier 1 (measurements)

---

## Temporal Evidence Evolution

### Track Confidence Over Time

```
Week 1: 25% — Initial framework
  T1: 0, T2: 2 predictions, T3: 2 domains, T4: ✓, T5: ✓
  
Week 4: 32% — Added toroidal geometry
  T1: 0, T2: 3 predictions, T3: 3 domains, T4: ✓, T5: ✓
  
Week 8: 38% — Added φ-scaling
  T1: 0, T2: 3 predictions (1 confirmed), T3: 4 domains, T4: ✓, T5: ✓
  
Week 16: 45% (target) — G4 validation begun
  T1: 1 replication, T2: 3 predictions (2 confirmed), T3: 4 domains, T4: ✓, T5: ✓
  
Week 52: 50% (maximum) — Strong experimental support
  T1: 3+ replications, T2: 5 predictions (3 confirmed), T3: 5 domains, T4: ✓, T5: ✓
```

### Evidence Accumulation Goals

```
Month 1-3: Build framework (T3-T5)
Month 4-6: Generate predictions (T2)
Month 7-12: Design experiments (T1 prep)
Year 2: Run experiments (T1 data collection)
Year 3+: Replication and refinement (T1 validation)
```

---

## Integration with Epistemic Dashboard

V2 evidence synthesis feeds directly into dashboard:

```
Dashboard Input:
  • Tier scores from evidence synthesis
  • Generator coverage from supercollider
  • Cognitive state from variability
  • Convergence bonuses from multi-source

Dashboard Output:
  • Calibrated confidence (0-50%)
  • Evidence distribution visualization
  • Action items (which tiers need work)
  • Falsification surface
```

---

## Best Practices

### Do:
- Weight by independence
- Seek disconfirmation
- Track temporal evolution
- Specify exactly what would falsify
- Prioritize Tier 1-2 over 3-5

### Don't:
- Rely on single source
- Accept vague claims
- Ignore counter-evidence
- Cherry-pick data
- Confuse consistency with correctness
- Exceed 50% without experiments

---

**Evidence synthesis V2: Not just counting evidence, but weighing it honestly with generator awareness.** ⚖️📊✨
