---
name: generating-end-to-end-tests
description: Use this skill when you need to create end-to-end tests for web applications, automating browser interactions to validate user workflows.
---

# Skill body

## Overview

This skill automates the creation of end-to-end tests, simulating real user interactions with a web application. By generating tests using Playwright, Cypress, or Selenium, it ensures comprehensive coverage of critical user workflows.

## How It Works

1. **Identify User Workflow**: Analyze the user's request to determine the specific user workflow to be tested (e.g., user registration, product checkout).
2. **Generate Test Script**: Based on the identified workflow, generate a test script using Playwright, Cypress, or Selenium. The script includes steps to navigate the web application, interact with elements, and assert expected outcomes.
3. **Configure Test Environment**: Configure the test environment, including browser selection (Chrome, Firefox, Safari, Edge) and any necessary dependencies.

## When to Use This Skill

This skill activates when you need to:
- Create end-to-end tests for a specific user flow (e.g., "create E2E tests for user login").
- Generate browser-based tests for a web application.
- Automate testing of multi-step processes in a web application (e.g., "generate end-to-end tests for adding an item to a shopping cart and completing the checkout process").

## Examples

### Example 1: Testing User Registration

User request: "Create E2E tests for the user registration workflow on my website."

The skill will:
1. Generate a Playwright script that automates the user registration process, including filling out the registration form, submitting it, and verifying the successful registration message.
2. Configure the test to run in Chrome and Firefox.

### Example 2: Testing Shopping Cart Functionality

User request: "Generate end-to-end tests for adding an item to a shopping cart and completing the checkout process."

The skill will:
1. Generate a test script that automates the process of adding an item to the cart, proceeding to checkout, and verifying the order confirmation.
2. Configure the test to run across multiple browsers.