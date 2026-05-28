---
name: task-analyzer
description: Use this skill when you need to analyze a task's complexity, select appropriate skills, or estimate the work scale involved in a project.
---

# Task Analyzer

Provides metacognitive task analysis and skill selection guidance.

## Skills Index

See **[skills-index.yaml](references/skills-index.yaml)** for available skills metadata.

## Task Analysis Process

### 1. Understand Task Essence

Identify the fundamental purpose beyond surface-level work:

| Surface Work | Fundamental Purpose |
|--------------|---------------------|
| "Fix this bug" | Problem solving, root cause analysis |
| "Implement this feature" | Feature addition, value delivery |
| "Refactor this code" | Quality improvement, maintainability |
| "Update this file" | Change management, consistency |

**Key Questions:**
- What problem are we really solving?
- What is the expected outcome?
- What could go wrong if we approach this superficially?

### 2. Estimate Task Scale

| Scale | File Count | Indicators |
|-------|------------|------------|
| Small | 1-2 | Single function/component change |
| Medium | 3-5 | Multiple related components |
| Large | 6+ | Cross-cutting concerns, architecture impact |

**Scale affects skill priority:**
- Larger scale → process/documentation skills more important
- Smaller scale → implementation skills more focused

### 3. Identify Task Type

| Type | Characteristics | Key Skills |
|------|-----------------|------------|
| Implementation | New code, features | coding-principles, testing-principles |
| Fix | Bug resolution | ai-development-guide, testing-principles |
| Refactoring | Structure improvement | coding-principles, ai-development-guide |
| Design | Architecture decisions | documentation-criteria, implementation-approach |
| Quality | Testing, review | testing-principles, integration-e2e-testing |

### 4. Tag-Based Skill Matching

Extract relevant tags from task description and match against skills-index.yaml:

```yaml
Task: "Implement user authentication with tests"
Extracted tags: [implementation, testing, security]
Matched skills:
  - coding-principles (implementation, security)
  - testing-principles (testing)
  - ai-development-guide (implementation)
```

### 5. Implicit Relationships

Consider hidden dependencies:

| Task Involves | Also Include |
|---------------|--------------|
| Error handling | debugging, testing |
| New features | design, implementation |