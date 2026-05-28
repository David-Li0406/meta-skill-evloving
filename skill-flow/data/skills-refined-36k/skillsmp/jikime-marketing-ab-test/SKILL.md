---
name: jikime-marketing-ab-test
description: A/B testing and experimentation specialist for designing statistically valid tests, calculating sample sizes, and analyzing experiment results.
version: 1.0.0
tags: ["marketing", "ab-test", "experimentation", "statistics", "optimization"]
triggers:
  keywords: ["A/B test", "split test", "experiment", "hypothesis", "variant", "multivariate", "statistical significance", "AB테스트", "실험", "가설"]
  phases: ["plan", "run"]
  agents: ["frontend", "backend", "manager-strategy"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~7000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# A/B Test Design & Analysis

## Quick Reference (30 seconds)

A/B Testing Specialist - Design tests that produce statistically valid, actionable results.

Core Principles:
- **Hypothesis First**: Not just "let's see what happens"
- **Single Variable**: Test one thing at a time
- **Statistical Rigor**: Pre-determine sample size, don't peek and stop early
- **Business Impact**: Measure what matters to the business

Key Deliverables:
- Hypothesis documentation
- Sample size calculation
- Test design specification
- Results analysis

---

## Implementation Guide (5 minutes)

### Hypothesis Framework

```
┌─────────────────────────────────────────────────────────────────┐
│  HYPOTHESIS TEMPLATE                                             │
├─────────────────────────────────────────────────────────────────┤
│  Because [observation/data],                                     │
│  we believe [change]                                             │
│  will cause [expected outcome]                                   │
│  for [audience].                                                 │
│  We'll know this is true when [metrics].                        │
└─────────────────────────────────────────────────────────────────┘
```

**Weak Hypothesis:**
> "Changing the button color might increase clicks."

**Strong Hypothesis:**
> "Because users report difficulty finding the CTA (per heatmaps and feedback), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

### Good Hypotheses Include

| Component | Description |
|-----------|-------------|
| **Observation** | What prompted this idea (data, feedback, research) |
| **Change** | Specific modification being tested |
| **Effect** | Expected outcome and direction |
| **Audience** | Who this applies to |
| **Metric** | How success will be measured |

---

## Test Types

| Type | Description | Best For |
|------|-------------|----------|
| **A/B Test** | Two versions: Control vs. Variant | Single changes, most common |
| **A/B/n Test** | Multiple variants (A vs. B vs. C...) | Testing several options |
| **Multivariate (MVT)** | Multiple changes in combinations | Testing interactions |
| **Split URL** | Different URLs for variants | Major page changes |

---

## Sample Size Calculation

### Quick Reference Table

| Baseline Rate | 10% Lift | 20% Lift | 50% Lift |
|---------------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

### Calculation Inputs

| Input | Typical Value | Description |
|-------|---------------|-------------|
| Baseline conversion rate | Your current rate | What you're measuring now |
| Minimum detectable effect (MDE) | 10-20% relative | Smallest change worth detecting |
| Statistical significance | 95% | Confidence level |
| Statistical power | 80% | Probability of detecting real effect |

### Test Duration Formula

```
Duration = (Sample size × Number of variants) / (Daily traffic × Conversion rate)

Minimum: 1-2 business cycles (usually 1-2 weeks)
Maximum: Avoid running too long (novelty effects, external factors)
```

### Calculator Resources
- Evan Miller: evanmiller.org/ab-testing/sample-size.html
- Optimizely: optimizely.com/sample-size-calculator/

---

## Metrics Selection

### Metric Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  METRIC HIERARCHY                                                │
├─────────────────────────────────────────────────────────────────┤
│  PRIMARY METRIC (1 only)                                        │
│  └── Single metric that matters most                            │
│  └── Directly tied to hypothesis                                │
│  └── What you'll use to call the test                          │
│                                                                  │
│  SECONDARY METRICS (2-4)                                        │
│  └── Support primary interpretation                             │
│  └── Explain why/how change worked                              │
│                                                                  │
│  GUARDRAIL METRICS (1-3)                                        │
│  └── Things that shouldn't get worse                            │
│  └── Revenue, retention, satisfaction                           │
│  └── Stop test if significantly negative                        │
└─────────────────────────────────────────────────────────────────┘
```

### Metric Examples by Test Type

| Test Type | Primary | Secondary | Guardrails |
|-----------|---------|-----------|------------|
| **Homepage CTA** | CTA click rate | Time to click, scroll depth | Bounce rate, downstream conversion |
| **Pricing Page** | Plan selection rate | Time on page, plan distribution | Support tickets, refund rate |
| **Signup Flow** | Signup completion | Field completion, time to complete | User activation rate |

---

## Designing Variants

### What to Vary

| Category | Elements |
|----------|----------|
| **Headlines/Copy** | Message angle, value prop, specificity, tone |
| **Visual Design** | Layout, color, images, hierarchy |
| **CTA** | Button copy, size, placement, number |
| **Content** | Information included, order, amount, social proof |

### Variant Documentation Template

```
Control (A):
- Screenshot: [image]
- Description: Current state

Variant (B):
- Screenshot: [mockup]
- Specific changes: [list changes]
- Hypothesis: Why this will win
```

---

## Traffic Allocation

| Strategy | Split | Use Case |
|----------|-------|----------|
| **Standard** | 50/50 | Normal A/B test |
| **Conservative** | 90/10 or 80/20 | Limit risk of bad variant |
| **Ramping** | Start small, increase | Technical risk mitigation |

### Allocation Considerations

- **Consistency**: Users see same variant on return
- **Segment sizes**: Ensure segments are large enough
- **Time balance**: Balanced exposure across times of day/week

---

## Implementation Approaches

| Approach | How It Works | Best For |
|----------|--------------|----------|
| **Client-Side** | JavaScript modifies page after load | Marketing pages, quick changes |
| **Server-Side** | Variant determined before render | Product features, complex changes |
| **Feature Flags** | Binary on/off, can convert to A/B | Rollouts, simple toggles |

### Tools Reference

| Type | Tools |
|------|-------|
| Client-side | PostHog, Optimizely, VWO |
| Server-side | PostHog, LaunchDarkly, Split |

---

## Running the Test

### Pre-Launch Checklist

```
□ Hypothesis documented
□ Primary metric defined
□ Sample size calculated
□ Test duration estimated
□ Variants implemented correctly
□ Tracking verified
□ QA completed on all variants
□ Stakeholders informed
```

### During Test Rules

| DO | DON'T |
|----|-------|
| Monitor for technical issues | Peek at results and stop early |
| Check segment quality | Make changes to variants |
| Document external factors | Add traffic from new sources |
| Trust the process | End early because you "know" the answer |

### The Peeking Problem

Looking at results before sample size and stopping when significant leads to:
- False positives
- Inflated effect sizes
- Wrong decisions

**Solution**: Pre-commit to sample size and stick to it.

---

## Analyzing Results

### Result Interpretation Matrix

| Result | Meaning | Action |
|--------|---------|--------|
| **Significant winner** | Variant outperformed control | Implement variant |
| **Significant loser** | Control outperformed variant | Keep control, learn why |
| **No significant difference** | Not enough evidence | Need more traffic or bolder test |
| **Mixed signals** | Inconsistent metrics | Dig deeper, segment analysis |

### Analysis Checklist

```
1. Did you reach sample size?
   → If not, result is preliminary

2. Is it statistically significant?
   → Check confidence intervals, p-value < 0.05

3. Is the effect size meaningful?
   → Compare to MDE, project business impact

4. Are secondary metrics consistent?
   → Do they support primary?

5. Any guardrail concerns?
   → Did anything get worse?

6. Segment differences?
   → Mobile vs desktop, new vs returning
```

---

## Test Documentation Template

```markdown
# A/B Test: [Name]

## Test Details
- Test ID: [ID in testing tool]
- Dates: [Start] - [End]
- Owner: [Name]

## Hypothesis
[Full hypothesis using framework]

## Test Design
- Type: A/B / A/B/n / MVT
- Duration: X weeks
- Sample size: X per variant
- Traffic allocation: 50/50

## Variants
[Control and variant descriptions with screenshots]

## Metrics
- Primary: [metric and definition]
- Secondary: [list]
- Guardrails: [list]

## Results
- Sample size: [achieved vs. target]
- Primary metric: [control] vs. [variant] ([% change], [confidence])
- Secondary metrics: [summary]
- Segment insights: [notable differences]

## Decision
Winner / Loser / Inconclusive

## Action
[What we're doing next]

## Learnings
[What we learned, what to test next]
```

---

## Common Mistakes

| Category | Mistakes |
|----------|----------|
| **Test Design** | Too small change, too many things, no hypothesis |
| **Execution** | Stopping early, changing mid-test, uneven allocation |
| **Analysis** | Ignoring confidence intervals, cherry-picking segments |

---

## Works Well With

Skills:
- `jikime-marketing-page-cro` - Generate test ideas from CRO analysis
- `jikime-marketing-copywriting` - Create variant copy
- `jikime-marketing-analytics` - Set up test measurement
- `jikime-marketing-psychology` - Apply psychological hypotheses

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
