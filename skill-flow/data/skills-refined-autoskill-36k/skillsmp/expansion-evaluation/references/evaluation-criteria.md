# Expansion Evaluation Criteria

## Decision Framework

### Primary Criteria

| Criteria        | Weight | Description                                      |
| --------------- | ------ | ------------------------------------------------ |
| ROADMAP Overlap | High   | Already planned? Merge vs add new?               |
| User Benefit    | High   | Direct value to recovery journey                 |
| Feasibility     | Medium | Achievable with current stack?                   |
| Dependencies    | Medium | What must exist first?                           |
| Technical Debt  | Low    | Complexity cost (acceptable if benefit high)     |
| Effort          | Low    | Size estimate (not blocking, just informational) |

### Decision Categories

| Symbol | Category | Meaning                                       | Action                 |
| ------ | -------- | --------------------------------------------- | ---------------------- |
| ✅     | ACCEPTED | Fits vision, feasible, valuable               | Add to ROADMAP         |
| ⏸️     | DEFERRED | Good idea, wrong time or dependencies missing | Park for later         |
| ❌     | REJECTED | Doesn't fit, too complex, low value           | Document why, move on  |
| 🔀     | MERGED   | Already in ROADMAP under different name       | Enhance existing item  |
| ❓     | DISCUSS  | Need more info, user input, or debate         | Log questions, revisit |

## Evaluation Questions

### 1. ROADMAP Overlap Check (First!)

- Is this already in ROADMAP.md?
- Is it partially covered by an existing item?
- Could it enhance an existing item?
- Is it truly new scope?

### 2. User Benefit Assessment

- Does this directly help someone in recovery?
- Is this "nice to have" or "need to have"?
- Does it align with app values (privacy, simplicity, evidence-based)?
- Would users notice if we didn't build this?

### 3. Feasibility Check

- Can we build this with Next.js + Firebase?
- Does it require new infrastructure?
- Are there security/privacy implications?
- Does it work offline (or need to)?

### 4. Dependency Mapping

- What features must exist before this?
- Does this enable other features?
- Is this blocked by technical work?
- Is this part of a larger epic?

### 5. Technical Debt Consideration

- Does this add complexity to the codebase?
- Will this require future refactoring?
- Does it conflict with architectural goals?
- Is the complexity worth the user benefit?

### 6. Effort Estimation

| Size | Meaning                            | Example                       |
| ---- | ---------------------------------- | ----------------------------- |
| S    | A few hours, single file           | Add a button, tweak UI        |
| M    | A day or two, multiple files       | New component, simple feature |
| L    | A week, cross-cutting changes      | New section, integration      |
| XL   | Multiple weeks, architectural work | Offline queue, encryption     |

## Recording Decisions

Format for tracker:

```markdown
### [Module]: [Idea Name]

**Decision:** ✅ ACCEPTED → M5 **Rationale:** [Brief explanation]
**Dependencies:** [If any] **Effort:** S/M/L/XL **Date:** YYYY-MM-DD
```

## Open Questions Protocol

When an idea raises a question:

1. Mark idea as ❓ DISCUSS
2. Add question to Open Questions section
3. Include context for why it's unclear
4. Note what information would resolve it
5. Revisit when information available

## Cross-Module Dependencies

Track when ideas span modules:

| Feature Idea | Technical Dependency | Notes               |
| ------------ | -------------------- | ------------------- |
| F4.x         | T1, T3               | Needs offline queue |
| F7.x         | T5                   | Export system       |
| F2.x         | T2, T4               | Sponsor + privacy   |

## Milestone Mapping Guide

| Milestone | Focus                        | Typical Candidates |
| --------- | ---------------------------- | ------------------ |
| M2        | Architecture, infrastructure | T1-T7 items        |
| M3        | Nashville local features     | F3 items           |
| M4        | Daily engagement             | F9, F5 items       |
| M5        | Inventories & step work      | F1 items           |
| M6        | Knowledge base               | F6 items           |
| M7        | Sponsor tooling              | F2, F7 items       |
| M8        | Personalization              | F8, F11 items      |
