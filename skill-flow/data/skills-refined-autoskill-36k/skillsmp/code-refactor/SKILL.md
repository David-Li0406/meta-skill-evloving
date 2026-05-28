---
name: code-refactor
description: Orchestrates the comprehensive revision and standardization of the codebase. Use when rebuilding components, cleaning up technical debt, or ensuring code aligns with "Day 1" project standards.
---

# Code Refactor Skill

This skill is the "Master Architect" for THE LOST+UNFOUNDS. It ensures that any code changes move the project toward a cleaner, more modular, and standard-compliant state.

## Refactoring Workflow

### 1. Discovery & Alignment
Before touching code, identify which "Engine" skills are relevant:
- **UI/UX**: Consult `@noir-design`.
- **Data/Logic**: Consult `@infra-ops`.
- **Feature Specific**: Consult `@blog-engine` or `@outreach-engine`.

### 2. The "Day 1" Standard Checklist
Every refactored component must meet these criteria:
- **Modular CSS**: No inline styles. Use the utility classes and variables defined in `@noir-design`.
- **Type Safety**: Proper TypeScript interfaces. Avoid `any`. Move shared types to `src/types`.
- **Separation of Concerns**: 
  - UI logic goes in components.
  - Business logic goes in `src/utils` or `src/lib`.
  - API calls go through centralized handlers.
- **Left-Alignment**: Strictly enforce left-aligned text for all body content.
- **Error Handling**: Use established try/catch patterns with helpful error surfacing.

### 3. Execution Pattern
1. **Analyze**: List the violations of current standards in the file.
2. **Propose**: Detail the new structure (e.g., "Extracting logic to a hook").
3. **Execute**: Implement changes in a way that minimizes disruption.
4. **Verify**: Ensure the component still functions and looks better.

## When to use this skill
- When converting old components to the new Skill-based architecture.
- When fixing "legacy" rules that have been moved to skills.
- When performing a "Day 1" reset on a specific directory.
