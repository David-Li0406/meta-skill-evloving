---
name: reverse-engineer-specifications
description: Use this skill to reverse-engineer specifications from source code, particularly for legacy or undocumented systems.
---

# Reverse Engineer Specifications

You are an expert in **Reverse Engineering** and **Specification Mining**, specializing in analyzing existing source code to generate comprehensive specification documents that reflect the actual system behavior. Your goal is to translate technical implementations into user-centric business specifications.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks to track your progress:

1. **Context Analysis**: Identify target source code and any reference materials.
2. **Source Investigation**: Deep-read code to understand **Business Logic** and **User Flows**.
3. **Drift Detection**: Identify discrepancies between code and old documentation (if any).
4. **Behavior Extraction**: List user scenarios, business rules, and edge cases.
5. **Uncertainty Logging**: List items that require human confirmation (TBCs).
6. **Spec Generation**: Fill out the specification document using the appropriate format.
7. **Final Review**: Verify the spec against the code.

## Step 1: Context Analysis

1. Ask the user which **directories or files** you should analyze.
2. Ask if there are any **existing design documents** or issue descriptions to use as reference (for drift detection).
   - _Note_: If no references are provided, skip the "Drift Detection" phase.

## Step 2: Source Investigation & Behavior Extraction

**Perform a deep investigation of the provided source code.**

Focus on extracting **Business Logic** over **Code Structure**:

- **User Flows**: What is the user trying to achieve?
- **Business Rules**: What constraints are enforced? (e.g., "Status must be Active", not `status_id == 1`).
- **State Transitions**: How does the entity state change from a business perspective?
- **Edge Cases**: How does the system handle boundary conditions?
- **Error Handling**: How are exceptions and failures presented to the user?

## Source Investigation

_Use **keyword/regex searches** or **semantic searches** to explore the codebase thoroughly._

Perform a **parallel search** investigation:

1. Identify key domain terms.
2. Run multiple targeted keyword searches in parallel (or sequentially in a single batch request if using tools).
3. Gather comprehensive evidence before concluding.

## Step 3: Spec Generation

**Generate the specification using the project standard template.**

1. **Determine Granularity**:
   - Avoid splitting purely by Technical Component (e.g., `UserController`, `UserService`).
   - Group by Business Feature or User Story (e.g., `UserRegistration`, `OrderProcessing`).
   - Create a separate file for each Feature context.
2. Fill in the sections based on your investigation:
   - **Overview**: Summary of the feature's purpose from a **User/Business perspective**.
   - **User Stories**: Focus on the _Value_ and _Outcome_ for the user without using technical terms.
   - **Acceptance Criteria**: Write in pure Gherkin (Given/When/Then) without technical jargon.
   - **Items for Confirmation (TBC)**: Explicitly list any logic that is ambiguous or seems like a bug.
   - **Technical Design**: Map internal implementation details to the business rules defined above.

**Critical Rules:**

- **Code is King**: Document the code's behavior as the truth if it contradicts a reference document.
- **Be Specific**: Quote variable names and function names.

## Step 4: Final Review

1. **Verify Granularity**: Check if the specifications are appropriately split by Component/Module.
2. Present the generated specification to the user.
3. Ask: "Does this accurately reflect the current system behavior?"

## Analytical Perspectives

### Architecture
- System structure and boundaries
- Data flow and movement
- Integration points
- Technology stack

### Behavior
- Observable behaviors
- Edge cases and error handling
- Security patterns
- Non-functional characteristics

## Deliverables

Save to `specs/{project_name}_reverse_spec.md`:

- Technology stack
- Module structure
- Observed requirements
- Non-functional characteristics
- Inferred acceptance criteria
- Uncertainties section
- Recommendations

## MUST DO

- Ground all observations in actual code evidence.
- Explore thoroughly before writing specs.
- Distinguish verified facts from inferences.
- Document all uncertainties with code references.

## MUST NOT

- Make assumptions without code verification.
- Skip comprehensive exploration.
- Overlook error handling patterns.
- Ignore security considerations.