---
name: rule-creator
description: Use this skill when users want to create, update, or manage rules that customize AI behavior for their projects or personal preferences.
---

# Rule Creator

Create effective user rules that customize AI behavior for projects and personal preferences.

## What Are User Rules?

User rules are custom instructions that modify how the AI assistant behaves. They can define:

- **Coding standards** - Style, patterns, and conventions
- **Language preferences** - Response language, terminology
- **Project configuration** - Framework choices, file structure
- **Workflow guidelines** - Git, testing, documentation practices

## Rule Creation Workflow

### Step 1: Identify Rule Purpose

Ask the user:
1. What behavior do you want to modify?
2. Is this a project rule (shared) or personal preference?
3. Are there exceptions to this rule?

### Step 2: Choose Rule Category

Common categories:
- `coding-style` - Code formatting, syntax preferences
- `language` - Response language, communication style
- `project` - Framework-specific, architecture decisions
- `git` - Commit messages, branching, PR guidelines
- `naming` - Variable, function, file naming conventions
- `security` - Authentication, secrets, input validation
- `testing` - Test coverage, naming, mocking practices
- `documentation` - Comments, README, JSDoc requirements

### Step 3: Write the Rule

Follow these principles:

1. **Be specific** - Use concrete examples.
2. **Be actionable** - Provide clear instructions, not vague guidance.
3. **Include examples** - Show correct usage.
4. **Define exceptions** - Specify when the rule doesn't apply.

### Step 4: Format the Rule

Use this format:

```
## [Category]: [Short Title]

[Clear instruction in imperative form]

Example:
[Code or text example showing correct usage]

Exception: [When this rule doesn't apply, if any]
```

### Step 5: Validate the Rule

Check against this list:
- [ ] Clear and unambiguous?
- [ ] Specific context defined?
- [ ] Actionable instruction?
- [ ] Example included (if complex)?
- [ ] Exceptions documented?
- [ ] No conflicts with existing rules?

## Quick Templates

### Coding Style Rule

```
## Coding: [Title]

[What to do and how to do it]
```