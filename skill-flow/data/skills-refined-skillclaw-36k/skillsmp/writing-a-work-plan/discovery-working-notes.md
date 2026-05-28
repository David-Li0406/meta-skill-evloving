# Writing Work Plans: Discovery Working Notes

Working notes from a discovery session on 2025-01-26.

---

## Skill Development Notes

### Insight 1: Infrastructure Tasks Follow Create → Verify → Commit

Infrastructure work (scaffolding, config, skeleton files) doesn't have tests. Verification is operational: "does it build?", "does the command run?", "can I import the module?"

**Skill implication**: Define two (later three) task types with different verification patterns.

### Insight 2: One AC = One Task (Usually)

For M1, each AC mapped cleanly to one task. This keeps tasks bite-sized and provides clear completion signals.

**Skill implication**: Start with 1:1 mapping. If an AC is compound ("X and Y"), split into multiple tasks.

### Insight 3: Explicit Verify and Commit Steps

Implementers (especially LLM agents) benefit from explicit "verify" and "commit" steps. Without them, they might skip verification or batch commits inappropriately.

**Skill implication**: Always include verification and commit steps in task definitions.

### Insight 4: Separate Scaffold Task for Each Component

Before TDD cycles, create a scaffold task that:
- Creates the module file with class skeleton
- Creates the test file with test stubs (empty test functions with descriptive names)
- This is infrastructure (verified operationally: "pytest runs")

### Insight 5: Tests Should Have Single Assertions (Arrange/Act/Assert)

Each test should:
1. **Arrange**: Set up preconditions
2. **Act**: Execute the behavior
3. **Assert**: Verify a single outcome

If an AC requires testing multiple outcomes, split into multiple tests.

### Insight 6: Include Concrete Test Code in Plans

LLM agents (and human engineers unfamiliar with the codebase) benefit from seeing example test code. This:
- Reduces ambiguity about what to test
- Shows the expected structure (Arrange/Act/Assert)
- Documents the exact behavior being verified

### Insight 7: Verify Framework Behaviors Explicitly

Even if a behavior is "handled by the framework" (like requests.Session cookie persistence), include a verification task. This:
- Documents the expected behavior
- Catches regressions if the implementation changes
- Confirms understanding is correct

### Insight 8: Codebase Verification Before AND After

**Before writing tasks**:
- Run `codebase-investigator` to check design assumptions
- Prevents planning tasks for files/features that don't exist

**After writing tasks**:
- Run `codebase-investigator` again to verify implementability
- Catches any drift that emerged during planning

### Insight 9: Work Plans Live Separate from Design Docs

Work plans should not be in the same document as design docs because:
- Design docs can be old; work plans must be fresh
- Work plans are implementation-level detail; design docs are architecture-level
- Keeping them separate allows regeneration without touching design

**Location**: `docs/work-plans/YYYY-MM-DD-<plan-name>/milestone_##.md`

### Insight 10: Interactive Milestone-by-Milestone Review

Process milestones one at a time:
1. Write tasks for milestone N
2. Present to user for review
3. Iterate until approved
4. Proceed to milestone N+1

This prevents wasted effort if early milestones need rework.

### Insight 11: Full Context in Document Header

Each milestone plan document should include:
- Goal, Architecture notes, Tech stack, Scope, Codebase verification status, References

This ensures someone reading the plan has zero prior context.

### Insight 12: Integration Is a Third Task Type

Integration work is distinct from infrastructure and functionality:
- **Infrastructure**: Creates scaffolding, verified operationally
- **Functionality**: Implements core behavior, verified via unit tests (TDD)
- **Integration**: Wires components together, verified via integration tests

### Insight 13: Integration Milestones Need Scaffold Task Too

Just like functionality milestones, integration milestones benefit from a scaffold task that sets up integration test files and fixtures.

### Insight 14: Fixtures Bridge Unit and Integration Testing

Integration tests need fixtures that set up the "world" — authenticated sessions, databases, mock external services. These should be defined during the scaffold task.

### Insight 15: Integration AC Map to End-to-End Flows

Each AC in an integration milestone is a complete user flow. The task structure:
- One task per AC
- Each task wires necessary components and tests end-to-end
- TDD still applies: write failing integration test, then wire components

---

## Questions and Resolutions

### Question: Should verify/commit be explicit or assumed?

**Resolution**: Explicit (Recommended). Implementers might skip verification without explicit steps.

### Question: Should scaffold be separate from first TDD task?

**Resolution**: Yes, separate. Scaffolding is infrastructure; TDD cycles are functionality.

### Question: Should task template include example test code?

**Resolution**: Include code (Recommended). Concrete examples guide implementers.

### Question: Should we include verification tasks for framework behaviors?

**Resolution**: Yes. Explicit verification documents expected behavior and catches regressions.

### Question: Interactive vs batch milestone planning?

**Resolution**: Interactive (Recommended). Approving each milestone prevents compounding errors.

### Question: Three task types or two?

**Resolution**: Three types (Infrastructure, Functionality, Integration). Integration has distinct characteristics.

---

## Cross-Skill Notes

- **`writing-code`**: Must be loaded as parent skill
- **`writing-useful-tests`**: TDD workflow, Arrange/Act/Assert patterns
- **`writing-effective-acceptance-criteria`**: AC grain and testability checks
- **`performing-milestone-reviews`**: Provides milestone structure that work plans consume

---

## Process Summary

See the Core Pattern in SKILL.md for the synthesized process.

---

## Milestones Used for Discovery

1. **M1 (Infrastructure)**: Project scaffolding — revealed infrastructure task patterns
2. **M3 (Functionality)**: Session Manager — revealed TDD patterns, scaffold tasks
3. **M7 (Integration)**: CLI command integration — revealed integration as third type

---

## Next Steps

- [x] Create skill using `writing-skills` patterns
- [ ] Address cross-skill updates (none identified)
- [ ] Pressure test with RED-GREEN-REFACTOR on a real implementation session
