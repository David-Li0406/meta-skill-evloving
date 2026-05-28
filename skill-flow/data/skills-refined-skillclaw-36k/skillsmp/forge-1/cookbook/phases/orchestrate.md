# Orchestrate Phase Guide

**Purpose**: Planning - How do you break this into pieces?

## Key Question

Do you have a complete list of tasks in order, each small enough for one AI session, where you can trace how pieces connect to form the whole?

## Required Outputs

1. **Container Architecture** - C4 Level 2 (deployable units)
2. **Component Architecture** - C4 Level 3 (internal structure)
3. **Dependency Map** - What must exist before what
4. **Task List** - Session-sized work items

## C4 Level 2: Containers

Shows deployable/runnable units:
- Web applications, APIs, databases
- Mobile apps, CLI tools
- Message queues, file systems

## C4 Level 3: Components

Shows internal structure of each container:
- Controllers, services, repositories
- Modules, packages, classes
- How they interact

## Task Sizing

A task is the right size when:
- Completable in one AI conversation
- Has clear inputs and outputs
- Can be tested independently
- Doesn't require holding too much context

## Dependency Mapping

For each task, identify:
- What must exist before starting (prerequisites)
- What it produces that others need (outputs)
- Whether it can run in parallel with other tasks

## Completion Checklist

- [ ] Container architecture designed
- [ ] Component architecture designed
- [ ] Dependencies mapped
- [ ] Tasks sized for single sessions
- [ ] Build order established

## Common Mistakes

- Tasks too large (spanning multiple sessions)
- Missing dependencies (getting stuck mid-implementation)
- No clear interfaces between components
- Parallel work that actually has hidden dependencies

## Next Phase

When Orchestrate is complete, advance to **Refine** where you'll define exactly what "done" looks like for each task.
