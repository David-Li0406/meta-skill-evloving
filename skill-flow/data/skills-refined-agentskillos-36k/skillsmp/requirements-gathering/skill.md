---
name: requirements-gathering
description: (opencode-project - Skill) Template and guidelines for creating comprehensive requirements specifications
---

# Requirements Gathering Skill

Use this skill when creating requirements specifications for new features. This follows the Kiro spec-driven development format with EARS (Easy Approach to Requirements Syntax) acceptance criteria.

## Directory Structure

Each feature gets its own directory under `specs/`:

```
specs/
├── <feature-name>/
│   ├── requirements.md    # This document
│   ├── design.md          # Technical design (created by /dev/design)
│   └── tasks.md           # Implementation tasks (created by /dev/tasks)
```

**Feature Name Format (CRITICAL)**: Feature names MUST be lowercase with dashes (kebab-case):
- ✅ `user-authentication`
- ✅ `api-rate-limiting`
- ✅ `budget-owner-implementation`
- ❌ `User Authentication`
- ❌ `API_Rate_Limiting`
- ❌ `BudgetOwnerImplementation`

## Requirements Document Template

Create the document at `specs/<feature-name>/requirements.md` with this structure:

```markdown
# Requirements Document: <Feature Name>

## Introduction

<2-4 paragraph description of the feature, its purpose, and why it is critical. Include context about where this fits in the overall system.>

## Glossary

Define key terms used throughout this specification. Use underscores in term names for clarity.

- **Term_One**: <Definition of the first key term>
- **Term_Two**: <Definition of the second key term>
- **Term_Three**: <Definition of the third key term>

## Requirements

### Requirement 1: <Requirement Title>

**User Story:** As a <user type>, I want <goal>, so that <benefit>.

#### Acceptance Criteria

Use EARS (Easy Approach to Requirements Syntax) format for acceptance criteria:

1. WHEN <trigger condition>, THE System SHALL <expected behavior>
2. WHEN <trigger condition>, THE System SHALL <expected behavior>
3. THE <Component> SHALL <constraint or capability>
4. IF <condition>, THE System SHALL <behavior>
5. WHILE <state>, THE System SHALL <maintain behavior>

### Requirement 2: <Requirement Title>

**User Story:** As a <user type>, I want <goal>, so that <benefit>.

#### Acceptance Criteria

1. WHEN <trigger condition>, THE System SHALL <expected behavior>
2. WHEN <trigger condition>, THE System SHALL <expected behavior>

### Requirement 3: <Requirement Title>
...

```

## EARS Syntax Patterns

Use these patterns for acceptance criteria:

| Pattern | Template | Example |
|---------|----------|---------|
| **Ubiquitous** | THE \<system\> SHALL \<requirement\> | THE System SHALL log all API requests |
| **Event-Driven** | WHEN \<trigger\>, THE \<system\> SHALL \<response\> | WHEN a user submits a form, THE System SHALL validate all fields |
| **State-Driven** | WHILE \<state\>, THE \<system\> SHALL \<behavior\> | WHILE in maintenance mode, THE System SHALL reject new connections |
| **Optional** | WHERE \<feature\> is enabled, THE \<system\> SHALL \<behavior\> | WHERE audit logging is enabled, THE System SHALL record timestamps |
| **Unwanted** | IF \<condition\>, THE \<system\> SHALL \<response\> | IF database connection fails, THE System SHALL retry 3 times |
| **Complex** | WHEN \<trigger\> AND WHILE \<state\>, THE \<system\> SHALL | WHEN timeout occurs AND WHILE processing, THE System SHALL rollback |

## Best Practices

1. **Start with Introduction**: Provide 2-4 paragraphs of context before diving into requirements
2. **Define Glossary**: Define ALL domain-specific terms before using them
3. **Use EARS Format**: Every acceptance criterion follows EARS syntax (WHEN/THE/SHALL)
4. **Be Specific**: Avoid vague terms like "fast" or "user-friendly" - quantify when possible
5. **Be Testable**: Every criterion should have clear pass/fail conditions
6. **Number Criteria**: Number acceptance criteria for easy reference (1.1, 1.2, etc.)
7. **Reference Glossary Terms**: Use defined terms consistently (with underscores: `Budget_Owner`)

## Acceptance Criteria Quality Checklist

Before finalizing, verify each acceptance criterion:

- [ ] Uses EARS format (WHEN/WHILE/IF + THE System SHALL)
- [ ] Is testable with clear pass/fail
- [ ] References glossary terms correctly
- [ ] Is atomic (tests one thing)
- [ ] Is traceable to a user story

## Example: Budget Owner Requirements (Reference)

See `.kiro/specs/budget-owner-implementation/requirements.md` for a comprehensive example of this format in action.

## Questions to Ask When Gathering Requirements

When gathering requirements, consider:
- Who are the users of this feature?
- What problem does this solve?
- What does success look like?
- What are the constraints (time, tech, etc.)?
- How does this integrate with existing features?
- What could go wrong?
- What domain terms need to be defined?
