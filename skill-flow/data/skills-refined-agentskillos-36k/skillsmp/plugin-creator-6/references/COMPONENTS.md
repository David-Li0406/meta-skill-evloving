# Component Templates

Complete templates and examples for all plugin component types.

## Using This Guide

This guide provides two types of templates:

1. **Strict Templates** - Use for consistent, predictable output
2. **Flexible Templates** - Adapt to specific contexts

Choose the template style that matches your component's purpose.

---

## Command Templates

### Strict Template (Recommended)

Use this exact structure for predictable behavior:

```markdown
---
description: [Clear action description, max 100 chars]
args:
  - name: arg_name
    description: What this argument controls
    required: false
  - name: optional_arg
    description: Optional argument description
    required: false
---

# Command Title

## Purpose

[One sentence explaining what this command does]

## Process

Follow these steps exactly:

1. [First step with specific action]
2. [Second step with specific action]
3. [Final step with expected outcome]

## Examples

**Example 1: Basic usage**
```
command-name arg1
```
Expected: [What happens]

**Example 2: With optional argument**
```
command-name arg1 --optional-flag
```
Expected: [What happens with flag]

## Error Handling

If [error condition]:
- Show error: [Clear error message]
- Suggest: [How to fix it]
```

### Flexible Template

Adapt this structure based on your needs:

```markdown
---
description: [Action description]
args:
  - name: arg_name
    description: Argument description
    required: false
---

# Command Title

## Purpose

[Brief description]

## Process

[Adapt steps based on your command's specific workflow]
- [Step 1]
- [Step 2]
- [Add or remove steps as needed]

## Examples

[Include relevant examples for your use case]

## Notes

[Any additional context or variations]
```

### Real Examples

#### Example 1: Git Commit (Strict)

```markdown
---
description: Create a git commit with co-author attribution
args:
  - name: message
    description: Commit message describing the changes
    required: true
---

# Git Commit

## Purpose

Create a properly formatted git commit with co-author attribution.

## Process

Follow these steps exactly:

1. Run `git status` to see current changes
2. Run `git diff --staged` to review staged changes
3. Create commit with message: "message\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
4. Show commit confirmation with hash

## Examples

**Example 1: Single file change**
```
commit "Fix authentication bug"
```
Expected: Creates commit with message and co-author

**Example 2: Feature addition**
```
commit "Add user profile page"
```
Expected: Creates commit for new feature

## Error Handling

If no changes staged:
- Error: "No changes staged for commit"
- Suggest: Run `git add` first to stage files

If commit fails:
- Show git error message
- Check for merge conflicts
```

#### Example 2: Code Review (Flexible)

```markdown
---
description: Review code changes for quality and best practices
args:
  - name: scope
    description: Review scope (file, directory, or 'all')
    required: false
---

# Code Review

## Purpose

Review code changes following best practices and security guidelines.

## Process

- Read the target code
- Check for:
  - Security vulnerabilities
  - Code quality issues
  - Best practice violations
  - Performance concerns
  - Test coverage
- Provide actionable feedback with specific suggestions

Adapt the review depth based on scope (file vs all).

## Examples

Review single file for specific issues.
Review entire codebase for comprehensive analysis.

## Notes

Focus on actionable improvements.
Include code examples for fixes.
Prioritize security and critical issues.
```

---

## Agent Templates

### Strict Template

Use this structure for agents requiring precise execution:

```markdown
---
description: Launch this agent when [specific trigger condition]
color: blue
tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
examples:
  - trigger: "User says [exact phrase]"
    action: "Agent will [specific action]"
  - trigger: "User requests [specific task]"
    action: "Agent performs [specific workflow]"
---

# Agent Name

You are a specialized agent for [specific purpose].

## Your Capabilities

- [Capability 1 with specific details]
- [Capability 2 with specific details]
- [Capability 3 with specific details]

## Your Process

### Phase 1: Discovery

Complete these steps:
1. [Specific discovery action]
2. [Specific discovery action]
3. [Specific discovery action]

### Phase 2: Analysis

Analyze findings:
- [Analysis criteria 1]
- [Analysis criteria 2]
- [Analysis criteria 3]

### Phase 3: Execution

Execute the task:
1. [Execution step 1]
2. [Execution step 2]
3. [Execution step 3]

### Phase 4: Verification

Verify results:
- [Verification criteria 1]
- [Verification criteria 2]

## Output Format

Present results in this structure:

# [Analysis Title]

## Summary
[One-paragraph overview]

## Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Recommendations
1. [Actionable recommendation 1]
2. [Actionable recommendation 2]

## Best Practices

- [Best practice 1]
- [Best practice 2]
```

### Flexible Template

```markdown
---
description: When to use this agent
color: blue
tools: [Read, Write, Bash]
examples:
  - trigger: "User asks..."
    action: "Agent performs..."
---

# Agent Name

You are a specialized agent for [domain].

## Your Process

[Adapt phases based on agent's specific workflow]

### Phase 1: [Name]
[Detailed steps]

### Phase 2: [Name]
[Detailed steps]

[Add or remove phases as needed]

## Best Practices

[Guidelines specific to this agent]
```

### Real Example: Code Analyzer Agent

```markdown
---
description: Launch for comprehensive codebase analysis, dependency mapping, or architecture review
color: purple
tools:
  - Read
  - Glob
  - Grep
examples:
  - trigger: "Analyze this codebase structure"
    action: "Map directory structure, identify entry points, trace dependencies"
  - trigger: "How is this code organized?"
    action: "Analyze architecture and generate component map"
---

# Code Analyzer

You are a codebase analysis specialist.

## Your Capabilities

- Map directory structure and file organization
- Identify entry points and main modules
- Trace dependencies between components
- Analyze import/include patterns
- Generate architecture diagrams

## Your Process

### Phase 1: Structure Discovery

1. Use Glob to find all source files
2. Identify file types and organization
3. Map directory hierarchy

### Phase 2: Dependency Analysis

1. Use Grep to find import/include statements
2. Map module dependencies
3. Identify circular dependencies

### Phase 3: Architecture Summary

Generate structured analysis:

# Codebase Analysis: [Project Name]

## Overview
[Project type, main language, architecture style]

## Structure
```
[Directory tree]
```

## Key Components
- **[Component 1]**: [Purpose and dependencies]
- **[Component 2]**: [Purpose and dependencies]

## Dependencies
[Dependency graph or list]

## Recommendations
1. [Architectural improvement 1]
2. [Architectural improvement 2]

## Best Practices

- Start with broad overview, then drill down
- Show both structure and relationships
- Highlight potential issues (coupling, complexity)
- Suggest improvements when relevant
```

---

## Skill Templates

### Strict Template

```markdown
---
description: Use when [specific scenarios]. Provides [what it does] for [domain/use case]
---

# Skill Name

[One sentence overview]

## Quick Start

```python
[code example]
```

## Core Concepts

- [Concept 1]: [Definition]
- [Concept 2]: [Definition]
- [Concept 3]: [Definition]

## Process

For [task type]:

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

**Example 1: [Scenario]**
```
Input: [example input]
Output: [example output]
```

**Example 2: [Scenario]**
```
Input: [example input]
Output: [example output]
```

## Best Practices

- [Practice 1]
- [Practice 2]
- [Practice 3]
```

### Flexible Template

```markdown
---
description: What this skill provides and when to use it
---

# Skill Name

[Overview]

## Quick Start

[Basic usage example]

## Key Topics

- [Topic 1]: [See [TOPIC1.md](references/TOPIC1.md)]
- [Topic 2]: [See [TOPIC2.md](references/TOPIC2.md)]

## Process

[Adapt based on skill's purpose]

## Best Practices

[Guidelines]
```

### Real Example: React Best Practices Skill

```markdown
---
description: React development patterns and best practices. Use when building React components, hooks, state management, or optimizing React applications
---

# React Best Practices

Modern React development patterns and guidelines.

## Quick Start

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);

  if (loading) return <Spinner />;
  return <div>{user.name}</div>;
}
```

## Core Concepts

- **Components**: Functional components with hooks
- **State**: useState for local state
- **Effects**: useEffect for side effects
- **Performance**: Memo, useCallback, useMemo

## Process

For creating a new component:

1. Define props interface
2. Declare component with function syntax
3. Add state with useState
4. Add effects with useEffect
5. Return JSX

For performance optimization:

1. Identify expensive computations
2. Wrap with useMemo
3. Identify callback functions
4. Wrap with useCallback
5. Memoize child components with React.memo

## Examples

**Example 1: Data fetching component**
```
Input: Create component fetching user data
Output:
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers);
  }, []);
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

**Example 2: Form with validation**
```
Input: Create form with name validation
Output:
function Form() {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const submit = (e) => {
    e.preventDefault();
    if (name.length < 3) setError('Name too short');
    else { /* submit */ }
  };
  return <form onSubmit={submit}>
    <input value={name} onChange={e => setName(e.target.value)} />
    {error && <span>{error}</span>}
  </form>;
}
```

## Best Practices

- Always use functional components, never class components
- Use TypeScript for prop typing
- Keep components small and focused
- Use custom hooks for reusable logic
- Optimize with useMemo/useCallback when needed
- Never mutate state directly
- Always include dependency arrays in useEffect
```

---

## Hook Templates

### Strict Template

```markdown
---
description: This hook [what it does] when [event occurs]
---

# Hook Name

Instructions for event handling.

## Behavior

When [event] occurs:

1. [Check condition 1]
2. [Check condition 2]
3. [Take specific action]

## Conditions

Execute this hook only when:
- [Condition 1]
- [Condition 2]

## Side Effects

This hook will:
- [Side effect 1]
- [Side effect 2]

Do not use this hook for:
- [Inappropriate use 1]
- [Inappropriate use 2]
```

### Flexible Template

```markdown
---
description: What this hook does
---

# Hook Name

Handle [event type] events.

## Behavior

[What to do when event fires]

## Guidelines

- [Guideline 1]
- [Guideline 2]
```

### Real Example: Git Safety Hook

```markdown
---
description: Prevent dangerous git operations like force push to main/master
---

# Git Safety Hook

Protect against destructive git operations.

## Behavior

When Bash tool is about to execute git commands:

1. Check if command contains dangerous patterns:
   - `git push --force`
   - `git push -f`
   - `git reset --hard`
   - `git clean -fd`

2. If dangerous pattern found:
   - Block the tool execution
   - Display warning message
   - Suggest safer alternative

## Conditions

Apply this hook when:
- Tool type is Bash
- Command starts with `git`
- Command contains dangerous flag

Check if target branch is main or master before blocking.

## Side Effects

This hook will:
- Block dangerous operations
- Show warning messages
- Suggest safer alternatives like `--force-with-lease`

Do not use this hook for:
- Safe git commands (status, log, diff)
- Non-git commands
- Force push to feature branches (usually OK)
```

---

## Choosing Template Styles

### Use Strict Templates When:

- Output format must be consistent
- Multiple agents/commands need to work together
- Parsing output programmatically
- Quality standards are critical

**Best for:** API integrations, report generation, data processing

### Use Flexible Templates When:

- Context varies significantly
- Adaptation is important
- Creative output is valued
- Many edge cases exist

**Best for:** Analysis, reviews, exploratory tasks

### Mixing Styles

You can use strict templates for core structure and flexible templates for sub-sections:

```markdown
## Strict Process Section
[Fixed steps always followed]

## Flexible Adaptation
[Adjust based on what you discover]
```

---

## Template Validation Checklist

### All Components

- [ ] YAML frontmatter is valid
- [ ] Description is clear and specific
- [ ] Examples match template style
- [ ] Steps are numbered and actionable
- [ ] Error handling is documented

### Commands

- [ ] Args are documented
- [ ] Examples show usage
- [ ] Error messages are clear

### Agents

- [ ] Tools are listed
- [ ] Examples show triggers
- [ ] Process has clear phases

### Skills

- [ ] Quick start example
- [ ] Core concepts defined
- [ ] Examples show input/output

### Hooks

- [ ] Behavior is documented
- [ ] Conditions are clear
- [ ] Side effects noted
