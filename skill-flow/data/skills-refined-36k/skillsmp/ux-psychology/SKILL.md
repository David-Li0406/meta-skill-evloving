---
name: ux-psychology
description: Apply UX psychology principles when building UI components, forms, pricing pages, onboarding flows, checkout experiences, modals, or any user-facing interface. Use when designing CTAs, implementing progress indicators, creating loading states, improving user engagement, or reviewing UI for psychological effectiveness.
user-invocable: false
---

# UX Psychology Frontend Development Guide

Apply these 46 UX psychology principles to predict user behavior and design more effective interfaces. This skill provides actionable guidelines with code examples for frontend implementation.

## Quick Reference

| Category | Key Concepts | When to Use |
|----------|--------------|-------------|
| [Cognition](concepts/cognition.md) | Cognitive Load, Selective Attention, Banner Blindness | Forms, information-dense pages |
| [Biases](concepts/biases.md) | Anchor, Confirmation, Expectation, Familiarity | Pricing, comparisons, navigation |
| [Behavioral](concepts/behavioral.md) | Nudge, Default, Decoy, Framing, Priming | Conversions, sign-ups, purchases |
| [Value](concepts/value.md) | Loss Aversion, Scarcity, Endowment, Sunk Cost | Retention, urgency, personalization |
| [Engagement](concepts/engagement.md) | Gamification, Variable Reward, Goal Gradient, Zeigarnik | Progress tracking, habit formation |
| [Experience](concepts/experience.md) | Peak-End Rule, User Delight, Labor Illusion | Loading states, completion flows |
| [UI Design](concepts/ui-design.md) | Doherty Threshold, Progressive Disclosure, Visual Hierarchy | Performance, layout, navigation |
| [Social](concepts/social.md) | Social Proof, Halo Effect | Trust building, credibility |
| [Caution](concepts/caution.md) | Reactance, Decision Fatigue, Intentional Friction | Avoiding dark patterns |
| [Research](concepts/research.md) | Hawthorne Effect, Survey Bias, Empathy Gap | User testing, research design |

## Core Principles Summary

### Reduce Friction
- Split complex forms into steps (Cognitive Load)
- Use skeleton UI for loads over 400ms (Doherty Threshold)
- Set smart defaults (Default Bias)
- Limit choices to reduce fatigue (Decision Fatigue)

### Guide Behavior
- Show original price before discount (Anchor Effect)
- Frame positively: "90% success" not "10% failure" (Framing)
- Use progress bars near completion (Goal Gradient)
- Ask satisfaction before reviews (Priming)

### Create Value
- Show what users lose on cancel (Loss Aversion)
- Display limited stock/time (Scarcity)
- Personalize the experience (Endowment Effect)
- Celebrate completions (Peak-End Rule)

### Build Trust
- Show reviews, user counts, logos (Social Proof)
- Provide value before asking for payment (Reactance)
- Add confirmation for destructive actions (Intentional Friction)

## Implementation Checklist

See [checklist.md](checklist.md) for a complete checklist to review your UI against these principles.

## Detailed References

Each concept file contains:
- Definition and psychological basis
- Implementation guidelines
- Code examples (JSX/CSS)
- Common patterns

Browse by category:
- [Cognition & Perception](concepts/cognition.md) - Managing mental effort
- [Biases](concepts/biases.md) - Leveraging cognitive shortcuts
- [Behavioral Guidance](concepts/behavioral.md) - Influencing decisions
- [Value Perception](concepts/value.md) - Creating perceived value
- [Engagement](concepts/engagement.md) - Driving continued use
- [Experience Design](concepts/experience.md) - Memorable moments
- [UI Design Principles](concepts/ui-design.md) - Visual and interaction patterns
- [Social Influence](concepts/social.md) - Trust and credibility
- [Effects to Watch](concepts/caution.md) - Avoiding pitfalls
- [Research Considerations](concepts/research.md) - Testing awareness

## Source

Based on [Shokasonjuku Inc. UX Psychology Concepts](https://www.shokasonjuku.com/ux-psychology)
