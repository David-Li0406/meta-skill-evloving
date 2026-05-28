---
name: bdd-and-gherkin-scenarios
description: Use this skill to guide developers through the Behavior-Driven Development (BDD) workflow and to write Gherkin scenarios in Given/When/Then format for acceptance tests and specifications.
---

# BDD and Gherkin Scenarios

This skill combines guidance for the Behavior-Driven Development (BDD) workflow with the ability to write Gherkin scenarios using Given/When/Then syntax. It is designed to help developers create clear, business-readable specifications and acceptance criteria.

## Purpose

This skill assists developers in:
- Conducting Discovery sessions to explore requirements.
- Writing effective Gherkin scenarios in Given-When-Then format.
- Creating reusable step definitions.
- Integrating BDD with TDD for implementation.
- Maintaining living documentation.

## When to Use This Skill

- When asked to "write scenarios", "create features", "add Given/When/Then", or "write BDD specs".
- Documenting expected behavior for user stories, acceptance criteria, or test cases.
- Creating scenario-driven tests for various applications.

## BDD Workflow Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 DISCOVERY Phase                                              │
│  □ Stakeholders identified (Business, Dev, QA)                  │
│  □ User story discussed and understood                          │
│  □ Concrete examples collected (Example Mapping)                │
│  □ Edge cases identified                                        │
│  □ Questions answered or noted for follow-up                    │
├─────────────────────────────────────────────────────────────────┤
│  📝 FORMULATION Phase                                            │
│  □ Scenarios use correct Gherkin syntax                         │
│  □ Scenarios are declarative (WHAT, not HOW)                    │
│  □ Business language used (no technical jargon)                 │
│  □ Each scenario is independent and self-contained              │
│  □ Scenarios have 5-10 steps maximum                            │
│  □ Scenarios reviewed by stakeholders                           │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ AUTOMATION Phase                                             │
│  □ Step definitions created for all steps                       │
│  □ Step definitions are reusable                                │
│  □ Scenarios fail initially (RED)                               │
│  □ TDD used for unit-level implementations                      │
│  □ All scenarios pass (GREEN)                                   │
│  □ Code refactored and clean                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Gherkin File Structure

### Feature File Format

```gherkin
Feature: Brief description of the feature

  Background:
    Given common setup steps
    And shared preconditions

  Scenario: Description of specific scenario
    Given a precondition
    When an action occurs
    Then expect this outcome
```

### Keywords and Structure

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Feature` | High-level description of a software feature | `Feature: User Login` |
| `Scenario` | Single test case | `Scenario: Successful login` |
| `Given` | Set up initial context | `Given I am on the login page` |
| `When` | Trigger action | `When I enter valid credentials` |
| `Then` | Assert outcome | `Then I should see my dashboard` |
| `And`/`But` | Continue previous | `And I should see a welcome message` |
| `Background` | Common setup | Runs before each scenario |
| `Scenario Outline` | Data-driven | Template with Examples table |

## Writing Scenarios

### Step 1: Understand the Requirement

- Parse the requirement to identify user behavior, business rules, and acceptance criteria.

### Step 2: Identify Scenarios

Create scenarios for:
1. **Happy path** - User achieves goal successfully.
2. **Business rules** - Each business rule gets at least one scenario.
3. **Error cases** - User makes mistakes, sees helpful errors.
4. **Edge cases** - Boundary conditions.

### Step 3: Write Feature File in Gherkin

**Template**:

```gherkin
Feature: User Login
  As a registered user
  I want to log in with my email and password
  So that I can access my account

  Background:
    Given the application is running
    And I am on the login page

  Scenario: Successful login with valid credentials
    Given I am a registered user with email "user@example.com"
    And my password is "SecurePassword123!"
    When I enter email "user@example.com"
    And I enter password "SecurePassword123!"
    Then I should see "Welcome back"
```

## Best Practices

1. **Write Declarative Steps**: Focus on what happens, not how.
2. **One Scenario = One Behavior**: Keep scenarios focused.
3. **Use Background for Common Setup**: Avoid repetition.
4. **Keep Scenarios Focused and Short**: Aim for 3-7 steps per scenario.
5. **Use Meaningful Scenario Titles**: Clearly describe the scenario's intent.

## Validation

**Good Scenario Checklist**:
- [ ] Has descriptive title
- [ ] Uses Given (setup), When (action), Then (verify)
- [ ] Tests one specific behavior
- [ ] Written in business language
- [ ] Avoids implementation details
- [ ] Could be understood by non-technical stakeholders

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scenarios too long | Split into multiple scenarios, use Background |
| Too much repetition | Use Scenario Outline with Examples |
| Too technical | Focus on behavior, not implementation |
| Unclear intent | Add feature description, use descriptive titles |

## References

- **Gherkin Reference**: <https://cucumber.io/docs/gherkin/reference/>
- **Gherkin Best Practices**: <https://cucumber.io/docs/bdd/>
- **Given/When/Then Guide**: <https://martinfowler.com/bliki/GivenWhenThen.html>

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)