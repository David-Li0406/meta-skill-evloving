---
name: overnight-development
description: Use this skill when you want to automate software development overnight, ensuring all code changes are fully tested and meet quality standards through test-driven development (TDD) using Git hooks.
---

# Overnight Development

## Overview

This skill automates software development overnight by leveraging Git hooks to enforce test-driven development (TDD). It ensures that all code changes are fully tested and meet specified quality standards before being committed. This approach allows Claude to work autonomously, building new features, refactoring existing code, or fixing bugs while adhering to a rigorous TDD process.

## Core Capabilities

- Enforces test-driven development (TDD) using Git hooks.
- Automates debugging and code fixing until all tests pass.
- Tracks progress and logs activities during overnight sessions.
- Supports flexible configuration for various testing frameworks and languages.
- Provides guidance and support through the `overnight-dev-coach` agent.

## Workflow

### Phase 1: Project Setup and Configuration

To prepare the project for overnight development:

1. **Verify Prerequisites:** Ensure the project is a Git repository, has a configured test framework, and includes at least one passing test.
    ```bash
    git init
    npm install --save-dev jest # Example for Node.js
    ```

2. **Install the Plugin:** Add the Claude Code Plugin marketplace and install the `overnight-dev` plugin.
    ```bash
    /plugin marketplace add jeremylongshore/claude-code-plugins
    /plugin install overnight-dev@claude-code-plugins-plus
    ```

3. **Run Setup Command:** Execute the `/overnight-setup` command to create necessary Git hooks and configuration files.
    ```bash
    /overnight-setup
    ```

### Phase 2: Task Definition and Planning

To define the task for the overnight session:

1. **Define a Clear Goal:** Specify a clear and testable goal for the overnight session, such as "Build user authentication with JWT (90% coverage)."
    ```text
    Task: Build user authentication with JWT (90% coverage).
    ```

2. **Initiate the Overnight Session:** Start the overnight development process with the defined goal.
    ```bash
    /overnight-start "Build user authentication with JWT (90% coverage)."
    ```

### Phase 3: Monitoring and Completion

1. **Monitor Progress:** Check logs and progress reports generated during the overnight session.
2. **Review Results:** After completion, review the results to ensure all tests have passed and the code meets quality standards.

This skill is perfect for automating development tasks while you sleep, ensuring high-quality code through rigorous testing.