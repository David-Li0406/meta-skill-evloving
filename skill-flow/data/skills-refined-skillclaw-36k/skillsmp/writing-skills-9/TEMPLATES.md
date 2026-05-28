# Skill Templates

Starter templates for creating new Claude Code skills.

## Basic Skill Template

Minimal skill with required elements:

```markdown
---
name: skill-name
description: Brief description of what skill does. Use when [trigger conditions]. Helps with [outcomes].
---

# Skill Title

One-sentence overview of what this skill accomplishes.

## Quick Reference

| Element | Value |
|---------|-------|
| Key concept | Description |

## Core Instructions

Main guidance content here.

## Workflow

### Steps

1. **First Step**
   - [ ] Action item

2. **Second Step**
   - [ ] Action item

## Examples

### Example: Basic Usage

**Input:**
User request

**Output:**
Expected result
```

## Development Skill Template

For skills that guide code development:

```markdown
---
name: developing-feature
description: Guide for implementing [feature type]. Use when creating new [components], debugging [issues], or extending [functionality].
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Developing [Feature]

Guide for implementing [feature type] following project patterns.

## Quick Reference

| Pattern | Location |
|---------|----------|
| Pattern 1 | `src/path/` |
| Pattern 2 | `src/other/` |

## Architecture

Brief description of how this feature type fits in the codebase.

## Implementation Workflow

### Prerequisites
- [ ] Understand existing patterns
- [ ] Identify target location

### Steps

1. **Create Base Structure**
   - [ ] Create file at correct location
   - [ ] Add required imports

2. **Implement Core Logic**
   - [ ] Follow established patterns
   - [ ] Add error handling

3. **Add Tests**
   - [ ] Unit tests
   - [ ] Integration tests

4. **Validate**
   - [ ] Run test suite
   - [ ] Check types

## Code Patterns

### Pattern: [Name]

```typescript
// Example code pattern
```

## Reference Files

| File | Contents |
|------|----------|
| [PATTERNS.md](./PATTERNS.md) | Detailed code patterns |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues |
```

## Documentation Skill Template

For skills that guide documentation:

```markdown
---
name: documenting-component
description: Guide for documenting [component type]. Use when writing READMEs, API docs, or inline documentation.
allowed-tools: ["Read", "Write", "Edit", "Glob"]
---

# Documenting [Component]

Standards for [component type] documentation.

## Quick Reference

| Doc Type | Template |
|----------|----------|
| README | See README section |
| API | See API Docs section |

## README Structure

### Required Sections

1. Title and description
2. Installation
3. Quick start
4. API reference
5. Examples

### Template

```markdown
# Component Name

Brief description.

## Installation

\`\`\`bash
bun add component
\`\`\`

## Quick Start

\`\`\`typescript
import { Component } from 'component';
\`\`\`

## API

### `functionName(params)`

Description.

## Examples

Example code.
```

## Workflow

1. **Identify Audience**
   - [ ] Determine reader expertise level
   - [ ] Identify key use cases

2. **Structure Content**
   - [ ] Create outline
   - [ ] Add required sections

3. **Write Content**
   - [ ] Clear, concise language
   - [ ] Code examples

4. **Validate**
   - [ ] Test code examples
   - [ ] Check links
```

## Workflow-Heavy Skill Template

For skills focused on procedures:

```markdown
---
name: deploying-service
description: Guide for deploying [service type]. Use when preparing releases, configuring environments, or troubleshooting deployments.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Deploying [Service]

Step-by-step deployment procedures.

## Quick Reference

| Environment | URL |
|-------------|-----|
| Development | localhost:3000 |
| Staging | staging.example.com |
| Production | example.com |

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Dependencies audited

## Workflow: Development Deploy

### Steps

1. **Build**
   ```bash
   bun run build
   ```
   - [ ] Build succeeds
   - [ ] No warnings

2. **Test**
   ```bash
   bun test
   ```
   - [ ] All tests pass

3. **Deploy**
   ```bash
   bun run deploy:dev
   ```
   - [ ] Deployment completes
   - [ ] Health check passes

### Validation
- [ ] Service responds at expected URL
- [ ] Logs show no errors

## Workflow: Production Deploy

### Prerequisites
- [ ] Staging deploy verified
- [ ] Stakeholder approval

### Steps

1. **Create Release**
   - [ ] Tag version
   - [ ] Update changelog

2. **Deploy**
   ```bash
   bun run deploy:prod
   ```
   - [ ] Zero-downtime deployment
   - [ ] Rollback plan ready

3. **Verify**
   - [ ] Health checks pass
   - [ ] Monitor metrics

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check dependencies |
| Deploy timeout | Increase timeout, check resources |
```

## Tool-Restricted Skill Template

For skills with limited tool access:

```markdown
---
name: reviewing-code
description: Guide for code review. Use when reviewing PRs, auditing code quality, or checking security.
allowed-tools: ["Read", "Glob", "Grep"]
model: sonnet
---

# Reviewing Code

Code review guidelines without modification capabilities.

## Quick Reference

| Check | Priority |
|-------|----------|
| Security | High |
| Logic | High |
| Style | Medium |

## Review Checklist

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS prevented

### Logic
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No infinite loops

### Style
- [ ] Consistent formatting
- [ ] Meaningful names
- [ ] Comments where needed

## Workflow

1. **Initial Scan**
   - [ ] Read PR description
   - [ ] Understand scope

2. **Security Review**
   - [ ] Check for vulnerabilities
   - [ ] Verify auth/authz

3. **Logic Review**
   - [ ] Trace data flow
   - [ ] Check edge cases

4. **Report Findings**
   - [ ] Document issues
   - [ ] Suggest improvements
```
