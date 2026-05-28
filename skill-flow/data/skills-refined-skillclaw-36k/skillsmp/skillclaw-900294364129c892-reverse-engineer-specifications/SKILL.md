---
name: reverse-engineer-specifications
description: Use this skill to extract and document specifications from source code, particularly for legacy or undocumented systems.
---

# Skill body

## Overview
This skill allows you to reverse-engineer specifications from existing source code, translating technical implementations into user-centric business specifications. It is particularly useful for legacy systems or when documentation is lacking.

## Step-by-Step Instructions

### 1. Context Analysis
- Ask the user which **directories or files** should be analyzed.
- Inquire about any **existing design documents** or issue descriptions for reference (for drift detection).
  - If no references are provided, skip the drift detection phase.

### 2. Source Investigation
- Perform a deep investigation of the provided source code.
- Focus on extracting **Business Logic** over **Code Structure**:
  - **User Flows**: Identify what users are trying to achieve.
  - **Business Rules**: Determine constraints enforced by the system (e.g., "Status must be Active").
  - **State Transitions**: Analyze how entity states change from a business perspective.
  - **Edge Cases**: Document how the system handles boundary conditions.
  - **Error Handling**: Review how errors are managed.

### 3. Drift Detection (if applicable)
- Identify discrepancies between the code and any existing documentation.

### 4. Behavior Extraction
- List user scenarios, business rules, and edge cases.
- Log uncertainties that require human confirmation (TBCs).

### 5. Spec Generation
- Fill out the `specification.template.md` using the extracted information.
- Use EARS format for documenting specifications.

### 6. Final Review
- Verify the generated specifications against the code to ensure accuracy.

## Deliverables
Save the final specifications to `specs/{project_name}_reverse_spec.md`, including:
- Technology stack
- Module structure
- Observed requirements
- Non-functional characteristics
- Inferred acceptance criteria
- Uncertainties section
- Recommendations

## Important Notes
- Ground all observations in actual code evidence.
- Explore thoroughly before writing specifications.
- Distinguish verified facts from inferences.
- Document all uncertainties with code references.
- Analyze security patterns and review error handling mechanisms.
- Avoid making assumptions without code verification or skipping comprehensive exploration.