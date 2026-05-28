# Plan File Template

Use this template when writing plan files to `.claude/plans/research_tasks/plan-{N}.md`.

## Full Template

```markdown
# Plan: {Experiment Name}

**Created:** {YYYY-MM-DD}
**Priority:** {1-5, where 1 is highest}
**Estimated Time:** {time estimate}

## Research Question

{One clear question this experiment answers}

## Hypothesis

{Specific, falsifiable prediction - must be testable}

## Variables

- **Independent:** {what you manipulate}
- **Dependent:** {what you measure}
- **Controls:** {what you hold constant}

## Supporting Evidence

{Why we expect this hypothesis might be true - cite papers, prior experiments, intuitions}

## Methodology

1. {Step-by-step procedure}
2. {Data collection approach}
3. {Analysis plan}

## Evaluation Criteria

- **Success:** {quantitative threshold for supporting hypothesis}
- **Failure:** {what falsifies the hypothesis}
- **Ambiguous:** {results requiring follow-up}

## Iteration Rewards

**After 1 min**: {smoke test - what should be true?}
**After 5 min**: {quick metric on small sample}
**After 15 min**: {what should the partial results look like?}
**After 30 min**: {pivot or persist decision point}

**Progress signals to log**:
- {metric 1 to print/plot}
- {metric 2}

**Green flags (REQUIRED before done)**:
- [ ] {checkpoint 1}
- [ ] {checkpoint 2}
- [ ] {checkpoint 3}

**Red flags (abandon immediately)**:
- {sign this approach won't work}

## Tractability Assessment

| Factor | Status |
|--------|--------|
| Experiment loop | {< 1 day / 1-7 days / > 1 week} |
| Data availability | {have it / can generate / need to collect} |
| Tooling | {exists / minor mods / build from scratch} |
| Swamp risk | {low / medium / high} |

## Todoist Tasks

- [ ] {task 1 if created}
- [ ] {task 2 if created}

## Open Questions

- {questions for follow-up}
```

## Quick Template (Minimal)

For simpler experiments, use this condensed version:

```markdown
# Plan: {Name}

**Created:** {date} | **Priority:** {1-5} | **Time:** {estimate}

## Question & Hypothesis
- **Q:** {research question}
- **H:** {falsifiable prediction}

## Method
1. {step 1}
2. {step 2}
3. {step 3}

## Iteration Rewards
- **1 min:** {smoke test}
- **5 min:** {quick metric}
- **30 min:** {pivot decision}

## Green Flags (REQUIRED)
- [ ] {done criterion 1}
- [ ] {done criterion 2}

## Red Flags (Abandon)
- {failure signal}
```

## Naming Convention

Files are named `plan-{N}.md` where N is sequential:
- `plan-1.md` (highest priority / next to execute)
- `plan-2.md`
- `plan-3.md`

When `/research-executor` consumes a plan:
1. Moves `plan-1.md` to `.claude/plans/research_tasks/executed/{date}_{name}.md`
2. Renumbers remaining plans (plan-2 → plan-1, etc.)
