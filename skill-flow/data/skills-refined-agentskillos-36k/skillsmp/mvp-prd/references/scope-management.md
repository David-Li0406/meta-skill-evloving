# Scope Management

Strategies for preventing scope creep and handling legitimate scope expansion.

## The Scope Triangle

Every PRD balances three constraints:

```
        Time
         /\
        /  \
       /    \
      /------\
   Scope    Quality
```

When one changes, others must adjust. For demo-grade PRDs:
- **Time:** Fixed (demo deadline)
- **Quality:** Non-negotiable (must work)
- **Scope:** Variable (cut here first)

## Scope Categories

### Core Scope
Must exist for demo to function:
- Primary user flow (happy path)
- Essential data operations
- Minimum viable feedback states

**Never cut from core scope.**

### Supporting Scope
Makes demo believable:
- Secondary flows
- Error handling
- Edge case coverage
- Loading states

**Cut last if needed.**

### Polish Scope
Makes demo impressive:
- Animations
- Micro-interactions
- Performance optimization
- Accessibility refinements

**Cut first if needed.**

### Out of Scope
Explicitly excluded:
- Features for future versions
- Enterprise-only features
- Performance at scale
- Full error coverage

**Document to prevent creep.**

## Scope Lock Protocol

### When to Lock
- Core flow defined
- Acceptance criteria written
- Dependencies identified
- Risk levels assigned
- Stakeholders aligned

### Lock Documentation
```markdown
## Scope Lock Record

**Date:** YYYY-MM-DD
**Version:** X.X

### Locked Scope
- [Feature 1]
- [Feature 2]

### Explicitly Out of Scope
- [Feature A] - reason
- [Feature B] - reason

### Change Process
All changes after lock require:
1. Impact assessment
2. Trade-off documentation
3. Stakeholder approval
```

## Expansion Handling

### Expansion Detection
Signs scope is creeping:
- "While we're at it..." statements
- New edge cases every discussion
- Requirements discovered during implementation
- "Quick addition" requests

### Expansion Assessment

For each proposed addition:

| Question | Answer |
|----------|--------|
| Does this block the core flow? | Yes → Add to core |
| Can demo work without it? | Yes → Defer |
| Is this a new feature disguised? | Yes → New sprint |
| Does this fix a bug? | Yes → Add immediately |

### Expansion Protocols

#### Protocol 1: Absorb
**When:** Addition is small, low risk, directly related
**Action:** Add to current sprint
**Document:** Note in PRD changelog

#### Protocol 2: Defer
**When:** Addition is valuable but not blocking
**Action:** Create follow-up ticket
**Document:** Add to "Future Scope" section

#### Protocol 3: Split
**When:** Addition is substantial (>20% new work)
**Action:** Create new sprint
**Document:** New PRD section or separate PRD

#### Protocol 4: Replace
**When:** New requirement replaces existing scope
**Action:** Swap items, keep total scope constant
**Document:** Update PRD, note trade-off

## Saying No Effectively

### The "Yes, and Later" Pattern
Instead of: "No, we can't do that"
Say: "Yes, that's valuable—let's add it to Sprint 2"

### The Trade-off Pattern
"We can add [X], but we'd need to cut [Y] to meet the deadline. Which is more important for the demo?"

### The Scope Budget Pattern
"We have capacity for N more story points this sprint. [X] is M points. What should we cut to fit it?"

## Scope Negotiation Tactics

### Tactic 1: MoSCoW Prioritization
- **Must have:** Core scope, non-negotiable
- **Should have:** Supporting scope, high value
- **Could have:** Polish scope, if time permits
- **Won't have:** Explicitly out of scope

### Tactic 2: Impact/Effort Matrix

```
High Impact │ Do First    │ Plan Carefully
            │ (Quick Wins)│ (Major Features)
            │─────────────┼─────────────────
Low Impact  │ Fill Time   │ Don't Do
            │ (If Spare)  │ (Scope Creep)
            └─────────────┴─────────────────
             Low Effort    High Effort
```

### Tactic 3: Demo Lens
"Will an investor/user notice if this is missing?"
- Yes → Core scope
- Maybe → Supporting scope
- No → Polish or cut

## Scope Documentation

### PRD Scope Section Template
```markdown
## Scope Definition

### In Scope (Core)
- [ ] User can [action]
- [ ] System provides [feedback]
- [ ] Data persists [where/how long]

### In Scope (Supporting)
- [ ] Error handling for [cases]
- [ ] Loading states for [operations]
- [ ] Edge case: [description]

### In Scope (Polish)
- [ ] Animation for [interaction]
- [ ] Micro-interaction: [description]
- [ ] Performance: [optimization]

### Out of Scope
| Feature | Reason | Future Version |
|---------|--------|----------------|
| [Feature] | [Why excluded] | V2 / Never |

### Scope Change Log
| Date | Change | Impact | Decision |
|------|--------|--------|----------|
| YYYY-MM-DD | [Change] | [Impact] | Added/Deferred/Rejected |
```

## Red Flags Checklist

Scope is at risk when:
- [ ] PRD has grown >50% since start
- [ ] "Final" requirements keep changing
- [ ] Team discovers missing pieces during implementation
- [ ] Stakeholders add "small" requests frequently
- [ ] Original deadline feels impossible
- [ ] Core flow keeps expanding

## Recovery Strategies

When scope has already crept:

### Strategy 1: Hard Reset
1. Stop all implementation
2. Re-evaluate from core scope
3. Cut everything non-essential
4. Restart with locked scope

### Strategy 2: Phase Split
1. Identify what's shippable now
2. Create MVP cut (what works)
3. Move rest to Phase 2
4. Ship MVP, then iterate

### Strategy 3: Timeline Extension
1. Document scope that caused expansion
2. Calculate realistic new timeline
3. Get stakeholder buy-in
4. Lock scope at new level

## Metrics to Track

| Metric | Target | Red Flag |
|--------|--------|----------|
| Scope additions post-lock | <3 | >5 |
| Scope growth % | <20% | >50% |
| Out-of-scope requests | Declining | Increasing |
| Core scope stability | 100% | <90% |
| Features cut pre-ship | <20% | >40% |
