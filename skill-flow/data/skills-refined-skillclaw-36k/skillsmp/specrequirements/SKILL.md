---
name: spec:requirements
description: Create Requirements Document - generates a structured requirements document based on the task context and project
---

# Create Requirements Document

Creates a requirements document based on the task context and project. The user provides a spec name and task description, and this command generates a structured requirements document.

## When to use

Use this skill when the user needs to:
- Create a new feature specification
- Document requirements for a task
- Generate a structured requirements document for planning

## Instructions

### Step 1: Gather Information

If the user hasn't provided sufficient context, ask them:
1. What is the name for this specification? (used for folder name, e.g., "user-authentication", "payment-integration")
2. What is the main goal or purpose of this feature/task?
3. What are the key user stories or use cases?
4. Are there any specific technical constraints or requirements?

### Step 2: Analyze the Codebase

Before writing requirements:
1. Explore the relevant parts of the codebase to understand existing patterns
2. Identify related services, components, or modules
3. Note any dependencies or integrations that will be affected

### Step 3: Create the Requirements Document

Create the document at `.specs/<spec-name>/requirements.md` with this structure:

```markdown
# Requirements Document

## Introduction

[Brief description of what this feature/task aims to achieve and why it's needed]

## Glossary

[Define key terms used throughout the document, formatted as:]
- **Term**: Definition

## Requirements

### Requirement 1: [Requirement Name]

**User Story:** As a [role], I want [feature] so that [benefit].

#### Acceptance Criteria

1. THE [Component] SHALL [action/behavior]
2. WHEN [condition] THEN [Component] SHALL [action/behavior]
3. THE [Component] SHALL NOT [prohibited action]

[Continue with additional requirements following the same pattern]
```

### Writing Guidelines

1. **Use SHALL for mandatory requirements** - "THE system SHALL..."
2. **Use WHEN-THEN for conditional behavior** - "WHEN user clicks submit THEN system SHALL..."
3. **Use SHALL NOT for prohibitions** - "THE system SHALL NOT expose..."
4. **Be specific and testable** - Each criterion should be verifiable
5. **Reference existing code patterns** - Align with project conventions
6. **Keep requirements atomic** - One requirement per item

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the requirements
3. Ask if they want to make any changes

## Arguments

This skill accepts an optional argument:
- `<args>` - Can include the spec name and/or description. Parse it to extract:
  - Spec name (kebab-case, e.g., "user-auth" or "payment-flow")
  - Task description or context

If `<args>` is provided, use it to determine the spec name and context. If not sufficient, ask the user for clarification.
