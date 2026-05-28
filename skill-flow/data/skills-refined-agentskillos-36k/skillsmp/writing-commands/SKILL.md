---
name: writing-commands
description: "Use when creating slash commands, user-invokable shortcuts, or command-based workflows with frontmatter and skill delegation."
---

# Writing Commands

## Overview

Commands are user-invokable shortcuts that trigger specific workflows. Good commands have clear triggers, delegate to skills, and provide feedback.

## When to Create

**Create a command when:**
- User performs same multi-step workflow repeatedly
- Complex process benefits from simple invocation
- Workflow requires specific skill sequence
- Consistent output format is needed

**Don't create for:**
- One-off tasks
- Simple actions (use skills directly)
- Workflows that vary significantly each time

## Structure Template

```markdown
---
name: /command-name
description: [What this command does - shown in help]
allowed_tools: [List of tools command can use]
---

# /command-name

## Purpose
[What problem this command solves]

## Skills to Invoke
[Ordered list of skills to load]

## User Prompts
[Questions to ask user if needed]

## Execution Steps
1. [Step 1]
2. [Step 2]
...

## Success Criteria
[How to know command completed successfully]

## Output Format
[Structure of command response]
```

## Quality Checklist

- [ ] Name starts with / and is memorable
- [ ] Description fits in one line
- [ ] Skills to invoke explicitly ordered
- [ ] User prompts defined for required input
- [ ] Execution steps are clear and sequential
- [ ] Success criteria are measurable
- [ ] Output format is consistent
- [ ] allowed_tools limits scope appropriately

## Testing Requirements

1. **Invocation test** - Command triggers correctly
2. **Skill loading test** - Required skills load in order
3. **User prompt test** - Questions asked when needed
4. **Execution test** - Steps complete as expected
5. **Output test** - Response matches format
6. **Error handling test** - Graceful failure on issues

## Examples

**Good Command:**
```markdown
---
name: /new-feature
description: Start a new feature with session, tests, and implementation
allowed_tools: [Read, Write, Edit, Bash, Skill, Task]
---

## Purpose
Initialize complete feature development workflow with TDD.

## Skills to Invoke
1. session (create session file)
2. test-driven-development (setup test structure)
3. git-expert (create feature branch)

## User Prompts
- "What is the feature name?"
- "Brief description of the feature?"

## Execution Steps
1. Create feature branch: feature/{name}
2. Initialize session file
3. Create test file with first failing test
4. Report setup complete

## Success Criteria
- Branch created
- Session file exists
- Test file with failing test exists

## Output Format
Feature '{name}' initialized:
- Branch: feature/{name}
- Session: .claude/tasks/session-{name}.md
- Test: tests/{name}.test.ts (RED)
```

**Bad Command:**
```markdown
---
name: /do-stuff
---

Does various things.
```
(No purpose, no steps, no criteria)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague name | Use descriptive /verb-noun format |
| No skill delegation | List skills to invoke in order |
| Missing user prompts | Define what input is needed |
| No success criteria | Add measurable completion check |
| Uncontrolled scope | Use allowed_tools to limit actions |
| No output format | Define consistent response structure |
