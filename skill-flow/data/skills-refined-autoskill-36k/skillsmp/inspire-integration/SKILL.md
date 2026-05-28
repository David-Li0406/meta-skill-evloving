---
name: inspire-integration
description: Inspire team API standards, integration patterns, and third-party service documentation. Use when building integrations or working with external services.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Integration Context

When this skill is activated, load the following integration documentation:

## Required Context Files

Read these files to understand the Inspire team's integration patterns:

1. **API Standards**: `./references/api-standards.md`
   - REST conventions
   - Request/response formats
   - Authentication patterns

2. **Integration Patterns**: `./references/integration-patterns.md`
   - Event-driven patterns
   - Synchronous vs async
   - Error handling

3. **Third-Party Services**: `./references/third-party-services.md`
   - External service inventory
   - Integration details
   - Rate limits and constraints

## Instructions

Before responding to integration questions:
1. Use the Read tool to load relevant files above
2. Follow the team's API standards
3. Reference integration patterns for consistency

## When to Load This Context

- Building new API endpoints
- Integrating with external services
- Designing service communication
- Reviewing integration code
