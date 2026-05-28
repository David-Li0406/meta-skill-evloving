---
name: automating-api-testing
description: Use this skill to automate API endpoint testing, including request generation, validation, and comprehensive test coverage for REST and GraphQL APIs.
---

## Overview

This skill empowers the AI to automatically generate and execute comprehensive API tests for REST and GraphQL endpoints. It ensures thorough validation, covers various authentication methods, and performs contract testing against OpenAPI specifications.

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

## Prerequisites

Before using this skill, ensure you have:
- API definition files (OpenAPI/Swagger, GraphQL schema, or endpoint documentation).
- Base URL for the API service (development, staging, or test environment).
- Authentication credentials or API keys if endpoints require authorization.
- Testing framework installed (Jest, Mocha, Supertest, or equivalent).
- Network connectivity to the target API service.

## Instructions

### Step 1: Analyze API Definition
Examine the API structure and endpoints:
1. Use the Read tool to load OpenAPI/Swagger specifications.
2. Identify all available endpoints, HTTP methods, and request/response schemas.
3. Document authentication requirements and rate limiting constraints.
4. Note any deprecated endpoints or breaking changes.

### Step 2: Generate Test Cases
Create comprehensive test coverage:
1. Generate CRUD operation tests (Create, Read, Update, Delete).
2. Add authentication flow tests (login, token refresh, logout).
3. Include edge case tests (invalid inputs, boundary conditions, malformed requests).
4. Create contract validation tests against OpenAPI schemas.
5. Add performance tests for critical endpoints.

### Step 3: Execute Test Suite
Run automated API tests:
1. Use the appropriate testing framework to execute test files.
2. Validate HTTP status codes match expected responses (200, 201, 400, 401, 404, 500).
3. Verify response headers (Content-Type, Cache-Control, CORS headers).
4. Validate response body structure against schemas using JSON Schema validation.
5. Test authentication token expiration and renewal flows.

### Step 4: Generate Test Report
Document results in a specified directory:
- Test execution summary with pass/fail counts.
- Coverage metrics by endpoint and HTTP method.
- Failed test details with request/response payloads.
- Performance benchmarks (response times, throughput).
- Contract violation details if schema mismatches detected.

## Best Practices

- **API Definition**: Provide a clear and accurate API definition for optimal test generation.
- **Authentication Details**: Specify the authentication method and credentials required to access the API endpoints.
- **Contextual Information**: Provide context about the API's purpose and usage to guide the test generation process.
- Test against non-production environments to avoid data corruption.
- Use test data factories to create consistent test fixtures.

## Error Handling

Common issues and solutions:
- **Connection Refused**: Verify service is running and check network connectivity.
- **Authentication Failures**: Ensure API keys are valid and not expired.
- **Schema Validation Errors**: Update OpenAPI specification to match actual API behavior.
- **Timeout Errors**: Increase timeout for slow endpoints and investigate performance issues.

## Examples

### Example 1: Generating REST API Tests
User request: "Generate API tests for the user management endpoints in `src/routes/users.js`."
- The skill will analyze the user management endpoints and generate a test suite covering CRUD operations.

### Example 2: Creating GraphQL API Tests
User request: "Create GraphQL API tests for the product queries and mutations."
- The skill will analyze the product queries and mutations in the GraphQL schema and generate tests to verify functionality and data integrity.

## Integration

This skill can integrate with other plugins to retrieve API definitions from various sources, such as code repositories or API gateways. It can also be combined with reporting tools to generate detailed test reports and dashboards.