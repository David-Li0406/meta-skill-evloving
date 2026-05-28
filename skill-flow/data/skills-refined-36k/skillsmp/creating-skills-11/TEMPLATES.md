# Skill Templates

Ready-to-use templates for common skill types. Copy and customize.

---

## Template 1: Simple Task Skill

For focused, single-purpose skills.

```yaml
---
name: [skill-name]
description: [Action verb] [what]. Use when [specific triggers].
---

# [Skill Name]

## Overview
[One sentence: what this skill does]

## When to Use
- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]

## Instructions

1. [First step]
2. [Second step]
3. [Third step]

## Example

**User says:** "[Example request]"

**Claude does:**
1. [Action 1]
2. [Action 2]
3. [Result]
```

---

## Template 2: Read-Only Analysis Skill

For skills that analyze without modifying.

```yaml
---
name: [analysis-skill-name]
description: Analyze [what] for [purpose]. Use when reviewing, auditing, or examining [domain].
allowed-tools: Read, Grep, Glob
---

# [Analysis Skill Name]

## Overview
Provides read-only analysis of [domain] without making changes.

## Capabilities
- [Analysis capability 1]
- [Analysis capability 2]
- [Analysis capability 3]

## What This Skill Does NOT Do
- Modify files
- Execute commands
- Make changes

## Analysis Process

### Step 1: Gather Information
[How to collect data]

### Step 2: Analyze
[What to look for]

### Step 3: Report
[How to present findings]

## Output Format

```
## Analysis Summary
- Finding 1: [description]
- Finding 2: [description]

## Recommendations
1. [Recommendation]
2. [Recommendation]
```
```

---

## Template 3: Code Generation Skill

For skills that generate code following patterns.

```yaml
---
name: [generator-skill-name]
description: Generate [what] following [patterns/conventions]. Use when creating [artifacts], scaffolding [components], or setting up [features].
---

# [Generator Skill Name]

## Overview
Generates [artifacts] following project conventions and best practices.

## Prerequisites
- [Required dependency 1]
- [Required dependency 2]

## Conventions

### Naming
- Files: `[naming-pattern]`
- Functions: `[naming-pattern]`
- Types: `[naming-pattern]`

### Structure
```
[directory-structure]
```

### Patterns
[Key patterns to follow]

## Generation Process

1. **Validate inputs** - [What to check]
2. **Determine location** - [Where to create]
3. **Generate code** - [What to create]
4. **Verify** - [How to validate]

## Template

```[language]
[Code template with placeholders]
```

## Example

**Request:** "[Example request]"

**Generated:**
```[language]
[Example output]
```
```

---

## Template 4: Multi-Step Workflow Skill

For skills that guide complex workflows.

```yaml
---
name: [workflow-skill-name]
description: [Workflow description]. Use when [triggers]. Guides through [process].
---

# [Workflow Skill Name]

## Overview
Guides you through [workflow] from start to finish.

## When to Use
- [Scenario 1]
- [Scenario 2]

## Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Workflow Steps

### Phase 1: [Phase Name]

#### Step 1.1: [Step Name]
[Instructions]

#### Step 1.2: [Step Name]
[Instructions]

### Phase 2: [Phase Name]

#### Step 2.1: [Step Name]
[Instructions]

#### Step 2.2: [Step Name]
[Instructions]

### Phase 3: [Phase Name]

#### Step 3.1: [Step Name]
[Instructions]

## Verification

After completing the workflow:
- [ ] [Verification check 1]
- [ ] [Verification check 2]
- [ ] [Verification check 3]

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| [Problem 1] | [Cause] | [Solution] |
| [Problem 2] | [Cause] | [Solution] |
```

---

## Template 5: Domain Expert Skill

For skills that encode specialized domain knowledge.

```yaml
---
name: [domain-skill-name]
description: [Domain] expertise for [purpose]. Use when working with [domain], implementing [features], or troubleshooting [issues].
---

# [Domain] Expertise

## Overview
Provides specialized knowledge for [domain].

## Core Concepts

### [Concept 1]
[Explanation]

### [Concept 2]
[Explanation]

### [Concept 3]
[Explanation]

## Best Practices

1. **[Practice 1]** - [Why and how]
2. **[Practice 2]** - [Why and how]
3. **[Practice 3]** - [Why and how]

## Common Patterns

### Pattern: [Pattern Name]
**When to use:** [Scenario]
**Implementation:**
```[language]
[Code example]
```

### Pattern: [Pattern Name]
**When to use:** [Scenario]
**Implementation:**
```[language]
[Code example]
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| [Anti-pattern 1] | [Why it's bad] | [What to do instead] |
| [Anti-pattern 2] | [Why it's bad] | [What to do instead] |

## Troubleshooting Guide

### [Issue 1]
**Symptoms:** [What you see]
**Cause:** [Why it happens]
**Solution:** [How to fix]

### [Issue 2]
**Symptoms:** [What you see]
**Cause:** [Why it happens]
**Solution:** [How to fix]

## Resources
- [Link to supporting file 1](file1.md)
- [Link to supporting file 2](file2.md)
```

---

## Template 6: Tool Integration Skill

For skills that integrate with external tools.

```yaml
---
name: [tool-skill-name]
description: Integrate with [tool] for [purpose]. Use when [triggers]. Requires [dependencies].
allowed-tools: Bash([tool]:*), Read
---

# [Tool] Integration

## Overview
Enables [tool] operations for [purpose].

## Prerequisites

```bash
# Install [tool]
[installation-command]

# Verify installation
[verification-command]
```

## Configuration

Required environment variables:
- `[ENV_VAR_1]` - [Description]
- `[ENV_VAR_2]` - [Description]

## Available Commands

### [Command 1]
**Purpose:** [What it does]
**Usage:**
```bash
[command-syntax]
```

### [Command 2]
**Purpose:** [What it does]
**Usage:**
```bash
[command-syntax]
```

## Common Workflows

### [Workflow 1]
```bash
# Step 1: [Description]
[command]

# Step 2: [Description]
[command]
```

### [Workflow 2]
```bash
# Step 1: [Description]
[command]

# Step 2: [Description]
[command]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| [Error message 1] | [Cause] | [How to fix] |
| [Error message 2] | [Cause] | [How to fix] |
```

---

## Quick Reference: Description Formulas

Use these formulas to write effective descriptions:

```
# Action-focused
[Verb] [what] for [purpose]. Use when [triggers].

# Capability-focused
[Capability 1], [capability 2], and [capability 3]. Use when [triggers].

# Domain-focused
[Domain] expertise for [purpose]. Use when working with [domain] or [related activities].
```

**Power words for triggers:**
- "Use when creating...", "Use when debugging...", "Use when reviewing..."
- "Use for...", "Use with...", "Use during..."
- Specific nouns: "PRs", "migrations", "tests", "deployments"
