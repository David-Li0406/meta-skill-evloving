---
title: Phase 2 - Planning
description: TodoWrite patterns, task granularity guidelines, and dependency handling for task execution planning phase
keywords: planning, todowrite, granularity, dependencies, breakdown
file-type: reference
skill: executing-tasks
---

# Phase 2: Planning

## TodoWrite Patterns

**Standard task structure:**
```javascript
TodoWrite([
  {
    id: "task-prefix-001",
    content: "Clear action description with success criteria",
    status: "pending",
    priority: "high|medium|low"
  }
]);
```

**Naming conventions:**
- Use task ID prefix from story (e.g., `T-001-setup`, `T-001-impl`, `T-001-test`)
- Sequential numbering within task
- Suffix indicates work type: `-setup`, `-impl`, `-test`, `-doc`

## Task Granularity

| Duration | Appropriate For |
|----------|-----------------|
| 5-15 min | Single function, config change, small fix |
| 15-30 min | Feature component, test suite for module |
| 30-60 min | Complex integration, major refactor section |
| >60 min | Split into smaller tasks |

**Granularity rules:**
- Target 15-30 min per todo item
- Each item = one atomic commit opportunity
- Larger items indicate need for decomposition
- Smaller items can be grouped for efficiency

## Dependency Handling

**Dependency types:**
| Type | TodoWrite Approach |
|------|-------------------|
| Sequential | Order items, mark later items blocked |
| Parallel | No dependencies, can execute simultaneously |
| External | Document blocker, skip in planning |

**Dependency notation:**
```javascript
{
  id: "T-001-api",
  content: "Implement API endpoint",
  status: "pending",
  priority: "high"
},
{
  id: "T-001-test",
  content: "Write API tests (depends: T-001-api)",
  status: "pending",
  priority: "medium"
}
```

## Planning Checklist

- [ ] Break task into 15-30 min items
- [ ] Identify parallelizable work
- [ ] Note dependencies in content field
- [ ] Assign priorities based on dependency chain
- [ ] Verify all story acceptance criteria covered
