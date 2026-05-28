# Gherkin Feature Examples

Well-structured feature files with behavior-focused scenarios.

## Authentication Feature

```gherkin
@auth
Feature: User Authentication
  As a registered user
  I want to log in to my account
  So that I can access personalized content

  Background:
    Given I am on the login page

  @smoke @critical
  Scenario: Successful login with valid credentials
    When I login with valid credentials
    Then I should be logged in

  @negative
  Scenario: Failed login shows generic error
    When I login with invalid credentials
    Then I should see a login error

  @validation
  Scenario: Form validation for empty fields
    When I submit the login form without credentials
    Then the email field should show a validation error

  @compliance @legal
  Scenario: Error message meets compliance requirements
    When I login with invalid credentials
    Then the error message should be "Invalid email or password"
```

## Role-Based Access Feature

```gherkin
@authorization @roles
Feature: Role-Based Access Control
  As a system administrator
  I want to restrict access based on user roles
  So that sensitive functions are protected

  @data-driven
  Scenario Outline: Access control for admin page
    Given I am logged in as <role>
    When I visit the admin page
    Then I should <result>

    Examples:
      | role  | result              |
      | admin | see the admin panel |
      | valid | see access denied   |
```

## Tag Reference

| Tag | Purpose |
|-----|---------|
| `@smoke` | Critical path tests |
| `@negative` | Error scenarios |
| `@validation` | Input validation |
| `@compliance` | Required text/copy |
| `@data-driven` | Scenario outlines |
| `@wip` | Work in progress |
