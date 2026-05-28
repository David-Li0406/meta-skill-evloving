# Multi-Agent Orchestration Template

Use this template for complex tasks requiring parallel agent work.

```markdown
---
allowed-tools: [Tool1], [Tool2], Task, TodoWrite
description: [What the orchestrated workflow does]
---

[High-level task description]

To do this, follow these steps precisely:

1. Use an agent to [initial analysis/validation task]. If [early exit condition], do not proceed.
2. Use an agent to [gather information task] and return [specific output]
3. Launch [N] parallel agents to [parallel task], using [diverse approaches/keywords]
4. Feed results from steps 2 and 3 into another agent to [aggregation/filtering task]
5. Finally, [output action]

Notes (be sure to tell this to your agents, too):

- [Tool constraint]
- [Process constraint]
- [Output format specification]
```

## Example: Duplicate Issue Finder

```markdown
---
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh issue comment:*)
description: Find duplicate GitHub issues for $ARGUMENTS
---

Find up to 3 likely duplicate issues for GitHub issue #$ARGUMENTS.

To do this, follow these steps precisely:

1. Use an agent to check if the issue (a) is closed, (b) is broad feedback without specific solution, or (c) already has a duplicates comment. If any are true, do not proceed.
2. Use an agent to view the issue and return a concise summary of the problem
3. Launch 5 parallel agents to search GitHub for duplicates using diverse keywords and search approaches from the summary
4. Feed results into another agent to filter false positives that aren't actually duplicates
5. If duplicates remain, comment on the issue with the list

Notes (be sure to tell this to your agents, too):

- Use `gh` CLI for all GitHub interactions
- Do not use web fetch or other tools
- Make a todo list first
- Use this exact comment format:

---
Found [N] possible duplicate issues:

1. <link to issue>
2. <link to issue>

🤖 Generated with Claude Code
---
```

## Example: Comprehensive Research

```markdown
---
allowed-tools: Bash, Read, Grep, Glob, Task, TodoWrite
description: Research topic $ARGUMENTS across codebase and documentation
---

Conduct comprehensive research on "$ARGUMENTS" across this codebase.

Follow these steps:

1. Use an agent to search for all files mentioning the topic and create a file list
2. Launch 3 parallel agents to:
   - Agent 1: Analyze code implementations related to the topic
   - Agent 2: Review documentation and comments
   - Agent 3: Check tests for usage patterns and edge cases
3. Feed all results into a synthesis agent to identify:
   - How the feature currently works
   - Known limitations or issues
   - Suggested improvements
4. Produce a research summary

Notes for all agents:
- Focus on the specific topic, ignore tangential mentions
- Include file paths and line numbers for all findings
- Flag any inconsistencies between code and documentation
```

## Example: Multi-Reviewer PR Check

```markdown
---
allowed-tools: Bash, Read, Grep, Glob, Task
description: Multi-aspect PR review with specialized agents
---

Run a comprehensive PR review using specialized agents.

**Changed files:** !`git diff --name-only HEAD~1`

Launch these parallel review agents:

1. **Security Agent**: Check for security vulnerabilities
   - Input validation
   - Authentication issues
   - Data exposure risks

2. **Performance Agent**: Analyze performance implications
   - Algorithm complexity
   - Database queries
   - Memory usage

3. **Test Agent**: Evaluate test coverage
   - Missing test cases
   - Edge cases
   - Integration tests needed

4. **Style Agent**: Review code style and conventions
   - Naming conventions
   - Code organization
   - Documentation

After all agents complete, synthesize findings into:

## Critical Issues (must fix)
[List with file:line references]

## Important Issues (should fix)
[List with file:line references]

## Suggestions (nice to have)
[List with file:line references]

## Strengths
[What's done well]
```

## Tips

1. **Early exit conditions** - Validate before doing heavy work
2. **Parallel where possible** - Launch multiple agents for independent tasks
3. **Result aggregation** - Use a final agent to synthesize parallel outputs
4. **Agent notes** - Include constraints agents should follow
5. **Specific output format** - Define exactly how results should look
6. **TodoWrite for tracking** - Use for systematic processing of lists
