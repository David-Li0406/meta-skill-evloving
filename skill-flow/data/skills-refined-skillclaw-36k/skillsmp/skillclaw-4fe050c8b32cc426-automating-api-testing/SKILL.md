---
name: automating-api-testing
description: Use this skill when you need to automate API endpoint testing, including request generation, validation, and comprehensive test coverage for REST and GraphQL APIs.
---

# Skill body

## Overview

This skill automates the generation and execution of comprehensive API tests for REST and GraphQL endpoints. It ensures thorough validation, covers various authentication methods, and performs contract testing against OpenAPI specifications.

## How It Works

1. **Analyze API Definition**: The skill parses the provided API definition (e.g., OpenAPI/Swagger file, code files) or infers it from usage.
2. **Generate Test Cases**: Based on the API definition, it creates test cases covering different scenarios, including CRUD operations, authentication, and error handling.
3. **Execute Tests and Validate Responses**: The skill executes the generated tests and validates the responses against expected status codes, headers, and body structures.

## When to Use This Skill

This skill activates when you need to:
- Generate comprehensive API tests for REST endpoints.
- Create GraphQL API tests covering queries, mutations, and subscriptions.
- Validate API contracts against OpenAPI/Swagger specifications.
- Test API authentication flows, including login, refresh, and protected endpoints.

## Examples

### Example 1: Generating REST API Tests

User request: "Generate API tests for the user management endpoints in src/routes/users.js"

The skill will:
1. Analyze the user management endpoints in the specified file.
2. Generate a test suite covering CRUD operations (create, read, update, delete) for user resources.

### Example 2: Creating GraphQL API Tests

User request: "Create GraphQL API tests for the product queries and mutations"

The skill will:
1. Analyze the product queries and mutations in the GraphQL schema.
2. Generate tests to verify the functionality and data integrity of these operations.

## Best Practices

- **API Definition**: Provide a clear and accurate API definition (e.g., OpenAPI/Swagger file) to ensure effective test generation.