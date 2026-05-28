---
name: gherkin-scenario-writing
description: Use this skill to create and write Gherkin scenarios using Given/When/Then syntax for behavior-driven development (BDD) and test specifications in pure business language.
---

# Gherkin Scenario Writing

Write behavior-driven development (BDD) scenarios using Gherkin syntax. Gherkin uses Given/When/Then steps to describe expected behavior in plain language that both technical and non-technical stakeholders can understand.

## When to Use This Skill

- User asks to "write scenarios", "create features", "add Given/When/Then", or "write BDD specs"
- Documenting expected behavior for software features or user stories
- Creating acceptance criteria for features
- Writing test specifications in human-readable format
- Converting requirements into executable specifications
- Documenting workflows or processes in structured format

## Gherkin File Structure

### Feature File Format

```gherkin
Feature: Brief description of the feature

  Optional longer description that provides
  more context about the feature.

  Background:
    Given common setup steps
    And shared preconditions

  Scenario: Description of specific scenario
    Given a precondition
    And another precondition
    When an action occurs
    And another action
    Then expect this outcome
    And expect another outcome

  Scenario Outline: Parameterized scenario
    Given a <parameter>
    When I perform <action>
    Then I expect <result>

    Examples:
      | parameter | action  | result  |
      | value1    | action1 | result1 |
      | value2    | action2 | result2 |
```

### Keywords and Structure

- **Feature**: High-level description of a software feature or module capability.
- **Background**: Common steps that run before each scenario in the feature.
- **Scenario**: Concrete example of business rule or acceptance criterion.
- **Given**: Set up the initial state/context for the scenario.
- **When**: Describe the key action/event in the scenario.
- **Then**: Describe the expected result or observable outcome.
- **And / But**: Additional steps of the same type (Given/When/Then).

### Scenario Outline (Parameterization)

**Purpose:** Run the same scenario with different input values.

```gherkin
Scenario Outline: Title with <placeholder>
  Given a <parameter>
  When I do <action>
  Then I expect <result>

  Examples:
    | parameter | action  | result  |
    | value1    | action1 | result1 |
    | value2    | action2 | result2 |
```

### Best Practices

1. **Write Declarative Steps (Not Imperative)**: Focus on what happens, not how.
2. **One Scenario = One Behavior**: Each scenario should test a single behavior.
3. **Use Background for Common Setup**: Avoid repeating setup steps across scenarios.
4. **Keep Scenarios Focused and Short**: Aim for 3-7 steps per scenario.
5. **Use Meaningful Scenario Titles**: Titles should clearly describe the scenario's intent.
6. **Avoid Technical Implementation Details**: Use business language that stakeholders can understand.

## Workflow for Writing Scenarios

### Step 1: Understand the Requirement

- Parse the requirement to identify user behavior, business rules, and acceptance criteria.

### Step 2: Identify Scenarios

- Create scenarios for happy paths, business rules, error cases, and edge cases.

### Step 3: Write Feature File in Gherkin

- Use the provided template to structure your scenarios in Gherkin format.

### Step 4: Validate Business Language

- Ensure that all scenarios are written in pure business language without technical jargon.

### Step 5: Run Scenarios

- Execute the scenarios in your BDD framework to check for undefined steps.

### Step 6: Commit Scenarios

- Create a commit with a clear message about the scenarios added.

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

## Quick Start

1. Identify the feature and write a feature description.
2. List scenarios based on user behavior and acceptance criteria.
3. Write scenarios in Gherkin format using the Given/When/Then structure.
4. Validate the language and clarity of each scenario.
5. Store the feature files in the appropriate directory.