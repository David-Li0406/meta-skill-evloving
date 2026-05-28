---
name: gherkin-scenarios
description: Use this skill when you need to write behavior-driven development (BDD) scenarios in Gherkin format, ensuring clarity for both technical and non-technical stakeholders.
---

# Skill body

## Purpose
Write behavior scenarios in Gherkin format using Given/When/Then syntax for behavior-driven development (BDD) and test specifications.

## When to Use This Skill
- When asked to "write scenarios", "create features", "add Given/When/Then", or "write BDD specs".
- Documenting expected behavior, acceptance criteria, or test cases in a human-readable format.
- Creating scenario-driven tests for various applications.

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

#### Feature
**Purpose:** High-level description of a software feature or module capability.

**Format:**
```gherkin
Feature: Name of the feature
  Optional free-form description
  that can span multiple lines
```

## Workflow for Writing Scenarios

### Step 1: Understand the Requirement
- Parse the requirement to identify user behavior, business rules, and acceptance criteria.

### Step 2: Identify Scenarios
- Create scenarios for:
  1. Happy path
  2. Business rules
  3. Error cases
  4. Edge cases

### Step 3: Determine Feature File Location
- Follow BDD framework conventions for file organization.

### Step 4: Write Feature File in Gherkin
- Use the provided template to structure your scenarios clearly.

## Example
```gherkin
Feature: User Login

  Background:
    Given a user with valid credentials

  Scenario: Successful login
    When the user logs in
    Then they should be redirected to the dashboard

  Scenario: Login fails with invalid email
    Given the user enters an invalid email
    When they attempt to log in
    Then an error message should be displayed
```