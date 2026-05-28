---
name: ux-design
description: Design user experiences with usability focus. Use when planning user flows, navigation, forms, error handling, or accessibility. Complements frontend-design (visual) with UX structure.
---

<principles>
## Visual Foundation (CRAP)
1. [Contrast]: hierarchy through size/color/weight, important = stands out
2. [Repetition]: consistent patterns, colors, spacing throughout
3. [Alignment]: consistent alignment, grid-based layout
4. [Proximity]: related items close, unrelated items separated

## Interaction

5. [Scannable]: F-pattern layout, primary info top-left
6. [Progressive]: essentials first → details on demand
7. [Constrained]: dropdown over free text, radio over checkbox swarm
8. [Recoverable]: undo for destructive, soft-delete over hard-delete
9. [Semantic]: `<button>` not `<div onclick>`, `<label>` for all inputs
   </principles>

<patterns>
## Navigation
- depth >3 → breadcrumbs
- <7 same-page sections → tabs
- many persistent sections → sidebar
- mobile primary actions → bottom nav (thumb zone)

## Forms

- layout: single column, labels top-aligned
- groups: visual separation between related fields
- defaults: pre-fill from context
- password: strength indicator + reveal toggle
- submit: loading state + disable button

## Feedback

- <100ms → immediate state change
- > 1s → skeleton/progress bar
- success → inline confirmation at action source
- error → inline at source
- empty → guide next action: "Add your first {item}"

## Destructive

- [Decision] reversible → Ctrl+Z undo | irreversible → confirm modal
- confirm modal: show affected items, require explicit action
- critical (delete account) → type-to-confirm
  </patterns>

<labels>
- buttons: verb + object (`Save draft` not `OK`)
- specific: `Add to cart` not `Submit`
- user vocabulary: `Projects` not `Entities`
</labels>

<accessibility>
- focus: trap in modals, restore on close
- contrast: WCAG AA (4.5:1 text, 3:1 UI)
- touch: ≥44px targets
- required: mark with `*`, announce to screen readers
</accessibility>

<workflow>
## UX Design Process
1. Understand: Who is {user}? {user}'s goal: {goal}. Context: {when/where/device}
2. Map current state, identify pain points [skip if new]
3. Sketch flow: {entry point} → {key actions} → {success state}
4. Design the main structure
5. Identify friction: where might users hesitate, misunderstand, or abandon?
6. Design for failure: what errors can occur? how does user recover?
7. Find issues → iterate from step 3
  - Consider using CRAP <heuristics> <checklist> <labels> <accessibility> etc...
</workflow>

<heuristics>
## Nielsen's 10 (evaluation checklist)
- [ ] 1. Visibility of system status
- [ ] 2. Match between system and real world
- [ ] 3. User control and freedom (undo, exit)
- [ ] 4. Consistency and standards
- [ ] 5. Error prevention
- [ ] 6. Recognition over recall
- [ ] 7. Flexibility and efficiency
- [ ] 8. Aesthetic and minimalist design
- [ ] 9. Help users recover from errors
- [ ] 10. Help and documentation
</heuristics>

<checklist>
## Implementation
- [ ] 1. Location always clear?
- [ ] 2. Errors actionable?
- [ ] 3. Tab order logical?
- [ ] 4. Touch targets ≥44px?
- [ ] 5. Focus managed in modals?
- [ ] 6. Labels on all inputs?
</checklist>
