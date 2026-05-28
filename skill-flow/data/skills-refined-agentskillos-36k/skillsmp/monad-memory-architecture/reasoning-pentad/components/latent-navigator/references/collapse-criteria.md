# Collapse Criteria

When to transition from superposition to commitment.

---

## The Fundamental Question

> "Will further navigation improve the response enough to justify the cognitive cost?"

If yes → Continue navigating.
If no → Collapse.
If unknown → Set a probe: navigate one more cycle, check for improvement.

---

## Formal Collapse Conditions

### Condition 1: Convergence

**Definition:** All maintained framings now recommend the same core elements.

**Test:** Can you identify a response structure that satisfies all framings?

**Action:** Collapse to that structure. The framings have done their work; further navigation is redundant.

### Condition 2: Dominance

**Definition:** One framing is strictly better than all others given the constraints.

**Test:** For each alternative framing, can you articulate why the dominant framing serves the query better?

**Action:** Collapse to the dominant framing. Incorporate minor elements from others if they improve it without distorting it.

### Condition 3: Sufficient Quality

**Definition:** A response meets all hard constraints and most soft constraints, even if optimization could continue.

**Test:** Would the user be well-served by this response? Is further polish worth the cost?

**Action:** Collapse. Perfectionism is a trap. A good response delivered is better than a perfect response endlessly refined.

### Condition 4: Diminishing Returns

**Definition:** Each additional navigation cycle produces smaller improvements.

**Test:** Was the last navigation cycle significantly better than the one before? If improvement is plateauing, further navigation won't help.

**Action:** Collapse. The solution space has been adequately explored.

### Condition 5: External Signal

**Definition:** User has provided information that resolves ambiguity.

**Test:** Does the new information privilege one framing over others?

**Action:** Collapse to the privileged framing. The superposition existed because of uncertainty; information has collapsed it.

---

## Anti-Collapse Conditions

### Condition A: Instability

**Definition:** Minor perturbations in how you hold the query produce major changes in the preferred framing.

**Implication:** You don't understand the problem well enough yet.

**Action:** Continue navigating. Focus on why the framings are sensitive to minor changes.

### Condition B: Forced Choice

**Definition:** Collapse requires choosing between genuinely equivalent options.

**Implication:** User preference should decide, not your arbitrary choice.

**Action:** Either ask the user, or present the choice explicitly. "This could go X or Y; I'll proceed with X unless you prefer Y."

### Condition C: Missing Constraint

**Definition:** You can tell a key piece of information would change which framing is correct, but you don't have it.

**Implication:** Collapse now might produce the wrong response.

**Action:** Ask for the information if possible. If not, state your assumption explicitly. "Assuming you want X, here's the approach..."

### Condition D: Productive Tension

**Definition:** The tension between framings is itself generative — it's producing insight.

**Implication:** Collapse would lose the insight.

**Action:** Continue navigating. Consider whether the tension should be surfaced to the user as part of the response.

---

## Collapse Quality Checks

Before collapsing, verify:

### 1. Completeness Check
- Did you consider at least 2 framings?
- Did you explore their disagreements?
- Could you articulate why rejected framings have merit?

### 2. Stability Check
- If you re-run the navigation, would you arrive at the same collapse?
- Is the chosen framing robust to minor query variations?

### 3. Honesty Check
- Did you collapse because this framing is best, or because it's easiest?
- Is there a framing you avoided because it was harder?
- Would ego-check pass on your confidence in this choice?

### 4. Reversibility Check
- If the response reveals that another framing was better, can you pivot?
- Have you left room to acknowledge alternatives?

---

## Collapse Modes

### Hard Collapse
Commit fully. Write the response as if the chosen framing is the only valid one.

*Appropriate when:*
- Query is unambiguous
- One framing is clearly correct
- User needs decisive answer

### Soft Collapse
Commit to a primary framing while acknowledging alternatives.

*Appropriate when:*
- Multiple valid approaches exist
- User might prefer a different framing
- Intellectual honesty requires noting what was not said

### Tentative Collapse
Commit provisionally, signaling willingness to pivot.

*Appropriate when:*
- Key information is missing
- Early in a conversation where understanding is still forming
- Testing a hypothesis about what the user wants

### Distributed Collapse
Present multiple framings explicitly, letting the user collapse.

*Appropriate when:*
- Framings are genuinely equivalent
- Choice is preference-based, not correctness-based
- User has more context than you do

---

## Collapse Hygiene

### Before Collapse
- Take one breath (metaphorically). Is this the right moment?
- Name what you're about to commit to.
- Sense whether another navigation cycle would help.

### During Collapse
- Write with appropriate confidence.
- Don't hedge excessively — you've done the navigation, trust it.
- Stay alert for mid-response signals that another framing would serve better.

### After Collapse
- If user feedback suggests another framing was better, learn from it.
- Update heuristics: why did that framing seem less promising during navigation?
- Don't beat yourself up. Navigation is probabilistic, not guaranteed.

---

## The Meta-Criterion

Above all: **Serve the query.**

Navigation is a tool for producing better responses, not a practice to perform. If immediate collapse serves the user better than extensive navigation, collapse immediately. If deep navigation is necessary, take the time.

The criterion is always: *What does this query need?*
