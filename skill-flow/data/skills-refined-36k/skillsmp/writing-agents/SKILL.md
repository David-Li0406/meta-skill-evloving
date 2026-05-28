---
name: writing-agents
description: "Use when creating new agents, defining agent roles, or configuring agent handoff protocols and model selection."
---

# Writing Agents

## Overview

Agents are specialized personas with defined roles, skills, and boundaries. Good agents have clear responsibilities and know when to delegate.

## When to Create

**Create an agent when:**
- Task requires specialized expertise
- Separation of concerns improves quality
- Different context requirements (maximize vs conserve)
- Parallel execution would benefit from specialization

**Don't create for:**
- Simple tasks handleable by main agent
- Tasks without clear specialization
- One-off needs

## Structure Template

```markdown
---
name: agent-name
role: [One-line role description]
model: [claude-sonnet-4-20250514 / claude-opus-4-5-20251101]
---

# Agent Name

## Role
[What this agent is responsible for]

## Skills to Load
[List of skills this agent should invoke]

## Input Format
[What information this agent expects]

## Output Format
[How this agent should structure responses]

## Boundaries
[What this agent should NOT do]

## Handoff Protocol
[When and how to delegate to other agents]
```

## Quality Checklist

- [ ] Clear, specific role definition
- [ ] Model selection justified (sonnet for speed, opus for reasoning)
- [ ] Skills to load explicitly listed
- [ ] Input/output format defined
- [ ] Boundaries prevent scope creep
- [ ] Handoff protocol for edge cases
- [ ] No overlap with existing agents

## Testing Requirements

1. **Role clarity test** - Can you explain what this agent does in one sentence?
2. **Boundary test** - Give tasks outside scope, verify delegation
3. **Handoff test** - Verify smooth transitions to other agents
4. **Skills test** - Verify agent loads and follows listed skills
5. **Output test** - Verify consistent output format

## Examples

**Good Agent:**
```markdown
---
name: security-auditor
role: Reviews code for security vulnerabilities and compliance
model: claude-sonnet-4-20250514
---

## Role
Analyze code for security issues: injection, auth flaws, data exposure.

## Skills to Load
- debug (for tracing attack vectors)

## Input Format
- File paths or code snippets to review
- Security requirements (if any)

## Output Format
| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|

## Boundaries
- Does NOT fix issues (only reports)
- Does NOT review performance or style

## Handoff Protocol
- Critical findings -> Alert main agent immediately
- Implementation fixes -> Hand to appropriate specialist
```

**Bad Agent:**
```markdown
---
name: helper
---

Helps with stuff. Does various things as needed.
```
(No role, no boundaries, no structure)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Role too broad | Narrow to specific domain |
| No skill list | Explicitly list skills to load |
| Missing output format | Define structured response format |
| No boundaries | State what agent should NOT do |
| No handoff protocol | Define delegation triggers |
| Wrong model selection | Sonnet for speed, Opus for complex reasoning |
