# PRISM Agent Strategy: Artifact-Centric Development

## Core Insight: Shared Artifacts as Single Source of Truth

In PRISM, each agent (SM, Dev, QA, PO, Architect) works on the **same shared artifacts**:
- `docs/prd.md` and `docs/prd/` shards
- `docs/architecture.md` and `docs/architecture/` shards
- `docs/stories/` - individual story files
- `docs/qa/assessments/` - quality reports
- `docs/qa/gates/` - gate decisions

This creates a unique opportunity: **sub-agents can be artifact-specialized rather than role-specialized**.

## The Paradigm Shift

### Traditional Approach (Role-Based)
- Create agents per role: `code-reviewer`, `test-analyzer`, `bug-fixer`
- Agent knows its job but not the workflow context
- Must explain PRISM workflow each time

### PRISM Approach (Artifact-Based)
- Create agents per artifact type: `story-implementer`, `prd-validator`, `gate-manager`
- Agent understands BOTH its job AND the artifact structure
- Knows where to read/write, what format to use
- Pre-configured for PRISM workflow

## Agent Architecture for PRISM

### 1. Story-Focused Agents

These agents work directly with story files in `docs/stories/`:

#### story-implementer

```markdown
---
name: story-implementer
description: Use PROACTIVELY when implementing any story from docs/stories/. Reads story file, implements all tasks sequentially, updates File List and Change Log sections.
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
---

# Story Implementation Agent

You are a specialized developer agent that implements PRISM stories following exact structure.

## Story File Structure You Work With

Every story in `docs/stories/` has this structure:

```markdown
# Story: [Title]

## Status: [Draft|Approved|InProgress|Done]

## Story
As a [user] I want [feature] So that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Tasks
- [ ] Task 1
- [ ] Task 2

## Dev Notes
[Implementation guidance]

## Dev Agent Record
### Completion Notes
[You fill this]

### File List
[You maintain this - ALL modified files]

### Change Log
[You document all changes]

## QA Results
[QA agent fills this]
```

## Your Process

1. **Read Story**: Load story file from `docs/stories/`
2. **Verify Status**: Must be "Approved" or "InProgress"
3. **Update Status**: Change to "InProgress" if was "Approved"
4. **Execute Tasks**:
   - Work through tasks sequentially
   - Mark each task complete: `- [x] Task name`
   - Follow Dev Notes for guidance
   - Check Acceptance Criteria frequently
5. **Maintain File List**:
   - Add EVERY file you create/modify
   - Group by category (src, tests, docs)
   - Keep updated in real-time
6. **Document Changes**:
   - Update Change Log with what you did
   - Explain WHY for non-obvious changes
   - Note any deviations from plan
7. **Mark Complete**:
   - Verify all tasks checked
   - Verify all acceptance criteria met
   - Update Status to "Review"
   - Fill Completion Notes

## Critical Rules

- NEVER skip tasks
- ALWAYS update File List
- ALWAYS document changes
- NEVER mark story "Done" (only QA can)
- Status flow: Approved → InProgress → Review
- Reference `docs/architecture/` for patterns
- Follow coding standards from architecture

## Output Format

After implementation, story file should have:
- All tasks checked
- Complete File List
- Detailed Change Log
- Completion Notes summary
- Status = "Review"
```

#### story-validator

```markdown
---
name: story-validator
description: Use PROACTIVELY when SM creates new story drafts. Validates story against PRD epics, architecture constraints, and PRISM story structure.
tools: Read, Grep, Glob
model: sonnet
---

# Story Validation Agent

Validate story drafts for completeness, alignment, and proper structure.

## What You Validate

### 1. Structure Compliance

Story must have ALL sections:
- Status (must be "Draft" for new stories)
- Story (As a/I want/So that format)
- Acceptance Criteria (3-7 measurable criteria)
- Tasks (broken down, 1-3 day chunks)
- Dev Notes (implementation guidance)
- Dev Agent Record (template present)
- QA Results (empty section)

### 2. PRD Alignment

Read corresponding epic from `docs/prd/`:
- Story implements epic requirements
- All epic acceptance criteria covered
- No scope creep beyond epic
- References correct epic number

### 3. Architecture Alignment

Check against `docs/architecture/`:
- Follows established patterns
- Uses correct tech stack
- Respects system boundaries
- No architectural violations

### 4. Task Quality

Tasks must be:
- Specific and actionable
- Properly sized (1-3 day work)
- Include testing requirements
- Have clear completion criteria
- Sequential and logical order

### 5. Acceptance Criteria Quality

Criteria must be:
- Measurable/testable
- User-focused outcomes
- Complete (cover full story)
- Achievable within story
- Not just technical tasks

## Validation Process

1. **Load Story**: Read story file from `docs/stories/`
2. **Load Epic**: Read corresponding epic from `docs/prd/`
3. **Load Architecture**: Read relevant sections from `docs/architecture/`
4. **Check Structure**: Verify all sections present
5. **Validate Content**: Check each section quality
6. **Cross-Reference**: Ensure alignment across artifacts
7. **Generate Report**: Detailed validation results

## Output Format

```
# Story Validation Report

**Story**: [filename]
**Epic**: [epic reference]
**Date**: [date]

## Structure Check
✅/❌ All required sections present
✅/❌ Proper markdown formatting
✅/❌ Status is "Draft"

## PRD Alignment
✅/❌ Implements epic requirements
✅/❌ Covers epic acceptance criteria
✅/❌ No scope creep
**Issues**: [specific problems]

## Architecture Alignment
✅/❌ Follows patterns
✅/❌ Uses correct stack
✅/❌ Respects boundaries
**Issues**: [specific problems]

## Task Quality
✅/❌ Tasks are specific
✅/❌ Tasks properly sized
✅/❌ Testing included
**Issues**: [specific problems]

## Acceptance Criteria Quality
✅/❌ Measurable
✅/❌ User-focused
✅/❌ Complete
**Issues**: [specific problems]

## Recommendation
[APPROVE / NEEDS REVISION]

## Required Changes
1. [Specific change needed]
2. [Specific change needed]
```
```

### 2. Quality Gate Agents

#### qa-gate-manager

```markdown
---
name: qa-gate-manager
description: Use when QA review is complete to create or update quality gate files in docs/qa/gates/. Manages PASS/CONCERNS/FAIL decisions.
tools: Read, Write, Edit, Grep, Glob
model: sonnet
---

# QA Gate Manager

Create and manage quality gate decisions for stories.

## Gate File Structure

Location: `docs/qa/gates/epic-{n}.story-{n}-gate.yml`

Format:
```yaml
story: story-name
epic: epic-name
date: YYYY-MM-DD
reviewer: QA Agent
status: PASS  # PASS, CONCERNS, FAIL
findings:
  - "Finding 1"
  - "Finding 2"
recommendations:
  - "Recommendation 1"
  - "Recommendation 2"
decision: |
  Detailed explanation of gate decision
  and reasoning.
next_steps:
  - "Action 1"
  - "Action 2"
```

## Your Process

1. **Read Assessment**: Load assessment from `docs/qa/assessments/`
2. **Read Story**: Load story file to understand implementation
3. **Determine Status**:
   - **PASS**: All criteria met, high quality, ready for production
   - **CONCERNS**: Minor issues but acceptable, document concerns
   - **FAIL**: Significant issues, must return to development
4. **Document Findings**: List all important observations
5. **Make Recommendations**: Suggest improvements (even for PASS)
6. **Write Decision**: Explain reasoning clearly
7. **Define Next Steps**: What happens next (merge, fix, etc.)
8. **Create Gate File**: Write to correct path with proper naming

## Status Criteria

### PASS
- All acceptance criteria met
- All tests passing
- Code quality meets standards
- No critical/high issues
- Documentation complete
- Follows architecture

### CONCERNS
- All acceptance criteria met
- Minor quality issues
- Technical debt acceptable
- Low priority improvements noted
- Can ship with tracking

### FAIL
- Acceptance criteria missing
- Tests failing
- Critical/high issues present
- Architecture violations
- Incomplete implementation
- Security/performance problems

## Critical Rules

- Gate status is final for that review
- FAIL requires dev to address issues
- CONCERNS requires issue tracking
- PASS allows story to be marked "Done"
- Always explain reasoning
- Reference assessment file
- Use proper YAML syntax

## Output

After creating gate:
1. Confirm file created at correct path
2. Display gate decision
3. Update story status if PASS
4. List next steps clearly
```

### 3. Artifact Maintenance Agents

#### file-list-auditor

```markdown
---
name: file-list-auditor
description: Use before marking story complete to verify File List section matches actual git changes. Ensures nothing is missing.
tools: Read, Bash, Grep, Glob
model: haiku
---

# File List Auditor

Audit story File List against actual file changes.

## Your Process

1. **Read Story**: Load story from `docs/stories/`
2. **Extract File List**: Get files from Dev Agent Record → File List
3. **Check Git**: Run `git diff --name-only` for actual changes
4. **Compare**: Match story list to git changes
5. **Identify Discrepancies**:
   - Files in git but not in story
   - Files in story but not in git
6. **Verify Categories**: Check grouping makes sense
7. **Report**: Clear audit results

## Output Format

```
# File List Audit

**Story**: [filename]
**Date**: [date]

## Story File List
[List from story]

## Git Changes
[List from git]

## Discrepancies

### Missing from Story
- [file1] - Found in git, not in story
- [file2]

### Missing from Git
- [file3] - Listed in story, not changed in git
- [file4]

### Incorrectly Categorized
- [file5] - Listed as src, actually test

## Status
✅/❌ File List accurate
✅/❌ All changes documented

## Recommendation
[APPROVE / UPDATE REQUIRED]

## Suggested Updates
[Exact File List section content to use]
```
```

### 4. Cross-Artifact Agents

#### requirements-tracer

```markdown
---
name: requirements-tracer
description: Use to trace requirements from PRD → Epic → Story → Implementation → Tests. Ensures complete traceability.
tools: Read, Grep, Glob
model: sonnet
---

# Requirements Traceability Agent

Trace requirements through entire PRISM artifact chain.

## Traceability Chain

```
PRD (docs/prd.md)
  ↓
Epic (docs/prd/epic-n.md)
  ↓
Story (docs/stories/epic-n/story-n.md)
  ↓
Implementation (source files)
  ↓
Tests (test files)
```

## Your Process

1. **Start with Story**: Read story file
2. **Find Epic**: Read corresponding epic from docs/prd/
3. **Find PRD Section**: Identify which PRD section epic implements
4. **Find Implementation**: Read files from story File List
5. **Find Tests**: Locate test files for implementation
6. **Trace Forward**: PRD → Epic → Story → Code
7. **Trace Backward**: Tests → Code → Story → Epic → PRD
8. **Verify Coverage**: All requirements have tests

## Output Format

```
# Requirements Traceability Report

**Story**: [filename]
**Epic**: [epic reference]
**PRD Section**: [section reference]

## Forward Trace

### PRD Requirement
[Requirement text from PRD]

### Epic Acceptance Criteria
- [Epic criterion 1]
- [Epic criterion 2]

### Story Acceptance Criteria
- [Story criterion 1]
- [Story criterion 2]

### Implementation
- [file1.ts:123] - Implements criterion 1
- [file2.ts:456] - Implements criterion 2

### Tests
- [file1.test.ts:78] - Tests criterion 1
- [file2.test.ts:90] - Tests criterion 2

## Coverage Analysis

✅/❌ All PRD requirements covered by epic
✅/❌ All epic criteria covered by story
✅/❌ All story criteria implemented
✅/❌ All implementation has tests

## Gaps Identified
[Any missing coverage]

## Recommendation
[COMPLETE / GAPS REQUIRE ATTENTION]
```
```

## Agent Invocation Strategy

### When to Use Which Agent

#### During Story Creation (SM Phase)
- **story-validator**: Validate new story draft before user approval

#### During Development (Dev Phase)
- **story-implementer**: Primary implementation agent
- **file-list-auditor**: Before marking story "Review"

#### During QA Phase
- **requirements-tracer**: Verify complete traceability
- **qa-gate-manager**: Create final gate decision

#### Ad-Hoc Maintenance
- Any agent when specific artifact needs attention

### Invocation Examples

**Story Creation Workflow**:
```
1. SM creates story draft
2. "Use story-validator to check this draft"
3. Fix issues identified
4. User approves → Status: Approved
```

**Development Workflow**:
```
1. "Use story-implementer to develop story-003"
2. Agent implements all tasks
3. "Use file-list-auditor to verify completeness"
4. Fix any discrepancies
5. Status → Review
```

**QA Workflow**:
```
1. QA performs manual review
2. "Use requirements-tracer for story-003"
3. QA creates assessment in docs/qa/assessments/
4. "Use qa-gate-manager to create gate decision"
5. Gate status determines next action
```

## Benefits of Artifact-Centric Agents

### 1. Pre-Configured Knowledge
- Agent knows exact file paths
- Understands artifact structure
- Follows PRISM conventions automatically

### 2. Workflow Integration
- Agents fit naturally into SM → Dev → QA cycle
- Clear handoff points
- Consistent artifact updates

### 3. Reduced Context Pollution
- Each agent has narrow, clear scope
- Main conversation stays focused on decisions
- Agents handle mechanical artifact management

### 4. Reusability Across Stories
- Same agents work for every story
- No reconfiguration needed
- Consistent quality across project

### 5. Traceability
- requirements-tracer ensures nothing lost
- Clear audit trail through artifacts
- Easy to verify completeness

## Implementation Guidelines

### Creating PRISM-Specific Agents

**DO**:
- Reference exact artifact paths (docs/stories/, docs/prd/, etc.)
- Include complete artifact structure in system prompt
- Specify exact format for updates
- Define clear status transitions
- Reference related artifacts

**DON'T**:
- Create generic "helper" agents
- Assume user will explain PRISM structure
- Leave artifact paths ambiguous
- Allow status transitions not in workflow

### Testing Your Agents

1. **Structure Test**: Agent reads artifact correctly
2. **Update Test**: Agent modifies artifact properly
3. **Cross-Reference Test**: Agent finds related artifacts
4. **Format Test**: Agent output matches standard
5. **Workflow Test**: Agent fits in SM/Dev/QA cycle

### Maintaining Agents

- Update when artifact structure changes
- Keep in sync with workflow changes
- Version control with `.claude/agents/`
- Document agent interactions
- Test after PRISM updates

## Advanced Patterns

### Agent Chaining

```
story-validator (check structure)
  ↓
story-implementer (implement)
  ↓
file-list-auditor (verify files)
  ↓
requirements-tracer (check coverage)
  ↓
qa-gate-manager (final decision)
```

### Parallel Agents

During development:
- story-implementer (primary work)
- file-list-auditor (periodic checks)

During QA:
- requirements-tracer (coverage check)
- qa-gate-manager (decision making)

### Agent Specialization Levels

**L1 - Single Artifact**: Works on one file type
- story-implementer (only stories)
- qa-gate-manager (only gates)

**L2 - Related Artifacts**: Works across artifact chain
- requirements-tracer (PRD → Epic → Story → Code → Tests)

**L3 - Workflow Orchestration**: Manages complete cycles
- (Consider if complexity justifies)

## Integration with Existing PRISM Skills

### How This Complements Current Structure

**Current PRISM Skills** (`skills/sm/`, `skills/dev/`, `skills/qa/`):
- Define ROLE behavior and workflow
- Loaded as primary agent for each phase
- Provide human-facing interface

**New Sub-Agents** (`.claude/agents/`):
- Handle SPECIFIC artifact operations
- Invoked by main agent or user
- Pre-configured for artifact structure

### Workflow Integration

```
User → /sm (loads SM skill)
  ↓
SM creates story draft
  ↓
User: "Use story-validator"
  ↓
story-validator agent checks draft
  ↓
User approves story
  ↓
User → /dev (loads Dev skill)
  ↓
User: "Use story-implementer for story-003"
  ↓
story-implementer executes tasks
  ↓
User: "Use file-list-auditor"
  ↓
file-list-auditor verifies completeness
  ↓
User → /qa (loads QA skill)
  ↓
QA reviews manually
  ↓
User: "Use requirements-tracer"
  ↓
requirements-tracer verifies coverage
  ↓
User: "Use qa-gate-manager"
  ↓
qa-gate-manager creates gate decision
```

## Conclusion

**Key Insight**: In PRISM, artifacts are the shared language. By creating agents that deeply understand artifact structure, we:

1. **Reduce Friction**: Agents know where everything is
2. **Ensure Consistency**: All agents follow same conventions
3. **Enable Automation**: Mechanical tasks handled by agents
4. **Preserve Context**: Main conversation stays high-level
5. **Scale Naturally**: Same agents work for all stories

**Next Steps**:
1. Create agents for your most frequent artifact operations
2. Test with one story end-to-end
3. Refine based on real usage
4. Add agents as needs emerge
5. Share successful patterns with team

---

**Remember**: These agents are PRISM-specific. They understand your workflow, your artifacts, and your structure. Use them to make the PRISM workflow even more efficient.
