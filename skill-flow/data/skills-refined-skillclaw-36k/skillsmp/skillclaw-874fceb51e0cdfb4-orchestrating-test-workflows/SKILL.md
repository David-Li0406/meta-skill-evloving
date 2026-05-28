---
name: orchestrating-test-workflows
description: Use this skill when you need to manage and execute complex test workflows, optimizing test execution through dependency management, parallel execution, and smart test selection based on code changes.
---

# Skill body

## Overview

This skill empowers Claude to orchestrate complex test suites efficiently using the test-orchestrator plugin. It handles test dependencies, executes tests in parallel, and intelligently selects tests to run, resulting in faster and more reliable testing processes.

## How It Works

1. **Workflow Definition**: Define the test workflow using the plugin, specifying dependencies between tests.
2. **Parallelization**: Identify independent tests and execute them in parallel to reduce overall execution time.
3. **Smart Selection**: Select only the affected tests to run based on recent code changes, minimizing unnecessary execution.

## When to Use This Skill

Activate this skill when you need to:
- Optimize test execution time.
- Manage dependencies between tests.
- Run only relevant tests after code changes.

## Examples

### Example 1: Optimizing Regression Testing

User request: "Orchestrate the regression tests for the user authentication module after the recent code changes."

The skill will:
1. Use the test-orchestrator plugin to identify the tests affected by the changes in the user authentication module.
2. Execute those tests in parallel, respecting any dependencies.

### Example 2: Setting up a CI/CD Pipeline

User request: "Set up a test workflow for the CI/CD pipeline that runs unit tests, integration tests, and end-to-end tests with appropriate dependencies."

The skill will:
1. Define a test workflow using the test-orchestrator plugin, specifying the order and dependencies between the different test suites (unit, integration, end-to-end).
2. Configure the pipeline to trigger the orchestrated test execution upon code commits.

## Best Practices

- **Dependency Mapping**: Clearly define dependencies between tests to ensure correct execution order.
- **Granularity**: Break down large test suites into smaller, manageable tests to enhance parallel execution efficiency.