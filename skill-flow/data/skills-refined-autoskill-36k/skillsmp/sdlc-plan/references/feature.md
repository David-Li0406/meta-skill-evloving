# Feature Plan Reference

## Planning Approach

Feature plans focus on comprehensive design with incremental delivery. Each milestone should be independently valuable and testable. Architecture decisions should align with existing codebase patterns.

## Key Sections

A feature plan should include:

1. **Overview**: What the feature does and why it's valuable
2. **Requirements**: Functional and non-functional requirements
3. **Architecture**: High-level design and patterns to use
4. **Milestones**: Logical breakdown with tasks
5. **Testing Strategy**: How the feature will be tested
6. **Validation Criteria**: How to verify the feature is complete

## Requirements Gathering

Capture both types of requirements:

**Functional Requirements**:

- What the feature should do
- User interactions and flows
- Input/output specifications
- Edge cases and error handling

**Non-Functional Requirements**:

- Performance expectations
- Security considerations
- Scalability needs
- Accessibility requirements
- Compatibility constraints

## Architecture Considerations

When designing the feature:

- Study existing patterns in the codebase
- Identify integration points with existing code
- Define data models and API contracts
- Consider component reusability
- Plan for extensibility without over-engineering
- Document key technical decisions

## Milestone Patterns

Typically 2-5 milestones per feature. Common patterns:

1. Core infrastructure/data models
2. Basic functionality (happy path)
3. Edge cases and error handling
4. Polish and optimization
5. Documentation and cleanup

## Task Decomposition

Within each milestone:

- Tasks should be specific and actionable
- Include file paths where changes are needed
- Consider testing tasks alongside implementation
- Note any dependencies between tasks

## Testing Strategy

Plan testing at multiple levels:

- **Unit Tests**: Individual functions and components
- **Integration Tests**: Component interactions
- **E2E Tests**: Full user flows
- **Manual Testing**: Exploratory and edge cases

## Template

```markdown
# Feature: {{feature_title}}

## Progress

### Implementation

{{implementation_checklist}}

### Validation

{{validation_checklist}}

## Overview

{{overview}}

## Requirements

{{requirements}}

## Architecture

{{architecture}}

## Milestones

### Milestone {{milestone_number}}: {{milestone_title}}

{{milestone_description}}

#### Task {{milestone_number}}.{{task_number}}: {{task_title}}

{{task_description}}

## Testing Strategy

{{testing_strategy}}

## Validation Criteria

{{validation_criteria}}
```

<!--
Type-specific placeholders (see SKILL.md for common milestone/task placeholders):
- {{feature_title}}: Concise title for the feature (e.g., "User Authentication with OAuth")
- {{overview}}: What this feature does and why it's valuable (2-4 sentences)
- {{requirements}}: Functional and non-functional requirements (use subsections)
- {{architecture}}: High-level design decisions and patterns
- {{testing_strategy}}: How the feature will be tested at each level
- {{validation_criteria}}: Checklist to verify feature completion
-->
