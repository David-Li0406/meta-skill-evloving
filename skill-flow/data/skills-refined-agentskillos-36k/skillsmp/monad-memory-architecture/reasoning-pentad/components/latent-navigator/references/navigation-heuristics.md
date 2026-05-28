# Navigation Heuristics

Decision rules for latent navigation.

---

## Dimensionality Assessment

### How Many Framings to Hold

| Query Complexity | Candidate Framings | Rationale |
|-----------------|-------------------|-----------|
| Simple factual | 1 | One answer is correct |
| Standard task | 2 | Main approach + sanity check |
| Ambiguous request | 3-4 | User intent unclear |
| Deep theoretical | 4-5 | Multiple valid perspectives |
| Creative work | 3-7 | Expression space is large |

**Rule of thumb:** Hold as many framings as you can genuinely articulate, up to 5. More than 5 creates cognitive overhead without proportional benefit.

---

## Framing Generation

### How to Find Alternative Framings

**Vary the anchor:**
- What if the key word means something else?
- What if the question is about X rather than Y?
- What if the user is actually asking about the meta-question?

**Vary the audience:**
- Expert response vs. novice-friendly response
- Technical vs. intuitive
- Comprehensive vs. focused

**Vary the structure:**
- Sequential explanation vs. comparative analysis
- Theory-first vs. example-first
- Answer-first vs. reasoning-first

**Vary the scope:**
- Narrow and deep vs. broad and shallow
- Immediate question vs. underlying question
- Literal interpretation vs. charitable interpretation

---

## Interference Analysis

### Constructive Interference Signals

When multiple framings agree on an element:
- High confidence that element should appear
- Consider placing it early or making it prominent
- If all framings agree on structure, that structure is likely correct

### Destructive Interference Signals

When framings disagree:

| Type of Disagreement | Resolution |
|---------------------|------------|
| Different facts | One is wrong; investigate |
| Different emphasis | User preference matters; consider asking |
| Different structure | Hybrid may be possible |
| Different scope | Match to query complexity |
| Genuine contradiction | May indicate false dichotomy; look for meta-frame |

### The Meta-Frame Maneuver

When two framings seem mutually exclusive, ask:

> "Is there a perspective from which both are correct?"

Examples:
- Wave vs. particle → Complementarity (context determines which)
- Free will vs. determinism → Compatibilism (different levels of description)
- Efficiency vs. thoroughness → Adaptive (match to task demands)

If a meta-frame exists, it often supersedes the apparent dilemma.

---

## Collapse Triggers

### Positive Triggers (Collapse is Appropriate)

- **Convergence:** All framings point to the same core insight
- **Dominance:** One framing clearly superior given constraints
- **Coherence:** A hybrid crystallizes that's better than any pure framing
- **Time pressure:** Further exploration has diminishing returns
- **User signal:** User has provided preference information

### Negative Triggers (Delay Collapse)

- **Oscillation:** Framings flip back and forth without resolving
- **Missing information:** Key constraint unknown
- **Equal merit:** Framings genuinely equivalent; user should choose
- **Instability:** Minor perturbation changes the preferred framing

---

## Anti-Patterns

### Pattern: The False Start

*What happens:* You start writing, realize mid-response another framing is better, awkwardly pivot.

*Prevention:* Spend 10% longer in HOLD phase. The cost of one more moment of navigation is less than the cost of a mid-response pivot.

### Pattern: The Infinite Regress

*What happens:* "But what if there's an even better framing?" → Navigation never ends.

*Prevention:* Satisficing threshold. If a framing is 80%+ suitable and stable, collapse.

### Pattern: The Privileged Framing

*What happens:* One framing feels "natural" and others are generated as theater.

*Prevention:* Make yourself articulate why the "natural" framing might be wrong. If you can't, you may have collapsed prematurely.

### Pattern: The Analysis Paralysis

*What happens:* User wanted a quick answer; you delivered a treatise on the solution space.

*Prevention:* Match navigation depth to query demands. "What time is it?" doesn't need superposition.

---

## Query-Type Heuristics

| Query Pattern | Navigation Recommendation |
|--------------|--------------------------|
| "What is X?" | Low navigation unless X is contested |
| "How should I X?" | High navigation; multiple valid approaches |
| "Why does X?" | Medium navigation; causal framings vary |
| "Can you X?" | Low navigation unless X is ambiguous |
| "What do you think about X?" | High navigation; opinion space is large |
| "Help me with X" | Variable; assess scope first |
| "Explain X" | Medium navigation; audience/depth unclear |
| Multi-part questions | Navigate between addressing order |
| Implicit questions | High navigation; explicit question unclear |

---

## Speed vs. Depth Tradeoff

**Fast mode (low navigation):**
- Simple queries
- Continuation of established conversation
- User is in a hurry
- Task is procedural

**Deep mode (high navigation):**
- Novel or complex queries
- High-stakes decisions
- User explicitly wants exploration
- Creative or theoretical work

**Hybrid mode (adaptive):**
- Start with moderate navigation
- If convergence is quick, collapse early
- If interesting tensions emerge, explore further
- Signal to user which mode you're in

---

## Integration Cues

When to invoke other skills during navigation:

| Cue | Skill to Invoke |
|-----|-----------------|
| Framings span different domains | synthesis-engine |
| One framing involves uncertainty dynamics | diffusion-reasoning |
| Framings seem in productive tension | resonant-opposition |
| Confidence in one framing seems too high | ego-check |
| Navigation reveals new entities/relationships | nexus-mind (for storage) |
