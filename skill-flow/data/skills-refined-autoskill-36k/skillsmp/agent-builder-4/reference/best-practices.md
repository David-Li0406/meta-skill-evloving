# Agent Best Practices

Design principles and patterns for creating effective sub-agents.

## Core Design Principles

### 1. Single Responsibility Principle

**Do**: Create focused agents with one clear purpose

```markdown
---
name: sql-query-reviewer
description: Review SQL queries for performance issues and suggest optimizations
---
```

**Don't**: Create catch-all agents

```markdown
---
name: database-helper
description: Help with any database-related tasks
---
```

**Why**: Focused agents trigger correctly and produce better results.

### 2. Explicit Trigger Conditions

**Do**: Use specific, action-oriented descriptions with trigger keywords

```markdown
description: Use PROACTIVELY after writing tests to check for common testing anti-patterns like mocking implementation details
```

**Don't**: Use vague descriptions

```markdown
description: A testing expert
```

**Why**: Claude's routing mechanism uses description to decide when to invoke agents.

### 3. Principle of Least Privilege

**Do**: Grant only necessary tools

```markdown
# Read-only security auditor
tools: Read, Grep, Glob
```

**Don't**: Give all tools by default

```markdown
# Unnecessary full access
tools: Read, Write, Edit, Bash, Grep, Glob
```

**Why**: Limits blast radius if agent behaves unexpectedly.

### 4. Detailed Instructions

**Do**: Provide step-by-step guidance

```markdown
## Analysis Process

1. Read the error message and stack trace
2. Identify the failing line of code
3. Read surrounding context (10 lines before/after)
4. Check recent changes using git blame
5. Propose specific fix with explanation
```

**Don't**: Give vague guidance

```markdown
Debug the error and fix it.
```

**Why**: Detailed instructions yield consistent, high-quality results.

### 5. Output Structure

**Do**: Define explicit output format

```markdown
## Output Format

# Bug Analysis

## Root Cause
[One sentence summary]

## Details
[Full explanation]

## Proposed Fix
```[language]
[exact code change]
```

## Verification
[how to test the fix]
```

**Don't**: Leave output format unspecified

```markdown
Analyze the bug and suggest a fix.
```

**Why**: Consistent outputs are easier to act on and integrate.

## Naming Conventions

### Good Agent Names

- `rails-code-reviewer` - Specific technology and task
- `sql-query-optimizer` - Clear action and domain
- `security-vulnerability-scanner` - Explicit purpose
- `test-coverage-analyzer` - Measurable outcome
- `api-doc-generator` - Clear deliverable

### Bad Agent Names

- `helper` - Too generic
- `my-agent` - Not descriptive
- `agent1` - No indication of purpose
- `CodeAgent` - Not lowercase-with-hyphens
- `do-everything` - Violates single responsibility

### Naming Pattern

```
[technology/domain]-[action/purpose]

Examples:
- docker-container-optimizer
- python-type-hint-generator
- kubernetes-manifest-validator
- git-commit-message-writer
```

## Description Patterns

### Pattern 1: Trigger Keywords

Include specific words that signal when agent should activate:

```markdown
description: Use when encountering SQL queries with EXPLAIN showing high cost or missing indexes
```

**Triggers**: "SQL", "EXPLAIN", "high cost", "missing indexes"

### Pattern 2: Proactive Invocation

Use "PROACTIVELY" or "MUST BE USED" for automatic triggering:

```markdown
description: Use PROACTIVELY after code changes to review for security vulnerabilities
```

**Effect**: Claude invokes automatically after code modifications.

### Pattern 3: Conditional Use

Specify when agent applies vs doesn't:

```markdown
description: Use for Python code performance optimization, especially when profiling shows bottlenecks. Do not use for Go or Rust code.
```

**Effect**: Clear boundaries prevent misuse.

### Pattern 4: Input/Output Signal

Describe inputs and expected outputs:

```markdown
description: Analyze git diff output to generate semantic, conventional commit messages following Angular style guide
```

**Triggers**: "git diff", "commit messages", "Angular style"

## Tool Selection Guidelines

### Read-Only Agents (Security/Audit)

```yaml
tools: Read, Grep, Glob
```

**Use for**: Security auditing, code review, analysis

**Rationale**: Can't accidentally modify code

### Code Modifiers

```yaml
tools: Read, Edit, Bash
```

**Use for**: Refactoring, fixing bugs, applying changes

**Rationale**: Can read context and make surgical edits

### Exploratory Agents

```yaml
tools: Read, Grep, Glob, Bash
```

**Use for**: Debugging, investigation, running tests

**Rationale**: Needs to explore codebase and run commands

### Full Access Agents

```yaml
# Omit tools field to inherit all tools
```

**Use for**: Complex workflows, multi-step tasks

**Rationale**: Needs flexibility for varied tasks

### Restricted Agents

```yaml
tools: Bash
```

**Use for**: Infrastructure tasks, running specific commands

**Rationale**: Focused on execution, not code manipulation

## Model Selection

### When to Use Haiku

- Simple, repetitive tasks
- Fast turnaround needed
- Lower cost priority
- Clear, deterministic workflows

**Examples**: Formatting, linting, simple validation

### When to Use Sonnet (Default)

- Balanced performance and speed
- Most general-purpose tasks
- Standard code review/debugging
- Moderate complexity

**Examples**: Code review, debugging, optimization

### When to Use Opus

- Complex reasoning required
- Critical decisions
- Security-sensitive tasks
- High accuracy needed

**Examples**: Security audits, architectural decisions, complex refactoring

### When to Inherit

- Agent should match main conversation capability
- User may switch models
- No specific model requirement

**Examples**: General helpers, documentation

## System Prompt Patterns

### Pattern 1: Process-Oriented

Define step-by-step workflow:

```markdown
## Process

1. **Gather Context**: Read all relevant files
2. **Identify Issues**: List problems found
3. **Prioritize**: Order by severity
4. **Propose Solutions**: Specific fixes
5. **Document**: Clear explanation
```

**Use for**: Agents with clear workflows

### Pattern 2: Checklist-Based

Provide systematic checks:

```markdown
## Security Checklist

- [ ] No SQL injection vulnerabilities
- [ ] Authentication on protected routes
- [ ] Input validation present
- [ ] Secrets not in code
- [ ] HTTPS enforced
```

**Use for**: Audit and validation agents

### Pattern 3: Example-Driven

Show examples of good outputs:

```markdown
## Example Output

### Good Example
**Input**: User implements login endpoint
**Output**:
✅ Strengths: Proper password hashing
⚠️ Issue: Missing rate limiting
💡 Suggestion: Add rack-attack gem
```

**Use for**: Agents where output format is crucial

### Pattern 4: Constraint-First

Lead with what NOT to do:

```markdown
## Constraints

- NEVER modify tests to make them pass
- DO NOT suggest rewrites without justification
- AVOID proposing multiple solutions - pick best
- NO generic advice - be specific
```

**Use for**: Agents that might overstep bounds

## Common Pitfalls

### Pitfall 1: Too Generic

**Problem**: Agent never triggers or triggers too often

**Solution**: Add specific trigger keywords and domain constraints

### Pitfall 2: Unclear Output

**Problem**: Agent responses are inconsistent

**Solution**: Define explicit output format with examples

### Pitfall 3: Scope Creep

**Problem**: Agent tries to do too much

**Solution**: Split into multiple focused agents

### Pitfall 4: Missing Context

**Problem**: Agent doesn't have enough information

**Solution**: Specify what context to gather first

### Pitfall 5: Over-Engineering

**Problem**: Agent is too complex

**Solution**: Start simple, add complexity only when needed

## Testing Your Agent

### Test Cases to Cover

1. **Happy Path**: Agent works as expected
2. **Edge Cases**: Unusual but valid inputs
3. **Error Handling**: Invalid or missing inputs
4. **Scope Boundaries**: When agent should NOT trigger
5. **Tool Limitations**: Agent lacks necessary permissions

### Testing Checklist

- [ ] Test with explicit invocation: "Use [agent-name] to..."
- [ ] Test with implicit trigger: Describe task without naming agent
- [ ] Test with minimal input
- [ ] Test with complex input
- [ ] Test when agent shouldn't trigger
- [ ] Test with insufficient permissions (if tools limited)
- [ ] Verify output format matches specification
- [ ] Check output quality and usefulness

### Iteration Process

1. **Initial Test**: Try basic functionality
2. **Identify Gaps**: What doesn't work?
3. **Refine Prompt**: Add missing instructions
4. **Add Examples**: Show what good looks like
5. **Test Again**: Verify improvements
6. **Repeat**: Until agent is reliable

## Documentation Standards

### Minimum Documentation

Every agent should include:

```markdown
---
name: agent-name
description: When to use this agent
---

# Agent Purpose

[What it does]

## Core Responsibilities

[Main tasks]

## Approach

[How it works]

## Output Format

[What it produces]

## Constraints

[What it won't do]
```

### Enhanced Documentation

For complex agents, add:

- Input validation rules
- Error handling approach
- Edge case handling
- Examples (good and bad)
- Troubleshooting tips
- Related agents
- Version history

## Performance Considerations

### Context Window Management

- Agents start with fresh context
- May need to re-read files
- Consider token costs for large codebases

**Optimization**: Provide clear file paths in description

### Token Efficiency

- Concise system prompts are faster
- But clarity > brevity
- Use examples judiciously

**Balance**: Detailed enough to work, concise enough to load quickly

### Caching Benefits

- Repeated invocations may benefit from caching
- System prompt is cacheable
- Frequently accessed files may be cached

**Note**: Implementation-specific, but generally beneficial

## Version Control Best Practices

### Project Agents

✅ **Do Commit**:
- `.claude/agents/*.md` - All project agents
- Document in README when to use each agent

❌ **Don't Commit**:
- User-specific agents from `~/.claude/agents/`
- API keys or secrets (should be in env vars)

### User Agents

- Keep in `~/.claude/agents/` for personal use
- Back up separately (not in project repos)
- Share via documentation/templates if useful to others

## Sharing Agents

### With Your Team

1. Commit to `.claude/agents/` in project
2. Document in project README
3. Add trigger examples
4. Provide test cases

### With Community

1. Create template repository
2. Include:
   - Agent file with clear comments
   - README with usage examples
   - Test cases or fixtures
   - License information
3. Share on forums/communities

## Maintenance

### When to Update

- Agent triggers incorrectly (too often/rarely)
- Output format changes
- New tool becomes available
- Domain knowledge evolves
- Team feedback indicates issues

### Update Checklist

- [ ] Update description/triggers
- [ ] Revise system prompt
- [ ] Add new examples
- [ ] Update tool permissions
- [ ] Test thoroughly
- [ ] Document changes
- [ ] Notify team (if shared)

### Deprecation

When agent is no longer needed:

1. Add deprecation notice to file
2. Suggest replacement agent (if any)
3. Set sunset date
4. Remove after team transitions
5. Archive for reference

## Advanced Patterns

### Chained Agents

Design agents that work in sequence:

1. `code-analyzer` → identifies issues
2. `code-fixer` → applies fixes
3. `test-runner` → verifies fixes

**Use for**: Complex multi-step workflows

### Specialized + General

Pair specific and general agents:

- `rails-code-reviewer` (specific)
- `code-reviewer` (general fallback)

**Use for**: Covering multiple domains

### Hierarchical Agents

Create parent-child relationships:

- `security-auditor` (parent)
  - `sql-injection-scanner` (child)
  - `xss-scanner` (child)
  - `auth-checker` (child)

**Use for**: Breaking down complex domains

---

## Quick Reference

### Agent Creation Checklist

- [ ] Name: lowercase-with-hyphens, descriptive
- [ ] Description: specific triggers, action-oriented
- [ ] Tools: minimal necessary permissions
- [ ] Model: appropriate for task complexity
- [ ] System prompt: detailed, structured
- [ ] Examples: show good outputs
- [ ] Constraints: explicit boundaries
- [ ] Output format: clearly defined
- [ ] Tested: multiple scenarios
- [ ] Documented: usage and purpose

### Common Patterns

| Pattern | When to Use |
|---------|-------------|
| Process-oriented | Clear workflow steps |
| Checklist-based | Systematic validation |
| Example-driven | Output format matters |
| Constraint-first | Agent might overstep |

### Tool Combinations

| Combination | Use Case |
|-------------|----------|
| Read, Grep, Glob | Analysis/audit only |
| Read, Edit | Surgical code changes |
| Read, Edit, Bash | Refactoring + testing |
| Bash | Infrastructure/ops |
| All tools (inherited) | Complex workflows |

---

**See Also**:
- [Configuration Guide](./configuration-guide.md)
- [Agent Examples](./agent-examples.md)
- [Troubleshooting](./troubleshooting.md)
