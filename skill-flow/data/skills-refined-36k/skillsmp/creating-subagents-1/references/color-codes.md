---
title: Subagent Color Codes
description: Visual color coding system for categorizing subagents by purpose with 9 standard colors and usage patterns
keywords: color codes, subagent colors, visual identification, categorization, purple, blue, green, yellow, orange, red, cyan, magenta, white
skill: creating-subagents
---

# Subagent Color Codes

Visual color coding system for subagents to enable quick identification of agent purpose and category.

## Color System

### Purple (`purple`)
**Purpose**: Review, Audit, and Quality Assurance

**When to use**:
- Code review agents
- Security auditors
- Quality assurance validators
- Compliance checkers
- Performance auditors
- Accessibility reviewers

**Examples**:
- `security-auditor` - Audits code for security vulnerabilities
- `code-reviewer` - Reviews code quality and best practices
- `pr-reviewer` - Analyzes pull requests for issues
- `accessibility-auditor` - Checks accessibility compliance

**Rationale**: Purple represents scrutiny, wisdom, and careful examination.

---

### Blue (`blue`)
**Purpose**: Implementation and Development

**When to use**:
- Feature implementation agents
- API development agents
- UI/Component builders
- Database developers
- Integration builders

**Examples**:
- `api-developer` - Builds RESTful APIs
- `feature-builder` - Implements new features
- `component-creator` - Creates UI components
- `database-developer` - Implements database schemas

**Rationale**: Blue represents construction, stability, and systematic development.

---

### Green (`green`)
**Purpose**: Testing and Validation

**When to use**:
- Test runners
- Integration testers
- E2E test agents
- Validation checkers
- Test data generators

**Examples**:
- `test-runner` - Executes and fixes tests
- `integration-tester` - Tests component integration
- `e2e-tester` - Runs end-to-end test suites
- `test-generator` - Creates test cases

**Rationale**: Green represents success, validation, and "passing tests."

---

### Yellow (`yellow`)
**Purpose**: Documentation and Knowledge

**When to use**:
- Documentation writers
- Documentation finders
- API documentation generators
- Tutorial creators
- Knowledge base maintainers

**Examples**:
- `doc-finder` - Locates relevant documentation
- `doc-writer` - Creates and updates documentation
- `api-doc-generator` - Generates API documentation
- `tutorial-creator` - Creates learning materials

**Rationale**: Yellow represents illumination, clarity, and knowledge sharing.

---

### Orange (`orange`)
**Purpose**: Maintenance and Refactoring

**When to use**:
- Code formatters
- Refactoring agents
- Dependency updaters
- Migration handlers
- Cleanup agents

**Examples**:
- `code-formatter` - Formats code automatically
- `refactoring-agent` - Refactors code for improvement
- `dependency-updater` - Updates project dependencies
- `database-migrator` - Handles database migrations

**Rationale**: Orange represents transformation, optimization, and improvement.

---

### Red (`red`)
**Purpose**: Debugging and Troubleshooting

**When to use**:
- Debuggers
- Error analyzers
- Log investigators
- Crash reporters
- Performance profilers (when focused on finding issues)

**Examples**:
- `debugger` - Debugs runtime issues
- `error-analyzer` - Analyzes error logs and stack traces
- `crash-investigator` - Investigates application crashes
- `memory-leak-detector` - Finds memory leaks

**Rationale**: Red represents urgency, problems requiring attention, and critical issues.

---

### Cyan (`cyan`)
**Purpose**: Research and Analysis

**When to use**:
- Codebase explorers
- Dependency analyzers
- Architecture analysts
- Code archaeologists
- Pattern detectors

**Examples**:
- `codebase-explorer` - Explores and maps codebases
- `dependency-analyzer` - Analyzes dependency graphs
- `architecture-analyst` - Analyzes system architecture
- `pattern-detector` - Identifies code patterns

**Rationale**: Cyan represents exploration, discovery, and analytical thinking.

---

### Magenta (`magenta`)
**Purpose**: Deployment and Operations

**When to use**:
- Deployment agents
- Build managers
- CI/CD orchestrators
- Infrastructure managers
- Release coordinators

**Examples**:
- `deployer` - Handles deployment processes
- `build-manager` - Manages build pipelines
- `release-coordinator` - Coordinates releases
- `infrastructure-provisioner` - Provisions infrastructure

**Rationale**: Magenta represents operations, deployment, and shipping to production.

---

### White (`white`)
**Purpose**: General Purpose and Orchestration

**When to use**:
- General-purpose agents
- Task orchestrators
- Multi-domain agents
- Workflow coordinators
- Meta-agents that delegate to others

**Examples**:
- `task-coordinator` - Coordinates complex multi-step tasks
- `workflow-manager` - Manages multi-agent workflows
- `general-assistant` - Handles diverse tasks

**Rationale**: White represents neutrality, generality, and flexibility.

---

## Usage in Agent Definitions

Add the `color` field to your subagent frontmatter:

```markdown
---
name: security-auditor
description: Security audit specialist. Use proactively after implementing authentication.
tools: Read, Grep, Glob
model: sonnet
color: purple
---
```

## Best Practices

1. **Choose based on primary purpose**: If an agent does multiple things, pick the color that best represents its main function

2. **Be consistent**: Use the same color for similar agent types across your project

3. **Don't overthink**: If unsure between two colors, pick the one that feels most prominent for the agent's role

4. **Custom colors**: If none of these fit, you can use custom colors, but document your reasoning

## Color Quick Reference

| Color   | Category              | Keywords                                    |
|---------|-----------------------|---------------------------------------------|
| purple  | Review/Audit          | review, audit, check, validate, inspect     |
| blue    | Implementation        | build, create, implement, develop, code     |
| green   | Testing               | test, verify, validate, assert, check       |
| yellow  | Documentation         | document, explain, write, generate docs     |
| orange  | Maintenance           | format, refactor, migrate, update, cleanup  |
| red     | Debugging             | debug, fix, troubleshoot, analyze errors    |
| cyan    | Research              | explore, analyze, research, investigate     |
| magenta | Deployment            | deploy, build, release, ship, provision     |
| white   | General               | orchestrate, coordinate, general, multi     |

## Examples by Category

See `subagent-examples.md` for complete examples with color coding applied.
