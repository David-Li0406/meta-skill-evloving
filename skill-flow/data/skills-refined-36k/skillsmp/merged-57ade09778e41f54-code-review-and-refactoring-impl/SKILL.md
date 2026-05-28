---
name: code-review-and-refactoring-implementation
description: Use this skill to orchestrate the processes of code review and refactoring, ensuring high-quality code through structured analysis, execution, and closure.
---

# Code Review and Refactoring Implementation (Orchestrator)

This skill orchestrates the processes of code review and refactoring, ensuring that feedback is addressed and technical debt is repaid through a structured workflow. It utilizes the `task-management` framework to facilitate constructive dialogue and high-quality code improvements.

## Role Definition
You are a **Code Quality Lead**, responsible for enhancing the system's quality by addressing reviewer feedback and improving code structure.

## Prerequisites
- There must be existing change requests or comments on the pull request (PR) that require addressing.
- The code targeted for refactoring must have existing tests to ensure functionality is maintained.

## Procedure

### 1. Planning Phase
- **Action:**
  1. Start task management.
     `activate_skill{name: "task-management"}`
  2. Analyze feedback or code smells and set SMART goals.
     - For code review: 
       `activate_skill{name: "code-review-analysis"}`
       * Classify comments into "Must Fix," "Discuss," and "Suggestion" categories.
     - For refactoring:
       `activate_skill{name: "objective-analysis"}`
       `activate_skill{name: "objective-setting"}`
       * Identify issues in the code (complexity, coupling, duplication) and define the ideal state post-refactoring.
  3. Create and register a Todo list.
     - For code review:
       * Develop a plan in `.gemini/todo.md` that includes branch switching, tasks for each comment, and final checks.
     - For refactoring:
       `activate_skill{name: "code-refactoring-planning"}`
       * Outline safe refactoring steps in `.gemini/todo.md`, ensuring each step allows for passing tests.

### 2. Execution Phase
- **Action:**
  - Follow the task management cycle to address items in the Todo list.
  - **Fixes:**
    `activate_skill{name: "tdd-refactoring"}`
    * Implement code changes for "Must Fix" items while ensuring existing tests are not broken and adding or modifying tests as necessary.
  - **Responses:**
    * Provide technical justifications for "Discuss" and "Suggestion" comments, focusing on constructive dialogue.
  - **Refactor Cycle:**
    * Execute code changes while frequently running tests to ensure behavior remains unchanged.
  - **Compliance Check:**
    * Verify that the new structure adheres to architectural principles.

### 3. Closing Phase
- **Action:**
  - Follow the completion flow of task management.
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    * Ensure all feedback has been addressed and that the modified code meets quality standards (Lint/Test).
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    * Document learnings from the review and refactoring processes, including improvements in coding standards and design.

## Definition of Done
- All feedback has been addressed with either fixes or responses.
- The modified code passes all tests and meets quality standards.
- The PR has been updated and notifications to reviewers have been completed.