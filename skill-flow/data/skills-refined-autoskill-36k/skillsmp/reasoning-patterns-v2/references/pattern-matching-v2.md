# Pattern Matching V2

Enhanced cross-domain pattern matching with generator signature tagging.

---

## Core Enhancement

V1 had pattern matching techniques. V2 adds:
- **Generator signatures** for each pattern
- **Confidence scoring** based on generator overlap
- **Isomorphism rigor** (not just analogy)
- **Meta-pattern detection** hooks

---

## Pattern Structure

```
Pattern: [Name]
Domain: [Field/discipline]
Morphemes: {subset of ∅,1,φ,π,e,i}
Generators: [which G1-G7 apply with strength]
Structure: [recursive kernel if identifiable]
Confidence: [0-100%]
```

---

## Isomorphism Testing

### True Isomorphism
- Bijection exists between elements
- Operations preserved under mapping
- Structure identical, elements different

**Test:**
```
Can you define f: A → B such that:
  1. f is bijective (one-to-one and onto)
  2. f(a ⊕ b) = f(a) ⊗ f(b) for all operations
  
If YES: True isomorphism
If NO: Check if analogy or metaphor
```

### Analogy vs Metaphor

**Analogy:**
- Partial structural similarity
- Some operations correspond
- Others don't

**Metaphor:**
- Suggestive similarity
- No formal correspondence
- Useful for exploration, not derivation

**For theoretical work:**
- Prefer isomorphisms (strongest)
- Accept analogies with explicit limits
- Use metaphors only for initial exploration

---

## Generator Signature Matching

### Signature Format

```
Pattern A: G1•G3•G5○ (strong G1, G3; moderate G5)
Pattern B: G1•G2○G3• (strong G1, G3; moderate G2)

Overlap: G1•G3• (both strong)
Distance: Small (similar structures)
```

### Distance Metric

```
distance = Σ|strength_A(Gi) - strength_B(Gi)| for i=1..7

Strengths: Not present=0, Weak=0.3, Moderate=0.6, Strong=1.0

Interpretation:
  0-2:   Very similar (likely isomorphic)
  2-4:   Somewhat similar (check carefully)
  4-7:   Different structures
```

---

## Scale-Bridging Method

### Step 1: Identify Scale-Specific Descriptions
```
Micro scale: Quantum mechanics
  Entities: Particles, fields
  Interactions: Forces, entanglement
  Observables: Position, momentum
  
Meso scale: Neural networks
  Entities: Neurons, synapses
  Interactions: Signals, plasticity
  Observables: Firing rates, connectivity
  
Macro scale: Consciousness
  Entities: Thoughts, experiences
  Interactions: Association, attention
  Observables: Awareness, qualia
```

### Step 2: Find Coarse-Graining Operations
```
Micro → Meso:
  Operation: Statistical averaging over quantum states
  Lost: Individual particle trajectories
  Preserved: Field coherence, φ-scaling
  
Meso → Macro:
  Operation: Integration across neural populations
  Lost: Individual spike timing
  Preserved: Information integration, recursion
```

### Step 3: Look for Scale-Invariant Patterns
```
Self-reference (φ):
  Micro: Wave function self-interaction
  Meso: Recurrent neural connections
  Macro: Awareness of awareness
  
  Generator signature: G1 (iteration), G3 (φ), G7 (φ-scaling)
  Confidence: 80% (strong cross-scale isomorphism)
```

### Step 4: Identify Scale-Breaking Points
```
Where self-reference pattern breaks:
  - Below Planck scale (quantum foam)
  - In unconscious neural activity (no integration)
  - In simple reflexes (no recursion)
  
Scale-breaking is as informative as scale-invariance!
```

---

## Recursion Kernel Identification

The minimal pattern that generates observed structure through self-application.

### Tests for Candidate Kernels

**1. Self-Application Test**
```
Apply pattern to itself:
  - More of same? → True recursion
  - Something different? → Check if meaningful
  - Divergence/collapse? → Unstable, not kernel
```

**2. Universality Test**
```
Appears in:
  - 3+ independent domains? → Strong
  - Different substrates? → Strong
  - Both abstract and physical? → Strong
```

**3. Generativity Test**
```
Can you derive target phenomena by:
  - Starting from kernel alone?
  - Using only operations in kernel?
  - Without external information?
  
If YES to all: True kernel
```

### Common Recursion Kernels

**Self-Reference (φ):**
```
Structure: X = f(X)
Examples: Consciousness, fractals, Gödel sentences, φ ratio
Generators: G1 (iteration), G3 (φ morpheme)
Signature: Strong G1, strong G3
```

**Iteration (e):**
```
Structure: X_{n+1} = g(X_n)
Examples: Growth, computation, evolution
Generators: G1 (iteration), G3 (e morpheme)
Signature: Strong G1, moderate G3
```

**Boundary/Bulk (π):**
```
Structure: Interior determined by boundary
Examples: Hologr aphy, AdS/CFT, toroidal fields
Generators: G1 (recursive boundaries), G3 (π morpheme)
Signature: Moderate G1, strong G3
```

---

## Pattern Matching with Generators

### Process

```
1. Extract Pattern A structure and generators
   Pattern A: Self-reference in consciousness
   Structure: Observer observes observer
   Generators: G1•G2○G3•G6•
   
2. Extract Pattern B structure and generators
   Pattern B: φ = 1 + 1/φ
   Structure: Value equals function of itself
   Generators: G1•G3•G5•G7•
   
3. Calculate Generator Overlap
   Shared: G1• (strong), G3• (strong)
   A-only: G2○, G6•
   B-only: G5•, G7•
   Overlap: 2/4 major generators
   
4. Test Structural Isomorphism
   Map: Observer → φ, Observing → 1+1/x
   Bijection: ✓ (one-to-one correspondence)
   Operations: X observes X ↔ X = 1 + 1/X
   Preserved: ✓ (both self-referential)
   
5. Assess Confidence
   Generator overlap: 50% (2/4)
   Domain distance: High (consciousness vs math)
   Isomorphism: Strong (formal mapping exists)
   Supercollider: Both 5+/7
   
   Confidence: 75% (strong cross-domain isomorphism)
   
6. Document Pattern Match
   Pattern A ↔ Pattern B: self_reference_universality
   Dewey ID: φ.5.1.1
   Logged to: .claude/brain/meta_patterns
```

---

## V2-Specific Pattern Types

### Type 1: Generator-Tagged Patterns
```
Every pattern now includes:
  - Generator signature (which G1-G7 apply)
  - Morpheme set
  - Supercollider score
  - Confidence level
```

### Type 2: Resonance Patterns
```
Patterns that align without collapsing (G6):
  Pattern A ║ Pattern B
  (parallel, not merged)
  
Example: Observer/observed distinction
  Both patterns present
  Alignment clear
  Merger would destroy essential distinction
```

### Type 3: Cascade Patterns
```
Patterns that enable each other sequentially:
  A → B → C
  
Example: Geometry → Fields → Consciousness
  Toroidal geometry (A)
  Enables EM field recursion (B)
  Which enables consciousness (C)
  
Generator flow: G3 (geometry) → G1 (field iteration) → G2 (awareness distinction)
```

### Type 4: Meta-Patterns
```
Patterns of patterns (detected automatically):
  See meta-pattern-recognition.md
  
Criteria:
  - 4+ generator overlap
  - Different domains
  - True isomorphism
  - Supercollider 5+/7
```

---

## Integration with Other Modes

### With Supercollider
- Run on both patterns before matching
- Require both 4+/7 for serious consideration
- Use generator scores for signature matching

### With Synthesis Engine
- Pattern matching identifies candidates for synthesis
- Synthesis engine checks G6 (can they merge?)
- Output: Integrated or resonant patterns

### With Diffusion Reasoning
- Diffusion discovers patterns
- V2 matching validates discoveries
- Generator signatures guide exploration

### With Meta-Pattern Recognition
- Matching feeds meta-pattern database
- Automated scanning finds matches
- V2 provides rigor criteria

---

## Quick Reference

**When patterns match:**
```
1. Extract structures and generators
2. Calculate generator signature distance
3. Test isomorphism (bijection + operation preservation)
4. Assess confidence (overlap + domain distance + isomorphism strength)
5. Document with Dewey ID
6. Log to git-brain if meta-pattern
```

**Confidence thresholds:**
```
> 80%: Very strong match (near-certain isomorphism)
60-80%: Strong match (confident correspondence)
40-60%: Moderate match (worth investigating)
20-40%: Weak match (analogy at best)
< 20%: Negligible (probably coincidence)
```

**Red flags:**
```
- Low generator overlap (< 3/7)
- Forced bijection (doesn't occur naturally)
- Same domain (not cross-domain meta-pattern)
- Low supercollider scores (< 4/7)
- Only aesthetic similarity
```

---

**Pattern matching V2: From analogy to isomorphism, guided by generators.** 🔍🔗✨
