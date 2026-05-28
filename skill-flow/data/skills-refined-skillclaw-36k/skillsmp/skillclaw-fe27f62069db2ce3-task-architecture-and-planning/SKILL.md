---
name: task-architecture-and-planning
description: Use this skill when you need to analyze a task's requirements, design its architecture, and create a structured implementation plan.
---

# Skill body

## Overview

This skill combines task analysis, architectural design, and planning to ensure a comprehensive approach to software development. It is useful for defining requirements, designing system architecture, and creating actionable task lists.

## Steps

### 1. Task Analysis

- **Understand the Essence**: Identify the core purpose of the task beyond surface-level requests.
  - Example: Instead of "fix this bug," determine the underlying issue and expected outcomes.

- **Estimate Task Scale**: Classify the task based on the number of files involved.
  - Small: 1-2 files
  - Medium: 3-5 files
  - Large: 6 or more files

- **Identify Task Type**: Determine if the task is implementation, fix, refactoring, design, or quality assurance.

### 2. Architectural Design

- **Define Architecture Principles**: Choose appropriate architectural patterns based on project requirements.
- **Data Flow Principles**: Ensure a single source of truth for data and prioritize structured data.
- **Security Considerations**: Manage sensitive information through environment variables and avoid logging confidential data.

### 3. Planning

- **Create a Steering Document**: For significant changes, document the requirements, design, and task list.
  - Directory structure:
    ```
    .steering/
    └── YYYYMMDD-feature-name/
        ├── requirements.md
        ├── design.md
        └── tasklist.md
    ```

- **Task List Management**: Use the task list to track progress and update it as tasks are completed.
  - Mark tasks as complete and add new tasks as they arise.

### 4. Implementation Approach

- **Outline Implementation Steps**: Provide a high-level overview of the implementation process.
- **Document Design Decisions**: Record architectural decisions and their rationale.
- **Review and Feedback**: After implementation, gather feedback and document any necessary adjustments.

### 5. Final Documentation

- **Compile Results**: Summarize findings and decisions in a structured format for future reference.
- **Ensure Clarity**: Use clear language and avoid technical jargon to make documentation accessible.

## Output Format

The final output should include:
- Task analysis summary
- Architectural design details
- Implementation plan with a task list
- Any identified risks or dependencies

## Notes

- Always validate requirements with stakeholders before proceeding.
- Maintain a focus on quality and security throughout the process.
- Regularly review and update documentation to reflect changes and lessons learned.