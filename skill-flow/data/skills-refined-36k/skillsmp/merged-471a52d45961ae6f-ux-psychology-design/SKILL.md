---
name: ux-psychology-design
description: Use this skill to apply UX psychology principles in UI design, enhancing user experience across various interfaces such as landing pages, forms, and onboarding processes.
---

# UX Psychology and Design

This skill applies principles of UX psychology to improve UI design, making interfaces more user-friendly and engaging.

## Usage

```
/ux-psychology-design <file or URL or screenshot>
```

Analyze applicable UX psychology principles and provide design improvement suggestions.

## Key Principles

### Cognitive and Attention Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Cognitive Load | The mental effort required for information processing | Present information in stages, break complex tasks into smaller parts |
| Selective Attention | The tendency to focus on relevant information | Visually emphasize important elements |
| Banner Blindness | The tendency to ignore elements that appear as ads | Avoid designing important CTAs like advertisements |
| Decision Fatigue | Diminished decision-making ability after repeated choices | Reduce options, set default values |

### Memory and Learning Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Serial Position Effect | Items at the beginning and end are more memorable | Place important items at the start or end |
| Zeigarnik Effect | Unfinished tasks are more memorable | Use progress bars, visualize incomplete tasks |
| Progressive Disclosure | Information is revealed gradually | Use onboarding wizards or step-by-step forms |

### Bias and Judgment Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Anchoring Effect | The first piece of information serves as a reference point | Display high-priced plans first |
| Confirmation Bias | Preference for information that confirms existing beliefs | Design information to align with user expectations |
| Familiarity Bias | Preference for familiar items | Follow common UI patterns |
| Framing Effect | The way information is presented affects judgment | Use positive framing (e.g., "90% success" vs. "10% failure") |
| Loss Aversion | Tendency to overvalue losses | Use phrases like "limited time offer" |

### Motivation and Behavior Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Goal Gradient Effect | Motivation increases as one approaches a goal | Display progress bars, show remaining steps |
| Gradual Requests | Start with small requests before larger ones | Begin with simple actions |
| Reactance | Resistance when forced | Provide choices, avoid being pushy |
| Variable Rewards | Unpredictable rewards enhance motivation | Incorporate gamification elements |

### Social and Trust Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Social Proof | Influence from others' actions or opinions | Show reviews, user counts, "popular" labels |
| Halo Effect | A single impression affects overall evaluation | Use trustworthy design and display achievements |
| Observational Effect | Behavior changes when being watched | Consider privacy concerns |

### Experience and Impression Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Aesthetic-Usability Effect | Beautiful designs are perceived as more usable | Create visually appealing UIs |
| Peak-End Rule | Focus on the peak and end of experiences | Leave a good impression at the end, use thank-you pages |
| Expectation Bias | Preconceived expectations affect evaluations | Set appropriate expectations, avoid overpromising |
| Labor Illusion | Visible effort increases perceived value | Use loading animations, visualize search efforts |

### Default and Choice Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Default Effect | Tendency to stick with initial settings | Set appropriate default values |
| Decoy Effect | Guide choices through options | Highlight recommended plans |
| Scarcity Effect | Limited availability increases desire | Show stock levels, time-limited offers |

### Visual and Design Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Visual Hierarchy | Organize information by visual priority | Use size, color, and position to indicate importance |
| Visual Anchoring | Draw attention through visual emphasis | Highlight CTA buttons with contrast |
| Skeuomorphism | Mimic real-world appearances | Use familiar metaphors |

### Responsiveness Principles

| Principle | Description | Application Example |
|-----------|-------------|---------------------|
| Doherty Threshold | Interest is lost after waiting more than 0.4 seconds | Ensure fast responses, use loading indicators |

## Output Format

```markdown
## UX Psychology Analysis

### Applied Principles
- **[Principle Name]**: How it is applied

### Improvement Suggestions
| Principle | Current Issue | Improvement Proposal | Expected Effect |
|-----------|---------------|---------------------|-----------------|
| Principle Name | Issue Description | Specific improvement proposal | Expected outcome |

### Notes
- Be cautious of over-application leading to dark patterns.
- Prioritize user benefits.
- A/B testing is recommended to validate effectiveness.
```

## Quick Reference

### Form Design

| Issue | Principle | Implementation |
|-------|-----------|----------------|
| Difficult input | Default Effect | Set appropriate default values |
| Too many fields | Progressive Disclosure | Split into steps or use collapsible sections |
| Unclear errors | Cognitive Load | Use inline validation |
| Anxiety about submission | Social Proof | Display "used by X people" |

### Button and CTA Design

| Issue | Principle | Implementation |
|-------|-----------|----------------|
| Low clicks | Visual Hierarchy | Emphasize with color and size |
| Confusion | Decoy Effect | Clearly highlight recommended plans |
| Anxiety about pressing | Loss Aversion | Use phrases like "free" or "cancel anytime" |

### Loading Design

| Issue | Principle | Implementation |
|-------|-----------|----------------|
| Long wait times | Doherty Threshold | Use streaming or skeleton screens |
| Unclear progress | Labor Illusion | Show processing content |
| Unclear completion | Peak-End Rule | Use success animations |

## Anti-Patterns

### ❌ Dark Patterns

Avoid the following manipulative UX patterns:

- **Confirmshaming**: Embarrassing wording for rejection options
- **Hidden Costs**: Concealing additional fees until the end
- **Roach Motel**: Easy to sign up, difficult to cancel
- **Trick Questions**: Confusing checkboxes

### ❌ Over-Application

- Abuse of gamification (excessive points/badges)
- False scarcity (always showing "limited stock")
- Forced nudges (making choices appear non-existent)

## Related Skills

- **ui-ux-pro-max**: Visual implementation
- **lp-optimizer**: Page optimization
- **marketing-psychology**: Marketing-focused psychology
- **copywriting**: Applying psychology to copywriting