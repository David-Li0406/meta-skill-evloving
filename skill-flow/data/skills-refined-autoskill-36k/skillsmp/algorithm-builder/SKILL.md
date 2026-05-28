---
name: algorithm-builder
description: Guide for building professional, high-accuracy algorithms with a focus on documentation verification and error-free execution. Use this skill when the user asks for "algorithms", "complex logic", "robust functions", or explicitly mentions "no errors" and "check docs".
---

# Algorithm Builder

This skill enforces a disciplined approach to creating professional algorithms, ensuring accuracy through documentation verification and robust error handling.

## Workflow

### 1. Research & Verification (MANDATORY)

**Before writing any code:**

1.  **Consult Documentation**: Use `context7` or `search_web` to find the official documentation for relevant libraries (e.g., standard libraries, third-party packages).
    - _Do not guess_ API signatures or behaviors.
    - _Do not rely_ solely on pre-training knowledge for critical logic.
2.  **Verify Assumptions**: Confirm edge case behaviors (e.g., empty inputs, nulls, boundary values) from authoritative sources.

### 2. Design & Strategy

1.  **Pseudocode**: Briefly outline the algorithm steps in comments or a scratchpad.
2.  **Edge Case Identification**: List at least 3 potential failure modes or edge cases (e.g., "Input array is empty", "Network timeout", "Invalid date format").
3.  **Complexity Analysis**: Briefly note time/space complexity if ensuring performance is critical.

### 3. Implementation

1.  **Type Safety**: Use strong typing (TypeScript interfaces, Python type hints) to enforce data structures.
2.  **Input Validation**: specific checks at the start of the function to reject invalid state early (Programming by Contract).
3.  **Error Handling**:
    - Use `try/catch` blocks around risky operations.
    - Throw descriptive custom errors rather than generic ones.
    - Ensure cleanup (e.g., closing file handles) in `finally` blocks.
4.  **Modularity**: Break down complex logic into smaller, testable helper functions.

### 4. Verification

1.  **Happy Path**: Verify the standard use case works.
2.  **Edge Cases**: strict check against the identified failure modes.
3.  **Self-Correction**: If an error occurs, _stop_, re-read the error message, consult docs again, and fix. Do not blindly retry.
