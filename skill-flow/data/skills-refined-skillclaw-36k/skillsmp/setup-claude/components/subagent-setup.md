# Subagent Setup Component

This component guides the configuration of subagents for specialized workflows.

## Core Concept

Subagents are specialized Claude instances with **scoped tools** for focused execution. By limiting what tools a subagent can use, you get more reliable, focused results.

## Why Use Subagents?

| Problem | Solution |
|---------|----------|
| Claude tries to edit while planning | `planner` subagent has no Edit tool |
| Reviews get distracted by fixes | `code-reviewer` has no Edit tool |
| Tests written after implementation | `tdd-guide` enforces test-first |
| Refactoring creates new features | `refactor-cleaner` focuses on removal |

## Available Subagent Templates

| Subagent | Purpose | Tools |
|----------|---------|-------|
| `planner` | Feature planning | Read, Glob, Grep |
| `code-reviewer` | Quality review | Read, Glob, Grep |
| `tdd-guide` | Test-driven dev | Read, Write, Edit, Bash |
| `refactor-cleaner` | Dead code removal | Read, Edit, Grep |

## Setup Flow

### Step 1: Explain Subagents

Present to user:
```
Subagents are specialized Claude instances with limited tools.
They help with focused tasks by preventing scope creep.

Examples:
- planner: Can research but can't edit (prevents premature coding)
- code-reviewer: Can read but can't modify (pure review)
- tdd-guide: Full tools but enforces test-first workflow
- refactor-cleaner: Can edit but can't create (removal focus)
```

### Step 2: Interview User

```
AskUserQuestion: "Set up subagents for common workflows?"
(Multi-select)

├── planner - Feature implementation planning
│   Tools: Read, Glob, Grep (research only)
│   Use when: Planning features before implementation
│
├── code-reviewer - Quality/security review
│   Tools: Read, Glob, Grep (no editing)
│   Use when: Reviewing PRs or code quality
│
├── tdd-guide - Test-driven development
│   Tools: Read, Write, Edit, Bash (full dev)
│   Use when: Implementing with test-first approach
│
├── refactor-cleaner - Dead code removal
│   Tools: Read, Edit, Grep (modify only)
│   Use when: Cleaning up unused code
│
└── None - I'll add subagents later
```

### Step 3: Copy Templates

For each selected subagent:

```bash
# Create agents directory if needed
mkdir -p .claude/agents

# Copy selected templates
cp templates/subagents/planner.md .claude/agents/
cp templates/subagents/code-reviewer.md .claude/agents/
cp templates/subagents/tdd-guide.md .claude/agents/
cp templates/subagents/refactor-cleaner.md .claude/agents/
```

### Step 4: Customize (Optional)

Ask if customization needed:

```
AskUserQuestion: "Customize subagent tools?"

For planner subagent:
├── Keep defaults (Read, Glob, Grep)
├── Add WebSearch (for external research)
└── Custom selection
```

### Step 5: Document Usage

Add to CLAUDE.md:

```markdown
## Subagents

| Subagent | Invocation | Purpose |
|----------|------------|---------|
| planner | `Task with subagent_type=planner` | Feature planning |
| code-reviewer | `Task with subagent_type=code-reviewer` | Code review |
| tdd-guide | `Task with subagent_type=tdd-guide` | Test-first development |
| refactor-cleaner | `Task with subagent_type=refactor-cleaner` | Dead code removal |

### When to Use Each

- **planner**: Before implementing any feature, use to create implementation plan
- **code-reviewer**: After completing feature, use for quality review
- **tdd-guide**: When implementing feature with tests required
- **refactor-cleaner**: When cleaning up code or removing unused features
```

## Subagent Definition Format

Each subagent is a markdown file in `.claude/agents/`:

```markdown
---
name: subagent-name
description: What this subagent does
allowed-tools:
  - Tool1
  - Tool2
---

# Subagent Name

Instructions for the subagent...

## Workflow

Steps to follow...

## Output Format

What to produce...
```

## Tool Scoping Reference

### Research-Only (No Modifications)

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - WebSearch
```

Use for: Planning, reviewing, researching

### Full Development

```yaml
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

Use for: Implementation with specific workflow

### Modification-Only (No Creation)

```yaml
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
```

Use for: Refactoring, cleanup

### Read + Execute

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
```

Use for: Analysis, testing, verification

## Integration with Workflows

### Feature Development Flow

```
1. /prd - Create requirements
2. Task(planner) - Create implementation plan
3. Implement feature
4. Task(code-reviewer) - Review implementation
5. Fix issues
```

### Refactoring Flow

```
1. Task(code-reviewer) - Identify issues
2. Task(refactor-cleaner) - Remove dead code
3. Task(code-reviewer) - Verify cleanup
```

### TDD Flow

```
1. Task(tdd-guide) - Implement with tests
   - Writes failing test first
   - Implements to pass
   - Refactors
2. Task(code-reviewer) - Review result
```

## Customization Examples

### Adding WebSearch to Planner

```markdown
---
name: planner
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch  # Added for external research
---
```

### Adding Bash to Reviewer (for running tests)

```markdown
---
name: code-reviewer
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash  # Added for running tests
---
```

## Troubleshooting

### Subagent Tries Unauthorized Tool

The tool will be blocked. Subagent should:
1. Acknowledge limitation
2. Provide recommendation instead
3. Return to parent for execution

### Subagent Gets Stuck

May need more tools. Consider:
1. Adding specific tool temporarily
2. Creating new specialized subagent
3. Handling task in main context

### When NOT to Use Subagents

- Simple, straightforward tasks
- Tasks requiring many different tools
- Interactive tasks needing user input

## Output Format

Present subagent status:

```
═══════════════════════════════════════════════════════════════════════════
Subagent Configuration
═══════════════════════════════════════════════════════════════════════════

Configured Subagents:
├── planner
│   Tools: Read, Glob, Grep
│   Use: Feature planning before implementation
│
├── code-reviewer
│   Tools: Read, Glob, Grep
│   Use: Quality/security review
│
└── tdd-guide
    Tools: Read, Write, Edit, Bash
    Use: Test-driven development

Location: .claude/agents/

Usage Example:
  Task with subagent_type="planner"
  Task with subagent_type="code-reviewer"
```
