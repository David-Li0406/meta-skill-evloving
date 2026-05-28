# Validation & Memory Management

Guidelines for maintaining design consistency across conversations.

## When to Reference This Skill

Re-read this skill when:
- Starting a new design task
- User mentions "design review" or "design consistency"
- Creating or modifying presets
- Making UI/UX decisions that affect multiple components

## Design Decision Checklist

Before finalizing any design work:

```
- [ ] Spacing uses 4px grid (4, 8, 12, 16, 24, 32)
- [ ] Padding is symmetrical (or justified exception)
- [ ] Border radius is consistent with chosen system
- [ ] Depth strategy matches design direction (borders-only OR shadows, not mixed)
- [ ] Color is used for meaning, not decoration
- [ ] Typography hierarchy is maintained
- [ ] Accessibility: WCAG AA contrast met
```

## Preset Validation

When creating or modifying presets:

1. **Structure check**: Does the hierarchy make semantic sense?
2. **Naming check**: Are labels descriptive of purpose (not appearance)?
3. **Flexibility check**: Uses `fr` units or `flex-grow` instead of fixed widths?
4. **Default check**: Are initial values reasonable for most use cases?

## Common Mistakes to Catch

- Mixed depth strategies (shadows on some cards, borders on others)
- Inconsistent border radius within the same view
- Decorative color that doesn't communicate meaning
- Asymmetric padding without justification
- Fixed widths where flexible units would work better
