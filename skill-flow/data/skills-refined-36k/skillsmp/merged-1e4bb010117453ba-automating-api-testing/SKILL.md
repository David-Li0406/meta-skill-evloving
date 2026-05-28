---
name: automating-api-testing
description: Use this skill to automate API endpoint testing, including request generation, validation, and comprehensive test coverage for REST and GraphQL APIs.
---

## Overview

This skill empowers the AI to automatically generate and execute comprehensive API tests for REST and GraphQL endpoints. It ensures thorough validation, covers various authentication methods, and performs contract testing against OpenAPI specifications.

## Prerequisites

Before using this skill, ensure you have:
- API definition files (OpenAPI/Swagger, GraphQL schema, or endpoint documentation)
- Base URL for the API service (development, staging, or test environment)
- Authentication credentials or API keys if endpoints require authorization
- Testing framework installed (Jest, Mocha, Supertest, or equivalent)
- Network connectivity to the target API service

## How It Works

1. **Analyze API Definition**: The skill parses the provided API definition or infers it from usage, identifying all available endpoints, HTTP methods, and request/response schemas.
2. **Generate Test Cases**: Based on the API definition, it creates test cases covering different scenarios, including CRUD operations, authentication flows, edge cases, and contract validation against OpenAPI schemas.
3. **Execute Tests and Validate Responses**: The skill executes the generated tests and validates the responses against expected status codes, headers, and body structures.
4. **Generate Test Report**: Document results, including test execution summary, coverage metrics, and performance benchmarks.

## When to Use This Skill

This skill activates when you need to:
- Generate comprehensive API tests for REST endpoints.
- Create GraphQL API tests covering queries, mutations, and subscriptions.
- Validate API contracts against OpenAPI/Swagger specifications.
- Test API authentication flows, including login, refresh, and protected endpoints.

## Examples

### Example 1: Generating REST API Tests

User request: "Generate API tests for the user management endpoints in `<input_path>`"

The skill will:
1. Analyze the user management endpoints in the specified file.
2. Generate a test suite covering CRUD operations (create, read, update, delete) for user resources.

### Example 2: Creating GraphQL API Tests

User request: "Create GraphQL API tests for the product queries and mutations"

The skill will:
1. Analyze the product queries and mutations in the GraphQL schema.
2. Generate tests to verify the functionality and data integrity of these operations.

## Best Practices

- **API Definition**: Provide a clear and accurate API definition for optimal test generation.
- **Authentication Details**: Specify the authentication method and credentials required to access the API endpoints.
- **Contextual Information**: Provide context about the API's purpose and usage to guide the test generation process.

## Error Handling

Common issues and solutions:
- **Connection Refused**: Verify service is running and check network connectivity.
- **Authentication Failures**: Ensure API keys are valid and check scope permissions.
- **Schema Validation Errors**: Update OpenAPI specification to match actual API behavior.
- **Timeout Errors**: Increase timeout for slow endpoints and investigate performance issues.

## Resources

### API Testing Frameworks
- Supertest for Node.js HTTP assertion testing
- REST-assured for Java API testing
- Postman/Newman for collection-based API testing
- Pact for contract testing and consumer-driven contracts

### Validation Libraries
- Ajv for JSON Schema validation
- OpenAPI Schema Validator for spec compliance
- Joi for Node.js schema validation
- GraphQL Schema validation tools

## Integration

This skill can integrate with other plugins to retrieve API definitions from various sources, such as code repositories or API gateways. It can also be combined with reporting tools to generate detailed test reports and dashboards.