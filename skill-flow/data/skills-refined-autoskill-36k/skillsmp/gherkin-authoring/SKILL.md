---
name: gherkin-authoring
description: Expert in authoring Gherkin-compliant behavior specifications (Given, When, Then). Use when defining executable scenarios for feature specifications or acceptance tests.
---

# Gherkin Scenario Authoring

## What is it?

This skill provides expertise in writing **executable behavior specifications** using Gherkin syntax. It translates user requirements into structured, unambiguous scenarios that serve as both documentation and automated tests.

## Why use it?

- **Eliminate Ambiguity**: Forced structure (Given/When/Then) clarifies expectations.
- **Executable Documentation**: Scenarios can be verified automatically by tools like Cucumber.
- **Shared Language**: Simple keywords allow product, engineering, and non-technical stakeholders to collaborate on the same artifact.

## How to use it?

### Step 1: Define the Feature Context

Start with the `Feature:` keyword to group related scenarios. Use `Rule:` to represent specific business logic if needed.

### Step 2: Establish Preconditions (Given)

Use `Given` to describe the initial state of the system. Avoid user interactions here; focus on system state (e.g., "Given the user is logged in").

### Step 3: Describe the Action (When)

Use `When` to describe the trigger or event (e.g., "When the user clicks 'Submit'").

### Step 4: Define the Outcome (Then)

Use `Then` to describe the observable result (e.g., "Then the confirmation message is displayed"). Use assertions (e.g., "should", "must") implicitly or explicitly.

### Step 5: Leverage Advanced Keywords

- Use `Background:` for common preconditions.
- Use `Scenario Outline:` and `Examples:` for testing multiple data variations.
- Use `Doc Strings` (triple quotes) or `Data Tables` for complex inputs.

## Examples

### Scenario Outline: User Authentication

```gherkin
Feature: User Login

  Scenario Outline: Successful login with valid credentials
    Given the login page is open
    When I enter "<username>" and "<password>"
    And I click "Login"
    Then I should be redirected to the "<target_page>"

    Examples:
      | username | password | target_page |
      | admin    | secret12 | dashboard   |
      | user     | pass456  | home        |
```

## Supporting References

- [GHERKIN_REFERENCE.md](references/GHERKIN_REFERENCE.md) - Detailed Gherkin keyword documentation.

## Limitations

- **Syntactic Only**: This skill helps authoring but does not execute tests or verify step definitions.
- **Abstraction Level**: Avoid tying scenarios too closely to UI implementation details (e.g., use "login" instead of "click the blue button at the top right").
