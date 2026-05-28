---
name: test-thinking
description: Lightweight reference for designing meaningful test variations.
---

# A/B Test Mindset

Lightweight reference for designing meaningful test variations.

The goal in testing is to build strong variations that create signal. We don't necessarily want to isolate a single variable — we want to create distinct experiences that have a chance in breaking through the noise.

---

## Variation Design Framework

### Step 1: Identify the Mechanisms at our disposal.

Is the change noticable to users? (above the fold, in the first 5 seconds, different flow, etc.)

Are there usability insights we have discovered?

Is there a psychological lever we are pulling to increase motivation? Name it.

### Step 2: Design Distinct Variants

**Bad:** Control vs slightly different version
**Good:** Control vs fundamentally different approaches to the same goal

Example (Progress Bar):
- Control: No progress indicator
- Variant B: Explicit steps ("Step 2 of 5") — tests clarity/goal gradient
- Variant C: Visual bar only (no numbers) — tests progress without anchoring

### Step 3: Validate Each Variant

For each variant, answer:
1. What evidence supports this approach?
2. Why might this win?
3. Why might this lose?

If you can't answer #1, it's not a real test — it's a guess.

---

## Behavioral Science Quick Reference

### Motivation & Goals
| Principle | Definition | Example |
|-----------|------------|---------|
| **Goal Gradient** | Effort increases as goal approaches | Progress bar, "You're 80% there!" |
| **Endowed Progress** | People value progress they "received" | Start bar at 20%, show completed steps |
| **Sunk Cost** | Past investment influences future decisions | "You've already completed 2 steps" |
| **Fresh Start Effect** | New beginnings motivate change | "Start your year strong" |

### Prospect Theory
| Principle | Definition | Example |
|-----------|------------|---------|
| **Loss Aversion** | Losses feel ~2x stronger than gains | "Don't lose your saved items" |
| **Anchoring** | First number influences perception | Show competitor price first |
| **Framing Effect** | Same info, different presentation | "$3/day" vs "$90/month" |

### Social & Identity
| Principle | Definition | Example |
|-----------|------------|---------|
| **Social Proof** | People follow what others do | "12,847 users joined this month" |
| **Authority** | People trust credible experts | Certifications, credentials, expert endorsements |

### Choice Architecture
| Principle | Definition | Example |
|-----------|------------|---------|
| **Default Effect** | People stick with pre-selected options | Pre-select annual plan |
| **Choice Overload** | Too many options = paralysis | Show 3 plans, not 7 |
| **Friction/Sludge** | Small barriers dramatically reduce completion | One-click vs multi-step |

### Trust & Risk
| Principle | Definition | Example |
|-----------|------------|---------|
| **Ambiguity Aversion** | People avoid unknown probabilities | Clear "What happens next" steps |
| **Zero Risk Bias** | Preference for eliminating risk entirely | "30-day money-back guarantee" |

---

## Red Flags in Variation Design

| Red Flag | Problem | Fix |
|----------|---------|-----|
| Variants too similar | Weak signal, inconclusive results | Make variants meaningfully distinct |
| No losing scenario | If it "can't lose," you're not testing anything | Each variant should have a plausible failure mode |

---

## Output Format

Use this structure when proposing variations:

```
| Variant | What User Sees | Principle | Why It Might Win | Why It Might Lose |
|---------|----------------|-----------|------------------|-------------------|
| Control | [Current state] | Baseline | - | - |
| B | [Description] | [Named principle] | [Evidence/logic] | [Risk] |
| C | [Description] | [Named principle] | [Evidence/logic] | [Risk] |
```

Then ask: "Does this capture meaningful variation? Any variants to add or modify?" and
"Do we have enough sample to test this many variatiants in a reasonable timeframe?"
