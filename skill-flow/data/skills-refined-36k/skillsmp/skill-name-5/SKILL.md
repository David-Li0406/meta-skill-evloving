---
name: skill-name
description: Description of what the skill does and when to use it
---

<!-- # Skill Instructions -->

<!-- 
Your detailed instructions, guidelines, and examples go here...

Body
The skill body contains the instructions, guidelines, and examples that Copilot should follow when using this skill. Write clear, specific instructions that describe:

What the skill helps accomplish
When to use the skill
Step-by-step procedures to follow
Examples of the expected input and output
References to any included scripts or resources
You can reference files within the skill directory using relative paths. For example, to reference a script in your skill directory, use [test script](./test-template.js).

Example skills -->

# Web Application Testing with Playwright

This skill helps you create and run browser-based tests for web applications using Playwright.

## When to use this skill

Use this skill when you need to:
- Create new Playwright tests for web applications
- Debug failing browser tests
- Set up test infrastructure for a new project

## Creating tests

1. Review the [test template](./test-template.js) for the standard test structure
2. Identify the user flow to test
3. Create a new test file in the `tests/` directory
4. Use Playwright's locators to find elements (prefer role-based selectors)
5. Add assertions to verify expected behavior

## Running tests

To run tests locally:
```bash
npx playwright test
```

To debug tests:
```bash
npx playwright test --debug
```

## Best practices

- Use data-testid attributes for dynamic content
- Keep tests independent and atomic
- Use Page Object Model for complex pages
- Take screenshots on failure