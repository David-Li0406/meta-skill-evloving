@feature-tag
Feature: Feature Name
  As a user role
  I want to goal/action
  So that benefit/value

  Background:
    Given I am on the home page

  # ✅ Behavior-focused, test data in step definitions
  @smoke
  Scenario: Successful login
    Given I am on the login page
    When I login with valid credentials
    Then I should be logged in

  # ✅ Generic error assertion
  @negative
  Scenario: Login fails with invalid credentials
    Given I am on the login page
    When I login with invalid credentials
    Then I should see a login error

  # ✅ Parameterize when exact copy IS the requirement
  @negative @compliance
  Scenario: Error message meets compliance requirements
    Given I am on the login page
    When I login with invalid credentials
    Then the error message should be "Invalid email or password"

  # ✅ Parameterize when role affects behavior
  @data-driven
  Scenario Outline: Role-based access
    Given I am logged in as <role>
    When I navigate to the admin panel
    Then I should <result>

    Examples:
      | role  | result              |
      | admin | see the admin panel |
      | user  | see access denied   |
