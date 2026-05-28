---
name: aico-pm-acceptance-criteria
description: Use this skill when you need to define clear, testable acceptance criteria for user stories using the Given/When/Then (Gherkin) format.
---

# Acceptance Criteria

## ⚠️ CRITICAL RULES - READ FIRST

1. **READ STORY FIRST**: Always read the story file from `docs/reference/pm/stories/` before writing criteria.
2. **USE GIVEN/WHEN/THEN**: All criteria must follow this format.
3. **UPDATE STORY FILE**: Add criteria to existing story file, don't create new files.

## Language Configuration

Before generating any content, check `aico.json` in project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Review story/feature**: Understand what needs to be done.
2. **Identify success scenarios**: Focus on happy paths first.
3. **Write Given/When/Then**: For each scenario.
4. **Add edge cases**: Include boundary conditions and errors.
5. **Verify testability**: Ensure each criterion is independently verifiable.

## Acceptance Criteria Template

```markdown
### Acceptance Criteria for [Story/Feature]

#### Scenario 1: [Scenario Name]

- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

#### Scenario 2: [Scenario Name]

- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

#### Edge Cases

- **Given** [edge case condition]
- **When** [action]
- **Then** [expected behavior]
```

## Criteria Categories

| Category       | Examples                    |
| -------------- | --------------------------- |
| Functional     | Feature works as specified  |
| Validation     | Input validation rules      |
| Error handling | Error messages and recovery |
| Performance    | Response time expectations  |
| Accessibility  | A11y requirements           |

## Quality Checklist

- [ ] Each criterion is independently testable.
- [ ] No ambiguous language ("should", "might", "could").
- [ ] Edge cases are covered.
- [ ] Error states are defined.
- [ ] Performance expectations stated (if relevant).

## Key Rules

- ALWAYS use Given/When/Then structure.
- MUST make each criterion independently testable.
- ALWAYS include edge cases and error scenarios.
- NEVER use vague language - be specific.

## Common Mistakes

- ❌ Vague criteria ("works correctly") → ✅ Specific conditions.
- ❌ Missing edge cases → Always include them.