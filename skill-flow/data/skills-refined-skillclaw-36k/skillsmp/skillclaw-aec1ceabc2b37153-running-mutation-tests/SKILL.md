---
name: running-mutation-tests
description: Use this skill when you need to validate the effectiveness of a test suite through mutation testing, helping to identify weaknesses and improve test coverage.
---

# Skill body

## Overview

This skill empowers Claude to execute mutation testing, providing insights into the effectiveness of a test suite. By introducing small changes (mutations) into the code and running the tests, it determines if the tests are capable of detecting these changes. This helps identify weaknesses in the test suite and improve overall code quality.

## How It Works

1. **Mutation Generation**: The skill automatically introduces mutations (e.g., changing `+` to `-`) into the code.
2. **Test Execution**: The test suite is run against the mutated code.
3. **Result Analysis**: The skill analyzes which mutations were "killed" (detected by tests) and which "survived" (were not detected).
4. **Reporting**: A mutation score is calculated, and surviving mutants are identified for further investigation.

## When to Use This Skill

This skill activates when you need to:
- Validate the effectiveness of a test suite.
- Identify gaps in test coverage.
- Improve the mutation score of a project.
- Analyze surviving mutants to strengthen tests.

## Examples

### Example 1: Improving Test Coverage

User request: "Run mutation testing on the validator module and suggest improvements to the tests."

The skill will:
1. Execute mutation tests on the validator module.
2. Analyze the results and identify surviving mutants, indicating areas where tests are weak.
3. Suggest specific improvements to the tests based on the surviving mutants, such as adding new test cases or modifying existing ones.

### Example 2: Assessing Test Quality

User request: "What is the mutation score for the user authentication service?"

The skill will:
1. Execute mutation tests on the user authentication service.
2. Calculate the mutation score based on the number of killed mutants.
3. Report the mutation score to the user, providing a metric for test effectiveness.