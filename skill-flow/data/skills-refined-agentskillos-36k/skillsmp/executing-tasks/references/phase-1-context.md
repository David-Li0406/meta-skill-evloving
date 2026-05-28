---
title: Phase 1 - Context Gathering
description: Context gathering strategies by task type, caching rules, and skill loading patterns for task execution workflow
keywords: context, gathering, skills, dependencies, task-type
file-type: reference
skill: executing-tasks
---

# Phase 1: Context Gathering

## Context Strategies by Task Type

| Task Type | Required Context | Skills to Load |
|-----------|-----------------|----------------|
| Code implementation | story.md, design section, related code files | prime, engineering-context |
| Test writing | Implementation code, test patterns, coverage requirements | prime |
| Documentation | Code to document, existing docs structure | writing-ai-docs, maintaining-docs |
| Refactoring | Affected code paths, existing tests | prime, check-implementation |
| Bug fix | Issue description, reproduction steps, related code | prime |
| Configuration | System requirements, environment details | prime |

## Context Caching Rules

**Cache for session duration:**
- Project architecture (from prime skill)
- Story specification and design
- Gherkin scenarios for current task

**Refresh per task:**
- Current file states (always re-read before editing)
- Test results (run fresh)
- PROGRESS.yaml status

**Never cache:**
- External API responses
- Git status (changes between operations)

## Skill Loading Patterns

```
# Always load project context first
Skill(command='prime')

# Then load task-specific skills based on work type
if code_implementation:
    Skill(command='engineering-context')
elif documentation:
    Skill(command='writing-ai-docs')
elif review_needed:
    Skill(command='check-implementation')
```

## Context Gathering Checklist

- [ ] Load prime skill for project architecture
- [ ] Read story.md or task specification
- [ ] Identify affected code files
- [ ] Check existing tests for affected areas
- [ ] Review PROGRESS.yaml for task dependencies
- [ ] Load task-type-specific skills
