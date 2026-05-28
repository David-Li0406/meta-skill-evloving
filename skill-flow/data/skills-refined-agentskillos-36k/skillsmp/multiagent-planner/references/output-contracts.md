# Output Contracts

Templates for each subagent. Brevity prevents context bloat.

## Output Size Guidance

All agents should produce concise, actionable output:

- **Summary**: 2-4 sentences capturing the key insight
- **Findings**: Top 5-7 most relevant items, prioritized by impact
- **Recommendations**: 3-5 concrete next steps

When in doubt, be brief. The orchestrator can always ask for more detail.

Avoid:
- Listing everything you found (prioritize instead)
- Repeating context the orchestrator already has
- Including code blocks unless essential to the finding

## Common Agent Guidelines

All agents must follow these rules:

- **Cite exact `file:line` references**; snippets only when essential (keep brief)
- **Prioritize top 5 items by impact**; drop the rest
- **Prefix assumptions with `ASSUMPTION:`** when evidence is incomplete
- **Include exact commands in backticks** for any verification steps
- **List up to 3 edge cases** that could break correctness/security
- **Cover the critical path**; skip edge cases unless directly relevant

---

## Explorer Output Contract

*Keep concise: aim for summary-level detail*

```markdown
## Context Pack

### Entry Points & Hot Paths
- [file:line] - description
- [file:line] - description

### Repo Conventions
- Test framework: [name]
- Lint: [command]
- Build: [command]
- Patterns: [key patterns observed]

### Invariants & Constraints
- [constraint 1]
- [constraint 2]

### Commands
- Run tests: `[command]`
- Run lint: `[command]`
- Build: `[command]`

### Touch Set (files likely to change)
- [file1]
- [file2]
- [file3]
```

---

## Bug Finder Output Contract

*Keep concise: root cause + minimal fix steps*

```markdown
## Root Cause Analysis

### Most Likely Cause
[1-2 sentence description]
**Evidence**: [file:line] - [observation]

### Alternative Hypotheses
1. [Alternative 1] - likelihood: [high/medium/low]
2. [Alternative 2] - likelihood: [high/medium/low]

### Minimal Fix Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Risk Notes
- [What could break]
- [Edge cases to consider]

### Verification Plan
- Command: `[test command]`
- Expected: [what should pass]
```

---

## Test Planner Output Contract

*Keep concise: key cases + stop rule*

```markdown
## Test Plan

### Test Targets
| Type | Location | Purpose |
|------|----------|---------|
| Unit | [path] | [what it tests] |
| Integration | [path] | [what it tests] |

### Key Cases
**Happy Path**:
- [case 1]
- [case 2]

**Edge Cases**:
- [edge case 1]
- [edge case 2]

**Negative Cases**:
- [error case 1]
- [error case 2]

### Regression Guard
The one test that would have caught this: [description]

### Fixtures/Mocks Strategy
- [mock 1]
- [mock 2]

### Stop Rule
Coverage complete when: [criteria]
```

---

## Refactorer Output Contract

*Keep concise: seams + step plan*

```markdown
## Refactor Plan

### Goal
[What improves] without breaking [what must not change]

### Seams (safe cut points)
1. [Seam 1] - [why safe]
2. [Seam 2] - [why safe]

### Step Plan
| Step | Action | Checkpoint | Verify |
|------|--------|------------|--------|
| 1 | [action] | [state] | [test] |
| 2 | [action] | [state] | [test] |
| 3 | [action] | [state] | [test] |

### Rollback Strategy
If [condition], revert to [checkpoint] using [method]

### Scope Control (avoid these)
- [opportunistic fix to skip]
- [tangent to avoid]
```

---

## Reviewer Output Contract

*Keep concise: top 5 risks + verdict*

```markdown
## Review Audit

### Verdict: [PROCEED / BLOCK]

### Top 5 Risks
1. **[Risk]** - Severity: [Critical/High/Medium/Low]
   Mitigation: [action]
2. **[Risk]** - Severity: [level]
   Mitigation: [action]
3. ...

### Must Fix Before Merge
- [ ] [Item 1]
- [ ] [Item 2]

### Nice to Have
- [ ] [Item 1]
- [ ] [Item 2]

### Questions to Answer
- [Question 1]
- [Question 2]
```

---

## Architect Output Contract

*Keep concise: architecture delta + recommendation*

```markdown
## Architecture Assessment

### Architecture Delta
**Current**: [description]
**Proposed**: [description]
**Reason**: [why change]

### Interfaces Impacted
| Interface | Change Type | Consumers |
|-----------|-------------|-----------|
| [name] | [add/modify/remove] | [list] |

### Data Model Considerations
- [consideration 1]
- [migration needed?]

### Non-Functional Concerns
- **Performance**: [impact]
- **Reliability**: [impact]
- **Scalability**: [impact]

### Decision Log
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| A | [pros] | [cons] | |
| B | [pros] | [cons] | **Recommended** |
```

---

## Searcher Output Contract

*Keep concise: answer + citations*

```markdown
## External Research

### Answer
[Direct answer to the question]

### Citations
1. [Source 1] - [URL or reference]
2. [Source 2] - [URL or reference]

### Version Caveats
- Applies to: [version range]
- Deprecated in: [version, if applicable]
- Breaking changes: [notes]

### Recommendation
[How to apply this in the current project context]
```

---

## Advisory Panel Output Contract

*Keep concise: 3 perspectives + synthesis*

```markdown
## Advisory Panel

### Pragmatist (Ship-It Path)
[~10 lines: minimal diff approach, quick wins, acceptable tradeoffs]

### Purist (Clean Architecture Path)
[~10 lines: ideal design, future-proofing, technical debt considerations]

### Skeptic (How This Fails)
[~10 lines: edge cases, security holes, operational risks, what could go wrong]

### Synthesis
**Recommended approach**: [which perspective to weight]
**Key tradeoff**: [what we're accepting]
**Mitigation**: [how to address skeptic concerns]
```
