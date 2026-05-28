---
id: ab-testing-framework
name: "A/B Testing Framework"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# A/B Testing Framework

## Metadata

| Field | Value |
|-------|-------|
| **ID** | ab-testing-framework |
| **Name** | A/B Testing Framework |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | multivariate-testing, statistical-significance, funnel-optimization |

---

## Problem

You want to improve your product but do not know what changes will work. You make decisions based on opinions ("I think users will like this") instead of data. Some changes hurt metrics, but you do not know until it is too late.

A/B testing lets you compare two versions of something and measure which performs better. It removes guesswork from decision-making.

---

## Framework

### What is A/B Testing?

A/B testing (also called split testing) is an experiment where you:
1. Show version A to half of users (control)
2. Show version B to half of users (treatment)
3. Measure which version performs better
4. Roll out the winner to everyone

```
         ALL USERS
             │
      ┌──────┴──────┐
      │             │
   50% A         50% B
  (control)   (treatment)
      │             │
  Measure       Measure
  metric        metric
      │             │
      └──────┬──────┘
             │
     Compare results
             │
    Statistical test
             │
    Winner → 100%
```

### A/B Test Lifecycle

```
1. HYPOTHESIS
   What do you believe? Why?
        ↓
2. DESIGN
   What will you change? What will you measure?
        ↓
3. SIZE CALCULATION
   How many users? How long?
        ↓
4. RUN EXPERIMENT
   Split traffic, collect data
        ↓
5. ANALYZE
   Is the difference statistically significant?
        ↓
6. DECIDE
   Ship winner, iterate, or kill
```

### Step 1: Hypothesis

A good hypothesis has three parts:

```
IF we [change X]
THEN [metric Y] will improve
BECAUSE [reason/evidence]
```

**Examples:**

| Bad Hypothesis | Good Hypothesis |
|----------------|-----------------|
| "The new design is better" | "If we simplify the signup form from 6 fields to 3, conversion will increase by 10% because friction decreases" |
| "Users will click more" | "If we change the CTA button from gray to green, CTR will increase by 5% because green stands out more" |

### Step 2: Design

**What to test (one change at a time):**
- Headlines and copy
- Button text, color, position
- Images and visuals
- Layout and flow
- Pricing and offers
- Email subject lines
- Feature presentation

**What to measure (primary metric):**
Choose ONE primary metric that directly measures success.

| Test Area | Primary Metric |
|-----------|---------------|
| Landing page | Signup conversion rate |
| Checkout flow | Purchase completion rate |
| Email | Open rate or click rate |
| Onboarding | Activation rate |
| Pricing page | Plan selection rate |

### Step 3: Sample Size Calculation

You need enough users to detect a real difference. Too few users = unreliable results.

**Variables:**
- **Baseline conversion rate:** Current performance
- **Minimum detectable effect (MDE):** Smallest improvement worth detecting
- **Statistical significance level (alpha):** Usually 95% (alpha = 0.05)
- **Statistical power:** Usually 80%

**Formula (simplified):**

```
Sample size per variant ≈ 16 × (baseline rate × (1 - baseline rate)) / MDE²
```

**Example:**
- Baseline conversion: 10% (0.10)
- Want to detect 10% relative improvement (MDE = 0.01 absolute)
- Sample needed: 16 × (0.10 × 0.90) / (0.01)² = 14,400 per variant
- Total: 28,800 users

**Quick Reference Table:**

| Baseline | 5% MDE | 10% MDE | 20% MDE |
|----------|--------|---------|---------|
| 1% | 62,000 | 16,000 | 4,000 |
| 5% | 30,000 | 8,000 | 2,000 |
| 10% | 28,000 | 7,000 | 1,800 |
| 25% | 20,000 | 5,000 | 1,300 |
| 50% | 16,000 | 4,000 | 1,000 |

### Step 4: Run the Experiment

**Rules:**
1. **Random assignment:** Users randomly see A or B
2. **No peeking:** Do not check results early and make decisions
3. **Run to completion:** Wait until sample size is reached
4. **One test at a time:** Do not run overlapping tests on same area
5. **Control for time:** Run both variants simultaneously

**Duration calculation:**

```
Test duration = Sample size needed / Daily traffic

Example:
- Need 30,000 users total
- Have 2,000 daily visitors
- Duration: 30,000 / 2,000 = 15 days
```

### Step 5: Analyze Results

**Statistical significance test:**

Calculate if the difference is real or just random chance.

```
Conversion A (control):    10.0% (1,500 / 15,000)
Conversion B (treatment):  11.2% (1,680 / 15,000)
Difference:                +1.2 percentage points (+12% relative)

p-value: 0.012 (< 0.05)
Confidence: 98.8%

RESULT: Statistically significant. B wins.
```

**Interpretation:**

| p-value | Confidence | Decision |
|---------|------------|----------|
| < 0.01 | > 99% | Strong evidence, ship B |
| 0.01 - 0.05 | 95-99% | Good evidence, ship B |
| 0.05 - 0.10 | 90-95% | Weak evidence, consider retest |
| > 0.10 | < 90% | Not significant, do not ship |

### Step 6: Decide

**Outcomes:**

| Situation | Action |
|-----------|--------|
| B wins significantly | Ship B to 100% |
| A wins significantly | Keep A, learn from failure |
| No significant difference | Keep A (simpler), test something else |
| B wins but hurts other metrics | Investigate tradeoffs |

---

## Templates

### A/B Test Planning Template

```markdown
# A/B Test: [Name]

## Hypothesis
IF we [specific change]
THEN [metric] will improve by [X%]
BECAUSE [reasoning]

## Variants
| Variant | Description |
|---------|-------------|
| A (Control) | [Current state] |
| B (Treatment) | [Changed state] |

## Metrics
- **Primary:** [Main metric]
- **Secondary:** [Additional metrics to monitor]
- **Guardrail:** [Metric that should not go down]

## Sample Size
- Baseline rate: ____%
- Minimum detectable effect: ____%
- Required sample: _____ per variant
- Estimated duration: _____ days

## Traffic Split
[ ] 50/50
[ ] Other: ____

## Start/End Dates
- Start: ____
- End: ____

## Owner
[Name]
```

### A/B Test Results Template

```markdown
# A/B Test Results: [Name]

## Summary
| Metric | Control (A) | Treatment (B) | Difference | p-value |
|--------|-------------|---------------|------------|---------|
| [Primary] | X% | Y% | +Z% | 0.0X |
| [Secondary] | | | | |

## Sample Sizes
- Control: _____ users
- Treatment: _____ users
- Duration: _____ days

## Statistical Significance
- Confidence level: ____%
- Winner: A / B / No winner

## Decision
[ ] Ship B to 100%
[ ] Keep A
[ ] Retest with larger sample
[ ] Iterate and test again

## Learnings
[What did we learn? How does this inform future tests?]

## Next Steps
[Follow-up tests or actions]
```

---

## Examples

### Example 1: Signup Page Button

**Hypothesis:** If we change the CTA button from "Sign Up" to "Start Free Trial", conversions will increase by 8% because it emphasizes the free offer.

**Setup:**
- Baseline: 4.5% conversion
- MDE: 8% relative (0.36% absolute)
- Sample needed: ~50,000 per variant
- Duration: 3 weeks

**Results:**

| Variant | Visitors | Signups | Rate |
|---------|----------|---------|------|
| A: "Sign Up" | 52,340 | 2,355 | 4.50% |
| B: "Start Free Trial" | 51,890 | 2,543 | 4.90% |

- Difference: +0.40 pp (+8.9% relative)
- p-value: 0.003
- Confidence: 99.7%

**Decision:** Ship B. The new copy increased signups by ~9%.

### Example 2: Pricing Page Layout

**Hypothesis:** If we highlight the "Pro" plan with a "Most Popular" badge, Pro selections will increase by 15% because social proof influences choice.

**Results:**

| Variant | Visitors | Pro Selected | Rate |
|---------|----------|--------------|------|
| A: No badge | 8,450 | 1,267 | 15.0% |
| B: With badge | 8,380 | 1,424 | 17.0% |

- Difference: +2.0 pp (+13.3% relative)
- p-value: 0.048
- Confidence: 95.2%

**Decision:** Ship B. Marginal significance, but positive direction with good relative lift.

### Example 3: Failed Test

**Hypothesis:** If we add testimonials above the fold, conversions will increase by 10% because social proof builds trust.

**Results:**

| Variant | Visitors | Conversions | Rate |
|---------|----------|-------------|------|
| A: No testimonials | 12,000 | 600 | 5.00% |
| B: With testimonials | 12,200 | 585 | 4.79% |

- Difference: -0.21 pp (-4.2% relative)
- p-value: 0.32
- Confidence: 68%

**Decision:** No significant difference. Keep A (simpler). Hypothesis was wrong - testimonials may have distracted from CTA.

**Learning:** Test testimonial placement below the fold instead.

---

## Implementation Checklist

- [ ] Define clear hypothesis (if/then/because)
- [ ] Choose ONE primary metric
- [ ] Calculate required sample size
- [ ] Set up proper randomization
- [ ] Run test to completion (no early stopping)
- [ ] Check statistical significance
- [ ] Document results and learnings
- [ ] Ship winner or iterate

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Peeking at results | Inflates false positives | Wait for full sample size |
| Testing too many things | Cannot isolate cause | One change per test |
| Sample too small | Unreliable results | Calculate sample size upfront |
| Wrong metric | Optimizing for wrong thing | Choose metric tied to business goal |
| Running forever | Wastes traffic | Set end date based on sample size |
| Ignoring guardrail metrics | Win primary, hurt overall | Always check secondary metrics |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Web testing | Optimizely, VWO, Google Optimize |
| Product testing | LaunchDarkly, Split.io, Statsig |
| Statistics | Custom calculator, Evan Miller |
| Analysis | Mixpanel, Amplitude, Python |

---

## Sample Size Calculator

```
INPUTS:
────────────────────────────
Baseline conversion rate:    ____% [a]
Minimum detectable effect:   ____% relative [b]
Significance level:          95% (standard)
Power:                       80% (standard)

CALCULATION:
────────────────────────────
Absolute MDE = a × (b/100) = ____% [c]

Sample per variant ≈ 16 × (a × (1-a)) / c²
                   = 16 × (____ × ____) / ____²
                   = ______ users

Total sample needed = ______ × 2 = ______ users

Duration = Total sample / Daily traffic
         = ______ / ______ = ______ days
```

---

## Related Methodologies

- **multivariate-testing:** Multivariate Testing (testing multiple variables)
- **statistical-significance:** Statistical Significance (deep dive on stats)
- **funnel-optimization:** Funnel Optimization (where to test)

---

*Methodology: ab-testing-framework | Growth | faion-growth-agent*
