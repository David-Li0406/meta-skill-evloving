---
name: research-plan-implement
description: A structured workflow for AI-assisted development using research, planning, and systematic implementation phases. Users refer to this skill as RPI, rpi or Research Plan Implement.
agents:
  - codebase-locator
  - codebase-analyzer
  - pattern-finder
---

# Research-Plan-Implement Workflow

This skill provides a structured approach to software development through five distinct phases: Research, Plan, Validate, Implement, and Test. Each phase builds on the previous to ensure thorough understanding before making changes and verification after. This skill can be referred to as RPI, rpi, Research Plan Implement or research-plan-implement.

## Workflow Phases

### Phase 1: Research Codebase

Save findings to: `_thoughts/research/NNN_topic_name.md`

Before writing the research summary or making any changes to the filesystem, deeply explore the codebase to understand:

1. **Architecture Analysis**
   - Identify the overall project structure and organization
   - Map dependencies and module relationships
   - Understand build systems and tooling

2. **Pattern Discovery**
   - Find existing patterns for similar functionality
   - Identify coding conventions and style guides
   - Note testing patterns and coverage expectations

3. **Relevant Code Location**
   - Locate files that will need modification
   - Identify related files that may be affected
   - Find existing tests for the areas of change

**Research Execution Strategy:**
- Use parallel agent execution for faster analysis
- Document findings in a structured format
- Answer specific questions about the codebase before proceeding

**Research Questions to Answer:**
- Where does similar functionality already exist?
- What patterns should new code follow?
- What files will need to be modified?
- What tests already exist for this area?
- Are there any architectural constraints to consider?

### Phase 2: Create Implementation Plan

Save plan to: `_thoughts/plan/NNN_feature_name.md`

Based on research findings, create a detailed implementation plan:

1. **Define Scope**
   - List all files that will be created or modified
   - Identify dependencies between changes
   - Set clear boundaries for what is included/excluded

2. **Phase the Work**
   - Break implementation into logical phases
   - Order phases by dependencies
   - Define success criteria for each phase

3. **Specify Details**
   - For each change, describe the specific modifications
   - Include code patterns to follow
   - Note any risks or considerations

**Plan Structure Template:**

```markdown
## Implementation Plan: [Feature/Change Name]

### Overview
[Brief description of the change and its purpose]

### Research Summary
[Key findings from the research phase]

### Phases

#### Phase 1: [Phase Name]
**Files:**
- [ ] `path/to/file1.ts` - [Description of changes]
- [ ] `path/to/file2.ts` - [Description of changes]

**Success Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

#### Phase 2: [Phase Name]
[Continue with additional phases...]

### Testing Strategy
[How to verify the implementation]

### Rollback Plan
[How to revert if issues arise]
```

### Phase 3: Validate Plan

Save validation notes to: `_thoughts/validate/NNN_feature_name_validation.md`

Before implementation, verify the plan is complete and correct:

1. **Completeness Check**
   - All necessary files identified
   - All dependencies mapped
   - Success criteria are testable

2. **Feasibility Review**
   - Changes are technically sound
   - No conflicts with existing code
   - Follows established patterns

3. **Risk Assessment**
   - Potential issues identified
   - Mitigation strategies defined
   - Rollback path is clear

### Phase 4: Implement Plan

Save progress to: `_thoughts/implement/NNN_feature_name.md`

Execute the plan systematically:

1. **Follow the Plan**
   - Implement changes in phase order
   - Mark checkboxes as tasks complete
   - Verify success criteria at each step

2. **Track Progress**
   - Update plan document with completion status
   - Note any deviations from the plan
   - Document decisions made during implementation

3. **Validate Continuously**
   - Run tests after each phase
   - Verify integration points
   - Check against success criteria

**Implementation Rules:**
- Never skip phases or steps
- If the plan needs changes, update it before proceeding
- Document any issues encountered
- Commit after completing each phase

### Phase 5: Run Tests

Save results to: `_thoughts/test/NNN_feature_name_results.md`

After implementation, execute the testing strategy defined in the plan:

1. **Execute Test Cases**
   - Run all tests specified in the Testing Strategy
   - Execute unit tests for modified components
   - Run integration tests for affected systems
   - Perform any manual verification steps defined

2. **Verify Success Criteria**
   - Check each success criterion from the plan
   - Confirm all acceptance criteria are met
   - Validate edge cases and error handling

3. **Handle Failures**
   - If tests fail, diagnose the root cause
   - Fix issues in the implementation
   - Re-run failed tests until they pass
   - Do NOT mark work as complete until all tests pass

4. **Document Results**
   - Record test execution results
   - Note any issues discovered and how they were resolved
   - Update plan with final completion status

**Testing Rules:**
- Never skip tests defined in the plan
- All tests must pass before work is considered complete
- If new issues are discovered, add them to the plan and address them
- Run the full test suite, not just new tests

## Usage Instructions

When invoking this skill, specify your intent:

1. **To Research:** "Research the codebase to understand [specific topic or area]"
2. **To Plan:** "Create an implementation plan for [feature/change]"
3. **To Validate:** "Validate the implementation plan for [feature/change]"
4. **To Implement:** "Implement the plan for [feature/change]"
5. **To Test:** "Run the tests for [feature/change]"

## Agent Collaboration

This skill leverages specialized agents for research:

### Codebase Locator Agent
Finds relevant files and directories for a given topic or feature area. Use when you need to discover where specific functionality lives.

### Codebase Analyzer Agent
Performs deep analysis of code structure, patterns, and dependencies. Use for understanding how systems work.

### Pattern Finder Agent
Identifies coding patterns, conventions, and best practices used in the codebase. Use to ensure new code follows existing standards.

## Document Storage

All workflow documents MUST be written to the `_thoughts` directory with stage-based subdirectories:

```
_thoughts/
├── research/           # Research findings and analysis
│   ├── 001_architecture_analysis.md
│   └── 002_pattern_discovery.md
├── plan/               # Implementation plans
│   ├── 001_migrate_to_bun.md
│   └── 002_add_authentication.md
├── validate/           # Validation notes and checklists
│   └── 001_migrate_to_bun_validation.md
├── implement/          # Implementation progress tracking
│   ├── 001_migrate_to_bun.md
│   └── 002_add_authentication.md
└── test/               # Test results and reports
    └── 001_migrate_to_bun_results.md
```

### File Naming Convention

Files should follow this naming pattern:
- Format: `NNN_descriptive_name.md`
- NNN: Three-digit sequential number (001, 002, etc.)
- Use lowercase with underscores for the descriptive name
- Match filenames across stages for the same feature (e.g., `001_migrate_to_bun.md` in both `plan/` and `implement/`)

### When to Write Documents

1. **Research Phase**: Write to `_thoughts/research/` when documenting findings
2. **Plan Phase**: Write to `_thoughts/plan/` when creating implementation plans
3. **Validate Phase**: Write to `_thoughts/validate/` when documenting validation results
4. **Implement Phase**: Write to `_thoughts/implement/` to track progress and decisions
5. **Test Phase**: Write to `_thoughts/test/` for test results and reports

## Context Persistence

For long-running projects, save progress using a structured format in the appropriate `_thoughts/` subdirectory:

```markdown
## Session: [Date/Time]

### Current State
- Phase: [Research/Plan/Validate/Implement/Test]
- Progress: [Description]

### Completed
- [x] [Completed item]

### In Progress
- [ ] [Current work]

### Next Steps
- [ ] [Upcoming work]

### Notes
[Important observations or decisions]
```

## Best Practices

1. **Research First**: Never skip the research phase. Understanding prevents mistakes.
2. **Plan Thoroughly**: A detailed plan saves time during implementation.
3. **Validate Before Acting**: Catch issues before they become problems.
4. **Track Everything**: Document progress and decisions.
5. **Use Parallel Agents**: Speed up research with concurrent analysis.
6. **Commit Often**: Save progress after each logical unit of work.
7. **Test Continuously**: Verify each phase before moving on.
