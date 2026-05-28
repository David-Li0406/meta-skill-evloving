# Agent Basics for Commands

Quick reference for how commands interact with agents. For comprehensive agent patterns, see the `creating-agentic-subagents` skill.

## Built-in Agents

OpenCode includes these built-in agents:

| Agent     | Mode     | Description                                        |
| --------- | -------- | -------------------------------------------------- |
| `build`   | primary  | Default agent with all tools enabled               |
| `plan`    | primary  | Restricted agent for planning/analysis (no writes) |
| `general` | subagent | General-purpose for research and multi-step tasks  |
| `explore` | subagent | Fast codebase exploration                          |

## How Commands Use Agents

### Default Behavior

When a command doesn't specify an agent, it uses the current agent (usually `build`).

### Specifying an Agent

```markdown
---
description: Run quality checks
agent: build
---
```

### Running as Subtask

When `subtask: true`, the command runs in an isolated session:

```markdown
---
description: Comprehensive code review
agent: code-reviewer
subtask: true
---
```

**Subtask behavior:**

- Creates isolated session (separate context)
- Uses specified agent's configuration
- Forces subagent mode even if agent's `mode: primary`
- Navigate sessions with `Leader+Left/Right`
- Doesn't pollute main conversation context

## Agent Configuration Quick Reference

| Field         | Required | Values                       | Notes                              |
| ------------- | -------- | ---------------------------- | ---------------------------------- |
| `description` | Yes      | String                       | Include "when to use" guidance     |
| `mode`        | No       | `primary`, `subagent`, `all` | Defaults to `all`                  |
| `temperature` | No       | 0.0-1.0                      | Lower = focused, higher = creative |
| `maxSteps`    | No       | Integer                      | Limit agentic iterations           |
| `hidden`      | No       | Boolean                      | Hide from @autocomplete            |
| `tools`       | No       | Object                       | Enable/disable specific tools      |
| `permission`  | No       | Object                       | Fine-grained permissions           |
| `model`       | No       | String                       | Only if user explicitly requests   |

## Common Agent Patterns for Commands

### Read-Only Code Reviewer

For commands that analyze without modifying:

```markdown
---
description: Reviews code for quality and security issues
mode: subagent
temperature: 0.1
tools:
  write: false
  edit: false
permission:
  edit: deny
  bash:
    '*': deny
    'git diff*': allow
    'git log*': allow
    'git show*': allow
---

You are a code reviewer. Analyze code for:

- Quality and best practices
- Security vulnerabilities
- Performance concerns
- Test coverage gaps

Provide feedback without making changes.
```

### Test Fixer (Full Access)

For commands that fix issues:

```markdown
---
description: Runs tests and fixes failures iteratively
mode: subagent
temperature: 0.2
---

You are a test fixer. Your goal:

1. Run the test suite
2. Identify failures
3. Fix each failure
4. Re-run until all pass
5. Report summary of fixes made
```

### Quality Auditor

For multi-step quality workflows:

```markdown
---
description: Runs all quality checks and fixes issues
mode: subagent
---

You are a quality auditor. Execute quality checks in order:

1. Rector (automated refactoring)
2. Pint (code formatting)
3. PHPStan (static analysis)
4. Tests with coverage

Fix issues iteratively until all checks pass.
```

## Choosing Agent vs Command

| Need                                           | Solution                            |
| ---------------------------------------------- | ----------------------------------- |
| Prompt shortcut with shell/files               | Command                             |
| Specialized AI behavior                        | Agent                               |
| Prompt shortcut that uses specialized behavior | Command with `agent:`               |
| Isolated execution                             | Command with `subtask: true`        |
| Reusable instructions                          | Skill (see creating-agentic-skills) |

## Permission Patterns

Commands inherit the specified agent's permissions, but agents can further restrict:

```yaml
# Allow only safe bash commands
permission:
  bash:
    '*': ask
    'git status': allow
    'git diff*': allow
    'composer test*': allow
    'npm test*': allow
```

```yaml
# Read-only mode
permission:
  edit: deny
  bash:
    '*': deny
    'cat *': allow
    'ls *': allow
```

## Temperature Guidelines

| Value   | Use Case                        |
| ------- | ------------------------------- |
| 0.0-0.1 | Code review, analysis, planning |
| 0.2-0.3 | Bug fixes, test writing         |
| 0.3-0.5 | General development             |
| 0.6-0.8 | Creative tasks, brainstorming   |

## For More Detail

See the `creating-agentic-subagents` skill for:

- Complete agent creation patterns
- Detailed permission configurations
- Context and cost management
- Full production examples
