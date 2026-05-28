# Chore Plan Reference

## Planning Approach

Chore plans focus on maintenance tasks that improve code quality, update dependencies, or perform housekeeping without adding new functionality. The goal is clear scope definition and methodical execution.

## Key Sections

A chore plan should include:

1. **Description**: What needs to be done and why
2. **Scope**: What is in scope and explicitly out of scope
3. **Tasks**: Specific implementation tasks in execution order
4. **Validation Criteria**: How to verify the chore is complete

## Common Chore Types

- **Dependency Updates**: Upgrading packages, handling breaking changes
- **Refactoring**: Improving code structure without changing behavior
- **Configuration**: Updating build configs, CI/CD pipelines, tooling
- **Cleanup**: Removing dead code, fixing warnings, organizing files
- **Documentation**: Updating outdated docs, adding missing docs
- **Migration**: Moving to new patterns, APIs, or technologies

## Scope Definition

Clear scope prevents scope creep:

- List specific files, directories, or components in scope
- Explicitly state what is NOT in scope
- Define boundaries for the change
- Note any related work that should be done separately

## Task Ordering

Order tasks for safe, incremental progress:

1. Preparation tasks (backups, feature flags, etc.)
2. Core changes in dependency order
3. Cleanup and verification tasks
4. Documentation updates

## Risk Mitigation

For chores that could break things:

- Identify rollback strategies
- Plan for incremental changes that can be tested
- Note any feature flags or gradual rollout needs
- Consider timing (avoid high-traffic periods)

## Milestone Patterns

Typically 1-2 milestones per chore. Common patterns:

1. **Implementation**: Execute the main tasks
2. **Verification**: Validate changes, update docs (if needed)

For larger chores, break into logical phases based on scope boundaries.

## Template

```markdown
# Chore: {{chore_title}}

## Progress

### Implementation

{{implementation_checklist}}

### Validation

{{validation_checklist}}

## Description

{{description}}

## Scope

{{scope}}

## Milestones

### Milestone {{milestone_number}}: {{milestone_title}}

{{milestone_description}}

#### Task {{milestone_number}}.{{task_number}}: {{task_title}}

{{task_description}}

## Validation Criteria

{{validation_criteria}}
```

<!--
Type-specific placeholders (see SKILL.md for common milestone/task placeholders):
- {{chore_title}}: Concise title for the chore (e.g., "Update All Dependencies")
- {{description}}: Brief explanation of what needs to be done and why
- {{scope}}: What is in scope and out of scope (use bullet points)
- {{validation_criteria}}: Checklist to verify completion
-->
