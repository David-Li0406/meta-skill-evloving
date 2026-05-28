# Gherkin Reference

Gherkin uses a set of special keywords to give structure and meaning to executable specifications.

## Primary Keywords

- **Feature**: Provides a high-level description of a software feature and groups related scenarios.
- **Rule**: Represents one business rule that should be implemented. Groups several scenarios belonging to this rule.
- **Example / Scenario**: A concrete example that illustrates a business rule. Consists of a list of steps.
- **Given**: Describes the initial context of the system (preconditions).
- **When**: Describes an event or action (interaction).
- **Then**: Describes an expected outcome or result (assertion).
- **And, But**: Used to chain steps together fluidly.
- **Background**: Allows you to add context to the scenarios that follow it (common Given steps).
- **Scenario Outline**: Runs the same Scenario multiple times with different combinations of values.
- **Examples**: Table section for Scenario Outlines containing variable data.

## Secondary Keywords & Syntax

- **""" (Doc Strings)**: Multi-line text for passing large data.
- **| (Data Tables)**: Passes a list of values to a step definition.
- **@ (Tags)**: Used to group and filter features/scenarios.
- **# (Comments)**: Single-line comments starting with #.

## Best Practices

### Imagine it's 1922

Try hard to come up with examples that don't make any assumptions about technology or user interface. Implementation details should be hidden in step definitions.

### Descriptive Steps

Make steps clear and unambiguous.
*Bad*: `Then there is money in my account`
*Good*: `Then my account should have a balance of £430`

### Observable Outcomes

Only verify outcomes observable to the user (e.g., UI changes, reports), not internal state like database records.

## Localisation

Gherkin supports over 70 languages using the `# language: [iso]` header.

## Formatting Example

```gherkin
Feature: Guess the word

  Background:
    Given the game is initialized

  Scenario Outline: Successful guess
    Given the Maker has started a game with the word "<word>"
    When the Breaker joins the Maker's game
    Then the Breaker must guess a word with <length> characters

    Examples:
      | word  | length |
      | silky | 5      |
      | apple | 5      |
```
