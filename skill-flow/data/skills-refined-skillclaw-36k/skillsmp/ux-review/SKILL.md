---
name: ux-review
description: Reviews UI code or designs for UX issues, suggests improvements based on Laws of UX. Use when reviewing components, designing new interfaces, or improving user experience for web applications.
---

## Task

Analyze the provided UI code or design context and provide actionable UX recommendations.

**For code review:** Read the relevant component files first, then identify violations.
**For new designs:** Ask clarifying questions about user goals, then suggest patterns.

## Output Format

For each issue found, output:

```
**[Law Name]** - [Severity: High/Medium/Low]
- Issue: [One sentence describing the problem]
- Fix: [Specific actionable fix]
- Location: [file:line if reviewing code]
```

Group by severity. Limit to top 10 issues unless asked for comprehensive review.

## Quick Reference: Most Common Web UX Issues

### Layout & Visual Hierarchy
| Check | Law | Action |
|-------|-----|--------|
| Touch targets < 44px | Fitts's Law | Increase to min 44x44px |
| Related items spaced apart | Proximity | Group with whitespace or containers |
| No visual grouping | Common Region | Add cards, borders, or background colors |
| Inconsistent button styles | Similarity | Unify styles for same-type actions |
| Primary CTA doesn't stand out | Von Restorff | Use distinct color/size for primary action |

### Navigation & Choices
| Check | Law | Action |
|-------|-----|--------|
| Too many nav items (>7) | Miller's Law | Group into categories, use progressive disclosure |
| Many options without default | Hick's Law | Highlight recommended option, reduce choices |
| Non-standard patterns | Jakob's Law | Use familiar conventions (hamburger, search icon, etc.) |
| Important items in middle | Serial Position | Move to start or end of lists |
| No progress indicator | Goal-Gradient | Add progress bar/steps for multi-step flows |

### Feedback & Performance
| Check | Law | Action |
|-------|-----|--------|
| No loading state | Doherty Threshold | Add spinner/skeleton for >400ms operations |
| Form rejects minor variations | Postel's Law | Accept flexible input, normalize internally |
| No error recovery | Peak-End Rule | Design graceful error states with clear next steps |
| Manual user input for known data | Tesler's Law | Auto-fill, save state, reduce user effort |

### Cognitive Load
| Check | Law | Action |
|-------|-----|--------|
| Wall of text | Chunking | Break into sections with headers |
| Complex form on one page | Zeigarnik | Split into steps with progress indicator |
| Users must remember across pages | Working Memory | Persist selections, show context |
| No embedded help | Paradox of Active User | Add tooltips, inline hints, contextual help |

## Review Checklist

When reviewing, check these in order:

1. **Critical (blocks users)**
   - Touch/click targets too small (Fitts's Law)
   - No feedback on actions (Doherty Threshold)
   - Confusing navigation structure (Jakob's Law)

2. **Major (causes friction)**
   - Choice overload without guidance (Hick's Law)
   - Poor visual grouping (Proximity, Common Region)
   - Missing progress indicators (Goal-Gradient)

3. **Minor (polish)**
   - Inconsistent visual treatment (Similarity)
   - Suboptimal element positioning (Serial Position)
   - Missing micro-interactions (Flow)

## Design Mode

When designing new interfaces:

1. **Start with user goal** - What's the primary action?
2. **Apply 80/20** (Pareto) - Focus on the 20% of features serving 80% of users
3. **Match mental models** (Jakob's Law) - Use patterns from similar products
4. **Minimize choices** (Hick's Law) - Default to best option, hide advanced settings
5. **Show progress** (Goal-Gradient, Zeigarnik) - Break flows into visible steps
6. **Design the end** (Peak-End Rule) - Success states deserve premium attention

## When to Read Full Laws Reference

Read [laws-reference.md](laws-reference.md) when:
- User asks for detailed explanation of a specific law
- Recommending significant architectural changes
- Writing documentation or educating team members
