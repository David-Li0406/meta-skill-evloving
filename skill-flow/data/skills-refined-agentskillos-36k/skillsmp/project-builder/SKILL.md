---
name: Project Builder
description: Automatically analyze project plans and generate comprehensive task breakdowns. Use when user describes a project, feature set, or asks to build/implement something complex requiring multiple tasks.
allowed-tools: Read, Grep, Glob, TodoWrite
---

# Project Builder Skill

## Purpose
Transform high-level project plans into actionable, well-organized task breakdowns with proper phasing, dependencies, and assignments.

## Auto-Activation Triggers
This skill activates when the user:
- Describes a multi-step project or feature set
- Says "build a [complex feature]"
- Mentions implementing something requiring multiple components
- Asks to "create a project plan" or "break down this project"
- Uses phrases like "I want to build/create/implement [complex system]"

## Workflow Overview

### Phase 1: Plan Analysis
Extract from user's description:
- Core objectives and deliverables
- Technical requirements (API, database, frontend, auth, etc.)
- Complexity level (Low/Medium/High)
- Required project phases

### Phase 2: Agent Selection
Based on technical requirements, select appropriate work areas:
- **backend**: API, server, database work
- **frontend**: UI, components, user experience
- **security**: Authentication, authorization
- **testing**: Unit tests, integration, E2E
- **data**: Schema, migrations, pipelines
- **infrastructure**: Docker, deployment, CI/CD
- **performance**: Optimization, caching

### Phase 3: Task Generation
For each area, create tasks with:
- **Title**: Clear and actionable
- **Description**: Detailed context and acceptance criteria
- **Priority**: Critical/High/Medium/Low based on dependencies
- **Size**: XS/S/M/L/XL based on complexity
- **Phase**: Assignment based on dependencies
- **Dependencies**: Between tasks

**Context Integration:**
- Check `.claude/memory/` for existing patterns
- Apply specifications from `CLAUDE.md`
- Reference architecture documentation

### Phase 4: Compliance Review
Run comprehensive checks:
- All tasks have required fields
- Workload balanced
- No phase overloaded with critical tasks
- Dependencies properly sequenced

### Phase 5: Task Creation
Create tasks using TodoWrite or your task management system.

### Phase 6: Project Summary
Generate comprehensive overview:
- Task metrics and distribution
- Critical path identification
- Risk assessment
- Progress tracking setup

## Output Format

```markdown
## Project Builder

**Plan:** [user's project description]

### Analysis
- **Complexity:** [Low/Medium/High]
- **Technical Requirements:** [count]
- **Required Areas:** [list]

### Task Distribution
- Critical: [count] tasks
- High: [count] tasks
- Medium: [count] tasks
- Low: [count] tasks

### Phase Breakdown
- Phase 1: [name] - [count] tasks
- Phase 2: [name] - [count] tasks

### Compliance Review
- [ ] All tasks have required fields
- [ ] Workload balanced across areas
- [ ] Dependencies properly sequenced

### Tasks Created
[List of tasks with priorities]

### Next Steps
1. Review generated tasks
2. Adjust priorities based on needs
3. Begin Phase 1 critical tasks
```

## Best Practices

### 1. Memory-Driven Planning
**Always check memory first:**
- `.claude/memory/active/quick-reference.md` - Top patterns
- `.claude/memory/active/procedural-memory.md` - Proven procedures

### 2. Context Awareness
- Check existing tasks for capacity
- Review current workload
- Factor in technical debt backlog

### 3. Realistic Estimation
- Historical velocity from similar tasks
- Complexity multipliers
- Buffer for unknowns (15-20%)

### 4. Progressive Elaboration
- Phase 1: Core functionality
- Phase 2: Enhancement and polish
- Phase 3: Optimization and scaling
- Phase 4: Documentation and deployment

## Integration with Other Workflows

**After Project Building:**
- Use `/orchestrate-tasks` for parallel execution
- Track progress regularly

**Update Context:**
- Document project outcome in episodic memory
- Add new patterns to procedural memory

## Error Handling

### If Plan Unclear
1. Ask clarifying questions about scope
2. Request technical requirements specification
3. Suggest examples of well-structured plans

### If Complexity Estimation Fails
1. Default to Medium complexity
2. Request additional context
3. Conservative estimates with explicit assumptions

## Skill Metadata

**Version:** 1.0.0
**Category:** Project Management & Planning
