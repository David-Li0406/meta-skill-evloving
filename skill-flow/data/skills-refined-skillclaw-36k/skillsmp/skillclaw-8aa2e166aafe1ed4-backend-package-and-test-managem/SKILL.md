---
name: backend-package-and-test-management
description: Use this skill when you need to manage package installations and create test code for a Python/FastAPI backend project.
---

# Skill body

## Overview

This skill provides guidelines for adding packages to a Python/FastAPI backend project and generating test code, including unit tests, integration tests, and end-to-end tests.

## Part 1: Adding Packages

### Instructions

1. **Check Current Directory**
   - Ensure you are in the `src/api` directory.

2. **Add Packages**
   - Use the command `uv add <package-name>` to add a regular dependency.
   - For development dependencies, use `uv add -D <package-name>`.

3. **Verify Package Addition**
   - Confirm that the package is listed in `pyproject.toml`.
   - Check that `uv.lock` has been updated.

### Important Note
⚠️ **Do not edit `pyproject.toml` directly.** Always use the `uv add` command to maintain dependency integrity.

## Part 2: Creating Test Code

### Test Implementation Guidelines

1. **Understand Testing Principles**
   - Focus on manageable coverage, primarily testing normal cases.
   - Limit abnormal case tests to the essentials.

2. **Use API for Test Data Creation**
   - Create test data through API endpoints instead of directly inserting into the database.
   - Utilize fixtures like `create_transaction` and `create_dividend`.

3. **Database and Transactions**
   - Each test runs in an isolated PostgreSQL database (using testcontainers).
   - Use the `db_session` fixture for transactions with automatic rollback after tests.

4. **Authentication**
   - Use `auth_token` for general users and `auth_admin_token` for admin users in API requests.

5. **Mock External APIs**
   - Automatically mock external APIs for all tests using the `mock_external_apis` fixture.

6. **Setup Test Data Fixtures**
   - Define fixtures for necessary test data, such as stock data and portfolio data.

### Running Tests
- Execute tests using `uv run pytest <test_file>` to ensure they function correctly.

By following these steps, you can effectively manage package installations and create robust test code for your Python/FastAPI backend project.