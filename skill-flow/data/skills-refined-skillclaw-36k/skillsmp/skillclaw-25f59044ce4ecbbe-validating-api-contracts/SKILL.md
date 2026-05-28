---
name: validating-api-contracts
description: Use this skill when you need to generate contract tests, validate API responses, or check backward compatibility using consumer-driven contract testing and OpenAPI validation.
---

# Skill body

## Overview

This skill enables Claude to generate and validate API contracts, ensuring compatibility between API providers and consumers. It leverages Pact for consumer-driven contract testing and OpenAPI validation for specification compliance.

## How It Works

1. **Generating Contract Tests**: Claude creates Pact consumer tests based on API usage, generating provider verification tests and building OpenAPI contract validators.
2. **Validating Contracts**: The skill verifies if API responses match the defined contracts.
3. **Checking Compatibility**: It checks for backward compatibility to identify breaking changes in the API.

## When to Use This Skill

This skill activates when you need to:
- Generate contract tests for an API.
- Validate API responses against existing contracts.
- Identify breaking changes in an API.

## Examples

### Example 1: Generating Pact Contracts

User request: "Generate contract tests for my API using Pact."

The skill will:
1. Analyze the API and generate Pact consumer contracts.
2. Create provider verification tests based on the contracts.

### Example 2: Validating an OpenAPI Specification

User request: "Validate my API against the OpenAPI specification."

The skill will:
1. Validate the API against the provided OpenAPI specification.
2. Report any discrepancies or violations of the specification.

## Best Practices

- **Clarity**: Be specific when requesting contract generation or validation, providing relevant API details.
- **Completeness**: Ensure that your OpenAPI specifications are up-to-date for accurate validation.
- **Context**: Provide context about the consumer and provider roles when using Pact.

## Integration

This skill can be integrated with other testing and deployment tools in the Claude Code ecosystem to automate contract verification as part of a CI/CD pipeline.