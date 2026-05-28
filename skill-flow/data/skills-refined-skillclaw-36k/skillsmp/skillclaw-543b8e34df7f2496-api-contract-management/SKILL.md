---
name: api-contract-management
description: Use this skill when you need to write or review API contracts to ensure they meet the required standards and align with project specifications.
---

# API Contract Management

This skill assists in both writing and reviewing API contracts, ensuring they are well-defined, consistent, and aligned with project requirements. It covers the entire lifecycle from contract creation to review.

## Core Principles

1. **Contract as a Source of Truth**: All development must reference the contract version; no new interfaces should be added without proper documentation.
2. **Evidence-Based**: All contracts must be based on existing documentation; if evidence is lacking, ask for clarification.
3. **Reuse Existing Interfaces**: Prioritize the use of existing APIs and modules to avoid redundancy.
4. **Compatibility First**: Default to backward compatibility; any breaking changes must be clearly marked with a migration plan.
5. **No Implementation Details**: Focus solely on the contract; do not include internal architecture, database details, or implementation specifics.
6. **Decision Support**: Provide options and implications without making decisions on behalf of stakeholders.

## Writing an API Contract

### Steps to Follow

1. **Context Collection**
   - Scan existing PRD, API specifications, and service documentation.
   - Confirm the latest approved baseline with stakeholders.

2. **Boundary and Ownership Confirmation**
   - Verify service/module boundaries and data ownership.
   - Identify primary consumers and calling directions.

3. **Contract Type Selection**
   - Determine the type of contract (e.g., HTTP, GraphQL, gRPC) and confirm the output format.

4. **Contract Drafting**
   - Generate the contract based on selected templates.
   - Create a mapping table from PRD to contract.
   - Clearly indicate compatibility and versioning strategies.

5. **Consistency Check**
   - Ensure 100% coverage of PRD requirements in the contract.
   - Check for conflicts or duplicates with existing contracts.
   - Validate compatibility and versioning strategies.

## Reviewing an API Contract

### Review Process

1. **Baseline Collection**
   - Confirm the accessibility of the contract and its alignment with the PRD.
   - Scan for existing contracts and confirm the contract type.

2. **Gate Checks**
   - **Gate 1**: Verify baseline references, ownership, and coverage.
   - **Gate 2**: Check for completeness and required fields in the contract.
   - **Gate 3**: Detect any drift from the PRD and conflicts with existing interfaces.
   - **Gate 4**: Review compatibility and evolution strategies.

3. **Final Reporting**
   - Summarize findings and provide a review report or approval certificate.

## Contract Content Requirements

### Must Include

- Basic contract information: name, version, status, owner, consumers, PRD reference.
- Scope and boundaries: coverage capabilities, data ownership.
- Interface definitions: paths, request/response formats, error handling.
- Security and permissions: authentication and authorization details.
- Compatibility and versioning strategies: upgrade and deprecation rules.
- Non-functional constraints: SLOs, idempotency, rate limiting.

### Must Not Include

- Internal design details, deployment topology, or database specifics.
- Specific algorithms or retry parameters.
- UI interaction details or implementation code.

This skill provides a comprehensive framework for managing API contracts effectively, ensuring clarity and alignment across teams.