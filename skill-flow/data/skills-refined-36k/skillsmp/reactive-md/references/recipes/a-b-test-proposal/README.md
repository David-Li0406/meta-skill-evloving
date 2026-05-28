---
title: Signup CTA Button Test
author: @product-team
status: ready-to-launch
date: 2026-01-13
instruction: "Copy this template for A/B testing proposals. Include hypothesis, metrics baseline, variant changes, audience, risk mitigation, and decision criteria."
tags: ["A/B-test", "experimentation", "conversion-optimization"]
related-jtbd: "Prototype features"
---

# Signup CTA Button Test: "Sign Up" vs "Get Started Free"

## Hypothesis

Changing the primary CTA button from "Sign Up" to "Get Started Free" will increase signup conversions by 15%, because "Free" reduces perceived risk and "Get Started" implies immediate value rather than a long-term commitment.

Our main page shows 3.2% CTR on the button. If we can lift that to 3.7%, we'll see roughly 50 additional signups per day at current traffic—that's $2,400/month in ARR at our average ACV, with near-zero implementation cost.

## Control: Current Button Copy

```jsx live
export default function ControlVariant() {
  return (
    <div className="p-6 bg-white rounded-lg shadow max-w-sm">
      <h2 className="text-xl font-bold mb-2">Ready to dive in?</h2>
      <p className="text-gray-600 mb-4">
        Join thousands of teams already using our platform.
      </p>
      <button className="w-full py-3 bg-blue-500 text-white rounded-lg font-medium">
        Sign Up
      </button>
    </div>
  );
}
```

**Performance baseline** (last 30 days):
- CTR: 3.2%
- Signup-to-completion: 45%
- Est. monthly signups: ~1,600

## Variant A: "Get Started Free"

Removing friction with two key words:

```jsx live
export default function VariantA() {
  return (
    <div className="p-6 bg-white rounded-lg shadow max-w-sm">
      <h2 className="text-xl font-bold mb-2">Ready to dive in?</h2>
      <p className="text-gray-600 mb-4">
        Join thousands of teams already using our platform.
      </p>
      <button className="w-full py-3 bg-green-500 text-white rounded-lg font-medium">
        Get Started Free
      </button>
    </div>
  );
}
```

Key word changes:
- "Sign Up" → "Get Started Free" (psychological safety: "Free" removes cost barrier, "Get Started" implies action not obligation)
- Color shift to green signals a positive, actionable choice

**Expected impact**: +15% CTR

## Variant B: "Start Free Trial" + Reassurance

More explicit about the trial nature with direct objection handling:

```jsx live
export default function VariantB() {
  return (
    <div className="p-6 bg-white rounded-lg shadow max-w-sm">
      <h2 className="text-xl font-bold mb-2">Ready to dive in?</h2>
      <p className="text-gray-600 mb-4">
        Join thousands of teams already using our platform.
      </p>
      <button className="w-full py-3 bg-blue-500 text-white rounded-lg font-medium">
        Start Free Trial →
      </button>
      <p className="text-center text-sm text-gray-500 mt-2">
        No credit card required
      </p>
    </div>
  );
}
```

This variant addresses the biggest objection: "Do I need to enter my credit card?" The reassurance text directly answers this fear.

**Expected impact**: +20% CTR

## Side-by-Side Comparison

```jsx live
import ABTestVariants from './ABTestVariants.jsx';

export default function AllVariants() {
  return (
    <ABTestVariants
      control={{
        title: "Control",
        buttonText: "Sign Up",
        buttonClass: "bg-blue-500",
        expectedCTR: "3.2%"
      }}
      variantA={{
        title: "Variant A",
        buttonText: "Get Started Free",
        buttonClass: "bg-green-500",
        expectedLift: 15
      }}
      variantB={{
        title: "Variant B",
        buttonText: "Start Free Trial →",
        buttonClass: "bg-blue-500",
        subtext: "No credit card required",
        expectedLift: 20
      }}
    />
  );
}
```

## Test Parameters

| Parameter | Value |
|-----------|-------|
| **Traffic split** | 33% / 33% / 34% |
| **Duration** | 2 weeks minimum |
| **Sample size** | 10,000 visitors per variant |
| **Primary metric** | Signup button CTR |
| **Secondary metrics** | Signup completion, Time to click |
| **Significance level** | 95% confidence |

## Audience

- All new visitors
- Desktop and mobile
- Exclude returning users

## Risks

| Risk | Mitigation |
|------|------------|
| Lower quality signups | Track 7-day retention as guardrail |
| Brand inconsistency | Run by design team before launch |
| Technical issues | QA all variants before going live |

## Timeline

| Date | Milestone |
|------|-----------|
| Week 1 | Implement variants, QA |
| Week 2-3 | Run experiment |
| Week 4 | Analyze results, document learnings |

## Decision Criteria

- **Ship Variant A/B if**: CTR increase ≥ 10% with 95% confidence
- **Iterate if**: Positive signal but < 95% confidence
- **Kill if**: Negative impact on signup completion rate

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
