# PRISM Command Reference

This document describes the command structure and common commands available across PRISM skills.

## Command Structure

All PRISM commands follow a consistent pattern:

```
{command-name} [arguments]
```

When using skills in slash command mode, prefix with `*`:
```
*help
*create-story
*develop-story
```

## Common Commands (All Skills)

### Help & Information

**`help`**
- **Purpose**: Display available commands for the current skill
- **Output**: Numbered list of commands with descriptions
- **Usage**: `*help`

**`exit`**
- **Purpose**: Exit the current skill persona
- **Output**: Farewell message and return to normal mode
- **Usage**: `*exit`

### Jira Integration

**`jira {issueKey}`**
- **Purpose**: Fetch context from a Jira ticket
- **Arguments**:
  - `issueKey`: The Jira issue identifier (e.g., "PROJ-123")
- **Output**: Issue details including description, acceptance criteria, comments
- **Usage**: `*jira PROJ-123`
- **Available in**: All skills with Jira integration

## Architect Commands

### Document Creation

**`create-architecture`**
- **Purpose**: Intelligently create architecture documentation based on project type
- **How it works**:
  - Analyzes PRD and project requirements
  - Recommends appropriate template (fullstack or backend-focused)
  - Gets user confirmation
  - Creates comprehensive architecture doc
- **Templates**:
  - `fullstack-architecture-tmpl.yaml` for full-stack projects
  - `architecture-tmpl.yaml` for backend/services projects
- **Output**: Complete architecture covering all relevant layers

### Analysis & Research

**`research {topic}`**
- **Purpose**: Conduct deep technical research
- **Arguments**: `topic` - The architecture topic to research
- **Task**: Executes `create-deep-research-prompt.md`
- **Output**: Comprehensive research findings

**`document-project`**
- **Purpose**: Document existing project architecture
- **Task**: Executes `document-project.md`
- **Output**: Complete project documentation

### Quality & Validation

**`execute-checklist`**
- **Purpose**: Run architecture quality checklist
- **Arguments**: Optional checklist name (defaults to `architect-checklist`)
- **Task**: Executes `execute-checklist.md`
- **Output**: Checklist validation results

**`shard-prd`**
- **Purpose**: Break architecture document into implementable pieces
- **Task**: Executes `shard-doc.md`
- **Output**: Multiple story files from architecture

**`doc-out`**
- **Purpose**: Output full document to destination file
- **Usage**: Used during document creation workflows

## Product Owner Commands

### Story Management

**`create-story`**
- **Purpose**: Create user story from requirements
- **Task**: Executes `brownfield-create-story.md`
- **Output**: Complete story YAML file

**`validate-story-draft {story}`**
- **Purpose**: Validate story completeness and quality
- **Arguments**: `story` - Path to story file
- **Task**: Executes `validate-next-story.md`
- **Output**: Validation results and recommendations

**`correct-course`**
- **Purpose**: Handle requirement changes and re-estimation
- **Task**: Executes `correct-course.md`
- **Output**: Updated stories and estimates

### Document Processing

**`shard-doc {document} {destination}`**
- **Purpose**: Break large document into stories
- **Arguments**:
  - `document`: Path to source document (PRD, architecture, etc.)
  - `destination`: Output directory for story files
- **Task**: Executes `shard-doc.md`
- **Output**: Multiple story files with dependencies

**`doc-out`**
- **Purpose**: Output full document to destination file
- **Usage**: Used during document creation workflows

### Quality Assurance

**`execute-checklist-po`**
- **Purpose**: Run PO master checklist
- **Task**: Executes `execute-checklist.md` with `po-master-checklist`
- **Output**: Checklist validation results

**`yolo`**
- **Purpose**: Toggle Yolo Mode (skip confirmations)
- **Usage**: `*yolo`
- **Note**: ON = skip section confirmations, OFF = confirm each section

## Developer Commands

### Story Implementation

**`develop-story`**
- **Purpose**: Execute complete story implementation workflow
- **Workflow**:
  1. Set PSP tracking started timestamp
  2. Read task → Implement → Write tests → Validate
  3. Mark task complete, update File List
  4. Repeat until all tasks complete
  5. Run full regression
  6. Update PSP tracking, set status to "Ready for Review"
- **Critical Rules**:
  - Only update Dev Agent Record sections
  - Follow PRISM principles (Predictability, Resilience, Intentionality, Sustainability, Maintainability)
  - Write tests before implementation (TDD)
  - Run validations before marking tasks complete

**`explain`**
- **Purpose**: Educational breakdown of implementation
- **Usage**: `*explain`
- **Output**: Detailed explanation of recent work, teaching junior engineer perspective

### Quality & Testing

**`review-qa`**
- **Purpose**: Apply QA fixes from review feedback
- **Task**: Executes `apply-qa-fixes.md`
- **Usage**: After receiving QA review results

**`run-tests`**
- **Purpose**: Execute linting and test suite
- **Usage**: `*run-tests`
- **Output**: Test results and coverage

### Integration

**`strangler`**
- **Purpose**: Execute strangler pattern migration workflow
- **Usage**: For legacy code modernization
- **Pattern**: Gradual replacement of legacy systems

## QA/Test Architect Commands

### Risk & Design (Before Development)

**`risk-profile {story}` (short: `*risk`)**
- **Purpose**: Assess regression and integration risks
- **Arguments**: `story` - Story file path or ID
- **Task**: Executes `risk-profile.md`
- **Output**: `docs/qa/assessments/{epic}.{story}-risk-{YYYYMMDD}.md`
- **Use When**: IMMEDIATELY after story creation, especially for brownfield

**`test-design {story}` (short: `*design`)**
- **Purpose**: Plan comprehensive test strategy
- **Arguments**: `story` - Story file path or ID
- **Task**: Executes `test-design.md`
- **Output**: `docs/qa/assessments/{epic}.{story}-test-design-{YYYYMMDD}.md`
- **Use When**: After risk assessment, before development

### Review (After Development)

**`review {story}`**
- **Purpose**: Comprehensive quality review with active refactoring
- **Arguments**: `story` - Story file path or ID
- **Task**: Executes `review-story.md`
- **Outputs**:
  - QA Results section in story file
  - Gate file: `docs/qa/gates/{epic}.{story}-{slug}.yml`
- **Gate Statuses**: PASS / CONCERNS / FAIL / WAIVED
- **Use When**: Development complete, before committing

**`gate {story}`**
- **Purpose**: Update quality gate decision after fixes
- **Arguments**: `story` - Story file path or ID
- **Task**: Executes `qa-gate.md`
- **Output**: Updated gate YAML file
- **Use When**: After addressing review issues

## Scrum Master Commands

**`create-epic`**
- **Purpose**: Create epic from brownfield requirements
- **Task**: Executes `brownfield-create-epic.md`
- **Output**: Epic document with stories

## Command Execution Order

### Typical Story Lifecycle

```
1. PO: *create-story
2. PO: *validate-story-draft {story}
3. QA: *risk {story}              # Assess risks (optional)
4. QA: *design {story}            # Plan tests (optional)
5. Dev: *develop-story            # Implement
6. QA: *review {story}            # Full review (optional)
7. Dev: *review-qa                # Apply fixes (if needed)
8. QA: *gate {story}              # Update gate (optional)
```

### Brownfield Story Lifecycle (High Risk)

```
1. PO: *create-story
2. QA: *risk {story}              # CRITICAL: Before dev
3. QA: *design {story}            # Plan regression tests
4. PO: *validate-story-draft {story}
5. Dev: *develop-story
6. QA: *review {story}            # Deep integration analysis
7. Dev: *review-qa
8. QA: *gate {story}              # May WAIVE legacy issues
```

## Command Flags & Options

### Yolo Mode (PO)
- **Toggle**: `*yolo`
- **Effect**: Skip document section confirmations
- **Use**: Batch story creation, time-critical work

### Checklist Variants
- `execute-checklist` - Default checklist for skill
- `execute-checklist {custom-checklist}` - Specific checklist

## Best Practices

**Command Usage:**
- ✅ Use short forms in brownfield workflows (`*risk`, `*design`)
- ✅ Always run `*help` when entering a new skill
- ✅ Use `*risk` before starting ANY brownfield work
- ✅ Run `*design` after risk assessment
- ✅ Execute `*review` when development is complete

**Anti-Patterns:**
- ❌ Skipping `*risk` on legacy code changes
- ❌ Running `*review` before all tasks are complete
- ❌ Using `*yolo` mode for critical stories

## Integration Commands

### Jira Integration Pattern

```
1. *jira PROJ-123              # Fetch issue
2. Use fetched context for story/architecture creation
3. Reference Jira key in created artifacts
```

## Command Help

For skill-specific commands, use the `*help` command within each skill:
- Architect: `*help` → Lists architecture commands
- PO: `*help` → Lists story/backlog commands
- Dev: `*help` → Lists development commands
- QA: `*help` → Lists testing commands
- SM: `*help` → Lists scrum master commands

---

**Last Updated**: 2025-10-22
