# Model Selection Guide

Choose the right Claude model for each task to optimize cost-effectiveness without sacrificing quality.

## Model Overview

### Available Models

| Model | Strengths | Cost | Speed |
|-------|-----------|------|-------|
| **Haiku** | Fast, efficient, simple tasks | $ | Fastest |
| **Sonnet** | Balanced, general purpose | $$ | Fast |
| **Opus** | Deep reasoning, complex analysis | $$$$$ | Slower |

### Relative Pricing

Approximate cost ratios (Haiku = 1x):

| Model | Input | Output |
|-------|-------|--------|
| Haiku | 1x | 1x |
| Sonnet | 3x | 5x |
| Opus | 15x | 75x |

**Key insight**: Opus output tokens are significantly more expensive. Long Opus responses add up quickly.

## Model Capabilities

### Haiku

**Best for:**
- File exploration and listing
- Simple find/replace operations
- Formatting and cleanup
- Running commands
- Straightforward edits
- Repetitive tasks

**Limitations:**
- May miss nuances
- Limited multi-step reasoning
- Less context retention
- Simpler explanations

**Example tasks:**
```
> List all TypeScript files in src/
> Rename all instances of "oldName" to "newName"
> Format this JSON file
> Run npm install
> Add "use strict" to all JS files
```

### Sonnet (Default)

**Best for:**
- General development work
- Feature implementation
- Bug fixing
- Code review
- Testing
- Documentation

**Sweet spot:**
- 80% of typical development tasks
- Good balance of cost and capability
- Sufficient reasoning for most code
- Reliable for production work

**Example tasks:**
```
> Implement user registration with validation
> Fix the memory leak in the event handler
> Write unit tests for the auth module
> Refactor this function to be async
> Review this PR for issues
```

### Opus

**Best for:**
- Architecture decisions
- Complex refactoring
- Security analysis
- Performance optimization
- Debugging difficult issues
- Multi-system integration
- Critical code review

**When the cost is worth it:**
- Decisions affecting entire codebase
- Security-sensitive operations
- Complex reasoning required
- High-stakes changes
- Exploring novel solutions

**Example tasks:**
```
> ultrathink: Design the authentication architecture
> Analyze security implications of this change
> Optimize database queries across the application
> Debug this race condition in the distributed system
> Plan migration from monolith to microservices
```

## Decision Framework

### The 3-Question Test

1. **Is this exploratory or straightforward?**
   - Exploratory/simple -> Haiku
   - Some complexity -> Sonnet
   - Deep reasoning needed -> Opus

2. **What's the blast radius?**
   - Single file, reversible -> Haiku/Sonnet
   - Multiple files -> Sonnet
   - Architecture/security -> Opus

3. **Can a mistake be easily fixed?**
   - Yes -> Haiku/Sonnet
   - No -> Sonnet/Opus
   - Definitely not -> Opus

### Task-to-Model Mapping

| Task Category | Model | Reasoning |
|---------------|-------|-----------|
| **Exploration** | | |
| Find files | Haiku | Simple search |
| Understand codebase | Sonnet | Needs synthesis |
| Architecture analysis | Opus | Deep reasoning |
| **Modification** | | |
| Rename/format | Haiku | Mechanical |
| Implement feature | Sonnet | Balanced |
| Major refactor | Opus | Complex reasoning |
| **Debugging** | | |
| Syntax errors | Haiku | Obvious fixes |
| Logic bugs | Sonnet | Reasoning needed |
| Race conditions | Opus | Complex analysis |
| **Review** | | |
| Linting issues | Haiku | Pattern matching |
| Code review | Sonnet | Judgment needed |
| Security audit | Opus | Deep analysis |
| **Testing** | | |
| Run tests | Haiku | Execution |
| Write tests | Sonnet | Coverage thinking |
| Test strategy | Opus | Architecture |

## Usage Patterns

### Setting Model in Skills

```yaml
---
name: code-explorer
model: haiku
---
Explore codebase and report findings concisely.
```

### Model in Subagents

```yaml
---
name: security-reviewer
model: opus
tools: Read, Grep
---
Perform deep security analysis. Flag all concerns.
```

### Model Escalation Pattern

Start cheap, escalate as needed:

```
Step 1 (Haiku): Scan for potential issues
[Finds 5 files with concerns]

Step 2 (Sonnet): Review flagged files
[Identifies 2 real issues]

Step 3 (Opus): Deep analysis of issues
[Provides comprehensive fix strategy]
```

Total cost: Much less than using Opus for everything.

## Cost Optimization Strategies

### Haiku First Strategy

1. Use Haiku for initial exploration
2. Identify specific areas needing attention
3. Switch to Sonnet/Opus for targeted work

**Example:**
```
> [Haiku] List all API endpoints in src/api/
> [Haiku] Find endpoints without error handling
> [Sonnet] Add error handling to these 5 endpoints
```

### The Sonnet Default

Sonnet is the default for good reason:
- Handles 80% of tasks well
- Cost-effective for sustained work
- Reliable enough for production
- Fast enough for iteration

**Don't reach for Opus unless you need it.**

### Opus Sparingly

Reserve Opus for:
- Initial architecture decisions
- Security-critical changes
- When Sonnet gives unsatisfactory results
- Complex multi-file refactors
- Debugging after Sonnet attempts fail

**Track Opus usage**: Know when you use it and why.

## Cost Comparison Scenarios

### Scenario 1: Implement User Feature

| Approach | Estimated Cost |
|----------|---------------|
| All Opus | $$$$$ |
| All Sonnet | $$$ |
| Sonnet + Haiku exploration | $$ |

**Best**: Haiku for file exploration, Sonnet for implementation.

### Scenario 2: Security Audit

| Approach | Estimated Cost |
|----------|---------------|
| All Opus | $$$$$ |
| Haiku scan + Opus review | $$ |
| Just Sonnet | $$$ (may miss issues) |

**Best**: Haiku identifies candidates, Opus does deep review.

### Scenario 3: Codebase Exploration

| Approach | Estimated Cost |
|----------|---------------|
| Opus exploration | $$$$$ |
| Sonnet exploration | $$$ |
| Haiku exploration | $ |

**Best**: Almost always Haiku. Exploration is simple.

## Multi-Model Workflows

### Feature Implementation

```
Phase 1: Exploration (Haiku)
- Find relevant files
- Understand structure
- List dependencies

Phase 2: Design (Sonnet/Opus)
- Plan implementation
- Define interfaces
- Consider edge cases

Phase 3: Implementation (Sonnet)
- Write code
- Add tests
- Handle errors

Phase 4: Review (Sonnet)
- Self-review changes
- Verify tests pass
- Check edge cases
```

### Bug Investigation

```
Level 1 (Haiku): Gather information
- Find related files
- Collect error messages
- List recent changes

Level 2 (Sonnet): Initial analysis
- Review code flow
- Form hypotheses
- Test simple fixes

Level 3 (Opus): Deep debugging
- Complex root cause analysis
- Multi-component investigation
- Non-obvious fixes
```

### Code Review Pipeline

```
Stage 1 (Haiku): Surface checks
- Formatting issues
- Obvious errors
- Missing files

Stage 2 (Sonnet): Logic review
- Code correctness
- Test coverage
- Error handling

Stage 3 (Opus): Deep review
- Security implications
- Architecture concerns
- Performance issues
```

## Model Selection Checklist

Before choosing a model, ask:

- [ ] What's the task complexity? (Simple -> Haiku)
- [ ] Does it need reasoning? (Yes -> Sonnet/Opus)
- [ ] Is it security-sensitive? (Yes -> Opus)
- [ ] Is it reversible? (No -> higher tier)
- [ ] Did Sonnet fail? (Yes -> try Opus)
- [ ] Is this exploration? (Yes -> Haiku)
- [ ] Am I doing architecture? (Yes -> Opus)

## Common Mistakes

| Mistake | Better Approach |
|---------|-----------------|
| Opus for all tasks | Use Sonnet default |
| Opus for exploration | Use Haiku |
| Sonnet for simple edits | Use Haiku |
| Not escalating when stuck | Try higher model |
| Staying with failing model | Switch up |

## Quick Reference

**Use Haiku when:**
- Exploring
- Searching
- Simple edits
- Running commands
- Formatting

**Use Sonnet when:**
- Implementing features
- Fixing bugs
- Writing tests
- Reviewing code
- General development

**Use Opus when:**
- Designing architecture
- Security analysis
- Complex refactoring
- Stuck on hard problem
- High-stakes decisions
