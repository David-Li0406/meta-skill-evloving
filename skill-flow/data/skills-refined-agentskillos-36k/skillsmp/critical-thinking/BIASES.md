# Cognitive Biases in Technical Decisions

Common cognitive biases that affect software engineering decisions and how to counter them.

---

## High-Impact Biases

### Confirmation Bias

**What It Is:**
Seeking information that confirms existing beliefs while ignoring contradictory evidence.

**In Technical Decisions:**
```
Example: "I know Redis is the right choice"
→ Searches: "Redis benefits", "Redis success stories"
→ Ignores: "Redis limitations", "Redis failures at scale"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Seek disconfirmation | Search for "[technology] problems" not just benefits |
| Devil's advocate | Explicitly argue the opposite position |
| Pre-mortem | Assume it failed—why? |
| Multiple sources | Require evidence from different source types |

**Search Strategy:**
```
Instead of: "Why X is good"
Search: "X problems", "X alternatives", "X vs Y comparison"
```

---

### Anchoring Bias

**What It Is:**
Over-relying on the first piece of information encountered.

**In Technical Decisions:**
```
Example: First estimate is "2 weeks"
→ All subsequent estimates cluster around 2 weeks
→ Actual work might be 6 weeks but adjustments stay close to anchor
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Multiple independent estimates | Get estimates before sharing yours |
| Reference class forecasting | What did similar projects actually take? |
| Break down first | Estimate components, then sum |
| Delay anchors | Share information that might anchor last |

**Questions to Ask:**
- What would a fresh estimate look like?
- What did similar work actually take historically?
- Am I adjusting from an initial number or calculating fresh?

---

### Survivorship Bias

**What It Is:**
Focusing on successes while ignoring failures that didn't survive to be counted.

**In Technical Decisions:**
```
Example: "Netflix uses microservices successfully"
→ Ignores: Thousands of companies that failed with microservices
→ Ignores: Netflix's unique context (resources, team, scale)
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Seek failure stories | Search for "[approach] failures" |
| Consider context | What makes success cases different? |
| Base rates | What percentage actually succeed? |
| Selection bias awareness | Why am I hearing about this example? |

**Questions to Ask:**
- What about the companies we DON'T hear about?
- What's the failure rate for this approach?
- Does our context match the success stories?

---

### Availability Heuristic

**What It Is:**
Overweighting information that comes to mind easily (recent, dramatic, personal).

**In Technical Decisions:**
```
Example: Recent outage caused by X
→ Overestimate probability of X causing future outages
→ Underestimate other risks that haven't happened recently
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Data over memory | Check actual incident statistics |
| Systematic risk assessment | Evaluate all risks, not just memorable ones |
| Cool-down period | Wait before making reactive decisions |
| Written records | Review historical data, not just memory |

**Questions to Ask:**
- Am I weighting this because it's recent or because it's likely?
- What does the actual data show?
- What risks am I NOT thinking about?

---

### Sunk Cost Fallacy

**What It Is:**
Continuing investment due to past investment rather than future value.

**In Technical Decisions:**
```
Example: "We've spent 6 months on this approach"
→ Continue despite evidence it's wrong
→ "We can't stop now after all this work"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Future-only evaluation | Ignore past investment in decisions |
| Kill criteria | Define upfront when to stop |
| Fresh perspective | "If starting today, would we choose this?" |
| Incremental gates | Regular go/no-go decisions |

**Questions to Ask:**
- If we started fresh today, would we choose this?
- What's the best use of resources FROM HERE?
- Are we continuing because it's right or because we started?

---

### Dunning-Kruger Effect

**What It Is:**
Overestimating competence in unfamiliar areas; underestimating in familiar ones.

**In Technical Decisions:**
```
Low experience: "Kubernetes is easy, we can learn as we go"
High experience: "This is more complex than it looks"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Unknown unknowns check | "What don't we know we don't know?" |
| Expert consultation | Get input from experienced practitioners |
| Proof of concept | Validate assumptions with actual work |
| Calibrated confidence | Track prediction accuracy over time |

**Questions to Ask:**
- How much actual experience do we have with this?
- Who has done this successfully and what did they learn?
- What surprised people who've done this before?

---

### Optimism Bias

**What It Is:**
Underestimating negative outcomes and overestimating positive ones.

**In Technical Decisions:**
```
"This migration should go smoothly"
"We won't hit those edge cases"
"The happy path covers 99% of cases"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Pre-mortem | Assume failure, work backwards |
| Historical reference | What actually happened in similar projects? |
| Buffer time | Add contingency for unknowns |
| Pessimistic planning | Plan for problems, not just success |

**Questions to Ask:**
- What could go wrong?
- What went wrong in similar projects?
- What's our plan when (not if) we hit problems?

---

## Medium-Impact Biases

### Bandwagon Effect

**What It Is:**
Adopting something because others are doing it.

**In Technical Decisions:**
```
"Everyone is using Kubernetes"
"React is the industry standard"
"All the big companies use microservices"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Context match | Does our context match theirs? |
| Problem-first | Start with problem, not solution |
| Independent evaluation | What's right for US? |
| Verify claims | Is "everyone" actually everyone? |

**Questions to Ask:**
- Is this right for our specific situation?
- Why are others choosing this? (Do those reasons apply to us?)
- What would we choose if this weren't popular?

---

### Authority Bias

**What It Is:**
Accepting claims because of the source's status rather than evidence.

**In Technical Decisions:**
```
"Google recommends this approach"
"The documentation says to do it this way"
"A famous engineer wrote this library"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Evidence over authority | What's the actual evidence? |
| Context relevance | Does their context match ours? |
| Multiple authorities | Do experts agree? |
| Challenge respectfully | Even experts can be wrong |

**Questions to Ask:**
- What's the evidence, independent of who said it?
- Does this authority's context match ours?
- Are there dissenting expert opinions?

---

### Recency Bias

**What It Is:**
Overweighting recent events over historical patterns.

**In Technical Decisions:**
```
Recent success with X → "X is the answer for everything"
Recent failure with Y → "Never use Y again"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Historical view | Look at longer time periods |
| Pattern recognition | Is this a trend or an anomaly? |
| Statistical thinking | What's the base rate? |
| Regression to mean | Expect outliers to normalize |

**Questions to Ask:**
- Is this recent event representative or exceptional?
- What's the longer-term pattern?
- Am I overreacting to recent events?

---

### Status Quo Bias

**What It Is:**
Preferring current state over change, regardless of merit.

**In Technical Decisions:**
```
"We've always done it this way"
"Changing would be too risky"
"If it ain't broke, don't fix it" (even when it IS broke)
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Cost of inaction | What's the cost of NOT changing? |
| Fresh evaluation | Evaluate as if choosing new |
| Opportunity cost | What are we missing by staying? |
| Incremental change | Reduce change risk with small steps |

**Questions to Ask:**
- If starting fresh, would we choose current approach?
- What's the cost of staying the same?
- What opportunities are we missing?

---

### IKEA Effect

**What It Is:**
Overvaluing things we built ourselves.

**In Technical Decisions:**
```
"Our custom solution is better than open source"
"This internal tool is perfect for our needs"
(Despite evidence that alternatives are better)
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Objective comparison | Compare with standard metrics |
| External review | Get outside perspective |
| Total cost | Include maintenance and opportunity cost |
| Buy vs build analysis | Rigorous, not emotional |

**Questions to Ask:**
- Would we choose this if we hadn't built it?
- What would an outside evaluator say?
- What's the true total cost of ownership?

---

### Planning Fallacy

**What It Is:**
Underestimating time, costs, and risks while overestimating benefits.

**In Technical Decisions:**
```
"This should take about 2 weeks" → Actually takes 2 months
"Implementation will be straightforward" → Hits unexpected complexity
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| Reference class | What did similar projects take? |
| Outside view | Ask someone not invested |
| Task decomposition | Break down and sum estimates |
| Buffers | Add explicit contingency |

**Estimation Multipliers:**
| Confidence Level | Multiplier |
|------------------|------------|
| "I've done this exact thing" | 1.2x |
| "I've done similar things" | 1.5x |
| "I understand this well" | 2x |
| "Seems straightforward" | 3x |
| "How hard can it be?" | 5x |

---

### Not Invented Here (NIH) Syndrome

**What It Is:**
Rejecting external solutions in favor of building custom ones.

**In Technical Decisions:**
```
"This library doesn't quite fit our needs"
"We can build something better suited to us"
"External dependencies are risky"
```

**How to Counter:**
| Action | Implementation |
|--------|----------------|
| True cost comparison | Include maintenance, bugs, opportunity cost |
| 80/20 rule | Is 80% fit good enough? |
| Customization cost | What does the last 20% really cost? |
| Core competency | Is this our competitive advantage? |

**Questions to Ask:**
- Is building this our core business?
- What's the true long-term cost of maintaining custom code?
- Would we accept 80% fit to save 80% effort?

---

## Bias Detection Questions

Ask these when evaluating any technical decision:

### Source Evaluation
- Why do I believe this?
- What would change my mind?
- What evidence have I NOT looked for?

### Perspective Check
- Would I accept this argument from someone else?
- What would a skeptic say?
- What am I assuming that might not be true?

### Decision Quality
- Am I deciding based on evidence or emotion?
- Am I anchored to an early estimate or opinion?
- Am I continuing because it's right or because we started?

### Context Relevance
- Does this apply to our specific situation?
- What's different about our context?
- What worked elsewhere might not work here—why?

---

## Bias Checklist

Before finalizing a technical decision:

### Information Quality
- [ ] Sought disconfirming evidence
- [ ] Consulted multiple source types
- [ ] Checked for recent vs. comprehensive data
- [ ] Verified claims independently

### Decision Process
- [ ] Considered multiple alternatives
- [ ] Evaluated without anchoring to first option
- [ ] Ignored sunk costs
- [ ] Assessed our actual (not assumed) expertise

### Context Fit
- [ ] Verified success stories match our context
- [ ] Accounted for survivorship bias
- [ ] Distinguished popularity from suitability
- [ ] Considered what failures we're not seeing

### Risk Assessment
- [ ] Identified what could go wrong
- [ ] Used realistic (not optimistic) estimates
- [ ] Planned for problems, not just success
- [ ] Defined kill criteria upfront

---

## Quick Reference: Bias → Counter

| Bias | Quick Counter |
|------|---------------|
| Confirmation | Search for "[X] problems" |
| Anchoring | Get multiple independent estimates |
| Survivorship | Search for "[approach] failures" |
| Availability | Check actual data, not memory |
| Sunk Cost | "If starting today, would we choose this?" |
| Dunning-Kruger | "What don't we know we don't know?" |
| Optimism | Pre-mortem: assume failure, work backwards |
| Bandwagon | "Is this right for OUR situation?" |
| Authority | "What's the evidence, independent of source?" |
| Recency | Look at longer time periods |
| Status Quo | "Cost of NOT changing?" |
| IKEA Effect | Get outside evaluation |
| Planning Fallacy | Reference similar past projects |
| NIH Syndrome | True total cost comparison |

---

## When Biases Are Most Dangerous

| Situation | Elevated Risk Of |
|-----------|------------------|
| Time pressure | Anchoring, Availability, Recency |
| New technology | Dunning-Kruger, Optimism, Bandwagon |
| Team investment | Sunk Cost, IKEA Effect, Confirmation |
| Expert recommendation | Authority, Confirmation |
| Recent incident | Availability, Recency |
| Popular choice | Bandwagon, Survivorship |
| Custom vs. buy | NIH, IKEA Effect |
| Estimation | Planning Fallacy, Optimism, Anchoring |

> **Rule:** The more confident we feel, the more we should question our thinking.
