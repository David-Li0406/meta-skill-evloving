# metaprompt quality rubric

validation checklist for generated metaprompts.

## dimensions

| dimension | weight | description |
|-----------|--------|-------------|
| clarity | 25% | roles, I/O, constraints unambiguous |
| completeness | 25% | workflow + failure modes + output spec |
| groundedness | 20% | technical claims cited or marked |
| reusability | 15% | parameters cover variability |
| operability | 15% | machine-readable, deterministic |

## clarity checks

| check | pass criteria |
|-------|---------------|
| role defined | explicit statement of who/what the agent is |
| inputs listed | all required inputs enumerated |
| outputs specified | exact deliverables with format |
| constraints explicit | must-do and must-not-do clear |
| scope bounded | in-scope and out-of-scope defined |

## completeness checks

| check | pass criteria |
|-------|---------------|
| workflow present | step-by-step phases with named steps |
| failure modes | at least 3 failure scenarios handled |
| output sections | all required sections listed |
| examples included | at least one happy path example |
| validation method | how to verify output correctness |

## groundedness checks

| check | pass criteria |
|-------|---------------|
| no phantom specifics | no invented APIs, versions, paths |
| citations present | technical claims have sources |
| official docs preferred | primary sources over blogs |
| unverified marked | uncertain claims labeled |
| version caveats | volatile info has disclaimers |

## reusability checks

| check | pass criteria |
|-------|---------------|
| parameterized | variable parts are parameters |
| defaults sensible | missing params have safe defaults |
| domain modules | optional sections for different contexts |
| extensible | clear extension points |
| not overfit | works beyond the example case |

## operability checks

| check | pass criteria |
|-------|---------------|
| machine summary | JSON block with structured output |
| deterministic sections | same input → same structure |
| copy-pasteable | no broken XML/markdown |
| size appropriate | not bloated with redundancy |
| testable | can validate output programmatically |

## scoring

```
score = (clarity * 0.25) + (completeness * 0.25) +
        (groundedness * 0.20) + (reusability * 0.15) +
        (operability * 0.15)
```

| score | grade | action |
|-------|-------|--------|
| 90-100 | A | ready to use |
| 80-89 | B | minor improvements |
| 70-79 | C | address gaps before use |
| < 70 | F | significant rework needed |

## quick validation

run these checks before finalizing:

```
[ ] roles and mission clear?
[ ] all inputs documented?
[ ] output format specified?
[ ] workflow has named phases?
[ ] failure modes handle common issues?
[ ] technical claims cited?
[ ] no invented specifics?
[ ] parameters cover variations?
[ ] JSON summary included?
[ ] XML/markdown valid?
```
